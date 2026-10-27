"""User registration, authentication and account management."""
import uuid

from backend.auth import security
from backend.database.store import get_store


def _users():
    return get_store().collection("users")


def _public(user: dict) -> dict:
    return {"id": user["id"], "email": user["email"], "name": user.get("name", "")}


def get_by_email(email: str) -> dict | None:
    return _users().find_one({"email": email.lower()})


def get_by_id(user_id: str) -> dict | None:
    return _users().find_one({"id": user_id})


def register(email: str, password: str, name: str = "") -> dict:
    email = email.lower().strip()
    if get_by_email(email):
        raise ValueError("An account with this email already exists.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
    user = {
        "id": uuid.uuid4().hex,
        "email": email,
        "name": name.strip(),
        "password_hash": security.hash_password(password),
    }
    _users().insert_one(user)
    return _public(user)


def authenticate(email: str, password: str) -> dict | None:
    user = get_by_email(email.lower().strip())
    if not user or not security.verify_password(password, user["password_hash"]):
        return None
    return _public(user)


def update_account(user_id: str, name: str | None = None) -> dict | None:
    patch = {}
    if name is not None:
        patch["name"] = name.strip()
    if not patch:
        user = get_by_id(user_id)
        return _public(user) if user else None
    updated = _users().update_one({"id": user_id}, patch)
    return _public(updated) if updated else None
