# Buyer evaluation â€” Atlas of Knowledge

## Goal

In 15â€“45 minutes, verify the Product builds or runs as documented and that proprietary notices are present.

## Steps

1. Confirm root `LICENSE` is proprietary and `ACQUISITION.md` exists.
2. Skim `README.md` install/run claims.
3. Execute:

```
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
```bash
python -m pip install atlas-of-knowledge==1.1.0
atlas run
```
```bash
python scripts/validate_dataset.py
python atlas_cli.py run --version 1.1.0
python -m unittest discover -s tests -v
```
```python
import json
with open("data/atlas-v1.jsonl", encoding="utf-8") as stream:
    concepts = [json.loads(line) for line in stream if line.strip()]
```
```bash
hf auth login
python scripts/package_hf_release.py --version 1.1.0 --model-version 1.0.3
hf repos create theworker02/atlas-of-knowledge --type dataset --public --exist-ok
hf upload theworker02/atlas-of-knowledge dist/huggingface/atlas-of-knowledge-v1.1.0 --type dataset --commit-message "Atlas v1.1.0 complete release"
```
```bash
python scripts/train_baselines.py --version 1.1.0
```
```

4. Run tests if present (`npm test`, `pytest`, `cargo test`, `go test ./...`, etc.).
5. Record README vs observed behavior gaps in workpapers.

## Pass criteria

- [ ] Clone succeeds
- [ ] Documented happy path works **or** failure is explained
- [ ] Minimal path needs no surprise secrets
- [ ] License notices intact

*Updated: 2026-09-22*
