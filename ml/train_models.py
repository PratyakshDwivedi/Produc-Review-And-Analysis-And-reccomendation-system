"""Train and persist the baseline sentiment and rating-prediction models.

Run:  python ml/train_models.py
Reads data/raw/reviews.csv, trains TF-IDF pipelines, prints evaluation metrics,
and saves artifacts to models/.
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import joblib

from backend import config
from ml import preprocessing
from ml.sentiment import label_from_rating


def _load():
    df = pd.read_csv(config.REVIEWS_CSV)
    df["clean"] = df["review_text"].map(preprocessing.clean_text)
    df = df[df["clean"].str.len() > 0]
    return df


def train_sentiment(df) -> dict:
    y = df["rating"].map(label_from_rating)
    X = df["clean"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    pipe.fit(Xtr, ytr)
    pred = pipe.predict(Xte)
    metrics = {
        "accuracy": round(float(accuracy_score(yte, pred)), 3),
        "f1_macro": round(float(f1_score(yte, pred, average="macro")), 3),
        "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
    }
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, config.MODELS_DIR / "sentiment_model.pkl")
    return metrics


def train_rating(df) -> dict:
    y = df["rating"].astype(float)
    X = df["clean"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ("reg", Ridge(alpha=1.0)),
    ])
    pipe.fit(Xtr, ytr)
    pred = np.clip(pipe.predict(Xte), 1, 5)
    metrics = {"mae": round(float(mean_absolute_error(yte, pred)), 3),
               "n_train": int(len(Xtr)), "n_test": int(len(Xte))}
    joblib.dump(pipe, config.MODELS_DIR / "rating_model.pkl")
    return metrics


if __name__ == "__main__":
    df = _load()
    print(f"Loaded {len(df)} reviews")
    print("Sentiment:", train_sentiment(df))
    print("Rating:", train_rating(df))
    print(f"Saved models to {config.MODELS_DIR}")
