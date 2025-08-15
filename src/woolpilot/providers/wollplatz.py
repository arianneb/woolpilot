from woolpilot.providers.browser import fetch_html
from woolpilot.parsers.wollplatz import WollplatzParser


class WollplatzProvider:
    BASE_URL = "https://www.wollplatz.de"

    def fetch_search_html(self, brand, name):

        # fetch the raw HTML for a product search on Wollplatz, use Playwright to load page and return HTML
        query = f"{brand} {name}".replace(" ", "+")
        url = f"{self.BASE_URL}/suche?q={query}"
        return fetch_html(url)

    def search_products(self, brand, name):
    
        # search Wollplatz for products by brand and name, return a list of structured Product data
        html = self.fetch_search_html(brand, name)
        parser = WollplatzParser()
        return parser.parse_search_results(html)
