"""Transparent, confidence-adjusted category ranking."""


def rank(analyses: list[dict], preferred_aspects: list[str] | None = None) -> dict:
    """Rank products using a Bayesian-adjusted rating plus sentiment evidence.

    Bayesian average dampens products with very few reviews so a single high
    rating cannot dominate:  (C*m + sum_ratings) / (C + n)
    """
    preferred_aspects = preferred_aspects or []
    if not analyses:
        return {"ranking": [], "methodology": "No products to rank."}

    n_all = [a.get("review_count", 0) for a in analyses]
    ratings = [a.get("rating", 0) for a in analyses]
    global_mean = sum(ratings) / len(ratings) if ratings else 0
    C = max(5, (sum(n_all) / len(n_all)) if n_all else 5)  # confidence prior

    ranked = []
    for a in analyses:
        n = a.get("review_count", 0)
        bayes = (C * global_mean + a.get("rating", 0) * n) / (C + n) if (C + n) else 0
        pos_share = a.get("positive_share", 0.5)
        pref_score = 0.0
        if preferred_aspects:
            vals = [r["score"] for r in a.get("aspects", []) if r["aspect"] in preferred_aspects and r["total"] > 0]
            pref_score = (sum(vals) / len(vals) + 1) / 2 if vals else 0.5
        score = 0.55 * (bayes / 5) + 0.25 * pos_share + 0.2 * pref_score
        ranked.append({
            "product_id": a["product_id"], "name": a["name"], "category": a["category"],
            "price": a["price"], "rating": a.get("rating", 0), "review_count": n,
            "adjusted_rating": round(bayes, 2), "positive_share": pos_share,
            "rank_score": round(score * 100, 1),
        })
    ranked.sort(key=lambda x: -x["rank_score"])
    for i, r in enumerate(ranked, 1):
        r["rank"] = i
    return {
        "ranking": ranked,
        "methodology": ("Ranked by a confidence-adjusted (Bayesian) rating that dampens "
                        "products with few reviews, combined with positive-sentiment share"
                        + (" and your preferred aspects." if preferred_aspects else ".")),
    }
