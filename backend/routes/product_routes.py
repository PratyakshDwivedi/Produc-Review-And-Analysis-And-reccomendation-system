"""Product endpoints."""
from fastapi import APIRouter, HTTPException

from backend.services import data_loader

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products(q: str | None = None):
    """List products, optionally filtered by a name search query."""
    return data_loader.list_products(q)


@router.get("/{product_id}")
def get_product(product_id: str):
    product = data_loader.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
