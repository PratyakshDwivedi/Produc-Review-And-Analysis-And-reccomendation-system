"""Pydantic request/response schemas."""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AccountUpdate(BaseModel):
    name: str


class RecommendRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = 5


class PreferencesRequest(BaseModel):
    category: str | None = None
    budget: int | None = None
    preferred_aspects: list[str] = []
    min_rating: float = 0


class WishlistRequest(BaseModel):
    product_id: str


class AlertCreate(BaseModel):
    product_id: str
    target_price: float = Field(gt=0)


class AlertUpdate(BaseModel):
    target_price: float | None = None
    active: bool | None = None


class PriceRecord(BaseModel):
    product_id: str
    price: int = Field(gt=0)


class RatingPredictRequest(BaseModel):
    text: str = Field(min_length=1)


class TransformerRequest(BaseModel):
    text: str = Field(min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[dict] = []
