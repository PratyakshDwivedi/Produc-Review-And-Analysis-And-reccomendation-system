"""In-app notifications with read/unread state."""
import uuid
from datetime import datetime, timezone

from backend.database.store import get_store


def _coll():
    return get_store().collection("notifications")


def create(user_id: str, message: str, kind: str = "info", meta: dict | None = None) -> dict:
    note = {
        "id": uuid.uuid4().hex, "user_id": user_id, "message": message,
        "kind": kind, "meta": meta or {}, "read": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _coll().insert_one(note)
    return note


def list_for(user_id: str) -> list[dict]:
    items = _coll().find({"user_id": user_id})
    return sorted(items, key=lambda n: n.get("created_at", ""), reverse=True)


def unread_count(user_id: str) -> int:
    return _coll().count({"user_id": user_id, "read": False})


def mark_read(user_id: str, notification_id: str) -> dict | None:
    return _coll().update_one({"user_id": user_id, "id": notification_id}, {"read": True})


def mark_all_read(user_id: str) -> int:
    count = 0
    for n in _coll().find({"user_id": user_id, "read": False}):
        _coll().update_one({"user_id": user_id, "id": n["id"]}, {"read": True})
        count += 1
    return count
