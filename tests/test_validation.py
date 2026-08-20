import unittest
from scripts.validate_dataset import validate

class ValidationTests(unittest.TestCase):
    def test_rejects_unresolved_edges(self):
        record = {"id": "math:test:sample", "concept": "Sample", "discipline": "Mathematics", "course": "Test", "topic": "Test", "definition": "A sufficiently long definition for validation.", "explanation": "A sufficiently long explanation for the structural validator to accept.", "prerequisites": ["math:missing:item"], "related_concepts": [], "core_principles": ["A principle long enough."], "examples": ["Example"], "applications": ["Application"], "common_misconceptions": [], "assumptions": [], "reasoning": "Reasoning which is comfortably longer than thirty characters.", "questions": ["Question?"], "answers": ["Answer."]}
        self.assertTrue(any("unresolved prerequisite" in error for error in validate([record], {"builds_on"})))

    def test_rejects_unknown_relationship(self):
        record = {"id": "math:test:sample", "concept": "Sample", "discipline": "Mathematics", "course": "Test", "topic": "Test", "definition": "A sufficiently long definition for validation.", "explanation": "A sufficiently long explanation for the structural validator to accept.", "prerequisites": [], "related_concepts": [{"target_id": "math:test:sample", "relationship": "invented", "rationale": "This rationale is long enough."}], "core_principles": ["A principle long enough."], "examples": ["Example"], "applications": ["Application"], "common_misconceptions": [], "assumptions": [], "reasoning": "Reasoning which is comfortably longer than thirty characters.", "questions": ["Question?"], "answers": ["Answer."]}
        self.assertTrue(any("unknown relationship" in error for error in validate([record], {"builds_on"})))

    def test_rejects_circular_prerequisites(self):
        base = {"concept":"Sample","discipline":"Mathematics","course":"Test","topic":"Test","definition":"A sufficiently long definition for validation.","explanation":"A sufficiently long explanation for the structural validator to accept.","related_concepts":[],"core_principles":["A principle long enough."],"examples":["Example"],"applications":["Application"],"common_misconceptions":[],"assumptions":[],"reasoning":"Reasoning which is comfortably longer than thirty characters.","questions":["Question?"],"answers":["Answer."]}
        first={**base,"id":"math:test:first","prerequisites":["math:test:second"]}; second={**base,"id":"math:test:second","prerequisites":["math:test:first"]}
        self.assertTrue(any("circular prerequisite" in error for error in validate([first, second], {"builds_on"})))

if __name__ == "__main__":
    unittest.main()
