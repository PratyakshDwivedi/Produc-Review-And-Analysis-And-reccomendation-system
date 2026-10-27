"""Rating prediction from review text (TF-IDF + Ridge regression)."""
from functools import lru_cache
from pathlib import Path

import joblib

from ml import preprocessing


def _model_path() -> Path:
    from backend import config
    return config.MODELS_DIR / "rating_model.pkl"


@lru_cache(maxsize=1)
def _load():
    path = _model_path()
    if path.exists():
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None


def available() -> bool:
    return _load() is not None


def predict(text: str) -> dict:
    model = _load()
    cleaned = preprocessing.clean_text(text)
    if model is None or not cleaned:
        return {"predicted_rating": None,
                "note": "Rating model not trained. Run ml/train_models.py."}
    raw = float(model.predict([cleaned])[0])
    return {
        "predicted_rating": round(max(1.0, min(5.0, raw)), 2),
        "note": "Estimated from review text; it may differ from the customer's actual star rating.",
    }
