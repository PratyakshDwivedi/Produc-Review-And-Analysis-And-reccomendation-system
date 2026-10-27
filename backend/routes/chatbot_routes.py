"""AI product assistant (local retrieval)."""
from fastapi import APIRouter

from backend import schemas
from backend.services import chatbot_service

router = APIRouter(prefix="/api", tags=["chatbot"])


@router.post("/chat")
def chat(req: schemas.ChatRequest):
    result = chatbot_service.answer(req.message, req.history)
    return {"reply": result["answer"], "data": result.get("data", {})}
