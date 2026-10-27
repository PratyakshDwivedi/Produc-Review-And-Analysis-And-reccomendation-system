"""Per-user recommendation preferences."""
from backend.database.store import get_store

DEFAULTS = {"category": None, "budget": None, "preferred_aspects": [], "min_rating": 0}


def _coll():
    return get_store().collection("preferences")


def get_preferences(user_id: str) -> dict:
    doc = _coll().find_one({"user_id": user_id})
    if not doc:
        return {"user_id": user_id, **DEFAULTS}
    return {k: doc.get(k, v) for k, v in {"user_id": user_id, **DEFAULTS}.items()}


def set_preferences(user_id: str, prefs: dict) -> dict:
    patch = {k: prefs[k] for k in DEFAULTS if k in prefs}
    _coll().update_one({"user_id": user_id}, {"user_id": user_id, **patch}, upsert=True)
    return get_preferences(user_id)
