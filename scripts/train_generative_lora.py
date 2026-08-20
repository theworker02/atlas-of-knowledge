#!/usr/bin/env python3
"""Train a resumable CPU LoRA adapter for a small causal language model.

This runner is deliberately conservative: it trains a generative adapter on Atlas
instruction records, holds out validation examples, writes periodic checkpoints,
and never publishes an artifact by itself. Publishing happens only after metrics
and the generated model card have been reviewed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

ROOT = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def instruction(record: dict) -> str:
    question = record["questions"][0]
    answer = record["answers"][0]
    return (
        "### Instruction\n"
        f"{question}\n\n"
        "### Response\n"
        f"{answer}\n\n"
        "### Supporting context\n"
        f"Concept: {record['concept']}\n"
        f"Definition: {record['definition']}\n"
        f"Reasoning: {record['reasoning']}"
    )


def build_dataset(records: list[dict], tokenizer, max_length: int) -> Dataset:
    dataset = Dataset.from_dict({"text": [instruction(record) for record in records]})

    def tokenize(batch: dict) -> dict:
        return tokenizer(batch["text"], truncation=True, max_length=max_length)

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


def write_model_card(output: Path, variant: str, base_model: str, total_parameters: int, trainable_parameters: int, version: str, train_count: int, eval_count: int, metrics: dict) -> None:
    eval_loss = metrics.get("eval_loss")
    loss_text = f"{eval_loss:.4f}" if isinstance(eval_loss, (int, float)) else "not available"
    output.joinpath("README.md").write_text(
        f"""---
license: mit
base_model: {base_model}
library_name: peft
pipeline_tag: text-generation
tags:
- atlas-of-knowledge
- lora
- generative-ai
- education
---
# Atlas {variant} generative LoRA adapter

This is a LoRA adapter for `{base_model}` trained on Atlas of Knowledge v{version}
instruction records. It generates educational responses; it is not a factual authority,
professional advisor, or benchmark of broad educational competence.

## Training

- Training records: {train_count}
- Held-out validation records: {eval_count}
- Validation loss: {loss_text}
- Base-model parameters: {total_parameters:,}
- LoRA trainable parameters: {trainable_parameters:,}
- Hardware: local CPU in WSL; no cloud GPU was used.
- Objective: next-token prediction over question, answer, definition, and reasoning text.

The adapter requires the named base model. Its training data contains systematically
expanded educational records, so outputs can repeat dataset phrasing or overfit to its
structure. Evaluate outputs independently before any consequential use.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune a small generative Atlas LoRA adapter on CPU")
    parser.add_argument("--version", default="1.1.0")
    parser.add_argument("--base-model", default="distilgpt2")
    parser.add_argument("--variant", default="custom")
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--max-steps", type=int, default=2_000)
    parser.add_argument("--save-steps", type=int, default=100)
    parser.add_argument("--eval-samples", type=int, default=256)
    parser.add_argument("--resume-from-checkpoint")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    release = ROOT / "releases" / f"v{args.version}"
    output = args.output_dir or ROOT / "artifacts" / "generative" / f"v{args.version}" / "atlas-distilgpt2-lora"
    train_records = load_jsonl(release / "train.jsonl")
    validation_records = load_jsonl(release / "validation.jsonl")[: args.eval_samples]
    if not train_records or not validation_records:
        raise SystemExit("Expected deterministic train and validation JSONL files in the release directory.")

    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(args.base_model)
    total_parameters = sum(parameter.numel() for parameter in model.parameters())
    model.config.pad_token_id = tokenizer.pad_token_id
    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["c_attn", "c_proj"],
    )
    model = get_peft_model(model, lora)
    trainable_parameters = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
    model.print_trainable_parameters()

    train_dataset = build_dataset(train_records, tokenizer, args.max_length)
    eval_dataset = build_dataset(validation_records, tokenizer, args.max_length)
    training_args = TrainingArguments(
        output_dir=str(output / "checkpoints"),
        max_steps=args.max_steps,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        warmup_ratio=0.03,
        logging_steps=10,
        save_strategy="steps",
        save_steps=args.save_steps,
        eval_strategy="steps",
        eval_steps=args.save_steps,
        save_total_limit=3,
        report_to="none",
        dataloader_num_workers=0,
        use_cpu=True,
        seed=42,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
    metrics = trainer.evaluate()
    output.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(output))
    tokenizer.save_pretrained(str(output))
    metadata = {
        "base_model": args.base_model,
        "variant": args.variant,
        "base_model_parameters": total_parameters,
        "lora_trainable_parameters": trainable_parameters,
        "dataset": "theworker02/atlas-of-knowledge",
        "dataset_revision": f"v{args.version}",
        "train_records": len(train_records),
        "validation_records": len(validation_records),
        "max_length": args.max_length,
        "max_steps": args.max_steps,
        "device": "cpu",
        "metrics": metrics,
    }
    output.joinpath("training-metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    write_model_card(output, args.variant, args.base_model, total_parameters, trainable_parameters, args.version, len(train_records), len(validation_records), metrics)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
