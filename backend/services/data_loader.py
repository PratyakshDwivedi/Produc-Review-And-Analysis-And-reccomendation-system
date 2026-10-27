"""Loads product and review data from CSV files (the demo data source).

Product ratings and review counts are computed from the review data so they
always reflect the actual reviews.
"""
import json
from functools import lru_cache
from typing import Optional

import pandas as pd

from backend import config


@lru_cache(maxsize=1)
def _products_df() -> pd.DataFrame:
    return pd.read_csv(config.PRODUCTS_CSV)


@lru_cache(maxsize=1)
def _reviews_df() -> pd.DataFrame:
    df = pd.read_csv(config.REVIEWS_CSV)
    if "date" in df.columns:
        df["date"] = df["date"].astype(str)
    return df


@lru_cache(maxsize=1)
def _rating_stats() -> dict:
    df = _reviews_df()
    stats = {}
    for pid, grp in df.groupby("product_id"):
        stats[pid] = {
            "rating": round(float(grp["rating"].mean()), 2),
            "review_count": int(len(grp)),
        }
    return stats


def _parse_specs(value) -> dict:
    try:
        return json.loads(value) if isinstance(value, str) else {}
    except Exception:
        return {}


def _product_record(row: dict) -> dict:
    stats = _rating_stats().get(row["product_id"], {"rating": 0.0, "review_count": 0})
    return {
        "product_id": row["product_id"],
        "name": row["name"],
        "brand": row.get("brand", ""),
        "category": row["category"],
        "price": int(row["price"]),
        "description": row.get("description", ""),
        "specs": _parse_specs(row.get("specs")),
        "rating": stats["rating"],
        "review_count": stats["review_count"],
    }


def list_products(query: Optional[str] = None, category: Optional[str] = None) -> list[dict]:
    df = _products_df()
    if query:
        mask = (df["name"].str.contains(query, case=False, na=False)
                | df["brand"].str.contains(query, case=False, na=False))
        df = df[mask]
    if category:
        df = df[df["category"].str.lower() == category.lower()]
    return [_product_record(r) for r in df.to_dict(orient="records")]


def get_product(product_id: str) -> Optional[dict]:
    df = _products_df()
    match = df[df["product_id"] == product_id]
    if match.empty:
        return None
    return _product_record(match.iloc[0].to_dict())


def get_reviews(product_id: str) -> list[dict]:
    df = _reviews_df()
    return df[df["product_id"] == product_id].to_dict(orient="records")


def all_reviews() -> list[dict]:
    return _reviews_df().to_dict(orient="records")


def categories() -> list[str]:
    return sorted(_products_df()["category"].unique().tolist())
