"""Build entry.png for "I Knitted You an Octopus" (make.fun ai-excited-01).

Pipeline, all deterministic (no randomness, no clock, no network):
  1. open scene.jpg (photoreal base scene, made in this session)
  2. center-crop it to a square and resize to 1024x1024
  3. draw Maya's handwritten note on a small taped paper card and paste
     it, slightly tilted, near the bottom of the frame
  4. save as JPEG bytes to entry.png (JPEG-in-.png is accepted: the
     container is chosen by magic bytes, and JPEG keeps a photo-real
     1024x1024 image far under the 1 MiB cap)

Run:  python3 generate.py
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
INK = (18, 38, 110)          # dark blue ballpoint ink
PAPER = (255, 248, 231)       # warm cream paper
TAPE = (255, 196, 60, 205)    # translucent washi tape, stronger so it reads

NOTE_LINES = [
    "dear judge,",
    "you watch the sea all day,",
    "but nothing ever hugged you back —",
    "so i knitted you an octopus.",
    "love, maya (7)",
    "p.s. it only hugs judges it likes.",
]


def draw_heart(draw, cx, cy, size, color):
    """Draw a small filled heart centred at (cx, cy).

    Caveat has no heart glyph (it renders as a tofu box), so the heart
    after Maya's signature is drawn with two circles and a triangle.
    """
    r = size // 2
    draw.ellipse([cx - r - r // 2, cy - r // 2, cx - r // 2, cy + r // 2],
                 fill=color)
    draw.ellipse([cx + r // 2 - r, cy - r // 2, cx + r // 2 + r // 2,
                  cy + r // 2], fill=color)
    draw.polygon([(cx - r - r // 2, cy), (cx + r + r // 2, cy),
                  (cx, cy + size)], fill=color)


def square_crop(img):
    """Crop the middle square out of a rectangular photo."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def make_note():
    """Render the handwritten note on its own paper card."""
    card_w, card_h = 560, 272
    card = Image.new("RGBA", (card_w, card_h), PAPER + (255,))
    draw = ImageDraw.Draw(card)

    # faint ruled lines, like notebook paper
    for y in range(52, card_h - 16, 42):
        draw.line([(26, y), (card_w - 26, y)], fill=(180, 200, 235, 130), width=1)

    font = ImageFont.truetype("fonts/Caveat-Bold.ttf", 37)
    small = ImageFont.truetype("fonts/Caveat-Bold.ttf", 31)
    y = 12
    for i, line in enumerate(NOTE_LINES):
        use = small if i == len(NOTE_LINES) - 1 else font
        draw.text((30, y), line, font=use, fill=INK)
        if i == 4:
            # hand-drawn heart right after "love, maya (7)"
            text_w = draw.textlength("love, maya (7) ", font=font)
            draw_heart(draw, 30 + int(text_w) + 16, y + 22, 22, INK)
        y += 43 if i < 4 else 38

    # a strip of washi tape across the top edge
    tape = Image.new("RGBA", (170, 34), TAPE)
    card.alpha_composite(tape, (card_w // 2 - 85, -8))
    return card


def main():
    base = Image.open("scene.jpg").convert("RGB")
    base = square_crop(base).resize((SIZE, SIZE), Image.LANCZOS)

    note = make_note().rotate(-2, expand=True, resample=Image.BICUBIC)

    # drop shadow for the card, offset down-right. The card sits low and
    # slightly left of centre so Maya (far left) stays fully visible and
    # only the guard's shin goes behind it.
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh = ImageDraw.Draw(shadow)
    cx, cy = 480, 850
    x0 = cx - note.width // 2 + 10
    y0 = cy - note.height // 2 + 12
    sh.rounded_rectangle([x0, y0, x0 + note.width, y0 + note.height],
                         radius=10, fill=(0, 0, 0, 110))
    base = Image.alpha_composite(base.convert("RGBA"), shadow)
    base.alpha_composite(note, (cx - note.width // 2, cy - note.height // 2))

    # JPEG bytes in a .png name: magic bytes decide the format, and this
    # keeps the photo-real frame well under 1 MiB. Fixed quality + no
    # metadata, so two runs produce identical bytes.
    base.convert("RGB").save("entry.png", format="JPEG", quality=88,
                             optimize=False, progressive=False)


if __name__ == "__main__":
    main()
