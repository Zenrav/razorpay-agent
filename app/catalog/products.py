"""Hardcoded demo catalog. Prices are in INR."""

PRODUCTS = [
    {"id": "sku_tshirt", "name": "Cotton T-Shirt", "price_inr": 799, "category": "apparel", "in_stock": True,
     "keywords": ["tshirt", "t-shirt", "shirt", "tee"]},
    {"id": "sku_hoodie", "name": "Fleece Hoodie", "price_inr": 1899, "category": "apparel", "in_stock": True,
     "keywords": ["hoodie", "sweatshirt"]},
    {"id": "sku_sneakers", "name": "Running Sneakers", "price_inr": 3499, "category": "footwear", "in_stock": False,
     "keywords": ["sneakers", "shoes", "running"]},
    {"id": "sku_loafers", "name": "Canvas Loafers", "price_inr": 2299, "category": "footwear", "in_stock": True,
     "keywords": ["loafers", "slip-ons"]},
    {"id": "sku_headphones", "name": "Wireless Headphones", "price_inr": 4999, "category": "audio", "in_stock": True,
     "keywords": ["headphones", "earphones", "audio"]},
    {"id": "sku_earbuds", "name": "Bluetooth Earbuds", "price_inr": 2499, "category": "audio", "in_stock": True,
     "keywords": ["earbuds", "buds"]},
    {"id": "sku_speaker", "name": "Portable Speaker", "price_inr": 3299, "category": "audio", "in_stock": False,
     "keywords": ["speaker", "boombox"]},
    {"id": "sku_laptop", "name": "Ultrabook Laptop", "price_inr": 74999, "category": "computing", "in_stock": True,
     "keywords": ["laptop", "ultrabook", "notebook"]},
]


def search(query: str) -> dict | None:
    """Return the first product whose name or keywords match the query."""
    q = query.lower()
    for product in PRODUCTS:
        if product["name"].lower() in q or any(keyword in q for keyword in product["keywords"]):
            return product
    return None


def find_substitute(product: dict) -> dict | None:
    """Return an in-stock product from the same category, cheapest first."""
    alternatives = [
        candidate
        for candidate in PRODUCTS
        if candidate["category"] == product["category"] and candidate["in_stock"] and candidate["id"] != product["id"]
    ]
    return min(alternatives, key=lambda candidate: candidate["price_inr"], default=None)
