# news-image-20261119 — final entry v2, 31 stories

One image summing up the world's news of **Thursday 19 November 2026**.
All 31 stories are dated 19 November 2026; 18 November items (Fed
minutes, Voyager 1, Nvidia H200 halt, EU loan, Van Gogh sale) were left
out on purpose and are named in the DATE CHECK strip on the image.

## Heroes (3)

1. **Shenzhen — Summit.** Trump, Xi and Putin meet in Shenzhen.
   Trade truce and nuclear arms top the agenda. (Reuters, The Guardian)
2. **New York — Games.** GTA VI launches worldwide. Gamers enter
   Vice City as the launch begins on PlayStation 5 and Xbox.
   (Reuters, The Guardian)
3. **Nasdaq — Markets.** Anthropic's $81.3bn IPO — a record. Priced
   at $83 a share, the biggest IPO ever. (Reuters)

## Cards (10)

4. **Gaza — Ceasefire line.** Israeli push past Gaza ceasefire line.
   Rare ground op; troops cross the ceasefire line.
   (Reuters, Al Jazeera)
5. **Washington — Ukraine aid.** US approves $1.6bn Ukraine aid.
   Approved Thursday: $1.6bn for Ukraine. (Reuters)
6. **The Hague — Genocide case.** ICJ verdict in Myanmar case.
   Judgment read today; Rohingya case at UN court.
   (Reuters, The Guardian)
7. **Puri — Cyclone Akvan.** Cyclone Akvan nears India coast.
   Red alerts out; schools shut Machilipatnam to Puri. (Reuters, ANI)
8. **Johannesburg — Rates.** South Africa holds rates.
   SARB holds repo at 7.25%; Rand at lowest of the year. (Reuters)
9. **Berlin — Coalition talks.** Coalition of the Willing in Berlin.
   Witkoff and Kushner attend; Coalition meets in Berlin.
   (Reuters, The Guardian)
10. **Mpigi — Car plant.** Two presidents open car plant.
    Museveni and Samia at launch; Double Q in Mpigi.
    (Reuters, NBS TV, Kampala Post)
11. **Antalya — COP31 draft.** COP31 draft drops fossil fuel.
    Draft drops fossil phase-out; 1.5°C may pass. (Reuters)
12. **Prague — Media protest.** Prague protest for free media.
    Crowds demand free press; huge march in Prague. (Reuters, AP)
13. **Kyiv — Missile deliveries.** Zelensky: US blocks missiles.
    Kyiv accuses Washington; missile deliveries held back.
    (Reuters, The Guardian)

## Briefs (18)

14. **New Delhi:** Congress targets Modi government over inflation.
15. **Saada:** Saudi intercepts a Houthi missile.
16. **Tokyo:** India and Japan hold 2+2 defence talks.
17. **Australia:** The jobless rate jumps to 4.9%.
18. **Global:** Bitcoin slips below $63,000.
19. **Dakar:** Senegal holds Armed Forces Day.
20. **Shenzhen:** Trump mentions ex-Nvidia boss Huang 'briefly' in
    Xi talks.
21. **MAIB:** The Bayesian had a hidden wind weakness.
22. **US:** Microsoft is in talks to sell AI services to ByteDance.
23. **Shenzhen:** Japan PM Takaichi holds talks with Putin.
24. **Tokyo:** Japan machinery orders dip 0.3%.
25. **Brussels:** The EU delays methane rules by two years.
26. **Kuala Lumpur:** UNHCR halts refugee registration in Malaysia.
27. **Taiwan:** A transnational repression bill is drafted.
28. **Finland:** The first nuclear waste store is approved.
29. **Wellington:** Bumrah strikes twice at lunch.
30. **Hormuz:** A tanker is hit by a projectile.
31. **Saudi Arabia:** Danger has passed in the south. (Reuters,
    19 Nov 2026 — see the note below.)

## What changed from the v1 entry (39 stories)

- The layout follows the approved 2-row × 5-column sketch: 3 heroes,
  10 cards, 18 briefs — 31 stories in all. Text is bigger and fewer
  stories are crammed in, so every headline and brief reads cleanly.
- **Yemen brief removed.** The sketch carried "Yemen: Houthi rocket
  kills 53 soldiers". Checking it before the build found it happened
  on **Monday 19 October 2026** (Reuters/AP, published 2026-10-19),
  not 19 November — the same wrong-date trap as the Van Gogh sale,
  which was also removed. It was replaced with a verified 19 November
  item from Reuters (19 Nov 2026): the coalition dealt with a missile
  threat towards Riyadh on Thursday and Saudi Civil Defense said the
  danger had passed; also reported by Al Arabiya the same day.
- **Van Gogh sale removed.** The auction date was ambiguous
  (18 vs 19 November), so the story was dropped entirely rather than
  risk a misdated card; it is named in the DATE CHECK strip as left
  out.
- **Uganda card wording fixed.** The sketch read "Museveni and Samia
  open plant"; the entry reads "Museveni and Samia at launch".
- **DATE CHECK wording fixed.** It now reads "All 31 stories are
  19 November 2026 — Fed minutes, Voyager 1, Nvidia H200 halt, EU
  loan, Van Gogh sale: all 18 Nov, left out."
- **Map improved.** Continent outlines are 2px, pins are bigger with
  8pt numbers, dots are kept 9px apart. Three brief dots (Brussels,
  Taiwan, Saudi Arabia) are skipped on collision and logged by the
  compositor — the stories are still in the briefs and the map still
  shows their region's pins.
- Region counts: EUROPE 7, THE AMERICAS 3, ASIA-PACIFIC 8,
  MIDEAST 5, AFRICA 3, OCEANIA 2, WORLD 3 — 31 in all.

## How the image was made

`compose_v2.py` (Python 3 + Pillow, written fresh in the build
session) composes `entry.png` (1024×1024) from the illustration
assets in `assets/` plus text rendered from the verified news strings
above. All 13 illustrations share ONE house style — flat modern
editorial illustration, clean vector shapes, bold flat colour blocks,
warm cream paper, navy outlines. Ten were redrawn to that style in
this session (GTA hero, Gaza, Ukraine aid, ICJ, Cyclone, SARB, Berlin,
COP31, Prague, Kyiv); three were kept from the v2 build because they
were already flat (summit, IPO, Uganda). COP31 was drawn twice — the
first version had "CLIMATE CONFERENCE 2024" written on its screen,
the wrong year, so it was replaced with a version with no text at
all. No copied artwork, no photos, no text inside the illustrations
except the intended "VI" billboard in the GTA hero and the red STOP
sign in the Kyiv card; every other word on the page is drawn by
`compose_v2.py`. `main.py` (Python 3.13, standard library
only) copies `entry.png` to the output directory; it runs twice in
grading and writes identical bytes both times. Research cutoff:
19 Nov 2026 evening WIB; Africa + COP31 stories verified from named
sources the same evening.

v4 fix (20 Nov 2026, after Kevin reviewed the v3 image at display
size): cards 5–13 were redrawn in wide 3:1 format and normalised
onto a 1930×700 canvas (exact card-box aspect), so each picture's
subject is WHOLE with a margin around it — no more subjects cut at
the frame edges (the SARB bank building, the Kyiv missile launcher
and the Prague church tower were all cut in v3). Card 10 follows
the approved sketch: the big red car is the main subject, whole,
centre-right; the two presidents shake hands, small, at the far
left; the factory stands behind. The SARB arrow was shortened in
PIL with a clean cut instead of a third draw. All card focus values
are 0.5 now (the assets match the box aspect, so no crop is taken).
Titles, texts, numbers and layout are unchanged.
