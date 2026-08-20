#!/usr/bin/env bash
# Train Atlas generative LoRA adapters one at a time on CPU.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${1:-1.1.0}"
LOG_DIR="$ROOT/artifacts/generative/v$VERSION"
SMALL="$LOG_DIR/atlas-distilgpt2-lora"
MEDIUM="$LOG_DIR/atlas-gpt2-medium-lora"
LARGE="$LOG_DIR/atlas-gpt2-large-lora"
mkdir -p "$LOG_DIR"

wait_for_small() {
  until [[ -f "$SMALL/training-metadata.json" ]]; do
    if ! pgrep -f "train_generative_lora.py --version $VERSION --max-steps 2000" >/dev/null; then
      echo "Small run stopped without producing training metadata." >&2
      exit 1
    fi
    sleep 30
  done
}

wait_for_small
python3 "$ROOT/scripts/train_generative_lora.py" --version "$VERSION" --variant medium --base-model gpt2-medium --max-steps 1200 --save-steps 100 --output-dir "$MEDIUM" > "$MEDIUM.log" 2>&1
python3 "$ROOT/scripts/train_generative_lora.py" --version "$VERSION" --variant large --base-model gpt2-large --max-steps 600 --save-steps 100 --output-dir "$LARGE" > "$LARGE.log" 2>&1
