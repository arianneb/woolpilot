from abc import ABC, abstractmethod
from typing import Optional
from ..models import Product

class Provider(ABC):
    # abstract interface for any wool website data sources

    # return a Product if found, otherwise return none
    @abstractmethod
    def search(self, brand: str, name: str) -> Optional[Product]:
        raise NotImplementedError