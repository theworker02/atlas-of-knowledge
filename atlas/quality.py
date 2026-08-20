from __future__ import annotations
import hashlib
from scripts.validate_dataset import validate

def fingerprint(record: dict) -> str:
    text = " ".join([record["concept"], record["definition"], record["explanation"]]).lower()
    return hashlib.sha256(" ".join(sorted(set(text.split()))).encode()).hexdigest()
def report(record: dict, records: list[dict], relationship_types: set[str], license_valid: bool, validation_errors: list[str] | None = None, duplicate: bool = False) -> dict:
    errors = validation_errors if validation_errors is not None else validate(records, relationship_types)
    duplicates = duplicate
    warnings = [error for error in errors if record["id"] in error]
    confidence = 0.91 if not warnings and license_valid else 0.3
    score = round(max(0, confidence - (0.25 if duplicates else 0)), 2)
    return {"record_id":record["id"],"schema_valid":not bool(warnings),"quality_score":score,"confidence":confidence,"duplicate":duplicates,"license_valid":license_valid,"approved":score >= 0.85 and not duplicates,"warnings":warnings}
