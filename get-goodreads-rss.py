import feedparser
import requests
from dotenv import load_dotenv
import os

load_dotenv()
USER_ID = os.getenv("GOODREADS_USER_ID")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_feed(shelf):
    url = f"https://www.goodreads.com/review/list_rss/{USER_ID}?shelf={shelf}&per_page=1"
    response = requests.get(url, headers=HEADERS)
    return feedparser.parse(response.content)

feed = get_feed("currently-reading")
currently_reading = bool(feed.entries)

if not currently_reading:
    print("No currently reading books")
    feed = get_feed("read")

print(feed)

if feed.entries:
    book = feed.entries[0]
    title = book.title
    author = book.author_name
    cover_url = book.book_large_image_url

    img_data = requests.get(cover_url).content
    with open("cover.jpg", "wb") as f:
        f.write(img_data)

    label = "Reading" if currently_reading else "Recently read"
    print(f"{label}: {title} by {author}")