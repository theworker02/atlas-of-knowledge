# Local generative training

`scripts/train_generative_lora.py` creates a LoRA adapter for `distilgpt2` from
the deterministic Atlas train split. It uses question-answer, definition, and
reasoning fields as a causal-language-model objective and evaluates against a
separate validation sample. It is designed to resume from periodic checkpoints.

Run it in a Linux environment with Python, PyTorch, `transformers`, `datasets`,
and `peft` installed:

```bash
python3 scripts/train_generative_lora.py --version 1.1.0 --max-steps 2000
```

The three-size free CPU family is run sequentially to avoid resource contention:

```bash
bash scripts/train_generative_family.sh 1.1.0
```

It trains a small `distilgpt2` adapter (~83M base parameters), a medium
`gpt2-medium` adapter (~355M), and a large `gpt2-large` adapter (~774M). The
models write under `artifacts/generative/v<version>/`; the release packager copies
them into `models/generative/` in an Atlas Hugging Face dataset release only after
their artifacts are available and evaluated. To package trained artifacts from an
earlier data revision into a new release tag, pass `--model-version` to the
packager explicitly.
