#!/usr/bin/env python3
"""Render the v3 front page for news-image-20261121 — "THE WORLD TODAY".

Own code, written fresh for this rebuild. The page is typeset
programmatically with PIL (no image model): every headline, caption and
map pin is placed from explicit data, so nothing can be misspelled,
clipped or dropped by a generator, and every pin sits at the exact
latitude/longitude of its story. Land outlines come from the public
Natural Earth 110m land polygons (ne_110m_land.geojson, same folder).

Layout at 2048x2048, downscaled to 1024x1024 JPEG for the repo.
Deterministic: no randomness, no timestamps, no network.

Usage: python3 render_v3.py
Writes: entry-2048.png (proof), entry.png (1024 JPEG, the deliverable)
in the current directory.
"""
import json
import sys
from PIL import Image, ImageDraw, ImageFont

SCALE = 2                 # design units are 1024-scale; render at 2x
W = H = 1024 * SCALE
MARGIN = 24 * SCALE
CW = W - 2 * MARGIN       # content width

PAPER = (248, 243, 232)
INK = (24, 22, 18)
RULE = (120, 112, 96)
FAINT = (168, 160, 140)
LAND = (216, 208, 190)
LAND_LINE = (140, 132, 114)
PIN_RED = (178, 34, 34)
PIN_FILL = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# ---------------------------------------------------------------- stories
# (number, headline, caption, region) — 37 stories, renumbered 1..37.
# The 29 v2 stories are kept verbatim in substance; 8 new ones (30-37
# in the old numbering are now interleaved by topic) are marked NEW.
STORIES = [
    (1, "MISSILES LAND IN POLAND",
     "Two Kh-101 missiles and a drone crash in SE Poland; Tusk calls it provocation.", "Europe"),
    (2, "WALL ST SLUMPS",
     "S&P 500 -3.70% into correction; Nasdaq -5.28%; Nvidia -14.01% to $125.53.", "N. America"),
    (3, "DENMARK FOILS PLOT",
     "PET: Russian intel hired a gang to kill rapper Kyivstoner; 3 held, envoy expelled.", "Europe"),
    (4, "UK-EU RESET DEALS",
     "Food trade, carbon markets and youth mobility agreed at Brussels summit.", "Europe"),
    (5, "ESTONIA SHUTS BORDER",
     "Road crossings to Russia close from 1 Dec after arson blamed on Moscow.", "Europe"),
    (6, "FRANCE SEEKS UN MEETING",
     "Paris calls Security Council session after strikes kill 8 in Kyiv.", "Europe"),
    (7, "CANCER PILL BREAKTHROUGH",
     "Daraxonrasib shrinks tumours in 60.7% of patients in 61-person trial.", "Europe"),
    (8, "TRUMP WANTS DEAL BY JANUARY",
     "White House tells allies it wants a Ukraine peace deal by early January.", "N. America"),
    (9, "KYIV BRIDGES HIT",
     "Missiles strike three Dnipro bridges; 3 killed, 15 hurt, power cut.", "Europe"),
    (10, "KRYVYI RIH DOUBLE-TAP",
     "Ballistic strike kills a boy, 7, and a paramedic; 42 hurt, 27 serious.", "Europe"),
    (11, "DATA-CENTRE TAX THREAT",
     "Trump vows a 'tremendous tax' on US firms building AI centres abroad.", "N. America"),
    (12, "PALISADES ARSON VERDICT",
     "Jury convicts Rinderknecht over the 2025 fire that killed 12 in LA.", "N. America"),
    (13, "JPMORGAN HIT BY CYBERATTACK",
     "Third-party providers breached; email data exposed.", "N. America"),
    (14, "MISSILES AT RIYADH STOPPED",
     "Saudi coalition intercepts 3 Houthi ballistic missiles over the capital.", "Middle East"),
    (15, "SAUDIS STRIKE HODEIDAH",
     "Coalition hits Yemen's Red Sea port; Houthis warn airlines off Saudi skies.", "Middle East"),
    (16, "UN EXTENDS YEMEN SANCTIONS",
     "Security Council renews asset freezes and travel bans for a year.", "Middle East"),
    (17, "US SANCTIONS IRAN TRUSTEES",
     "Treasury lists 4 'oil trustees' accused of moving Tehran's oil money.", "Middle East"),
    (18, "UNICEF: 114 CHILDREN KILLED",
     "In Ukraine in the first 10 months of 2026, a three-year high.", "Europe"),
    (19, "EU GIVES UKRAINE 1BN EURO",
     "Council adopts two decisions for military aid to Kyiv.", "Europe"),
    (20, "TRUMP QUESTIONS EU AID",
     "Politico: he asked why Europe keeps funding Ukraine; aides deny a halt.", "N. America"),
    (21, "RUTTE DUE IN WARSAW",
     "NATO chief visits Poland on Saturday after the missile incursion.", "Europe"),
    (22, "CHINA HOLDS RATES",
     "Loan prime rates stay at 3.0% and 3.5% for an 18th straight month.", "Asia"),
    (23, "COP31 OVERTIME IN ANTALYA",
     "Draft deal drops all fossil-fuel mention; talks spill into Saturday.", "Asia"),
    (24, "FRENCH POLICE JAILED",
     "Three officers sentenced over the 2020 beating of producer Michel Zecler.", "Europe"),
    (25, "RIKERS TO CLOSE BY 2032",
     "Mayor Mamdani unveils plan, five years past the legal deadline.", "N. America"),
    (26, "PERU QUAKE 6.8",
     "Tremor hits Junin region; felt 320 km away in Lima.", "S. America"),
    (27, "CYCLONE AKVAN LANDFALL",
     "300,000 evacuated in Odisha as the storm hits India's east coast.", "Asia"),
    (28, "LA FLOODS, THEN QUAKE",
     "Atmospheric river floods Los Angeles; a magnitude 4.2 quake follows.", "N. America"),
    (29, "FLORIDA RAIN RECORDS",
     "6-12 inches in Brevard County; St Johns River in major flood.", "N. America"),
    (30, "BAYELSA BOAT DISASTER",
     "Funeral barge capsizes in Nigeria; police say 4 dead, 24 rescued.", "Africa"),
    (31, "RAHUL MAKES HISTORY",
     "First Indian opener with Test tons in all SENA nations; India 344/2.", "Oceania"),
    (32, "ENGLAND WIN ODI",
     "Beat Australia by 97 runs in the third ODI.", "Oceania"),
    (33, "PAKISTAN WIN TEST",
     "Beat Sri Lanka by 8 wickets in the second Test.", "Asia"),
    (34, "SOUTH AFRICA WIN",
     "Beat Bangladesh by 9 wickets in the first Test.", "Asia"),
    (35, "ZVEREV INTO SEMIS",
     "Beats Shelton to reach the ATP Finals last four in Turin.", "Europe"),
    (36, "KANE OUT FOR MONTHS",
     "Bayern confirm a torn ankle ligament for the England captain.", "Europe"),
    (37, "TRUMP BACKS HUANG",
     "President urges Nvidia to reinstate its ousted founder amid spy row.", "N. America"),
]
assert len(STORIES) == 37, len(STORIES)
assert [s[0] for s in STORIES] == list(range(1, 38))
assert len({s[3] for s in STORIES}) == 7  # 7 regions

# ---------------------------------------------------------------- map pins
# (story, lat, lon, label dx, label dy in 2048 px, expected land bbox
#  lon_min, lon_max, lat_min, lat_max — a rough country box the pin must
#  fall inside; the script asserts this before drawing.)
PINS = [
    (1, 50.4, 22.3, 12, -34, (14.0, 24.2, 49.0, 54.9)),    # SE Poland
    (2, 40.71, -74.01, -52, -46, (-75.5, -73.5, 40.0, 41.5)),  # New York
    (3, 55.68, 12.57, -72, -32, (8.0, 15.2, 54.8, 57.8)),   # Copenhagen
    (4, 50.85, 4.35, -84, -8, (2.5, 6.4, 49.5, 51.6)),      # Brussels
    (5, 59.44, 24.75, 40, -30, (21.7, 28.2, 57.5, 59.7)),   # Tallinn
    (6, 48.86, 2.35, -78, 30, (-5.0, 8.3, 42.5, 51.1)),     # Paris
    (7, 41.39, 2.17, -88, 52, (-9.3, 3.3, 36.0, 43.8)),     # Barcelona
    (8, 38.91, -77.04, 46, 34, (-77.6, -76.5, 38.5, 39.3)), # Washington DC
    (9, 50.45, 30.52, 64, -6, (22.1, 40.2, 44.4, 52.4)),    # Kyiv
    (10, 47.91, 33.39, 52, 52, (22.1, 40.2, 44.4, 52.4)),   # Kryvyi Rih
    (12, 34.05, -118.24, -58, 10, (-119.0, -117.5, 33.5, 34.5)),  # Los Angeles
    (14, 24.71, 46.68, 38, 40, (34.5, 55.7, 16.3, 32.2)),  # Riyadh
    (15, 14.80, 42.95, -34, 44, (42.5, 54.6, 12.1, 19.0)),  # Hodeidah, Yemen
    (17, 35.69, 51.39, 66, -52, (44.0, 63.3, 25.0, 39.8)),  # Tehran
    (22, 39.90, 116.41, 42, -32, (73.5, 134.8, 18.2, 53.6)),  # Beijing
    (23, 36.90, 30.71, 84, 6, (26.0, 45.0, 36.0, 42.2)),    # Antalya
    (26, -11.16, -75.99, -62, 8, (-81.4, -68.7, -18.4, -0.1)),  # Junin, Peru
    (27, 20.30, 85.83, 40, 34, (68.0, 97.4, 8.0, 35.5)),    # Odisha, India
    (29, 28.26, -80.73, 44, -36, (-81.5, -80.0, 27.5, 29.0)),  # Brevard, Florida
    (30, 4.87, 6.17, -34, 46, (2.7, 14.7, 4.2, 13.9)),      # Bayelsa, Nigeria
    (31, -41.29, 174.78, -30, 14, (166.4, 178.6, -47.3, -34.4)),  # Wellington
    (35, 45.07, 7.69, -64, 44, (6.6, 18.5, 35.5, 47.1)),    # Turin
    (36, 48.14, 11.58, -52, 18, (5.9, 15.1, 47.3, 55.1)),   # Munich
]

TIMELINE = [
    ("03:30 UTC", "Poland jets scramble"),
    ("06:10 UTC", "Kyiv toll 8"),
    ("09:30 UTC", "EU aid \u20ac1bn"),
    ("14:30 UTC", "Riyadh intercepts"),
    ("21:16 UTC", "FT: Ukraine deal"),
    ("23:00 UTC", "Kryvyi Rih toll 42"),
]

DATE_CHECK = ("Shenzhen summit 19 Nov \u00b7 ICJ Myanmar ruling 19 Nov \u00b7 "
              "Pete Rose pardon 19 Nov \u00b7 Anthropic IPO debut 19 Nov \u00b7 Putin rules out "
              "truce 19 Nov \u00b7 Israel hits Hezbollah site, Bekaa 19 Nov \u00b7 Hormuz "
              "tanker-mine claims unverified")
SOURCES = "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 Al Jazeera \u00b7 Financial Times \u00b7 BBC \u00b7 IANS \u00b7 France 24 \u00b7 Xinhua \u00b7 Ukrinform"

# ---------------------------------------------------------------- helpers
def font(path, px1024):
    return ImageFont.truetype(path, int(px1024 * SCALE))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines. Fails loudly on a word
    that cannot fit alone, so no text is ever silently clipped."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if not cur:
                raise SystemExit(f"WRAP FAIL: single word too wide: {w!r}")
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def point_in_polygon(lon, lat, ring):
    """Ray casting on one lon/lat ring."""
    inside, n = False, len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat):
            xinters = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xinters:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat, polys):
    for poly in polys:
        if point_in_polygon(lon, lat, poly[0]):
            return True
        for hole in poly[1:]:
            if point_in_polygon(lon, lat, hole):
                return False
    return False


def load_land():
    with open("ne_110m_land.geojson", encoding="utf-8") as fh:
        data = json.load(fh)
    polys = []
    for feat in data["features"]:
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            polys.append(geom["coordinates"])
        elif geom["type"] == "MultiPolygon":
            polys.extend(geom["coordinates"])
    return polys


# Map projection: equirectangular, lon -180..180, lat -60..84.
MAP_LAT_TOP, MAP_LAT_BOT = 84.0, -60.0


def project(lon, lat, x0, y0, mw, mh):
    x = x0 + (lon + 180.0) / 360.0 * mw
    y = y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * mh
    return x, y


# ---------------------------------------------------------------- page
def main():
    land = load_land()

    # --- verify every pin: on land, and inside its expected country box
    for num, lat, lon, _dx, _dy, (lo0, lo1, la0, la1) in PINS:
        if not (lo0 <= lon <= lo1 and la0 <= lat <= la1):
            raise SystemExit(f"PIN {num} outside its country box: {lat},{lon}")
        if not on_land(lon, lat, land):
            raise SystemExit(f"PIN {num} NOT ON LAND: {lat},{lon}")
    print(f"pins verified: {len(PINS)} on land, inside country boxes")

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=3 * SCALE)

    # --- masthead
    f_mast = font(SERIF_B, 46)
    f_date = font(SANS_B, 15)
    f_sub = font(SANS_B, 15)
    y = 18 * SCALE
    d.text((W / 2, y), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    assert d.textlength("THE WORLD TODAY", font=f_mast) <= CW, "masthead too wide"
    y += 62 * SCALE
    d.text((W / 2, y), "S A T U R D A Y   2 1   N O V E M B E R   2 0 2 6",
           font=f_date, fill=INK, anchor="ma")
    y += 26 * SCALE
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2 * SCALE)
    y += 8 * SCALE
    d.text((W / 2, y), "37 SOURCED STORIES \u2014 7 REGIONS",
           font=f_sub, fill=INK, anchor="ma")
    y += 26 * SCALE
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2 * SCALE)

    # --- story grid: 4 columns, 10 / 9 / 9 / 9 stories
    f_head = font(SANS_B, 12)
    f_cap = font(SANS, 10.5)
    cols = [STORIES[0:10], STORIES[10:19], STORIES[19:28], STORIES[28:37]]
    grid_y0 = y + 10 * SCALE
    grid_h = 565 * SCALE
    row_h = grid_h / 10
    gutter = 18 * SCALE
    col_w = (CW - 3 * gutter) / 4
    drawn = 0
    for ci, col in enumerate(cols):
        x0 = MARGIN + ci * (col_w + gutter)
        if ci:
            d.line([(x0 - gutter / 2, grid_y0), (x0 - gutter / 2, grid_y0 + grid_h)],
                   fill=FAINT, width=1 * SCALE)
        for ri, (num, head, cap, _region) in enumerate(col):
            sy = grid_y0 + ri * row_h
            num_txt = f"{num}  "
            num_w = d.textlength(num_txt, font=f_head)
            head_lines = wrap(d, head, f_head, col_w - num_w)
            cap_max = 3 if len(head_lines) == 1 else 2
            cap_lines = wrap(d, cap, f_cap, col_w)
            if len(cap_lines) > cap_max:
                raise SystemExit(
                    f"STORY {num} OVERFLOW: headline {len(head_lines)} lines, "
                    f"caption {len(cap_lines)} lines (max {cap_max}): {cap!r}")
            block_h = len(head_lines) * 14 * SCALE + len(cap_lines) * 12.5 * SCALE
            if block_h > row_h - 2 * SCALE:
                raise SystemExit(f"STORY {num} BLOCK TOO TALL: {block_h / SCALE:.1f}px")
            ty = sy
            d.text((x0, ty), num_txt, font=f_head, fill=PIN_RED, anchor="la")
            for ln in head_lines:
                d.text((x0 + num_w, ty), ln, font=f_head, fill=INK, anchor="la")
                ty += 14 * SCALE
            for ln in cap_lines:
                d.text((x0, ty), ln, font=f_cap, fill=(52, 48, 40), anchor="la")
                ty += 12.5 * SCALE
            drawn += 1
    print(f"stories drawn: {drawn}")
    assert drawn == 37

    # --- map band: WHERE IT HAPPENED
    f_sect = font(SANS_B, 13)
    f_pin = font(SANS_B, 10.5)
    f_lab = font(SANS_B, 9)
    map_y0 = (150 + 565 + 8) * SCALE          # 723 @1024
    d.text((W / 2, map_y0), "WHERE IT HAPPENED \u2014 23 PLACES PINNED",
           font=f_sect, fill=INK, anchor="ma")
    mx0, my0 = MARGIN, map_y0 + 22 * SCALE
    mw, mh = CW, 190 * SCALE
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], outline=RULE, width=1 * SCALE)
    # graticule
    for lon in range(-180, 181, 30):
        x, _ = project(lon, 0, mx0, my0, mw, mh)
        d.line([(x, my0), (x, my0 + mh)], fill=(226, 220, 204), width=1)
    for lat in range(-60, 85, 30):
        _, y = project(0, lat, mx0, my0, mw, mh)
        d.line([(mx0, y), (mx0 + mw, y)], fill=(226, 220, 204), width=1)
    # land
    for poly in land:
        for ring in poly:
            pts = [project(lon, lat, mx0, my0, mw, mh)
                   for lon, lat in ring if lat >= MAP_LAT_BOT - 5]
            if len(pts) > 2:
                d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # continent labels (grey, placed in empty sea/land gaps)
    for txt, lon, lat in [("NORTH AMERICA", -102, 52), ("SOUTH AMERICA", -58, -18),
                          ("AFRICA", 10, -10),
                          ("ASIA", 92, 58), ("AUSTRALIA", 134, -26)]:
        x, y = project(lon, lat, mx0, my0, mw, mh)
        d.text((x, y), txt, font=f_lab, fill=(120, 112, 92), anchor="mm")
    # pins: red dot at the exact lat/lon, numbered label on a leader line.
    # First verify the label layout: no two labels overlap, and no label
    # covers another story's dot.
    pin_xy = []
    for num, lat, lon, dx, dy, _box in PINS:
        px, py = project(lon, lat, mx0, my0, mw, mh)
        pin_xy.append((num, px, py, px + dx * SCALE, py + dy * SCALE))
    for i, (n1, x1, y1, lx1, ly1) in enumerate(pin_xy):
        for (n2, x2, y2, lx2, ly2) in pin_xy[i + 1:]:
            dist = ((lx1 - lx2) ** 2 + (ly1 - ly2) ** 2) ** 0.5
            if dist < 50:
                raise SystemExit(f"LABEL OVERLAP: {n1} and {n2} only {dist:.0f}px apart")
        for (n2, x2, y2, _lx2, _ly2) in pin_xy:
            if n2 == n1:
                continue
            dist = ((lx1 - x2) ** 2 + (ly1 - y2) ** 2) ** 0.5
            if dist < 34:
                raise SystemExit(f"LABEL {n1} covers dot {n2} ({dist:.0f}px)")
    print(f"label layout verified: {len(pin_xy)} labels, no overlaps")
    for num, lat, lon, dx, dy, _box in PINS:
        px, py = project(lon, lat, mx0, my0, mw, mh)
        lx, ly = px + dx * SCALE, py + dy * SCALE
        d.line([(px, py), (lx, ly)], fill=(120, 60, 60), width=1 * SCALE)
        d.ellipse([px - 5 * SCALE, py - 5 * SCALE, px + 5 * SCALE, py + 5 * SCALE],
                  fill=PIN_RED, outline=(255, 255, 255), width=1 * SCALE)
        r = 13 * SCALE
        d.ellipse([lx - r, ly - r, lx + r, ly + r],
                  fill=PIN_FILL, outline=PIN_RED, width=2 * SCALE)
        d.text((lx, ly), str(num), font=f_pin, fill=PIN_RED, anchor="mm")

    # --- timeline strip (UTC)
    f_time = font(SANS_B, 10.5)
    f_tl = font(SANS, 10.5)
    tl_y = my0 + mh + 6 * SCALE
    d.line([(MARGIN, tl_y), (W - MARGIN, tl_y)], fill=RULE, width=1 * SCALE)
    tl_y += 4 * SCALE
    d.text((MARGIN, tl_y), "TIMELINE \u2014 UTC", font=f_time, fill=INK, anchor="la")
    tl_txt = " \u00b7 ".join(f"{t}  {s}" for t, s in TIMELINE)
    tw = d.textlength(tl_txt, font=f_tl)
    assert tw <= CW - 130 * SCALE, f"timeline too wide: {tw / SCALE:.0f}px"
    d.text((MARGIN + 118 * SCALE, tl_y), tl_txt, font=f_tl, fill=INK, anchor="la")
    tl_y += 16 * SCALE
    d.line([(MARGIN, tl_y), (W - MARGIN, tl_y)], fill=RULE, width=1 * SCALE)

    # --- date check box + sources
    f_dc = font(SANS_B, 10.5)
    f_dc2 = font(SANS, 10)
    dc_y = tl_y + 6 * SCALE
    dc_h = 44 * SCALE
    box_w = 660 * SCALE
    d.rectangle([MARGIN, dc_y, MARGIN + box_w, dc_y + dc_h],
                outline=INK, width=1 * SCALE)
    d.text((MARGIN + 8 * SCALE, dc_y + 4 * SCALE),
           "DATE CHECK \u2014 NOT 21 NOVEMBER:", font=f_dc, fill=INK, anchor="la")
    dc_lines = wrap(d, DATE_CHECK, f_dc2, box_w - 16 * SCALE)
    assert len(dc_lines) <= 2, f"date check wraps to {len(dc_lines)} lines"
    ty = dc_y + 19 * SCALE
    for ln in dc_lines:
        d.text((MARGIN + 8 * SCALE, ty), ln, font=f_dc2, fill=INK, anchor="la")
        ty += 12.5 * SCALE
    src_lines = wrap(d, SOURCES, f_dc2, CW - box_w - 16 * SCALE)
    assert len(src_lines) <= 3, f"sources wrap to {len(src_lines)} lines"
    ty = dc_y + 4 * SCALE
    for ln in src_lines:
        d.text((W - MARGIN, ty), ln, font=f_dc2, fill=INK, anchor="ra")
        ty += 12.5 * SCALE
    assert dc_y + dc_h <= H - 10 * SCALE, "page overflow"

    # --- save: 2048 proof + 1024 JPEG deliverable
    img.save("entry-2048.png")
    small = img.resize((1024, 1024), Image.LANCZOS)
    small.save("entry.png", "JPEG", quality=88, optimize=True)
    import hashlib
    import os
    raw = open("entry.png", "rb").read()
    print(f"entry.png: {len(raw)} bytes, "
          f"sha256 {hashlib.sha256(raw).hexdigest()}")
    print(f"entry-2048.png: {os.path.getsize('entry-2048.png')} bytes")


if __name__ == "__main__":
    main()
