"""Create detailed study content beneath each validated learning-content unit."""
from __future__ import annotations
import hashlib

MODULES = (
    ("context", "Learning context", "Learning context frames the question, prior knowledge, and scope needed before working with the parent content unit."),
    ("prompt", "Guided prompt", "A guided prompt asks the learner to identify the relevant claim, evidence, method, and constraint before proposing an answer."),
    ("worked-path", "Worked reasoning path", "A worked reasoning path models an explicit sequence of justified steps while preserving room for independent checking."),
    ("counterexample", "Counterexample and boundary", "A counterexample and boundary record tests where a tempting generalization fails and identifies the condition that prevents the error."),
    ("rubric", "Quality rubric", "A quality rubric provides observable criteria for checking accuracy, scope, reasoning, and communication in a response."),
    ("reflection", "Reflection and transfer", "Reflection and transfer asks the learner to explain what changed, what remains uncertain, and how the learning applies in a new setting."),
)

def granulate(units: list[dict]) -> list[dict]:
    output=[]
    for unit in units:
        for suffix, label, definition in MODULES:
            identifier=f"{unit['id']}--{suffix}"
            digest=hashlib.sha256(unit["id"].encode()).hexdigest()
            output.append({
                "id":identifier,"concept":f"{unit['concept']}: {label}","discipline":unit["discipline"],"course":unit["course"],"topic":unit["topic"],
                "definition":definition,
                "explanation":f"This granular Atlas record develops {unit['concept']} into a reusable learning component. It is original instructional structure, anchored to the parent unit and constrained by its assumptions rather than reproduced source text.",
                "prerequisites":[unit["id"]],"related_concepts":[{"target_id":unit["id"],"relationship":"builds_on","rationale":"The granular component relies on the explanation, practice, and verification work established by its parent unit."}],
                "core_principles":["Keep the parent concept and evidence boundary visible.","Use explicit checks rather than unsupported confidence."],
                "examples":[f"Use {unit['concept']} to analyze a new, bounded learning scenario."],"applications":["Supports retrieval practice, tutoring, curriculum sequencing, and auditable educational AI."],
                "common_misconceptions":["A detailed response is automatically a well-reasoned response."],"assumptions":["The parent content unit and its prerequisite chain have been studied."],
                "reasoning":"Identify the parent claim, select the relevant evidence or method, make assumptions explicit, perform the reasoning, and evaluate the result against the stated boundary.",
                "questions":[f"How would you use the {label.lower()} for {unit['concept']} to improve a learner's answer?"],"answers":["Use it to make the reasoning visible, testable, appropriately scoped, and transferable to a new but comparable case."],
                "domain_properties":{"module_type":suffix,"parent_unit":unit["id"]},
                "provenance":{"source_course":"atlas-editorial:v1","source_resource":unit["id"],"source_hash":digest,"ingested_at":"2026-08-19T00:00:00+00:00","pipeline_version":"1.0.0"}
            })
    return output
