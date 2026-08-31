import razorpay

from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

_client: razorpay.Client | None = None


def get_client() -> razorpay.Client:
    global _client
    if _client is None:
        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            raise RuntimeError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set (see .env.example)")
        _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    return _client


def create_order(amount_inr: int, receipt: str, notes: dict | None = None) -> dict:
    """Create a Razorpay test-mode order. Amounts are converted to paise."""
    return get_client().order.create(
        {
            "amount": amount_inr * 100,
            "currency": "INR",
            "receipt": receipt,
            "notes": notes or {},
        }
    )
