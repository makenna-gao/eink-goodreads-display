from PIL import Image, ImageDraw, ImageFont
import os

DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300
COVER_PANEL_WIDTH = 190
TEXT_PANEL_X = 200
PADDING = 12

# Waveshare 4.2" 4-grayscale levels: black, dark gray, light gray, white
_GRAY_LEVELS = [0, 85, 170, 255]
_GRAY_LUT = [min(_GRAY_LEVELS, key=lambda l: abs(l - i)) for i in range(256)]


def _quantize_4gray(img):
    return img.convert("L").point(_GRAY_LUT)


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

    cx = PADDING + (cover_area_w - cover.width) // 2
    cy = PADDING + (cover_area_h - cover.height) // 2
    canvas.paste(cover, (cx, cy))

    # Divider
    draw.line(
        [(COVER_PANEL_WIDTH, PADDING), (COVER_PANEL_WIDTH, DISPLAY_HEIGHT - PADDING)],
        fill=170,
        width=1,
    )

    # --- Text panel (right) ---
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

    canvas = _quantize_4gray(canvas)
    canvas.save(output_path)
    print(f"Saved: {output_path}")
    return canvas


if __name__ == "__main__":
    render("cover.jpg", "Project Hail Mary", "Andy Weir", "Recently read")
