# compose_v2.py — builds entry.png (1024x1024) for news-image-20261119, v2.
#
# Design: sketch B-rev1 (31 stories: 3 heroes + 10 cards in 2 rows x 5
# columns + 18 briefs, map + MORE STORIES, DATE CHECK bar). Geometry,
# fonts and colours reproduce that sketch exactly; only the pictures
# change (AI illustrations instead of the sketch's Pillow stand-ins)
# plus the defect fixes listed below.
#
# v2 changes vs the B-rev1 sketch (all decided before this build):
#  1. All 13 panels use AI illustrations (files in assets/). Three were
#     regenerated in this session: the summit (the old one was a
#     photorealistic photo-style image; Kevin disliked that look — the
#     new one is a flat editorial drawing with friendly plain faces),
#     the IPO (the old one showed no "Anthropic" board; the new one
#     has a big dark board reading "Anthropic" with the orange star
#     and a rising gold chart), and the Uganda car plant (the old one
#     showed two men shaking hands, but the second president, Samia,
#     is a woman; the new one shows a woman and a man).
#  2. Uganda card summary fixed: "Museveni and Samia open plant"
#     (the duel judge read it as a typo, "open open car plant") is now
#     "Museveni and Samia at launch".
#  3. DATE CHECK wording fixed: "...Van Gogh sale are 18 Nov: left
#     out." is now "...Van Gogh sale: all 18 Nov, left out."
#  4. Brief 31 replaced: "Yemen: Houthi rocket kills 53 soldiers."
#     is OUT. That attack happened on Monday 19 OCTOBER 2026
#     (Reuters / AP, 19 Oct), not 19 November — keeping it would
#     repeat the Van Gogh wrong-date mistake. Replacement, verified
#     19 Nov by Reuters: "Saudi Arabia: Danger has passed in the
#     south." (Saudi Civil Defense lifted the danger alerts; the
#     coalition dealt with the missile threat towards Riyadh on
#     Thursday 19 Nov). Region count unchanged (MIDEAST still 5),
#     total still 31, columns still 6/6/6.
#  5. Map improved (the duel judges called the sketch map a jumble):
#     continent outlines drawn 2px wide, pins bigger (r 6, 8pt
#     numbers), brief dots bigger (r 3) and kept further apart
#     (9px minimum instead of 8px). Same places, same projection.
#  6. Cover-crop now centres horizontally as well as vertically, so
#     the main subject stays in the middle of each picture box.
#
# v3 changes (20 Nov, Kevin's instruction before reporting): ONE house
# style for all 13 pictures — flat modern editorial illustration,
# clean vector shapes, simple forms, bold flat colour blocks, warm
# cream paper, navy outlines. The v2 entry mixed flat illustrations
# (the 3 heroes) with photo-like cards, so 10 pictures were redrawn
# to the same flat style: GTA hero (was a neon render; now a flat
# art-deco pink/teal Vice City street, big pink car, big "VI"
# billboard), Gaza, Ukraine aid, ICJ, Cyclone, SARB, Berlin, COP31,
# Prague, Kyiv. COP31 needed a second draw (the first had
# "CLIMATE CONFERENCE 2024" written on its screen — the wrong year;
# the redraw has no text at all). Kept from v2, already flat:
# summit, IPO, Uganda. Titles, texts, numbers, layout and the v2
# defect fixes above are unchanged; only the pictures' style changed.
# Focus values were re-tuned per new picture (see HEROES / CARDS);
# crop windows were chosen so no in-picture text with a wrong date
# or number can show (Ukraine "APRIL 2024", SARB "04 NOV 2026" /
# "RATE HIKE", COP31 "2024" are all outside the crop).
#
# v4 changes (20 Nov ~06:00, Kevin 05:48 WIB: "Two president belum pake
# sketsa. Gambar 5-13 bisa di cek lagi. Gambarnya tuh ke potong teks nya.
# Contohnya no 8, saya tuh pengennya keliatan gedung full ga kepotong."):
# All 9 card pictures 5-13 were REDRAWN in wide 3:1 format with the
# subject whole inside the frame, then NORMALISED onto a 1930x700 canvas
# (exact 2.757:1 card-box aspect) so cover_crop shows them whole:
# subject bbox fitted into an inner box (3% sides, 18% top to clear the
# 10px strip, 3% bottom), padded with each picture's OWN corner colour.
#  - 10 Uganda follows the sketch: big red car whole centre-right (main
#    subject), two SMALL presidents shaking hands at far left, factory
#    behind (was: two big suited men hiding the car).
#  - 5 Ukraine: Capitol whole with sky margin, flag on short pole with
#    tripod base fully visible, crates whole. 6 ICJ: palace whole with
#    sky margin, spire tip clear of the strip, Myanmar flag + gavel +
#    files whole. 7 Cyclone: spiral + temple town whole. 8 SARB: bank
#    building whole with margins left AND right (Kevin's example); the
#    red arrow shaft (cut at the top edge in the first draw) was
#    shortened with a clean perpendicular cut in PIL — no 3rd draw.
#    The second SARB draw was REJECTED (building = a long bar touching
#    both edges, the exact defect Kevin flagged).
#  - 9 Berlin: gate whole incl. quadriga + eagle with sky margin, table
#    + 6 people + flags whole. 11 COP31: chart screen + red X + 3
#    chimneys whole (bottom stage/audience band, cut at the source's
#    bottom edge, cropped out before normalising). 12 Prague: twin-
#    towered church whole with spires + sky margin. 13 Kyiv: launcher
#    truck whole with side margins, STOP sign whole, flags whole.
#  - In-picture text: only "VI" (GTA hero, unchanged) and "STOP"
#    (Kyiv) remain, both whole; no half-cut letters at any edge.
#  - All card focus values are now 0.5 (assets are exact box aspect,
#    cover_crop is a pure scale). Titles, texts, numbers, layout,
#    house style and the v2/v3 defect fixes are unchanged.
#
# Run:  python3 compose_v2.py   (needs Pillow; writes entry.png here)
# The entrypoint main.py only copies entry.png — it never re-renders.

import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024

# ---- palette (same paper/ink as the sketch) ----
PAPER = (246, 241, 231)
INK = (24, 28, 36)
NAVY = (15, 36, 64)
RED = (178, 44, 36)
GOLD = (217, 164, 65)
MUTED = (92, 96, 104)
CARD_BG = (250, 247, 240)
CARD_LINE = (205, 200, 185)
SEA = (198, 220, 236)
LAND = (210, 188, 140)
LAND_LINE = (168, 148, 108)
WHITE = (255, 255, 255)

REGION_COLORS = {
    "AMERICAS": (178, 44, 36),
    "EUROPE": (40, 90, 160),
    "MIDEAST": (200, 120, 40),
    "ASIA": (130, 80, 160),
    "AFRICA": (40, 130, 70),
    "OCEANIA": (30, 140, 140),
    "WORLD": (110, 110, 110),
}
REGION_ORDER = [
    ("EUROPE", "EUROPE"),
    ("THE AMERICAS", "AMERICAS"),
    ("ASIA-PACIFIC", "ASIA"),
    ("MIDEAST", "MIDEAST"),
    ("AFRICA", "AFRICA"),
    ("OCEANIA", "OCEANIA"),
    ("WORLD", "WORLD"),
]
# Hero strips use fixed colours (not the region greedy pick).
HERO_STRIPS = [(130, 80, 160), (178, 44, 36), (122, 28, 28)]

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ---- geometry (B-rev1, unchanged) ----
GAP = 1
HERO_H, HERO_IMG, HERO_HEAD, HERO_DECK = 220, 121, 24, 13
CARD_H, CARD_IMG, CARD_HEAD, CARD_SUM = 152, 70, 16, 13
MAP_W = 260
BRIEF_SIZE, BRIEF_LH = 14, 16

# ---- stories ----
# Heroes: file, headline, deck, strip, region, focus_y (0=top, 1=bottom).
HEROES = [
    {
        "file": "media-generation-hero-summit-v2-0-2ef3918e-852b-4192-82f2-4dc4ce2eedb5.png",
        "headline": "Trump, Xi and Putin meet in Shenzhen",
        "deck": "Trade truce and nuclear arms top the agenda as the three leaders meet in Shenzhen",
        "strip": "1 · SHENZHEN · SUMMIT",
        "region": "ASIA",
        "focus": 0.55,
    },
    {
        "file": "media-generation-hero-gtavi-0-2ba192a8-4751-42fd-bb85-541410d0920c.png",
        "headline": "GTA VI launches worldwide",
        "deck": "Gamers enter Vice City as the launch begins on PlayStation 5 and Xbox",
        "strip": "2 · NEW YORK · GAMES",
        "region": "AMERICAS",
        "focus": 0.57,
    },
    {
        "file": "media-generation-hero-ipo-v2-0-49b14d6a-813e-4e61-a965-6d53f5fc43fb.png",
        "headline": "Anthropic's $81.3bn IPO — a record",
        "deck": "Priced at $83 a share, the biggest IPO ever; markets rise ahead of the debut",
        "strip": "3 · NASDAQ · MARKETS",
        "region": "AMERICAS",
        "focus": 0.48,
    },
]

# Cards in reading order (numbers 4-13): city, title, file, s1, s2,
# strip, region, focus_y.
CARDS = [
    ("Gaza", "Israel pushes past Gaza line",
     "media-generation-card-gaza-0-f096b08f-9edf-4908-b025-7a2ac5ab476f.png",
     "Rare ground op", "Troops cross the ceasefire line",
     "4 · GAZA · CEASEFIRE LINE", "MIDEAST", 0.50),
    ("Washington", "US approves $1.6bn Ukraine aid",
     "media-generation-card-ukraine-0-1bb1ae8f-f27e-4ca3-81ce-65f60fefa8a5.png",
     "Approved Thursday:", "$1.6bn for Ukraine",
     "5 · WASHINGTON · UKRAINE AID", "AMERICAS", 0.50),
    ("The Hague", "ICJ verdict in Myanmar case",
     "media-generation-card-icj-0-011a1eeb-2b66-41b8-a944-1d5ddf9a0fda.png",
     "Judgment read today", "Rohingya case at UN court",
     "6 · THE HAGUE · GENOCIDE CASE", "EUROPE", 0.50),
    ("Puri", "Cyclone Akvan nears India coast",
     "media-generation-card-cyclone-0-d9f8d73c-ef93-4c67-b3e4-31660ea6557b.png",
     "Red alerts out; schools shut", "Machilipatnam to Puri",
     "7 · PURI · CYCLONE AKVAN", "ASIA", 0.50),
    ("Johannesburg", "South Africa holds rates",
     "media-generation-card-sarb-0-1ae3bf5f-15dd-42cd-9cf8-09688ab8d5fa.png",
     "SARB holds repo at 7.25%", "Rand at lowest of the year",
     "8 · JOHANNESBURG · RATES", "AFRICA", 0.50),
    ("Berlin", "Coalition of the Willing in Berlin",
     "media-generation-card-berlin-0-bf1abbaa-3f07-4a81-bf3c-09cc2250243e.png",
     "Witkoff and Kushner attend", "Coalition meets in Berlin",
     "9 · BERLIN · COALITION TALKS", "EUROPE", 0.50),
    ("Mpigi", "Two presidents open car plant",
     "media-generation-card-uganda-v2-0-3a6cb6aa-71d0-4b1a-8a03-8950e79bddec.png",
     "Museveni and Samia at launch", "Double Q in Mpigi",
     "10 · MPIGI · CAR PLANT", "AFRICA", 0.50),
    ("Antalya", "COP31 draft drops fossil fuel",
     "media-generation-card-cop31-0-b3cba7ef-38d6-43dc-b5ed-902701778d89.png",
     "Draft drops fossil phase-out", "1.5°C may pass",
     "11 · ANTALYA · COP31 DRAFT", "MIDEAST", 0.50),
    ("Prague", "Prague protest for free media",
     "media-generation-card-prague-0-85b675a9-6723-4533-ac21-802291588bd5.png",
     "Crowds demand free press", "Huge march in Prague",
     "12 · PRAGUE · MEDIA PROTEST", "EUROPE", 0.50),
    ("Kyiv", "Zelensky: US blocks missiles",
     "media-generation-card-kyiv-0-bd53f931-1191-476d-9dd6-cafd2dc91fdd.png",
     "Kyiv accuses Washington", "Missile deliveries held back",
     "13 · KYIV · MISSILE DELIVERIES", "EUROPE", 0.50),
]

# Briefs in reading order (numbers 14-31): city, region, text.
# Every text is the first sentence of the verified story.
BRIEFS = [
    ("New Delhi", "ASIA", "Congress targets the Modi government over inflation."),
    ("Saada", "MIDEAST", "Saudi intercepts a Houthi missile."),
    ("Tokyo", "ASIA", "India and Japan hold 2+2 defence talks."),
    ("Australia", "OCEANIA", "The jobless rate jumps to 4.9%."),
    ("Global", "WORLD", "Bitcoin slips below $63,000."),
    ("Dakar", "AFRICA", "Senegal holds Armed Forces Day."),
    ("Shenzhen", "ASIA", "Trump mentions ex-Nvidia boss Huang 'briefly' in Xi talks."),
    ("MAIB", "WORLD", "The Bayesian had a hidden wind weakness."),
    ("US", "WORLD", "Microsoft is in talks to sell AI services to ByteDance."),
    ("Shenzhen", "EUROPE", "Japan PM Takaichi holds talks with Putin."),
    ("Tokyo", "ASIA", "Japan machinery orders dip 0.3%."),
    ("Brussels", "EUROPE", "The EU delays methane rules by two years."),
    ("Kuala Lumpur", "ASIA", "UNHCR halts refugee registration in Malaysia."),
    ("Taiwan", "ASIA", "A transnational repression bill is drafted."),
    ("Finland", "EUROPE", "The first nuclear waste store is approved."),
    ("Wellington", "OCEANIA", "Bumrah strikes twice at lunch."),
    ("Hormuz", "MIDEAST", "A tanker is hit by a projectile."),
    ("Saudi Arabia", "MIDEAST", "Danger has passed in the south."),
]

# Big numbers strip (number, caption, region of the divider colour).
NUMBERS = [
    ("$81.3bn", "Anthropic IPO — largest ever", "AMERICAS"),
    ("$83", "Anthropic IPO price", "AMERICAS"),
    ("$1.6bn", "US aid package for Ukraine", "AMERICAS"),
    ("7.25%", "SARB holds repo rate", "AFRICA"),
    ("4.9%", "Australia jobless — highest", "OCEANIA"),
    ("$63,000", "Bitcoin slips below, down 2.7%", "WORLD"),
]

COUNTS = [("EUROPE", 7), ("THE AMERICAS", 3), ("ASIA-PACIFIC", 8),
          ("MIDEAST", 5), ("AFRICA", 3), ("OCEANIA", 2), ("WORLD", 3)]
TOTAL = 31

DATECHECK_MSG = ("All 31 stories are 19 November 2026 — Fed minutes, "
                 "Voyager 1, Nvidia H200 halt, EU loan, Van Gogh sale: "
                 "all 18 Nov, left out.")
SOURCES_LINE = ("Sources: Reuters · BBC · The Guardian · Fox News · ABS · "
                "CoinGecko · Al Jazeera · gov.uk · TBS · Daily Star · ANI · "
                "Kampala Post · NBS TV · ECOWAS · PropFlow360")

# ---- map data ----
# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-80, 73),
     (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-76, 35), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-102, 18), (-110, 24), (-117, 33),
     (-124, 40), (-124, 49), (-135, 58), (-150, 60), (-168, 66)],
    [(-45, 60), (-32, 68), (-22, 70), (-20, 76), (-40, 80), (-58, 76),
     (-55, 70), (-45, 60)],
    [(-79, 9), (-72, 11), (-62, 9), (-52, 5), (-50, -2), (-42, -5),
     (-35, -9), (-39, -18), (-48, -28), (-55, -35), (-62, -41), (-68, -50),
     (-73, -54), (-74, -44), (-72, -30), (-80, -18), (-81, -5), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (5, 57), (8, 57), (12, 55),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70), (22, 70),
     (15, 68), (10, 64), (5, 60), (-2, 57), (-6, 53), (-10, 50), (-10, 44),
     (-10, 36)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (3, 37), (10, 37),
     (15, 32), (22, 33), (30, 31), (34, 28), (37, 22), (43, 12), (48, 11),
     (51, 12), (46, 2), (41, -8), (38, -18), (33, -26), (28, -33),
     (20, -35), (16, -29), (14, -22), (12, -17), (9, -2), (9, 4), (0, 6),
     (-8, 5), (-13, 8), (-17, 15)],
    [(30, 70), (60, 70), (90, 75), (120, 73), (150, 70), (178, 66),
     (170, 60), (158, 52), (142, 40), (130, 33), (122, 38), (118, 25),
     (108, 18), (103, 7), (97, 15), (91, 22), (85, 19), (77, 8), (72, 20),
     (63, 25), (54, 27), (48, 30), (40, 32), (36, 36), (30, 42), (30, 70)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    [(-5, 50), (-3, 53), (-1, 55), (0, 53), (1, 51), (-2, 50), (-5, 50)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 39),
     (143, 42), (144, 44), (142, 42), (140, 38), (137, 35), (134, 34),
     (131, 32), (130, 31)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -41),
     (172, -43), (169, -46), (167, -45)],
]

# City -> (lon, lat). Only places that appear on the page need entries.
PLACES = {
    "Gaza": (34.4, 31.4),
    "Washington": (-77.0, 38.9),
    "Kyiv": (30.5, 50.4),
    "Estonia": (24.7, 59.4),
    "Prague": (14.4, 50.1),
    "Spain": (-3.7, 40.4),
    "Kerch": (36.5, 45.3),
    "The Hague": (4.3, 52.1),
    "Puri": (85.8, 19.8),
    "Taiwan": (121.0, 25.0),
    "Yemen": (44.2, 15.3),
    "Saudi Arabia": (46.7, 24.6),
    "Finland": (24.9, 60.2),
    "Wellington": (174.8, -41.3),
    "Berlin": (13.4, 52.5),
    "Saada": (43.8, 16.9),
    "Tokyo": (139.7, 35.7),
    "Hormuz": (56.3, 26.6),
    "Shenzhen": (114.1, 22.5),
    "New Delhi": (77.2, 28.6),
    "London": (-0.1, 51.5),
    "UK": (-0.1, 51.5),
    "US": (-77.0, 38.9),
    "China": (116.4, 39.9),
    "Australia": (149.1, -35.3),
    "Kuala Lumpur": (101.7, 3.1),
    "Beijing": (116.4, 39.9),
    "Brussels": (4.4, 50.8),
    "Johannesburg": (-28.0, -26.2),
    "Mpigi": (32.3, 0.2),
    "Antalya": (30.7, 36.9),
    "Dakar": (-17.4, 14.7),
}

# Hand-tuned pin offsets (dx, dy in px) so clustered pins do not
# overlap; a thin leader line joins each offset pin to its true spot.
PIN_OFFSETS = {
    "Finland": (0, -12),
    "Prague": (0, 14),
    "The Hague": (-14, 0),
    "Kerch": (12, 0),
    "Saada": (0, 14),
    "Hormuz": (0, -12),
    "Taiwan": (12, 0),
    "Antalya": (16, -12),
}
# Which pins get a name label, and on which side (l/r/a/b).
PIN_LABELS = {"Gaza": "l", "Wellington": "l", "Tokyo": "a", "Shenzhen": "b"}

# Strip colour choices per region (first pick is the region colour;
# the rest are nearby shades so neighbours can always differ).
STRIP_VARIANTS = {
    "ASIA": [(130, 80, 160), (160, 110, 190), (100, 60, 130)],
    "AMERICAS": [(178, 44, 36), (140, 30, 30), (205, 70, 55)],
    "EUROPE": [(40, 90, 160), (90, 150, 210), (15, 45, 95),
               (65, 125, 195), (25, 60, 120), (50, 110, 175)],
    "MIDEAST": [(200, 120, 40), (170, 95, 25), (220, 150, 70)],
    "AFRICA": [(40, 130, 70), (25, 100, 55), (70, 160, 95)],
    "OCEANIA": [(30, 140, 140), (20, 110, 110)],
    "WORLD": [(110, 110, 110), (80, 80, 80), (140, 140, 140)],
}


# ---- small helpers ----
def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap; if it still overflows, trim the last line
    with an ellipsis (callers reject any ellipsis via assert)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last + "…" if last else "…"
    return lines


def wrap_first_narrow(draw, text, fnt, first_w, rest_w, max_lines):
    """Like wrap, but the first line is narrower (a bold "N. City: "
    head sits on it)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        limit = first_w if not lines else rest_w
        if draw.textlength(trial, font=fnt) <= limit:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > rest_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last + "…" if last else "…"
    return lines


def cover_crop(img, box_w, box_h, focus_y=0.5):
    """Scale the picture so it covers the box completely, then cut a
    window centred on focus_y (fraction of the scaled height) and
    centred horizontally. Only sky/ground at the edges gets cut; the
    main subject stays in the middle of the box."""
    iw, ih = img.size
    scale = max(box_w / iw, box_h / ih)
    nw = max(1, int(iw * scale + 0.5))
    nh = max(1, int(ih * scale + 0.5))
    big = img.resize((nw, nh), Image.LANCZOS)
    left = max(0, min((nw - box_w) // 2, nw - box_w))
    top = int(focus_y * nh - box_h / 2 + 0.5)
    top = max(0, min(top, nh - box_h))
    return big.crop((left, top, left + box_w, top + box_h))


def paint_strip(draw, x, y, w, h, text, bg, size):
    """A coloured band on the top edge of a picture: "N · CITY · TOPIC"
    in bold white. The font shrinks until the text fits."""
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    fnt = None
    for s in (size, size - 1, size - 2):
        trial = load(SANS_B, s)
        if draw.textlength(text, font=trial) <= w - 8:
            fnt = trial
            break
    if fnt is None:
        fnt = load(SANS_B, size - 2)
    draw.text((x + 4, y + h / 2), text, font=fnt, fill=WHITE, anchor="lm")


def assign_strips(grid):
    """grid: rows of regions. Pick a strip colour per cell so every
    cell differs from its left and upper neighbour (greedy)."""
    colours = [[None] * len(row) for row in grid]
    for r, row in enumerate(grid):
        for c, region in enumerate(row):
            left = colours[r][c - 1] if c > 0 else None
            up = (colours[r - 1][c]
                  if r > 0 and c < len(colours[r - 1]) else None)
            pick = None
            for v in STRIP_VARIANTS[region]:
                if v != left and v != up:
                    pick = v
                    break
            colours[r][c] = pick if pick is not None else STRIP_VARIANTS[region][0]
    return colours

# ---- map ----
def project(lon, lat, mw, mh):
    """Equirectangular: lon -180..180 across (8px side padding),
    lat 75..-55 down."""
    x = 8 + (lon + 180.0) / 360.0 * (mw - 16)
    y = (75.0 - lat) / 130.0 * mh
    return (x, y)


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def build_markers():
    """Pins: one per card (its global story number, region colour) +
    a gold star for the Shenzhen summit + a numbered pin for the
    New Delhi brief. Dots: one per distinct brief place that is not
    already pinned. Returns (pins, dots)."""
    pins = []
    for _city, _t, _f, _s1, _s2, strip, region, _focus in CARDS:
        num = strip.split(" · ")[0]
        city = strip.split(" · ")[1].title()
        if city in PLACES:
            pins.append((city, num, region))
    pins.append(("Shenzhen", "star", "ASIA"))
    for i, (city, region, _text) in enumerate(BRIEFS):
        if city == "New Delhi":
            pins.append((city, str(14 + i), region))
            break
    seen = {PLACES[city] for city, _m, _r in pins}
    dots = []
    for city, region, _text in BRIEFS:
        if city in ("Global", "New Delhi") or city not in PLACES:
            continue
        if PLACES[city] in seen:
            continue
        seen.add(PLACES[city])
        dots.append((city, region))
    return pins, dots


def draw_map(mw, mh):
    """The world map filling its box edge to edge. v2: continent
    outlines 2px (the sketch's 1px outlines blurred together at this
    size), pins r 6 with 8pt numbers, dots r 3 kept 9px apart.
    Returns (image, log)."""
    pins, dots = build_markers()
    im = Image.new("RGB", (mw, mh), SEA)
    d = ImageDraw.Draw(im)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND)
        d.line(pts + [pts[0]], fill=LAND_LINE, width=2)
    f_label = load(SANS_B, 10)
    f_num = load(SANS_B, 8)
    placed = []
    for city, mark, region in pins:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, mw, mh)
        dx, dy = PIN_OFFSETS.get(city, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([(px, py), (qx, qy)], fill=NAVY, width=1)
        if mark == "star":
            d.polygon(star_points(qx, qy, 8, 3.5), fill=GOLD, outline=NAVY)
            placed.append((qx, qy, 8))
        else:
            col = REGION_COLORS[region]
            d.ellipse([qx - 6, qy - 6, qx + 6, qy + 6], fill=col,
                      outline=WHITE, width=1)
            tw = d.textlength(mark, font=f_num)
            d.text((qx - tw / 2, qy - 4), mark, font=f_num, fill=WHITE)
            placed.append((qx, qy, 6))
        if city in PIN_LABELS:
            side = PIN_LABELS[city]
            tw = d.textlength(city, font=f_label)
            if side == "r":
                tx, ty = qx + 8, qy - 5
            elif side == "l":
                tx, ty = qx - 8 - tw, qy - 5
            elif side == "a":
                tx, ty = qx - tw / 2, qy - 16
            else:
                tx, ty = qx - tw / 2, qy + 9
            d.text((tx, ty), city, font=f_label, fill=NAVY,
                   stroke_width=2, stroke_fill=PAPER)
    for i, (x1, y1, _r1) in enumerate(placed):
        for x2, y2, _r2 in placed[i + 1:]:
            assert ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 >= 12, \
                f"map pins collide: {(x1, y1)} vs {(x2, y2)}"
    placed_dots, skipped = [], []
    for city, region in dots:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, mw, mh)
        if any(((px - x) ** 2 + (py - y) ** 2) ** 0.5 < 9
               for x, y, _r in placed):
            skipped.append(city)
            continue
        d.ellipse([px - 3, py - 3, px + 3, py + 3],
                  fill=REGION_COLORS[region], outline=WHITE, width=1)
        placed.append((px, py, 3))
        placed_dots.append(city)
    log = {"pins": [m for _c, m, _r in pins],
           "dots": placed_dots, "skipped_dots": skipped}
    return im, log


# ---- page sections ----
def draw_chrome(d):
    """Top line + masthead + deck. Returns y=100."""
    d.text((12, 8), "ALL DATED 19 NOV", font=load(SANS_B, 11), fill=RED)
    d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=load(SANS_B, 11),
           fill=NAVY, anchor="ma")
    d.text((1012, 8), f"{TOTAL} STORIES", font=load(SANS_B, 11), fill=RED,
           anchor="ra")
    y_base = 72
    w1 = d.textlength("THURSDAY ", font=load(SERIF, 54))
    w2 = d.textlength("19", font=load(SERIF, 62))
    w3 = d.textlength(" NOVEMBER 2026", font=load(SERIF, 54))
    x0 = (W - (w1 + w2 + w3)) // 2
    d.text((x0, y_base), "THURSDAY ", font=load(SERIF, 54), fill=INK,
           anchor="ls")
    d.text((x0 + w1, y_base), "19", font=load(SERIF, 62), fill=RED,
           anchor="ls")
    d.text((x0 + w1 + w2, y_base), " NOVEMBER 2026", font=load(SERIF, 54),
           fill=INK, anchor="ls")
    deck = ("a three-president summit, GTA VI on sale, "
            "an $81.3bn IPO, the ICJ verdict, a storm off India")
    d.text((W // 2, 82), deck, font=load(SANS_B, 14), fill=RED, anchor="ma")
    return 100


def draw_region_bar(d, y):
    """Navy title cell + 7 region-tinted segments. Returns y + 36."""
    hgt = 36
    x0, x1 = 12, 1012
    title_w = 204
    d.rectangle([x0, y, x0 + title_w, y + hgt], fill=NAVY)
    title = f"{TOTAL} STORIES FROM 7 REGIONS"
    tw = d.textlength(title, font=load(SANS_B, 11))
    assert tw <= title_w - 16, f"region title too wide: {tw}"
    d.text((x0 + (title_w - tw) / 2, y + hgt / 2), title,
           font=load(SANS_B, 11), fill=WHITE, anchor="lm")
    seg_w = (x1 - (x0 + title_w)) / 7
    for i, (name, n) in enumerate(COUNTS):
        rc = REGION_COLORS[dict(REGION_ORDER)[name]]
        tint = tuple(int(255 * 0.88 + c * 0.12) for c in rc)
        sx = x0 + title_w + i * seg_w
        ex = sx + seg_w if i < 6 else x1
        d.rectangle([sx, y, ex, y + hgt], fill=tint)
        label, num = f"{name} ", str(n)
        gw = (d.textlength(label, font=load(SANS_B, 11)) + 2
              + d.textlength(num, font=load(SANS_B, 13)))
        assert gw <= seg_w - 6, f"region segment too wide: {name} {gw}"
        cx = sx + (ex - sx) / 2
        tx = cx - gw / 2
        d.text((tx, y + hgt / 2), label, font=load(SANS_B, 11),
               fill=NAVY, anchor="lm")
        d.text((tx + d.textlength(label, font=load(SANS_B, 11)) + 2,
                y + hgt / 2), num, font=load(SANS_B, 13), fill=NAVY,
               anchor="lm")
        if i > 0:
            d.line([(sx, y), (sx, y + hgt)], fill=rc, width=1)
    d.rectangle([x0, y, x1, y + hgt], outline=NAVY, width=2)
    return y + hgt


def draw_numbers(d, y0):
    """Six big numbers with captions, no boxes, thin region-coloured
    dividers between segments. Returns y0 + 58."""
    hgt = 58
    x = 12
    for i, (num, label, region) in enumerate(NUMBERS):
        bw = 163 if i < 5 else 165
        rc = REGION_COLORS[region]
        d.text((x + 8, y0 + 3), num, font=load(SANS_B, 22), fill=NAVY)
        clines = wrap(d, label, load(SANS_B, 11), bw - 16, 2)
        assert "…" not in "".join(clines), f"number caption cut: {label}"
        cy = y0 + 30
        for ln in clines:
            d.text((x + 8, cy), ln, font=load(SANS_B, 11), fill=INK)
            cy += 14
        if i > 0:
            d.line([(x, y0), (x, y0 + hgt)], fill=rc, width=1)
        x += bw + 4
    return y0 + hgt


def draw_hero(canvas, d, x, y, w, hero, strip_color, col):
    """One hero panel; returns its strip rect for the colour check."""
    d.rectangle([x, y, x + w, y + HERO_H], fill=CARD_BG,
                outline=CARD_LINE, width=1)
    img = Image.open(os.path.join(ASSETS, hero["file"])).convert("RGB")
    canvas.paste(cover_crop(img, w - 2, HERO_IMG, hero["focus"]),
                 (x + 1, y + 1))
    paint_strip(d, x + 1, y + 1, w - 2, 12, hero["strip"], strip_color, 11)
    ty = y + 1 + HERO_IMG + 6
    for ln in wrap(d, hero["headline"], load(SANS_B, HERO_HEAD), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS_B, HERO_HEAD), fill=INK)
        ty += HERO_HEAD + 4
    ty += 2
    for ln in wrap(d, hero["deck"], load(SANS, HERO_DECK), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS, HERO_DECK), fill=MUTED)
        ty += HERO_DECK + 4
    return (x + 1, y + 1, w - 2, 12, strip_color, hero["strip"], 0, col)


def draw_card(canvas, d, x, y, w, card, strip_color, row, col):
    """One story card; returns its strip rect for the colour check."""
    city, title, fname, s1, s2, strip, _region, focus = card
    d.rectangle([x, y, x + w, y + CARD_H], fill=CARD_BG,
                outline=CARD_LINE, width=1)
    img = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
    canvas.paste(cover_crop(img, w - 2, CARD_IMG, focus), (x + 1, y + 1))
    paint_strip(d, x + 1, y + 1, w - 2, 10, strip, strip_color, 10)
    ty = y + 1 + CARD_IMG + 6
    for ln in wrap(d, title, load(SANS_B, CARD_HEAD), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS_B, CARD_HEAD), fill=INK)
        ty += CARD_HEAD + 4
    ty += 1
    summ = s1 + " " + s2
    for ln in wrap(d, summ, load(SANS, CARD_SUM), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS, CARD_SUM), fill=MUTED)
        ty += CARD_SUM + 4
    return (x + 1, y + 1, w - 2, 10, strip_color, strip, row, col)


def draw_briefs(d, x, y, w, total_h):
    """MORE STORIES: 3 even columns of 6 briefs each, "N. City: text…"
    with the number red bold and the city navy bold. Returns y+total_h."""
    d.text((x, y), "MORE STORIES FROM 19 NOVEMBER",
           font=load(SANS_B, 16), fill=NAVY)
    col_w = (w - 2 * 12) // 3
    measured = []
    for i, (city, region, text) in enumerate(BRIEFS):
        num_txt = f"{14 + i}. "
        city_txt = f"{city}: "
        head_w = (d.textlength(num_txt, font=load(SANS_B, BRIEF_SIZE))
                  + d.textlength(city_txt, font=load(SANS_B, BRIEF_SIZE)))
        lines = wrap_first_narrow(d, text, load(SANS, BRIEF_SIZE),
                                  col_w - 12 - head_w, col_w - 12, 4)
        assert "…" not in "".join(lines), f"brief cut: {city} {lines}"
        measured.append((city, region, num_txt, city_txt, head_w, lines))
    groups = [list(range(i * 6, (i + 1) * 6)) for i in range(3)]
    avail = total_h - 24
    for ci, idxs in enumerate(groups):
        chunk = [measured[i] for i in idxs]
        bx = x + ci * (col_w + 12)
        content = sum(len(lines) * BRIEF_LH
                      for (_, _, _, _, _, lines) in chunk)
        slack = avail - content
        assert slack >= 0, f"briefs do not fit: {content} > {avail}"
        n = len(chunk)
        base, rem = divmod(slack, n) if n else (0, 0)
        leads = [base + (1 if s < rem else 0) for s in range(n)]
        by = y + 24
        for si, (city, region, num_txt, city_txt, head_w, lines) in \
                enumerate(chunk):
            by += leads[si]
            ch = len(lines) * BRIEF_LH
            rc = REGION_COLORS[region]
            d.rectangle([bx, by + 2, bx + 5, by + ch - 2], fill=rc)
            tx = bx + 10
            d.text((tx, by), num_txt, font=load(SANS_B, BRIEF_SIZE),
                   fill=RED)
            d.text((tx + d.textlength(num_txt,
                                       font=load(SANS_B, BRIEF_SIZE)), by),
                   city_txt, font=load(SANS_B, BRIEF_SIZE), fill=NAVY)
            ty = by
            for li, ln in enumerate(lines):
                lx = tx + head_w if li == 0 else tx
                d.text((lx, ty), ln, font=load(SANS, BRIEF_SIZE), fill=INK)
                ty += BRIEF_LH
            by += ch
    return y + total_h


def draw_datecheck(d, y):
    """DATE CHECK bar + source lines under it."""
    d.rectangle([12, y, 1012, y + 24], fill=NAVY)
    d.rectangle([12, y, 120, y + 24], fill=GOLD)
    d.text((66, y + 12), "DATE CHECK", font=load(SANS_B, 11), fill=NAVY,
           anchor="mm")
    d.text((130, y + 12), DATECHECK_MSG, font=load(SANS, 12), fill=WHITE,
           anchor="lm")
    d.text((W // 2, y + 32), SOURCES_LINE, font=load(SANS, 10), fill=MUTED,
           anchor="ma")
    d.text((W // 2, y + 44), "Disputed claims are attributed, not stated as fact.",
           font=load(SANS, 10), fill=MUTED, anchor="ma")


def check_strips(canvas, rects):
    """Every strip's background must be exactly its assigned colour
    (sampled in the strip's left column, clear of the text), and no
    strip may share a colour with an orthogonal neighbour."""
    px = canvas.load()
    grid = {}
    bad = []
    for (x, y, w, h, exp, label, r, c) in rects:
        got = set()
        for i in range(20):
            sy = y + 1 + int((h - 2) * i / 19)
            got.add(px[x + 1, sy])
        if got != {exp}:
            bad.append(f"{label}: strip colour {got} != {exp}")
        grid[(r, c)] = exp
    for (r, c), col in grid.items():
        if (r, c - 1) in grid and grid[(r, c - 1)] == col:
            bad.append(f"same as left neighbour: row {r} col {c}")
        if (r - 1, c) in grid and grid[(r - 1, c)] == col:
            bad.append(f"same as upper neighbour: row {r} col {c}")
    return (not bad, bad)


# ---- build ----
def build():
    counts = {k: 0 for _n, k in REGION_ORDER}
    for hh in HEROES:
        counts[hh["region"]] += 1
    for cc in CARDS:
        counts[cc[6]] += 1
    for bb in BRIEFS:
        counts[bb[1]] += 1
    assert sum(counts.values()) == TOTAL, counts
    assert [(n, counts[k]) for n, k in REGION_ORDER] == COUNTS, counts

    grid = [[h["region"] for h in HEROES]]
    for r in range(2):
        grid.append([CARDS[r * 5 + c][6] for c in range(5)])
    scol = assign_strips(grid)
    scol[0] = HERO_STRIPS
    assert scol[0][2] != scol[1][2], "hero 3 strip equals the card below it"

    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    y = draw_chrome(d)
    y = draw_region_bar(d, y) + GAP
    y = draw_numbers(d, y)

    hw = (1000 - 2 * 6) // 3
    for hero in HEROES:
        assert "…" not in "".join(wrap(
            d, hero["headline"], load(SANS_B, HERO_HEAD), hw - 16, 2)), \
            hero["headline"]
        assert "…" not in "".join(wrap(
            d, hero["deck"], load(SANS, HERO_DECK), hw - 16, 2)), hero["deck"]
    rects = []
    hy = y
    for i, hero in enumerate(HEROES):
        hx = 12 + i * (hw + 6)
        rects.append(draw_hero(canvas, d, hx, hy, hw, hero, scol[0][i], i))
    y = hy + HERO_H + GAP

    cw = (1000 - 4 * 6) // 5
    for r in range(2):
        for c in range(5):
            card = CARDS[r * 5 + c]
            assert "…" not in "".join(wrap(
                d, card[1], load(SANS_B, CARD_HEAD), cw - 16, 2)), card[1]
            assert "…" not in "".join(wrap(
                d, card[3] + " " + card[4], load(SANS, CARD_SUM),
                cw - 16, 2)), card[1]
            cx = 12 + c * (cw + 6)
            rects.append(draw_card(canvas, d, cx, y, cw, card,
                                   scol[r + 1][c], r + 1, c))
        y += CARD_H + GAP

    bottom_y = y
    bottom_h = 964 - bottom_y
    map_top = bottom_y + 24
    map_h = bottom_h - 24
    map_im, mlog = draw_map(MAP_W, map_h)
    canvas.paste(map_im, (12, map_top))
    d.rectangle([12, map_top, 12 + MAP_W, bottom_y + bottom_h],
                outline=CARD_LINE, width=1)
    bx = 12 + MAP_W + 10
    bw = 1012 - bx
    used = draw_briefs(d, bx, bottom_y, bw, bottom_h)
    assert used == bottom_y + bottom_h, (used, bottom_y + bottom_h)
    d.text((12, bottom_y), "WHERE IT HAPPENED", font=load(SANS_B, 14),
           fill=NAVY)

    draw_datecheck(d, 968)
    ok, bad = check_strips(canvas, rects)
    assert canvas.size == (1024, 1024)
    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    assert len(data) <= 1048576, f"entry.png {len(data)} bytes > 1 MiB"
    assert ok, bad
    print(f"wrote {out} {len(data)} bytes sha256 "
          f"{hashlib.sha256(data).hexdigest()}")
    print(f"  {TOTAL} stories; strip check: 0 violations")
    print(f"  map pins {mlog['pins']} dots {mlog['dots']} "
          f"skipped_dots {mlog['skipped_dots']}")
    return out


if __name__ == "__main__":
    build()
