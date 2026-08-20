"""Deterministic release builder: no random split assignment or network access."""
from __future__ import annotations
import hashlib, json, shutil
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load_jsonl(path: Path) -> list[dict]: return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
def write_jsonl(path: Path, values: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text("".join(json.dumps(value, sort_keys=True, ensure_ascii=False)+"\n" for value in values), encoding="utf-8")
def split(identifier: str) -> str:
    bucket = int(hashlib.sha256(identifier.encode()).hexdigest()[:8], 16) % 100
    return "test" if bucket < 10 else "validation" if bucket < 20 else "train"
def build(version: str = "1.0.2", additional_records: list[dict] | None = None, collection_stats: dict | None = None) -> Path:
    records = load_jsonl(ROOT / "data" / "atlas-v1.jsonl") + (additional_records or [])
    records = sorted({record["id"]:record for record in records}.values(), key=lambda x:x["id"])
    target = ROOT / "releases" / f"v{version}"; shutil.rmtree(target, ignore_errors=True); target.mkdir(parents=True)
    for name in ("train","validation","test"): write_jsonl(target/f"{name}.jsonl", [r for r in records if split(r["id"]) == name])
    write_jsonl(target/"concepts.jsonl", records)
    write_jsonl(target/"questions.jsonl", [{"record_id":r["id"],"question":q,"answer":a} for r in records for q,a in zip(r["questions"],r["answers"])])
    write_jsonl(target/"reasoning.jsonl", [{"record_id":r["id"],"reasoning":r["reasoning"]} for r in records])
    write_jsonl(target/"misconceptions.jsonl", [{"record_id":r["id"],"misconception":m} for r in records for m in r["common_misconceptions"]])
    write_jsonl(target/"prerequisites.jsonl", [{"source_id":r["id"],"target_id":p,"relationship":"requires"} for r in records for p in r["prerequisites"]])
    edges = [{"source_id":r["id"],"target_id":e["target_id"],"relationship":e["relationship"],"rationale":e["rationale"]} for r in records for e in r["related_concepts"]]
    write_jsonl(target/"relationships.jsonl", edges); write_jsonl(target/"cross_domain.jsonl", [e for e in edges if e["source_id"].split(":")[0] != e["target_id"].split(":")[0]])
    courses = [{"course_id":r["discipline"].lower().replace(" ","-")+":"+r["course"].lower().replace(" ","-"),"discipline":r["discipline"],"title":r["course"]} for r in records]
    write_jsonl(target/"courses.jsonl", sorted({json.dumps(c,sort_keys=True):c for c in courses}.values(),key=lambda x:x["course_id"]))
    graph = {"nodes":[{"id":r["id"],"type":"concept","label":r["concept"],"discipline":r["discipline"],"course":r["course"],"topic":r["topic"]} for r in records],"edges":edges+[{"source_id":r["id"],"target_id":p,"relationship":"requires"} for r in records for p in r["prerequisites"]]}
    (target/"knowledge-graph.json").write_text(json.dumps(graph,indent=2),encoding="utf-8")
    stats={"version":version,"built_at":datetime.now(UTC).isoformat(),"record_count":len(records),"disciplines":dict(sorted(Counter(r["discipline"] for r in records).items())),"splits":{n:sum(split(r["id"])==n for r in records) for n in ("train","validation","test")},"graph_edges":len(graph["edges"]),**(collection_stats or {})}
    (target/"build-metadata.json").write_text(json.dumps(stats,indent=2),encoding="utf-8"); (ROOT/"site"/"data").mkdir(parents=True,exist_ok=True); (ROOT/"site"/"data"/"stats.json").write_text(json.dumps(stats,indent=2),encoding="utf-8")
    return target
