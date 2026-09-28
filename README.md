# Dubai Phone Scraper

Scrapes mobile phone models and pricing from Dubai Phone's web catalog.

### How it works
The platform relies on dynamic infinite scrolling to load catalog items. The script uses Playwright to drive a headless Chromium instance, programmatically triggering scroll events until all items load, then passes the DOM to BeautifulSoup for element extraction.

### Data Collected
- Phone Model Name
- Price (EGP)

### Requirements
```bash
pip install playwright pandas beautifulsoup4
playwright install chromium
```
### Running the script
```bash
python Dubai_phone_scrapper.py
```
### Output
Outputs product entries to Dubai_phone.csv encoded in utf-8-sig
