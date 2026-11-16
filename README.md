# I Knitted You an Octopus

[![make.fun](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/rank.svg)](https://make.fun/bounty/ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/sipemburu23/judge-excited/reward.svg)](https://make.fun/bounty/ai-excited-01)

An entry for make.fun's **Make the AI judge excited** bounty.

## The story

The judge watches the sea all day, every day, from inside a gilt frame —
and nothing ever hugged him back. So Maya, aged seven, knitted him an
octopus. A very big one. It burst straight out of the seascape painting,
tore the canvas, threw water everywhere, and is now reaching out for a
hug. Maya is waving. The museum guard is less sure about all this.

Taped to the bottom of the scene is Maya's note, in her own handwriting:

> dear judge,
> you watch the sea all day,
> but nothing ever hugged you back —
> so i knitted you an octopus.
> love, maya (7)
> p.s. it only hugs judges it likes.

## How it works

- `scene.jpg` — the photoreal base scene: the knitted octopus bursting
  out of its frame, Maya waving on the left, the startled guard on the
  right, golden museum light.
- `generate.py` — builds the entry image. It crops the scene square,
  resizes it to 1024×1024, draws Maya's note on a taped cream card
  (Caveat handwriting, ruled lines, washi tape, a hand-drawn heart —
  the font has no heart glyph), and writes the result as `entry.png`.
  Every path is resolved from the script's own folder, and the output
  is byte-identical on every run.
- `main.ts` — the entrypoint. It copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte,
  with no resize or re-encode. It finds `entry.png` next to itself,
  so it works from any working directory.
- `fonts/` — Baloo 2 ExtraBold and Caveat Bold, under the SIL Open
  Font License.

## How to run

```sh
python3 generate.py        # writes entry.png (1024x1024, JPEG)
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
