import feedparser
import requests
from dotenv import load_dotenv
import os

load_dotenv()
USER_ID = os.getenv("GOODREADS_USER_ID")
RSS_KEY = os.getenv("GOODREADS_RSS_KEY")

HEADERS = {"User-Agent": "Mozilla/5.0"}


def _get_feed(shelf):
    url = f"https://www.goodreads.com/review/list_rss/{USER_ID}?shelf={shelf}&per_page=1"
    if RSS_KEY:
        url += f"&key={RSS_KEY}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return feedparser.parse(response.content)


def fetch_current_book():
    feed = _get_feed("currently-reading")
    currently_reading = bool(feed.entries)

    if not currently_reading:
        feed = _get_feed("read")

    if not feed.entries:
        return None

    book = feed.entries[0]
    label = "Reading" if currently_reading else "Recently read"

    img_response = requests.get(book.book_large_image_url, headers=HEADERS, timeout=10)
    img_response.raise_for_status()
    with open("cover.jpg", "wb") as f:
        f.write(img_response.content)

    return {
        "title": book.title,
        "author": book.author_name,
        "cover_path": "cover.jpg",
        "label": label,
    }


if __name__ == "__main__":
    try:
        result = fetch_current_book()
        if result:
            print(result)
        else:
            print("No books found on either shelf.")
    except requests.RequestException as e:
        print(f"Could not reach Goodreads: {e}")
