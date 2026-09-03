# Demo script

A sample conversation to record for the pitch video. The server is running with
`uvicorn app.main:app --reload` and `SPEND_LIMIT_INR=5000`.

For the video, drive it from the chat UI at <http://localhost:8000> — the four
suggestion buttons run these scenarios in order and the audit panel updates live.
The curl equivalents below are for the API-only version of the demo.

## 1. Happy path — agent places a real test-mode order

```bash
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message": "buy me the wireless headphones"}' | jq
```

```json
{
  "reply": "Created a Razorpay order for Wireless Headphones (INR 4999). Order id: order_Nx1yZ...",
  "order_id": "order_Nx1yZ...",
  "log": [...]
}
```

## 2. Out of stock — agent substitutes gracefully

```bash
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message": "buy me the running sneakers"}' | jq
```

```json
{
  "reply": "Running Sneakers is out of stock, so I ordered Canvas Loafers (INR 2299) instead. Order id: order_Nx2aB...",
  "order_id": "order_Nx2aB..."
}
```

## 3. Guardrail — spend limit blocks the purchase

```bash
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message": "order the ultrabook laptop"}' | jq
```

```json
{
  "reply": "That purchase is above your spend limit of INR 5000, so I did not place it.",
  "order_id": null
}
```

## 4. Unknown product — graceful failure

```bash
curl -s localhost:8000/chat -H 'content-type: application/json' \
  -d '{"message": "buy me a helicopter"}' | jq
```

## 5. Audit trail

```bash
curl -s localhost:8000/audit | jq   # in-memory trail
cat audit_log.jsonl                 # same entries, on disk
```

Every decision the agent made — placed, blocked, or failed — with the reason and
amount, ready to show as the compliance artifact.
