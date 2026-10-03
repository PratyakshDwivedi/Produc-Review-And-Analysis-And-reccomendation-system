"""Loads product and review data from CSV files.

This is the Phase 1 data source. A later phase swaps the CSV source for
MongoDB without changing the route/service interface.
"""
from functools import lru_cache
from typing import Optional

import pandas as pd

from backend import config


@lru_cache(maxsize=1)
def _products_df() -> pd.DataFrame:
    return pd.read_csv(config.PRODUCTS_CSV)


@lru_cache(maxsize=1)
def _reviews_df() -> pd.DataFrame:
    return pd.read_csv(config.REVIEWS_CSV)


def list_products(query: Optional[str] = None) -> list[dict]:
    df = _products_df()
    if query:
        mask = df["name"].str.contains(query, case=False, na=False)
        df = df[mask]
    return df.to_dict(orient="records")


def get_product(product_id: str) -> Optional[dict]:
    df = _products_df()
    match = df[df["product_id"] == product_id]
    if match.empty:
        return None
    return match.iloc[0].to_dict()


def get_reviews(product_id: str) -> list[dict]:
    df = _reviews_df()
    return df[df["product_id"] == product_id].to_dict(orient="records")
