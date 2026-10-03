"""Review endpoints."""
from fastapi import APIRouter, HTTPException

from backend.services import data_loader

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.get("/{product_id}")
def get_reviews(product_id: str):
    """Return all reviews for a product."""
    if data_loader.get_product(product_id) is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return data_loader.get_reviews(product_id)
