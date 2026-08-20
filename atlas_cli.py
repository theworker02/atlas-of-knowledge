#!/usr/bin/env python3
import argparse, json
from atlas.pipeline import run
def main() -> None:
    parser=argparse.ArgumentParser(prog="atlas",description="Atlas autonomous, policy-gated collector")
    parser.add_argument("command",choices=["discover","evaluate","approve","ingest","validate","build","stats","run"]); parser.add_argument("--version",default="1.0.0")
    args=parser.parse_args()
    if args.command == "validate":
        from scripts.validate_dataset import main as validate; raise SystemExit(validate())
    result=run(version=args.version,collect=args.command in {"ingest","run"}); print(json.dumps(result,indent=2))
if __name__ == "__main__": main()
