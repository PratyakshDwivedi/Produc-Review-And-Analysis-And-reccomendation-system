"""Aspect-based sentiment analysis (keyword + clause rules + negation)."""
from collections import defaultdict

from ml import preprocessing, sentiment
from ml.lexicon import ASPECT_PHRASES


def _aspects_in(clause: str) -> set[str]:
    low = clause.lower()
    found = set()
    for phrase, aspect in ASPECT_PHRASES:
        if phrase in low:
            found.add(aspect)
    return found


def analyze_review(text: str) -> dict[str, str]:
    """Return {aspect: sentiment} for aspects mentioned in the review.

    Polarity is computed per clause so one review can be positive about one
    aspect and negative about another.
    """
    result: dict[str, str] = {}
    for clause in preprocessing.split_clauses(text):
        aspects = _aspects_in(clause)
        if not aspects:
            continue
        pol = sentiment.lexicon_sentiment(clause)
        for a in aspects:
            # if an aspect appears in multiple clauses, keep the stronger signal
            if a not in result or result[a] == "neutral":
                result[a] = pol
    return result


def aggregate(reviews: list[dict]) -> list[dict]:
    """Aggregate aspect sentiment across a product's reviews.

    Returns a list of {aspect, positive, neutral, negative, total, score}
    sorted by how often the aspect is discussed. score is in [-1, 1].
    """
    counts: dict[str, dict] = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    for r in reviews:
        for aspect, pol in analyze_review(r.get("review_text", "")).items():
            counts[aspect][pol] += 1
    out = []
    for aspect, c in counts.items():
        total = c["positive"] + c["neutral"] + c["negative"]
        score = (c["positive"] - c["negative"]) / total if total else 0.0
        out.append({"aspect": aspect, **c, "total": total, "score": round(score, 3)})
    out.sort(key=lambda x: (-x["total"], x["aspect"]))
    return out


def strengths_weaknesses(aspect_rows: list[dict], min_mentions: int = 3):
    """Derive strengths/weaknesses from aggregated evidence (not hard-coded)."""
    strengths, weaknesses = [], []
    for row in aspect_rows:
        if row["total"] < min_mentions:
            continue
        if row["score"] >= 0.3:
            strengths.append(row["aspect"])
        elif row["score"] <= -0.3:
            weaknesses.append(row["aspect"])
    return strengths, weaknesses
