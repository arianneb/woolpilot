# WoolPilot

A small Python project that fetches product data for a fixed list of yarns from [wollplatz.de](https://www.wollplatz.de), then stores the results in JSON format.

At this stage, the program runs end-to-end:  
- Product pages are fetched using a Playwright-powered headless browser  
- Parsing is stubbed (all fields except brand and name are `null`)  
- Results are written to `data/output.json`

---

## Setup

### 1. Install Python & dependencies
```bash
python3 -m venv venv
source venv/bin/activate.fish   # or venv/bin/activate for bash/zsh
pip install -r requirements.txt
```

### 2. Install Playwright browser
```bash
playwright install chromium
```

## Running

```bash
PYTHONPATH=src python -m woolpilot
```
Running the above will fetch search pages for the five yarns and write to data/output.json
```bash
[
  {
    "brand": "DMC",
    "name": "Natura XL",
    "price": null,
    "availability": null,
    "needle_size": null,
    "composition": null,
    "source_url": null
  },
  ...
]
```

## Project Structure
```bash
src/woolpilot/
  cli.py          # entry point logic (loops yarns, writes JSON)
  models.py       # Product dataclass
  storage.py      # JSON writer
  providers/      # data source implementations
    base.py       # abstract Provider interface
    browser.py    # Playwright fetch helper
    wollplatz.py  # Wollplatz provider (uses browser + parser)
  parsers/        # HTML parsing logic
    base.py       # abstract Parser interface
    wollplatz.py  # Wollplatz parser (currently stubbed)
    utils.py      # parsing helpers
tests/            # (initial smoke test; parser tests to come)
data/             # output JSON files
```

## Notes

### Fetching HTML

In a production setup, fetching would require a real browser fetcher (e.g. Playwright or requests+Cloudscraper) to handle Cloudflare and dynamic JS rendering (I was unable to get this working in a reasonable time frame)  

For this coding challenge, the `WollplatzProvider.fetch_search_html` method is stubbed to load a saved HTML file from `data/sample_wollplatz.html`. This lets me focus on clean architecture, parsing logic, and SOLID design without relying on fragile scraping.

### Structure
Code is structured with SOLID principles in mind (separation of provider and parser, clear model objects, isolated storage)

### Provider Extension 
Currently only Wollplatz is implemented; other providers could be added under providers/ with their own parsers.

