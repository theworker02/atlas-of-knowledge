"""Allowlist and licensing decisions. Public availability alone is insufficient."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_policy() -> dict:
    return json.loads((ROOT / "sources" / "source-policy.json").read_text(encoding="utf-8"))

def source_for(url: str, policy: dict | None = None) -> dict | None:
    for source in (policy or load_policy())["sources"]:
        if url.startswith(source["url_prefix"]): return source
    return None

def license_decision(url: str, license_name: str, policy: dict | None = None) -> tuple[bool, str]:
    source = source_for(url, policy)
    if not source: return False, "source is not allowlisted"
    if license_name not in source["accepted_licenses"]: return False, "license is not approved for this source"
    if license_name not in (policy or load_policy())["compatible_licenses"]: return False, "license is reference-only or incompatible"
    return True, "licensed for original structured transformation with attribution"
