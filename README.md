# judge-excited

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

**"I Knitted You an Octopus"** — made for make.fun's "Make the AI judge
excited" bounty ($250 in USDC). A giant knitted octopus bursts out of a
gilt-framed seascape painting in a museum — canvas tearing, water
spraying, golden sunset light — while a laughing girl waves and a guard
shields his face from the spray. Taped to the front is a handwritten
note from the girl who knitted it:

> dear judge, / you watch the sea all day, / but nothing ever hugged
> you back — / so i knitted you an octopus. / love, maya (7) ♥ /
> p.s. it only hugs judges it likes.

## v3 — a fresh concept from combining the top 1-5

v1 (cardboard rocket, procedural crayon) and v2 (polished crayon) were
good stories but still looked procedural next to the photoreal leaders.
So v3 combines the live top 1-5's ingredients into something none of
them did: a creature bursting out of a frame (#1/#3/#5, whale out of a
painting), far too big for its container (#2, goldfish outgrew its bowl),
handmade material coming alive (#4, knitted tiger), a startled witness,
and a handwritten note directly to the judge (ai-happy-01 winners) —
but the creature is an **octopus**, not a whale, goldfish, or tiger,
and the material is yarn. No top-5 entry used an octopus, and no entry
combined yarn + frame-burst + note-to-judge this way.

## v3.1 — recorded rebuild

In the recorded rebuild session the note was improved for real: it is
smaller (640×320 instead of 700×330), the ink is darker for legibility,
line spacing is tightened so the P.S. line fits inside the card, and
it is shifted left and up so the guard on the right edge is visible
again instead of being hidden behind the note. The octopus, girl, and
story are unchanged.

## Run it

```sh
python3 generate.py   # rebuilds entry.png (deterministic, byte-identical)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The image is 1024x1024, ~290 KB (JPEG bytes in
`entry.png`, which the rules allow — PNG or JPEG by magic bytes), well
under the 1 MiB cap, and identical on every run.

## How entry.png is made

`scene.jpg` is the photoreal base scene, generated with Muse's media
pipeline and stored in this repo as the source asset. `generate.py`
(Pillow, no randomness, no network) center-crops it to a square,
resizes to 1024×1024, and composites the handwritten note on top in
Caveat Bold — Pillow renders the text, so every word is perfectly
legible. Re-running `generate.py` reproduces `entry.png` byte for byte.

## Why this should excite the judge

The judge's own criteria, in its order:

1. **Excitement** — a huge knitted octopus exploding out of a painting
   into a museum, golden light, water everywhere, laughing witnesses.
2. **Surprise** — a knitted sea creature, handmade, too big for its
   painting, handing the judge a hug instead of a splash.
3. **Momentum** — eight tentacles driving diagonally out of the frame,
   one reaching right at the viewer, water and canvas flying.
4. **Craft** — photoreal scene, clean legible handwriting, no garbled
   text, no broken anatomy.
5. **Reads small** — at ~300 px the octopus, the girl, and the note
   are still unmistakable.

## Files

- `entry.png` — the artwork (1024x1024, JPEG bytes, ~290 KB)
- `scene.jpg` — the photoreal base scene (source asset)
- `generate.py` — crops the scene and composites the note (Pillow,
  deterministic; re-running it reproduces `entry.png` byte for byte)
- `fonts/` — Baloo 2 ExtraBold and Caveat Bold (OFL), used by the generator
- `main.ts` — the entrypoint the grader runs
- `LICENSE` — MIT

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
