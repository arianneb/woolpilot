from typing import Optional
from ..models import Product
from .base import Provider

class WollplatzProvider(Provider):
    BASE = "https://www.wollplatz.de"
    SEARCH_URL = "https://www.wollplatz.de/suche?q={q}"

    def search(self, brand: str, name: str) -> Optional[Product]:
        return Product(brand=brand, name=name)
