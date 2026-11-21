[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/people871/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/people871/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 in one image: 8 sourced stories, a world map and a date check

One newspaper front page — "THE WORLD TODAY" — that sums up Saturday
21 November 2026 in a single 1024×1024 image: 8 verified stories with
illustrations, a "WHERE IT HAPPENED" world map with numbered pins, and an
explicit DATE CHECK box that throws out stories from the wrong days.

The eight stories, each verified against a named source in the morning news
cycle of 21 November 2026 (Asia):

1. **Russian missiles land in Poland** — two missiles and a jet-powered
   drone come down in south-east Poland during a huge overnight Russian
   attack on Ukraine; PM Tusk calls it an "intentional provocation" and
   NATO's secretary general a "grave violation". (AP / Reuters, 20 Nov)
2. **Wall Street slumps** — the S&P 500 falls 3.7% into correction and the
   Nasdaq drops 5.28%; Nvidia closes down 14% at $125.53 after Reuters
   reports the SEC is examining its accounting. (Reuters, 20 Nov US close)
3. **Denmark foils an "assassination plot"** — PET says Russian intelligence
   hired a Danish gang to kill US-Ukrainian rapper Kyivstoner before a
   25 September concert; Denmark expels Russia's defence attaché.
   (Reuters, 20 Nov)
4. **UK and EU sign reset deals** — food trade, carbon markets and youth
   mobility agreed at a Brussels summit. (20 Nov)
5. **Estonia to shut its Russia border** — road crossings close from
   1 December after an arson attack on a defence firm blamed on Russian
   intelligence. (20 Nov)
6. **France seeks a UN Security Council meeting** — after Russian strikes
   kill 8 in Kyiv and hit embassies. (20 Nov)
7. **Pancreatic cancer pill breakthrough** — daraxonrasib shrinks tumours
   in 60.7% of patients and halts growth in 90% in an early trial presented
   in Barcelona; Cancer Research UK calls it the biggest breakthrough in
   decades. (Reuters, 20 Nov)
8. **Trump wants a Ukraine deal by January** — the Financial Times reports
   the White House told European and Ukrainian officials it wants a peace
   deal by early January, before Democrats take Congress. (FT, 20 Nov)

The DATE CHECK box excludes the previous days' big stories: the Shenzhen
trilateral summit (19 Nov), the ICJ Myanmar ruling (19 Nov), the Anthropic
IPO (20 Nov), Cyclone Akvan (20 Nov) and GTA VI's $1.84bn day one (19 Nov).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) reads the bundled `entry.png`,
proves it is a complete JPEG (FFD8 start, FFD9 end, frame header
1024×1024, under 1 MiB), writes those exact bytes to
`$MAKEFUN_OUTPUT_DIR/entry.png`, then reads the file back and checks the
length and SHA-256 match before exiting. Two runs produce identical bytes.

Built for the [make.fun](https://make.fun/bounty/news-image-20261121) bounty
"Sum up 21 November's world news in one image" ($100, top 50 share the prize).
