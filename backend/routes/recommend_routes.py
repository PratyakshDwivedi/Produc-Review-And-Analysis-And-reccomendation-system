"""Recommendation, category ranking and personalized recommendation."""
from fastapi import APIRouter, Depends, Query

from backend import schemas
from backend.auth.dependencies import get_optional_user
from backend.services import analysis_service, preference_service
from ml import ranking, recommend

router = APIRouter(prefix="/api", tags=["recommend"])


@router.post("/recommend")
def recommend_products(req: schemas.RecommendRequest):
    return recommend.recommend(req.query, analysis_service.all_analyses(), top_k=req.top_k)


@router.get("/rankings")
def category_rankings(category: str | None = None, preferred_aspects: str | None = Query(None)):
    analyses = analysis_service.all_analyses()
    if category:
        analyses = [a for a in analyses if a["category"].lower() == category.lower()]
    prefs = [a.strip() for a in preferred_aspects.split(",")] if preferred_aspects else []
    return ranking.rank(analyses, prefs)


@router.get("/personalized")
def personalized(user=Depends(get_optional_user)):
    analyses = analysis_service.all_analyses()
    if user is None:
        # guest default: overall top ranking
        return {"personalized": False, **ranking.rank(analyses)}
    prefs = preference_service.get_preferences(user["id"])
    filtered = analyses
    if prefs.get("category"):
        filtered = [a for a in analyses if a["category"] == prefs["category"]] or analyses
    if prefs.get("budget"):
        within = [a for a in filtered if a["price"] <= prefs["budget"]]
        filtered = within or filtered
    result = ranking.rank(filtered, prefs.get("preferred_aspects", []))
    return {"personalized": True, "preferences": prefs, **result}
