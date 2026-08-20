from __future__ import annotations
import hashlib, json
from pathlib import Path
from .build import build, load_jsonl
from .discovery import discover, score
from .policy import load_policy
from .quality import report
from .registry import Registry

ROOT=Path(__file__).resolve().parents[1]
def run(state_path: Path = ROOT/"state"/"atlas.sqlite", version: str="1.1.0", collect: bool=False) -> dict:
    registry=Registry(state_path); policy=load_policy()
    try:
        for candidate in discover():
            value,status=score(candidate); registry.upsert_course(candidate,status,value,"automatic allowlist, license, and quality decision")
        records=load_jsonl(ROOT/"data"/"atlas-v1.jsonl")
        collected_path=ROOT/"state"/"collected-records.jsonl"; collected=load_jsonl(collected_path) if collected_path.exists() else []; resource_count=0; failures=[]
        if collect:
            from .collector import collect_course, records_from_outline
            for course in registry.approved_courses():
                try:
                    outline, resources = collect_course(course); resource_count += len(resources)
                    collected = list({record["id"]:record for record in collected + records_from_outline(outline, course)}.values())
                except Exception as error:
                    failures.append({"course_id":course["course_id"],"error":str(error)})
        from .expansion import expand
        editorial = expand(records + collected)
        from .deepening import deepen
        deepened = deepen(editorial)
        from .granular import granulate
        granular = granulate(deepened)
        all_records=records + editorial + deepened + granular + collected; relation_types=set(json.loads((ROOT/"schema"/"relationship-types.json").read_text())["types"])
        from scripts.validate_dataset import validate
        validation_errors = validate(all_records, relation_types)
        fingerprints={}
        from .quality import fingerprint
        for item in all_records: fingerprints[fingerprint(item)] = fingerprints.get(fingerprint(item), 0) + 1
        reports=[]
        for record in all_records:
            provenance = record.get("provenance", {})
            source_hash = hashlib.sha256(f"{provenance.get('source_hash', '')}:{record['id']}".encode()).hexdigest() if provenance else hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest()
            if registry.seen(source_hash): continue
            course_id=record["discipline"].lower().replace(" ","-")+":"+record["course"].lower().replace(" ","-")
            quality=report(record,all_records,relation_types,True,validation_errors,fingerprints[fingerprint(record)] > 1); registry.record(record["id"],course_id,source_hash,quality,"approved" if quality["approved"] else "quarantined"); reports.append(quality)
        registry.mark_approved_ingested()
        (ROOT/"state").mkdir(exist_ok=True); (ROOT/"state"/"course-registry.json").write_text(json.dumps(registry.export_courses(),indent=2),encoding="utf-8")
        (ROOT/"state"/"quality-reports.json").write_text(json.dumps(reports,indent=2),encoding="utf-8")
        (ROOT/"state"/"dead-letter.json").write_text(json.dumps(failures,indent=2),encoding="utf-8")
        if collected: collected_path.write_text("".join(json.dumps(record,sort_keys=True)+"\n" for record in collected),encoding="utf-8")
        courses = registry.export_courses(); summary={"courses":len(courses),"institutions":len({course["institution"] for course in courses}),"sources_processed":len(courses),"sources_approved":sum(course["approval_status"]=="approved" for course in courses),"sources_quarantined":sum(course["approval_status"]=="quarantined" for course in courses),"resources_discovered":resource_count,"collection_failures":len(failures)}
        release=build(version,editorial + deepened + granular + collected,summary); return {"release":str(release),"new_reports":len(reports),"approved_courses":len(registry.approved_courses()),"editorial_records":len(editorial),"deepened_records":len(deepened),"granular_records":len(granular),"collected_records":len(collected),"resources_discovered":resource_count,"failures":len(failures)}
    finally: registry.close()
