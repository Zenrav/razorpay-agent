import json
from datetime import datetime, timezone

from app.config import AUDIT_LOG_PATH


def log_action(action: str, reason: str, amount: int | None = None) -> dict:
    """Append a single audit entry to the JSONL audit trail and return it."""
    entry = {
        "action": action,
        "reason": reason,
        "amount": amount,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    return entry
