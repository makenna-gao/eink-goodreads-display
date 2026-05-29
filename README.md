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
   python3 get_goodreads_rss.py
   ```

4. Run the display renderer (preview on desktop):
   ```bash
   python3 render_display.py
   ```

## How it works

- `get_goodreads_rss.py` — fetches your currently-reading shelf via Goodreads RSS. Falls back to your most recently finished book if the shelf is empty.
- `render_display.py` — takes a cover image, title, author, and label and produces a 400×300 grayscale image ready for the Waveshare display.
- `update_display.py` — orchestrator that runs the full pipeline end-to-end.

## Deployment on Raspberry Pi

1. Install a font for better rendering:
   ```bash
   sudo apt install fonts-liberation
   ```

2. Run the full pipeline manually to verify:
   ```bash
   cd ~/eink-goodreads-display && python3 update_display.py
   ```

3. Enable the Waveshare driver in `update_display.py` by uncommenting the driver block and installing the library from the [Waveshare wiki](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module).

4. Schedule with cron to refresh hourly:
   ```bash
   crontab -e
   ```
   Add:
   ```
   0 * * * * cd /home/pi/eink-goodreads-display && python3 update_display.py >> /home/pi/eink-display.log 2>&1
   ```
