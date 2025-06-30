from pydantic import BaseModel
from typing import List, Optional

class CertaintyEvalInput(BaseModel):
    messages: List[str]

class EvalResult(BaseModel):
    input: str
    certainty_score: float
    reasoning: Optional[str] = None
