#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261121 — ROUND 2 (LOCAL BUILD TOOL ONLY).

Draws a dense newspaper front page with PIL + DejaVu fonts, following the
top-10 winning template ("The World in One Day"): giant date headline,
6-stat strip, region bar, 3 illustrated leads, 10 illustrated briefs,
"ALSO ON SATURDAY" list, world map with numbered pins, DATE CHECK box,
per-story sources. This script is NOT run by the grader: the shipped
main.py only copies the finished entry.png.
Run: python3 generate.py  ->  writes entry.png next to itself.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (176, 30, 36)
RULE = (201, 191, 168)
PANEL = (255, 253, 246)
MUTED = (90, 84, 70)
MAPLAND = (122, 140, 158)
MAPSEA = (233, 238, 240)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "ASIA": (176, 110, 0),
    "MIDDLE EAST": (150, 60, 60),
    "AFRICA": (30, 107, 58),
    "AMERICAS": (107, 45, 122),
    "OCEANIA": (0, 120, 130),
    "GLOBAL": (90, 84, 70),
}
# Story counts per region (36 stories: 3 leads + 10 briefs + 23 ALSO ON).
REGION_COUNTS = [("EUROPE", 13), ("ASIA", 4), ("MIDDLE EAST", 3),
                 ("AFRICA", 3), ("AMERICAS", 9), ("OCEANIA", 1), ("GLOBAL", 3)]

FDIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

# 6 big numbers for the stat strip: (number, label).
STATS = [
    ("M6.7", "Peru quake, 00:09 UTC"),
    ("12 killed", "42 hurt in Ukraine strikes"),
    ("372,000", "moved to safety in Odisha"),
    ("~900,000", "AI chips cleared for China"),
    ("€1bn", "EU arms aid for Ukraine"),
    ("8 yrs", "BepiColombo's voyage"),
]

# (kicker incl. source, headline, deck) — 3 illustrated leads.
LEADS = [
    ("WARSAW  •  NATO  •  AP",
     "Rutte flies to Warsaw after Poland missile scare",
     "NATO chief meets Tusk on Saturday; Poland seeks more air "
     "defences on its eastern flank."),
    ("JUNIN, PERU  •  USGS",
     "M6.7 quake shakes Peru, felt in Lima",
     "00:09 UTC Saturday, 30 km from Junin; no deaths reported, "
     "homes cracked."),
    ("KYIV  •  KRYVYI RIH  •  REUTERS",
     "Overnight strikes kill 12, hurt 42 in Ukraine",
     "Double-tap hit on Kryvyi Rih; Kyiv bridges damaged in mass "
     "attack."),
]

# (icon, kicker incl. source, headline, deck) — 10 illustrated briefs 4-13.
BRIEFS = [
    ("planet", "MERCURY  •  ESA",
     "BepiColombo enters Mercury orbit",
     "Eight-year voyage ends 19:24 CET; science starts April 2027."),
    ("globe", "ANTALYA  •  AP",
     "COP31 talks run into overtime",
     "Third draft due Saturday; fossil-fuel wording dropped."),
    ("shield", "RIYADH  •  REUTERS",
     "Saudi jets down three Houthi missiles",
     "Intercepted over Riyadh; coalition strikes Hodeidah."),
    ("cyclone", "ODISHA  •  IMD",
     "Akvan leaves Odisha unscathed",
     "372,000 moved to safety; zero deaths reported."),
    ("chip", "WASHINGTON  •  REUTERS",
     "US cleared ~900,000 AI chips for China",
     "House panel: 879,000 Nvidia, AMD chips approved in six months."),
    ("euro", "BRUSSELS  •  EU COUNCIL",
     "EU approves €1bn in arms for Ukraine",
     "Joint buys of drones, air defence; delivery by end of 2027."),
    ("magnifier", "COPENHAGEN  •  BBC",
     "Denmark says it foiled a Russian murder plot",
     "Copenhagen says plot to kill a US-Ukrainian rapper failed."),
    ("flag", "LAS VEGAS  •  BBC",
     "Russell fastest in Las Vegas practice",
     "Verstappen sent to stewards after contact in final session."),
    ("cricket", "GUWAHATI  •  AP",
     "India reach 239/1 vs New Zealand",
     "Rahul 93*, Padikkal 53* at lunch on day three of first Test."),
    ("tennis", "TURIN  •  BBC",
     "Alcaraz beats Cobolli 6-4, 6-1",
     "Perfect group stage at the ATP Finals in Turin."),
]

# ALSO ON SATURDAY — 23 more stories (14-36), one line each.
ALSO_ON = [
    "Estonia closes border with Russia (BBC)",
    "Portugal's public sector walks out (BBC)",
    "France, Germany strike ECB deal (BBC)",
    "Lufthansa to cut 1,000 jobs (BBC)",
    "Iraq moves against Iran-backed militia (Reuters)",
    "Man jailed 19 years over US murder plot (BBC)",
    "Nepal's new leader faces his India test (BBC)",
    "US opens Pacific deep-sea mining auction (Reuters)",
    "ANC fights to hold South Africa's big cities (BBC)",
    "Nearly 600 women killed in South Africa (BBC)",
    "Sudan war hits disabled children's schooling (BBC)",
    "Mamdani vows to close Rikers Island by 2032 (BBC)",
    "LA jury convicts Palisades Fire arsonist (BBC)",
    "Texas execution takes more than an hour (BBC)",
    "Trump: US flight systems 'ancient' but 'safe' (BBC)",
    "US declassifies more UFO footage (BBC)",
    "Kane out for months with ankle injury (BBC)",
    "Price beats Kotaskova to undisputed crown (BBC)",
    "Kim leads LPGA finale after ace (BBC)",
    "England target style win over All Blacks (BBC)",
    "AI maths claim sparks debate (BBC)",
    "Iran war nears its ninth month (Reuters)",
    "French police sentenced over Zecler beating (BBC)",
]

# DATE CHECK — big stories deliberately LEFT OUT (not Saturday news).
DATE_CHECK = [
    ("Russian missiles land in Poland", "Fri 20 Nov"),
    ("Wall Street enters correction", "Fri 20 Nov"),
    ("UK-EU food and youth deals", "Fri 20 Nov"),
    ("ICJ: Myanmar genocide ruling", "Thu 19 Nov"),
    ("Trump-Xi-Putin Shenzhen summit", "Thu 19 Nov"),
    ("Pancreatic-cancer pill results", "Fri 20 Nov"),
    ("GTA VI rollout", "19 Nov"),
]

# World map: rough continent polygons in fraction coords (x 0-1, y 0-1).
CONTINENTS = [
    [(0.02, 0.10), (0.10, 0.03), (0.20, 0.05), (0.28, 0.10), (0.30, 0.18),
     (0.24, 0.25), (0.20, 0.30), (0.16, 0.42), (0.12, 0.46), (0.08, 0.38),
     (0.04, 0.28), (0.01, 0.18)],  # North America
    [(0.32, 0.03), (0.38, 0.02), (0.40, 0.08), (0.35, 0.12), (0.31, 0.08)],  # Greenland
    [(0.24, 0.48), (0.30, 0.46), (0.34, 0.52), (0.32, 0.66), (0.28, 0.80),
     (0.25, 0.72), (0.22, 0.58)],  # South America
    [(0.47, 0.10), (0.55, 0.08), (0.58, 0.14), (0.55, 0.20), (0.50, 0.22),
     (0.47, 0.16)],  # Europe
    [(0.47, 0.28), (0.56, 0.26), (0.60, 0.32), (0.58, 0.48), (0.54, 0.60),
     (0.50, 0.52), (0.47, 0.38)],  # Africa
    [(0.58, 0.06), (0.75, 0.04), (0.90, 0.08), (0.97, 0.14), (0.92, 0.22),
     (0.85, 0.30), (0.80, 0.36), (0.76, 0.42), (0.72, 0.46), (0.70, 0.40),
     (0.68, 0.30), (0.62, 0.20), (0.58, 0.14)],  # Asia (India peninsula)
    [(0.80, 0.42), (0.83, 0.40), (0.85, 0.44), (0.82, 0.46)],  # SE Asia islands
    [(0.82, 0.62), (0.90, 0.60), (0.93, 0.66), (0.88, 0.72), (0.83, 0.68)],  # Australia
    [(0.455, 0.10), (0.468, 0.12), (0.46, 0.15)],  # Britain
    [(0.935, 0.81), (0.968, 0.80), (0.982, 0.86), (0.955, 0.90), (0.935, 0.88)],  # New Zealand
]
# (story number, lon, lat, dx, dy) — dx/dy nudge the pin so the Europe
# cluster does not collide. Story 4 (Mercury) is drawn in orbit, top right.
PINS = [
    (1, 21.0, 52.2, 2, -2), (2, -76.0, -11.0, 0, 0), (3, 30.5, 50.4, 9, 0),
    (5, 30.7, 36.9, 0, -6), (6, 46.7, 24.7, 0, 0), (7, 84.9, 19.3, 0, 0),
    (8, -77.0, 38.9, 0, 0), (9, 4.35, 50.85, -7, 2), (10, 12.57, 55.68, -4, -7),
    (11, -115.1, 36.2, 0, 0), (12, 174.8, -41.3, 0, -6), (13, 7.7, 45.1, 0, 7),
]

TRUNCATED = []


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, max_w, max_lines, tag=""):
    """Wrap to at most max_lines; record (never silently hide) truncation."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    TRUNCATED.append("%s: %r needs %d lines, max %d"
                     % (tag, text, len(lines), max_lines))
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + " ...", font=font) > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
    lines[-1] = lines[-1] + " ..."
    return lines


# ---- Flat illustrations for the 3 leads -----------------------------------
def draw_warsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 92))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(16, 28, 56))
    # Skyline silhouettes + Palace of Culture spire.
    heights = [26, 34, 20, 40, 28, 36, 24]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 2
        d.rectangle([bx, y + h - 22 - hh, bx + bw - 4, y + h - 22],
                    fill=(10, 18, 38))
        for wy in range(y + h - 22 - hh + 5, y + h - 26, 9):
            d.rectangle([bx + 4, wy, bx + 7, wy + 3], fill=(255, 214, 120))
    sx = x + w // 2 - 3
    d.polygon([(sx, y + 8), (sx + 6, y + 8), (sx + 3, y + h - 22 - 40)],
              fill=(10, 18, 38))
    # NATO compass star in a circle, top right.
    cx, cy, r = x + w - 26, y + 20, 13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy), (cx + 3, cy + 3),
               (cx, cy + 10), (cx - 3, cy + 3), (cx - 10, cy), (cx - 3, cy - 3)],
              fill=(255, 255, 255))


def draw_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    # Andes triangles.
    d.polygon([(x, y + h), (x + 70, y + 12), (x + 140, y + h)], fill=(150, 110, 70))
    d.polygon([(x + 110, y + h), (x + 200, y + 4), (x + 300, y + h)],
              fill=(120, 88, 54))
    d.polygon([(x + 185, y + 18), (x + 200, y + 4), (x + 215, y + 18)],
              fill=(245, 240, 225))
    # Ground + cracks.
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(176, 138, 88))
    d.line([(x + 40, y + h - 18), (x + 70, y + h - 8), (x + 95, y + h - 18),
            (x + 130, y + h - 6)], fill=(90, 60, 30), width=2)
    d.line([(x + 210, y + h - 18), (x + 240, y + h - 7), (x + 275, y + h - 18)],
           fill=(90, 60, 30), width=2)
    # Seismograph trace in red.
    pts = []
    import math
    for i in range(0, w + 1, 6):
        amp = 2 if i < w * 0.3 or i > w * 0.75 else 12
        yy = y + h // 2 + (amp * math.sin(i / 3.0) if i % 12 else -amp)
        pts.append((x + i, yy))
    d.line(pts, fill=RED, width=2)


def draw_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 36))
    # Skyline.
    heights = [22, 30, 18, 34, 26, 20, 32]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 2
        d.rectangle([bx, y + h - hh, bx + bw - 4, y + h], fill=(5, 8, 16))
        for wy in range(y + h - hh + 5, y + h - 4, 9):
            d.rectangle([bx + 4, wy, bx + 7, wy + 3], fill=(255, 214, 120))
    # Missile trail arc.
    d.arc([x + 30, y - 30, x + 240, y + 70], start=200, end=340,
          fill=(255, 255, 255), width=2)
    # Two orange explosion starbursts.
    for cx, cy, r in [(x + 70, y + 22, 12), (x + 250, y + 30, 14)]:
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                   fill=(255, 150, 40), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 210, 90))
    # Smoke.
    d.ellipse([x + 55, y + 30, x + 95, y + 48], fill=(90, 90, 100))
    d.ellipse([x + 235, y + 38, x + 275, y + 56], fill=(90, 90, 100))


LEAD_ART = [draw_warsaw, draw_quake, draw_kyiv]


# ---- Mini icons for briefs 4-13 (26x26 box) -------------------------------
def icon_planet(d, x, y):
    d.ellipse([x + 4, y + 4, x + 22, y + 22], fill=(205, 120, 50))
    d.ellipse([x + 8, y + 8, x + 13, y + 13], fill=(160, 85, 35))
    d.rectangle([x + 1, y + 11, x + 4, y + 15], fill=(120, 120, 130))
    d.rectangle([x + 22, y + 11, x + 25, y + 15], fill=(120, 120, 130))


def icon_globe(d, x, y):
    d.ellipse([x + 3, y + 3, x + 23, y + 23], fill=(31, 78, 121))
    d.polygon([(x + 8, y + 8), (x + 15, y + 7), (x + 18, y + 12), (x + 12, y + 15),
               (x + 8, y + 13)], fill=(60, 160, 90))
    d.polygon([(x + 10, y + 17), (x + 16, y + 17), (x + 14, y + 21), (x + 10, y + 20)],
              fill=(60, 160, 90))
    d.arc([x + 3, y + 3, x + 23, y + 23], start=300, end=60,
          fill=(255, 255, 255), width=1)


def icon_shield(d, x, y):
    d.polygon([(x + 13, y + 2), (x + 23, y + 6), (x + 23, y + 14), (x + 13, y + 24),
               (x + 3, y + 14), (x + 3, y + 6)], fill=(31, 78, 121))
    d.line([(x + 8, y + 13), (x + 12, y + 17), (x + 19, y + 9)],
           fill=(255, 255, 255), width=2)


def icon_cyclone(d, x, y):
    for r in (10, 7, 4):
        d.arc([x + 13 - r, y + 13 - r, x + 13 + r, y + 13 + r],
              start=20, end=300, fill=(31, 78, 121), width=2)
    d.ellipse([x + 11, y + 11, x + 15, y + 15], fill=RED)


def icon_chip(d, x, y):
    d.rectangle([x + 5, y + 5, x + 21, y + 21], fill=(17, 17, 17))
    d.rectangle([x + 9, y + 9, x + 17, y + 17], outline=(255, 214, 120), width=1)
    for i in range(3):
        d.line([(x + 8 + i * 5, y + 2), (x + 8 + i * 5, y + 5)], fill=(17, 17, 17), width=2)
        d.line([(x + 8 + i * 5, y + 21), (x + 8 + i * 5, y + 24)], fill=(17, 17, 17), width=2)
        d.line([(x + 2, y + 8 + i * 5), (x + 5, y + 8 + i * 5)], fill=(17, 17, 17), width=2)
        d.line([(x + 21, y + 8 + i * 5), (x + 24, y + 8 + i * 5)], fill=(17, 17, 17), width=2)


def icon_euro(d, x, y):
    d.ellipse([x + 2, y + 2, x + 24, y + 24], fill=(31, 78, 121))
    d.text((x + 7, y + 5), "€", font=SANS_B(14), fill=(255, 214, 120))


def icon_magnifier(d, x, y):
    d.ellipse([x + 3, y + 3, x + 17, y + 17], outline=(17, 17, 17), width=3)
    d.line([(x + 15, y + 15), (x + 23, y + 23)], fill=(17, 17, 17), width=3)


def icon_flag(d, x, y):
    d.line([(x + 5, y + 2), (x + 5, y + 24)], fill=(17, 17, 17), width=2)
    for r in range(2):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([x + 6 + c * 6, y + 3 + r * 6, x + 11 + c * 6, y + 8 + r * 6],
                            fill=(17, 17, 17))


def icon_cricket(d, x, y):
    d.ellipse([x + 13, y + 13, x + 23, y + 23], fill=(176, 30, 36))
    d.arc([x + 13, y + 13, x + 23, y + 23], start=40, end=140,
          fill=(255, 255, 255), width=1)
    d.polygon([(x + 3, y + 3), (x + 7, y + 5), (x + 13, y + 13), (x + 10, y + 16),
               (x + 5, y + 8)], fill=(200, 160, 100))


def icon_tennis(d, x, y):
    d.ellipse([x + 3, y + 3, x + 23, y + 23], fill=(170, 200, 60))
    d.arc([x + 3, y + 3, x + 23, y + 23], start=300, end=60,
          fill=(255, 255, 255), width=2)
    d.arc([x + 3, y + 3, x + 23, y + 23], start=120, end=240,
          fill=(255, 255, 255), width=2)


ICONS = {"planet": icon_planet, "globe": icon_globe, "shield": icon_shield,
         "cyclone": icon_cyclone, "chip": icon_chip, "euro": icon_euro,
         "magnifier": icon_magnifier, "flag": icon_flag,
         "cricket": icon_cricket, "tennis": icon_tennis}


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead: kicker + giant date headline + sub-headline ------------
    d.rectangle([18, 10, 1006, 15], fill=INK)
    kick = "THE WORLD IN ONE DAY"
    kf = SANS_B(15)
    kw = d.textlength(kick, font=kf)
    d.text(((W - kw) / 2, 22), kick, font=kf, fill=INK)
    date = "Saturday 21 November 2026"
    df = SERIF_B(46)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 40), date, font=df, fill=INK)
    sub = ("Rutte flies to Warsaw  •  M6.7 quake shakes Peru  •  "
           "Overnight strikes kill 12 in Ukraine")
    sf = SANS(13)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 92), sub, font=sf, fill=MUTED)
    d.rectangle([18, 110, 1006, 112], fill=RED)

    # ---- Stat strip: 6 big numbers ---------------------------------------
    sy = 120
    cw = 160
    for i, (num, label) in enumerate(STATS):
        x = 18 + i * (cw + 5)
        d.rectangle([x, sy - 4, x + cw, sy + 44], fill=PANEL, outline=RULE, width=1)
        nf = SERIF_B(26)
        nw = d.textlength(num, font=nf)
        d.text((x + (cw - nw) / 2, sy), num, font=nf, fill=RED)
        lf = SANS(10)
        lw = d.textlength(label, font=lf)
        d.text((x + (cw - lw) / 2, sy + 32), label, font=lf, fill=INK)

    # ---- Region bar --------------------------------------------------------
    ry = 176
    x = 18
    rf = SANS_B(11)
    for name, count in REGION_COUNTS:
        d.rectangle([x, ry, x + 12, ry + 12], fill=REGION_COLORS[name])
        label = "%s %d" % (name, count)
        d.text((x + 17, ry - 1), label, font=rf, fill=INK)
        x += 17 + int(d.textlength(label, font=rf)) + 24
    d.rectangle([18, 196, 1006, 198], fill=INK)

    # ---- 3 illustrated leads ----------------------------------------------
    ly, lh = 206, 154
    lw = 322
    for i, (kicker, head, deck) in enumerate(LEADS):
        x = 18 + i * (lw + 10)
        LEAD_ART[i](d, x, ly, lw, 58)
        d.text((x, ly + 64), kicker, font=SANS_B(11), fill=RED)
        hf = SERIF_B(19)
        hlines = fit_lines(d, head, hf, lw, 2, tag="lead%d-head" % (i + 1))
        hy = ly + 82
        for ln in hlines:
            d.text((x, hy), ln, font=hf, fill=INK)
            hy += 22
        df2 = SANS(12)
        dlines = fit_lines(d, deck, df2, lw, 2, tag="lead%d-deck" % (i + 1))
        dy = ly + 126
        for ln in dlines:
            d.text((x, dy), ln, font=df2, fill=MUTED)
            dy += 15
        if i < 2:
            d.line([x + lw + 5, ly, x + lw + 5, ly + lh], fill=RULE, width=1)
    d.rectangle([18, 368, 1006, 370], fill=INK)

    # ---- 10 illustrated briefs, 5 x 2 --------------------------------------
    bx0, by0 = 18, 378
    cw2, ch2, gx2, gy2 = 190, 88, 9, 8
    for idx, (icon, kicker, head, deck) in enumerate(BRIEFS):
        row, col = divmod(idx, 5)
        x = bx0 + col * (cw2 + gx2)
        y = by0 + row * (ch2 + gy2)
        num = str(idx + 4)
        nf = SANS_B(11)
        nw = d.textlength(num, font=nf)
        d.text((x, y + 1), num, font=nf, fill=RED)
        ICONS[icon](d, x + 16, y)
        d.text((x + 46, y + 6), kicker, font=SANS_B(9), fill=MUTED)
        hf = SANS_B(12)
        hlines = fit_lines(d, head, hf, cw2, 2, tag="brief%d-head" % (idx + 4))
        hy = y + 28
        for ln in hlines:
            d.text((x, hy), ln, font=hf, fill=INK)
            hy += 15
        df3 = SANS(10)
        dlines = fit_lines(d, deck, df3, cw2, 2, tag="brief%d-deck" % (idx + 4))
        dy = hy + 1
        for ln in dlines:
            d.text((x, dy), ln, font=df3, fill=MUTED)
            dy += 13
    d.rectangle([18, 562, 1006, 564], fill=INK)

    # ---- ALSO ON SATURDAY: 23 more stories, 2 columns --------------------
    ay = 572
    tf = SANS_B(13)
    d.text((18, ay), "ALSO ON SATURDAY — 23 MORE STORIES", font=tf, fill=INK)
    af = SANS(11)
    col_w = 312
    for idx, item in enumerate(ALSO_ON):
        col = 0 if idx < 12 else 1
        row = idx if idx < 12 else idx - 12
        x = 18 + col * (col_w + 14)
        y = ay + 26 + row * 16
        line = "%d  %s" % (idx + 14, item)
        lines = fit_lines(d, line, af, col_w, 1, tag="also%d" % (idx + 14))
        d.text((x, y), lines[0], font=af, fill=INK)

    # ---- DATE CHECK box (bottom left) --------------------------------------
    dx0, dy0 = 18, 800
    d.rectangle([dx0, dy0, dx0 + 638, dy0 + 156], fill=(233, 226, 208),
                outline=RED, width=2)
    d.text((dx0 + 12, dy0 + 8), "DATE CHECK — WHAT WE LEFT OUT",
           font=SANS_B(13), fill=RED)
    d.text((dx0 + 12, dy0 + 28),
           "These big stories are NOT from Saturday 21 November, so they are not in this paper:",
           font=SANS(10), fill=INK)
    cf = SANS(11)
    for i, (story, when) in enumerate(DATE_CHECK):
        y = dy0 + 50 + i * 14
        d.text((dx0 + 12, y), "×  %s" % story, font=cf, fill=INK)
        ww = d.textlength(when, font=SANS_B(11))
        d.text((dx0 + 638 - 12 - ww, y), when, font=SANS_B(11), fill=RED)

    # ---- World map with numbered pins (right column) -----------------------
    mx0, my0, mw, mh = 668, 572, 338, 238
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=PANEL, outline=RULE, width=1)
    d.text((mx0 + 10, my0 + 8), "WHERE IT HAPPENED — PINS 1–13",
           font=SANS_B(12), fill=INK)
    map_x, map_y, map_w, map_h = mx0 + 8, my0 + 30, mw - 16, 176
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAPSEA)
    for poly in CONTINENTS:
        pts = [(map_x + fx * map_w, map_y + fy * map_h) for fx, fy in poly]
        d.polygon(pts, fill=MAPLAND)
    # Mercury pin (story 4) in orbit, top right of the map.
    ox, oy = map_x + map_w - 24, map_y + 14
    d.ellipse([ox - 12, oy - 12, ox + 12, oy + 12], outline=(200, 120, 40), width=2)
    d.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=(205, 120, 50))
    d.ellipse([ox + 16, oy - 6, ox + 28, oy + 6], fill=RED)
    d.text((ox + 18, oy - 5), "4", font=SANS_B(8), fill=(255, 255, 255))
    pf = SANS_B(7)
    for num, lon, lat, ddx, ddy in PINS:
        px = map_x + (lon + 170) / 360.0 * map_w + ddx
        py = map_y + (75 - lat) / 130.0 * map_h + ddy
        fill = RED if num <= 3 else (31, 78, 121)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=fill,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=pf)
        d.text((px - tw / 2, py - 5), str(num), font=pf, fill=(255, 255, 255))
    d.text((mx0 + 10, my0 + 212),
           "Pins 1–13 mark the drawn stories. 4 is in orbit:",
           font=SANS(10), fill=MUTED)
    d.text((mx0 + 10, my0 + 226),
           "BepiColombo at Mercury.",
           font=SANS(10), fill=MUTED)

    # ---- Honesty note + sources (right column, below map) ------------------
    hy = 826
    d.text((mx0, hy), "OUR PROMISE", font=SANS_B(11), fill=RED)
    promise = ("Every story here happened, or was first reported, on Saturday "
               "21 November 2026 in at least one time zone. Claims are "
               "attributed; forecasts are flagged. Original drawings.")
    plines = fit_lines(d, promise, SANS(10), mw, 6, tag="promise")
    yy = hy + 18
    for ln in plines:
        d.text((mx0, yy), ln, font=SANS(10), fill=INK)
        yy += 13
    yy += 6
    d.text((mx0, yy), "SOURCES", font=SANS_B(11), fill=RED)
    yy += 16
    src = "BBC, Reuters, AP, AFP, ESA, USGS, IMD, EU Council."
    for ln in fit_lines(d, src, SANS(10), mw, 2, tag="sources"):
        d.text((mx0, yy), ln, font=SANS(10), fill=INK)
        yy += 13

    # ---- Footer ------------------------------------------------------------
    d.rectangle([18, 968, 1006, 970], fill=INK)
    foot = "THE WORLD IN ONE DAY  •  SATURDAY 21 NOVEMBER 2026  •  ONE DAY, EVERY CONTINENT"
    ff = SANS_B(11)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 978), foot, font=ff, fill=MUTED)

    return img


if __name__ == "__main__":
    import hashlib, os
    img = draw()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    print("size", img.size, "mode", img.mode)
    if TRUNCATED:
        print("TRUNCATION-RISK: %d items" % len(TRUNCATED))
        for t in TRUNCATED:
            print("  -", t)
    else:
        print("TRUNCATION-RISK: none")
