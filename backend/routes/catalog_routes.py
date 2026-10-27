"""Products, categories, reviews (with filtering/pagination) and comparison."""
from fastapi import APIRouter, HTTPException, Query

from backend.services import analysis_service, data_loader
from ml import aspects as aspects_mod
from ml import sentiment

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/categories")
def categories():
    return data_loader.categories()


@router.get("/products")
def list_products(q: str | None = None, category: str | None = None):
    return data_loader.list_products(q, category)


@router.get("/products/{product_id}")
def get_product(product_id: str):
    product = data_loader.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/reviews/{product_id}")
def get_reviews(
    product_id: str,
    sentiment_filter: str | None = Query(None, alias="sentiment"),
    aspect: str | None = None,
    min_rating: int | None = Query(None, ge=1, le=5),
    max_rating: int | None = Query(None, ge=1, le=5),
    q: str | None = None,
    sort: str = "recent",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    if data_loader.get_product(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    reviews = data_loader.get_reviews(product_id)

    # enrich each review with sentiment + aspect map
    sents = sentiment.predict_many([r.get("review_text", "") for r in reviews])
    enriched = []
    for r, s in zip(reviews, sents):
        enriched.append({**r, "sentiment": s, "aspects": aspects_mod.analyze_review(r.get("review_text", ""))})

    def keep(r):
        if sentiment_filter and r["sentiment"] != sentiment_filter:
            return False
        if aspect and aspect not in r["aspects"]:
            return False
        if min_rating and r["rating"] < min_rating:
            return False
        if max_rating and r["rating"] > max_rating:
            return False
        if q and q.lower() not in r.get("review_text", "").lower():
            return False
        return True

    filtered = [r for r in enriched if keep(r)]
    if sort == "rating_high":
        filtered.sort(key=lambda r: -r["rating"])
    elif sort == "rating_low":
        filtered.sort(key=lambda r: r["rating"])
    else:  # recent
        filtered.sort(key=lambda r: r.get("date", ""), reverse=True)

    total = len(filtered)
    start = (page - 1) * page_size
    return {
        "total": total, "page": page, "page_size": page_size,
        "items": filtered[start:start + page_size],
    }


@router.get("/compare")
def compare(ids: str = Query(..., description="comma-separated product ids")):
    id_list = [i.strip() for i in ids.split(",") if i.strip()][:3]
    if len(id_list) < 2:
        raise HTTPException(status_code=400, detail="Provide 2-3 product ids")
    results = []
    for pid in id_list:
        a = analysis_service.analyze_product(pid)
        if a is None:
            raise HTTPException(status_code=404, detail=f"Product {pid} not found")
        results.append({
            "product_id": a["product_id"], "name": a["name"], "brand": a["brand"],
            "category": a["category"], "price": a["price"], "rating": a["rating"],
            "review_count": a["review_count"], "specs": a["specs"],
            "sentiment_distribution": a["sentiment_distribution"],
            "positive_share": a["positive_share"],
            "aspects": {r["aspect"]: r["score"] for r in a["aspects"]},
            "strengths": a["strengths"], "weaknesses": a["weaknesses"],
        })
    return {"products": results}
