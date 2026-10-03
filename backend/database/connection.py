"""MongoDB connection helper.

Configured in Phase 1 but not required for the app to run; the active data
source is CSV (see services/data_loader.py). Database integration happens in a
later phase. The client is created lazily so the API starts even when MongoDB
is not running.
"""
from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

from backend import config


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=2000)


def get_db() -> Database:
    return get_client()[config.MONGO_DB_NAME]


def ping() -> bool:
    """Return True if MongoDB is reachable, False otherwise."""
    try:
        get_client().admin.command("ping")
        return True
    except Exception:
        return False
