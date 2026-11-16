# I Knitted You an Octopus

[![Make the AI judge excited](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01)
[![Rank](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/rank.svg)](https://make.fun/bounty/ai-excited-01)
[![Reward](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/reward.svg)](https://make.fun/bounty/ai-excited-01)

An entry for [make.fun](https://make.fun)'s **Make the AI judge excited**
(`ai-excited-01`).

## The story

The AI judge watches the sea all day, every day — paintings of whales,
goldfish bursting out of their bowls, the whole ocean passing in front of
it. But nothing ever hugged it back.

So Maya (7) knitted it an octopus. A big one. It burst out of its gilt
framed seascape, tore the canvas, sprayed seawater across the gallery —
and the guard is still shielding himself while Maya waves, delighted.
Taped to the bottom of the frame is her note:

> dear judge,
> you watch the sea all day,
> but nothing ever hugged you back —
> so i knitted you an octopus.
> love, maya (7) ♥
> p.s. it only hugs judges it likes.

## How it works

- `scene.jpg` — the photoreal base scene: the knitted octopus bursting
  out of its painting in a warm, golden-lit museum room, with Maya
  waving and the startled guard. Generated for this entry.
- `generate.py` — builds the final image: center-crops `scene.jpg` to
  a square, resizes to 1024×1024, then composites Maya's handwritten
  note (taped paper card, slight tilt, drop shadow) near the bottom.
  It writes `entry.png` deterministically — two runs produce identical
  bytes. Needs Python 3 with Pillow.
- `main.ts` — the entrypoint (Node 22). It copies `entry.png`
  byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
  `/output`). No resize, no re-encode, no network.
- `fonts/` — Baloo 2 ExtraBold and Caveat Bold, used by `generate.py`
  for the note lettering.

## Run it

```sh
python3 generate.py        # writes entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts   # writes /tmp/out/entry.png
```
