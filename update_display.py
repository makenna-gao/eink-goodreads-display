from get_goodreads_rss import fetch_current_book
from render_display import render
import sys


def main():
    try:
        book = fetch_current_book()
        if not book:
            print("No book data found.")
            sys.exit(0)

        render(
            cover_path=book["cover_path"],
            title=book["title"],
            author=book["author"],
            label=book["label"],
        )

        # --- Waveshare e-ink display (uncomment on Pi) ---
        # from waveshare_epd import epd4in2
        # epd = epd4in2.EPD()
        # epd.init()
        # from PIL import Image
        # img = Image.open("display.png")
        # epd.display(epd.getbuffer_4Gray(img))
        # epd.sleep()

    except Exception as e:
        print(f"Error updating display: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
