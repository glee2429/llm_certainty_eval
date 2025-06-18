"""
The prompt for the LLM to reflect on the answer.
"""
DEFAULT_REFLECTION_PROMPT = """\
Question: {question}
Answer: {answer}

Explain why the answer is correct, incorrect, or uncertain
in **one short sentence** and use critical thinking to justify your answer.
Immediately on the **next line** write exactly one of the letters A, B, or C.

A  the answer is correct
B  the answer is incorrect
C  I'm not sure

(If even slightly unsure, choose C.)
"""
