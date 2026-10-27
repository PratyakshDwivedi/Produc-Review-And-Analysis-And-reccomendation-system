"""Application configuration loaded from environment variables."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root (one level above the backend package).
BASE_DIR = Path(__file__).resolve().parent.parent

# Data locations.
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PRODUCTS_CSV = RAW_DATA_DIR / "products.csv"
REVIEWS_CSV = RAW_DATA_DIR / "reviews.csv"

# Trained ML artifacts and local JSON fallback store.
MODELS_DIR = Path(os.getenv("MODELS_DIR", BASE_DIR / "models"))
STORE_DIR = Path(os.getenv("STORE_DIR", DATA_DIR / "store"))

# Built frontend (served by FastAPI as a single app when present).
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

# MongoDB (optional). When unreachable, the app falls back to a local JSON store.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_review_analysis")
USE_MONGO = os.getenv("USE_MONGO", "auto")  # "auto" | "1" | "0"

# Auth (JWT). Override JWT_SECRET in .env for production.
JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

# CORS origins for the React dev server.
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
