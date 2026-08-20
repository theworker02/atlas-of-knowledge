# Atlas of Knowledge v1.0.3

Released 2026-08-20.

## Complete tagged package

Version `v1.0.3` is the first Atlas release whose tagged Hugging Face package
contains both the full structured dataset and trained baseline artifacts. The
release contains 20,417 validated records across 17 courses and 15 disciplines,
40,832 graph edges, deterministic splits, schemas, provenance metadata, and
documentation.

## Included baselines

`models/atlas-discipline-classifier` and `models/atlas-course-classifier` each
contain a serialized TF-IDF + logistic-regression model, exact metrics,
requirements, and a limitation-focused model card. They were trained only on the
Atlas training split and are task-specific classification baselines, not
generative models or evidence of general educational competence.

## Metadata correction

Build metadata now reports `courses: 17` for the dataset itself and preserves
`source_catalog_courses: 10` as a separate source-registry statistic.
