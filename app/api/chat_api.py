from pydantic import BaseModel
from fastapi import APIRouter

from app.core.orchestrator import AssistantOrchestrator


router = APIRouter()
orchestrator = AssistantOrchestrator()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):
    return await orchestrator.chat(request.message)