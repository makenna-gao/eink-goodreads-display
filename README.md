# eink-goodreads-display

A Raspberry Pi e-ink display that shows your current (or most recently read) book from Goodreads.

## Hardware

- Waveshare 4.2" e-ink display (400×300, 4 grayscale levels)
- Raspberry Pi (any model)

## Setup

1. Install dependencies:
   ```bash
   pip install feedparser requests python-dotenv Pillow
   ```

2. Copy `.env.example` to `.env` and fill in your Goodreads user ID:
   ```bash
   cp .env.example .env
   ```
   Your user ID is the number in your Goodreads profile URL.

3. Run the fetch script:
   ```bash
   python3 get-goodreads-rss.py
   ```

4. Run the display renderer (preview on desktop):
   ```bash
   python3 render_display.py
   ```

## How it works

- `get-goodreads-rss.py` — fetches your currently-reading shelf via Goodreads RSS. Falls back to your most recently finished book if the shelf is empty.
- `render_display.py` — takes a cover image, title, author, and label and produces a 400×300 grayscale image ready for the Waveshare display.
