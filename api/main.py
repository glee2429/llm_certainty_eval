from typing import List

from fastapi import FastAPI
from api.schema import CertaintyEvalInput, EvalResult
from llm_reflection.scorer import SelfReflectionScorer  # hypothetical

app = FastAPI()

@app.post("/evaluate", response_model=List[EvalResult])
def evaluate_certainty_api(data: CertaintyEvalInput):
    results = []
    for answer, question in data.messages:
        explanation = SelfReflectionScorer.explain(answer, question)  # you can wrap your existing logic
        results.append({
            "input": data.message,
            "certainty_score": explanation["score_mean"],
            "reasoning": explanation["reasoning"],
        })
    return results
