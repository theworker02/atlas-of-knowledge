# Outreach

## Pitch (plain text)

Subject: PatentPulse — 5.93M USPTO full-text records, pipeline included

PatentPulse is a locally owned USPTO grants-and-applications corpus plus the weekly ingest pipeline that produced it. I am opening an acquisition conversation because buying it is cheaper than standing up an internal USPTO XML team.

Measured snapshot (Hugging Face `theworker02/patentpulse`, 2026-08-28):

- 5,929,464 unique full-text records (train/val/test by publication year)
- 6,500,178 valid JSONL rows in; 570,714 duplicates removed (8.78%); 186 malformed lines quarantined (0.00286%)
- 873.81 GB uncompressed JSONL → 211.41 GB Zstd Parquet (44 shards)
- 100% fill on grant id, application number, publication date, claims, document type
- 99.89% titles, 99.11% descriptions, 94.67% abstracts, 94.61% primary CPC
- Canonical digest 42d3a4ae94b40d7e0ba3d76e02ce8af92704adde242153389b3d7cef544e4944

The code stream-parses official weekly XML in constant memory, writes SQLite and JSONL, and exports a single Arrow schema with HUPD-compatible aliases. A 4-vCPU box parses 1,465 fixture docs/s and skips 100% of rows on replay into the same SQLite file.

This is the work your data engineers would otherwise spend the next several months on: concatenated Red Book dumps, DTD drift, identity keys, torn-write JSONL, disk guards, and a rights notice that does not pretend MIT covers every patent document.

I am not asking you to license a search UI. I am asking whether your corp-dev or data platform team wants the corpus and the plant.

Links:

- Pipeline: https://github.com/theworker02/patentpulse
- Snapshot: https://huggingface.co/datasets/theworker02/patentpulse
- Data room: https://github.com/theworker02/patentpulse/tree/main/docs/acquisition

Matthew Looney
matthewlooney5@gmail.com
https://github.com/theworker02

## Contact log

Emails are sent only to addresses published on the company's own site or company page, as general sales/partnerships inboxes, not personal employee inboxes.

| Date (UTC) | Company | Category | Address | Status |
| --- | --- | --- | --- | --- |
| 2026-09-21 | IPRally | Prior-art / search | sales@iprally.com | queued |
| 2026-09-21 | PatSnap | Patent intelligence | demo-inquiry@patsnap.com | queued |
| 2026-09-21 | Amplified | Prior-art / search | info@amplified.ai | queued |
| 2026-09-21 | Minesoft | Patent intelligence | info@minesoft.com | queued |
| 2026-09-21 | Questel | Patent intelligence | communication@questel.com | queued |
| 2026-09-21 | Luminance | Legal-AI | info@luminance.com | queued |
| 2026-09-21 | Digital Science | Scientific information | info@digital-science.com | queued |
| 2026-09-21 | Snorkel AI | AI-data | info@snorkel.ai | queued |
| 2026-09-21 | Hugging Face | AI-data | website@huggingface.co | queued |

Companies with partnership **forms only** (Clarivate IP, Harvey, Cohere, Together AI, Thomson Reuters, LexisNexis IP, CAS, Allen AI) are listed in [TARGET_ACQUIRERS.md](TARGET_ACQUIRERS.md) and were not cold-emailed to privacy or recruiting inboxes.
