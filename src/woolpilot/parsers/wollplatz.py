# src/woolpilot/parsers/wollplatz.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from woolpilot.models import Product

BASE = "https://www.wollplatz.de"

class WollplatzParser:

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
            
            # only keep product detail pages (not patterns)
            if "/wolle/" in href:
                return urljoin(BASE, href)

        return None

    def parse_product_detail(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        # price (look for .product-price-amount element)
        price_el = soup.select_one(".product-price-amount")
        price = price_el.get_text(strip=True)
        print("FRUITBAT: price - " + price)

        # availability (look for the availability meta tag)
        avail_el = soup.find("meta", itemprop="availability")
        availability = avail_el.get("content") if avail_el else None

        # parse availability string for Discontinued... 
        is_available = True
        if "Discontinued" in availability:
            is_available = False
        
        print("FRUITBAT: availabliity -  " + str(is_available))

        # needle size (look for the <dt>Nadelstärke</dt> row)
        needle_tr_el = soup.select_one('tr:has(> td:nth-of-type(1):-soup-contains("Nadelstärke")) > td:nth-of-type(2)')
        needle_size = needle_tr_el.get_text(strip=True) if needle_tr_el else None
        print("FRUITBAT: needle size -  " + needle_size)

        # composition (look for the <dt>Zusammenstellung</dt> row)
        composition_tr_el = soup.select_one('tr:has(> td:nth-of-type(1):-soup-contains("Zusammenstellung")) > td:nth-of-type(2)')
        composition = composition_tr_el.get_text(strip=True) if composition_tr_el else None
        print("FRUITBAT: composition-  " + composition)

        return {
            "price": price,
            "availability": is_available,
            "needle_size": needle_size,
            "composition": composition
        }