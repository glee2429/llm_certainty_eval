"""
Exceptions for the LLM reflection package.
"""


class LLMAPIError(Exception):
    """When the underlying LLM API fails after exhausting retries."""


class ReflectionParseError(Exception):
    """When the LLM’s self-reflection response can’t be mapped to A/B/C."""
