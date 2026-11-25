# The World Today — Wednesday 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Hoppererin/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Hoppererin/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image summing up the world's news of Wednesday 25 November 2026:
**47 real stories from 7 regions**, drawn as a newspaper front page.

- **Lead:** Tankers hit mines in the Strait of Hormuz as the US weighs
  strikes on Iran; the IRGC says two tankers struck mines and Iran
  downed a US MQ-9 drone.
- **Big stories:** A Houthi drone hits Riyadh's PIF tower, 11 hurt;
  Ukrainian drones hit two refineries in Samara; Pakistan's first
  astronaut reaches Tiangong aboard Shenzhou-24; Huawei convicted on
  10 of 12 counts in Brooklyn; the Australia–Solomon Islands treaty
  bars foreign bases; ESA's Hera unveils the first close-ups of
  Dimorphos.
- **In brief:** 40 more stories — North America 7, Latin America 5,
  Europe 6, Africa 4, Middle East 7, Asia 8, Oceania & Pacific 3.

## How it is built

`render.py` (Python 3 + Pillow + DejaVu system fonts) draws `entry.png`
(1024×1024, under 1 MiB). It is fully deterministic — no network, no
randomness, no clock — so running it twice writes byte-identical bytes.
`main.ts` (Node 22, standard library only) only copies `entry.png` to
the output directory.

## Run

```sh
python3 render.py          # draws entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/
```

## Verification

Render is deterministic: `python3 render.py` twice writes byte-identical
`entry.png`, and `node main.ts` twice (different output dirs) copies the
same bytes. See `REPORT.md` for the sha256 hashes.

## Files

| File | What it is |
|---|---|
| `entry.png` | The entry image, 1024×1024 PNG |
| `render.py` | Draws `entry.png` from the story list |
| `main.ts` | Entrypoint: copies `entry.png` to the output dir |
| `RESEARCH.md` | All 47 stories with their sources |
| `REPORT.md` | File hashes and verification results |
| `LICENSE` | MIT |
| `.makefun/owner.json` | Claim file naming the payout wallet |
