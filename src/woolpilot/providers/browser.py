from playwright.sync_api import sync_playwright

# fetch raw html using playright and headless chromium browser
def fetch_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # try with a visible browser for debugging
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.goto(url, timeout=5000, wait_until="networkidle")  # wait until no network requests

        html = page.content()
        browser.close()
        return html
