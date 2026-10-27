"""Extractive, evidence-based review summarization (no external LLM)."""
from collections import Counter

from ml import preprocessing, sentiment


def summarize(reviews: list[dict], aspect_rows: list[dict]) -> dict:
    """Build a concise summary from actual review text and aspect evidence."""
    texts = [r.get("review_text", "") for r in reviews if r.get("review_text")]
    if not texts:
        return {"summary": "No reviews available yet.", "common_positives": [],
                "common_complaints": [], "top_aspects": []}

    top_aspects = [r["aspect"] for r in aspect_rows[:5]]
    positives = [r["aspect"] for r in aspect_rows if r["score"] >= 0.3 and r["total"] >= 3]
    complaints = [r["aspect"] for r in aspect_rows if r["score"] <= -0.3 and r["total"] >= 3]

    sentiments = sentiment.predict_many(texts)
    pos = sentiments.count("positive")
    total = len(sentiments)
    share = pos / total if total else 0
    mood = ("Most customers are satisfied" if share >= 0.6
            else "Customer opinion is mixed" if share >= 0.4
            else "Many customers are dissatisfied")

    parts = [f"{mood} across {total} reviews."]
    if positives:
        parts.append("Frequently praised: " + ", ".join(positives) + ".")
    if complaints:
        parts.append("Common complaints: " + ", ".join(complaints) + ".")
    if not positives and not complaints and top_aspects:
        parts.append("Most discussed: " + ", ".join(top_aspects) + ".")

    return {
        "summary": " ".join(parts),
        "common_positives": positives,
        "common_complaints": complaints,
        "top_aspects": top_aspects,
    }


def keywords(reviews: list[dict], n: int = 10) -> list[str]:
    """Most frequent content words across reviews (stopwords removed)."""
    stop = {"the", "a", "an", "is", "are", "was", "and", "but", "however", "with",
            "for", "this", "that", "it", "of", "to", "in", "on", "my", "i", "very",
            "about", "much", "better", "one", "used", "day", "part", "clearly",
            "expected", "point", "strong", "needs", "work", "exceeded", "expectations"}
    counter: Counter[str] = Counter()
    for r in reviews:
        for tok in preprocessing.tokenize(r.get("review_text", "")):
            if tok not in stop and len(tok) > 2:
                counter[tok] += 1
    return [w for w, _ in counter.most_common(n)]
