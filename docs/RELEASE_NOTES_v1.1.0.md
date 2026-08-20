# Atlas of Knowledge v1.1.0

Released 2026-08-20.

## Complete Hugging Face package

`v1.1.0` is the first Atlas tag that visibly packages the full 20,417-record
dataset together with all Atlas training artifacts. It includes the deterministic
train, validation, and test splits; course, relationship, and graph subsets;
schemas; provenance; validation reports; documentation; and model artifacts.

## Generative LoRA adapters

The package's `models/generative/` directory contains three causal-language-model
LoRA adapters trained exclusively on Atlas training records:

| Variant | Base model | Base parameters | Trainable LoRA parameters | Steps | Validation loss |
| --- | --- | ---: | ---: | ---: | ---: |
| Small | `distilgpt2` | 82,723,584 | 811,008 | 2,000 | 0.117829 |
| Medium | `gpt2-medium` | 354,823,168 | 4,325,376 | 1,200 | 0.102025 |
| Large | `gpt2-large` | 774,030,080 | 8,110,080 | 600 | 0.097541 |

Each adapter includes its model card, PEFT adapter configuration and weights,
training metadata, validation output, and checkpoints. These are research
baselines, not standalone foundation models; users must load the named base model
with the supplied adapter and should evaluate behavior for their own use case.

## Earlier tag clarification

The prior `v1.0.3` tag remains immutable for reproducibility. The generative
artifacts were uploaded afterwards to the repository's default branch, so
`v1.1.0` is the version to use when a tagged package with the complete model
family is required.
