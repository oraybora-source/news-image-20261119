#!/usr/bin/env python3
"""M-C "Tanggal-Dulu + Aset" compositor for news-image-20261119.

Builds entry.png (1024x1024) from AI-directed illustration assets + text
rendered from verified strings (STORIES.md). No network, no clock, no
randomness: two runs must write identical bytes.

Layout (criterion 1 first, per Rule Ledger S2):
  1. Masthead: giant date "THURSDAY 19 NOVEMBER 2026" on a navy band.
  2. Four BIG heroes (2x2), each with a date stamp + source + short label.
  3. Breadth strip: 5 regions x 3 briefs (15 stories, all 19 Nov).
  4. Footer: date check + sources.

Assets are pure illustration, no text inside them (red-team mitigation:
AI text garbles); every word on the page is drawn here from strings
verified in STORIES.md (research cutoff 19 Nov 2026 ~09:50 WIB).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

NAVY = (15, 36, 64)
NAVY_SOFT = (28, 58, 96)
GOLD = (217, 164, 65)
PAPER = (246, 241, 231)
INK = (24, 28, 36)
MUTED = (92, 96, 104)
WHITE = (255, 255, 255)
LIGHT = (226, 231, 238)
RED = (178, 44, 36)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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
    return lines


def cover_crop(img, tw, th):
    """Center-crop img to exactly tw x th (no distortion)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


HEROES = [
    {
        "file": "media-generation-hero-summit-0-2facf046-c366-4c54-811a-378f151baf31.png",
        "kicker": "SHENZHEN  ·  SUMMIT",
        "headline": "TRUMP, XI AND PUTIN MEET",
        "sub": "Trilateral talks in Shenzhen at the APEC summit today",
        "source": "NYT",
    },
    {
        "file": "media-generation-hero-gtavi-0-2ba192a8-4751-42fd-bb85-541410d0920c.png",
        "kicker": "VICE CITY  ·  GAMES",
        "headline": "GTA VI ROLLS OUT WORLDWIDE",
        "sub": "Gamers enter Vice City as the global launch begins",
        "source": "BBC",
    },
    {
        "file": "media-generation-hero-ipo-0-8cbb9db1-f691-408f-ab20-746c58a7d930.png",
        "kicker": "MARKETS  ·  RECORD IPO",
        "headline": "ANTHROPIC RAISES $81.3BN",
        "sub": "Biggest IPO ever, shares priced at $83",
        "source": "AL JAZEERA",
    },
    {
        "file": "media-generation-hero-gaza-0-d883abe3-a658-4e15-8940-7187b06791d4.png",
        "kicker": "GAZA  ·  CONFLICT",
        "headline": "RARE GROUND OP IN GAZA",
        "sub": "Israeli troops move beyond the Yellow Line",
        "source": "BBC",
    },
]

STRIP = [
    ("AMERICAS", [
        "Jeffries set to be first Black House Speaker",
        "Fed minutes: most officials expect more rate hikes",
        "Canada adjusts China ties, seeks right US deal",
    ]),
    ("EUROPE", [
        "EU proposes €45bn Ukraine loan",
        "Estonia to close Russia border from December",
        "Prague: mass protest for media independence",
        "Spain: general strike hits ports and factories",
        "Crimean Bridge attacked again, traffic halted",
    ]),
    ("ASIA & PACIFIC", [
        "Myanmar faces historic genocide verdict at UN court",
        "Cyclone Akvan nears India's coast",
        "Nvidia halts H200 chip shipments to China",
    ]),
    ("MIDDLE EAST", [
        "Houthi rocket kills 53 soldiers in Yemen",
        "Saudi Arabia says danger passed in southern cities",
    ]),
    ("SCIENCE & CULTURE", [
        "Voyager 1 reaches one light-day from Earth",
        "Van Gogh sells for record $190.4m",
        "Finland approves first nuclear waste repository",
    ]),
]


def draw_masthead(d):
    d.rectangle([0, 0, W, 176], fill=NAVY)
    d.rectangle([0, 176, W, 180], fill=GOLD)
    f_small = font(BOLD, 19)
    f_day = font(BOLD, 40)
    f_date = font(BOLD, 76)
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=f_small,
           fill=GOLD, anchor="ma")
    d.text((W // 2, 52), "THURSDAY", font=f_day, fill=WHITE, anchor="ma")
    d.text((W // 2, 96), "19 NOVEMBER 2026", font=f_date,
           fill=WHITE, anchor="ma")


def draw_hero(canvas, d, hero, x, y, w, h):
    img = Image.open(os.path.join(ASSETS, hero["file"])).convert("RGB")
    canvas.paste(cover_crop(img, w, h), (x, y))
    # date stamp chip, top-right of the picture
    chip_f = font(BOLD, 14)
    chip = "19 NOV 2026"
    cw = int(d.textlength(chip, font=chip_f)) + 18
    d.rectangle([x + w - cw - 8, y + 8, x + w - 8, y + 32], fill=GOLD)
    d.text((x + w - 8 - cw // 2, y + 20), chip, font=chip_f,
           fill=NAVY, anchor="mm")
    # caption bar
    bar_h = 82
    bar = Image.new("RGBA", (w, bar_h), NAVY + (228,))
    canvas.paste(bar, (x, y + h - bar_h), bar)
    d2 = ImageDraw.Draw(canvas)
    fk = font(BOLD, 13)
    fh = font(BOLD, 23)
    fs = font(REG, 14)
    d2.text((x + 12, y + h - bar_h + 8), hero["kicker"], font=fk, fill=GOLD)
    d2.text((x + w - 12, y + h - bar_h + 8), hero["source"], font=fk,
            fill=LIGHT, anchor="ra")
    lines = wrap(d2, hero["headline"], fh, w - 24)
    ly = y + h - bar_h + 26
    for ln in lines[:2]:
        d2.text((x + 12, ly), ln, font=fh, fill=WHITE)
        ly += 25
    d2.text((x + 12, ly + 2), hero["sub"], font=fs, fill=LIGHT)


def draw_strip(d):
    y0 = 712
    f_head = font(BOLD, 20)
    f_date = font(BOLD, 14)
    d.text((12, y0), "AROUND THE WORLD TODAY", font=f_head, fill=NAVY)
    d.text((W - 12, y0 + 4), "19 NOVEMBER 2026", font=f_date,
           fill=MUTED, anchor="ra")
    d.line([12, y0 + 30, W - 12, y0 + 30], fill=GOLD, width=2)
    col_w = 193
    gap = 8
    x0 = 12
    f_col = font(BOLD, 13)
    f_b = font(REG, 13)
    for ci, (region, briefs) in enumerate(STRIP):
        cx = x0 + ci * (col_w + gap)
        d.text((cx, y0 + 40), region, font=f_col, fill=NAVY)
        d.line([cx, y0 + 60, cx + col_w - 6, y0 + 60], fill=NAVY, width=1)
        by = y0 + 70
        for b in briefs:
            lines = wrap(d, "•  " + b, f_b, col_w - 4)
            for ln in lines[:3]:
                d.text((cx, by), ln, font=f_b, fill=INK)
                by += 15
            by += 6


def draw_footer(d):
    d.line([12, 976, W - 12, 976], fill=MUTED, width=1)
    f_f = font(REG, 12)
    d.text((W // 2, 990),
           "All stories happened or were first reported on 19 November 2026.",
           font=f_f, fill=MUTED, anchor="ma")
    d.text((W // 2, 1006),
           "Sources: NYT · BBC · Al Jazeera · Sky News",
           font=f_f, fill=MUTED, anchor="ma")


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)
    draw_masthead(d)
    # heroes: 2x2 grid, y 188..700
    hw, hh = 502, 250
    positions = [(12, 188), (510, 188), (12, 446), (510, 446)]
    for hero, (x, y) in zip(HEROES, positions):
        draw_hero(canvas, d, hero, x, y, hw, hh)
    draw_strip(d)
    draw_footer(d)
    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
