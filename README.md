---
language:
- en
license: cc-by-4.0
pretty_name: Atlas of Knowledge
size_categories:
- 10K<n<100K
tags:
- education
- knowledge-graph
- university
- retrieval
- structured-data
task_categories:
- question-answering
- text-classification
---

<p align="center">
  <img src="assets/atlas-mark.svg" width="520" alt="Atlas of Knowledge" />
</p>

<p align="center">
  <a href="https://github.com/theworker02/atlas-of-knowledge/actions/workflows/validate.yml"><img src="https://github.com/theworker02/atlas-of-knowledge/actions/workflows/validate.yml/badge.svg" alt="Validation" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-2555d9.svg" alt="CC BY 4.0" /></a>
  <a href="https://huggingface.co/datasets/theworker02/atlas-of-knowledge"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-f7c95c.svg" alt="Hugging Face dataset" /></a>
  <a href="CITATION.cff"><img src="https://img.shields.io/badge/citation-CFF-10233e.svg" alt="Citation file" /></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776ab.svg" alt="Python 3.11 or newer" />
</p>

# Atlas of Knowledge

Atlas of Knowledge is an open, machine-readable map of university knowledge. It combines original concept explanations, explicit prerequisite and relationship edges, auditable provenance, and deterministic release generation. It is not a mirror of syllabi, textbooks, or lecture notes.

> Distribution policy: GitHub contains the lightweight source pipeline, schemas, policy, documentation, and compact seed data. Full generated releases, provenance reports, caches, and Hugging Face staging artifacts are intentionally excluded from Git and are published to Hugging Face only.

## Why Atlas

Atlas turns the structure of a strong university education into reusable data: **discipline → course → topic → concept → prerequisite → application**. It is built for educational retrieval, knowledge graphs, carefully evaluated training workflows, and transparent dataset research—not for reproducing source material.

## At a glance

| Release | Connected records | Courses | Minimum course depth | License |
| --- | ---: | ---: | ---: | --- |
| `v1.1.0` | 20,417 | 17 | 1,200+ records | CC BY 4.0 |

Every generated record retains a stable local identifier, prerequisite path, typed relationship, validation report, and provenance envelope. The release is deterministic: the same approved inputs and version produce the same split assignments and graph structure.

## Current release

V1.1.0 provides a production-oriented, offline-first pipeline around fifteen curated university anchors, their connected learning content, eligible collected course outlines, two transparent trained classification baselines, and a three-size generative LoRA adapter family. It includes allowlisted course discovery, licensing gates, a SQLite course registry, quality reports, deterministic releases, graph exports, CI, and a static GitHub Pages site. Each validated facet produces twelve distinct instructional records, increasing depth through diagnostic, retrieval, formal-checking, design, case-analysis, and peer-critique units rather than using a larger unstructured document dump.

## Generative model family

The complete [Hugging Face dataset release](https://huggingface.co/datasets/theworker02/atlas-of-knowledge/tree/v1.1.0/models/generative) contains three PEFT/LoRA causal-language-model adapters under `models/generative/`. They are research artifacts trained only on the deterministic Atlas training split, not general-purpose foundation models.

| Variant | Base model | Base parameters | LoRA parameters | Validation loss |
| --- | --- | ---: | ---: | ---: |
| Small | `distilgpt2` | 82,723,584 | 811,008 | 0.117829 |
| Medium | `gpt2-medium` | 354,823,168 | 4,325,376 | 0.102025 |
| Large | `gpt2-large` | 774,030,080 | 8,110,080 | 0.097541 |

Every adapter ships with weights, PEFT configuration, checkpoints, evaluation output, metadata, requirements, and a limitation-focused model card. Load it with the named base model plus `peft`; evaluate it for your use case before relying on output.

## Layout

```text
data/atlas-v1.jsonl       One JSON object per concept
schema/concept.schema.json JSON Schema (Draft 2020-12)
schema/relationship-types.json Controlled relationship vocabulary
scripts/validate_dataset.py Dependency-free structural and graph validator
tests/test_validation.py  Regression tests for the validator
atlas/                    Independently testable discovery, policy, registry, quality, and build modules
sources/                  Allowlist policy and small declared catalog feeds
releases/                 Generated deterministic release artifacts (Hugging Face only)
site/                     GitHub Pages dashboard driven by generated statistics
docs/                     Source policy and validation methodology
```

## Record model

`discipline -> course -> topic -> concept -> relationships`

Each concept has a stable `id`, original instructional prose, prerequisite IDs, related concept edges, question/answer pairs, and an optional `domain_properties` object for equations, algorithms, laws, complexity, or experimental methods. Relationship IDs are local dataset identifiers; external links are intentionally not required for a usable knowledge graph.

## Use

```bash
python scripts/validate_dataset.py
python atlas_cli.py run --version 1.1.0
python -m unittest discover -s tests -v
```

The pipeline is intentionally network-free by default. It consumes only declared catalog feeds in `sources/`, writes incremental state to `state/atlas.sqlite`, creates a course registry and per-record quality reports, then builds reproducible artifacts in `releases/v<version>/`. Re-running unchanged inputs does not reprocess registered record fingerprints.

## Automation and safety

The pipeline is `Discover → Evaluate → Approve → Ingest → Transform → Validate → Deduplicate → Graph → Release → Document`. Courses scoring at least 0.75 after allowlist, license, metadata, discipline, and level checks are approved automatically; others are quarantined. Records require a score of 0.85 to be released. License ambiguity, unsupported sources, duplicate candidates, failed graph checks, or low-confidence results are held for review.

See [source policy](docs/SOURCE_POLICY.md), [validation methodology](docs/VALIDATION.md), and the [dataset card](dataset_card.md). GitHub Actions validates scheduled and proposed changes, builds release artifacts, deploys Pages from main, and, in a protected manually dispatched workflow, uploads the complete package to Hugging Face and creates a matching GitHub release tag with generated release notes. The GitHub release intentionally contains no dataset payload.

Load with the Hugging Face datasets library after publishing, or read JSONL directly:

```python
import json
with open("data/atlas-v1.jsonl", encoding="utf-8") as stream:
    concepts = [json.loads(line) for line in stream if line.strip()]
```

## Curation policy

- Write original explanations; do not import course notes or textbook passages.
- State assumptions and boundaries when a model is idealized.
- Add only relationships that are meaningful and reviewable.
- Keep examples illustrative, not fabricated evidence or citations.
- Validate every proposed release with the included validator and review new facts against appropriate primary or authoritative academic sources.

## Expansion protocol

Add records in JSONL using lowercase hyphenated IDs (`discipline:topic:concept`). Use existing relationship types only; propose vocabulary changes in `schema/relationship-types.json` with a documented rationale. A new record must have at least one question/answer pair, an assumption or an explicit empty list, and only resolvable local edges. Add a regression fixture when changing validation behavior.

## Licensing and limitations

Dataset content is licensed under [CC BY 4.0](LICENSE). This is educational reference data, not professional, medical, legal, or safety-critical advice. Concepts deliberately simplify active debates and advanced special cases; their `assumptions` fields identify important boundaries.

## Publishing to Hugging Face

The repository never commits a full generated dataset to GitHub. Package and publish it to Hugging Face instead:

```bash
hf auth login
python scripts/package_hf_release.py --version 1.1.0 --model-version 1.0.3
hf repos create theworker02/atlas-of-knowledge --type dataset --public --exist-ok
hf upload theworker02/atlas-of-knowledge dist/huggingface/atlas-of-knowledge-v1.1.0 --type dataset --commit-message "Atlas v1.1.0 complete release"
```

The staged package contains all data subsets, splits, graph export, build metadata, schema, dataset card, licensing, citation, and methodology documentation.

## Reproducible model baselines

Atlas includes a CPU-friendly trainer for transparent discipline and course classification baselines. It fits only on the deterministic training split and evaluates separately on validation and test splits; it is not a generative-model trainer or a claim of broad educational competence. Packaged baseline artifacts are included under `models/` in the existing Hugging Face Atlas dataset release.

```bash
python scripts/train_baselines.py --version 1.1.0
```

See [model baseline documentation](docs/MODEL_BASELINES.md) for the artifact contract, evaluation boundary, and limitations.

## Citation

Recommended citation: **theworker02 (2026). Atlas of Knowledge (Version 1.1.0) [Dataset]. Hugging Face. https://huggingface.co/datasets/theworker02/atlas-of-knowledge**.
