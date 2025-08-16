from typing import List
from urllib.parse import quote
from woolpilot.models import Product
from woolpilot.providers.browser import fetch_html
from woolpilot.parsers.wollplatz import WollplatzParser


class WollplatzProvider:

    BASE_URL = "https://www.wollplatz.de/wolle/"

    # fetch the raw HTML for a product search on Wollplatz, use Playwright to load page and return HTML
    def fetch_search_html(self, brand, name):

        # build search query using brand and name
        query = f"{brand} {name}"
        encoded_query = quote(query)   # "Drops Baby Merino Mix" → "Drops%20Baby%20Merino%20Mix"
        url = self.BASE_URL + "#sqr:(q[" + encoded_query + "])"

        print("FRUITBAT: le url: " + url)
        return fetch_html(url)


    # search Wollplatz for products by brand and name, return a list of Product objects
    def search_product(self, brand, name):

        parser = WollplatzParser()

        # fetch search page html
        html = self.fetch_search_html(brand, name)

        # parse product detail link from search page
        detail_link = parser.parse_detail_url(html)
        if not detail_link:
            print(f"[WARNING] Skipping {brand} {name}, no detail link found")
            return None

        # fetch detail page html
        detail_html = None
        try:
            detail_html = fetch_html(detail_link)
        except Exception as e:
            print(f"[WARNING] Could not fetch {detail_link}: {e}")
            
        # parse desired product data from detail page html
        productDict = parser.parse_product_detail(detail_html)

        productDict["brand"] = brand
        productDict["name"] = name
        productDict["source_url"] = detail_link

        product = Product(**productDict) 
        print(str(product))
        return product
        