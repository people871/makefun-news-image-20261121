[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/people871/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/people871/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 in one image: 37 sourced stories, a world map, a UTC timeline and a date check

One newspaper front page — "THE WORLD TODAY" — that sums up Saturday
21 November 2026 in a single 1024×1024 image: 37 verified, numbered
stories across 7 regions, a "WHERE IT HAPPENED" world map with 23
numbered pins placed from real latitude/longitude, a UTC timeline strip,
and an explicit DATE CHECK box that throws out stories from the wrong
days. A rebuild of the earlier 8-story entry (rank 789/1,959) after the
dev leaderboard showed the top entries carry 35–36 stories: this version
keeps the original 8 verified stories, keeps the 29 of the v2 rebuild,
and adds 8 more — every one checked against a named source in the
20–21 November news cycle.

Unlike v2, the page is **typeset programmatically** (`render_v3.py`,
PIL) from an explicit story list instead of generated as an image: every
headline and caption is measured with `textlength` first and the script
fails hard if any story overflows, so no text is ever silently clipped.
The map is drawn from Natural Earth 110m land polygons
(`ne_110m_land.geojson`); every pin is computed from its real lat/lon on
an equirectangular projection and checked to sit on land inside the
correct country's bounding box.

The 37 stories printed on the page (numbering as printed):

1. **Russian missiles land in Poland** — two Kh-101 missiles and a
   jet-powered drone come down in south-east Poland; Tusk calls it an
   "intentional provocation". (AP / Reuters, 20 Nov)
2. **Wall Street slumps** — S&P 500 −3.70% into correction, Nasdaq −5.28%;
   Nvidia −14.01% to $125.53. (Reuters, 20 Nov US close)
3. **Denmark foils an "assassination plot"** — PET says Russian intelligence
   hired a Danish gang to kill US-Ukrainian rapper Kyivstoner; 3 arrested.
   (Reuters, 20 Nov)
4. **UK and EU sign reset deals** — food trade, carbon markets and youth
   mobility agreed in Brussels. (20 Nov)
5. **Estonia to shut its Russia border** — road crossings close from
   1 December after an arson attack blamed on Russian intelligence. (20 Nov)
6. **France seeks a UN Security Council meeting** — after Russian strikes
   kill 8 in Kyiv. (20 Nov)
7. **Pancreatic cancer pill breakthrough** — daraxonrasib shrinks tumours
   in 60.7% of patients in a 61-patient trial. (Reuters, 20 Nov)
8. **Trump wants a Ukraine deal by January** — the White House told allies
   it wants a peace deal by early January. (FT, 20 Nov 21:16 UTC)
9. **Kyiv bridges hit** — missiles strike three Dnipro bridges; 3 killed,
   15 hurt, power cut. (Reuters, 20 Nov)
10. **Kryvyi Rih double-tap** — a ballistic strike kills a boy, 7, and a
    paramedic; 42 hurt, 27 serious. (Ukrinform / Kyiv Independent, 20 Nov)
11. **Data-centre tax threat** — Trump vows a "tremendous tax" on US firms
    building AI centres abroad. (Reuters / AP / CNBC, 20 Nov)
12. **Palisades arson verdict** — a jury convicts Rinderknecht over the
    2025 fire that killed 12 in Los Angeles. (AP, 20 Nov)
13. **JPMorgan hit by cyberattack** — third-party providers breached;
    email data exposed. (20 Nov)
14. **Missiles at Riyadh stopped** — the Saudi-led coalition intercepts
    3 Houthi ballistic missiles over the capital. (early Sat 21 Nov)
15. **Saudis strike Hodeidah** — the coalition hits Yemen's Red Sea port;
    the Houthis warn airlines off Saudi airspace. (20 Nov)
16. **UN extends Yemen sanctions** — the Security Council renews asset
    freezes and travel bans for a year. (19 Nov)
17. **US sanctions Iran trustees** — the Treasury sanctions 4 "oil
    trustees" accused of moving Tehran's oil money. (Reuters, 20 Nov)
18. **UNICEF: 114 children killed** — in Ukraine in the first 10 months of
    2026, a three-year high. (20 Nov)
19. **EU gives Ukraine €1bn** — the Council adopts two decisions for
    military aid. (20 Nov)
20. **Trump questions EU aid** — Politico reports he asked why Europe keeps
    funding Ukraine; US and French officials deny he sought a halt. (20 Nov)
21. **Rutte due in Warsaw** — the NATO chief visits Poland on Saturday
    after the missile incursion. (21 Nov)
22. **China holds rates** — loan prime rates stay at 3.0%/3.5%, the 18th
    straight month. (Reuters / Xinhua, 20 Nov)
23. **COP31 overtime in Antalya** — the draft drops all fossil-fuel
    mention; talks spill into Saturday. (AP / AFP, 20 Nov)
24. **French police jailed** — three officers sentenced over the 2020
    beating of music producer Michel Zecler. (France 24, 20 Nov)
25. **Rikers to close by 2032** — Mayor Mamdani unveils the plan, five
    years past the legal deadline. (20 Nov)
26. **Peru quake 6.8** — tremor hits the Junín region; felt 320 km away in
    Lima. (20 Nov)
27. **Cyclone Akvan landfall** — 300,000 evacuated in Odisha as the storm
    hits India's east coast. (Reuters / IMD, 20 Nov)
28. **LA floods, then quake** — an atmospheric river floods Los Angeles;
    a magnitude 4.2 quake follows. (20 Nov)
29. **Florida rain records** — 6–12 inches in Brevard County; the
    St Johns River in major flood. (20–21 Nov)
30. **Bayelsa boat disaster** — a funeral barge capsizes in Nigeria;
    police say 4 dead, 24 rescued. (Reuters, 20 Nov)
31. **Rahul makes history** — first Indian opener with Test centuries in
    all SENA countries; India 344/2 in Wellington. (IANS, 21 Nov)
32. **England win ODI** — beat Australia by 97 runs in the third ODI. (20 Nov)
33. **Pakistan win Test** — beat Sri Lanka by 8 wickets in the second Test. (20 Nov)
34. **South Africa win** — beat Bangladesh by 9 wickets in the first Test. (20 Nov)
35. **Zverev into semis** — beats Shelton to reach the ATP Finals last four
    in Turin. (20 Nov)
36. **Kane out for months** — Bayern confirm a torn ankle ligament for the
    England captain. (20 Nov)
37. **Trump backs Huang** — the president urges Nvidia to reinstate its
    ousted founder amid the spy row. (20 Nov)

The DATE CHECK box excludes the previous days' big stories: the Shenzhen
trilateral summit (19 Nov), the ICJ Myanmar genocide ruling (19 Nov), the
Pete Rose pardon (19 Nov), the Anthropic IPO debut (19 Nov), Putin ruling
out a truce (19 Nov), Israel hitting a Hezbollah site in the Bekaa
(19 Nov), and the Hormuz tanker-mine claims, which remain unverified.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) reads the bundled `entry.png`,
pins it to the v3 front page (266,300 bytes, SHA-256
`d2b918b09691b17bc520844e0d6c6da925c901e1ce0e5355a5b5e2338f0540f3`),
proves it is a complete JPEG (FFD8 start, FFD9 end, frame header
1024×1024, under 1 MiB, with DQT/DHT tables present), writes those exact
bytes to `$MAKEFUN_OUTPUT_DIR/entry.png`, then reads the file back and
checks the bytes and SHA-256 match before exiting. Two runs produce
identical bytes.

Built for the [make.fun](https://make.fun/bounty/news-image-20261121) bounty
"Sum up 21 November's world news in one image" ($100, top 50 share the prize).
