# razorpay-agentic-checkout

A chat agent that can actually buy things. You tell it what you want, a LangGraph
agent resolves the product, checks a spend limit, and creates a Razorpay
(test-mode) order — writing every decision to an append-only audit trail.

Demo video: _TODO — add link_

![Architecture](demo/architecture.png)

## How it works

A single `POST /chat` endpoint runs a four-node LangGraph state machine:

| Node | Responsibility |
| --- | --- |
| `parse_intent` | Is the user trying to buy something, or just chatting? |
| `find_product` | Resolve the message against the hardcoded catalog |
| `create_order` | Enforce the spend limit, then create a Razorpay order |
| `handle_result` | Confirm the order, or explain the refusal gracefully |

Guardrails: purchases above `SPEND_LIMIT_INR` are refused before any call to
Razorpay, and every action (`order_created`, `order_blocked`, `order_failed`) is
appended to `audit_log.jsonl` with a reason, amount and timestamp.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your Razorpay test keys
uvicorn app.main:app --reload
```

## Usage

```bash
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message": "buy me the wireless headphones"}'
```

See [demo/demo_script.md](demo/demo_script.md) for the full walkthrough,
including the blocked-purchase and unknown-product paths.

## Configuration

| Variable | Description |
| --- | --- |
| `RAZORPAY_KEY_ID` | Razorpay test-mode key id |
| `RAZORPAY_KEY_SECRET` | Razorpay test-mode key secret |
| `SPEND_LIMIT_INR` | Per-order spend cap, default `5000` |
