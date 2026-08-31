from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.graph import get_graph

app = FastAPI(title="Razorpay Agentic Checkout")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    order_id: str | None = None
    log: list[dict]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = get_graph().invoke({"message": request.message, "log": []})
    order = result.get("order") or {}
    return ChatResponse(reply=result["reply"], order_id=order.get("id"), log=result.get("log", []))
