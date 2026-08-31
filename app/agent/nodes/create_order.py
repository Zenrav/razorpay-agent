import uuid

from app.agent.state import AgentState
from app.audit.logger import log_action
from app.config import SPEND_LIMIT_INR
from app.payments import razorpay_client


def create_order(state: AgentState) -> AgentState:
    """Create a Razorpay order, refusing anything above the configured spend limit."""
    product = state.get("product")
    if not product:
        return {"order": None, "log": [{"node": "create_order", "skipped": True}]}

    amount = product["price_inr"]
    if amount > SPEND_LIMIT_INR:
        log_action("order_blocked", f"amount exceeds spend limit of INR {SPEND_LIMIT_INR}", amount)
        return {
            "order": None,
            "error": "spend_limit_exceeded",
            "log": [{"node": "create_order", "blocked": True, "amount": amount}],
        }

    try:
        order = razorpay_client.create_order(amount, receipt=f"rcpt_{uuid.uuid4().hex[:12]}", notes={"sku": product["id"]})
    except Exception as exc:
        log_action("order_failed", str(exc), amount)
        return {
            "order": None,
            "error": "payment_provider_error",
            "log": [{"node": "create_order", "failed": True, "amount": amount}],
        }

    log_action("order_created", f"order for {product['name']}", amount)
    return {"order": order, "error": None, "log": [{"node": "create_order", "order_id": order.get("id")}]}
