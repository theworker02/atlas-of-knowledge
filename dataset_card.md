---
language: en
license: cc-by-4.0
tags: [education, knowledge-graph, university, retrieval, structured-data]
---
# Atlas of Knowledge dataset card

**Version:** 1.0.0 · **Records:** 11,237 · **Distribution:** Hugging Face release package

## Summary and uses

Atlas of Knowledge is an original, structured representation of university-level concepts. It supports retrieval, educational tooling, knowledge-graph analysis, and carefully evaluated model-training experiments. It is not a replacement for expert instruction, domain references, or professional advice.

## Structure

The primary `concepts` subset contains an ID, discipline, course, topic, definitions, explanatory fields, prerequisites, typed relationships, applications, misconceptions, assumptions, reasoning, questions, answers, and optional domain properties. The 1.0.0 release has 11,237 connected records across 17 courses. Releases also export `courses`, `prerequisites`, `relationships`, `questions`, `reasoning`, `misconceptions`, and `cross_domain`, plus deterministic train/validation/test splits and an independent graph.

## Collection, approval, and provenance

The pipeline uses an allowlist of declared course catalogs, checks source identity and compatible licensing, scores course metadata, and automatically approves high-confidence entries. It quarantines ambiguous sources. Source provenance is held separately from generated records. Atlas does not scrape arbitrary websites or publish source passages as data.

## Validation and limitations

Records undergo schema, relationship, duplication, licensing, consistency, and confidence checks. Automation can miss subtle factual errors, cultural framing, contested interpretations, source bias, or semantic duplication. Scores are not proof of correctness. Initial coverage is intentionally sparse and English-focused; it should not be used to benchmark broad educational competence.

## Versioning and citation

Semantic dataset versions identify reproducible builds. GitHub hosts the source pipeline; the complete generated release is published to Hugging Face and includes this card, schema, provenance metadata, citation, and license. Cite the exact release version. See `CITATION.cff` and README for a ready-to-use citation.

## Example

```json
{"id":"computer-science:algorithms:algorithmic-complexity","concept":"Algorithmic complexity","prerequisites":[],"related_concepts":[{"target_id":"mathematics:proofs:mathematical-induction","relationship":"formalizes","rationale":"Induction is a standard method for proving recurrence-based bounds."}]}
```
