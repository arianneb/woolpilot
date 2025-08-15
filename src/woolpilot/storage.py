import json
from typing import Iterable
from .models import Product

def write_json(products: Iterable[Product], path: str) -> None:
    data = []
    for product in products:
        data.append({
            "brand": product.brand,
            "name": product.name,
            "price": product.price,
            "availability": product.availability,
            "needle_size": product.needle_size,
            "composition": product.composition,
            "source_url": product.source_url,
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
