# Validation methodology

Every record receives a JSON quality report. The validator checks required fields, ID shape, duplicate IDs, local edge resolution, known relationship types, and one-to-one question/answer alignment. The quality stage adds normalized-content fingerprint duplicate detection, licensing state, confidence, and approval status.

Prerequisite edges are validated as references and release construction exports them separately. A release gate also rejects directed cycles in prerequisite graphs, malformed mathematical property fields, inconsistent course/discipline identifiers, unsupported source provenance, and split overlap. Failed records are quarantined in registry state rather than released.

Scores are automation triage signals, not truth guarantees. Claims require original authoring and source-backed review; low confidence, licensing ambiguity, contradictions, similarity flags, or failed checks require human review.
