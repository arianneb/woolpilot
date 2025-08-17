from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# abstract base class for wool parsers (currently only implementing Wollplatz)
class BaseParser(ABC):
   
    @abstractmethod
    def parse_detail_url(self, html: str) -> str:
        # fetch the detail page URL for a given yarn from the product search page
        pass

    @abstractmethod
    def parse_price(self, soup: BeautifulSoup) -> str:
        # parse price from product detail page
        pass

    @abstractmethod
    def parse_availability(self, soup: BeautifulSoup) -> str:
         # parse availability from product detail page
        pass

    @abstractmethod
    def parse_needle_size(self, soup: BeautifulSoup) -> str:
         # parse needle size from product detail page
        pass

    @abstractmethod
    def parse_composition(self, soup: BeautifulSoup) -> str:
         # parse composition from product detail page
        pass

    @abstractmethod
    def parse_product_detail(self, html: str) -> dict:
         # parse all above fields from product detail page
        pass