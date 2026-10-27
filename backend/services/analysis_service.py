"""Orchestrates per-product NLP analysis and caches the result in memory.

Combines sentiment distribution, aspect-based sentiment, strengths/weaknesses
and an extractive summary. Everything is computed from the review text.
"""
from functools import lru_cache

from backend.services import data_loader
from ml import aspects, sentiment, summarize


@lru_cache(maxsize=256)
def analyze_product(product_id: str) -> dict | None:
    product = data_loader.get_product(product_id)
    if product is None:
        return None
    reviews = data_loader.get_reviews(product_id)
    texts = [r.get("review_text", "") for r in reviews]

    sentiments = sentiment.predict_many(texts)
    total = len(sentiments) or 1
    dist = {s: sentiments.count(s) for s in ("positive", "neutral", "negative")}
    shares = {f"{k}_share": round(v / total, 3) for k, v in dist.items()}

    aspect_rows = aspects.aggregate(reviews)
    strengths, weaknesses = aspects.strengths_weaknesses(aspect_rows)
    summary = summarize.summarize(reviews, aspect_rows)

    evidence = [t for t in texts if t][:6]

    return {
        **product,
        "sentiment_distribution": dist,
        **shares,
        "aspects": aspect_rows,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "summary": summary,
        "keywords": summarize.keywords(reviews),
        "evidence": evidence,
    }


def all_analyses() -> list[dict]:
    out = []
    for p in data_loader.list_products():
        a = analyze_product(p["product_id"])
        if a:
            out.append(a)
    return out


def clear_cache() -> None:
    analyze_product.cache_clear()
