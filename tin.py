# books_scrape.py
# 1) Retrieve HTML pages from https://books.toscrape.com/
# 2) Get list of books on a page
# 3) Extract book links (convert relative -> absolute)
# 4) Parse a specific book page

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"


def fetch_html(url: str) -> str:
    """1) Retrieve HTML page"""
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text


def get_books_on_page(page_url: str):
    """
    2) Get list of books on the page
    3) Extract book links and make them absolute
    """
    html = fetch_html(page_url)
    soup = BeautifulSoup(html, "html.parser")

    books = []
    for item in soup.select("article.product_pod"):
        a = item.select_one("h3 a")
        title = a.get("title", "").strip() if a else ""
        rel_link = a.get("href", "").strip() if a else ""
        abs_link = urljoin(page_url, rel_link)  # relative -> absolute

        price_el = item.select_one(".price_color")
        price = price_el.get_text(strip=True) if price_el else ""

        books.append({
            "title": title,
            "price": price,
            "book_url": abs_link
        })

    return books


def parse_book_page(book_url: str):
    """4) Parse the page of a specific book"""
    html = fetch_html(book_url)
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one("div.product_main h1")
    price_el = soup.select_one("div.product_main p.price_color")
    avail_el = soup.select_one("div.product_main p.availability")

    title = title_el.get_text(strip=True) if title_el else ""
    price = price_el.get_text(strip=True) if price_el else ""
    availability = avail_el.get_text(" ", strip=True) if avail_el else ""

    # Description (if present)
    description = ""
    desc_anchor = soup.select_one("#product_description")
    if desc_anchor:
        p = desc_anchor.find_next_sibling("p")
        if p:
            description = p.get_text(" ", strip=True)

    # Product info table -> dict (UPC, Product Type, etc.)
    info = {}
    for row in soup.select("table.table.table-striped tr"):
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td:
            info[th.get_text(strip=True)] = td.get_text(" ", strip=True)

    return {
        "url": book_url,
        "title": title,
        "price": price,
        "availability": availability,
        "description": description,
        "product_info": info
    }


def main():
    # Step 1-3: scrape homepage list + absolute links
    page_url = BASE_URL
    books = get_books_on_page(page_url)

    print(f"Found {len(books)} books on {page_url}\n")
    for b in books[:5]:
        print(f"- {b['title']} | {b['price']} | {b['book_url']}")

    # Step 4: parse one specific book (first in list)
    if books:
        details = parse_book_page(books[0]["book_url"])
        print("\n--- Specific Book Parsed ---")
        print("Title:", details["title"])
        print("Price:", details["price"])
        print("Availability:", details["availability"])
        print("UPC:", details["product_info"].get("UPC", "N/A"))
        print("Description:", (details["description"][:200] + "...") if len(details["description"]) > 200 else details["description"])


if __name__ == "__main__":
    main()
