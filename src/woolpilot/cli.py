from typing import List
from .models import Product
from .providers.wollplatz import WollplatzProvider
from .storage import write_json

# hardcoded yarns to search for
YARNS: List[tuple[str, str]] = [
    ("DMC", "Natura XL"),
    ("Drops", "Safran"),
    ("Drops", "Baby Merino Mix"),
    ("Hahn", "Alpacca Speciale"),
    ("Stylecraft", "Special double knit"),
]

def main() -> int:
    # todo: allow switching between multiple providers
    provider = WollplatzProvider()
    
    # search for yarns from given provider
    results: List[Product] = []
    for brand, name in YARNS:
        try:
            product = provider.search_products(brand, name)
            results.append(product if product else Product(brand=brand, name=name))
        except Exception as e:
            # soft failure
            print(f"[WARNING] {brand} {name}: {e}")
            results.append(Product(brand=brand, name=name))

    write_json(results, "data/output.json")
    print("SUCCESS: result written to data/output.json")
    return 0
