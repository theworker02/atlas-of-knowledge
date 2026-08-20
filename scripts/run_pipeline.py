#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from atlas.pipeline import run
parser=argparse.ArgumentParser(description="Run the policy-gated Atlas pipeline."); parser.add_argument("--version",default="1.0.0"); parser.add_argument("--state",default="state/atlas.sqlite")
args=parser.parse_args(); print(json.dumps(run(__import__('pathlib').Path(args.state),args.version),indent=2))
