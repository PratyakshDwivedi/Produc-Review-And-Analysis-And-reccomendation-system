"""Price tracking.

DEMO MODE: price history is generated deterministically from each product's
base price (seeded by product_id). It is clearly labeled demo data and is NOT a
live marketplace feed. A manual price record can be added via record_price();
a real provider could be plugged into current_price() later.
"""
import random
from datetime import date, timedelta

from backend.database.store import get_store
from backend.services import data_loader

ANCHOR = date(2025, 10, 1)


def _coll():
    return get_store().collection("price_overrides")


def _demo_history(product_id: str, base: int) -> list[dict]:
    rnd = random.Random(hash(product_id) & 0xFFFFFFFF)
    history = []
    price = base
    for i in range(12):
        d = (ANCHOR - timedelta(days=(11 - i) * 30)).isoformat()
        price = max(int(base * 0.7), int(price * (1 + rnd.uniform(-0.06, 0.04))))
        history.append({"date": d, "price": price})
    history[-1]["price"] = base  # latest equals catalog price
    return history


def history(product_id: str) -> dict:
    product = data_loader.get_product(product_id)
    if product is None:
        return {}
    hist = _demo_history(product_id, product["price"])
    # merge any manually recorded prices
    for rec in _coll().find({"product_id": product_id}):
        hist.append({"date": rec["date"], "price": rec["price"]})
    hist.sort(key=lambda x: x["date"])
    prices = [h["price"] for h in hist]
    return {
        "product_id": product_id,
        "name": product["name"],
        "current_price": hist[-1]["price"],
        "min_price": min(prices),
        "max_price": max(prices),
        "change": hist[-1]["price"] - hist[0]["price"],
        "history": hist,
        "mode": "demo",
        "note": "Demo price history generated locally; not a live price feed.",
    }


def current_price(product_id: str) -> int | None:
    h = history(product_id)
    return h.get("current_price")


def record_price(product_id: str, price: int) -> dict:
    if data_loader.get_product(product_id) is None:
        raise ValueError("Product not found")
    rec = {"product_id": product_id, "price": int(price), "date": date.today().isoformat()}
    _coll().insert_one(rec)
    return rec
