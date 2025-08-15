import time
from typing import Dict, Optional

DEFAULT_TIMEOUT = 20

# return fixed and realistic user agent (stable for tests)
def _ua() -> str:
    return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# define request headers dictionary
def _base_headers() -> Dict[str, str]:
    return {
        "User-Agent": _ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }


def new_session():
    # use cloudscraper, fall back to requests.Session
    try:
        import cloudscraper  # type: ignore
        scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "mac", "mobile": False}
        )
    except Exception:
        import requests
        scraper = requests.Session()
    scraper.headers.update(_base_headers())
    return scraper

def polite_delay():
    time.sleep(1.0)

def get_with_session(scraper, url: str, *, referer: Optional[str] = None, timeout: Optional[int] = None):
    headers = {}
    if referer:
        headers["Referer"] = referer
    resp = scraper.get(url, headers=headers, timeout=timeout or DEFAULT_TIMEOUT, allow_redirects=True)
    
    # retry once on 403 with a fresh user agent
    if getattr(resp, "status_code", None) == 403:
        scraper.headers["User-Agent"] = _ua()
        time.sleep(1.2)
        resp = scraper.get(url, headers=headers, timeout=timeout or DEFAULT_TIMEOUT, allow_redirects=True)
    # raise if still bad
    if hasattr(resp, "raise_for_status"):
        resp.raise_for_status()
    polite_delay()
    return resp
