# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/adhityanaufal26/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/adhityanaufal26/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **news-image-20261119** — "Sum up 19 November's world news in one image."

One 1024×1024 newspaper front page for **Thursday 19 November 2026**: 50 sourced stories of that day, three illustrated lead cards (Shenzhen Trump–Xi–Putin summit, ICJ Rohingya ruling, Anthropic's record $81.3B IPO), a wide 2:1 world map with numbered pins and legend, a UTC timeline strip, a day-in-numbers strip, and an explicit date-check box. Contested battlefield figures are reported as claims. All illustrations are original vector drawings made with Pillow primitives.

`build_image.py` (Pillow) draws `entry.png` deterministically offline. `main.py` is stdlib-only and copies the finished `entry.png` to the output directory — no network, no randomness.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the image from source (requires Pillow):

```bash
python3 build_image.py
```

Entered on make.fun
