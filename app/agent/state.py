from typing import Annotated, Any, TypedDict


def append(left: list, right: list) -> list:
    return left + right


class AgentState(TypedDict, total=False):
    """State passed between graph nodes."""

    message: str
    intent: str
    product: dict[str, Any] | None
    requested_product: dict[str, Any] | None
    order: dict[str, Any] | None
    error: str | None
    reply: str
    log: Annotated[list[dict[str, Any]], append]
