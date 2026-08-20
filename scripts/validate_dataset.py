#!/usr/bin/env python3
"""Validate Atlas JSONL records and their local knowledge-graph edges."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "atlas-v1.jsonl"
RELATIONSHIPS = ROOT / "schema" / "relationship-types.json"
REQUIRED = {"id", "concept", "discipline", "course", "topic", "definition", "explanation", "prerequisites", "related_concepts", "core_principles", "examples", "applications", "common_misconceptions", "assumptions", "reasoning", "questions", "answers"}
ID = re.compile(r"^[a-z][a-z-]*:[a-z0-9-]+:[a-z0-9-]+$")

def load_records(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"line {line_number}: invalid JSON: {error.msg}") from error
    return records

def validate(records: list[dict], relation_types: set[str]) -> list[str]:
    errors, ids = [], set()
    for index, record in enumerate(records, 1):
        label = f"record {index}"
        missing = REQUIRED - record.keys()
        extra = record.keys() - REQUIRED - {"domain_properties", "provenance"}
        if missing: errors.append(f"{label}: missing fields {sorted(missing)}")
        if extra: errors.append(f"{label}: unsupported fields {sorted(extra)}")
        identifier = record.get("id", "")
        if not ID.fullmatch(identifier): errors.append(f"{label}: invalid id {identifier!r}")
        elif identifier in ids: errors.append(f"{label}: duplicate id {identifier}")
        else: ids.add(identifier)
        for field in ("prerequisites", "related_concepts", "core_principles", "examples", "applications", "common_misconceptions", "assumptions", "questions", "answers"):
            if not isinstance(record.get(field), list): errors.append(f"{label}: {field} must be a list")
        if len(record.get("questions", [])) != len(record.get("answers", [])):
            errors.append(f"{label}: questions and answers must have equal lengths")
        if not record.get("questions"): errors.append(f"{label}: at least one question is required")
        for edge in record.get("related_concepts", []):
            if not isinstance(edge, dict) or set(edge) != {"target_id", "relationship", "rationale"}:
                errors.append(f"{label}: malformed related_concepts edge")
            elif edge["relationship"] not in relation_types:
                errors.append(f"{label}: unknown relationship {edge['relationship']!r}")
    for record in records:
        for target in record.get("prerequisites", []):
            if target not in ids: errors.append(f"{record.get('id')}: unresolved prerequisite {target}")
        for edge in record.get("related_concepts", []):
            if isinstance(edge, dict) and edge.get("target_id") not in ids:
                errors.append(f"{record.get('id')}: unresolved relationship target {edge.get('target_id')}")
    graph = {record.get("id"): record.get("prerequisites", []) for record in records}
    visiting, visited = set(), set()
    def walk(node: str) -> None:
        if node in visiting:
            errors.append(f"circular prerequisite chain includes {node}"); return
        if node in visited: return
        visiting.add(node)
        for target in graph.get(node, []): walk(target)
        visiting.remove(node); visited.add(node)
    for node in graph: walk(node)
    return errors

def main() -> int:
    records = load_records(DATASET)
    relation_types = set(json.loads(RELATIONSHIPS.read_text(encoding="utf-8"))["types"])
    errors = validate(records, relation_types)
    if errors:
        print("Validation failed:", *[f"- {error}" for error in errors], sep="\n")
        return 1
    print(f"Validated {len(records)} concepts, {len({r['discipline'] for r in records})} disciplines, and all local edges.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
