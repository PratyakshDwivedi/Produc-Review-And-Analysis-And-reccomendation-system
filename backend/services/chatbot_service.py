"""Local retrieval-based product assistant (no external LLM required).

Answers questions using the computed product/review/aspect data. When an
external LLM is configured it could be added behind an env flag, but by default
this is a transparent retrieval assistant - it never pretends to be an LLM.
"""
from backend.services import analysis_service, data_loader
from ml import recommend
from ml.lexicon import ASPECT_KEYWORDS


def _find_products(text: str, analyses: list[dict]) -> list[dict]:
    low = text.lower()
    return [a for a in analyses if a["name"].lower() in low]


def _aspects_in(text: str) -> list[str]:
    low = text.lower()
    return [a for a, kws in ASPECT_KEYWORDS.items() if any(k in low for k in kws)]


def answer(query: str, history: list[dict] | None = None) -> dict:
    low = query.lower().strip()
    analyses = analysis_service.all_analyses()

    if not low:
        return {"answer": "Ask me about products, reviews, aspects, comparisons or recommendations.", "data": {}}

    named = _find_products(query, analyses)
    aspects = _aspects_in(query)

    # Compare two or more named products
    if ("compare" in low or " vs " in low or " versus " in low) and len(named) >= 2:
        lines = []
        for a in named[:3]:
            lines.append(f"{a['name']}: rating {a['rating']}, strengths {', '.join(a['strengths']) or 'n/a'}, "
                         f"weaknesses {', '.join(a['weaknesses']) or 'n/a'}.")
        return {"answer": "Here is how they compare:\n" + "\n".join(lines),
                "data": {"product_ids": [a["product_id"] for a in named[:3]]}}

    # Complaints / weaknesses about a specific product
    if named and any(w in low for w in ("complaint", "complaints", "problem", "issues", "wrong", "bad")):
        a = named[0]
        comps = a["summary"]["common_complaints"] or a["weaknesses"]
        msg = (f"Common complaints about {a['name']}: {', '.join(comps)}." if comps
               else f"No significant recurring complaints found for {a['name']}.")
        return {"answer": msg, "data": {"product_id": a["product_id"], "weaknesses": a["weaknesses"]}}

    # Is a specific product worth it?
    if named and ("worth" in low or "should i" in low or "good" in low):
        a = named[0]
        return {"answer": f"{a['name']} has a {a['rating']} rating from {a['review_count']} reviews. "
                          f"{a['summary']['summary']}",
                "data": {"product_id": a["product_id"]}}

    # Best product for an aspect
    if aspects and any(w in low for w in ("best", "which", "top", "most", "recommend", "suggest", "good", "want")):
        rec = recommend.recommend(query, analyses, top_k=3)
        if rec["results"]:
            top = rec["results"][0]
            reasons = "; ".join(top["reasons"][:2])
            return {"answer": f"For {', '.join(aspects)}, I'd suggest {top['name']} "
                              f"(match {top['match_score']}). {reasons}",
                    "data": {"recommendation": rec}}

    # Fallback: natural-language recommendation
    rec = recommend.recommend(query, analyses, top_k=3)
    if rec["results"] and rec["parsed"]["aspects"]:
        names = ", ".join(r["name"] for r in rec["results"])
        return {"answer": f"Based on your request, consider: {names}.", "data": {"recommendation": rec}}

    return {"answer": "I can help with product search, sentiment, aspects, comparisons, and recommendations. "
                      "Try: 'Which phone has the best camera?' or 'Recommend headphones under $150'.",
            "data": {"products": [a["name"] for a in analyses[:6]]}}
