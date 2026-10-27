"""Analysis endpoints: sentiment, aspects, summary, trends, authenticity,
rating prediction and optional transformer sentiment."""
from fastapi import APIRouter, HTTPException

from backend import schemas
from backend.services import analysis_service, data_loader
from ml import fake_review, rating, trends, transformer

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


def _require(product_id: str) -> dict:
    a = analysis_service.analyze_product(product_id)
    if a is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return a


@router.get("/{product_id}")
def full_analysis(product_id: str):
    return _require(product_id)


@router.get("/{product_id}/sentiment")
def sentiment(product_id: str):
    a = _require(product_id)
    return {"product_id": product_id, "distribution": a["sentiment_distribution"],
            "positive_share": a["positive_share"], "neutral_share": a["neutral_share"],
            "negative_share": a["negative_share"]}


@router.get("/{product_id}/aspects")
def aspects(product_id: str):
    a = _require(product_id)
    return {"product_id": product_id, "aspects": a["aspects"],
            "strengths": a["strengths"], "weaknesses": a["weaknesses"]}


@router.get("/{product_id}/summary")
def summary(product_id: str):
    a = _require(product_id)
    return {"product_id": product_id, **a["summary"], "keywords": a["keywords"]}


@router.get("/{product_id}/trends")
def product_trends(product_id: str):
    if data_loader.get_product(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return trends.analyze(data_loader.get_reviews(product_id))


@router.get("/{product_id}/authenticity")
def authenticity(product_id: str):
    if data_loader.get_product(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_review.analyze(data_loader.get_reviews(product_id))


@router.post("/predict-rating")
def predict_rating(req: schemas.RatingPredictRequest):
    return rating.predict(req.text)


@router.get("/transformer/status")
def transformer_status():
    return {"enabled": transformer.enabled(), "available": transformer.available(),
            "model": transformer.MODEL_NAME}


@router.post("/transformer/sentiment")
def transformer_sentiment(req: schemas.TransformerRequest):
    return transformer.predict(req.text)
