"""Text cleaning and tokenization helpers."""
import re

_URL = re.compile(r"https?://\S+|www\.\S+")
_NON_WORD = re.compile(r"[^a-z0-9\s]")
_WS = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Lowercase, strip URLs and punctuation, collapse whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = _URL.sub(" ", text)
    text = _NON_WORD.sub(" ", text)
    return _WS.sub(" ", text).strip()


def tokenize(text: str) -> list[str]:
    return clean_text(text).split()


def split_clauses(text: str) -> list[str]:
    """Split a review into clauses on sentence and contrast boundaries.

    Enables aspect-level polarity (e.g. "camera is great but battery is poor").
    """
    if not isinstance(text, str):
        return []
    parts = re.split(r"(?<=[.!?])\s+|\b(?:but|however|although|though|whereas|yet)\b", text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p and p.strip()]
