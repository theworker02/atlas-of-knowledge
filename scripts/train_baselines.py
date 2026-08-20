#!/usr/bin/env python3
"""Train transparent Atlas classification baselines from a deterministic release.

These are CPU-friendly supervised baselines, not language-model fine-tunes.  They
are deliberately trained only on ``train.jsonl`` and evaluated on the separate
validation and test splits to avoid reporting training-set performance as quality.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]


def load_records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def text_for(record: dict) -> str:
    """Use learning content, excluding course/discipline fields to prevent label leakage."""
    parts = [
        record["concept"], record["definition"], record["reasoning"],
        *record.get("core_principles", []), *record.get("examples", []),
        *record.get("applications", []), *record.get("common_misconceptions", []),
        *record.get("assumptions", []), *record.get("questions", []),
    ]
    return "\n".join(str(part) for part in parts)


def metrics(pipeline: Pipeline, records: list[dict], label: str) -> dict:
    actual = [record[label] for record in records]
    predicted = pipeline.predict([text_for(record) for record in records])
    return {
        "examples": len(records),
        "accuracy": round(float(accuracy_score(actual, predicted)), 6),
        "macro_f1": round(float(f1_score(actual, predicted, average="macro", zero_division=0)), 6),
        "per_class": classification_report(actual, predicted, output_dict=True, zero_division=0),
    }


def write_card(target: Path, name: str, label: str, version: str, train: list[dict], validation: dict, test: dict) -> None:
    target.joinpath("README.md").write_text(
        f"""---
license: cc-by-4.0
library_name: scikit-learn
tags:
- atlas-of-knowledge
- educational-data
- text-classification
- baseline
---
# {name}

This is a transparent CPU-friendly TF-IDF + logistic-regression baseline trained on
the [Atlas of Knowledge v{version} dataset](https://huggingface.co/datasets/theworker02/atlas-of-knowledge/tree/v{version}).
It predicts the record `{label}` from learning content only; the text builder excludes
the record's course and discipline fields to reduce direct label leakage.

## Evaluation

| Split | Examples | Accuracy | Macro F1 |
| --- | ---: | ---: | ---: |
| Validation | {validation['examples']} | {validation['accuracy']:.4f} | {validation['macro_f1']:.4f} |
| Test | {test['examples']} | {test['accuracy']:.4f} | {test['macro_f1']:.4f} |

The model was fit on {len(train)} records only. Evaluation uses the deterministic Atlas
validation and test splits; it is not a measure of general educational competence.

## Limitations

This is a classification baseline, not a generative model, factual authority, or
recommendation system. The Atlas corpus contains systematically expanded, family-linked
learning records; consequently, held-out split scores can be substantially easier than
classification of independently authored course material. Do not interpret these
results as broad educational understanding or real-world course-classification quality.
""",
        encoding="utf-8",
    )


def train(release: Path, output: Path, version: str) -> list[Path]:
    splits = {name: load_records(release / f"{name}.jsonl") for name in ("train", "validation", "test")}
    produced: list[Path] = []
    for label, slug, title in (
        ("discipline", "atlas-discipline-classifier", "Atlas Discipline Classifier"),
        ("course", "atlas-course-classifier", "Atlas Course Classifier"),
    ):
        target = output / slug
        target.mkdir(parents=True, exist_ok=True)
        pipeline = Pipeline([
            ("vectorizer", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=100_000, sublinear_tf=True)),
            ("classifier", LogisticRegression(max_iter=1_000, class_weight="balanced")),
        ])
        pipeline.fit([text_for(record) for record in splits["train"]], [record[label] for record in splits["train"]])
        validation, test = metrics(pipeline, splits["validation"], label), metrics(pipeline, splits["test"], label)
        joblib.dump(pipeline, target / "model.joblib")
        metadata = {
            "model_name": title, "task": f"predict_{label}", "dataset": "theworker02/atlas-of-knowledge",
            "dataset_revision": f"v{version}", "training_examples": len(splits["train"]),
            "training_labels": dict(sorted(Counter(record[label] for record in splits["train"]).items())),
            "validation": validation, "test": test, "framework": "scikit-learn",
            "algorithm": "TF-IDF (word 1-2 grams) + class-balanced logistic regression",
            "text_fields": "concept, definition, reasoning, principles, examples, applications, misconceptions, assumptions, and questions",
        }
        target.joinpath("metrics.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        target.joinpath("requirements.txt").write_text("scikit-learn==1.9.0\njoblib==1.5.3\n", encoding="utf-8")
        write_card(target, title, label, version, splits["train"], validation, test)
        produced.append(target)
        print(json.dumps({"model": slug, "validation": validation["macro_f1"], "test": test["macro_f1"]}))
    return produced


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Atlas classification baselines")
    parser.add_argument("--version", default="1.0.3")
    parser.add_argument("--release-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "artifacts" / "models")
    args = parser.parse_args()
    release = args.release_dir or ROOT / "releases" / f"v{args.version}"
    if not release.exists():
        raise SystemExit(f"Missing release: {release}. Run `python atlas_cli.py build --version {args.version}` first.")
    train(release, args.output_dir / f"v{args.version}", args.version)


if __name__ == "__main__":
    main()
