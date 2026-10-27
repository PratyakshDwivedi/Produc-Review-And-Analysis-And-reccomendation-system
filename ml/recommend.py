"""Natural-language, explainable recommendation.

Combines TF-IDF text relevance with aspect-sentiment matching, overall rating
and sentiment. The returned match score is a transparent relevance score in
[0, 100], NOT a probability that the user will like the product.
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ml.lexicon import ASPECT_KEYWORDS

_BUDGET = re.compile(r"(?:under|below|less than|within|max|budget of)\s*\$?\s*(\d+)")


def parse_query(query: str) -> dict:
    low = query.lower()
    aspects = [a for a, kws in ASPECT_KEYWORDS.items() if any(k in low for k in kws)]
    m = _BUDGET.search(low)
    budget = int(m.group(1)) if m else None
    categories = [c for c in ("smartphone", "phone", "laptop", "headphones", "earbuds",
                              "smartwatch", "watch") if c in low]
    cat_map = {"phone": "smartphone", "earbuds": "headphones", "watch": "smartwatch"}
    categories = sorted({cat_map.get(c, c) for c in categories})
    return {"aspects": aspects, "budget": budget, "categories": categories}


def _aspect_score(analysis: dict, aspect: str):
    for row in analysis.get("aspects", []):
        if row["aspect"] == aspect and row["total"] > 0:
            return row["score"]  # [-1, 1]
    return None


def recommend(query: str, analyses: list[dict], top_k: int = 5) -> dict:
    prefs = parse_query(query)
    candidates = analyses
    if prefs["categories"]:
        filtered = [a for a in analyses if a["category"] in prefs["categories"]]
        candidates = filtered or analyses

    # TF-IDF relevance between the query and each product profile.
    profiles = [
        f"{a['name']} {a['category']} {a.get('description', '')} "
        + " ".join(r["aspect"] for r in a.get("aspects", []) if r["score"] > 0)
        for a in candidates
    ]
    relevance = [0.0] * len(candidates)
    if profiles:
        vec = TfidfVectorizer(stop_words="english")
        matrix = vec.fit_transform(profiles + [query])
        relevance = cosine_similarity(matrix[-1], matrix[:-1]).flatten().tolist()

    results = []
    for a, rel in zip(candidates, relevance):
        reasons, matched, evidence = [], [], []
        aspect_vals = []
        for asp in prefs["aspects"]:
            sc = _aspect_score(a, asp)
            if sc is None:
                continue
            aspect_vals.append((sc + 1) / 2)  # -> [0,1]
            if sc >= 0.3:
                matched.append(asp)
                reasons.append(f"{asp.capitalize()} reviews are predominantly positive.")
            elif sc <= -0.3:
                reasons.append(f"{asp.capitalize()} feedback is largely negative.")
            else:
                reasons.append(f"{asp.capitalize()} feedback is mixed.")

        aspect_component = sum(aspect_vals) / len(aspect_vals) if aspect_vals else a.get("positive_share", 0.5)
        rating_component = a.get("rating", 0) / 5
        budget_component = 1.0
        if prefs["budget"] is not None:
            if a["price"] <= prefs["budget"]:
                budget_component = 1.0
                reasons.append(f"Within your ${prefs['budget']} budget (${a['price']}).")
            else:
                budget_component = 0.3
                reasons.append(f"Over your ${prefs['budget']} budget (${a['price']}).")

        score = 100 * (0.45 * aspect_component + 0.2 * rating_component
                       + 0.15 * a.get("positive_share", 0.5) + 0.1 * min(rel * 3, 1) + 0.1 * budget_component)
        reasons.append(f"Overall rating {a.get('rating', 0)} from {a.get('review_count', 0)} reviews.")

        # supporting evidence: up to 2 real review snippets mentioning matched aspects
        for snip in a.get("evidence", []):
            if any(asp in snip.lower() for asp in (matched or prefs["aspects"])):
                evidence.append(snip)
            if len(evidence) >= 2:
                break

        results.append({
            "product_id": a["product_id"], "name": a["name"], "category": a["category"],
            "price": a["price"], "rating": a.get("rating", 0),
            "match_score": round(score, 1),
            "matched_preferences": matched,
            "strengths": a.get("strengths", []), "weaknesses": a.get("weaknesses", []),
            "reasons": reasons, "evidence": evidence,
        })

    results.sort(key=lambda r: -r["match_score"])
    return {"query": query, "parsed": prefs, "results": results[:top_k],
            "note": "match_score is a relevance score (0-100), not a probability you will like the product."}
