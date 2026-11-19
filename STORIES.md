# news-image-20261119 — final entry, 39 stories

One image summing up the world's news of **Thursday 19 November 2026**.
All 39 stories are dated 19 November 2026; 18 November items (Fed
minutes, Voyager 1, Nvidia H200 halt, EU loan) were left out on purpose
and are named in the DATE CHECK strip on the image.

## Heroes (3)

1. **Shenzhen — Summit.** Trump, Xi and Putin meet in Shenzhen.
   Trade truce and nuclear arms top the agenda. (Reuters, The Guardian)
2. **New York — Games.** GTA VI launches worldwide. Gamers enter
   Vice City as the launch begins on PlayStation 5 and Xbox.
   (Reuters, The Guardian)
3. **Nasdaq — Markets.** Anthropic's $81.3bn IPO — a record. Priced
   at $83 a share, the biggest IPO ever. (Reuters)

## Cards (15)

4. **Gaza — Ceasefire line.** Israeli push past Gaza ceasefire line.
   Israeli troops cross the ceasefire line. (Reuters, Al Jazeera)
5. **Washington — Ukraine aid.** US approves $1.6bn Ukraine aid
   package. $1.6bn approved on Thursday for Ukraine's defence.
   (Reuters)
6. **Kyiv — Missile deliveries.** Zelensky: US blocking missile
   deliveries. Missile deliveries held back. (Reuters)
7. **Estonia — Russia border.** Estonia to shut Russia border.
   Border with Russia to shut. (Reuters)
8. **Prague — Media protest.** Prague mass protest for media
   independence. Hundreds of thousands protest. (Reuters)
9. **Spain — General strike.** Spain hit by nationwide general
   strike. Ports and factories disrupted. (Reuters)
10. **Kerch — Bridge attack.** Crimean Bridge attacked again.
    Russian official confirms the attack. (Reuters)
11. **The Hague — Genocide case.** ICJ rules on Myanmar genocide
    case. Verdict due today in The Hague. (Reuters)
12. **Puri — Cyclone Akvan.** Cyclone Akvan nears India's coast.
    Red alerts out; schools shut from Machilipatnam to Puri.
    (Reuters, ANI)
13. **Johannesburg — Rate decision.** South Africa holds rates as
    rand slides. SARB holds repo rate at 7.25%; rand falls to lowest
    of the year. (Reuters, PropFlow360)
14. **Yemen — Rocket strike.** Houthi rocket kills 53 soldiers in
    Yemen. 53 soldiers killed in Yemen. (Reuters)
15. **Auction — Van Gogh record.** Van Gogh sells for record
    $190.4m. Auction record for the artist. (BBC)
16. **Saudi Arabia — All clear.** Saudi: danger has passed in south.
    Alerts lifted in three southern cities. (Reuters)
17. **Mpigi — Car plant.** Two presidents open Uganda car plant.
    Museveni and Samia launch plant; Double Q–Sinotruk assembly in
    Mpigi. (Kampala Post, NBS TV)
18. **Antalya — COP31 draft.** COP31 draft drops fossil-fuel
    language. New draft omits fossil phase-out; Antalya text admits
    1.5°C may pass. (Reuters)

## Briefs (21)

19. Berlin — The Coalition of the Willing meets. Witkoff and Kushner
    attend.
20. Saada — The Saudi coalition intercepts a Houthi missile. The
    launcher is destroyed.
21. Tokyo — India and Japan hold 2+2 defence talks. The ministers
    meet in the capital.
22. Hormuz — A tanker is hit by a projectile. Oil steadies after the
    strike.
23. Malib — The Bayelsa head is hidden in weakness. Winds of 80 mph
    capsized her in seconds.
24. Shenzhen — Trump mentions ex-Nvidia boss Huang briefly in X
    talks. The talks are at the APEC summit.
25. Australia — The jobless rate jumps to 4.9%. It is the highest
    since 2021.
26. London — The UK leasehold Bill enters Parliament. Rents are
    capped at £250.
27. Washington — US senators warn AI cyber threats are outpacing
    defences.
28. US — Microsoft is in talks to sell AI services to ByteDance.
29. Shenzhen — Japan PM Takaichi holds talks with Putin. Both leaders
    are at the APEC summit.
30. New Delhi — Congress targets the Modi government over inflation.
31. Kuala Lumpur — UNHCR halts refugee registration in Malaysia.
32. Global — Bitcoin slips below $63,000. It is down 2.7%.
33. Tokyo — Japan machinery orders dip 0.3%. The figures are for
    September.
34. Brussels — The EU delays methane rules by two years.
35. Tokyo — Stocks rise. The Anthropic IPO lifts the AI mood.
36. Taiwan — Taiwan drafts a transnational repression law. The bill
    targets coercion abroad.
37. Finland — The first nuclear waste store is approved. It is the
    world's first permanent repository.
38. Wellington — Bumrah strikes twice at lunch. The 1st Test is at
    Basin Reserve.
39. Dakar — Senegal holds Armed Forces Day in Dakar. President Faye
    leads the ceremony. (ECOWAS)

## Regions

EUROPE 11 · THE AMERICAS 3 · ASIA-PACIFIC 9 · MIDEAST 6 · AFRICA 3 ·
OCEANIA 2 · WORLD 5 = 39.

## How the image was made

`compose_final.py` (Python 3 + Pillow, written fresh in the build
session) composes `entry.png` (1024×1024) from the illustration
assets in `assets/` plus text rendered from the verified news strings
above. The four hero illustrations were generated in an earlier build
session from my own prompts, and the 14 card illustrations were
generated in this session in the same style — no copied artwork, no
photos, no text inside the illustrations; every word on the page is
drawn by `compose_final.py`. `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory; it runs twice in
grading and writes identical bytes both times. Research cutoff:
19 Nov 2026 evening WIB; Africa + COP31 stories verified from named
sources the same evening.
