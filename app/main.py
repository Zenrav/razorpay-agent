from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agent.graph import get_graph
from app.audit.logger import DECISIONS

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Razorpay Agentic Checkout")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    order_id: Optional[str] = None
    log: List[dict]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = get_graph().invoke({"message": request.message, "log": []})
    order = result.get("order") or {}
    return ChatResponse(reply=result["reply"], order_id=order.get("id"), log=result.get("log", []))


@app.get("/audit")
def audit() -> List[dict]:
    """The in-memory audit trail of every decision made since startup."""
    return DECISIONS
