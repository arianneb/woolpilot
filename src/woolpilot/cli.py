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
    results = []
    for brand, name in YARNS:
        product = provider.search_product(brand, name)
        if product:
            results.append(product)

    write_json(results, "data/output.json")
    print("SUCCESS: result written to data/output.json")
    return 0