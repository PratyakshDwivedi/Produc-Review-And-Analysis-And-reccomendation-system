"""Baseline sentiment: TF-IDF + Logistic Regression, with a lexicon fallback.

Labels are derived from star ratings (documented rule):
    rating >= 4 -> positive,  rating == 3 -> neutral,  rating <= 2 -> negative
This is a weak-supervision heuristic; it is not human-annotated sentiment, so
reported metrics describe agreement with rating-derived labels only.
"""
from functools import lru_cache
from pathlib import Path

import joblib

from ml import preprocessing
from ml.lexicon import (
    NEGATIVE_PHRASES, NEGATIVE_WORDS, NEGATORS, NEUTRAL_PHRASES, POSITIVE_WORDS,
)

LABELS = ("negative", "neutral", "positive")


def label_from_rating(rating: float) -> str:
    if rating >= 4:
        return "positive"
    if rating <= 2:
        return "negative"
    return "neutral"


# ---- lexicon sentiment (used for aspect-level polarity and as fallback) ----

def lexicon_score(text: str) -> float:
    """Return a polarity score in roughly [-1, 1] for a short piece of text."""
    low = text.lower()
    score = 0.0
    for ph in NEGATIVE_PHRASES:
        if ph in low:
            score -= 1.5
    tokens = preprocessing.tokenize(text)
    for i, tok in enumerate(tokens):
        val = 0.0
        if tok in POSITIVE_WORDS:
            val = 1.0
        elif tok in NEGATIVE_WORDS:
            val = -1.0
        if val and i > 0 and tokens[i - 1] in NEGATORS:
            val = -val
        score += val
    if score == 0:
        for ph in NEUTRAL_PHRASES:
            if ph in low:
                return 0.0
    return max(-3.0, min(3.0, score))


def lexicon_sentiment(text: str) -> str:
    s = lexicon_score(text)
    if s > 0.5:
        return "positive"
    if s < -0.5:
        return "negative"
    return "neutral"


# ---- trained model ----

def _model_path() -> Path:
    from backend import config
    return config.MODELS_DIR / "sentiment_model.pkl"


@lru_cache(maxsize=1)
def _load_model():
    path = _model_path()
    if path.exists():
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None


def predict(text: str) -> str:
    """Predict sentiment for one review; falls back to the lexicon if untrained."""
    model = _load_model()
    if model is None:
        return lexicon_sentiment(text)
    cleaned = preprocessing.clean_text(text)
    if not cleaned:
        return "neutral"
    return str(model.predict([cleaned])[0])


def predict_many(texts: list[str]) -> list[str]:
    model = _load_model()
    if model is None:
        return [lexicon_sentiment(t) for t in texts]
    cleaned = [preprocessing.clean_text(t) for t in texts]
    return [str(p) for p in model.predict(cleaned)]
