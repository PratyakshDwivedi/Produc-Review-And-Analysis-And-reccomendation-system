"""Time-based review trend analysis (volume, rating, sentiment over months)."""
from collections import defaultdict

from ml import aspects as aspects_mod
from ml import sentiment


def _month(date_str: str) -> str | None:
    if not date_str or len(date_str) < 7:
        return None
    return date_str[:7]  # YYYY-MM


def analyze(reviews: list[dict]) -> dict:
    dated = [r for r in reviews if _month(r.get("date", ""))]
    if not dated:
        return {"available": False, "note": "No dated reviews available; trends cannot be computed.",
                "points": [], "aspect_trends": {}}

    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in dated:
        buckets[_month(r["date"])].append(r)

    points = []
    for month in sorted(buckets):
        rs = buckets[month]
        ratings = [r["rating"] for r in rs if r.get("rating") is not None]
        sents = sentiment.predict_many([r.get("review_text", "") for r in rs])
        total = len(sents)
        points.append({
            "month": month,
            "review_count": len(rs),
            "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
            "positive_share": round(sents.count("positive") / total, 3) if total else 0,
            "negative_share": round(sents.count("negative") / total, 3) if total else 0,
        })

    # aspect score per month for the 3 most-discussed aspects overall
    overall = aspects_mod.aggregate(dated)[:3]
    aspect_trends: dict[str, list] = {}
    for row in overall:
        asp = row["aspect"]
        series = []
        for month in sorted(buckets):
            rows = aspects_mod.aggregate(buckets[month])
            match = next((x for x in rows if x["aspect"] == asp), None)
            series.append({"month": month, "score": match["score"] if match else None})
        aspect_trends[asp] = series

    return {"available": True, "points": points, "aspect_trends": aspect_trends}
