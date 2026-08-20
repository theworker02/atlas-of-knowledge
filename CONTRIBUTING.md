# Contributing

Start with the source policy and validation methodology. Do not submit copied educational content, private material, credentials, or sources without a compatible license.

1. Add or amend a declared source catalog and provenance metadata.
2. Add original records that conform to the schema and use resolvable IDs.
3. Run `python scripts/validate_dataset.py`, `python scripts/run_pipeline.py`, and `python -m unittest discover -s tests -v`.
4. Explain factual support, licensing, and relationship choices in the pull request.

Potentially ambiguous, license-sensitive, or failed-validation entries remain quarantined for maintainer review. By contributing, you agree that your work may be released under CC BY 4.0.
