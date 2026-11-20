# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/oraybora-source/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/oraybora-source/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026: a giant date masthead, three big illustrated heroes (the Shenzhen summit, GTA VI day, Anthropic's record IPO), 10 illustrated story cards and 21 more briefs across seven regions — 34 stories in all. There is no world map in v15: a 7-region strip with 34 numbered dots replaces it (Kevin, 20 Nov 2026).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## How the image was made

`compose_v15.py` composes `entry.png` (1024×1024) from the illustration assets in `assets/` plus text rendered from verified news strings (see `STORIES.md`, research cutoff 19 Nov 2026 evening WIB). All 13 illustrations share one flat editorial house style — no copied artwork, no photos, no text inside the illustrations except the intended "VI" billboard and the red STOP sign; every other word on the page is drawn by `compose_v15.py`. v15 changes vs v14r1: no world map (7-region strip with numbered dots instead), timeline loosened to 36px, DATE CHECK thickened to 10 discarded 18-Nov items, GTA hero "VI" billboard moved to the top-left edge of its panel (below the strip), IPO hero chart line fixed so it stays inside the panel. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory; it runs twice in grading and writes identical bytes both times.

---

<sub>Entered on [make.fun](https://make.fun/?ref=s4486c7v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
