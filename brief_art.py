#!/usr/bin/env python3
"""Mini illustrations for the 10 briefs (4-13) of news-image-20261121.

Each function draws one flat, high-contrast scene into a strip box
(x, y, w, h) and stamps the brief's big number/keyword in bold white
or yellow at the lower left. Style follows the top-20 winners: a small
scene that reads at a glance, plus one big number that anchors the cell.

Drawn with PIL ImageDraw only. Imported by generate.py (the local build
tool); the shipped main.py only copies the finished entry.png.
"""
import math

RED = (176, 30, 36)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 120)
ORANGE = (255, 150, 40)
DARK = (12, 20, 34)
NIGHT = (18, 18, 30)
BLUE = (31, 78, 121)
GREEN = (30, 107, 58)


def _burst(d, cx, cy, r, color=ORANGE):
    """8-spoke explosion starburst with a bright core."""
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
               fill=color, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 210, 90))


def _stars(d, x, y, w, h, n=14, seed=7):
    """Deterministic starfield (no randomness)."""
    for i in range(n):
        sx = x + (i * 37 + seed * 11) % w
        sy = y + (i * 23 + seed * 5) % h
        r = 1 if i % 3 else 2
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)


def _bignum(d, x, y, text, size=19, fill=WHITE):
    """Big bold number/keyword at the lower left of the strip."""
    from PIL import ImageFont
    f = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    d.text((x + 6, y), text, font=f, fill=fill)


def art_planet(d, x, y, w, h):
    """#4 BepiColombo: dark space, orange Mercury, white spacecraft."""
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    _stars(d, x, y, w, h)
    d.ellipse([x + w - 52, y + 4, x + w - 12, y + h - 12], fill=(205, 120, 50))
    d.ellipse([x + w - 44, y + 10, x + w - 34, y + 20], fill=(160, 85, 35))
    d.rectangle([x + 72, y + 14, x + 96, y + 22], fill=WHITE)
    d.rectangle([x + 60, y + 17, x + 72, y + 19], fill=(150, 150, 160))
    d.rectangle([x + 96, y + 17, x + 108, y + 19], fill=(150, 150, 160))
    _bignum(d, x, y + h - 26, "8 YRS", fill=YELLOW)


def art_flame(d, x, y, w, h):
    """#5 Kyiv strikes: night skyline, two orange blasts."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for bx, bw, bh in [(x + 8, 26, 18), (x + 44, 34, 24), (x + 92, 30, 14),
                       (x + 132, 38, 26), (x + 168, 22, 16)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(8, 8, 16))
        d.rectangle([bx + 4, y + h - bh - 4, bx + 8, y + h - bh],
                    fill=(255, 220, 120))
    _burst(d, x + 118, y + 12, 11)
    _burst(d, x + 158, y + 16, 9)
    _bignum(d, x, y + h - 26, "12 KILLED")


def art_shield(d, x, y, w, h):
    """#6 Riyadh intercepts: missile trails, orange intercept flashes."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for t in range(0, 9):
        px = x + 20 + t * 16
        py = y + 30 - t * 2
        d.ellipse([px, py, px + 3, py + 3], fill=WHITE)
    for t in range(0, 7):
        px = x + 60 + t * 14
        py = y + 8 + t * 3
        d.ellipse([px, py, px + 3, py + 3], fill=WHITE)
    _burst(d, x + 150, y + 12, 10)
    _burst(d, x + 125, y + 30, 8)
    d.polygon([(x + w - 26, y + 6), (x + w - 8, y + 10),
               (x + w - 8, y + 18), (x + w - 26, y + 26), (x + w - 30, y + 16)],
              fill=BLUE)
    _bignum(d, x, y + h - 26, "3 DOWN", fill=YELLOW)


def art_cuffs(d, x, y, w, h):
    """#7 Chapo captured: handcuffs + red FBI-style badge."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 30, 30))
    d.ellipse([x + 104, y + 8, x + 126, y + 30], outline=WHITE, width=3)
    d.ellipse([x + 130, y + 8, x + 152, y + 30], outline=WHITE, width=3)
    d.line([(x + 126, y + 19), (x + 130, y + 19)], fill=WHITE, width=2)
    d.rectangle([x + 158, y + 6, x + 186, y + 32], fill=RED)
    from PIL import ImageFont
    _fbi = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    d.text((x + 166, y + 12), "FBI", font=_fbi, fill=WHITE)
    _bignum(d, x, y + h - 26, "CAPTURED", size=17)


def art_chip(d, x, y, w, h):
    """#8 AI chips: dark board, green circuit traces, gold chip."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 18))
    for gy in (y + 8, y + 20, y + 32):
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=(40, 120, 70), width=1)
    for gx in (x + 30, x + 90, x + 150):
        d.line([(gx, y + 4), (gx, y + h - 4)], fill=(40, 120, 70), width=1)
    d.rectangle([x + w - 56, y + 6, x + w - 16, y + h - 8], fill=INK)
    d.rectangle([x + w - 48, y + 14, x + w - 24, y + h - 16],
                outline=YELLOW, width=1)
    _bignum(d, x, y + h - 26, "900,000", size=18, fill=YELLOW)


def art_euro(d, x, y, w, h):
    """#9 EU arms: blue field, gold euro sign, ring of stars."""
    d.rectangle([x, y, x + w, y + h], fill=BLUE)
    for k in range(8):
        a = k * math.pi / 4
        sx = x + w - 34 + int(16 * math.cos(a))
        sy = y + h // 2 + int(12 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=YELLOW)
    d.ellipse([x + 68, y + 6, x + 108, y + h - 6], fill=(20, 60, 100))
    from PIL import ImageFont
    f = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    d.text((x + 78, y + 7), "€", font=f, fill=YELLOW)
    _bignum(d, x, y + h - 26, "€1bn", fill=YELLOW)


def art_magnifier(d, x, y, w, h):
    """#10 Denmark plot: magnifier over a foiled figure, red X."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.ellipse([x + 96, y + 4, x + 142, y + h - 10], outline=INK, width=4)
    d.line([(x + 136, y + h - 14), (x + 160, y + h - 2)], fill=INK, width=4)
    d.ellipse([x + 112, y + 12, x + 126, y + 26], fill=INK)
    d.rectangle([x + 106, y + 26, x + 132, y + h - 12], fill=INK)
    d.line([(x + 150, y + 8), (x + 178, y + 32)], fill=RED, width=4)
    d.line([(x + 178, y + 8), (x + 150, y + 32)], fill=RED, width=4)
    _bignum(d, x, y + h - 26, "FOILED", fill=RED)


def art_flag(d, x, y, w, h):
    """#11 Russell P1: checkered flag + track curve under lights."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 20))
    for r in range(2):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle([x + 96 + c * 12, y + 6 + r * 12,
                             x + 108 + c * 12, y + 18 + r * 12], fill=WHITE)
    d.line([(x + 4, y + h - 3), (x + w - 4, y + h - 3)], fill=YELLOW, width=2)
    for lx in (x + 20, x + 70, x + 130):
        d.ellipse([lx, y + 6, lx + 4, y + 10], fill=YELLOW)
    _bignum(d, x, y + h - 26, "P1", size=22, fill=YELLOW)


def art_cricket(d, x, y, w, h):
    """#12 Rahul 136: green pitch, bat, red ball, stumps."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 62))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 80, 44))
    d.polygon([(x + 108, y + 6), (x + 116, y + 10), (x + 128, y + 26),
               (x + 122, y + 32), (x + 110, y + 18)], fill=(200, 160, 100))
    d.ellipse([x + 140, y + 10, x + 154, y + 24], fill=RED)
    for sx in (x + 168, x + 174, x + 180):
        d.rectangle([sx, y + 22, sx + 3, y + 36], fill=YELLOW)
    _bignum(d, x, y + h - 26, "136")


def art_star(d, x, y, w, h):
    """#13 Rutte Warsaw: blue sky, NATO star, plane silhouette."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 60, 110))
    cx, cy = x + w - 40, y + h // 2
    d.polygon([(cx, cy - 14), (cx + 3, cy - 3), (cx + 14, cy),
               (cx + 3, cy + 3), (cx, cy + 14), (cx - 3, cy + 3),
               (cx - 14, cy), (cx - 3, cy - 3)], fill=WHITE)
    d.polygon([(x + 96, y + 16), (x + 130, y + 20), (x + 150, y + 14),
               (x + 128, y + 24), (x + 96, y + 22)], fill=(10, 20, 40))
    d.rectangle([x + 100, y + 10, x + 106, y + 16], fill=(10, 20, 40))
    _bignum(d, x, y + h - 26, "WARSAW", size=17)


ART = {
    "planet": art_planet,
    "flame": art_flame,
    "shield": art_shield,
    "cuffs": art_cuffs,
    "chip": art_chip,
    "euro": art_euro,
    "magnifier": art_magnifier,
    "flag": art_flag,
    "cricket": art_cricket,
    "star": art_star,
}
