from abc import ABC, abstractmethod
from typing import Optional
from ..models import Product

class Provider(ABC):
    # search for wool products on wool website
    @abstractmethod
    def search_products(self, brand: str, name: str) -> Optional[Product]:
        pass