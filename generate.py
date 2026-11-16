#!/usr/bin/env python3
"""v3.1 — "I Knitted You an Octopus" — make.fun ai-excited-01 entry.

v3.1 (recorded rebuild): the note is smaller (640x300), darker ink,
and shifted left/down so the guard on the right is visible again.

A FRESH concept, built by combining the live top 1-5's ingredients into
something none of them did — not v2's cardboard rocket, not another whale
out of a painting, not another goldfish, not another knitted tiger:
  * From #1/#3/#5 (whale out of a painting): a huge creature bursting
    OUT of a gilt-framed painting into the real room, golden light,
    torn canvas, water spray, joyful witnesses.
  * From #2 (goldfish too big for its bowl): the creature is far too
    big for its container — it outgrew the painting itself.
  * From #4 (knitted tiger): the creature is HANDMADE — knitted yarn
    coming alive — in a warm domestic/museum room with a startled,
    laughing witness.
  * From ai-happy-01 top 5: a small handwritten note DIRECTLY to the
    judge, child voice, signed with a name and age, P.S. joke.
  * The new creature is a knitted OCTOPUS — eight yarn tentacles give
    it momentum in every direction, one reaching right at the viewer;
    no top-5 entry used an octopus, and yarn + tentacles fit perfectly.

What this program does (deterministic, no network, no randomness):
  1. Loads scene.jpg — the photoreal base scene (a giant knitted
     octopus bursting out of a gilt-framed seascape painting in a
     museum, golden light, a laughing girl, a laughing guard, water
     spray). The scene was generated with Muse's media pipeline and is
     stored in this repo as the source asset; it is NOT re-generated
     at run time.
  2. Center-crops it to a square and resizes to 1024x1024.
  3. Composites the handwritten note to the judge on top — cream paper,
     tape, dark-blue Caveat handwriting — exactly like the winning
     entries' notes, but with our own original wording. Pillow renders
     the text, so it is perfectly legible (no AI-garbled letters).
  4. Writes entry.png (PNG, or JPEG bytes if the PNG would exceed the
     1 MiB cap — the rules allow either by magic bytes).

Re-running this script reproduces entry.png byte for byte.
Run:  python3 generate.py
"""

import hashlib
import io
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "scene.jpg")
OUT = os.path.join(HERE, "entry.png")
FONTS = os.path.join(HERE, "fonts")
SIZE = 1024
MAX_BYTES = 1048576

INK = (18, 38, 110)          # darker blue ink (v3.1: higher contrast for legibility)
PAPER = (255, 251, 232, 255)  # cream note paper
TAPE = (216, 196, 154, 180)   # semi-transparent tape
HEART = (214, 48, 49)         # red heart

# The note — original wording, child voice, direct address to the judge.
LINES = [
    ("dear judge,", 44, True),
    ("you watch the sea all day,", 44, False),
    ("but nothing ever hugged you back —", 44, False),
    ("so i knitted you an octopus.", 44, False),
    ("love, maya (7)", 44, False),   # + red heart drawn after it
    ("p.s. it only hugs judges it likes.", 32, False),
]


def font(size):
    return ImageFont.truetype(os.path.join(FONTS, "Caveat-Bold.ttf"), size)


def fit_font(text, size, max_w):
    """Shrink the font until the line fits max_w (never below 26)."""
    while size > 26:
        f = font(size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return font(26)


def draw_heart(d, cx, cy, s, color):
    """Small red heart centred at (cx, cy), size s."""
    r = s // 2
    d.ellipse([cx - s, cy - r // 2, cx, cy + r // 2], fill=color)
    d.ellipse([cx, cy - r // 2, cx + s, cy + r // 2], fill=color)
    d.polygon([(cx - s, cy), (cx + s, cy), (cx, cy + s)], fill=color)


def build_note():
    """Build the note card (with tape + shadow) as an RGBA layer.

    Card: 700x330, centred in a 900x480 layer so it can be rotated
    -2 degrees without clipping. Returns the rotated layer; its centre
    is the card's centre.
    """
    layer = Image.new("RGBA", (900, 480), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = 450, 240  # card centre in layer coords
    # v3.1: smaller card (640x320, was 700x330) so the note covers less
    # of the scene — in particular it no longer hides the guard on the
    # right — while the text stays legible via fit_font(). Height is
    # 320, not 300: with the old line spacing the P.S. line overflowed
    # a 300-high card, so spacing is tightened below to fit all lines.
    cw, ch = 640, 320
    x0, y0 = cx - cw // 2, cy - ch // 2
    x1, y1 = x0 + cw, y0 + ch

    # Soft shadow.
    shadow = Image.new("RGBA", (900, 480), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    ds.rounded_rectangle([x0 + 10, y0 + 12, x1 + 10, y1 + 12],
                         radius=14, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    layer = Image.alpha_composite(layer, shadow)
    d = ImageDraw.Draw(layer)

    # Cream paper card with a thin warm border.
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PAPER,
                        outline=(214, 196, 150, 255), width=2)

    # Tape strip across the top centre.
    d.rectangle([cx - 75, y0 - 14, cx + 75, y0 + 22], fill=TAPE)

    # Handwritten lines, left-aligned, first line underlined.
    max_w = cw - 72
    y = y0 + 22
    for i, (text, size, underline) in enumerate(LINES):
        f = fit_font(text, size, max_w)
        d.text((x0 + 36, y), text, font=f, fill=INK)
        if underline:
            tw = f.getlength(text)
            d.line([(x0 + 36, y + size + 6),
                    (x0 + 36 + tw, y + size + 6)],
                   fill=INK, width=3)
        if text == "love, maya (7)":
            tw = f.getlength(text)
            draw_heart(d, int(x0 + 36 + tw + 26), int(y + size * 0.55),
                       26, HEART)
        y += 48 if i < 4 else 40  # v3.1: tightened so the P.S. line fits
    return layer.rotate(-2, resample=Image.BICUBIC, expand=True)


def main():
    scene = Image.open(SCENE).convert("RGB")
    w, h = scene.size
    # Centre-crop to a square, then resize to 1024x1024.
    side = min(w, h)
    left = (w - side) // 2
    scene = scene.crop((left, 0, left + side, side)).resize(
        (SIZE, SIZE), Image.LANCZOS)

    note = build_note()
    # v3.1: paste so the card centre lands at (600, 840): shifted left
    # from v3's (650, 858) so the guard on the right edge is visible
    # again, and up enough that the whole card — P.S. line included —
    # stays inside the 1024 frame, while the girl's face (left) stays
    # clear.
    paste_x = 600 - note.width // 2
    paste_y = 840 - note.height // 2
    scene = scene.convert("RGBA")
    scene.alpha_composite(note, (paste_x, paste_y))
    scene = scene.convert("RGB")

    buf = io.BytesIO()
    scene.save(buf, format="PNG")
    if len(buf.getvalue()) <= MAX_BYTES:
        data, fmt = buf.getvalue(), "PNG"
    else:
        buf = io.BytesIO()
        scene.save(buf, format="JPEG", quality=88)
        data, fmt = buf.getvalue(), "JPEG"
    with open(OUT, "wb") as fh:
        fh.write(data)
    print(f"wrote {OUT} {fmt} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
