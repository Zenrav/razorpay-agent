from app.agent.state import AgentState
from app.catalog import products


def find_product(state: AgentState) -> AgentState:
    """Resolve the user message to a catalog product."""
    if state.get("intent") != "buy":
        return {"product": None, "log": [{"node": "find_product", "skipped": True}]}

    product = products.search(state.get("message", ""))
    error = None if product else "no_matching_product"
    return {
        "product": product,
        "error": error,
        "log": [{"node": "find_product", "product": product["id"] if product else None}],
    }
