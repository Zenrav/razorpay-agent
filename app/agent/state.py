from typing import Annotated, Any, Dict, List, Optional, TypedDict


def append(left: List[dict], right: List[dict]) -> List[dict]:
    return left + right


class AgentState(TypedDict, total=False):
    """State passed between graph nodes."""

    message: str
    intent: str
    product: Optional[Dict[str, Any]]
    requested_product: Optional[Dict[str, Any]]
    order: Optional[Dict[str, Any]]
    error: Optional[str]
    reply: str
    log: Annotated[List[Dict[str, Any]], append]
