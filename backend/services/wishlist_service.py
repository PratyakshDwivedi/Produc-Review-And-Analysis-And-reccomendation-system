"""User wishlist (deduplicated)."""
from backend.database.store import get_store
from backend.services import data_loader


def _coll():
    return get_store().collection("wishlist")


def add(user_id: str, product_id: str) -> dict:
    if data_loader.get_product(product_id) is None:
        raise ValueError("Product not found")
    if not _coll().find_one({"user_id": user_id, "product_id": product_id}):
        _coll().insert_one({"user_id": user_id, "product_id": product_id})
    return {"added": product_id}


def remove(user_id: str, product_id: str) -> dict:
    _coll().delete_one({"user_id": user_id, "product_id": product_id})
    return {"removed": product_id}


def list_items(user_id: str) -> list[dict]:
    items = _coll().find({"user_id": user_id})
    products = []
    for it in items:
        p = data_loader.get_product(it["product_id"])
        if p:
            products.append(p)
    return products
