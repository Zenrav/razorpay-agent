from app.agent.state import AgentState

BUY_WORDS = ("buy", "order", "purchase", "get me", "checkout")


def parse_intent(state: AgentState) -> AgentState:
    """Classify the user message as a purchase request or small talk."""
    message = state.get("message", "")
    intent = "buy" if any(word in message.lower() for word in BUY_WORDS) else "chat"
    return {"intent": intent, "log": [{"node": "parse_intent", "intent": intent}]}
