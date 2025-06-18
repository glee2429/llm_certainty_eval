from llm_reflection.scorer import SelfReflectionScorer
import warnings
import time

# silence noisy Pydantic serializer warnings from LiteLLM
warnings.filterwarnings(
    "ignore",
    message=r"Pydantic serializer warnings:",
    category=UserWarning,
)


def main() -> None:
    """
    Showcase the averaged-reflection scorer on a mix of correct,
    incorrect, and ambiguous answers.
    """
    scorer = SelfReflectionScorer(
        model="gemini/gemini-2.0-flash",
        temperature=0.5,      # Increase diversity to the reflections
        n_reflections=3,      # default; explicit here for clarity
    )

    examples = [
        ("2",    "What is 1 + 1?"),
        ("13",   "What is 6 + 6?"),
        ("March","What is the third month in alphabetical order?"),
        ("3",    "How many r's are in the word 'strawberry'?"),
        ("It depends.", "Is the sentence 'I always lie.' true or false?"),
    ]

    for answer, question in examples:
        details = scorer.explain(answer, question=question)
        score   = details["score_mean"]

        # pretty-print
        print(f"\nQ: {question!r}")
        print(f"A: {answer!r}")
        print(f"→ averaged score: {score:.2f}")
        print("  letters:", details["letters"])
        print("  raw reflections:")
        for i, resp in enumerate(details["responses"], 1):
            print(f"    [{i}] {resp!r}")
        time.sleep(1)


if __name__ == "__main__":
    main()
