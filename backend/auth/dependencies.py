"""FastAPI auth dependencies."""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.auth import security
from backend.services import user_service

_bearer = HTTPBearer(auto_error=False)


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> dict:
    if creds is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = security.decode_token(creds.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {"id": user["id"], "email": user["email"], "name": user.get("name", "")}


def get_optional_user(creds: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> dict | None:
    if creds is None:
        return None
    user_id = security.decode_token(creds.credentials)
    if not user_id:
        return None
    user = user_service.get_by_id(user_id)
    return {"id": user["id"], "email": user["email"], "name": user.get("name", "")} if user else None
