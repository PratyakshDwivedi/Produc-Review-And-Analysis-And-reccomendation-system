"""Optional transformer (DistilBERT) sentiment.

Disabled by default so local startup never triggers a large model download.
Enable by installing `transformers`+`torch` and setting ENABLE_TRANSFORMER=1.
The baseline TF-IDF model (ml/sentiment.py) is always the default; this is only
used when it is genuinely available. We never claim transformer inference when
the baseline is actually running.
"""
import os
from functools import lru_cache

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"


def enabled() -> bool:
    return os.getenv("ENABLE_TRANSFORMER", "0") == "1"


@lru_cache(maxsize=1)
def _pipe():
    if not enabled():
        return None
    try:
        from transformers import pipeline  # imported lazily on purpose
        return pipeline("sentiment-analysis", model=MODEL_NAME)
    except Exception:
        return None


def available() -> bool:
    """True only if enabled AND the pipeline actually loaded."""
    return _pipe() is not None


def predict(text: str) -> dict:
    pipe = _pipe()
    if pipe is None:
        return {"available": False,
                "note": "Transformer disabled or unavailable; set ENABLE_TRANSFORMER=1 and install transformers+torch."}
    out = pipe(text[:512])[0]
    label = out["label"].lower()  # POSITIVE / NEGATIVE
    return {"available": True, "model": MODEL_NAME, "sentiment": label,
            "confidence": round(float(out["score"]), 4)}
