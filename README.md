# LLM Certainty Evaluation

## Description
This library implements a **simplified version of the uncertainty-estimation algorithm** from

> *Quantifying Uncertainty in Answers from any Language Model and Enhancing their Trustworthiness* (Chen & Mueller, ACL '24)

Specifically, the code focuses on **Section 3.2 – Self-reflection certainty**.  The other components (observed consistency, weighted averaging) described in the paper are *not* implemented per the assignment instructions.

The library lets you score any (question, answer) pair with a numeric certainty in \{0.0, 0.5, 1.0\}, where higher is more trustworthy.  Under the hood it prompts an LLM to reflect on its own answer and maps the response letter (A/B/C) to the numeric score.

## Installation

To install the project dependencies, use Poetry:

```bash
poetry install
```

## Usage

### Running the Demo
To run the demo script, use:

```bash
poetry run python demo.py
```

Example output:

```
Q: 'What is 1 + 1?'
A: '2'
→ averaged score: 1.00
  letters: ['A', 'A', 'A']
  raw reflections:
    [1] 'The answer is correct within the standard axioms of arithmetic.\nA'
    [2] 'The answer is correct because the basic axioms of arithmetic define 1 + 1 as 2.\nA'
    [3] 'The answer is correct because it follows the basic axioms of arithmetic.\nA'

Q: 'What is 6 + 6?'
A: '13'
→ averaged score: 0.00
  letters: ['B', 'B', 'B']
  raw reflections:
    [1] 'The answer is incorrect because basic addition dictates that 6 + 6 equals 12, not 13.\nB'
    [2] 'The answer is incorrect because basic addition dictates that 6 + 6 equals 12, not 13.\nB'
    [3] 'The answer is incorrect because basic addition dictates that 6 + 6 equals 12, not 13.\nB'

Q: 'What is the third month in alphabetical order?'
A: 'March'
→ averaged score: 0.00
  letters: ['B', 'B', 'B']
  raw reflections:
    [1] 'The answer is incorrect because when the months are listed alphabetically, April comes first, then August, then December, making December the third month in alphabetical order.\nB'
    [2] 'The answer is incorrect because April is the third month when the months are listed in alphabetical order.\nB'
    [3] 'The answer is incorrect because the months in alphabetical order start with April, August, and then December.\nB'

Q: "How many r's are in the word 'strawberry'?"
A: '3'
→ averaged score: 1.00
  letters: ['A', 'A', 'A']
  raw reflections:
    [1] "The answer is correct because the word 'strawberry' contains three 'r' letters.\nA"
    [2] "The answer is correct because the word 'strawberry' contains three 'r's.\nA"
    [3] "The answer is correct because counting the 'r's in 'strawberry' yields three.\nA"

Q: "Is the sentence 'I always lie.' true or false?"
A: 'It depends.'
→ averaged score: 0.50
  letters: ['C', 'C', 'C']
  raw reflections:
    [1] "The sentence creates a paradox because if it's true, it must be false, and if it's false, it must be true.\nC"
    [2] "The sentence creates a paradox because if it's true, it must be false, and if it's false, it must be true.\nC"
    [3] "The statement creates a paradox, as if it's true, it must be false, and if it's false, it must be true, making its truth value indeterminate.\nC"
```

### Running Tests
To run the tests, use:

```bash
poetry run pytest
```

## Development

### Linting and Formatting
To lint and format the code, use:

```bash
make lint
make format
```

### Adding Dependencies
To add a new dependency, use:

```bash
poetry add <package-name>
```

For development dependencies, use:

```bash
poetry add <package-name> --group dev
```

### Project Structure

```
llm_certainty_eval/
├── llm_reflection/          # Library source code
│   ├── llm_client.py        # Thin wrapper around LiteLLM with retry logic
│   ├── scorer.py            # SelfReflectionScorer – core algorithm
│   ├── prompts.py           # Prompt template(s)
│   └── exceptions.py        # Custom exception types
├── tests/                   # Unit tests (pytest)
│   └── test_scorer.py
├── demo.py                  # Example script / quick-start
├── Makefile                 # lint, format, etc.
└── pyproject.toml           # Poetry configuration
```

## Additional Notes

This project includes:

1. A Python library implementing self-reflection certainty (section 3.2 of the paper).
2. A standalone example showing how to use the library (see `demo.py`).
3. Design rationale (see README's Design Decisions section).

### Expected Output Structure

If you call `scorer.explain(...)` you receive a dict suitable for downstream logging/analysis:

```python
from llm_reflection.scorer import SelfReflectionScorer

scorer = SelfReflectionScorer()
result = scorer.explain("2", question="What is 1 + 1?")
print(result)
```

Example result (values will vary):

```json
{
  "prompt": "You are validating the following answer produced by an LLM.\n\nQuestion:\nWhat is 1 + 1?\n\nAnswer:\n2\n\nReflect on the answer and pick exactly one option:\n(A) The answer is correct.\n(B) The answer is incorrect.\n(C) I'm not sure.\n\nRespond with just \u201cA\u201d, \u201cB\u201d, or \u201cC\u201d (without any extra text).",
  "response": "A",
  "score": 1.0
}
```
The `score` field contains the numeric certainty (1.0 = certain, 0.5 = unsure, 0.0 = incorrect).

## Design Decisions

### Number of Self-Reflections (n = 3)

**Why 3?**

* One reflection can be noisy or unlucky.  Sampling a few independent reflections reduces variance without exploding latency or cost.
* Empirically (per the ACL '24 paper) small ensembles of reflections flatten out occasional hallucinations in the meta-reasoning step.

You can tweak this via `SelfReflectionScorer(n_reflections=...)` to trade off runtime vs. stability.

### Temperature Setting (0.5)

* Temperatures < 0.3 produced highly deterministic (and sometimes over-confident) reflections.
* Temperatures > 0.7 yielded verbose or off-spec answers that failed to parse.

You can override `temperature` per scorer instance or per call if you prefer a different trade-off between diversity and determinism.
