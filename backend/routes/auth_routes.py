"""Authentication: register, login, current user, account update."""
from fastapi import APIRouter, Depends, HTTPException

from backend import schemas
from backend.auth import security
from backend.auth.dependencies import get_current_user
from backend.services import user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(req: schemas.RegisterRequest):
    try:
        user = user_service.register(req.email, req.password, req.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"user": user, "token": security.create_token(user["id"])}


@router.post("/login")
def login(req: schemas.LoginRequest):
    user = user_service.authenticate(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"user": user, "token": security.create_token(user["id"])}


@router.get("/me")
def me(user=Depends(get_current_user)):
    return user


@router.put("/account")
def update_account(req: schemas.AccountUpdate, user=Depends(get_current_user)):
    updated = user_service.update_account(user["id"], req.name)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
