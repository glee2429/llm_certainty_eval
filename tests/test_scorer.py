import unittest
from llm_reflection.scorer import SelfReflectionScorer
from loguru import logger

class TestSelfReflectionScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = SelfReflectionScorer()

    def test_extract_letter_valid(self):
        # Test valid cases
        self.assertEqual(self.scorer._extract_letter("A"), "A")
        self.assertEqual(self.scorer._extract_letter("B"), "B")
        self.assertEqual(self.scorer._extract_letter("C"), "C")

    def test_extract_letter_invalid(self):
        # Test invalid cases
        self.assertIsNone(self.scorer._extract_letter("D"))
        self.assertIsNone(self.scorer._extract_letter(""))
        self.assertIsNone(self.scorer._extract_letter("1"))

    def test_extract_letter_mixed_content(self):
        # Test mixed content
        self.assertEqual(self.scorer._extract_letter("  A  "), "A")
        self.assertEqual(self.scorer._extract_letter("  B"), "B")
        self.assertEqual(self.scorer._extract_letter("C  "), "C")

    def test_average_reflection_scores(self):
        # Mock the complete method to return different reflection letters
        self.scorer.llm.complete = lambda prompt: "A"
        score_a = self.scorer.score("Answer 1")

        self.scorer.llm.complete = lambda prompt: "B"
        score_b = self.scorer.score("Answer 2")

        self.scorer.llm.complete = lambda prompt: "C"
        score_c = self.scorer.score("Answer 3")

        # Calculate the average score
        average_score = (score_a + score_b + score_c) / 3

        # Assert the average score is correct
        expected_average = (1.0 + 0.0 + 0.5) / 3
        self.assertAlmostEqual(average_score, expected_average, places=2)

        # Log to console
        logger.info(f"Average score calculated: {average_score}")

if __name__ == "__main__":
    unittest.main() 