from fastapi import FastAPI
from app.api.chat_api import router as chat_router

app = FastAPI(
    title="Personal AI Assistant",
    description="Local Jarvis-like assistant for Pop!_OS",
    version="0.1.0"
)

app.include_router(chat_router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "Personal AI Assistant is running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP"
    }