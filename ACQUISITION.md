# Acquisition Brief â€” Atlas of Knowledge

**Date:** 2026-09-22  
**Repository:** https://github.com/theworker02/atlas-of-knowledge  
**Default branch:** `main`  
**Primary language:** Python  
**Status:** Diligence briefing only. **No acquisition has occurred** by virtue of this file.  
**License:** Proprietary â€” sale, written commercial license, or completed asset transfer required (see root `LICENSE`).  
**Valuation:** Not stated.  
**Contact:** GitHub [@theworker02](https://github.com/theworker02) Â· [thanks.dev/u/gh/theworker02](https://thanks.dev/u/gh/theworker02)

> Cloning or forking this repository does **not** grant production, redistribution, SaaS, OEM, or commercial rights.

---

## 1. Executive thesis

<img src="assets/atlas-mark.svg" width="520" alt="Atlas of Knowledge" /> <a href="https://github.com/theworker02/atlas-of-knowledge/actions/workflows/validate.yml"><img src="https://github.com/theworker02/atlas-of-knowledge/actions/workflows/validate.yml/badge.svg" alt="Validation" /></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-2555d9.svg" alt="CC BY 4.0" /></a>

**Why a buyer cares:** Atlas of Knowledge packages transferable product IP â€” source, docs, in-repo brand assets, and a diligence room under `docs/acquisition/` â€” under a clear proprietary posture so diligence can proceed without mistaking the repo for open source.

---

## 2. Product snapshot

| Item | Detail |
|------|--------|
| Product | Atlas of Knowledge |
| Repo | `theworker02/atlas-of-knowledge` |
| Language | Python |
| Open source? | **No** â€” proprietary |
| Rightsholder | theworker02 |
| Diligence pack | `docs/acquisition/` |

### Capability highlights (from current materials)

- en
- 10K<n<100K
- education
- knowledge-graph
- university
- retrieval
- structured-data
- question-answering
- text-classification
- Write original explanations; do not import course notes or textbook passages.
- State assumptions and boundaries when a model is idealized.
- Add only relationships that are meaningful and reviewable.

---

## 3. Problem / opportunity

Teams evaluating Atlas of Knowledge typically need either (a) a commercial right to run or embed it, or (b) outright ownership of the Product IP for strategic build-out. Public GitHub visibility without a proprietary license creates false assumptions about free production use. This brief and the linked data room make the commercial path explicit.

---

## 4. What ships today

Honest maturity: treat repository contents, README claims, tests, and release tags as the source of truth. Do not assume production customers, ARR, filed patents, or SLAs unless separately evidenced in diligence.

Typical transferable surfaces:

- Source tree and build/test scripts present in-repo
- Documentation and design notes
- Acquisition / diligence markdown under `docs/acquisition/`
- Branding assets committed to the repository (if any)

---

## 5. Demo / evaluation path (buyer)

Minimal path (no secrets required unless README says otherwise):

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

Extended evaluation: `docs/acquisition/BUYER_EVALUATION.md`. Written NDA / evaluation grants may be required for private materials.

---

## 6. What a transaction typically includes

Subject to definitive schedules:

| Included (typical) | Excluded (typical) |
|--------------------|--------------------|
| Repo materials + asserted original IP | Seller personal accounts / unrelated repos |
| Docs + diligence room at closing | Third-party dependency source under separate licenses |
| In-repo brand marks as assigned | Secrets without rotation plan |
| Know-how captured in docs | Fabricated revenue, user, or adoption metrics |

---

## 7. Suggested deal structures

| Structure | When it fits |
|-----------|--------------|
| Non-exclusive commercial license | Deploy/run under seat or environment terms |
| Exclusive field-of-use license | Buyer wants exclusivity; seller may retain entity |
| Asset / IP assignment | Buyer wants ownership of Materials outright |
| OEM / redistribution | Separate agreement â€” not implied here |

Commercial terms (price, earnouts, escrow) are negotiated under NDA with counsel.

---

## 8. Buyer diligence checklist

- [ ] Confirm Rightsholder identity and authority to sell/license
- [ ] Inventory Materials (`docs/acquisition/ASSET_INVENTORY.md`)
- [ ] Review IP posture (`IP_PROVENANCE.md`) and dependencies (`DEPENDENCY_INVENTORY.md`)
- [ ] Run evaluation script (`BUYER_EVALUATION.md`)
- [ ] Review risks (`RISK_REGISTER.md`)
- [ ] Agree transfer scope (`TRANSFER_MANIFEST.md`) and handoff (`HANDOFF_CHECKLIST.md`)
- [ ] Supersede root `LICENSE` at closing via definitive agreement

---

## 9. Related documents

| Document | Purpose |
|----------|---------|
| `LICENSE` | Proprietary â€” no default grant |
| `docs/acquisition/README.md` | Data-room index |
| `docs/acquisition/EXECUTIVE_SUMMARY.md` | One-page thesis |
| `README.md` | Product overview |
| `SECURITY.md` | Vulnerability reporting |
| `COMMERCIAL.md` | Licensing contact path |
| `.github/FUNDING.yml` | Sponsors / thanks.dev |

---

## 10. Disclaimer

This package is informational and **does not** create a binding offer, grant of rights, or investment advice. Engage counsel for any transaction.

---

*Document version: 2.0.0 / 2026-09-22 Â· Classification: acquisition briefing*
