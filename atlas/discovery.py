"""Discovery consumes small, declared catalog feeds; it does not crawl arbitrary pages."""
from __future__ import annotations
import json
from datetime import UTC, datetime
from pathlib import Path
from .models import CourseCandidate
from .policy import license_decision, load_policy

ROOT = Path(__file__).resolve().parents[1]
DISCIPLINES = {"computer science","mathematics","physics","chemistry","biology","engineering","economics","psychology","philosophy","statistics","linguistics","astronomy","environmental science","history","political science"}
def discover() -> list[CourseCandidate]:
    policy, found = load_policy(), []
    for source in policy["sources"]:
        fixture = ROOT / source["catalog_fixture"]
        for item in json.loads(fixture.read_text(encoding="utf-8"))["courses"]:
            found.append(CourseCandidate(discovered_at=datetime.now(UTC).isoformat(), source_name=source["name"], **item))
    return found
def score(course: CourseCandidate) -> tuple[float, str]:
    licensed, _ = license_decision(course.source_url, course.license)
    points = 0.35 if course.discipline.lower() in DISCIPLINES else 0
    points += 0.25 if course.level in {"undergraduate", "graduate"} else 0
    points += 0.20 if len(course.description) >= 80 else 0
    points += 0.20 if course.prerequisites is not None else 0
    return round(points, 2), "approved" if points >= 0.75 and licensed else "quarantined"
