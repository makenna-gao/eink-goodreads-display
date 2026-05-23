from PIL import Image, ImageDraw, ImageFont
import os

DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300
COVER_PANEL_WIDTH = 190
TEXT_PANEL_X = 200
PADDING = 12

# Waveshare 4.2" 4-grayscale levels: black, dark gray, light gray, white
_GRAY_LEVELS = [0, 85, 170, 255]


def _dither_cover(cover_img):
    """Floyd-Steinberg dither a grayscale cover image to the 4 valid gray levels."""
    pal_img = Image.new("P", (1, 1))
    palette = [0] * 768
    for i, level in enumerate(_GRAY_LEVELS):
        palette[i * 3] = palette[i * 3 + 1] = palette[i * 3 + 2] = level
    pal_img.putpalette(palette)
    dithered = cover_img.convert("RGB").quantize(palette=pal_img, dither=Image.Dither.FLOYDSTEINBERG)
    return dithered.convert("L")


def _load_font(size):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render(cover_path, title, author, label, output_path="display.png"):
    canvas = Image.new("L", (DISPLAY_WIDTH, DISPLAY_HEIGHT), 255)
    draw = ImageDraw.Draw(canvas)

    # --- Cover panel (left) ---
    cover_area_w = COVER_PANEL_WIDTH - PADDING * 2
    cover_area_h = DISPLAY_HEIGHT - PADDING * 2

    cover = Image.open(cover_path).convert("L")
    cover.thumbnail((cover_area_w, cover_area_h), Image.LANCZOS)
    cover = _dither_cover(cover)  # dither before pasting, not the whole canvas

    cx = PADDING + (cover_area_w - cover.width) // 2
    cy = PADDING + (cover_area_h - cover.height) // 2
    canvas.paste(cover, (cx, cy))

    # Divider — uses exact palette value 170 so it stays crisp
    draw.line(
        [(COVER_PANEL_WIDTH, PADDING), (COVER_PANEL_WIDTH, DISPLAY_HEIGHT - PADDING)],
        fill=170,
        width=1,
    )

    # --- Text panel (right) ---
    # All text uses exact palette values (0, 85, 170, 255) — no dithering needed
    text_x = TEXT_PANEL_X + PADDING
    text_max_w = DISPLAY_WIDTH - text_x - PADDING
    y = PADDING + 10

    label_font = _load_font(13)
    draw.text((text_x, y), label.upper(), font=label_font, fill=170)
    y += 22

    title_font = _load_font(20)
    for line in _wrap_text(draw, title, title_font, text_max_w):
        draw.text((text_x, y), line, font=title_font, fill=0)
        y += 27

    y += 10

    author_font = _load_font(15)
    draw.text((text_x, y), author, font=author_font, fill=85)

    # Canvas is "L" mode with only values in {0, 85, 170, 255}:
    # bg=255, cover dithered above, divider=170, label=170, title=0, author=85
    # This satisfies Waveshare getbuffer_4Gray() expectations.
    assert canvas.mode == "L"
    canvas.save(output_path)
    print(f"Saved: {output_path}")
    return canvas


if __name__ == "__main__":
    render("cover.jpg", "Project Hail Mary", "Andy Weir", "Recently read")
