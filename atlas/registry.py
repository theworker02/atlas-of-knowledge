from __future__ import annotations
import json, sqlite3
from pathlib import Path
from .models import CourseCandidate

SCHEMA = """
CREATE TABLE IF NOT EXISTS courses (
 course_id TEXT PRIMARY KEY, institution TEXT NOT NULL, source_name TEXT NOT NULL,
 title TEXT NOT NULL, discipline TEXT NOT NULL, level TEXT NOT NULL, description TEXT NOT NULL,
 source_url TEXT NOT NULL UNIQUE, license TEXT NOT NULL, discovered_at TEXT NOT NULL,
 prerequisites_json TEXT NOT NULL, approval_status TEXT NOT NULL, quality_score REAL NOT NULL,
 ingestion_status TEXT NOT NULL, provenance_json TEXT NOT NULL, content_hash TEXT
);
CREATE TABLE IF NOT EXISTS records (
 record_id TEXT PRIMARY KEY, course_id TEXT, source_hash TEXT NOT NULL, quality_json TEXT NOT NULL,
 approval_status TEXT NOT NULL, FOREIGN KEY(course_id) REFERENCES courses(course_id)
);
"""
class Registry:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True); self.db = sqlite3.connect(path); self.db.row_factory = sqlite3.Row; self.db.executescript(SCHEMA)
    def close(self): self.db.close()
    def upsert_course(self, course: CourseCandidate, status: str, score: float, reason: str) -> None:
        values = course.to_dict(); self.db.execute("""INSERT INTO courses VALUES (:course_id,:institution,:source_name,:title,:discipline,:level,:description,:source_url,:license,:discovered_at,:prerequisites,:status,:score,'discovered',:provenance,NULL)
        ON CONFLICT(course_id) DO UPDATE SET title=excluded.title, description=excluded.description, approval_status=excluded.approval_status, quality_score=excluded.quality_score, provenance_json=excluded.provenance_json""", {**values,"prerequisites":json.dumps(values["prerequisites"]),"status":status,"score":score,"provenance":json.dumps({"source_url":course.source_url,"license":course.license,"decision":reason})}); self.db.commit()
    def approved_courses(self) -> list[dict]: return [dict(row) for row in self.db.execute("SELECT * FROM courses WHERE approval_status='approved'")]
    def seen(self, source_hash: str) -> bool: return self.db.execute("SELECT 1 FROM records WHERE source_hash=?", (source_hash,)).fetchone() is not None
    def record(self, record_id: str, course_id: str, source_hash: str, quality: dict, status: str):
        self.db.execute("INSERT OR REPLACE INTO records VALUES (?,?,?,?,?)",(record_id,course_id,source_hash,json.dumps(quality,sort_keys=True),status)); self.db.commit()
    def export_courses(self) -> list[dict]:
        return [dict(row) for row in self.db.execute("SELECT course_id,institution,source_name,title,discipline,level,description,source_url,license,discovered_at,approval_status,quality_score,ingestion_status FROM courses ORDER BY course_id")]
    def mark_approved_ingested(self) -> None:
        self.db.execute("UPDATE courses SET ingestion_status='processed' WHERE approval_status='approved'"); self.db.commit()
