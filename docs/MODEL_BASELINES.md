# Atlas model baselines

The repository provides a reproducible CPU baseline trainer in
`scripts/train_baselines.py`. It trains two scikit-learn models from a versioned
Atlas release:

- `atlas-discipline-classifier`, which predicts a record's discipline.
- `atlas-course-classifier`, which predicts a record's course.

The trainer consumes only `train.jsonl`, evaluates separately on `validation.jsonl`
and `test.jsonl`, and omits the course and discipline fields from model input. It
writes serialized models, exact metrics, requirements, and model cards under
`artifacts/models/`; that directory is deliberately not tracked by Git.

When present during `scripts/package_hf_release.py --version <version>`, those
artifacts are included under `models/` in the existing Atlas Hugging Face dataset
repository. They are deliberately kept with the versioned dataset release rather
than requiring a separate model repository.

Run it after a release build:

```bash
python scripts/train_baselines.py --version 1.1.0
```

These artifacts are task-specific baselines, not general-purpose language models.
Training a generative model or adapter requires an explicitly selected compatible
base model, a separate license review, and suitable GPU compute.
