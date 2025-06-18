"""
This module provides the LLMClient class for interacting with an LLM.
"""
import time
from dotenv import load_dotenv
from litellm import completion
from litellm.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)
from .exceptions import LLMAPIError

load_dotenv()


class LLMClient:
    """
    A client for interacting with an LLM.
    """
    def __init__(
        self,
        model: str = "gemini/gemini-2.0-flash",
        temperature: float = 0.0,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
        **kwargs,
    ):
        self.model = model
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.extra_kwargs = kwargs

    def complete(self, prompt: str) -> str:
        """
        Complete a prompt with the LLM.
        """
        retries = 0
        while True:
            try:
                resp = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    **self.extra_kwargs,
                )
                return resp.choices[0].message.content
            except (AuthenticationError, NotFoundError, RateLimitError) as e:
                if retries >= self.max_retries:
                    raise LLMAPIError(
                        f"Failed after {self.max_retries} retries: {e}"
                    ) from e
                backoff = self.retry_backoff * (2**retries)
                time.sleep(backoff)
                retries += 1
