"""Hardcoded demo catalog. Prices are in INR."""

PRODUCTS = [
    {"id": "sku_tshirt", "name": "Cotton T-Shirt", "price_inr": 799, "keywords": ["tshirt", "t-shirt", "shirt", "tee"]},
    {"id": "sku_sneakers", "name": "Running Sneakers", "price_inr": 3499, "keywords": ["sneakers", "shoes", "running"]},
    {"id": "sku_headphones", "name": "Wireless Headphones", "price_inr": 4999, "keywords": ["headphones", "earphones", "audio"]},
    {"id": "sku_laptop", "name": "Ultrabook Laptop", "price_inr": 74999, "keywords": ["laptop", "ultrabook", "notebook"]},
]


def search(query: str) -> dict | None:
    """Return the first product whose name or keywords match the query."""
    q = query.lower()
    for product in PRODUCTS:
        if product["name"].lower() in q or any(keyword in q for keyword in product["keywords"]):
            return product
    return None
