# WoolPilot

A small Python project that fetches product data for a fixed list of yarns from [wollplatz.de](https://www.wollplatz.de), then stores the results in JSON format.

At this stage, the program runs end-to-end:  
- Product pages are fetched using a Playwright-powered headless browser  
- HTML parsing is implemented using BeautifulSoup
- Errors and edge-cases are being handled gracefully
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
    "price": 8.46,
    "availability": false,
    "needle_size": "8 mm",
    "composition": "100% Baumwolle",
    "source_url": "https://www.wollplatz.de/wolle/dmc/dmc-natura-xl"
  },
  {
    "brand": "Drops",
    "name": "Safran",
    "price": 1.55,
    "availability": true,
    "needle_size": "3 mm",
    "composition": "100% Baumwolle",
    "source_url": "https://www.wollplatz.de/wolle/drops/drops-safran"
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
    wollplatz.py  # Wollplatz parser
    utils.py      # parsing helper
tests/            # unit tests (including smoke and parser tests)
data/             # output JSON files
```

## Notes

### Structure
Code is structured with SOLID principles in mind: providers handle fetching data, parsers handle extracting structured data, and both inherit from abstract base classes. This makes it easy to add new providers/parsers while reusing the same core models and storage.

### Code Extension 
Currently only Wollplatz is implemented. Other providers could be added under `providers/` with their own parsers (under `parsers/`), and the rest of the code would work unchanged since all providers follow the same interface.

### TODO
Given time constraints, I wasn't able to handle everything exactly as I wanted to, but in a real-world scenario, I'd add:
- More unit tests, especially edge-case coverage
- I didn’t write unit tests for the providers since it’s best practice to exclude live network calls in unit tests; in a real-world project I’d add integration tests (with mocked HTTP responses) and end-to-end tests to validate full provider–parser–model flow
- More robust price handling (showing currency, clearly displaying if price is missing)
- Replace `print`-based warnings with structured logging
- Extend storage beyond JSON output (DB/API)
- Support concurrency/async for scaling to multiple providers, especially given scraping performance concerns 
- Even tighter handling of errors and edge-cases
- Change desired yarns from hard-coding to dynamic loading (to easily add more yarns in the search)



