import re
import pandas
import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = "https://www.dubaiphone.net/en/category/mobiles-all-2"

def playwright_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(1500)  # Wait for 1 second to allow content to load
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == page_height:
                break
            page_height = new_height
        try:
            page.wait_for_selector("div.container.mx-auto.py-2")
        except:
            print("Error occurred while waiting for selector")
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')
        container = soup.find("div", class_="container mx-auto py-2")
        time.sleep(random.uniform(1, 5))
        browser.close()
    return container

def extract_items(container):
    item_data = []
    if not container:
        print("Container not found. Exiting.")
        return item_data
    for cards in container.find_all("a", class_=re.compile(r"block")):
        model = cards.find("h3" , class_=re.compile(r"dp-product-title"))
        price = cards.find("span", class_=re.compile(r"font-manrope tabular-nums"))
        if model and price:
            Model = model.get_text(strip=True) if model else "N/A"
            Price = price.get_text(strip=True) if price else "N/A"
            print(f"Model: {Model} | Price: {Price}")
            item_data.append({"Model": Model, "Price": Price})
    return item_data

def save_to_csv(item_data):
    print(f"Scraping completed. Total items scraped: {len(item_data)}")
    df = pandas.DataFrame(item_data)
    df.to_csv("Dubai_phone.csv", index=False , encoding='utf-8-sig')

def main():
    container = playwright_scraper()
    item_data = extract_items(container)
    save_to_csv(item_data)

if __name__ == "__main__":
    main()