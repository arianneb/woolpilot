from bs4 import BeautifulSoup
from urllib.parse import urljoin
from woolpilot.models import Product
from woolpilot.parsers.utils import convert_price_to_float
from woolpilot.parsers.base import BaseParser

BASE = "https://www.wollplatz.de"

class WollplatzParser(BaseParser):

    # parse the product detail page url from search page html
    def parse_detail_url(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        urls: list[str] = []
        for el in soup.select(".productlistholder.sqr-resultItem"):
            a = el.select_one("a")
            if not a:
                continue
            href = a.get("href")
            if not href:
                continue
            
            # only keep product detail pages for wool
            if "/wolle/" in href:
                return urljoin(BASE, href)

        return None
    
    def parse_price(self, soup) -> float:
        # price (look for .product-price-amount element)
        try:
            price_el = soup.select_one(".product-price-amount")
            price_string = price_el.get_text(strip=True)
            price = convert_price_to_float(price_string)
            return price
        except Exception as e:
            print(f"[WARNING] Could not fetch price: {e}")
            return 0
    
    def parse_availability(self, soup) -> str:
        try:
            # availability (look for the availability meta tag)
            avail_el = soup.find("meta", itemprop="availability")
            availability = avail_el.get("content") if avail_el else None

            # parse availability for Discontinued and OutOfStock, otherwise set to Available
            if availability:
                if "Discontinued" in availability:
                    return "Discontinued"
                elif "OutOfStock" in availability:
                    return "OutOfStock"
                else:
                    return "Available"
        except Exception as e:
            print(f"[WARNING] Could not fetch availability: {e}")
        return "Availability not found"

    def parse_needle_size(self, soup) -> str:
        try:
            # needle size (look for the <dt>Nadelstärke</dt> row)
            needle_tr_el = soup.select_one('tr:has(> td:nth-of-type(1):-soup-contains("Nadelstärke")) > td:nth-of-type(2)')
            needle_size = needle_tr_el.get_text(strip=True) if needle_tr_el else None
            if needle_size:
                return needle_size
        except Exception as e:
            print(f"[WARNING] Could not fetch needle size: {e}")
        return "Needle size not found"

    def parse_composition(self, soup) -> str:
        try:
            # composition (look for the <dt>Zusammenstellung</dt> row)
            composition_tr_el = soup.select_one('tr:has(> td:nth-of-type(1):-soup-contains("Zusammenstellung")) > td:nth-of-type(2)')
            composition = composition_tr_el.get_text(strip=True) if composition_tr_el else None
            if composition:
                return composition
        except Exception as e:
            print(f"[WARNING] Could not fetch composition: {e}")
        return "Composition not found"

    # parse all desired data from product detail page html
    def parse_product_detail(self, html: str) -> dict:
        
        soup = BeautifulSoup(html, "html.parser")

        price = self.parse_price(soup)
        availability = self.parse_availability(soup)
        needle_size = self.parse_needle_size(soup)
        composition = self.parse_composition(soup)

        return {
            "price": price,
            "availability": availability,
            "needle_size": needle_size,
            "composition": composition
        }