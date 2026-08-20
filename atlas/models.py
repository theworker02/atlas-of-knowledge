from __future__ import annotations
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class CourseCandidate:
    course_id: str
    institution: str
    source_name: str
    title: str
    discipline: str
    level: str
    description: str
    source_url: str
    license: str
    discovered_at: str
    prerequisites: list[str]

    def to_dict(self) -> dict: return asdict(self)
