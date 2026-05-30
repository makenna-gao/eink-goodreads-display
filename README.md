# eink-goodreads-display

A Raspberry Pi e-ink display that shows your current (or most recently read) book from Goodreads.

## Hardware

- Waveshare 4.2" e-ink display (400×300, 4 grayscale levels)
- Raspberry Pi (any model)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Install Pi-specific dependencies:
   ```bash
   venv/bin/pip install spidev gpiozero lgpio
   sudo apt install fonts-liberation
   ```

3. Enable SPI:
   ```bash
   sudo raspi-config
   ```
   Go to **Interface Options → SPI → Yes**, then reboot.

4. Install the Waveshare library:
   ```bash
   cd ~
   git clone https://github.com/waveshare/e-Paper.git
   cp -r ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd ~/eink-goodreads-display/
   ```

5. Enable the Waveshare driver in `update_display.py` by uncommenting the driver block.

6. Run the full pipeline manually to verify:
   ```bash
   cd ~/eink-goodreads-display
   venv/bin/python3 update_display.py
   ```

7. Schedule with cron to refresh hourly:
   ```bash
   crontab -e
   ```
   Add (adjust path to match your username):
   ```
   0 * * * * cd /home/pi/eink-goodreads-display && venv/bin/python3 update_display.py >> /home/pi/eink-display.log 2>&1
   ```
