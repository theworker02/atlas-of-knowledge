#!/usr/bin/env python3
"""Package a complete Atlas release for Hugging Face without tracking it in Git."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description="Stage a complete Hugging Face dataset release")
parser.add_argument("--version", default="1.0.3")
args = parser.parse_args()
release = ROOT / "releases" / f"v{args.version}"
if not release.exists(): raise SystemExit(f"Missing release: {release}. Run atlas first.")
target = ROOT / "dist" / "huggingface" / f"atlas-of-knowledge-v{args.version}"
if target.exists(): shutil.rmtree(target)
shutil.copytree(release, target / "data")
for source, name in [(ROOT / "dataset_card.md", "README.md"), (ROOT / "LICENSE", "LICENSE"), (ROOT / "CITATION.cff", "CITATION.cff")]:
    shutil.copy2(source, target / name)
shutil.copytree(ROOT / "schema", target / "schema")
shutil.copytree(ROOT / "docs", target / "docs", dirs_exist_ok=True)
models = ROOT / "artifacts" / "models" / f"v{args.version}"
if models.exists():
    shutil.copytree(models, target / "models")
    print(f"Included trained model artifacts from {models}")
generative_models = ROOT / "artifacts" / "generative" / f"v{args.version}"
if generative_models.exists():
    shutil.copytree(generative_models, target / "models" / "generative", dirs_exist_ok=True)
    print(f"Included generative model artifacts from {generative_models}")
print(target)
