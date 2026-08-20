"""Deterministic original expansion of curated anchors into connected learning records."""
from __future__ import annotations
import hashlib

FACETS = (
    ("formal-model", "Formal model", "A formal representation specifies the quantities, structure, or rules needed to reason precisely about the concept.", "Translate the concept into variables, relations, or an explicit procedure before drawing conclusions."),
    ("evidence", "Evidence and measurement", "Evidence and measurement identify which observations would support, constrain, or challenge an account of the concept.", "Match the measurement method to the claim and state uncertainty, sampling limits, and possible confounders."),
    ("assumptions", "Assumptions and boundary conditions", "Assumptions and boundary conditions identify when a model of the concept can be expected to apply.", "State the system boundary, idealizations, and scale; then test whether changing them changes the conclusion."),
    ("worked-example", "Worked example", "A worked example applies the concept step by step to a representative problem without replacing general reasoning.", "Identify the givens, select a justified method, derive a result, and check it against the assumptions."),
    ("applications", "Applications and decisions", "Applications connect the concept to a practical decision, design, interpretation, or intervention.", "Use the concept to compare alternatives while recognizing costs, uncertainty, and domain-specific constraints."),
    ("limitations", "Limitations and alternatives", "Limitations and alternatives identify where a concept is incomplete, contested, or better complemented by another approach.", "Compare the concept with a relevant alternative and explain what evidence would favor each account."),
    ("terminology", "Terminology and distinctions", "Terminology and distinctions define the technical vocabulary needed to use the concept without conflating nearby ideas.", "Contrast the term with related terms and use each only within its stated scope."),
    ("methods", "Methods and procedure", "Methods and procedure identify a repeatable way to investigate, calculate, interpret, or apply the concept.", "Select a method that fits the question, document its steps, and check whether its inputs satisfy the method's requirements."),
    ("comparison", "Comparison with related models", "Comparison with related models clarifies what the concept explains well and what a neighboring framework explains differently.", "Hold the target question fixed, compare assumptions and predictions, then identify the evidence that distinguishes the models."),
    ("transfer", "Transfer to a new context", "Transfer to a new context tests whether the concept can be applied beyond the example in which it was first learned.", "Map the new situation to the concept's core structure and state which assumptions remain valid or need revision."),
    ("error-analysis", "Error analysis", "Error analysis identifies how uncertainty, approximation, measurement, or interpretation can affect a conclusion involving the concept.", "List plausible error sources, estimate their consequence, and avoid claiming more precision than the evidence supports."),
    ("synthesis", "Synthesis with course themes", "Synthesis with course themes connects the concept to broader disciplinary questions and other parts of the curriculum.", "Relate the concept to at least two course themes and explain the direction and limits of each connection."),
    ("assessment", "Assessment and mastery", "Assessment and mastery specify observable evidence that a learner can explain, apply, critique, and communicate the concept.", "Use a mix of explanation, application, and critique tasks rather than treating recall as complete mastery."),
    ("history", "Historical and intellectual context", "Historical and intellectual context situates the concept within the problems, debates, and developments that shaped its use.", "Connect the concept to a documented intellectual problem while avoiding anachronistic claims about its significance."),
    ("derivation", "Derivation and justification", "Derivation and justification show how a conclusion, formula, or method follows from explicit starting claims.", "Name each premise, apply valid transformations, and distinguish a derivation from an empirical observation."),
    ("representations", "Multiple representations", "Multiple representations express the concept through verbal, symbolic, graphical, computational, or physical forms.", "Translate between representations and check that each preserves the relevant relationships."),
    ("experiments", "Experimental and observational design", "Experimental and observational design specifies how evidence about the concept can be gathered without confusing design choices with results.", "Define variables, comparison conditions, sampling, and criteria for interpreting the resulting observations."),
    ("computation", "Computational implementation", "Computational implementation describes how the concept can be represented, simulated, calculated, or checked with an algorithm.", "Specify inputs, outputs, numerical limitations, and tests that connect program behavior to the concept."),
    ("communication", "Explanation and communication", "Explanation and communication adapt a rigorous account of the concept to a stated audience without removing necessary qualifications.", "Lead with the central claim, show the supporting reasoning, and mark uncertainty and boundaries clearly."),
    ("ethics", "Ethical and social implications", "Ethical and social implications consider how applying the concept can distribute benefits, risks, authority, and responsibility.", "Identify affected groups, possible harms, and the limits of drawing normative conclusions from descriptive claims."),
    ("collaboration", "Collaborative inquiry", "Collaborative inquiry identifies how roles, critique, shared standards, and replication improve work involving the concept.", "Make contributions auditable, invite independent checking, and resolve disagreements by returning to methods and evidence."),
    ("data", "Data interpretation", "Data interpretation connects observations to the concept while distinguishing patterns, uncertainty, and causal claims.", "Inspect data quality, visualize relevant variation, and avoid generalizing beyond the design and population."),
    ("case-study", "Case study", "A case study analyzes a concrete instance to illuminate both the usefulness and limits of the concept.", "Describe the case context, apply the concept carefully, and explain which conclusions do not generalize automatically."),
    ("problem-solving", "Problem-solving strategy", "Problem-solving strategy organizes how a learner recognizes, decomposes, and checks a problem involving the concept.", "Restate the goal, identify constraints, choose a method, work systematically, and verify the result."),
    ("advanced", "Advanced extension", "An advanced extension introduces a more demanding version of the concept that relaxes a simplifying assumption or connects to specialized study.", "State what changes from the introductory model and which new tools or prerequisites the extension requires."),
    ("interdisciplinary", "Interdisciplinary connection", "An interdisciplinary connection shows how the concept informs or is informed by a neighboring field without erasing differences in methods.", "Identify the shared structure and the discipline-specific assumptions before transferring an interpretation."),
    ("misuse", "Misuse and safeguards", "Misuse and safeguards identify ways the concept can be oversimplified, overgeneralized, or applied outside its evidential scope.", "Name the failure mode, its consequence, and a concrete check that reduces the risk."),
    ("research", "Research frontier", "A research frontier identifies an open question, methodological challenge, or active debate relevant to the concept.", "Distinguish established knowledge from unresolved questions and avoid presenting a single contested view as settled."),
    ("review", "Integrated review", "Integrated review consolidates definitions, methods, evidence, applications, and limitations into a coherent account of the concept.", "Reconstruct the concept from memory, apply it to a new case, and critique the assumptions used."),
    ("teaching-sequence", "Teaching sequence", "A teaching sequence orders prerequisite ideas, practice, feedback, and transfer tasks so that the concept can be learned progressively.", "Move from prerequisite recall to guided practice, independent application, and reflective correction."),
)

def expand(anchors: list[dict]) -> list[dict]:
    records=[]
    for anchor in anchors:
        for suffix, label, definition, reasoning in FACETS:
            identifier=f"{anchor['id']}--{suffix}"
            title=f"{anchor['concept']}: {label}"
            digest=hashlib.sha256(anchor["id"].encode()).hexdigest()
            records.append({
                "id":identifier,"concept":title,"discipline":anchor["discipline"],"course":anchor["course"],"topic":anchor["topic"],
                "definition":definition,
                "explanation":f"This record develops {anchor['concept']} as taught in {anchor['course']}. {anchor['explanation']} It is an original Atlas learning facet, linked to the anchor rather than copied from a course source.",
                "prerequisites":[anchor["id"]],"related_concepts":[{"target_id":anchor["id"],"relationship":"builds_on","rationale":f"Understanding the anchor concept is necessary to analyze its {label.lower()}."}],
                "core_principles":[f"Reason from the central account of {anchor['concept']}.","Make assumptions and evidence requirements explicit."],
                "examples":[f"Apply {anchor['concept']} to a bounded case and document each inference."],"applications":[f"Use {anchor['concept']} to structure a discipline-appropriate analysis."],
                "common_misconceptions":[f"The {label.lower()} of {anchor['concept']} can be understood without its underlying concept."],
                "assumptions":["The anchor concept is correctly scoped to the problem under analysis."],"reasoning":reasoning,
                "questions":[f"How does the {label.lower()} change the interpretation of {anchor['concept']}?"],"answers":[f"It makes the reasoning around {anchor['concept']} explicit, testable, and appropriately bounded."],
                "domain_properties":{"expansion_type":suffix,"anchor_id":anchor["id"]},
                "provenance":{"source_course":"atlas-editorial:v1","source_resource":anchor["id"],"source_hash":digest,"ingested_at":"2026-08-19T00:00:00+00:00","pipeline_version":"0.3.0"}
            })
    return records
