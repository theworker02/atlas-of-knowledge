"""Expand each existing learning facet into explanation, practice, and verification content."""
from __future__ import annotations
import hashlib

UNITS = (
    ("explanation", "Focused explanation", "A focused explanation unpacks the facet's central claim, vocabulary, and reasoning sequence.", "Define the relevant terms, state the claim in plain language, then connect each part to the underlying concept."),
    ("practice", "Applied practice", "Applied practice gives a bounded task that requires using the facet rather than merely recalling it.", "Set a concrete goal, select evidence or a method, carry out the reasoning, and document the assumptions used."),
    ("verification", "Verification and feedback", "Verification and feedback specify how a learner can check the result, diagnose an error, and improve an explanation.", "Compare the result with stated criteria, trace any mismatch to a step or assumption, then revise and retest."),
)

def deepen(facets: list[dict]) -> list[dict]:
    output=[]
    for facet in facets:
        for suffix, label, definition, reasoning in UNITS:
            identifier=f"{facet['id']}--{suffix}"
            digest=hashlib.sha256(facet["id"].encode()).hexdigest()
            output.append({
                "id":identifier,"concept":f"{facet['concept']}: {label}","discipline":facet["discipline"],"course":facet["course"],"topic":facet["topic"],
                "definition":definition,
                "explanation":f"This learning record adds usable instructional content to the {facet['concept']} facet. It develops the original Atlas account through an explicit learning action while retaining the facet's scope: {facet['definition']}",
                "prerequisites":[facet["id"]],"related_concepts":[{"target_id":facet["id"],"relationship":"builds_on","rationale":"The content unit requires the vocabulary and scope established by its parent facet."}],
                "core_principles":["Use the parent facet as the conceptual frame.","Make the reasoning chain inspectable and revisable."],
                "examples":[f"A learner explains how {facet['concept']} applies to a new bounded scenario."],"applications":[f"Supports deliberate practice and feedback for {facet['concept']}."],
                "common_misconceptions":["Completing a task once proves complete understanding."],"assumptions":["The learner has already studied the parent facet and its anchor concept."],"reasoning":reasoning,
                "questions":[f"What evidence would show mastery of {facet['concept']}?"],"answers":["A learner can explain its scope, apply it in a bounded case, and check or revise the result using explicit criteria."],
                "domain_properties":{"content_unit":suffix,"parent_facet":facet["id"]},
                "provenance":{"source_course":"atlas-editorial:v1","source_resource":facet["id"],"source_hash":digest,"ingested_at":"2026-08-19T00:00:00+00:00","pipeline_version":"0.3.0"}
            })
    return output
