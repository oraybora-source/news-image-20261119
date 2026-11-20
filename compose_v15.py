# compose_v15.py — builds entry.png (1024x1024) for news-image-20261119, v15.
#
# v15 = sketch 3 rev3 (Kevin Gas 20 Nov 12:52 WIB): NO world map;
# 7-region strip with 34 numbered dots; briefs full-width below;
# timeline 36px + TL_PAD 6; DATE CHECK 10 items; hero 200/94,
# card 141/51. GTA hero: VI board at top-left of panel, below the
# strip (asset edited: board moved down 110px by PIL so the strip
# does not cover it; old board spot filled with purple sky; stray
# pole stubs above the board erased). IPO hero: green chart line
# erased above the roofline (per-row sky fill). Kyiv card asset
# unchanged from v14r1 (deep-sea-blue + whole STOP).
#
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
# v5 changes (20 Nov ~06:07-06:15 WIB, Kevin):
#  - Map (Kevin 06:07: "petanya maksa vertical, sesuaikan saja, gpp
#    ada gap kecil"): project() now uses ONE scale for both axes
#    (contain-fit, true aspect ratio) — the world is no longer
#    stretched to fill the box; ocean gaps top/bottom are fine.
#    Pin/dot offsets reworked for the compressed cluster; the
#    "Gaza" label moved so no pin paints over it.
#  - 10 Uganda, 3rd draw (Kevin 06:12 "Boleh", overriding the
#    2x/panel limit): presidents BIGGER, clearly shaking hands at
#    far left; red car still BIG + WHOLE centre-right (main
#    subject); factory behind — sketch composition kept.
#  - Hero 2 GTA (Kevin 06:14: billboard "VI" still cut at the top):
#    the source poster is re-cropped to exclude the "GTA VI LAUNCH
#    DAY" headline + caption line entirely (the first re-crop cut
#    through the headline and left half-cut red letters at the top
#    edge); the scene now starts at clean sky, "VI" billboard whole
#    with margin, pink car big + whole. Hero focus 0.5.
#  - Enriched the bare panels (Kevin 06:15: "jangan terlalu hambar,
#    jangan cuma 1 gedung doang"): 8 SARB, 3rd draw (street +
#    people + tree + South African flag around the whole building;
#    Kevin named card 8 as the example), 11 COP31, 3rd draw
#    (audience + Turkish/EU flags + potted tree around the whole
#    screen/chimneys/X), 5 Ukraine (edited in place: street +
#    people + tree added, Capitol/flag/crates untouched). Main
#    subjects stay whole with margins; no new in-picture text.
#  - Titles, texts, numbers, layout, house style unchanged.
#
# v7 changes (20 Nov ~06:41 WIB, Kevin: "Maksudku ga perlu di full
# vertical"): the map does NOT have to fill the whole box height.
# It is now a NATURAL-ASPECT STRIP: full world width (no left/right
# crop — Americas, Europe, Africa, Asia, Australia all in), no
# stretch, no ocean gap inside the map; height follows the true
# ratio (260 px wide -> 130 px tall). The map box follows the map
# height; the space left in the left column holds a compact 3-line
# legend (numbered pin / gold star / small dot), centred. Pin/dot
# offsets retuned for the smaller scale so all 11 dots return
# (Tokyo, Australia, Wellington were lost in the v6 cover-fit crop).
#
# v8 changes (20 Nov ~07:05 WIB, Kevin picked preview A + "MORE
# STORIES naik sedikit sejajar sama peta"): the map column is
# widened 260 -> 400 px (map 400x190, still natural-aspect 2:1, full
# world width, only Arctic/Antarctic ocean cropped, no stretch, no
# ocean gap); the legend is now 2 compact lines (10pt) under the
# map; briefs take the remaining ~590 px in 3 columns at 12pt
# (largest size that fits, picked largest-first). The "Gaza" label
# is back (it fits at this scale) and the Brussels dot is shifted
# (-14,-14) so it clears the The Hague pin. Heroes + cards
# UNCHANGED from v7. MORE STORIES alignment: the first brief row
# now starts exactly at y+24 (= the map top) — the slack is spread
# over the remaining rows only, so the briefs sit level with the
# map instead of starting ~14 px below it.
#
# v9 changes (20 Nov ~07:20 WIB, Kevin GAS 07:17 WIB "perbaiki kartu 5
# dulu"): ATM 20 Nov 07:00 WIB membantah kartu 5 — "US approves $1.6bn
# Ukraine aid" TIDAK ADA di berita mana pun; satu-satunya $1,6 miliar
# adalah IMF, 16 Nov, bersyarat, bukan AS. Kartu 5 diganti dengan IEA
# World Energy Outlook 2026 (rilis 19 Nov, IEA sendiri 05:00 UTC):
# "IEA: energy shock reshapes world", Paris, region WORLD. Strip
# "$1.6bn" diganti "2.8bn" (barrel minyak hilang akibat krisis Hormuz,
# IEA via SAFETY4SEA/Tutubi/The Edge). Region counts: AMERICAS 3->2,
# WORLD 3->4; pin 5 pindah Washington -> Paris. Ilustrasi kartu 5 baru
# (gaya rumah; turbin angin + panel surya + matahari + globe; subjek
# utuh dengan margin, dinormalisasi ke inner box v4: 3% sisi, 18% atas
# supaya matahari tidak ketutup strip, 3% bawah). MORE STORIES (Kevin
# 07:14 WIB "jangan ada gap, 3 kolom harus sama atas bawahnya"):
# baris brief kini TINGGI TETAP (3 baris x leading) — semua kolom
# mulai dan berakhir di y yang sama, baris ke-k mulai di y yang sama
# di ketiga kolom; slack tidak lagi dibagi per kolom (itu yang bikin
# barisnya zig-zag: kolom 2 rapat 2-6px, kolom 1 renggang 12-16px).
#
# v10 changes (20 Nov ~07:30 WIB, Kevin 07:27 + 07:28 + 07:29 + 07:31 WIB):
#  - +3 brief (total 34 cerita, 21 brief, 7 baris/kolom) supaya 3 kolom
#    MORE STORIES selaras atas-bawah: London (UK leasehold Bill masuk
#    Parlemen 19 Nov), Brasilia (Lula kecam pasar atas "spekulasi",
#    Reuters 19 Nov), Dakar (Faye berlakukan anggaran lewat dekrit,
#    AFP/Reuters 19 Nov). DITOLAK sesudah verifikasi: Estonia (pengumuman
#    tutup perbatasan 15-16 Nov, tutupnya 1 Des), Spanyol (mogok umum
#    11 Nov, bukan 19 Nov), senator AS soal AI (Reuters 18 Nov), Epstein
#    (RUU diteken 19 Nov 2025, bukan 2026). Region: EUROPE 7->8,
#    AMERICAS 2->3, AFRICA 3->4; TOTAL 34; DATE CHECK "All 34 stories".
#  - Baris brief kini TINGGI VARIABEL (baris = brief terpanjang di
#    baris itu x leading): 6 baris x 36px + 1 baris x 24px = 240px.
#    Supaya muat, bagian atas dipadatkan 35px TANPA mengecilkan font
#    dan TANPA mengubah rasio gambar: masthead 100->96, region bar
#    36->32, numbers strip 58->54, hero image 121->110 (box 220->209),
#    card image 70->64 (box 152->146). Margin dikit di atas (judul ->
#    baris pertama) dan di bawah (baris terakhir -> DATE CHECK).
#  - Legenda peta ke bahasa Inggris (Kevin 07:29 WIB): "Numbered pin:
#    story number / Gold star: Shenzhen summit / Small dot: other
#    briefs" — sebelumnya bahasa Indonesia, satu-satunya teks
#    non-Inggris di gambar. Legenda kini di tengah vertikal di
#    ruangnya.
#  - Garis pembatas navy 2px selebar penuh band bawah, tepat di atas
#    judul WHERE IT HAPPENED / MORE STORIES (Kevin 07:31 WIB).
#  - Brasilia ditambah ke PLACES (-47.9, -15.8) untuk dot brief 33;
#    dot brief 32 (label "UK", koordinat London) tabrakan pin Den Haag
#    (jarak ~5px < 9px) jadi di-skip oleh compositor (tercatat di log);
#    dot Dakar ke-2 di-skip karena koordinat sama dengan dot Dakar
#    brief 19. Label brief 32 "UK" (bukan "London") supaya teksnya
#    muat 2 baris — mengikuti konvensi brief 22 ("US: Microsoft…").
#    KOREKSI susun kolom: brief baru 32-34 masuk kolom 3 (bukan baris
#    ke-7 tiap kolom) — baris ke-7 = brief 20, 27, 34. Brief 20
#    (Shenzhen) 3 baris, jadi brief 27 dan 34 DIPERPANJANG kalimatnya
#    supaya sama-sama 3 baris dan ketiga kolom berakhir di y yang
#    sama: 27 "A bill against transnational repression is drafted."
#    (MOJ kirim draf amandemen Anti-Infiltration Act ke Cabinet;
#    diumumkan di sidang 18 Nov, dilapor Taipei Times 19 Nov) dan 34
#    "Faye ordered the budget bill into force by decree." (AFP/
#    Reuters 19 Nov). Baris ke-7 kini 3/3/3 baris; jumlah baris
#    total tetap 240px, anggaran band tidak berubah.
#
# v14 changes (20 Nov, Kevin 11:23 WIB: "Pake format sebelum nya aja,
# perbaiki" — 3 sketsa fix A/B/C DITOLAK karena tambah jelek; pakai
# format v13, perbaiki di dalam format itu):
#  1. Timeline jam-per-jam (5 titik, SEMUA jam TERVERIFIKASI dari sumber
#     utama — lihat build-note-v14.md) di bawah deck, sebelum bar region.
#  2. Tag REPORTED/CLAIM/FORECAST (pill di strip, kanan) + sumber per
#     kartu di bawah ringkasan (hero + 10 kartu).
#  3. Strip label dipendekkan (topik 1 kata) supaya teks + pill muat.
#  4. DATE CHECK 2 baris dengan detail jam/angka cerita 18 Nov yang
#     dibuang (Fed minutes Wed 2pm ET, Voyager 1 Wed 10:16 GMT,
#     EU 45bn, Van Gogh $190.4m — semua TERVERIFIKASI).
#  5. Ruang untuk timeline + sumber: region bar 32->24, numbers 54->46,
#     hero img 110->96 (HERO_H 209->202, head 24->22, deck 13->12),
#     card img 64->52 (CARD_H 146->142, summary lh 15).
#  6. Ilustrasi digambar ulang (aset v14): SATU house style flat seperti
#     v13 TAPI tiap panel punya warna latar sendiri yang kuat (bukan
#     semua krem — memperbaiki 17/22 pasangan warna atas <8 RGB v13).
#  Layout, urutan, fakta, 34 cerita, peta opsi A, bar region, footer
#  TIDAK berubah. JANGAN submit, JANGAN bundle, JANGAN duel.
#
# Run:  python3 compose_v14.py   (needs Pillow; writes entry.png here)
# The entrypoint main.py only copies entry.png — it never re-renders.

import hashlib, json
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
HERO_H, HERO_IMG, HERO_HEAD, HERO_DECK = 200, 94, 22, 12
CARD_H, CARD_IMG, CARD_HEAD, CARD_SUM = 141, 51, 16, 12
MAP_W = 400
BRIEF_NCOLS = 3
BRIEF_SIZE, BRIEF_LH = 14, 16

# ---- stories ----
# Heroes: file, headline, deck, strip, region, focus_y (0=top, 1=bottom).
HEROES = [
    {
        "file": "media-generation-v14-hero-summit.png",
        "headline": "Trump, Xi and Putin meet in Shenzhen",
        "deck": "Trade truce and nuclear arms top the agenda as the three leaders meet in Shenzhen",
        "strip": "1 · SHENZHEN · SUMMIT",
        "region": "ASIA",
        "focus": 0.55,
        "tag": "REPORTED",
        "source": "Reuters, Guardian",
    },
    {
        "file": "media-generation-v15-hero-gtavi.png",
        "headline": "GTA VI launches worldwide",
        "deck": "Gamers enter Vice City as the launch begins on PlayStation 5 and Xbox",
        "strip": "2 · NEW YORK · GAMES",
        "region": "AMERICAS",
        "focus": 0.57,
        "tag": "REPORTED",
        "source": "Reuters, Guardian",
    },
    {
        "file": "media-generation-v15-hero-ipo.png",
        "headline": "Anthropic's $81.3bn IPO — a record",
        "deck": "Priced at $83 a share, the biggest IPO ever; markets rise ahead of the debut",
        "strip": "3 · NASDAQ · MARKETS",
        "region": "AMERICAS",
        "focus": 0.48,
        "tag": "REPORTED",
        "source": "Reuters",
    },
]

# Cards in reading order (numbers 4-13): city, title, file, s1, s2,
# strip, region, focus_y.
# v13 (20 Nov, Kevin GAS 'buat 1 gaya'): SEMUA 13 panel digambar ulang
# ke SATU house style (STYLE_GUIDE_v13.md) via media.generate_image mode
# edit dari aset v12 — komposisi sketsa tetap, hanya rendering disatukan:
# latar kertas krem, outline navy tipis, blok warna datar, tanpa gradien/
# shading 3D/glow. Retry: Prague 1x (kerumunan diperbesar), Gaza 1x
# (kotak-X navy liar dihapus), Kyiv 1x (rambu STOP terpotong tepi ->
# digeser utuh + focus 0.53). Teks v12 TETAP (Hormuz 'at risk', COP31
# '1.5C at risk', Gaza 'Israel says it crossed Gaza line').
# v12 (20 Nov ~09:05 WIB, Kevin GAS "Perbaiki v12"; 3 perbaikan teks
# murah dari audit pasca-kerja v11 — duel v11 GATE GAGAL, juri tidak
# percaya "lost" di Hormuz + deck COP31 kontradiktif + headline Gaza
# tanpa atribusi): Gaza "Israel pushes past Gaza line" -> "Israel says
# it crossed Gaza line" (wording audit "says it pushed past" TIDAK
# muat 2 baris di 16pt — "crossed" meminjam kata sumber "troops cross
# the ceasefire line"); kartu 5 "cost 2.8bn barrels of oil" -> "puts
# 2.8bn barrels of oil at risk" + strip "lost" -> "at risk" (angka
# 2.8bn + atribusi IEA tetap; sumber harfiah Birol "cumulative
# losses" — "at risk" adalah bingkai ulang per rekomendasi audit);
# kartu 11 "1.5°C may pass" -> "1.5°C at risk" ("goal" dibuang supaya
# muat 2 baris di 13pt). Layout, gambar, peta, divider, margin,
# legenda, DATE CHECK, footer TIDAK berubah.
CARDS = [
    ("Gaza", "Israel says it crossed Gaza line",
     "media-generation-v14-card-gaza.png",
     "Rare ground op", "Troops cross the ceasefire line",
     "4 · GAZA · CEASEFIRE", "MIDEAST", 0.50, "CLAIM", "Reuters, Al Jazeera"),
    ("Paris", "IEA: energy shock reshapes world",
     "media-generation-v14-card-iea.png",
     "Hormuz crisis puts 2.8bn", "barrels of oil at risk",
     "5 · PARIS · ENERGY", "WORLD", 0.50, "REPORTED", "IEA"),
    ("The Hague", "ICJ verdict in Myanmar case",
     "media-generation-v14-card-icj.png",
     "Judgment read today", "Rohingya case at UN court",
     "6 · THE HAGUE · ICJ", "EUROPE", 0.50, "REPORTED", "Reuters, Guardian"),
    ("Puri", "Cyclone Akvan nears India coast",
     "media-generation-v14-card-cyclone.png",
     "Red alerts out; schools shut", "Machilipatnam to Puri",
     "7 · PURI · CYCLONE", "ASIA", 0.50, "FORECAST", "Reuters, ANI"),
    ("Johannesburg", "South Africa holds rates",
     "media-generation-v14-card-sarb.png",
     "SARB holds repo at 7.25%", "Rand at lowest of the year",
     "8 · JOHANNESBURG · RATES", "AFRICA", 0.50, "REPORTED", "Reuters"),
    ("Berlin", "Coalition of the Willing in Berlin",
     "media-generation-v14-card-berlin.png",
     "Witkoff and Kushner attend", "Coalition meets in Berlin",
     "9 · BERLIN · TALKS", "EUROPE", 0.50, "REPORTED", "Reuters, Guardian"),
    ("Mpigi", "Two presidents open car plant",
     "media-generation-v14-card-uganda.png",
     "Museveni and Samia at launch", "Double Q in Mpigi",
     "10 · MPIGI · CAR PLANT", "AFRICA", 0.50, "REPORTED", "Reuters, NBS TV"),
    ("Antalya", "COP31 draft drops fossil fuel",
     "media-generation-v14-card-cop31.png",
     "Draft drops fossil phase-out", "1.5°C at risk",
     "11 · ANTALYA · COP31", "MIDEAST", 0.50, "FORECAST", "Reuters"),
    ("Prague", "Prague protest for free media",
     "media-generation-v14-card-prague.png",
     "Crowds demand free press", "Huge march in Prague",
     "12 · PRAGUE · PROTEST", "EUROPE", 0.50, "REPORTED", "Reuters, AP"),
    ("Kyiv", "Zelensky: US blocks missiles",
     "media-generation-v14r1-card-kyiv.png",
     "Kyiv accuses Washington", "Missile deliveries held back",
     "13 · KYIV · MISSILES", "EUROPE", 0.62, "CLAIM", "Reuters, Guardian"),
]

# Briefs in reading order (numbers 14-31): city, region, text.
# Every text is the first sentence of the verified story.
BRIEFS = [
    # v11 (20 Nov ~07:50 WIB, Kevin 07:47 WIB "kolom 2 terlalu melet,
    # pindah-pindah berita biar sesuai"): briefs disusun ulang supaya
    # TIAP BARIS seragam jumlah barisnya — baris 1, 4, 7 semua 3 baris,
    # baris 2, 3, 5, 6 semua 2 baris — jadi tidak ada celah di kolom
    # mana pun dan ketiga kolom terlihat sama ritmenya. Verifikasi v10:
    # kolom 2 ternyata penuh di SEMUA baris (6 dari 7 brief 3 baris),
    # kolom 1 dan 3 cuma 2 brief 3 baris — jadi tukar isi 25<->27 saja
    # tidak mengubah apa-apa (keduanya 3 baris). Satu-satunya ubah teks:
    # 26 Kuala Lumpur dipendekkan "UNHCR halts refugee registration."
    # (buang "in Malaysia" — label kota sudah Kuala Lumpur; fakta sama,
    # Reuters 19 Nov) supaya jadi 2 baris; 9 brief 3 baris + 12 brief
    # 2 baris = 3 baris x 3 baris + 4 baris x 2 baris. Set cerita,
    # region counts, dan set kota peta TIDAK berubah.
    ("New Delhi", "ASIA", "Congress targets the Modi government over inflation."),
    ("Saada", "MIDEAST", "Saudi intercepts a Houthi missile."),
    ("Tokyo", "ASIA", "India and Japan hold 2+2 defence talks."),
    ("Shenzhen", "ASIA", "Trump mentions ex-Nvidia boss Huang 'briefly' in Xi talks."),
    ("Australia", "OCEANIA", "The jobless rate jumps to 4.9%."),
    ("Global", "WORLD", "Bitcoin slips below $63,000."),
    ("Shenzhen", "EUROPE", "Japan PM Takaichi holds talks with Putin."),
    ("MAIB", "WORLD", "The Bayesian had a hidden wind weakness."),
    ("Tokyo", "ASIA", "Japan machinery orders dip 0.3%."),
    ("Hormuz", "MIDEAST", "A tanker is hit by a projectile."),
    ("US", "WORLD", "Microsoft is in talks to sell AI services to ByteDance."),
    ("UK", "EUROPE", "The UK leasehold Bill enters Parliament."),
    ("Kuala Lumpur", "ASIA", "UNHCR halts refugee registration."),
    ("Brussels", "EUROPE", "The EU delays methane rules by two years."),
    ("Finland", "EUROPE", "The first nuclear waste store is approved."),
    ("Wellington", "OCEANIA", "Bumrah strikes twice at lunch."),
    ("Saudi Arabia", "MIDEAST", "Danger has passed in the south."),
    ("Taiwan", "ASIA", "A bill against transnational repression is drafted."),
    ("Brasilia", "AMERICAS", "Lula blasts markets over speculation."),
    ("Dakar", "AFRICA", "Senegal holds Armed Forces Day."),
    ("Dakar", "AFRICA", "Faye ordered the budget bill into force by decree."),
]

# Big numbers strip (number, caption, region of the divider colour).
NUMBERS = [
    ("$81.3bn", "Anthropic IPO — largest ever", "AMERICAS"),
    ("$83", "Anthropic IPO price", "AMERICAS"),
    ("2.8bn", "Barrels of oil at risk in Hormuz crisis", "WORLD"),
    ("7.25%", "SARB holds repo rate", "AFRICA"),
    ("4.9%", "Australia jobless — highest", "OCEANIA"),
    ("$63,000", "Bitcoin slips below, down 2.7%", "WORLD"),
]

COUNTS = [("EUROPE", 8), ("THE AMERICAS", 3), ("ASIA-PACIFIC", 8),
          ("MIDEAST", 5), ("AFRICA", 4), ("OCEANIA", 2), ("WORLD", 4)]
TOTAL = 34

DATECHECK_LINES = [
    "All 34 stories are 19 Nov 2026 — left out: Fed minutes (Wed 2pm), "
    "Voyager 1 (Wed 10:16 GMT), Nvidia H200 halt, EU \u20ac45bn loan,",
    "Van Gogh sale $190.4m, Ruto address in Kenya, COP31 fossil-fuel "
    "coalition at 30, Uganda Airlines first flight, Trump–Xi hug, GST2 "
    "launch — all Wed 18 Nov, not on this page.",
]
SOURCES_LINE = ("Sources: Reuters · BBC · The Guardian · Fox News · ABS · "
                "CoinGecko · Al Jazeera · gov.uk · TBS · Daily Star · ANI · "
                "Kampala Post · NBS TV · ECOWAS · PropFlow360 · IEA · AFP · Taipei Times")

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
    "UK": (-0.1, 51.5),  # v10: label brief 32 (sama koordinat London)
    "UK": (-0.1, 51.5),
    "US": (-77.0, 38.9),
    "China": (116.4, 39.9),
    "Australia": (149.1, -35.3),
    "Kuala Lumpur": (101.7, 3.1),
    "Beijing": (116.4, 39.9),
    "Brussels": (4.4, 50.8),
    "Johannesburg": (28.0, -26.2),  # v7 fix: was (-28.0, -26.2) — wrong
    # hemisphere; the pin sat in the South Atlantic instead of South
    # Africa. Johannesburg is 28.0E, 26.2S.
    "Mpigi": (32.3, 0.2),
    "Antalya": (30.7, 36.9),
    "Dakar": (-17.4, 14.7),
    "Paris": (2.35, 48.85),  # v9: kartu 5 IEA WEO (markas IEA, Paris)
    "Brasilia": (-47.9, -15.8),  # v10: dot brief 33 (Lula, Reuters 19 Nov)
}

# Hand-tuned pin offsets (dx, dy in px) so clustered pins do not
# overlap; a thin leader line joins each offset pin to its true spot.
# v5 (undistorted map compresses Europe/India vertically): Berlin up
# so it clears Kyiv, Kyiv left so it clears Berlin and lets the
# Finland dot stay, Puri down so it clears New Delhi.
PIN_OFFSETS = {
    "Finland": (0, -12),
    "Prague": (0, 14),
    "The Hague": (-14, 0),
    "Kerch": (12, 0),
    "Saada": (0, 14),
    "Hormuz": (0, -12),
    "Taiwan": (12, 0),
    "Antalya": (16, -12),
    "Berlin": (0, -12),
    "Kyiv": (-12, 0),
    "Puri": (0, 12),
    "New Delhi": (0, -14),
}
# Dot offsets (same leader-line mechanism as pins). v7 (natural-aspect
# strip, smaller scale): Saada moved right so it clears the Mpigi pin,
# Taiwan moved down so it clears the Tokyo dot, Brussels moved up-left
# so it clears the Kyiv pin. v5: the Hormuz dot sat on top of the
# "Gaza" label, so it moves down-right.
DOT_OFFSETS = {
    "Hormuz": (8, 11),
    "Saada": (10, 14),
    "Taiwan": (0, 14),
    "Brussels": (-14, -14),  # v8: (-8,-8) lands within 9 px of the
    # The Hague pin at the bigger scale; (-14,-14) clears it.
}
# Which pins get a name label, and on which side (l/r/a/b).
# v8: "Gaza" is BACK — at the 400 px map scale its label fits
# (v7 dropped it: at 260 px it collided on all four sides).
# "Wellington"/"Tokyo" are dots, so their entries here are inert.
PIN_LABELS = {"Wellington": "l", "Tokyo": "a", "Shenzhen": "l",
              "Gaza": "l"}  # v6: star near right edge, label below would run off-box
# Extra vertical nudge (px) for a label, on top of its side offset.
# v7: Shenzhen -7 so the text clears the New Delhi pin above and the
# Saudi Arabia dot below (both sub-1px clearances, verified visually).
PIN_LABEL_DY = {"Shenzhen": -7}

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


def paint_strip(draw, x, y, w, h, text, bg, size, reserve=0):
    """A coloured band on the top edge of a picture: "N · CITY · TOPIC"
    in bold white. The font shrinks until the text fits in the width
    left after reserving `reserve` px at the right end (tag pill)."""
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    fnt = None
    for s in (size, size - 1, size - 2, size - 3):
        trial = load(SANS_B, s)
        if draw.textlength(text, font=trial) <= w - 8 - reserve:
            fnt = trial
            break
    if fnt is None:
        fnt = load(SANS_B, size - 3)
    draw.text((x + 4, y + h / 2), text, font=fnt, fill=WHITE, anchor="lm")


TAG_COLORS = {
    "REPORTED": (40, 130, 70),
    "CLAIM": (178, 44, 36),
    "FORECAST": (200, 120, 40),
}


def draw_tag_pill(d, x, y, w, h, tag, size):
    """Small attribution pill at the right end of a strip: REPORTED
    (green) / CLAIM (red) / FORECAST (amber), bold white text."""
    fnt = load(SANS_B, size)
    tw = d.textlength(tag, font=fnt)
    pw = int(tw + 10)
    ph = 9
    px = x + w - 4 - pw
    py = y + (h - ph) // 2
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=4,
                        fill=TAG_COLORS[tag])
    d.text((px + pw / 2, py + ph / 2), tag, font=fnt, fill=WHITE,
           anchor="mm")


# ---- v14 timeline (hours VERIFIED from primary sources, see
# build-note-v14.md): local times, in order, like rank 2 izayoi.
TIMELINE = [
    ("00:00", "AUCKLAND — GTA VI unlocks"),
    ("05:00", "IEA — Outlook released"),
    ("10:00", "THE HAGUE — ICJ ruling read"),
    ("11:48", "NEW YORK — ANT first trade"),
    ("16:27", "SHENZHEN — Three leaders meet"),
]


# ---- v15 geometry (sketch 3 rev3) ----
TL_H = 36            # timeline 28 -> 36 (loosened)
TL_PAD = 6           # breathing room under the timeline (rev1)
REG_PAD = 4          # breathing room under the stories bar (rev1)
STRIP_H = 66         # region strip height (dots r=11, two rows, rev2)
DC_Y = 968           # DATE CHECK bar y


def draw_timeline(d, y):
    """Timeline loosened (v15 / sketch 3 rev3): 36px tall, hour 11pt,
    event 10pt. Returns (spans, gaps) for the crosscheck audit; the
    caller advances y by TL_H + TL_PAD."""
    d.text((12, y + 2), "THE DAY BY HOURS", font=load(SANS_B, 10),
           fill=NAVY)
    d.text((1012, y + 2), "local time, in order", font=load(SANS, 9),
           fill=MUTED, anchor="ra")
    line_y = y + 20
    d.line([(110, line_y), (914, line_y)], fill=NAVY, width=2)
    spans = []
    for i, (hour, event) in enumerate(TIMELINE):
        cx = 150 + i * 181
        d.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5],
                  fill=RED, outline=WHITE, width=1)
        d.text((cx, y + 2), hour, font=load(SANS_B, 11), fill=RED,
               anchor="ma")
        d.text((cx, y + 24), event, font=load(SANS, 10), fill=INK,
               anchor="ma")
        w = d.textlength(event, font=load(SANS, 10))
        spans.append({"event": event, "hour": hour, "cx": cx,
                      "x0": round(cx - w / 2, 1), "x1": round(cx + w / 2, 1)})
    gaps = [round(spans[i + 1]["x0"] - spans[i]["x1"], 1)
            for i in range(len(spans) - 1)]
    return spans, gaps


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
# Map NATURAL-ASPECT STRIP (v7, Kevin 20 Nov 06:41 WIB: "Maksudku ga
# perlu di full vertikal"). The map does NOT have to fill the whole
# Map NATURAL-ASPECT (v8, Kevin picked preview A 20 Nov 07:05 WIB):
# the map column is widened 260 -> 400 px, so the map is 400x190 —
# box height: full world width (lon -180..180, no left/right crop),
# one undistorted scale, height follows the true ratio — 400 px wide
# -> 190 px tall (2:1, lat +-85°, only Arctic/Antarctic ocean
# cropped). Centre lon 10 so Wellington (174.8) still fits inside
# the right edge with its pin; centre lat 0. The space left in the
# left column holds a compact 2-line legend, not ocean.
MAP_S = 400 / 360.0
MAP_CLON = 10.0
MAP_CLAT = 0.0
MAP_H = 190


def project(lon, lat, mw, mh):
    """Equirectangular, UNDISTORTED, NATURAL-ASPECT STRIP (v7). One
    scale for both axes; the whole world (lon -180..180, lat 90..-90)
    spans the box width, height follows the true 2:1 ratio."""
    x = mw / 2.0 + (lon - MAP_CLON) * MAP_S
    y = mh / 2.0 + (MAP_CLAT - lat) * MAP_S
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
    for _city, _t, _f, _s1, _s2, strip, region, _focus, _tag, _src in CARDS:
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
    """The world map at its TRUE aspect ratio, NATURAL-ASPECT STRIP
    (v7: never stretched — Kevin 20 Nov 06:07 WIB; never ocean gaps
    — Kevin 20 Nov 06:31 WIB; never full-vertical — Kevin 20 Nov
    06:41 WIB). One scale for both axes; the whole world spans the
    box width, height follows the true 2:1 ratio. Pins r 6 with 8pt
    numbers, dots r 3 kept 9px apart; dots whose centre falls outside
    the box are skipped (logged, same as collisions).
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
            dy = PIN_LABEL_DY.get(city, 0)
            tw = d.textlength(city, font=f_label)
            if side == "r":
                tx, ty = qx + 8, qy - 5 + dy
            elif side == "l":
                tx, ty = qx - 8 - tw, qy - 5 + dy
            elif side == "a":
                tx, ty = qx - tw / 2, qy - 16 + dy
            else:
                tx, ty = qx - tw / 2, qy + 9 + dy
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
        dx, dy = DOT_OFFSETS.get(city, (0, 0))
        qx, qy = px + dx, py + dy
        if not (4 <= qx <= mw - 4 and 4 <= qy <= mh - 4):
            skipped.append(city + " (out of view)")
            continue
        if any(((qx - x) ** 2 + (qy - y) ** 2) ** 0.5 < 9
               for x, y, _r in placed):
            skipped.append(city)
            continue
        if (dx, dy) != (0, 0):
            d.line([(px, py), (qx, qy)], fill=NAVY, width=1)
        d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3],
                  fill=REGION_COLORS[region], outline=WHITE, width=1)
        placed.append((qx, qy, 3))
        placed_dots.append(city)
    log = {"pins": [m for _c, m, _r in pins],
           "dots": placed_dots, "skipped_dots": skipped}
    return im, log


def draw_map_legend(d, x, y_top, w, y_bottom):
    """Compact 3-line legend under the map strip (v7), centred in the
    leftover space of the left column. Explains the three marker
    kinds; plain on the paper background, no box."""
    f_txt = load(SANS, 11)
    f_num = load(SANS_B, 8)
    rows = [
        ("pin", "Numbered pin: story number"),
        ("star", "Gold star: Shenzhen summit"),
        ("dot", "Small dot: other briefs"),
    ]
    lh = 18
    y = y_top + (y_bottom - y_top - len(rows) * lh) // 2
    for kind, text in rows:
        cy = y + lh // 2
        if kind == "pin":
            d.ellipse([x + 2, cy - 6, x + 14, cy + 6],
                      fill=(40, 90, 160), outline=WHITE, width=1)
            tw = d.textlength("4", font=f_num)
            d.text((x + 8 - tw / 2, cy - 4), "4", font=f_num, fill=WHITE)
        elif kind == "star":
            d.polygon(star_points(x + 8, cy, 7, 3), fill=GOLD, outline=NAVY)
        else:
            d.ellipse([x + 5, cy - 3, x + 11, cy + 3],
                      fill=(40, 130, 70), outline=WHITE, width=1)
        d.text((x + 20, y + 2), text, font=f_txt, fill=INK)
        y += lh


def draw_map_legend_compact(d, x, y_top, w, y_bottom):
    """Compact 2-line legend (v8, preview A): the map is 190 px tall,
    so only ~26 px remain under it. Row 1: numbered pin. Row 2: gold
    star + small dot, side by side. v10: English text (Kevin 07:29 WIB)
    and vertically centred in the leftover space."""
    f_txt = load(SANS, 10)
    f_num = load(SANS_B, 8)
    y = y_top + (y_bottom - y_top - 26) // 2
    cy = y + 6
    d.ellipse([x + 2, cy - 6, x + 14, cy + 6],
              fill=(40, 90, 160), outline=WHITE, width=1)
    tw = d.textlength("4", font=f_num)
    d.text((x + 8 - tw / 2, cy - 4), "4", font=f_num, fill=WHITE)
    d.text((x + 20, y + 1), "Numbered pin: story number", font=f_txt,
           fill=INK)
    y += 13
    cy = y + 6
    d.polygon(star_points(x + 8, cy, 7, 3), fill=GOLD, outline=NAVY)
    tx = x + 20
    d.text((tx, y + 1), "Gold star: Shenzhen summit", font=f_txt, fill=INK)
    tx += d.textlength("Gold star: Shenzhen summit", font=f_txt) + 12
    d.ellipse([tx + 2, cy - 3, tx + 8, cy + 3],
              fill=(40, 130, 70), outline=WHITE, width=1)
    tx += 12
    d.text((tx, y + 1), "Small dot: other briefs", font=f_txt, fill=INK)


# ---- page sections ----
def draw_chrome(d):
    """Top line + masthead + deck. Returns y=96 (v10: was 100)."""
    d.text((12, 8), "ALL DATED 19 NOV", font=load(SANS_B, 11), fill=RED)
    d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=load(SANS_B, 11),
           fill=NAVY, anchor="ma")
    d.text((1012, 8), f"{TOTAL} STORIES", font=load(SANS_B, 11), fill=RED,
           anchor="ra")
    y_base = 68
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
    d.text((W // 2, 78), deck, font=load(SANS_B, 14), fill=RED, anchor="ma")
    return 96


def draw_region_bar(d, y):
    """Navy title cell + 7 region-tinted segments. Returns y + 24 (v14)."""
    hgt = 24
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
    dividers between segments. Returns y0 + 46 (v14: was 54)."""
    hgt = 46
    x = 12
    for i, (num, label, region) in enumerate(NUMBERS):
        bw = 163 if i < 5 else 165
        rc = REGION_COLORS[region]
        d.text((x + 8, y0 + 1), num, font=load(SANS_B, 17), fill=NAVY)
        clines = wrap(d, label, load(SANS_B, 10), bw - 16, 2)
        assert "…" not in "".join(clines), f"number caption cut: {label}"
        cy = y0 + 21
        for ln in clines:
            d.text((x + 8, cy), ln, font=load(SANS_B, 10), fill=INK)
            cy += 13
        if i > 0:
            d.line([(x, y0), (x, y0 + hgt)], fill=rc, width=1)
        x += bw + 4
    return y0 + hgt


def draw_hero(canvas, d, x, y, w, hero, strip_color, col):
    """One hero panel; returns its strip rect for the colour check.
    v14: tag pill on the strip (right) + source line under the deck."""
    d.rectangle([x, y, x + w, y + HERO_H], fill=CARD_BG,
                outline=CARD_LINE, width=1)
    img = Image.open(os.path.join(ASSETS, hero["file"])).convert("RGB")
    canvas.paste(cover_crop(img, w - 2, HERO_IMG, hero["focus"]),
                 (x + 1, y + 1))
    paint_strip(d, x + 1, y + 1, w - 2, 12, hero["strip"], strip_color, 11,
                reserve=62)
    draw_tag_pill(d, x + 1, y + 1, w - 2, 12, hero["tag"], 8)
    ty = y + 1 + HERO_IMG + 4
    for ln in wrap(d, hero["headline"], load(SANS_B, HERO_HEAD), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS_B, HERO_HEAD), fill=INK)
        ty += HERO_HEAD + 4
    ty += 2
    for ln in wrap(d, hero["deck"], load(SANS, HERO_DECK), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS, HERO_DECK), fill=MUTED)
        ty += HERO_DECK + 4
    ty += 2
    d.text((x + 8, ty), "— " + hero["source"], font=load(SANS, 9),
           fill=MUTED)
    return (x + 1, y + 1, w - 2, 12, strip_color, hero["strip"], 0, col)


def draw_card(canvas, d, x, y, w, card, strip_color, row, col):
    """One story card; returns its strip rect for the colour check.
    v14: strip 12px + tag pill on the strip (right) + source line
    under the summary; summary leading tightened to 15px."""
    city, title, fname, s1, s2, strip, _region, focus, tag, src = card
    d.rectangle([x, y, x + w, y + CARD_H], fill=CARD_BG,
                outline=CARD_LINE, width=1)
    img = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
    canvas.paste(cover_crop(img, w - 2, CARD_IMG, focus), (x + 1, y + 1))
    paint_strip(d, x + 1, y + 1, w - 2, 12, strip, strip_color, 10,
                reserve=56)
    draw_tag_pill(d, x + 1, y + 1, w - 2, 12, tag, 7)
    ty = y + 1 + CARD_IMG + 4
    for ln in wrap(d, title, load(SANS_B, CARD_HEAD), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS_B, CARD_HEAD), fill=INK)
        ty += CARD_HEAD + 4
    summ = s1 + " " + s2
    for ln in wrap(d, summ, load(SANS, CARD_SUM), w - 16, 2):
        d.text((x + 8, ty), ln, font=load(SANS, CARD_SUM), fill=MUTED)
        ty += CARD_SUM + 3
    ty += 2
    d.text((x + 8, ty), "— " + src, font=load(SANS, 9), fill=MUTED)
    return (x + 1, y + 1, w - 2, 12, strip_color, strip, row, col)


def draw_briefs(d, x, y, w, total_h):
    """MORE STORIES: 3 even columns of 7 briefs each, "N. City: text…"
    with the number red bold and the city navy bold. Returns y+total_h.
    v10: rows are VARIABLE height (tallest brief in the row x leading),
    so row k starts at the same y in all three columns and all three
    columns end at the same y. Small margins above the first row and
    below the last row (Kevin 07:28 WIB); the title sits below the
    divider line drawn by build() (Kevin 07:31 WIB)."""
    TITLE_DY = 4
    TITLE_ZONE = 20
    M_TOP = 6
    M_BOTTOM = 6
    d.text((x, y + TITLE_DY), "MORE STORIES FROM 19 NOVEMBER",
           font=load(SANS_B, 16), fill=NAVY)
    col_w = (w - (BRIEF_NCOLS - 1) * 12) // BRIEF_NCOLS
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
    per = len(BRIEFS) // BRIEF_NCOLS
    groups = [list(range(i * per, (i + 1) * per)) for i in
              range(BRIEF_NCOLS)]
    assert all(len(lines) <= 3 for (_, _, _, _, _, lines) in measured), \
        "brief over 3 lines"
    nrows = per
    row_hs = [max(len(measured[i][5]) for i in
                  [g[r] for g in groups]) * BRIEF_LH for r in range(nrows)]
    avail = total_h - TITLE_DY - TITLE_ZONE - M_TOP - M_BOTTOM
    assert sum(row_hs) <= avail, \
        f"briefs do not fit: {sum(row_hs)} > {avail}"
    # leftover slack (if any) lands in the bottom margin.
    row_ys = []
    yy = y + TITLE_DY + TITLE_ZONE + M_TOP
    for rh in row_hs:
        row_ys.append(yy)
        yy += rh
    for ci, idxs in enumerate(groups):
        chunk = [measured[i] for i in idxs]
        bx = x + ci * (col_w + 12)
        for si, (city, region, num_txt, city_txt, head_w, lines) in \
                enumerate(chunk):
            by = row_ys[si]
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
    """DATE CHECK bar (v14: 2 lines, 10pt, with hours/figures for the
    discarded 18 Nov stories) + source lines under it."""
    d.rectangle([12, y, 1012, y + 30], fill=NAVY)
    d.rectangle([12, y, 120, y + 30], fill=GOLD)
    d.text((66, y + 15), "DATE CHECK", font=load(SANS_B, 11), fill=NAVY,
           anchor="mm")
    d.text((130, y + 5), DATECHECK_LINES[0], font=load(SANS, 10),
           fill=WHITE, anchor="la")
    d.text((130, y + 18), DATECHECK_LINES[1], font=load(SANS, 10),
           fill=WHITE, anchor="la")
    d.text((W // 2, y + 38), SOURCES_LINE, font=load(SANS, 9), fill=MUTED,
           anchor="ma")
    d.text((W // 2, y + 49), "Disputed claims are attributed, not stated as fact.",
           font=load(SANS, 9), fill=MUTED, anchor="ma")


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



# ---- v15 bottom band: region strip + full-width briefs (no map) ----
REGION_SHORT = {"EUROPE": "EUROPE", "AMERICAS": "AMERICAS",
                "ASIA": "ASIA-PAC", "MIDEAST": "MIDEAST",
                "AFRICA": "AFRICA", "OCEANIA": "OCEANIA", "WORLD": "WORLD"}


def region_numbers():
    """Story numbers per region, computed from the data."""
    m = {k: [] for _d, k in REGION_ORDER}
    for h in HEROES:
        m[h["region"]].append(int(h["strip"].split(" · ")[0]))
    for card in CARDS:
        m[card[6]].append(int(card[5].split(" · ")[0]))
    for i, (_city, region, _text) in enumerate(BRIEFS):
        m[region].append(14 + i)
    for k in m:
        m[k].sort()
    return m


REG_NUMS = region_numbers()
assert [len(REG_NUMS[k]) for _d, k in REGION_ORDER] == [8, 3, 8, 5, 4, 2, 4], REG_NUMS


def draw_region_strip(d, x, y, w, h):
    """7 equal segments; region name on top, numbered story dots
    below (numbers, not counts). Dots r=11, 11pt bold white, TWO rows
    per segment (rev2, Kevin 12:30 WIB: two-digit numbers unreadable
    at r=8). Returns dot positions for the audit."""
    seg_w = w / 7.0
    dots_info = []
    for i, (disp, key) in enumerate(REGION_ORDER):
        rc = REGION_COLORS[key]
        tint = tuple(int(255 * 0.88 + c * 0.12) for c in rc)
        sx = x + i * seg_w
        ex = sx + seg_w if i < 6 else x + w
        d.rectangle([sx, y, ex, y + h], fill=tint)
        short = REGION_SHORT[key]
        f_name = load(SANS_B, 10)
        tw = d.textlength(short, font=f_name)
        assert tw <= seg_w - 8, f"region name too wide: {short}"
        d.text(((sx + ex) / 2, y + 3), short, font=f_name, fill=NAVY,
               anchor="ma")
        nums = REG_NUMS[key]
        r, gap = 11, 3
        n1 = (len(nums) + 1) // 2
        rows = [nums[:n1], nums[n1:]]
        f_num = load(SANS_B, 11)
        for ri, row in enumerate(rows):
            total_w = len(row) * (2 * r + gap) - gap
            assert total_w <= seg_w - 4, f"dots too wide: {short} {total_w}"
            cx0 = (sx + ex) / 2 - total_w / 2
            cy = y + 27 + ri * 23
            for j, num in enumerate(row):
                ccx = cx0 + r + j * (2 * r + gap)
                d.ellipse([ccx - r, cy - r, ccx + r, cy + r], fill=rc,
                          outline=WHITE, width=1)
                d.text((ccx, cy), str(num), font=f_num, fill=WHITE,
                       anchor="mm")
                dots_info.append({"n": num, "region": key,
                                  "cx": round(ccx, 1), "cy": cy, "r": r})
        if i > 0:
            d.line([(sx, y), (sx, y + h)], fill=rc, width=1)
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=2)
    return dots_info


def draw_briefs_n(d, x, y, w, total_h, items, size, lh):
    """draw_briefs, but briefs carry their ORIGINAL numbers
    (items: list of (num, city, region, text)).
    Rev1 (Kevin 12:21 WIB): (a) ROW_GAP px between rows; (b) the side
    bar is drawn ONCE per row spanning the FULL row height, so all
    three bars in a row are one straight, equal-height line."""
    ROW_GAP = 3
    TITLE_DY, TITLE_ZONE, M_TOP, M_BOTTOM = 4, 20, 4, 4
    d.text((x, y + TITLE_DY), "MORE STORIES FROM 19 NOVEMBER",
           font=load(SANS_B, 16), fill=NAVY)
    ncol = 3
    col_w = (w - (ncol - 1) * 12) // ncol
    measured = []
    for (num, city, region, text) in items:
        num_txt = f"{num}. "
        city_txt = f"{city}: "
        head_w = (d.textlength(num_txt, font=load(SANS_B, size))
                  + d.textlength(city_txt, font=load(SANS_B, size)))
        lines = wrap_first_narrow(d, text, load(SANS, size),
                                  col_w - 12 - head_w, col_w - 12, 4)
        if "…" in "".join(lines):
            raise AssertionError(f"brief cut: {city} {lines}")
        measured.append((city, region, num_txt, city_txt, head_w, lines))
    per = len(items) // ncol
    assert len(items) % ncol == 0
    groups = [list(range(i * per, (i + 1) * per)) for i in range(ncol)]
    if any(len(lines) > 3 for (_, _, _, _, _, lines) in measured):
        raise AssertionError("brief over 3 lines")
    row_hs = [max(len(measured[i][5]) for i in [g[r] for g in groups]) * lh
              for r in range(per)]
    avail = total_h - TITLE_DY - TITLE_ZONE - M_TOP - M_BOTTOM
    if sum(row_hs) + (per - 1) * ROW_GAP > avail:
        raise AssertionError(
            f"briefs do not fit: {sum(row_hs) + (per - 1) * ROW_GAP} > {avail}")
    row_lines = [[len(measured[i][5]) for i in [g[r] for g in groups]]
                 for r in range(per)]
    row_ys = []
    yy = y + TITLE_DY + TITLE_ZONE + M_TOP
    for rh in row_hs:
        row_ys.append(yy)
        yy += rh + ROW_GAP
    for ci, idxs in enumerate(groups):
        chunk = [measured[i] for i in idxs]
        bx = x + ci * (col_w + 12)
        for si, (city, region, num_txt, city_txt, head_w, lines) in \
                enumerate(chunk):
            by = row_ys[si]
            rc = REGION_COLORS[region]
            rh = row_hs[si]
            d.rectangle([bx, by + 2, bx + 5, by + rh - 2], fill=rc)
            tx = bx + 10
            d.text((tx, by), num_txt, font=load(SANS_B, size),
                   fill=RED)
            d.text((tx + d.textlength(num_txt,
                                       font=load(SANS_B, size)), by),
                   city_txt, font=load(SANS_B, size), fill=NAVY)
            ty = by
            for li, ln in enumerate(lines):
                lx = tx + head_w if li == 0 else tx
                d.text((lx, ty), ln, font=load(SANS, size), fill=INK)
                ty += lh
    return {"size": size, "lh": lh, "row_hs": row_hs,
            "row_lines": row_lines, "col_w": col_w, "row_gap": ROW_GAP}


def pick_briefs(canvas, x, y, w, total_h, items):
    """Largest-first brief size, same candidates as the v14r1 composer."""
    for sz, lh in [(14, 16), (13, 15), (13, 14), (12, 14), (12, 13),
                   (12, 12), (11, 13)]:
        trial = canvas.copy()
        dt = ImageDraw.Draw(trial)
        try:
            info = draw_briefs_n(dt, x, y, w, total_h, items, sz, lh)
            return (sz, lh, info)
        except AssertionError:
            continue
    raise AssertionError("no brief size fits")


# ---- crosscheck-1 audits (programmatic, run inside the build) ----
def audit_top_colors(canvas, rects):
    """Mode colour of the 8 rows just below each strip; every
    orthogonal neighbour pair (18 pairs) must differ by >= 8 RGB."""
    from collections import Counter
    px = canvas.load()
    modes = {}
    man = []
    for (x, y, w, h, _exp, label, r, c) in rects:
        n = int(label.split(" · ")[0])
        man.append({"strip": [x, y, x + w, y + h], "n": n,
                    "row": r, "col": c})
        cnt = Counter()
        for yy in range(y + h + 1, y + h + 9):
            for xx in range(x + 2, x + w - 1):
                cnt[px[xx, yy]] += 1
        modes[n] = cnt.most_common(1)[0][0]
    by_rc = {(m["row"], m["col"]): m["n"] for m in man}
    pairs = []
    for (r, c), n in sorted(by_rc.items()):
        if (r, c - 1) in by_rc:
            pairs.append((by_rc[(r, c - 1)], n))
        if r == 0 and (r + 1, c) in by_rc:
            pairs.append((n, by_rc[(r + 1, c)]))
        if r == 1 and (r + 1, c) in by_rc:
            pairs.append((n, by_rc[(r + 1, c)]))
    dists = []
    for a, b in pairs:
        ca, cb = modes[a], modes[b]
        dist = round(math.sqrt(sum((u - v) ** 2 for u, v in zip(ca, cb))), 1)
        dists.append({"pair": [a, b], "dist": dist,
                      "colors": [list(ca), list(cb)]})
    mind = min(x["dist"] for x in dists)
    return {"pairs": len(dists), "min_dist": mind,
            "violations": [x for x in dists if x["dist"] < 8],
            "distances": dists,
            "modes": {str(k): list(v) for k, v in modes.items()}}


def audit_white_above_strips(canvas, rects):
    """No pure-white pixel in the panel-top row directly above any
    strip (ni20 strip-bug lesson)."""
    px = canvas.load()
    bad = []
    for (x, y, w, h, _exp, label, _r, _c) in rects:
        for xx in range(x, x + w):
            if px[xx, y - 1] == (255, 255, 255):
                bad.append(label)
                break
    return bad


def audit_datecheck_widths(d):
    out = []
    for ln in DATECHECK_LINES:
        w = d.textlength(ln, font=load(SANS, 10))
        out.append({"line": ln, "width": round(w, 1), "fits_882": w <= 882})
    return out


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
    assert y == 96, y
    spans, gaps = draw_timeline(d, y)
    y += TL_H + TL_PAD
    y = draw_region_bar(d, y) + REG_PAD + GAP
    y = draw_numbers(d, y)
    assert y == 213, y

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
    assert bottom_y == 698, bottom_y
    # v15 (Kevin 12:21 WIB): NO world map — 7-region strip with
    # numbered story dots; briefs full-width below the strip.
    d.rectangle([12, bottom_y, 1012, bottom_y + 1], fill=NAVY)
    strip_y = bottom_y + 4
    dots_info = draw_region_strip(d, 12, strip_y, 1000, STRIP_H)
    assert len(dots_info) == 34, len(dots_info)
    by = strip_y + STRIP_H + 4
    bh = DC_Y - by
    brief_items = [(14 + i, bb[0], bb[1], bb[2])
                   for i, bb in enumerate(BRIEFS)]
    sz, lh, binfo = pick_briefs(canvas, 12, by, 1000, bh, brief_items)
    draw_briefs_n(d, 12, by, 1000, bh, brief_items, sz, lh)
    print(f"  briefs: {sz}pt/{lh}px lh row_hs={binfo['row_hs']} "
          f"row_lines={binfo['row_lines']}")


    draw_datecheck(d, DC_Y)
    # ---- crosscheck-1 (programmatic, during the process) ----
    dcw = audit_datecheck_widths(d)
    assert all(x["fits_882"] for x in dcw), dcw
    tc = audit_top_colors(canvas, rects)
    assert not tc["violations"], tc["violations"]
    wa = audit_white_above_strips(canvas, rects)
    assert not wa, wa
    print(f"  timeline gaps: {gaps}")
    print(f"  top colours: {tc['pairs']} pairs min_dist={tc['min_dist']} "
          f"violations={len(tc['violations'])}")
    print(f"  datecheck widths: {[x['width'] for x in dcw]}")
    print(f"  region strip dots: {len(dots_info)} (34 expected)")
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
    print(f"  map: NONE (7-region strip, {len(dots_info)} dots)")
    manifest = {
        "version": "v15", "stories": TOTAL,
        "geometry": {"timeline_h": TL_H, "timeline_pad": TL_PAD,
                     "reg_pad": REG_PAD, "hero_h": HERO_H,
                     "hero_img": HERO_IMG, "card_h": CARD_H,
                     "card_img": CARD_IMG, "strip_h": STRIP_H,
                     "bottom_y": bottom_y, "dc_y": DC_Y},
        "region_numbers": {k: v for k, v in REG_NUMS.items()},
        "timeline": {"spans": spans, "gaps": gaps,
                     "min_gap": min(gaps) if gaps else None},
        "briefs": {"size": sz, "lh": lh, "row_hs": binfo["row_hs"],
                   "row_lines": binfo["row_lines"],
                   "row_gap": binfo["row_gap"], "y": by, "h": bh},
        "region_strip": {"y": strip_y, "h": STRIP_H,
                         "dots": dots_info, "dot_count": len(dots_info)},
        "datecheck_widths": dcw,
        "audits": {"strip_check_violations": bad,
                   "top_color": {"pairs": tc["pairs"],
                                 "min_dist": tc["min_dist"],
                                 "violations": tc["violations"]},
                   "white_above_strips": wa},
        "file": {"path": out, "bytes": len(data),
                 "sha256": hashlib.sha256(data).hexdigest()},
    }
    with open(os.path.join(HERE, "entry-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return out


if __name__ == "__main__":
    build()
