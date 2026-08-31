from app.agent.state import AgentState
from app.audit.logger import log_action
from app.catalog import products


def find_product(state: AgentState) -> AgentState:
    """Resolve the user message to an in-stock catalog product, substituting when needed."""
    if state.get("intent") != "buy":
        return {"product": None, "log": [{"node": "find_product", "skipped": True}]}

    product = products.search(state.get("message", ""))
    if not product:
        log_action("product_not_found", f"nothing in the catalog matches {state.get('message', '')!r}")
        return {"product": None, "error": "no_matching_product", "log": [{"node": "find_product", "product": None}]}

    if product["in_stock"]:
        return {"product": product, "log": [{"node": "find_product", "product": product["id"]}]}

    substitute = products.find_substitute(product)
    if not substitute:
        log_action("out_of_stock", f"{product['name']} is out of stock and has no substitute", product["price_inr"])
        return {
            "product": None,
            "error": "out_of_stock",
            "requested_product": product,
            "log": [{"node": "find_product", "out_of_stock": product["id"], "substitute": None}],
        }

    log_action("substituted", f"{product['name']} is out of stock, offering {substitute['name']}", substitute["price_inr"])
    return {
        "product": substitute,
        "requested_product": product,
        "log": [{"node": "find_product", "out_of_stock": product["id"], "substitute": substitute["id"]}],
    }
