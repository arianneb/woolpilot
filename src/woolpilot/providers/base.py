from abc import ABC, abstractmethod
from woolpilot.models import Product

# abstract base class for wool providers (currently only implementing Wollplatz)
class BaseProvider(ABC):

    @abstractmethod
    def fetch_search_html(self, brand: str, name: str) -> str:
        # fetch the raw HTML for a product search page
        pass

    @abstractmethod
    def search_product(self, brand: str, name: str) -> Product | None:
        # search for a product and return a Product object, or None if not found
        pass
