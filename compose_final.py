#!/usr/bin/env python3
"""Final compositor for news-image-20261119 — Opsi A (re-plan fresh).

Draws the final entry image: 39 stories from Thursday 19 November
2026 in one 1024x1024 page — 3 hero pictures, 15 cards with
AI illustrations, a world map with numbered pins and dots, 21 briefs,
a merged big-numbers strip, a prominent DATE CHECK band and a clean
footer (sources + one attribution line only).

Layout data (positions, sizes, story texts) follows the approved
15-card beta sketch Kevin chose: masthead with the red "19",
region bar, merged numbers strip, heroes as cards, 5x3 card grid,
map + briefs section, DATE CHECK, footer. What changed from the beta
(re-plan §1-§2): 4 new stories in (South Africa, Uganda, Senegal,
COP31), 4 one-line market tickers out, Taiwan/Finland/Wellington
demoted from cards to briefs, sequential card numbering, individual
strip colours (Kevin's neighbour rule), clean footer, AI pictures
for every card instead of Pillow mini-illustrations.

Deterministic: no network, no clock, no randomness. Two runs write
byte-identical PNGs. Run: python3 compose_final.py (writes entry.png
next to this file).
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(HERE, "assets")

# Page palette (approved sketch).
PAPER = (246, 241, 231)
INK = (24, 28, 36)
NAVY = (15, 36, 64)
RED = (178, 44, 36)
GOLD = (217, 164, 65)
MUTED = (92, 96, 104)
WHITE = (255, 255, 255)
SEA = (198, 220, 236)
LAND = (210, 188, 140)
LAND_LINE = (168, 148, 108)
CARD_BG = (250, 247, 240)
CARD_LINE = (205, 200, 185)

# One colour per region (base colours: strips in the sketch, map pins,
# brief side strips, big-number tints).
REGION_RGB = {
    "AMERICAS": (178, 44, 36),
    "EUROPE": (40, 90, 160),
    "MIDEAST": (200, 120, 40),
    "ASIA": (130, 80, 160),
    "AFRICA": (40, 130, 70),
    "OCEANIA": (30, 140, 140),
    "WORLD": (110, 110, 110),
}
REGION_BAR_ORDER = [
    ("EUROPE", "EUROPE"), ("THE AMERICAS", "AMERICAS"),
    ("ASIA-PACIFIC", "ASIA"), ("MIDEAST", "MIDEAST"),
    ("AFRICA", "AFRICA"), ("OCEANIA", "OCEANIA"), ("WORLD", "WORLD"),
]

# Individual strip colours per picture (re-plan §2.2): variants inside
# a region's colour family so neighbours never share a top colour
# (Kevin 19:01 WIB). Map pins and brief strips keep the base colours.
STRIP_RGB = {
    1: (130, 80, 160),    # hero 1: ASIA purple
    2: (178, 44, 36),     # hero 2: AMERICAS red
    3: (122, 28, 28),     # hero 3: dark red (beta)
    4: (200, 120, 40),    # card 4: MIDEAST orange
    5: (140, 30, 30),     # card 5: dark red (differs from hero 2 above)
    6: (40, 90, 160),     # card 6: EUROPE blue
    7: (90, 150, 210),    # card 7: steel blue
    8: (15, 45, 95),      # card 8: dark navy
    9: (65, 125, 195),    # card 9: blue
    10: (25, 60, 120),    # card 10: blue
    11: (50, 110, 175),   # card 11: blue (thinnest pair vs card 6)
    12: (130, 80, 160),   # card 12: ASIA purple
    13: (40, 130, 70),    # card 13: AFRICA green
    14: (200, 120, 40),   # card 14: MIDEAST orange
    15: (110, 110, 110),  # card 15: WORLD grey
    16: (200, 120, 40),   # card 16: MIDEAST orange
    17: (40, 130, 70),    # card 17: AFRICA green
    18: (200, 120, 40),   # card 18: MIDEAST orange
}

# Heroes (1-3): AI pictures from v1.1, reused (our own assets).
HEROES = [
    {
        "file": "media-generation-hero-summit-0-2facf046-c366-4c54-811a-378f151baf31.png",
        "headline": "Trump, Xi and Putin meet in Shenzhen",
        "deck": "Trade truce and nuclear arms top the agenda as the three leaders meet in Shenzhen",
        "strip": "1 · SHENZHEN · SUMMIT",
        "region": "ASIA",
    },
    {
        "file": "media-generation-hero-gtavi-0-2ba192a8-4751-42fd-bb85-541410d0920c.png",
        "headline": "GTA VI launches worldwide",
        "deck": "Gamers enter Vice City as the launch begins on PlayStation 5 and Xbox",
        "strip": "2 · NEW YORK · GAMES",
        "region": "AMERICAS",
    },
    {
        "file": "media-generation-hero-ipo-0-8cbb9db1-f691-408f-ab20-746c58a7d930.png",
        "headline": "Anthropic's $81.3bn IPO — a record",
        "deck": "Priced at $83 a share, the biggest IPO ever; markets rise ahead of the debut",
        "strip": "3 · NASDAQ · MARKETS",
        "region": "AMERICAS",
    },
]

# Cards (4-18, sequential): (title, picture file, summary line 1,
# summary line 2, strip, region). Card 4 reuses the v1.1 Gaza AI
# picture; cards 5-18 use AI pictures generated in this build session
# (same flat editorial style as the heroes, no text in the pictures).
CARDS = [
    ("Israeli push past Gaza ceasefire line",
     "media-generation-hero-gaza-0-d883abe3-a658-4e15-8940-7187b06791d4.png",
     "Rare ground op beyond Yellow Line",
     "Israeli troops cross the ceasefire line",
     "4 · GAZA · CEASEFIRE LINE", "MIDEAST"),
    ("US approves $1.6bn Ukraine aid package",
     "media-generation-card05-capitol-0-96ed6c35-65e2-4661-8d50-f315298cacda.png",
     "Package approved on Thursday",
     "$1.6bn for Ukraine's defence",
     "5 · WASHINGTON · UKRAINE AID", "AMERICAS"),
    ("Zelensky: US blocking missile deliveries",
     "media-generation-card06-kyiv-0-fd22b23a-9957-4e80-a778-279c51f91f62.png",
     "Kyiv accuses Washington",
     "Missile deliveries held back",
     "6 · KYIV · MISSILE DELIVERIES", "EUROPE"),
    ("Estonia to shut Russia border",
     "media-generation-card07-estonia-forest-0-877554df-8f1e-4de1-b4bf-3cb6eea5c4ca.png",
     "Crossings close from December",
     "Border with Russia to shut",
     "7 · ESTONIA · RUSSIA BORDER", "EUROPE"),
    ("Prague mass protest for media independence",
     "media-generation-card08-prague-0-ba36692a-2638-4a3d-83b3-1d854b313031.png",
     "Crowds demand a free press",
     "Hundreds of thousands protest",
     "8 · PRAGUE · MEDIA PROTEST", "EUROPE"),
    ("Spain hit by nationwide general strike",
     "media-generation-card09-spain-port-0-42734762-2a83-483d-b9ab-ae6340841638.png",
     "Ports and factories disrupted",
     "General strike hits the country",
     "9 · SPAIN · GENERAL STRIKE", "EUROPE"),
    ("Crimean Bridge attacked again",
     "media-generation-card10-kerch-bridge-0-4c8ad532-9000-40b1-ac10-a413b50ddd24.png",
     "Traffic suspended, says official",
     "Russian official confirms the attack",
     "10 · KERCH · BRIDGE ATTACK", "EUROPE"),
    ("ICJ rules on Myanmar genocide case",
     "media-generation-card11-hague-court-0-b2078933-fd30-4694-8ba1-02ad9705ee47.png",
     "Verdict due today in The Hague",
     "Rohingya case at the UN court",
     "11 · THE HAGUE · GENOCIDE CASE", "EUROPE"),
    ("Cyclone Akvan nears India's coast",
     "media-generation-card12-puri-cyclone-0-52d14767-9a88-4a29-a7a0-1327900641af.png",
     "Red alerts out; schools shut",
     "Machilipatnam to Puri in its path",
     "12 · PURI · CYCLONE AKVAN", "ASIA"),
    ("South Africa holds rates as rand slides",
     "media-generation-card13-johannesburg-bank-0-08c25c4a-8c11-44e1-9878-66c46704c00c.png",
     "SARB holds repo rate at 7.25%",
     "Rand falls to lowest of the year",
     "13 · JOHANNESBURG · RATE DECISION", "AFRICA"),
    ("Houthi rocket kills 53 soldiers in Yemen",
     "media-generation-card14-yemen-desert-0-66920018-6869-4d6f-96c7-26ec1c633dca.png",
     "Strike reported on Thursday",
     "53 soldiers killed in Yemen",
     "14 · YEMEN · ROCKET STRIKE", "MIDEAST"),
    ("Van Gogh sells for record $190.4m",
     "media-generation-card15-starry-sky-0-879a0906-435a-4e94-b61c-3007a168ba76.png",
     "Auction record for the artist",
     "Painting sells for $190.4m",
     "15 · AUCTION · VAN GOGH RECORD", "WORLD"),
    ("Saudi: danger has passed in south",
     "media-generation-card16-saudi-dawn-0-82524d16-3724-49d5-8f27-8c6f83174e1d.png",
     "Danger passed, civil defence says",
     "Alerts lifted in three southern cities",
     "16 · SAUDI ARABIA · ALL CLEAR", "MIDEAST"),
    ("Two presidents open Uganda car plant",
     "media-generation-card17-mpigi-plant-0-bd2080ea-9a53-4095-93ca-afbfb6024f4d.png",
     "Museveni and Samia launch plant",
     "Double Q–Sinotruk assembly in Mpigi",
     "17 · MPIGI · CAR PLANT", "AFRICA"),
    ("COP31 draft drops fossil-fuel language",
     "media-generation-card18-antalya-draft-0-de39f8d5-f869-44c3-af29-3bee11d2e173.png",
     "New draft omits fossil phase-out",
     "Antalya text admits 1.5°C may pass",
     "18 · ANTALYA · COP31 DRAFT", "MIDEAST"),
]

# Briefs (19-39, continuing the numbering): (city, region, text).
# Two sentences where two verified facts exist; the city is not
# repeated inside the text. Region = the story's place, except 27/28
# WORLD (global tech) and 29 EUROPE (newsmaker Putin/Russia).
BRIEFS = [
    ("Berlin", "EUROPE", "The Coalition of the Willing meets. Witkoff and Kushner attend."),
    ("Saada", "MIDEAST", "The Saudi coalition intercepts a Houthi missile. The launcher is destroyed."),
    ("Tokyo", "ASIA", "India and Japan hold 2+2 defence talks. The ministers meet in the capital."),
    ("Hormuz", "MIDEAST", "A tanker is hit by a projectile. Oil steadies after the strike."),
    ("MAIB", "WORLD", "The Bayesian had a hidden wind weakness. Winds of 80 mph capsized her in seconds."),
    ("Shenzhen", "ASIA", "Trump mentions ex-Nvidia boss Huang 'briefly' in Xi talks. The talks are at the APEC summit."),
    ("Australia", "OCEANIA", "The jobless rate jumps to 4.9%. It is the highest since 2021."),
    ("London", "EUROPE", "The UK leasehold Bill enters Parliament. Rents are capped at £250."),
    ("Washington", "WORLD", "US senators warn AI cyber threats are outpacing defences."),
    ("US", "WORLD", "Microsoft is in talks to sell AI services to ByteDance."),
    ("Shenzhen", "EUROPE", "Japan PM Takaichi holds talks with Putin. Both leaders are at the APEC summit."),
    ("New Delhi", "ASIA", "Congress targets the Modi government over inflation."),
    ("Kuala Lumpur", "ASIA", "UNHCR halts refugee registration in Malaysia."),
    ("Global", "WORLD", "Bitcoin slips below $63,000. It is down 2.7%."),
    ("Tokyo", "ASIA", "Japan machinery orders dip 0.3%. The figures are for September."),
    ("Brussels", "EUROPE", "The EU delays methane rules by two years."),
    ("Tokyo", "ASIA", "Stocks rise. The Anthropic IPO lifts the AI mood."),
    ("Taiwan", "ASIA", "Taiwan drafts a transnational repression law. The bill targets coercion abroad."),
    ("Finland", "EUROPE", "The first nuclear waste store is approved. It is the world's first permanent repository."),
    ("Wellington", "OCEANIA", "Bumrah strikes twice at lunch. The 1st Test is at Basin Reserve."),
    ("Dakar", "AFRICA", "Senegal holds Armed Forces Day in Dakar. President Faye leads the ceremony."),
]

# Six big numbers for the merged strip — all verified from our own
# stories (never rank 1's unverified 15.9m / 200,000). Region per
# number = its story's strip region (soft 12% tint, number bold NAVY).
BIG_NUMBERS = [
    ("$81.3bn", "Anthropic IPO — largest ever", "AMERICAS"),
    ("$190.4m", "Van Gogh sells — artist record", "WORLD"),
    ("$1.6bn", "US aid package for Ukraine", "AMERICAS"),
    ("53", "soldiers killed in Yemen strike", "MIDEAST"),
    ("4.9%", "Australia jobless — highest since 2021", "OCEANIA"),
    ("$63,000", "Bitcoin slips below, down 2.7%", "WORLD"),
]


# ---- map data ----
# Places keyed by the city label in a card strip or a brief. Country
# labels resolve to their capital (Spain = Madrid, Estonia = Tallinn,
# UK = London, US = Washington, China = Beijing, Australia =
# Canberra). "Global" stories have no place and get no marker.
PLACES = {
    "Gaza": (34.4, 31.4), "Washington": (-77.0, 38.9),
    "Kyiv": (30.5, 50.4), "Estonia": (24.7, 59.4),
    "Prague": (14.4, 50.1), "Spain": (-3.7, 40.4),
    "Kerch": (36.5, 45.3), "The Hague": (4.3, 52.1),
    "Puri": (85.8, 19.8), "Taiwan": (121.0, 25.0),
    "Yemen": (44.2, 15.3), "Saudi Arabia": (46.7, 24.6),
    "Finland": (24.9, 60.2), "Wellington": (174.8, -41.3),
    "Berlin": (13.4, 52.5), "Saada": (43.8, 16.9),
    "Tokyo": (139.7, 35.7), "Hormuz": (56.3, 26.6),
    "Shenzhen": (114.1, 22.5), "New Delhi": (77.2, 28.6),
    "London": (-0.1, 51.5), "UK": (-0.1, 51.5),
    "US": (-77.0, 38.9), "China": (116.4, 39.9),
    "Australia": (149.1, -35.3), "Kuala Lumpur": (101.7, 3.1),
    "Beijing": (116.4, 39.9), "Brussels": (4.4, 50.8),
    # New in the final build (re-plan §2.3):
    "Dakar": (-17.4, 14.7), "Mpigi": (32.3, 0.2),
    "Johannesburg": (-28.0, -26.2), "Antalya": (30.7, 36.9),
}
# Hand-tuned offsets (dx, dy in px) for pins whose true positions
# collide on the 300px map. A thin leader line joins the pin to its
# true place. Kyiv (+10,-6) and Antalya (0,-12) are new: without them
# Antalya sits 7px from the Gaza pin and 4px from the Kyiv pin.
PIN_OFFSETS = {
    "Finland": (0, -12), "Prague": (0, 14), "The Hague": (-14, 0),
    "Kerch": (12, 0), "Saada": (0, 14), "Hormuz": (0, -12),
    "Taiwan": (12, 0), "Kyiv": (10, -6), "Antalya": (0, -12),
}
# Pins keep their city label only where the label cannot collide with
# another marker (isolated places). Rank 1 labels no pins at all.
PIN_LABELS = {"Gaza": "l", "Shenzhen": "b"}

# Simplified continents as (lon, lat) polygons, equirectangular.
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
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (3, 37), (10, 37), (15, 32),
     (22, 33), (30, 31), (34, 28), (37, 22), (43, 12), (48, 11), (51, 12),
     (46, 2), (41, -8), (38, -18), (33, -26), (28, -33), (20, -35),
     (16, -29), (14, -22), (12, -17), (9, -2), (9, 4), (0, 6), (-8, 5),
     (-13, 8), (-17, 15)],
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

# ---- fonts ----
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_capped(draw, text, fnt, max_w, max_lines):
    """wrap_text capped at max_lines; the last line gets an ellipsis."""
    lines = wrap_text(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last + "…" if last else "…"
    return lines


def one_line(draw, text, fnt, max_w):
    """Truncate to a single line with an ellipsis if it does not fit."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    out = ""
    for word in text.split():
        trial = (out + " " + word).strip()
        if draw.textlength(trial + "…", font=fnt) <= max_w:
            out = trial
        else:
            break
    return out + "…" if out else "…"


def cover_crop(img, target_w, target_h):
    """Scale the image to cover the target box, then centre-crop it."""
    iw, ih = img.size
    scale = max(target_w / iw, target_h / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - target_w) // 2
    y = (nh - target_h) // 2
    return img.crop((x, y, x + target_w, y + target_h))


def vgrad(draw, x, y, w, h, top, bottom):
    """Vertical gradient band, one horizontal line per row."""
    for i in range(h):
        t = i / max(h - 1, 1)
        col = tuple(int(top[k] + (bottom[k] - top[k]) * t)
                     for k in range(3))
        draw.line([(x, y + i), (x + w - 1, y + i)], fill=col)


def draw_strip(draw, x, y, w, h, text, bg, size):
    """Coloured band on the TOP edge of a picture: "N · CITY · TOPIC".

    Drawn on the canvas after the picture is pasted, so it sits on top
    of the picture and can never bleed into text below it. The font
    shrinks until the text fits.
    """
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    fnt = None
    for s in (size, size - 1, size - 2):
        trial = load_font(SANS_B, s)
        if draw.textlength(text, font=trial) <= w - 8:
            fnt = trial
            break
    if fnt is None:
        fnt = load_font(SANS_B, max(size - 2, 6))
    draw.text((x + 4, y + h // 2), text, font=fnt, fill=WHITE, anchor="lm")


def split_even(items, n):
    """Split a list into n columns as evenly as possible (sizes differ
    by at most 1; the first columns get the extra item)."""
    base, extra = divmod(len(items), n)
    cols, i = [], 0
    for c in range(n):
        k = base + (1 if c < extra else 0)
        cols.append(items[i:i + k])
        i += k
    return cols


# ---- region counts + map markers ----
def region_counts():
    """Count stories per region from the final lists. The bar above
    the heroes and the map legend are both drawn from this list, so
    they always agree."""
    counts = {key: 0 for _name, key in REGION_BAR_ORDER}
    for hero in HEROES:
        counts[hero["region"]] += 1
    for _t, _f, _s1, _s2, _strip, region in CARDS:
        counts[region] += 1
    for _city, region, _text in BRIEFS:
        counts[region] += 1
    total = sum(counts.values())
    assert total == 39, total
    expected = [("EUROPE", 11), ("THE AMERICAS", 3), ("ASIA-PACIFIC", 9),
                ("MIDEAST", 6), ("AFRICA", 3), ("OCEANIA", 2), ("WORLD", 5)]
    got = [(name, counts[key]) for name, key in REGION_BAR_ORDER]
    assert got == expected, got
    return got, total


def build_markers():
    """Pins + dots for the map, derived from the final story lists.

    Pins: every CARD story with a place in PLACES (mark = its global
    story number from the strip, colour = its region) + the gold star
    for the Shenzhen summit (hero 1) + a numbered pin for the New
    Delhi brief. Dots: one per DISTINCT brief place (a place already
    pinned gets no dot). Returns (pins, dots): pins are
    (city, mark, region), dots are (city, region).
    """
    pins = []
    for _t, _f, _s1, _s2, strip, region in CARDS:
        num = strip.split(" · ")[0]
        city = strip.split(" · ")[1].title()
        if city in PLACES:
            pins.append((city, num, region))
    pins.append(("Shenzhen", "star", "ASIA"))
    first_brief = 19
    for i, (city, region, _text) in enumerate(BRIEFS):
        if city == "New Delhi":
            pins.append((city, str(first_brief + i), region))
            break
    seen_coords = {PLACES[city] for city, _m, _r in pins}
    dots = []
    for city, region, _text in BRIEFS:
        if city in ("Global", "New Delhi") or city not in PLACES:
            continue
        if PLACES[city] in seen_coords:
            continue
        seen_coords.add(PLACES[city])
        dots.append((city, region))
    return pins, dots


def project(lon, lat, mx, my, mw, mh):
    """Equirectangular projection with 8px horizontal padding inside
    the box, so pins near the edge (Wellington) stay fully inside."""
    x = mx + 8 + (lon + 180.0) / 360.0 * (mw - 16)
    y = my + (75.0 - lat) / 130.0 * mh
    return (x, y)


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def render_map_box(mw, mh, region_counts):
    """The whole map box, drawn inside its own image so nothing can
    bleed past the border: map 156px on top, one key line, then the
    region counts in 2 lines (the SAME numbers as the bar above the
    heroes). Returns (image, log): log lists placed pins/dots and
    skipped dots (skipped = would collide, never drawn on top)."""
    pins, dots = build_markers()
    im = Image.new("RGB", (mw, mh), CARD_BG)
    d = ImageDraw.Draw(im)
    map_h = 156
    mtmp = Image.new("RGB", (mw, map_h), SEA)
    md = ImageDraw.Draw(mtmp)
    for poly in CONTINENTS:
        pts = [project(lon, lat, 0, 0, mw, map_h) for lon, lat in poly]
        md.polygon(pts, fill=LAND, outline=LAND_LINE)
    f_pin_label = load_font(SANS_B, 10)
    f_pin_num = load_font(SANS_B, 7)
    placed = []
    for city, mark, region in pins:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, 0, 0, mw, map_h)
        dx, dy = PIN_OFFSETS.get(city, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            md.line([(px, py), (qx, qy)], fill=NAVY, width=1)
        if mark == "star":
            md.polygon(star_points(qx, qy, 8, 3.5), fill=GOLD, outline=NAVY)
            placed.append((qx, qy, 8))
        else:
            col = REGION_RGB[region]
            md.ellipse([qx - 5.5, qy - 5.5, qx + 5.5, qy + 5.5],
                       fill=col, outline=WHITE, width=1)
            tw = md.textlength(mark, font=f_pin_num)
            md.text((qx - tw / 2, qy - 4), mark, font=f_pin_num, fill=WHITE)
            placed.append((qx, qy, 5.5))
        if city in PIN_LABELS:
            side = PIN_LABELS[city]
            tw = md.textlength(city, font=f_pin_label)
            if side == "r":
                tx, ty = qx + 8, qy - 5
            elif side == "l":
                tx, ty = qx - 8 - tw, qy - 5
            elif side == "a":
                tx, ty = qx - tw / 2, qy - 16
            else:  # "b"
                tx, ty = qx - tw / 2, qy + 9
            md.text((tx, ty), city, font=f_pin_label, fill=NAVY,
                    stroke_width=2, stroke_fill=PAPER)
    for i, (x1, y1, _r1) in enumerate(placed):
        for x2, y2, _r2 in placed[i + 1:]:
            assert ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 >= 10, \
                f"map pins collide: {(x1, y1)} vs {(x2, y2)}"
    placed_dots, skipped_dots = [], []
    for city, region in dots:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, 0, 0, mw, map_h)
        if any(((px - x) ** 2 + (py - y) ** 2) ** 0.5 < 8
               for x, y, _r in placed):
            skipped_dots.append(city)
            continue
        md.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                   fill=REGION_RGB[region], outline=WHITE, width=1)
        placed.append((px, py, 2.5))
        placed_dots.append(city)
    im.paste(mtmp, (0, 0))
    f_key = load_font(SANS_B, 8)
    ky = map_h + 4
    d.text((6, ky), "NUMBERED PINS = CARDS · DOTS = BRIEFS · ★ = SUMMIT",
           font=f_key, fill=NAVY)
    f_rc = load_font(SANS_B, 8)
    reg_key = {"EUROPE": "EUROPE", "THE AMERICAS": "AMERICAS",
               "ASIA-PACIFIC": "ASIA", "MIDEAST": "MIDEAST",
               "AFRICA": "AFRICA", "OCEANIA": "OCEANIA", "WORLD": "WORLD"}
    lines, cur, cur_w = [], [], 0.0
    for name, n in region_counts:
        w = 8 + d.textlength(f"{name} {n}", font=f_rc) + 8
        if cur and cur_w + w > mw - 12:
            lines.append(cur)
            cur, cur_w = [(name, n)], w
        else:
            cur.append((name, n))
            cur_w += w
    if cur:
        lines.append(cur)
    ly = ky + 13
    for line in lines[:2]:
        x = 6
        for name, n in line:
            d.ellipse([x, ly + 2, x + 6, ly + 8],
                      fill=REGION_RGB[reg_key[name]])
            d.text((x + 8, ly), f"{name} {n}", font=f_rc, fill=NAVY)
            x += 8 + int(d.textlength(f"{name} {n}", font=f_rc)) + 8
        ly += 12
    log = {"pins": [m for _c, m, _r in pins],
           "dots": placed_dots, "skipped_dots": skipped_dots}
    return im, log


# ---- brief text layout ----
def brief_lines(draw, city, text, width):
    """Wrap one brief's full text to the brief width (8pt). The first
    line starts with "CITY: " in bold; wrap counts the whole line
    INCLUDING the bold prefix, so the first line is measured honestly.
    Returns the wrapped lines (prefix included in line 0)."""
    f = load_font(SANS, 8)
    pref = f"{city}: "
    w_pref = draw.textlength(pref, font=load_font(SANS_B, 8))
    words, lines, cur, cur_w = text.split(), [], "", w_pref
    for w in words:
        ww = draw.textlength((" " if cur else "") + w, font=f)
        if cur and cur_w + ww > width:
            lines.append(pref + cur if not lines else cur)
            cur, cur_w = w, draw.textlength(w, font=f)
        else:
            cur = (cur + " " + w) if cur else w
            cur_w += ww
    if cur:
        lines.append(pref + cur if not lines else cur)
    return lines


# ---- page render ----
def render_page():
    counts, total = region_counts()
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(canvas)

    # Top strip (16px inset so the corner texts are never clipped).
    f_top = load_font(SANS_B, 13)
    f_top_c = load_font(SANS_B, 15)
    d.text((16, 8), "ALL DATED 19 NOV", font=f_top, fill=RED)
    kick = "  ".join(" ".join(w) for w in "THE WORLD IN ONE DAY".split())
    d.text((PAGE_W // 2, 7), kick, font=f_top_c, fill=NAVY, anchor="ma")
    d.text((PAGE_W - 16, 8), f"{total} STORIES", font=f_top, fill=RED,
           anchor="ra")

    # Masthead: the date is the largest text on the page. The red "19"
    # is 8pt bigger; all three segments share one baseline so the "19"
    # extends higher instead of floating lower.
    f_size = 52
    while f_size > 30:
        f_date = load_font(SERIF, f_size)
        f_19 = load_font(SERIF, f_size + 8)
        w = (d.textlength("THURSDAY ", font=f_date)
             + d.textlength("19", font=f_19)
             + d.textlength(" NOVEMBER 2026", font=f_date))
        if w <= 1000:
            break
        f_size -= 2
    w1 = d.textlength("THURSDAY ", font=f_date)
    w2 = d.textlength("19", font=f_19)
    w3 = d.textlength(" NOVEMBER 2026", font=f_date)
    x0 = (PAGE_W - (w1 + w2 + w3)) // 2
    baseline = 26 + f_date.getmetrics()[0]
    d.text((x0, baseline), "THURSDAY ", font=f_date, fill=INK, anchor="ls")
    d.text((x0 + w1, baseline), "19", font=f_19, fill=RED, anchor="ls")
    d.text((x0 + w1 + w2, baseline), " NOVEMBER 2026", font=f_date,
           fill=INK, anchor="ls")
    # Deck in our own words (not rank 1's): "three-president summit",
    # "GTA VI on sale", "an $81.3bn IPO", "the ICJ verdict",
    # "a storm off India".
    deck_txt = (f"{total} stories from one day — a three-president summit, "
                "GTA VI on sale, an $81.3bn IPO, the ICJ verdict, "
                "a storm off India")
    f_deck = None
    for dsize in (14, 13, 12):
        f_try = load_font(SANS_B, dsize)
        if d.textlength(deck_txt, font=f_try) <= 1000:
            f_deck = f_try
            break
    if f_deck is None:
        f_deck = load_font(SANS_B, 12)
    d.text((PAGE_W // 2, 80), deck_txt, font=f_deck, fill=RED, anchor="ma")
    d.line([12, 100, PAGE_W - 12, 100], fill=GOLD, width=2)

    # Region bar — computed from the final story lists; parts sum to 39.
    reg_txt = " · ".join(f"{name} {n}" for name, n in counts)
    f_reg = None
    for size in (13, 12, 11, 10):
        f_try = load_font(SANS_B, size)
        if (d.textlength("STORIES BY REGION — ", font=f_try)
                + d.textlength(reg_txt, font=f_try)) <= 1000:
            f_reg = f_try
            break
    if f_reg is None:
        f_reg = load_font(SANS_B, 10)
    lw = d.textlength("STORIES BY REGION — ", font=f_reg)
    total_w = lw + d.textlength(reg_txt, font=f_reg)
    rx = (PAGE_W - total_w) // 2
    d.text((rx, 104), "STORIES BY REGION — ", font=f_reg, fill=RED)
    d.text((rx + lw, 104), reg_txt, font=f_reg, fill=NAVY)

    # Big-numbers strip: one merged strip, segmented by 12% region
    # tint, NAVY outer frame, 1px region-colour dividers.
    f_nb = load_font(SANS_B, 17)
    f_nc = load_font(SANS, 9)
    strip_l, strip_t, strip_b = 7, 119, 168
    seg_w = 167  # 6 * 167 = 1002 (x 7..1009)
    for i, (num, cap, region) in enumerate(BIG_NUMBERS):
        nx = 12 + i * 168
        rc = REGION_RGB[region]
        tint = tuple(round(0.12 * a + 0.88 * b)
                     for a, b in zip(rc, PAPER))
        sx0 = strip_l + i * seg_w
        d.rectangle([sx0, strip_t, sx0 + seg_w - 1, strip_b], fill=tint)
        if i:
            d.line([sx0, strip_t, sx0, strip_b], fill=rc, width=1)
        d.text((nx, 124), num, font=f_nb, fill=NAVY)
        for j, ln in enumerate(wrap_capped(d, cap, f_nc, 156, 2)):
            d.text((nx, 146 + j * 11), ln, font=f_nc, fill=MUTED)
    d.rectangle([strip_l, strip_t, strip_l + 6 * seg_w - 1, strip_b],
                outline=NAVY, width=2)

    # Heroes as cards (3px border) with their strip on the image top.
    hw, img_h, hero_h = 328, 88, 170
    hy = 170
    f_hh = load_font(SANS_B, 16)
    f_hd = load_font(SANS, 13)
    hero_rects = []
    for i, hero in enumerate(HEROES):
        x = 12 + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hero_h], fill=CARD_BG,
                    outline=CARD_LINE, width=3)
        img = Image.open(os.path.join(ASSET_DIR, hero["file"])).convert("RGB")
        canvas.paste(cover_crop(img, hw - 6, img_h), (x + 3, hy + 3))
        draw_strip(d, x + 3, hy + 3, hw - 6, 16, hero["strip"],
                   STRIP_RGB[i + 1], 9)
        hero_rects.append((x + 3, hy + 3, hw - 6, 16))
        lines = wrap_capped(d, hero["headline"], f_hh, hw - 10, 2)
        ly = hy + img_h + 7
        for ln in lines:
            d.text((x + 5, ly), ln, font=f_hh, fill=INK)
            ly += 19
        deck_lines = wrap_capped(d, hero["deck"], f_hd, hw - 10, 2)
        ly = hy + img_h + 47
        for ln in deck_lines:
            d.text((x + 5, ly), ln, font=f_hd, fill=MUTED)
            ly += 16

    # Card grid: 5 cols x 3 rows, sequential numbering, 2px borders.
    # Strip / title / summary geometry from the approved sketch.
    col_w, card_h, gap_x, gap_y = 193, 112, 8, 5
    gx0, gy0 = 12, 346
    img_h2 = 60
    f_ct = load_font(SANS_B, 11)
    f_cs = load_font(SANS, 9)
    card_rects = []
    for idx, (title, pic, sum1, sum2, strip, region) in enumerate(CARDS):
        r, c = divmod(idx, 5)
        x = gx0 + c * (col_w + gap_x)
        y = gy0 + r * (card_h + gap_y)
        d.rectangle([x, y, x + col_w, y + card_h], fill=CARD_BG,
                    outline=CARD_LINE, width=2)
        img = Image.open(os.path.join(ASSET_DIR, pic)).convert("RGB")
        canvas.paste(cover_crop(img, col_w - 4, img_h2), (x + 2, y + 2))
        num = int(strip.split(" · ")[0])
        draw_strip(d, x + 2, y + 2, col_w - 4, 10, strip,
                   STRIP_RGB[num], 7)
        card_rects.append((x + 2, y + 2, col_w - 4, 10))
        lines = wrap_capped(d, title, f_ct, col_w - 12, 2)
        ly = y + img_h2 + 4
        for ln in lines:
            d.text((x + 6, ly), ln, font=f_ct, fill=INK)
            ly += 13
        d.text((x + 6, y + img_h2 + 31),
               one_line(d, sum1, f_cs, col_w - 12),
               font=f_cs, fill=MUTED)
        d.text((x + 6, y + img_h2 + 41),
               one_line(d, sum2, f_cs, col_w - 12),
               font=f_cs, fill=MUTED)

    # Map (300x202) + brief columns. Briefs are numbered 19-39,
    # CONTINUING from heroes 1-3 + cards 4-18. Each brief starts with
    # its city in bold and a vertical region-colour strip at the left.
    sec_y = 696
    f_sh = load_font(SANS_B, 16)
    d.text((12, sec_y), "WHERE IT HAPPENED", font=f_sh, fill=NAVY)
    d.text((324, sec_y), "MORE STORIES FROM 19 NOVEMBER",
           font=load_font(SANS_B, 15), fill=NAVY)
    d.line([324, sec_y + 22, PAGE_W - 12, sec_y + 22], fill=GOLD, width=2)
    map_im, map_log = render_map_box(300, 202, counts)
    canvas.paste(map_im, (12, sec_y + 22))
    d.rectangle([12, sec_y + 22, 12 + 300, sec_y + 22 + 202],
                outline=CARD_LINE, width=2)
    bw, bgap = 221, 12
    bx0, by0 = 324, sec_y + 24
    col_h = 200
    f_bn = load_font(SANS_B, 8)
    f_city = load_font(SANS_B, 8)
    f_bt = load_font(SANS, 8)
    LH, GAP = 10, 5
    cols = split_even(BRIEFS, 3)
    first_brief = 19
    for ci, col in enumerate(cols):
        cx = bx0 + ci * (bw + bgap)
        measured = []
        for bi, (city, region, b) in enumerate(col):
            n = first_brief + sum(len(c) for c in cols[:ci]) + bi
            lines = brief_lines(d, city, b, bw - 25)
            measured.append((n, city, region, lines))
        total_h = sum(len(lns) * LH for _n, _c, _r, lns in measured) \
            + (len(measured) - 1) * GAP
        assert total_h <= col_h, \
            f"brief column {ci} overflows by {total_h - col_h}px"
        extra = (col_h - total_h) / max(len(measured) - 1, 1)
        cy = by0
        for n, city, region, lines in measured:
            d.rectangle([cx, cy, cx + 5, cy + len(lines) * LH - 1],
                        fill=REGION_RGB[region])
            d.text((cx + 9, cy), f"{n}.", font=f_bn, fill=RED)
            ly = cy
            for li, ln in enumerate(lines):
                if li == 0:
                    pref = f"{city}: "
                    d.text((cx + 25, ly), pref, font=f_city, fill=INK)
                    d.text((cx + 25 + d.textlength(pref, font=f_city), ly),
                           ln[len(pref):], font=f_bt, fill=INK)
                else:
                    d.text((cx + 25, ly), ln, font=f_bt, fill=INK)
                ly += LH
            cy = ly + GAP + extra

    # DATE CHECK strip — prominent: navy band, gold frame, gold badge.
    dy, dh = 923, 46
    d.rectangle([12, dy, PAGE_W - 12, dy + dh], fill=NAVY)
    d.rectangle([12, dy, PAGE_W - 12, dy + dh], outline=GOLD, width=2)
    badge = "DATE CHECK"
    f_badge = load_font(SANS_B, 13)
    bw_b = int(d.textlength(badge, font=f_badge)) + 20
    d.rectangle([22, dy + 8, 22 + bw_b, dy + dh - 8], fill=GOLD)
    d.text((22 + bw_b // 2, dy + dh // 2), badge, font=f_badge, fill=NAVY,
           anchor="mm")
    msg = (f"All {total} stories are 19 November 2026 — Fed minutes, "
           "Voyager 1, Nvidia H200 halt, EU loan are 18 Nov: left out.")
    f_msg = 14
    while f_msg > 10:
        f_dc = load_font(SANS_B, f_msg)
        if d.textlength(msg, font=f_dc) <= (PAGE_W - 12) - (22 + bw_b + 12) - 10:
            break
        f_msg -= 1
    d.text((22 + bw_b + 12, dy + dh // 2), msg, font=f_dc, fill=WHITE,
           anchor="lm")

    # Footer — CLEAN: sources only + one attribution line. No
    # production notes, no "sketch", no revision numbers.
    src = ("Sources: Reuters · BBC · The Guardian · Fox News · ABS · "
           "CoinGecko · Al Jazeera · gov.uk · TBS · Daily Star · ANI · "
           "Kampala Post · NBS TV · ECOWAS · PropFlow360")
    f_size = 11
    while f_size > 8:
        f_ft = load_font(SANS, f_size)
        if d.textlength(src, font=f_ft) <= 1000:
            break
        f_size -= 1
    d.text((PAGE_W // 2, 975), src, font=f_ft, fill=MUTED, anchor="ma")
    note = "Disputed claims are attributed, not stated as fact."
    f_size = 10
    while f_size > 7:
        f_nt = load_font(SANS, f_size)
        if d.textlength(note, font=f_nt) <= 1000:
            break
        f_size -= 1
    d.text((PAGE_W // 2, 991), note, font=f_nt, fill=MUTED, anchor="ma")

    return canvas, map_log, hero_rects, card_rects


# ---- strip-colour verification (Kevin 19:01 WIB) ----
def sample_strip_color(img, rect):
    """Mode colour of 20 sample points across a strip's middle row."""
    x, y, w, h = rect
    mid = y + h // 2
    samples = [img.getpixel((x + int((i + 0.5) * w / 20), mid))
               for i in range(20)]
    counts = {}
    for s in samples:
        counts[s] = counts.get(s, 0) + 1
    return max(counts, key=counts.get)


def check_strip_neighbours(img, hero_rects, card_rects):
    """Every picture's TOP colour must differ from its orthogonal
    neighbours (left, right, above, below). Returns a list of
    violations (empty = 0 violations)."""
    rects = hero_rects + card_rects  # stories 1-3 heroes, 4-18 cards
    colours = [sample_strip_color(img, r) for r in rects]

    def overlaps_x(a, b):
        ax, _ay, aw, _ah = rects[a]
        bx, _by, bw, _bh = rects[b]
        return ax < bx + bw and bx < ax + aw

    pairs = []
    # Heroes row: left/right neighbours.
    pairs += [(0, 1), (1, 2)]
    # Cards: same-row neighbours + same-column vertical neighbours.
    for r in range(3):
        for c in range(5):
            i = 3 + r * 5 + c
            if c < 4:
                pairs.append((i, i + 1))
            if r < 2:
                pairs.append((i, i + 5))
    # Heroes above row-1 cards (where the x-ranges overlap).
    for h in range(3):
        for c in range(5):
            if overlaps_x(h, 3 + c):
                pairs.append((h, 3 + c))
    bad = []
    for a, b in pairs:
        if colours[a] == colours[b]:
            bad.append((a + 1, b + 1, colours[a]))
    return bad


def main():
    canvas, map_log, hero_rects, card_rects = render_page()
    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    # Determinism: render a second time, bytes must match exactly.
    canvas2, _log2, _h2, _c2 = render_page()
    out2 = os.path.join(HERE, "entry.png")
    canvas2.save(out2, format="PNG", optimize=True)
    data2 = open(out2, "rb").read()
    assert data == data2, "render is not deterministic"
    assert canvas.size == (1024, 1024), canvas.size
    assert len(data) <= 1048576, len(data)
    img = Image.open(out)
    bad = check_strip_neighbours(img, hero_rects, card_rects)
    print("map pins:", map_log["pins"], "| dots:", map_log["dots"],
          "| skipped dots:", map_log["skipped_dots"])
    print("strip violations:", bad if bad else "0")
    print("wrote", out, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest())
    assert not bad, f"strip colour violations: {bad}"


if __name__ == "__main__":
    main()
