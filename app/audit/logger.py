import json
from datetime import datetime, timezone

from app.config import AUDIT_LOG_PATH

DECISIONS: list[dict] = []
"""In-memory audit trail for the current process, mirrored to the JSONL file."""


def log_action(action: str, reason: str, amount: int | None = None) -> dict:
    """Record a single agent decision and return it."""
    entry = {
        "action": action,
        "reason": reason,
        "amount": amount,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    DECISIONS.append(entry)
    print(f"[audit] {entry['action']}: {entry['reason']}" + (f" (INR {amount})" if amount else ""))
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    return entry
