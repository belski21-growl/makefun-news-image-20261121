#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261121 — ROUND 2 (LOCAL BUILD TOOL ONLY).

Draws a dense newspaper front page with PIL + DejaVu fonts, following the
top-10 winning template ("The World in One Day"): giant date headline,
UTC timeline, 6-stat strip, region bar, 3 illustrated leads, 10 briefs,
"ALSO ON SATURDAY" list, world map with numbered pins, DATE CHECK box,
per-story sources + verification chips. This script is NOT run by the grader:
the shipped main.py only copies the finished entry.png.
Run: python3 generate.py  ->  writes entry.png next to itself.
"""
from PIL import Image, ImageDraw, ImageFont

import art_scenes  # Storytelling scenes for leads + briefs (rebuild r3c).
import art_polish_r3d  # Poles r3d: CONTINENTS_V2, strip v2, helper depth.

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (176, 30, 36)
RULE = (201, 191, 168)
PANEL = (255, 253, 246)
MUTED = (90, 84, 70)
MAPLAND = (222, 205, 170)
MAPSEA = (238, 232, 218)
GREEN = (30, 107, 58)
BLUE = (31, 78, 121)

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
REGION_COUNTS = [("EUROPE", 12), ("ASIA", 3), ("MIDDLE EAST", 4),
                 ("AFRICA", 3), ("AMERICAS", 11), ("OCEANIA", 1), ("GLOBAL", 2)]

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
    ("2 tankers", "hit off Khasab (UKMTO)"),
    ("~900,000", "AI chips cleared for China"),
    ("€1bn", "EU arms aid for Ukraine"),
    ("8 yrs", "BepiColombo's voyage"),
]

# (kicker incl. source, headline, deck, status) — 3 illustrated leads.
# Lead order follows the top-20 consensus: Iran-Bahrain, Peru, COP31.
LEADS = [
    ("MANAMA, BAHRAIN  •  IRAN WAR  •  AP",
     "Iran strikes Bahrain bases; tankers hit off Oman",
     "IRGC says it hit US radar at two bases; Bahrain says a plant "
     "burned. UKMTO: two tankers hit off Khasab.",
     "CONFIRMED"),
    ("JUNIN, PERU  •  USGS",
     "M6.7 quake shakes Peru, felt in Lima",
     "00:09 UTC Saturday, near Carhuamayo; no deaths reported, "
     "homes cracked.",
     "OFFICIAL"),
    ("ANTALYA, TÜRKIYE  •  CLIMATE  •  AP",
     "COP31 climate talks run into overtime",
     "Third draft due Saturday; fossil-fuel wording dropped. Talks run "
     "past a 12-day deadline.",
     "CONFIRMED"),
]

# (icon, region, kicker incl. source, headline, deck, status) — 10 briefs 4-13.
BRIEFS = [
    ("planet", "GLOBAL", "MERCURY  •  ESA",
     "BepiColombo enters Mercury orbit",
     "Eight-year voyage ends 19:24 CET; science starts April 2027.",
     "OFFICIAL"),
    ("flame", "EUROPE", "KYIV  •  REUTERS",
     "Overnight strikes kill 12, hurt 42 in Ukraine",
     "Double-tap hit on Kryvyi Rih; Kyiv bridges damaged in mass attack.",
     "CONFIRMED"),
    ("shield", "MIDDLE EAST", "RIYADH  •  REUTERS",
     "Saudi jets down three Houthi missiles",
     "Intercepted over Riyadh; coalition strikes Hodeidah.",
     "OFFICIAL"),
    ("cuffs", "AMERICAS", "GUASAVE, MEXICO  •  AP",
     "Mexico captures cartel boss 'El Chapo Isidro'",
     "FBI most-wanted seized in raid; 11 killed as cartel fights back.",
     "OFFICIAL"),
    ("chip", "AMERICAS", "WASHINGTON  •  REUTERS",
     "US cleared ~900,000 AI chips for China",
     "House panel: 879,000 Nvidia, AMD chips approved in six months.",
     "CONFIRMED"),
    ("euro", "EUROPE", "BRUSSELS  •  EU COUNCIL",
     "EU approves €1bn in arms for Ukraine",
     "Joint buys of drones, air defence; delivery by end of 2027.",
     "OFFICIAL"),
    ("magnifier", "EUROPE", "COPENHAGEN  •  BBC",
     "Denmark says it foiled a Russian murder plot",
     "Copenhagen says plot to kill a US-Ukrainian rapper failed.",
     "CONFIRMED"),
    ("flag", "AMERICAS", "LAS VEGAS  •  BBC",
     "Russell fastest in Las Vegas practice",
     "Verstappen sent to stewards after contact in final session.",
     "OFFICIAL"),
    ("cricket", "ASIA", "WELLINGTON  •  AP",
     "Rahul hits 136 as India lead by 118",
     "KL Rahul's 13th Test hundred; India 486/4 at stumps on day three.",
     "CONFIRMED"),
    ("star", "EUROPE", "WARSAW  •  NATO  •  AP",
     "Rutte flies to Warsaw after Poland missile scare",
     "NATO chief meets Tusk on Saturday; Poland seeks more air defences.",
     "OFFICIAL"),
]

# ALSO ON SATURDAY — 23 more stories (14-36), one line each.
ALSO_ON = [
    "Estonia closes border with Russia (BBC)",
    "Portugal's public sector walks out (BBC)",
    "France, Germany strike ECB deal (BBC)",
    "Lufthansa to cut 1,000 jobs (BBC)",
    "Iraq moves against Iran-backed militia (Reuters)",
    "Nikhil Gupta jailed 19 years in US murder plot (BBC)",
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
    "England beat All Blacks 37-12, a record win (BBC)",
    "Cricket Australia backs Cummins as captain (AFP)",
    "Iran war nears its ninth month (Reuters)",
    "Alcaraz beats Cobolli 6-4, 6-1 in Turin (BBC)",
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

# "THE DAY IN UTC" — timed events, Saturday 21 November 2026 (from top-10
# consensus: rank 1 / rank 10 timelines).
UTC_EVENTS = [
    ("00:09", "Peru quake"),
    ("05:00", "Tanker hit off Khasab"),
    ("09:42", "Banda Sea M6.8"),
    ("12:00", "EU-Indonesia pact"),
    ("18:24", "BepiColombo burn"),
    ("21:00", "COP31 resumes"),
]

# World map: rough continent polygons in fraction coords (x 0-1, y 0-1).
CONTINENTS = [
    [(0.02, 0.10), (0.06, 0.04), (0.14, 0.02), (0.22, 0.04), (0.28, 0.08),
     (0.30, 0.14), (0.28, 0.20), (0.30, 0.26), (0.26, 0.28), (0.22, 0.32),
     (0.19, 0.38), (0.16, 0.44), (0.13, 0.42), (0.12, 0.34), (0.08, 0.28),
     (0.04, 0.22), (0.01, 0.16)],  # North America (Alaska, Hudson Bay, Mexico)
    [(0.32, 0.03), (0.38, 0.02), (0.40, 0.08), (0.35, 0.12), (0.31, 0.08)],  # Greenland
    [(0.25, 0.50), (0.30, 0.48), (0.35, 0.50), (0.38, 0.56), (0.36, 0.66),
     (0.33, 0.78), (0.30, 0.90), (0.27, 0.82), (0.25, 0.68), (0.23, 0.58)],  # South America
    [(0.45, 0.10), (0.48, 0.05), (0.52, 0.04), (0.55, 0.08), (0.58, 0.12),
     (0.56, 0.16), (0.54, 0.20), (0.55, 0.24), (0.52, 0.28), (0.50, 0.24),
     (0.48, 0.20), (0.45, 0.16)],  # Europe
    [(0.44, 0.32), (0.50, 0.28), (0.56, 0.30), (0.60, 0.36), (0.59, 0.46),
     (0.57, 0.58), (0.54, 0.70), (0.52, 0.78), (0.50, 0.70), (0.48, 0.58),
     (0.45, 0.46), (0.42, 0.38)],  # Africa
    [(0.60, 0.62), (0.62, 0.64), (0.61, 0.70), (0.59, 0.66)],  # Madagascar
    [(0.58, 0.06), (0.68, 0.02), (0.80, 0.02), (0.92, 0.06), (0.97, 0.12),
     (0.94, 0.20), (0.88, 0.26), (0.84, 0.32), (0.80, 0.38), (0.76, 0.44),
     (0.74, 0.48), (0.72, 0.42), (0.70, 0.34), (0.68, 0.28), (0.64, 0.22),
     (0.60, 0.16), (0.58, 0.12)],  # Asia (India peninsula dip at 0.74,0.48)
    [(0.80, 0.42), (0.83, 0.40), (0.85, 0.44), (0.82, 0.46)],  # SE Asia islands
    [(0.90, 0.16), (0.92, 0.18), (0.91, 0.24), (0.89, 0.20)],  # Japan
    [(0.79, 0.70), (0.83, 0.66), (0.88, 0.67), (0.91, 0.72), (0.90, 0.78),
     (0.86, 0.82), (0.82, 0.80), (0.79, 0.75)],  # Australia
    [(0.455, 0.08), (0.468, 0.10), (0.46, 0.14)],  # Britain
    [(0.935, 0.81), (0.968, 0.80), (0.982, 0.86), (0.955, 0.90), (0.935, 0.88)],  # New Zealand
]
# (story number, lon, lat, dx, dy) — dx/dy nudge the pin so the Europe
# cluster does not collide. Story 4 (Mercury) is drawn in orbit, top right.
PINS = [
    (1, 50.6, 26.2, 12, -10), (2, -76.0, -11.0, 0, 0), (3, 30.7, 36.9, 0, -6),
    (5, 30.5, 50.4, 9, 0), (6, 46.7, 24.7, 0, 0), (7, -108.5, 25.6, 0, 0),
    (8, -77.0, 38.9, 0, 0), (9, 4.35, 50.85, -7, 2), (10, 12.57, 55.68, -4, -7),
    (11, -115.1, 36.2, 0, 0), (12, 174.8, -41.3, 0, -6), (13, 21.0, 52.2, 2, -2),
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


# ---- Lead scenes (322 x 58): layered storytelling scenes ----------
# Rebuild r3c: the art lives in art_scenes.py (scene_gulf, scene_quake,
# scene_cop31) — Gulf map scene with tankers + KHASAB, quake cross-section
# with epicentre rings, COP31 data scene with 9-21 grid + '+1 DAY' + 1.5C.
LEAD_ART = art_scenes.LEAD_SCENES


def chip(d, x, y, text):
    """Small verification chip: green CONFIRMED, blue OFFICIAL. Returns width."""
    color = GREEN if text == "CONFIRMED" else BLUE
    f = SANS_B(8)
    w = int(d.textlength(text, font=f)) + 10
    d.rectangle([x, y, x + w, y + 13], fill=color)
    d.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return w


def chip_small(d, right, y, text):
    """Compact verification chip (10px tall), right-aligned to `right`."""
    color = GREEN if text == "CONFIRMED" else BLUE
    f = SANS_B(7)
    w = int(d.textlength(text, font=f)) + 8
    d.rectangle([right - w, y, right, y + 10], fill=color)
    d.text((right - w + 4, y + 1), text, font=f, fill=(255, 255, 255))
    return w


# ---- Brief strips (190 x 40): mini-SCENES, not icons ----------------
# Rebuild r3c: the strips live in art_scenes.py (STRIPS dict) — each strip
# is a layered scene (gradient sky -> objects -> big number), e.g. satellite
# with blue solar panels, layered flames, jet silhouette, F1 car, bat+ball.
# (brief_art.py keeps the old flat strips for reference; not imported.)


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
    sub = ("Iran strikes Bahrain bases  •  M6.7 quake shakes Peru  •  "
           "COP31 runs into overtime")
    sf = SANS(13)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 92), sub, font=sf, fill=MUTED)
    d.rectangle([18, 110, 1006, 112], fill=RED)

    # ---- THE DAY IN UTC timeline -------------------------------------------
    ty = 118
    d.text((18, ty), "THE DAY IN UTC", font=SANS_B(11), fill=INK)
    tl_x0, tl_x1 = 150, 1006
    tl_y = ty + 16
    d.line([tl_x0, tl_y, tl_x1, tl_y], fill=RULE, width=2)
    n_ev = len(UTC_EVENTS)
    for i, (t, label) in enumerate(UTC_EVENTS):
        cx = tl_x0 + int(i * (tl_x1 - tl_x0) / (n_ev - 1))
        d.ellipse([cx - 4, tl_y - 4, cx + 4, tl_y + 4], fill=RED)
        # Time (bold red) + label (regular) on ONE line above the dots,
        # centred on the dot, so nothing collides with the stat strip.
        tf, lf = SANS_B(10), SANS(9)
        tw = d.textlength(t + " ", font=tf)
        lw = d.textlength(label, font=lf)
        sx = min(max(cx - (tw + lw) / 2, tl_x0), tl_x1 - (tw + lw))
        d.text((sx, ty - 1), t + " ", font=tf, fill=RED)
        d.text((sx + tw, ty), label, font=lf, fill=INK)

    # ---- Stat strip: 6 big numbers ---------------------------------------
    sy = 148
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
    ry = 204
    x = 18
    rf = SANS_B(11)
    for name, count in REGION_COUNTS:
        d.rectangle([x, ry, x + 12, ry + 12], fill=REGION_COLORS[name])
        label = "%s %d" % (name, count)
        d.text((x + 17, ry - 1), label, font=rf, fill=INK)
        x += 17 + int(d.textlength(label, font=rf)) + 24
    d.rectangle([18, 224, 1006, 226], fill=INK)

    # ---- 3 illustrated leads ----------------------------------------------
    ly, lh = 230, 154
    lw = 322
    for i, (kicker, head, deck, status) in enumerate(LEADS):
        x = 18 + i * (lw + 10)
        LEAD_ART[i](d, x, ly, lw, 58)
        d.text((x, ly + 64), kicker, font=SANS_B(11), fill=RED)
        kw = d.textlength(kicker, font=SANS_B(11))
        chip(d, x + kw + 8, ly + 63, status)
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
    d.rectangle([18, 392, 1006, 394], fill=INK)

    # ---- 10 illustrated briefs, 5 x 2 --------------------------------------
    # Each cell: a 40px mini-illustration strip (brief_art) on top — the
    # top-20 pattern (rank 1/2: every brief is an illustrated panel with
    # a big number) — then number + kicker + chip, headline, deck.
    bx0, by0 = 18, 402
    cw2, ch2, gx2, gy2 = 190, 120, 9, 8
    for idx, (icon, region, kicker, head, deck, status) in enumerate(BRIEFS):
        row, col = divmod(idx, 5)
        x = bx0 + col * (cw2 + gx2)
        y = by0 + row * (ch2 + gy2)
        # Mini illustration strip (full cell width, 40px tall).
        # Poles r3d: strip #6 (shield) + #11 (flag) pakai versi v2
        # (jet cerah + starburst pindah, F1 beroda); sisanya r3c.
        strip_fn = art_polish_r3d.STRIPS_V2.get(
            icon, art_scenes.STRIPS[icon])
        strip_fn(d, x, y, cw2, 40)
        # Region-coloured left border runs the text area.
        d.rectangle([x, y + 40, x + 3, y + ch2 - 4], fill=REGION_COLORS[region])
        num = str(idx + 4)
        nf = SANS_B(11)
        d.text((x + 6, y + 44), num, font=nf, fill=RED)
        kw2 = d.textlength(num, font=nf)
        d.text((x + 10 + kw2, y + 45), kicker, font=SANS_B(9), fill=MUTED)
        chip_small(d, x + cw2 - 6, y + 57, status)
        hf = SANS_B(12)
        hlines = fit_lines(d, head, hf, cw2 - 6, 2, tag="brief%d-head" % (idx + 4))
        hy = y + 69
        for ln in hlines:
            d.text((x + 6, hy), ln, font=hf, fill=INK)
            hy += 14
        df3 = SANS(10)
        dlines = fit_lines(d, deck, df3, cw2 - 6, 2, tag="brief%d-deck" % (idx + 4))
        dy = hy + 1
        for ln in dlines:
            d.text((x + 6, dy), ln, font=df3, fill=MUTED)
            dy += 12
    d.rectangle([18, 658, 1006, 660], fill=INK)

    # ---- ALSO ON SATURDAY: 23 more stories, 2 columns --------------------
    ay = 668
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

    # ---- DATE CHECK as a compact horizontal band (top-20 pattern: rank 1/2
    # use a 2-line strip, not a tall box — the freed ~90px pays for the
    # taller illustrated brief grid above). -------------------------------
    dx0, dy0 = 18, 892
    d.rectangle([dx0, dy0, dx0 + 638, dy0 + 88], fill=(233, 226, 208),
                outline=RED, width=2)
    d.text((dx0 + 12, dy0 + 6), "DATE CHECK — WHAT WE LEFT OUT",
           font=SANS_B(12), fill=RED)
    dc_items = ";  ".join("× %s (%s)" % (s, w) for s, w in DATE_CHECK)
    dc_lines = fit_lines(d, "Not Saturday news: " + dc_items, SANS(10),
                         638 - 24, 3, tag="datecheck")
    yy = dy0 + 24
    for ln in dc_lines:
        d.text((dx0 + 12, yy), ln, font=SANS(10), fill=INK)
        yy += 13
    # "Not yet" row + verification legend (top-20 pattern: rank 1/5).
    d.text((dx0 + 12, dy0 + 63), "Not yet: ", font=SANS_B(10), fill=RED)
    d.text((dx0 + 12 + int(d.textlength("Not yet: ", font=SANS_B(10))),
            dy0 + 63),
           "COP31 final text  •  Las Vegas GP result (Sun 22 Nov)",
           font=SANS(10), fill=INK)
    d.text((dx0 + 12, dy0 + 76),
           "HOW WE CHECKED:  CONFIRMED = 2+ outlets  •  OFFICIAL = official source  •  REPORTED = single source",
           font=SANS(9), fill=MUTED)

    # ---- World map with numbered pins (right column) -----------------------
    mx0, my0, mw, mh = 668, 668, 338, 216
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=PANEL, outline=RULE, width=1)
    d.text((mx0 + 10, my0 + 8), "WHERE IT HAPPENED — PINS 1–13",
           font=SANS_B(12), fill=INK)
    map_x, map_y, map_w, map_h = mx0 + 8, my0 + 30, mw - 16, 150
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAPSEA)
    for poly in art_polish_r3d.CONTINENTS_V2:
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
    d.text((mx0 + 10, my0 + 190),
           "Pins 1–13 mark the drawn stories. 4 is in orbit:",
           font=SANS(10), fill=MUTED)
    d.text((mx0 + 10, my0 + 204),
           "BepiColombo at Mercury.",
           font=SANS(10), fill=MUTED)

    # ---- Honesty note + sources (right column, below map) ------------------
    hy = 892
    d.text((mx0, hy), "OUR PROMISE", font=SANS_B(11), fill=RED)
    promise = ("Every story here happened, or was first reported, on Saturday "
               "21 November 2026 in at least one time zone. Claims are "
               "attributed; forecasts are flagged. Original drawings.")
    plines = fit_lines(d, promise, SANS(10), mw, 5, tag="promise")
    yy = hy + 18
    for ln in plines:
        d.text((mx0, yy), ln, font=SANS(10), fill=INK)
        yy += 13
    yy += 6
    d.text((mx0, yy), "SOURCES", font=SANS_B(11), fill=RED)
    yy += 16
    src = "BBC, Reuters, AP, AFP, ESA, USGS, IMD, EU Council."
    for ln in fit_lines(d, src, SANS(10), mw, 1, tag="sources"):
        d.text((mx0, yy), ln, font=SANS(10), fill=INK)
        yy += 13

    # ---- Footer ------------------------------------------------------------
    d.rectangle([18, 1000, 1006, 1002], fill=INK)
    foot = "THE WORLD IN ONE DAY  •  SATURDAY 21 NOVEMBER 2026  •  ONE DAY, EVERY CONTINENT"
    ff = SANS_B(11)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1008), foot, font=ff, fill=MUTED)

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
