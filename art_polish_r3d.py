#!/usr/bin/env python3
"""Poles art r3d — news-image-20261121 (ditulis dari nol, sesi ini).

Tugas Goldfish r3c §3: M8 depth/shading, M9 peta, M10 + minor m2/m4.
Aturan tegas yang dipegang di setiap keputusan di modul ini:
- CHASE-TOP-10: target rank TOP 10, lantai 25, peluang top-50 >=30%
  (target 50%+). Revisi yang tidak menaikkan rank beneran = tidak guna.
- FOKUS TIDAK DIBATASI: yang kurang dikejar, apa pun areanya.
- SANGGUP-SANGGUPIN: kalau satu pendekatan mentok, cari jalan lain.

Isi modul (semua baru):
- helper depth: gradasi vertikal halus (per-baris), bayangan lembut
  berlapis, kilau air, vignette tepi laut yang sangat tipis.
- CONTINENTS_V2: poligon benua digambar ulang, 2-3x titik vs r3c,
  garis pantai berlekuk (Hudson Bay, Alaska, Meksiko lancip, Amerika
  Selatan meruncing, tonjolan barat Afrika, Eropa dikenali, India +
  Asia Tenggara + Arabia, Australia). PINS TIDAK disentuh — poligon
  dirancang MENUTUPI posisi pin yang digambar (diuji point-in-polygon
  untuk ke-12 pin darat; r3c: pin 1/3/5/6/9 jatuh di laut).
- strip_shield_v2 (#6): jet cerah + kokpit gelap + starburst pertama
  dipindah sampai "3 DOWN" bersih (diukur: teks berakhir x+94.6,
  "W" di 57.8-78.7 — geser literal +5px MASIH menabrak W, jadi
  starburst dipindah ke ujung trail misil-2, x+102 — lihat catatan).
- strip_flag_v2 (#11): mobil F1 dengan 2 roda hitam besar + hub
  putih + kanopi putih + sayap belakang yang jelas.
"""
import math

INK = (17, 17, 17)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 120)
ORANGE = (255, 150, 40)
RED = (176, 30, 36)


def _font(name, size):
    from PIL import ImageFont
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + name, size)


def _mix(c1, c2, t):
    """Blend dua warna RGB; t=0 -> c1, t=1 -> c2."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def soft_vertical_gradient(d, x, y, w, h, top, mid, bottom):
    """Gradasi vertikal HALUS per-baris: top -> mid -> bottom.

    Beda dari _bands (r3c) yang menumpuk 3-4 blok warna kasar: di sini
    tiap baris diinterpolasi, jadi tidak ada garis batas antar-blok.
    """
    for row in range(h):
        t = row / max(h - 1, 1)
        if t < 0.5:
            col = _mix(top, mid, t * 2)
        else:
            col = _mix(mid, bottom, (t - 0.5) * 2)
        d.line([(x, y + row), (x + w, y + row)], fill=col)


def soft_shadow(d, cx, cy, rx, ry, base, dark=(8, 20, 36)):
    """Bayangan lembut: 3 elips konsentris, makin ke dalam makin gelap.

    Digambar di ATAS permukaan (air/tanah) tapi di BAWAH objek bila
    dipanggil sebelum objek digambar — pemanggil yang mengatur urutan.
    """
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
              fill=_mix(base, dark, 0.18))
    d.ellipse([cx - rx * 0.7, cy - ry * 0.7, cx + rx * 0.7, cy + ry * 0.7],
              fill=_mix(base, dark, 0.34))
    d.ellipse([cx - rx * 0.4, cy - ry * 0.4, cx + rx * 0.4, cy + ry * 0.4],
              fill=_mix(base, dark, 0.50))


def sea_glints(d, segments, color=(140, 190, 220)):
    """Kilau air: garis terang tipis 1px di permukaan laut."""
    for (x0, y0, x1, y1) in segments:
        d.line([(x0, y0), (x1, y1)], fill=color, width=1)


def sea_edge_vignette(d, x, y, w, h, color=(12, 32, 52)):
    """Vignette SANGAT tipis: 2 garis 1px di tepi kiri/kanan zona laut
    saja (y+20..y+h-20) — tidak menyentuh label apa pun (label paling
    kiri mulai x+8, paling kanan berakhir ~x+w-50). Tepi atas/bawah
    sengaja tidak disentuh: atas ada label IRAN, bawah daratan tan."""
    y0, y1 = y + 20, y + h - 20
    d.line([(x, y0), (x, y1)], fill=color, width=1)
    d.line([(x + w - 1, y0), (x + w - 1, y1)], fill=color, width=1)
    d.line([(x + 1, y0), (x + 1, y1)], fill=_mix(color, (24, 58, 88), 0.4),
           width=1)
    d.line([(x + w - 2, y0), (x + w - 2, y1)],
           fill=_mix(color, (24, 58, 88), 0.4), width=1)


def _bands(d, x, y, w, h, colors):
    """Gradasi blok (kompatibel perilaku r3c) untuk strip v2."""
    n = len(colors)
    for i, c in enumerate(colors):
        y0 = y + i * h // n
        y1 = y + (i + 1) * h // n
        d.rectangle([x, y0, x + w, y1], fill=c)


def _burst(d, cx, cy, r, color=ORANGE):
    """8-spoke explosion starburst dengan inti terang."""
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
               fill=color, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 210, 90))


def _bignum(d, x, y, text, size=19, fill=WHITE):
    """Angka/kata besar di kiri bawah strip."""
    d.text((x + 6, y), text, font=_font("DejaVuSans-Bold.ttf", size),
           fill=fill)


# ---- Peta r3d: CONTINENTS_V2 -------------------------------------------
# Poligon benua digambar ulang dari nol (koordinat fraksi 0-1, peta
# 322x150 di (676,698)). Syarat keras: SETIAP pin yang digambar harus
# jatuh di atas daratan (posisi pin TIDAK diubah — PINS di generate.py
# tidak disentuh). Posisi pin yang digambar (fx, fy, sudah termasuk
# dx/dy): 1 (0.650,0.309) Arabia/Iran, 2 (0.261,0.662) Peru,
# 3 (0.557,0.253) Antalya, 5 (0.585,0.189) Kyiv, 6 (0.602,0.387)
# Riyadh, 7 (0.171,0.380) Meksiko, 8 (0.258,0.278) DC,
# 9 (0.463,0.199) Brussels, 10 (0.495,0.102) Kopenhagen,
# 11 (0.153,0.298) Las Vegas, 12 (0.958,0.855) NZ, 13 (0.537,0.162)
# Warsawa. Di r3c, pin 1/3/5/6/9 jatuh di laut (diuji point-in-polygon)
# — V2 menutup celah itu: lobus Anatolia/Arabia di Asia, Eropa
# melebar ke timur (Rusia) + barat (Iberia), Afrika/Asia tumpang
# tindih secukupnya di Laut Merah (keduanya tan, tanpa sambungan
# terlihat). Diuji otomatis: semua 12 pin darat inside (lihat
# build-log r3d).
CONTINENTS_V2 = [
    # Amerika Utara — lekuk Hudson Bay, Alaska, lancip Meksiko.
    [(0.020, 0.160), (0.035, 0.100), (0.055, 0.055), (0.090, 0.035),
     (0.125, 0.045), (0.155, 0.030), (0.185, 0.050), (0.205, 0.045),
     (0.215, 0.085), (0.225, 0.115), (0.235, 0.085), (0.250, 0.055),
     (0.265, 0.075), (0.280, 0.100), (0.275, 0.140), (0.285, 0.180),
     (0.290, 0.220), (0.285, 0.260), (0.270, 0.290), (0.255, 0.315),
     (0.240, 0.335), (0.215, 0.360), (0.195, 0.385), (0.175, 0.415),
     (0.185, 0.440), (0.160, 0.420), (0.140, 0.380), (0.120, 0.330),
     (0.100, 0.280), (0.070, 0.240), (0.045, 0.200)],
    # Greenland.
    [(0.315, 0.030), (0.350, 0.015), (0.385, 0.025), (0.400, 0.060),
     (0.385, 0.100), (0.360, 0.125), (0.335, 0.100), (0.315, 0.060)],
    # Amerika Selatan — meruncing ke selatan.
    [(0.240, 0.470), (0.270, 0.455), (0.300, 0.460), (0.330, 0.475),
     (0.360, 0.500), (0.380, 0.540), (0.370, 0.600), (0.355, 0.670),
     (0.340, 0.750), (0.325, 0.830), (0.305, 0.890), (0.295, 0.920),
     (0.280, 0.850), (0.265, 0.770), (0.250, 0.680), (0.240, 0.590),
     (0.232, 0.520)],
    # Eropa — Skandinavia, Rusia ke timur, Iberia ke barat, tumit Italia,
    # pantai selatan sampai Anatolia (menutupi pin 3/5/9/10/13).
    [(0.455, 0.045), (0.485, 0.025), (0.515, 0.028), (0.540, 0.050),
     (0.552, 0.075), (0.545, 0.095), (0.565, 0.105), (0.590, 0.115),
     (0.608, 0.140), (0.618, 0.165), (0.605, 0.195), (0.590, 0.220),
     (0.578, 0.245), (0.560, 0.265), (0.540, 0.262), (0.525, 0.245),
     (0.505, 0.235), (0.498, 0.258), (0.485, 0.262), (0.478, 0.240),
     (0.462, 0.225), (0.442, 0.210), (0.432, 0.185), (0.438, 0.155),
     (0.432, 0.130), (0.440, 0.100), (0.448, 0.070)],
    # Afrika — tonjolan barat + meruncing ke selatan.
    [(0.430, 0.315), (0.460, 0.295), (0.490, 0.290), (0.520, 0.295),
     (0.550, 0.305), (0.575, 0.325), (0.585, 0.360), (0.600, 0.400),
     (0.595, 0.460), (0.585, 0.520), (0.575, 0.580), (0.560, 0.640),
     (0.545, 0.700), (0.530, 0.760), (0.515, 0.720), (0.500, 0.660),
     (0.485, 0.600), (0.470, 0.540), (0.452, 0.485), (0.438, 0.430),
     (0.428, 0.395), (0.422, 0.360), (0.425, 0.345)],
    # Madagaskar.
    [(0.598, 0.690), (0.612, 0.700), (0.608, 0.745), (0.595, 0.775),
     (0.585, 0.730)],
    # Asia — Siberia, pantai Tiongkok, Asia Tenggara, semenanjung
    # Melayu + India, lekuk Teluk Persia, Arabia, lobus Anatolia
    # (menutupi pin 1/3/6).
    [(0.600, 0.100), (0.630, 0.060), (0.670, 0.038), (0.720, 0.025),
     (0.780, 0.018), (0.840, 0.028), (0.890, 0.048), (0.930, 0.075),
     (0.962, 0.108), (0.945, 0.155), (0.918, 0.195), (0.898, 0.235),
     (0.872, 0.275), (0.848, 0.315), (0.828, 0.355), (0.808, 0.395),
     (0.782, 0.432), (0.758, 0.458), (0.740, 0.425), (0.748, 0.390),
     (0.738, 0.430), (0.722, 0.472), (0.702, 0.428), (0.682, 0.385),
     (0.662, 0.348), (0.652, 0.385), (0.632, 0.428), (0.602, 0.470),
     (0.575, 0.432), (0.555, 0.392), (0.543, 0.348), (0.533, 0.305),
     (0.526, 0.265), (0.543, 0.230), (0.570, 0.205), (0.590, 0.165),
     (0.596, 0.130)],
    # Kepulauan Asia Tenggara.
    [(0.795, 0.415), (0.820, 0.400), (0.835, 0.430), (0.810, 0.450)],
    [(0.845, 0.470), (0.865, 0.460), (0.860, 0.500), (0.845, 0.490)],
    # Jepang.
    [(0.895, 0.155), (0.912, 0.170), (0.908, 0.210), (0.895, 0.240),
     (0.885, 0.200)],
    # Australia.
    [(0.790, 0.700), (0.812, 0.668), (0.838, 0.655), (0.868, 0.660),
     (0.895, 0.678), (0.912, 0.705), (0.905, 0.740), (0.888, 0.775),
     (0.862, 0.798), (0.838, 0.805), (0.815, 0.785), (0.795, 0.752),
     (0.782, 0.722)],
    # Britania.
    [(0.452, 0.075), (0.466, 0.085), (0.462, 0.115), (0.452, 0.130),
     (0.444, 0.100)],
    # Selandia Baru.
    [(0.935, 0.810), (0.955, 0.795), (0.972, 0.815), (0.982, 0.850),
     (0.968, 0.885), (0.945, 0.895), (0.932, 0.860)],
]


# ---- Strip v2 ------------------------------------------------------------
def strip_shield_v2(d, x, y, w, h):
    """#6 Riyadh v2 (M10 + m4): jet PUTIH/PERAK terang + jendela kokpit
    gelap; starburst pertama PINDAH dari (x+62, y+26) ke (x+102, y+21)
    r7 — di ujung trail misil-2, di kanan akhir teks "3 DOWN".

    Kenapa bukan geser literal +5px: diukur dengan PIL, "3 DOWN"
    (bold 19, dari x+6) berakhir di x+94.6 dan "W" menempati 57.8-78.7
    — starburst lama (x 54-70) menabrak W, dan +5px (59-75) MASIH di
    dalam W. Satu-satunya tempat bersih: di kanan x+94.6. Posisi baru
    (95-109, 14-28) bersih dari teks dan berjarak 2px dari starburst
    kedua (111-125) — terverifikasi visual crop 2x."""
    _bands(d, x, y, w, h, [(20, 24, 44), (14, 16, 30), (10, 10, 20)])
    # Misil 1 (kiri atas) + trail titik-titik.
    d.polygon([(x + 14, y + 8), (x + 32, y + 6), (x + 38, y + 10),
               (x + 32, y + 14), (x + 14, y + 12)], fill=WHITE)
    d.polygon([(x + 10, y + 8), (x + 14, y + 10), (x + 10, y + 12)],
              fill=ORANGE)
    for t in range(0, 6):
        px = x + 44 + t * 6
        py = y + 10 + t * 2
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    # Misil 2 (tengah) menukik + trail.
    d.polygon([(x + 78, y + 6), (x + 92, y + 10), (x + 88, y + 16),
               (x + 76, y + 14)], fill=WHITE)
    for t in range(0, 5):
        px = x + 96 + t * 5
        py = y + 12 + t * 2
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    # Ledakan intersepsi: #1 PINDAH (ujung trail misil-2), #2 tetap.
    _burst(d, x + 102, y + 21, 7)
    _burst(d, x + 118, y + 30, 7)
    # Jet (kanan): PUTIH/PERAK terang + jendela kokpit gelap.
    jx, jy = x + 138, y + 10
    jet = (240, 240, 245)
    wing = (225, 228, 235)
    d.polygon([(jx, jy + 4), (jx + 34, jy + 2), (jx + 44, jy + 6),
               (jx + 34, jy + 10), (jx, jy + 8)], fill=jet)
    d.polygon([(jx + 12, jy + 4), (jx + 20, jy - 4), (jx + 24, jy + 4)],
              fill=wing)
    d.polygon([(jx + 28, jy + 6), (jx + 38, jy + 12), (jx + 30, jy + 10)],
              fill=wing)
    d.ellipse([jx + 28, jy + 3, jx + 36, jy + 7], fill=(18, 28, 44))
    d.ellipse([jx + 42, jy + 4, jx + 48, jy + 8], fill=ORANGE)
    _bignum(d, x, y + h - 26, "3 DOWN", fill=YELLOW)


def strip_flag_v2(d, x, y, w, h):
    """#11 Russell P1 v2 (M10): mobil F1 kini TERBACA — 2 roda HITAM
    BESAR (r7) dengan hub putih, kanopi/kokpit putih, sayap belakang
    yang jelas, sayap depan kecil. Latar gelap sengaja dipertahankan
    supaya roda hitam + hub putih kontras; roda digambar SETELAH garis
    trek supaya duduk di atas trek."""
    _bands(d, x, y, w, h, [(18, 18, 24), (14, 14, 20), (10, 10, 16)])
    # Lampu sorot.
    for lx in (x + 16, x + 60, x + 104):
        d.ellipse([lx, y + 4, lx + 4, y + 8], fill=YELLOW)
        d.polygon([(lx, y + 8), (lx + 2, y + 8), (lx + 8, y + 20),
                   (lx - 4, y + 20)], fill=(60, 60, 40))
    # Bendera kotak berkibar (kanan) + tiang.
    d.line([(x + 150, y + 4), (x + 150, y + h - 4)], fill=WHITE, width=2)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + 152 + c * 9, y + 5 + r * 8,
                             x + 161 + c * 9, y + 13 + r * 8], fill=WHITE)
            else:
                d.rectangle([x + 152 + c * 9, y + 5 + r * 8,
                             x + 161 + c * 9, y + 13 + r * 8], fill=INK)
    # Garis trek (digambar dulu — roda duduk di atasnya).
    d.line([(x + 4, y + h - 4), (x + w - 4, y + h - 4)], fill=YELLOW,
           width=2)
    # Mobil F1: bodi rendah + sayap belakang + sayap depan.
    cx0, cy0 = x + 72, y + 24
    car = (200, 40, 40)
    d.polygon([(cx0, cy0 + 2), (cx0 + 36, cy0), (cx0 + 46, cy0 + 4),
               (cx0 + 36, cy0 + 8), (cx0, cy0 + 8)], fill=car)
    d.rectangle([cx0 + 2, cy0 - 6, cx0 + 6, cy0 + 2], fill=car)
    d.rectangle([cx0 - 2, cy0 - 8, cx0 + 10, cy0 - 5], fill=car)
    d.rectangle([cx0 + 42, cy0 + 2, cx0 + 48, cy0 + 6], fill=car)
    # Kanopi/kokpit putih di atas bodi.
    d.ellipse([cx0 + 16, cy0 - 2, cx0 + 28, cy0 + 4], fill=WHITE)
    # 2 roda HITAM BESAR + hub putih (kontras di latar gelap).
    for wx in (cx0 + 8, cx0 + 34):
        d.ellipse([wx - 7, cy0 + 1, wx + 7, cy0 + 15], fill=INK)
        d.ellipse([wx - 2, cy0 + 6, wx + 2, cy0 + 10], fill=WHITE)
    _bignum(d, x, y + h - 26, "P1", size=22, fill=YELLOW)


STRIPS_V2 = {
    "shield": strip_shield_v2,
    "flag": strip_flag_v2,
}
