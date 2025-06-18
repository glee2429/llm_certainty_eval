"""
This module provides the SelfReflectionScorer class for
scoring self-reflection responses.
"""
import re
from statistics import mean
from .llm_client import LLMClient
from .prompts import DEFAULT_REFLECTION_PROMPT

_LINE_RE = re.compile(r"^[ \t]*([ABC])[ \t]*$", re.IGNORECASE | re.MULTILINE)


class SelfReflectionScorer:
    """
    Implements the "self-reflection certainty" (Chen & Mueller §3.2),
    averaging N independent reflections to reduce false-positive confidence.
    """

    _MAP = {"A": 1.0, "B": 0.0, "C": 0.5}
    _REGEX = re.compile(r"\b([ABC])\b", re.IGNORECASE)

    # --------------------------------------------------------------------- #
    def __init__(
        self,
        model: str = "gemini/gemini-2.0-flash",
        reflection_prompt: str | None = None,
        temperature: float = 0.5,
        n_reflections: int = 3,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
        **llm_kwargs,
    ):
        """
        Parameters
        ----------
        n_reflections : int
            How many independent reflection calls to sample and average.
        """
        if n_reflections < 1:
            raise ValueError("n_reflections must be ≥ 1")

        self.prompt_template = reflection_prompt or DEFAULT_REFLECTION_PROMPT
        self.n_reflections = n_reflections
        self.llm = LLMClient(
            model=model,
            temperature=temperature,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            **llm_kwargs,
        )

    # --------------------------------------------------------------------- #
    # helpers
    def _build_prompt(self, question: str, answer: str) -> str:
        return self.prompt_template.format(question=question, answer=answer)

    @staticmethod
    def _extract_letter(text: str) -> str | None:
        """
        Scan each line for one that consists solely of A, B, or C.
        Returns the uppercase letter or None if not found.
        """
        m = _LINE_RE.search(text)
        return m.group(1).upper() if m else None

    # --------------------------------------------------------------------- #
    # public API
    def score(self, answer: str, *, question: str = "") -> float:
        """
        Returns the average confidence score of the self-reflection.
        """
        return self.explain(answer, question=question)["score_mean"]

    def explain(self, answer: str, *, question: str = "") -> dict:
        """
        Returns:
          • prompt      – the exact prompt used
          • responses   – list of raw reflection strings
          • letters     – parsed letters (may include None)
          • scores      – numeric scores for each reflection
          • score_mean  – final averaged confidence
        """
        prompt = self._build_prompt(question, answer)
        responses, letters, scores = [], [], []

        for _ in range(self.n_reflections):
            raw = self.llm.complete(prompt).strip()
            responses.append(raw)
            letter = self._extract_letter(raw)
            letters.append(letter)
            if letter in self._MAP:
                scores.append(self._MAP[letter])

        return {
            "prompt": prompt,
            "responses": responses,
            "letters": letters,
            "scores": scores,
            "score_mean": mean(scores) if scores else None,
        }
