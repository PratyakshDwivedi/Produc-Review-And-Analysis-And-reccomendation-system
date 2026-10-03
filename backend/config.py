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
PRODUCTS_CSV = RAW_DATA_DIR / "products.csv"
REVIEWS_CSV = RAW_DATA_DIR / "reviews.csv"

# MongoDB (configured now, actually integrated in a later phase).
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "product_review_analysis")

# CORS origins for the React dev server.
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
