"""Build the entry image for "I Knitted You an Octopus".

Reads scene.jpg next to this script, shrinks it to a 1024x1024 square,
then sticks Maya's handwritten note to the judge on top of it and writes
the result as entry.png next to this script.

Every path is resolved from this file's own directory, never from the
current working directory, so the script works no matter where it is
run from. The output is deterministic: same input, same bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SIZE = 1024
CARD_W, CARD_H = 540, 280
INK = (18, 38, 110)
CREAM = (255, 248, 224)
RULE = (150, 180, 220)
TAPE = (190, 138, 58, 225)

NOTE_LINES = [
    "dear judge,",
    "you watch the sea all day,",
    "but nothing ever hugged you back -",
    "so i knitted you an octopus.",
    "love, maya (7)",
    "p.s. it only hugs judges it likes.",
]


def handwriting(size):
    """Caveat Bold, loaded from the fonts folder next to this script."""
    return ImageFont.truetype(str(HERE / "fonts" / "Caveat-Bold.ttf"), size)


def draw_heart(draw, cx, cy, r, colour):
    """A small hand-drawn heart: two circles joined by a triangle."""
    draw.ellipse((cx - r, cy - r, cx, cy + r // 3), fill=colour)
    draw.ellipse((cx, cy - r, cx + r, cy + r // 3), fill=colour)
    draw.polygon(
        [(cx - r, cy), (cx + r, cy), (cx, cy + r + r // 2)], fill=colour
    )


def make_note_card():
    """The taped cream card carrying Maya's note, tilted slightly."""
    card = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle(
        (0, 0, CARD_W - 1, CARD_H - 1), radius=10, fill=CREAM + (255,)
    )
    for y in range(52, CARD_H - 12, 40):
        draw.line((26, y, CARD_W - 26, y), fill=RULE + (255,), width=2)
    font = handwriting(34)
    y = 14
    for line in NOTE_LINES:
        draw.text((30, y), line, font=font, fill=INK + (255,))
        if line.startswith("love, maya"):
            text_w = draw.textlength(line + " ", font=font)
            draw_heart(draw, 30 + text_w + 16, y + 22, 11, INK + (255,))
        y += 40
    # Washi tape across the top edge, slightly crooked.
    tape = Image.new("RGBA", (170, 34), (0, 0, 0, 0))
    ImageDraw.Draw(tape).rectangle((0, 0, 169, 33), fill=TAPE)
    tape = tape.rotate(4, resample=Image.BICUBIC, expand=False)
    card.alpha_composite(tape, (CARD_W // 2 - 85, -8))
    return card.rotate(-2, resample=Image.BICUBIC, expand=False)


def main():
    scene = Image.open(HERE / "scene.jpg").convert("RGB")
    side = min(scene.size)
    left = (scene.width - side) // 2
    top = (scene.height - side) // 2
    base = scene.crop((left, top, left + side, top + side))
    base = base.resize((SIZE, SIZE), Image.LANCZOS)

    card = make_note_card()
    centre_x, centre_y = 520, 856
    paste_x = centre_x - card.width // 2
    paste_y = centre_y - card.height // 2

    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (paste_x + 7, paste_y + 9,
         paste_x + card.width + 7, paste_y + card.height + 9),
        radius=10, fill=(0, 0, 0, 110),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    base = base.convert("RGBA")
    base.alpha_composite(shadow)
    base.alpha_composite(card, (paste_x, paste_y))

    out = HERE / "entry.png"
    base.convert("RGB").save(
        out, format="JPEG", quality=88, subsampling=1,
        optimize=False, progressive=False,
    )
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
