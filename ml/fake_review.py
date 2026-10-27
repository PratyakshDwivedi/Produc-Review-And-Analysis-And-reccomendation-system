"""Heuristic review-authenticity risk estimator.

This is a HEURISTIC risk detector, not a trained fraud classifier. It flags
patterns that *may* indicate low authenticity; it cannot prove a review is fake.
"""
from ml import preprocessing, sentiment


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def analyze(reviews: list[dict]) -> dict:
    token_sets = [set(preprocessing.tokenize(r.get("review_text", ""))) for r in reviews]
    seen_text: dict[str, int] = {}
    results = []

    for i, r in enumerate(reviews):
        text = r.get("review_text", "")
        norm = preprocessing.clean_text(text)
        signals, risk = [], 0.0

        # exact duplicate
        if norm and norm in seen_text:
            signals.append("Exact duplicate of another review")
            risk += 0.5
        seen_text.setdefault(norm, i)

        # near-duplicate (high token overlap with any other review)
        best = 0.0
        for j, ts in enumerate(token_sets):
            if j != i:
                best = max(best, _jaccard(token_sets[i], ts))
        if best >= 0.8:
            signals.append(f"Very similar to another review ({int(best * 100)}% overlap)")
            risk += 0.3

        # very short
        if len(preprocessing.tokenize(text)) < 4:
            signals.append("Unusually short review")
            risk += 0.15

        # rating/text sentiment mismatch
        rating = r.get("rating")
        if rating is not None:
            sent = sentiment.lexicon_sentiment(text)
            if (rating >= 4 and sent == "negative") or (rating <= 2 and sent == "positive"):
                signals.append("Star rating contradicts the review text")
                risk += 0.25

        risk = min(1.0, risk)
        category = "high" if risk >= 0.6 else "medium" if risk >= 0.3 else "low"
        results.append({
            "review_id": r.get("review_id"), "risk_score": round(risk, 2),
            "risk_category": category, "signals": signals,
        })

    flagged = sum(1 for x in results if x["risk_category"] != "low")
    return {
        "reviews": results,
        "flagged_count": flagged,
        "total": len(results),
        "flagged_share": round(flagged / len(results), 3) if results else 0,
        "note": "Heuristic risk estimate based on duplication, length and rating/text consistency. Not a definitive fake-review verdict.",
    }
