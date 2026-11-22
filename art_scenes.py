#!/usr/bin/env python3
"""Storytelling scenes for news-image-20261121 — REBUILD r3c.

Replaces the flat-icon art (generate.py draw_gulf/draw_quake/draw_cop31 +
brief_art.ART) with layered mini-SCENES, following the top 1/10/20 pattern
(studied directly, see top10-analysis.md "Studi ART top 1/10/20"):

- Every panel TELLS its story: ship + smoke + sea, satellite + Mercury,
  delegates + clock, calendar grid + thermometer — not one flat shape.
- Depth in layers: gradient sky -> midground -> foreground objects.
- Recognisable objects: hull + superstructure + funnel, solar panels,
  layered flames, swept-wing jet, checkered flag + F1 car.
- Data as visual: date grid 9-21, thermometer 1.5C, stock chart.

Drawn with PIL ImageDraw only. Imported by generate.py (the local build
tool); the shipped main.py only copies the finished entry.png.
Skill basis: canvas-design (visual expression, meticulous craft),
design-dna (tokens + style + effects), algorithmic-art (deterministic
patterns, no randomness), image-entry (verify SOI/EOI + full decode).
"""
import math

import art_polish_r3d as polish  # Poles r3d: gradasi/bayangan/kilau.

RED = (176, 30, 36)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 120)
ORANGE = (255, 150, 40)
DARK = (12, 20, 34)
NIGHT = (18, 18, 30)
BLUE = (31, 78, 121)
GREEN = (30, 107, 58)
TAN = (222, 205, 170)


def _font(name, size):
    from PIL import ImageFont
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + name, size)


def _bands(d, x, y, w, h, colors):
    """Horizontal gradient via stacked bands (top -> bottom)."""
    n = len(colors)
    for i, c in enumerate(colors):
        y0 = y + i * h // n
        y1 = y + (i + 1) * h // n
        d.rectangle([x, y0, x + w, y1], fill=c)


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


def _smoke(d, cx, cy, r, color=(150, 150, 160), top=None):
    """Three overlapping puffs rising up-left. top: optional clip —
    nothing is drawn above y=top (panel edge, m7 r3e). Puffs fully
    above the clip are skipped; partially-overlapping ones are cut
    flat at the edge, exactly as a true clip would look."""
    boxes = [
        [cx - r, cy - r, cx + r, cy + r],
        [cx - r - 5, cy - r - 4, cx - r + 3, cy + r - 4],
        [cx - r + 2, cy - r - 8, cx + r + 4, cy - r],
    ]
    for b in boxes:
        if top is not None:
            if b[3] < top:
                continue
            b[1] = max(b[1], top)
        d.ellipse(b, fill=color)


def _ship(d, x, y, w, h, hull=(10, 18, 30), clip_top=None):
    """Recognisable tanker: pointed bow, hull, white superstructure,
    funnel with smoke. (x, y) = top-left of the hull. clip_top: if
    given, the funnel smoke is clipped at that y (panel edge)."""
    d.polygon([(x, y + 3), (x + w - 8, y + 3), (x + w, y + h // 2),
               (x + w - 8, y + h - 1), (x, y + h - 1)],
              fill=hull, outline=WHITE, width=1)
    # Superstructure (bridge block) + funnel, aft.
    d.rectangle([x + 4, y - 5, x + 12, y + 3], fill=WHITE)
    d.rectangle([x + 14, y - 7, x + 18, y + 3], fill=(150, 40, 40))
    _smoke(d, x + 16, y - 12, 3, color=(140, 140, 150), top=clip_top)
    # Waterline highlight.
    d.line([(x + 2, y + h - 2), (x + w - 10, y + h - 2)],
           fill=(120, 170, 210), width=1)


def _bignum(d, x, y, text, size=19, fill=WHITE):
    """Big bold number/keyword at the lower left of a strip."""
    d.text((x + 6, y), text, font=_font("DejaVuSans-Bold.ttf", size), fill=fill)


# ---- 3 lead scenes (322 x 58) ---------------------------------------------
def scene_gulf(d, x, y, w, h):
    """Strait of Hormuz as a MAP SCENE: tan Iran (top) + tan Arabia
    (bottom), blue Gulf channel with depth bands, Bahrain marked, two
    recognisable tankers, missile arcs, explosions. Labels on the art."""
    # Sea: gradasi vertikal HALUS per-baris (M8 r3e) — biru sedang di
    # atas -> biru gelap di bawah. Menggantikan _bands r3c (4 blok biru
    # gelap yang terbaca rata); gradasi kini terbaca di crop 2x.
    # Tetap cukup gelap untuk teks putih (BAHRAIN/KHASAB/2 TANKERS HIT).
    polish.soft_vertical_gradient(d, x, y, w, h,
                                 (52, 110, 155), (30, 72, 108),
                                 (14, 38, 62))
    # Iran (top): tan landmass with a wavy coastline.
    d.polygon([(x, y), (x + w, y), (x + w, y + 12), (x + 260, y + 18),
               (x + 200, y + 22), (x + 130, y + 14), (x + 90, y + 17),
               (x + 40, y + 12), (x, y + 19)], fill=TAN)
    # Arabia (bottom): tan landmass, wavy coast.
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 10),
               (x + 250, y + h - 18), (x + 200, y + h - 13),
               (x + 120, y + h - 19), (x + 60, y + h - 12), (x, y + h - 15)],
              fill=TAN)
    # Garis pantai tan terang berlekuk di tepi bawah kanal (M8 r3e) —
    # mengikuti tepi atas daratan Arabia, digambar sebelum kapal/
    # bayangan supaya objek duduk di atasnya. Label tidak disentuh.
    d.line([(x, y + h - 15), (x + 60, y + h - 12), (x + 120, y + h - 19),
            (x + 200, y + h - 13), (x + 250, y + h - 18), (x + w, y + h - 10)],
           fill=(238, 224, 196), width=2, joint="curve")
    # Bahrain: red dot with white ring, mid-Gulf.
    bx, by = x + w // 2 - 10, y + h // 2 + 2
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
              outline=WHITE, width=2)
    # Two tankers, +20% (m5): recognisable ships (hull + bridge +
    # funnel + smoke). Bayangan lembut di bawah tiap lambung (M8),
    # digambar SEBELUM kapal supaya kapal duduk di atas bayangannya.
    polish.soft_shadow(d, x + w - 72, y + 25, 26, 4, (24, 58, 88))
    polish.soft_shadow(d, x + w - 46, y + h - 19, 23, 4, (16, 42, 66))
    # m7 r3e: asap kedua kapal di-clip di tepi atas panel (y) — asap
    # tanker-1 sebelumnya menjorok ~11px di atas tepi panel.
    _ship(d, x + w - 96, y + 12, 48, 11, clip_top=y)
    _ship(d, x + w - 66, y + h - 31, 41, 10, clip_top=y)
    # Kilau air: garis terang tipis di air terbuka (M8) — A di antara
    # label kiri dan ledakan Bahrain, B di antara Bahrain dan tanker 1.
    polish.sea_glints(d, [(x + 100, y + 24, x + 135, y + 24),
                          (x + 175, y + 40, x + 220, y + 40)])
    # Missile arcs (dotted white): Iran -> Bahrain, Iran -> tanker 1.
    for t in range(0, 11):
        px = x + w // 2 + 30 + t * 4
        py = y + 4 + int(12 * math.sin(t / 10.0 * math.pi / 2))
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    for t in range(0, 9):
        px = x + w - 110 + t * 4
        py = y + 6 + int(8 * math.sin(t / 8.0 * math.pi / 2))
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    # Explosion starbursts: at Bahrain and at tanker 1.
    _burst(d, bx, by, 13)
    _burst(d, x + w - 72, y + 16, 11)
    _smoke(d, bx - 8, by + 12, 5)
    _smoke(d, x + w - 88, y + 26, 4)
    # Labels.
    d.text((bx + 12, by - 6), "BAHRAIN", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=WHITE)
    d.text((x + 10, y + 3), "IRAN", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=INK)
    d.text((x + 8, y + 21), "2 TANKERS HIT",
           font=_font("DejaVuSans-Bold.ttf", 8), fill=WHITE)
    d.text((x + 8, y + 31), "STRAIT OF HORMUZ",
           font=_font("DejaVuSans-Bold.ttf", 8), fill=WHITE)
    d.text((x + w - 96, y + 24), "KHASAB",
           font=_font("DejaVuSans-Bold.ttf", 8), fill=WHITE)
    # Vignette SANGAT tipis di tepi kiri/kanan zona laut (M8) — paling
    # akhir supaya di atas laut tapi tidak menyentuh label mana pun.
    polish.sea_edge_vignette(d, x, y, w, h)


def scene_quake(d, x, y, w, h):
    """Peru quake as a CROSS-SECTION SCENE: layered Andes with snow caps
    and shaded faces, cracked ground, red seismograph, epicentre rings."""
    # Sky gradient: pale sand -> deeper sand.
    _bands(d, x, y, w, h, [(236, 226, 198), (230, 216, 184),
                           (224, 206, 170)])
    # Back range (lighter), front range (darker, shaded right faces).
    d.polygon([(x, y + h), (x + 60, y + 20), (x + 120, y + h)],
              fill=(170, 132, 92))
    d.polygon([(x + 100, y + h), (x + 190, y + 8), (x + 290, y + h)],
              fill=(150, 112, 72))
    d.polygon([(x + 110, y + h), (x + 200, y + 4), (x + 300, y + h)],
              fill=(120, 88, 54))
    # Shaded right faces (darker slope on the front peak).
    d.polygon([(x + 200, y + 4), (x + 300, y + h), (x + 250, y + h)],
              fill=(96, 68, 40))
    # Snow caps.
    d.polygon([(x + 185, y + 18), (x + 200, y + 4), (x + 215, y + 18)],
              fill=(245, 240, 225))
    d.polygon([(x + 178, y + 22), (x + 190, y + 8), (x + 202, y + 22)],
              fill=(245, 240, 225))
    d.polygon([(x + 52, y + 28), (x + 60, y + 20), (x + 68, y + 28)],
              fill=(245, 240, 225))
    # Ground band + cracks.
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(176, 138, 88))
    d.line([(x + 40, y + h - 18), (x + 70, y + h - 8), (x + 95, y + h - 18),
            (x + 130, y + h - 6)], fill=(90, 60, 30), width=2)
    d.line([(x + 210, y + h - 18), (x + 240, y + h - 7), (x + 275, y + h - 18)],
           fill=(90, 60, 30), width=2)
    # Seismograph trace in red across the middle.
    pts = []
    for i in range(0, w + 1, 6):
        amp = 2 if i < w * 0.3 or i > w * 0.75 else 12
        yy = y + h // 2 + (amp * math.sin(i / 3.0) if i % 12 else -amp)
        pts.append((x + i, yy))
    d.line(pts, fill=RED, width=2)
    # Epicentre marker: concentric rings + star, on the ground line.
    ex, ey = x + 205, y + h - 20
    for r in (12, 8, 4):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], outline=RED, width=1)
    d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=RED)
    # Labels.
    d.text((x + w - 88, y + h - 16), "108 km deep",
           font=_font("DejaVuSans-Bold.ttf", 9), fill=WHITE)
    d.text((x + 245, y + 6), "ONCORES", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=INK)
    d.text((x + 8, y + h - 14), "LIMA", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=WHITE)


def scene_cop31(d, x, y, w, h):
    """COP31 as a DATA SCENE (rank 1 pattern): globe + thermometer +
    delegate silhouettes + a 9-21 date grid with day 21 highlighted,
    '+1 DAY' and '1.5C' — the summit's own numbers as the picture."""
    # Gradasi vertikal halus (M8): mint -> mint muda -> nyaris putih,
    # digambar DULU supaya globe/termometer/grid/delegasi tetap di atas.
    polish.soft_vertical_gradient(d, x, y, w, h, (206, 228, 208),
                                  (224, 238, 222), (244, 247, 240))
    # Globe (left): blue circle, green land blobs, white highlight.
    gx, gy, gr = x + 30, y + 26, 17
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=BLUE)
    d.polygon([(gx - 10, gy - 4), (gx - 2, gy - 9), (gx + 6, gy - 3),
               (gx + 2, gy + 5), (gx - 8, gy + 3)], fill=(60, 160, 90))
    d.polygon([(gx + 2, gy + 8), (gx + 9, gy + 8), (gx + 7, gy + 14),
               (gx, gy + 12)], fill=(60, 160, 90))
    d.arc([gx - gr + 3, gy - gr + 3, gx + gr - 8, gy + gr - 8],
          start=200, end=320, fill=WHITE, width=2)
    # Bayangan gelap tipis di bawah globe (M8).
    polish.soft_shadow(d, gx, gy + gr + 3, gr + 3, 4, (214, 230, 212))
    # Thermometer (right of globe): white tube, red mercury, 1.5C label.
    tx = x + 58
    d.rectangle([tx, y + 6, tx + 9, y + 38], fill=WHITE,
                outline=INK, width=1)
    d.rectangle([tx + 2, y + 12, tx + 7, y + 36], fill=RED)
    d.ellipse([tx - 3, y + 34, tx + 12, y + 49], fill=RED)
    d.text((tx + 14, y + 6), "1.5°C", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=RED)
    # Date grid 9-21 (13 cells): white days, day 21 red.
    gx0, gy0, cw, chh, gap = x + 108, y + 4, 13, 16, 2
    for i, day in enumerate(range(9, 22)):
        cx0 = gx0 + i * (cw + gap)
        if day == 21:
            d.rectangle([cx0, gy0, cx0 + cw, gy0 + chh], fill=RED)
            col = WHITE
        else:
            d.rectangle([cx0, gy0, cx0 + cw, gy0 + chh], fill=WHITE,
                        outline=INK, width=1)
            col = INK
        t = str(day)
        tw = d.textlength(t, font=_font("DejaVuSans-Bold.ttf", 7))
        d.text((cx0 + (cw - tw) / 2, gy0 + 4), t,
               font=_font("DejaVuSans-Bold.ttf", 7), fill=col)
    # Grid captions: schedule label + "+1 DAY" (overtime).
    d.text((gx0, gy0 + 19), "NOV 9–20 SCHEDULED",
           font=_font("DejaVuSans.ttf", 7), fill=(90, 84, 70))
    d.text((gx0 + 128, gy0 + 19), "+1 DAY",
           font=_font("DejaVuSans-Bold.ttf", 9), fill=RED)
    # Delegate silhouettes along the bottom + table line (m6: garis
    # meja ditebalkan + 2 lembar dokumen putih di depan siluet).
    d.line([(x + 108, y + 52), (x + w - 6, y + 52)], fill=INK, width=2)
    for i in range(6):
        dx = x + 118 + i * 30
        d.ellipse([dx, y + 38, dx + 10, y + 48], fill=INK)
        d.rectangle([dx - 2, y + 48, dx + 12, y + 52], fill=INK)
    for doc_x, doc_y in ((x + 134, y + 44), (x + 200, y + 45)):
        d.rectangle([doc_x, doc_y, doc_x + 14, y + 52], fill=WHITE,
                    outline=(120, 120, 110), width=1)
        d.line([(doc_x + 2, doc_y + 3), (doc_x + 12, doc_y + 3)],
               fill=(150, 150, 145), width=1)
        d.line([(doc_x + 2, doc_y + 6), (doc_x + 10, doc_y + 6)],
               fill=(150, 150, 145), width=1)


LEAD_SCENES = [scene_gulf, scene_quake, scene_cop31]

# ---- 10 brief strips (190 x 40): mini-SCENES, not icons -------------------
def strip_planet(d, x, y, w, h):
    """#4 BepiColombo: deep-space gradient, starfield, cratered Mercury
    with orbit ring, and a recognisable satellite — white body flanked
    by BLUE solar panels with grid lines, not a white bar."""
    _bands(d, x, y, w, h, [(16, 24, 48), (12, 18, 34), (8, 12, 24)])
    _stars(d, x, y, w, h, n=16)
    # Mercury (right): orange disc, craters, orbit ring.
    mx, my, mr = x + w - 30, y + 20, 14
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(205, 120, 50))
    d.ellipse([mx - 7, my - 5, mx - 1, my + 1], fill=(160, 85, 35))
    d.ellipse([mx + 2, my + 3, mx + 8, my + 9], fill=(160, 85, 35))
    d.ellipse([mx - mr - 6, my - mr - 4, mx + mr + 6, my + mr + 4],
              outline=(255, 180, 90), width=1)
    # Satellite (centre-right): blue solar panels + white body + dish.
    d.rectangle([x + 82, y + 14, x + 98, y + 18], fill=(40, 90, 160))
    d.rectangle([x + 112, y + 14, x + 128, y + 18], fill=(40, 90, 160))
    for px in (x + 86, x + 90, x + 94, x + 116, x + 120, x + 124):
        d.line([(px, y + 14), (px, y + 18)], fill=(120, 170, 230), width=1)
    d.rectangle([x + 98, y + 12, x + 112, y + 20], fill=WHITE)
    d.polygon([(x + 105, y + 20), (x + 102, y + 26), (x + 108, y + 26)],
              fill=YELLOW)
    _bignum(d, x, y + h - 26, "8 YRS", fill=YELLOW)


def strip_flame(d, x, y, w, h):
    """#5 Kyiv strikes: night-sky gradient, skyline on the RIGHT (lit
    windows kept clear of the '12 KILLED' text zone), two layered fireballs
    (orange tongue -> yellow core -> white heart) + smoke."""
    _bands(d, x, y, w, h, [(24, 24, 44), (16, 16, 30), (10, 10, 20)])
    # Skyline, right half only — windows never reach the text zone.
    for bx, bw, bh in [(x + 108, 24, 16), (x + 136, 30, 22),
                       (x + 168, 20, 14)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(6, 6, 14))
        for wx in (bx + 4, bx + 12, bx + 20):
            if wx + 3 < bx + bw:
                d.rectangle([wx, y + h - bh + 4, wx + 3, y + h - bh + 7],
                            fill=(255, 220, 120))
    # Layered flames over the skyline.
    for cx, cy, s in [(x + 122, y + 12, 9), (x + 152, y + 15, 7)]:
        d.polygon([(cx, cy - s), (cx + s, cy + s // 2), (cx + s // 2, cy + s),
                   (cx - s // 2, cy + s), (cx - s, cy + s // 2)],
                  fill=(255, 120, 30))
        d.polygon([(cx, cy - s // 2), (cx + s // 2, cy + s // 3),
                   (cx, cy + s), (cx - s // 2, cy + s // 3)],
                  fill=(255, 210, 90))
        d.ellipse([cx - 2, cy + 1, cx + 2, cy + 5], fill=WHITE)
    _smoke(d, x + 122, y + 4, 3)
    _bignum(d, x, y + h - 26, "12 KILLED")


def strip_shield(d, x, y, w, h):
    """#6 Riyadh intercepts: night sky, two missile silhouettes with
    dotted trails arcing down, orange intercept bursts, and a recognisable
    JET (fuselage + swept wings + tail fin) on the right."""
    _bands(d, x, y, w, h, [(20, 24, 44), (14, 16, 30), (10, 10, 20)])
    # Missile 1 (top-left) with dotted trail.
    d.polygon([(x + 14, y + 8), (x + 32, y + 6), (x + 38, y + 10),
               (x + 32, y + 14), (x + 14, y + 12)], fill=WHITE)
    d.polygon([(x + 10, y + 8), (x + 14, y + 10), (x + 10, y + 12)],
              fill=ORANGE)
    for t in range(0, 6):
        px = x + 44 + t * 6
        py = y + 10 + t * 2
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    # Missile 2 (centre) diving.
    d.polygon([(x + 78, y + 6), (x + 92, y + 10), (x + 88, y + 16),
               (x + 76, y + 14)], fill=WHITE)
    for t in range(0, 5):
        px = x + 96 + t * 5
        py = y + 12 + t * 2
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    # Intercept bursts.
    _burst(d, x + 62, y + 26, 8)
    _burst(d, x + 118, y + 30, 7)
    # Jet (right): fuselage, swept wings, tail fin, engine glow.
    jx, jy = x + 138, y + 10
    d.polygon([(jx, jy + 4), (jx + 34, jy + 2), (jx + 44, jy + 6),
               (jx + 34, jy + 10), (jx, jy + 8)], fill=(150, 170, 200))
    d.polygon([(jx + 12, jy + 4), (jx + 20, jy - 4), (jx + 24, jy + 4)],
              fill=(150, 170, 200))
    d.polygon([(jx + 28, jy + 6), (jx + 38, jy + 12), (jx + 30, jy + 10)],
              fill=(150, 170, 200))
    d.ellipse([jx + 42, jy + 4, jx + 48, jy + 8], fill=ORANGE)
    _bignum(d, x, y + h - 26, "3 DOWN", fill=YELLOW)


def strip_cuffs(d, x, y, w, h):
    """#7 Chapo captured: dark interrogation room, spotlight cone from
    above, steel handcuffs with highlight + chain, red FBI badge."""
    _bands(d, x, y, w, h, [(52, 36, 36), (40, 28, 28), (30, 20, 20)])
    # Spotlight cone from the top-right.
    d.polygon([(x + 118, y), (x + 148, y), (x + 178, y + h),
               (x + 128, y + h)], fill=(80, 58, 58))
    # Handcuffs: two steel rings + chain, right side, clear of the text.
    for cx in (x + 128, x + 152):
        d.ellipse([cx, y + 6, cx + 20, y + 26], outline=WHITE, width=3)
        d.ellipse([cx + 2, y + 8, cx + 18, y + 24], outline=(150, 150, 160),
                  width=1)
        d.ellipse([cx + 8, y + 14, cx + 12, y + 18], fill=WHITE)
    d.line([(x + 148, y + 16), (x + 152, y + 16)], fill=WHITE, width=2)
    # Red FBI badge.
    d.rectangle([x + 172, y + 6, x + 186, y + 28], fill=RED)
    d.text((x + 175, y + 11), "FBI", font=_font("DejaVuSans-Bold.ttf", 9),
           fill=WHITE)
    _bignum(d, x, y + h - 26, "CAPTURED", size=16)


def strip_chip(d, x, y, w, h):
    """#8 AI chips: dark-green circuit board, glowing traces with nodes,
    and a gold chip with pins + bright core on the right."""
    _bands(d, x, y, w, h, [(12, 30, 20), (10, 26, 18), (8, 20, 14)])
    # Circuit traces: horizontal + vertical with node dots.
    for gy in (y + 8, y + 20, y + 32):
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=(40, 120, 70), width=1)
    for gx in (x + 30, x + 90, x + 150):
        d.line([(gx, y + 4), (gx, y + h - 4)], fill=(40, 120, 70), width=1)
    for nx, ny in [(x + 30, y + 8), (x + 90, y + 20), (x + 150, y + 32),
                   (x + 60, y + 20), (x + 120, y + 8)]:
        d.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(80, 200, 120))
    # Gold chip: dark body, gold frame, pins, glowing core.
    d.rectangle([x + w - 58, y + 5, x + w - 14, y + h - 7], fill=INK)
    d.rectangle([x + w - 50, y + 13, x + w - 22, y + h - 15],
                outline=YELLOW, width=1)
    d.ellipse([x + w - 42, y + 16, x + w - 30, y + 28], fill=YELLOW)
    for i in range(3):
        d.line([(x + w - 58, y + 12 + i * 8), (x + w - 62, y + 12 + i * 8)],
               fill=YELLOW, width=2)
        d.line([(x + w - 14, y + 12 + i * 8), (x + w - 10, y + 12 + i * 8)],
               fill=YELLOW, width=2)
    _bignum(d, x, y + h - 26, "900,000", size=18, fill=YELLOW)


def strip_euro(d, x, y, w, h):
    """#9 EU arms: deep-blue field, gold euro medallion with ring of
    stars, small EU flag block on the right."""
    d.rectangle([x, y, x + w, y + h], fill=BLUE)
    # Ring of 8 stars around the euro medallion (centre-right).
    cx, cy = x + w - 52, y + h // 2
    for k in range(8):
        a = k * math.pi / 4
        sx = cx + int(22 * math.cos(a))
        sy = cy + int(15 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=YELLOW)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(20, 60, 100))
    d.text((cx - 8, cy - 12), "€", font=_font("DejaVuSans-Bold.ttf", 22),
           fill=YELLOW)
    # Small EU flag block (blue + gold stars) far right.
    d.rectangle([x + w - 22, y + 6, x + w - 6, y + h - 6], fill=(20, 60, 100),
                outline=YELLOW, width=1)
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2
        sx = x + w - 14 + int(5 * math.cos(a))
        sy = y + h // 2 + int(5 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=YELLOW)
    _bignum(d, x, y + h - 26, "€1bn", fill=YELLOW)


def strip_magnifier(d, x, y, w, h):
    """#10 Denmark plot: paper background, a document with lines, a
    magnifier over a shadow figure, red X — the foiled plot, told."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # Document (right): white page, ruled lines, red seal.
    d.rectangle([x + 96, y + 4, x + w - 8, y + h - 4], fill=WHITE,
                outline=(120, 110, 90), width=1)
    for ly in (y + 10, y + 16, y + 22, y + 28):
        d.line([(x + 102, ly), (x + w - 14, ly)], fill=(180, 170, 150),
               width=1)
    d.ellipse([x + w - 24, y + h - 14, x + w - 16, y + h - 6], fill=RED)
    # Shadow figure inside the magnifier lens.
    d.ellipse([x + 108, y + 8, x + 122, y + 22], fill=INK)
    d.rectangle([x + 102, y + 22, x + 128, y + 34], fill=INK)
    # Magnifier: ring + handle.
    d.ellipse([x + 96, y + 4, x + 134, y + 34], outline=INK, width=3)
    d.line([(x + 130, y + 30), (x + 150, y + 38)], fill=INK, width=4)
    # Red X over the plot.
    d.line([(x + 156, y + 6), (x + 182, y + 32)], fill=RED, width=4)
    d.line([(x + 182, y + 6), (x + 156, y + 32)], fill=RED, width=4)
    _bignum(d, x, y + h - 26, "FOILED", fill=RED)


def strip_flag(d, x, y, w, h):
    """#11 Russell P1: night circuit, floodlights, a WAVING checkered flag
    (offset rows) and a low F1 car silhouette on the track line."""
    _bands(d, x, y, w, h, [(18, 18, 24), (14, 14, 20), (10, 10, 16)])
    # Floodlights.
    for lx in (x + 16, x + 60, x + 104):
        d.ellipse([lx, y + 4, lx + 4, y + 8], fill=YELLOW)
        d.polygon([(lx, y + 8), (lx + 2, y + 8), (lx + 8, y + 20),
                   (lx - 4, y + 20)], fill=(60, 60, 40))
    # Waving checkered flag (right): two offset rows on a pole.
    d.line([(x + 150, y + 4), (x + 150, y + h - 4)], fill=WHITE, width=2)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + 152 + c * 9, y + 5 + r * 8,
                             x + 161 + c * 9, y + 13 + r * 8], fill=WHITE)
            else:
                d.rectangle([x + 152 + c * 9, y + 5 + r * 8,
                             x + 161 + c * 9, y + 13 + r * 8], fill=INK)
    # F1 car silhouette on the track line.
    d.line([(x + 4, y + h - 4), (x + w - 4, y + h - 4)], fill=YELLOW, width=2)
    cx0, cy0 = x + 78, y + 26
    d.polygon([(cx0, cy0), (cx0 + 34, cy0 - 2), (cx0 + 44, cy0 + 3),
               (cx0 + 34, cy0 + 6), (cx0, cy0 + 6)], fill=(200, 40, 40))
    d.rectangle([cx0 + 36, cy0 - 6, cx0 + 40, cy0 + 2], fill=(200, 40, 40))
    d.ellipse([cx0 + 6, cy0 + 4, cx0 + 12, cy0 + 10], fill=INK)
    d.ellipse([cx0 + 30, cy0 + 4, cx0 + 36, cy0 + 10], fill=INK)
    _bignum(d, x, y + h - 26, "P1", size=22, fill=YELLOW)


def strip_cricket(d, x, y, w, h):
    """#12 Rahul 136: green pitch with crease lines, a proper bat
    (handle + blade), red ball with seam, stumps with bails."""
    _bands(d, x, y, w, h, [(52, 118, 68), (46, 110, 62), (36, 88, 50)])
    # Pitch strip + crease lines.
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 80, 44))
    d.line([(x + 90, y + h - 14), (x + 190, y + h - 14)], fill=WHITE, width=1)
    d.line([(x + 90, y + 6), (x + 90, y + h - 14)], fill=WHITE, width=1)
    # Bat: handle + blade, angled mid-swing.
    d.polygon([(x + 104, y + 4), (x + 110, y + 6), (x + 122, y + 24),
               (x + 116, y + 28), (x + 104, y + 12)], fill=(200, 160, 100))
    d.rectangle([x + 100, y - 2, x + 106, y + 6], fill=(120, 80, 40))
    # Red ball with white seam.
    d.ellipse([x + 136, y + 8, x + 150, y + 22], fill=RED)
    d.arc([x + 136, y + 8, x + 150, y + 22], start=40, end=140,
          fill=WHITE, width=1)
    # Stumps with bails (right).
    for sx in (x + 166, x + 172, x + 178):
        d.rectangle([sx, y + 20, sx + 3, y + 34], fill=YELLOW)
    d.rectangle([x + 166, y + 18, x + 181, y + 20], fill=YELLOW)
    _bignum(d, x, y + h - 26, "136")


def strip_star(d, x, y, w, h):
    """#13 Rutte Warsaw: dawn sky gradient, Warsaw skyline with lit
    windows along the bottom, a recognisable JET (fuselage + swept wings
    + tail fin + engines) in the sky, white NATO star."""
    _bands(d, x, y, w, h, [(36, 78, 130), (28, 66, 118), (20, 52, 100)])
    # Warsaw skyline along the bottom (below the jet, clear of WARSAW text).
    for bx, bw, bh in [(x + 84, 9, 11), (x + 96, 9, 15), (x + 108, 9, 9),
                       (x + 120, 9, 13)]:
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(10, 20, 40))
        d.rectangle([bx + 2, y + h - bh + 3, bx + 4, y + h - bh + 5],
                    fill=YELLOW)
        d.rectangle([bx + 5, y + h - bh + 6, bx + 7, y + h - bh + 8],
                    fill=YELLOW)
    # Jet (centre-right sky): fuselage, swept wings, tail, engines.
    jx, jy = x + 118, y + 8
    d.polygon([(jx, jy + 4), (jx + 36, jy + 2), (jx + 46, jy + 6),
               (jx + 36, jy + 10), (jx, jy + 8)], fill=(240, 240, 245))
    d.polygon([(jx + 12, jy + 4), (jx + 22, jy - 4), (jx + 26, jy + 4)],
              fill=(240, 240, 245))
    d.polygon([(jx + 30, jy + 6), (jx + 40, jy + 12), (jx + 32, jy + 10)],
              fill=(240, 240, 245))
    d.ellipse([jx + 44, jy + 4, jx + 50, jy + 8], fill=ORANGE)
    # NATO star (right).
    cx, cy = x + w - 26, y + 18
    d.polygon([(cx, cy - 12), (cx + 3, cy - 3), (cx + 12, cy),
               (cx + 3, cy + 3), (cx, cy + 12), (cx - 3, cy + 3),
               (cx - 12, cy), (cx - 3, cy - 3)], fill=WHITE)
    _bignum(d, x, y + h - 26, "WARSAW", size=17)


STRIPS = {
    "planet": strip_planet,
    "flame": strip_flame,
    "shield": strip_shield,
    "cuffs": strip_cuffs,
    "chip": strip_chip,
    "euro": strip_euro,
    "magnifier": strip_magnifier,
    "flag": strip_flag,
    "cricket": strip_cricket,
    "star": strip_star,
}
