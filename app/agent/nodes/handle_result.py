from app.agent.state import AgentState
from app.config import SPEND_LIMIT_INR

MESSAGES = {
    "no_matching_product": "I could not find that in the catalog. Try a t-shirt, hoodie, loafers, headphones, earbuds or a laptop.",
    "out_of_stock": "That item is out of stock and I could not find a comparable substitute, so I did not place an order.",
    "spend_limit_exceeded": f"That purchase is above your spend limit of INR {SPEND_LIMIT_INR}, so I did not place it.",
    "payment_provider_error": "The payment provider rejected the order. Nothing was charged.",
}


def handle_result(state: AgentState) -> AgentState:
    """Turn the graph outcome into a user-facing reply."""
    if state.get("intent") != "buy":
        reply = "I can buy things for you — tell me what you want to order."
    elif error := state.get("error"):
        reply = MESSAGES.get(error, "Something went wrong, so I did not place the order.")
        if error == "spend_limit_exceeded" and (requested := state.get("requested_product")):
            reply = f"{requested['name']} is out of stock, and the substitute I found is above your spend limit, so I did not place it."
    else:
        product = state["product"]
        order = state["order"]
        reply = f"Created a Razorpay order for {product['name']} (INR {product['price_inr']}). Order id: {order.get('id')}."
        if requested := state.get("requested_product"):
            reply = f"{requested['name']} is out of stock, so I ordered {product['name']} (INR {product['price_inr']}) instead. Order id: {order.get('id')}."

    return {"reply": reply, "log": [{"node": "handle_result", "reply": reply}]}
