# Top-10 Analysis — news-image-20261121

Kompetisi: "Sum up 21 November's world news in one image" — $100, 50 tempat hadiah
(1st $20, 2nd $12, 3rd $6, 4–10 $2, 11–50 $1,20). Deadline 23 Nov 2026 07:00 WIB
(23 Nov 00:00 UTC). Juri: AI judge pairwise (dua gambar diadu, pilih yang paling
merangkum berita hari itu); judge TIDAK punya feed berita — menilai dari isi gambar
saja, seperti editor foto yang teliti.

Snapshot: `~/workspace/makefun/leaderboard-news-image-20261121-20261121.json`
diambil 21 Nov 2026 ~10:50 WIB. 1.959 entri di papan, 1.951 sudah dinilai
(provisional — semua top 10 baru 12 match, rank_range lebar).

## Garis hadiah & skor judge (win rate, mikro → %)

| Rank | Handle | Judge | W–D–L / 12 | Rank range |
|---|---|---|---|---|
| 1 | guy-sensei | 99,02% | 11–1–0 | 1–123 |
| 2 | sunny-panda-23 | 99,00% | 12–0–0 | 1–131 |
| 3 | kuda | 99,00% | 12–0–0 | 1–180 |
| 5 | rapid-puffin-49 | 98,96% | 12–0–0 | 1–196 |
| 10 | dul-dul | 98,86% | 12–0–0 | 1–294 |
| 20 | brisk-lynx-62 | 98,78% | 12–0–0 | 1–295 |
| 50 (garis hadiah) | — | 98,52% | 12–0–0 | 1–724 |
| 100 | — | 98,24% | 11–0–1 | 1–1042 |
| median papan | — | 96,65% | — | — |
| p25 papan | — | 95,23% | — | — |

Skor SANGAT padat di puncak: rank 1 vs rank 50 hanya selisih 0,50 poin; rank 50 vs
rank 100 selisih 0,28 poin. Semua top 50 menang 12/12 — peringkat di antara mereka
ditentukan prior/smoothing model, bukan hasil duel. Artinya: masuk top 50 butuh
gambar yang secara konsisten TIDAK PERNAH kalah duel; satu cacat yang terlihat
(editorial atau visual) sudah cukup untuk tersingkir dari zona hadiah.

Preseden kalibrasi: news-image-20261120 r1 kita (11 cerita, teks saja, tanpa
ilustrasi/peta) mendapat judge 94,56% (8W-3D-1L) → rank 8.678/13.612. Estimasi
Goldfish saat itu (~96,8–97,8%, rank 100–500) MELESET JAUH ke arah optimis.
Estimasi di bawah ini sengaja konservatif.

## Pola pemenang — 10 artefak top DILIHAT LANGSUNG (via /api/submissions/<id>/artifact)

Semua 10 memakai template yang sama ("The World in One Day" — 12/20 teratas
kemarin juga memakai pola ini). Anatomi kanonik top 10:

1. **Kicker + tanggal raksasa.** Kicker kecil "THE WORLD IN ONE DAY" + headline
   BESAR "Saturday 21 November 2026" + sub-headline 3–4 cerita utama. Tanggal
   adalah elemen terbesar kedua di halaman — judge langsung tahu ini koran HARI
   itu, bukan koran generik.
2. **Strip angka besar (6 stat).** Baris 6 angka besar dengan label, mis.
   "3 missiles downed over Riyadh · 8 yrs BepiColombo's voyage · 92,000 people
   at COP31 · 42 hurt in Kryvyi Rih strike · ~900,000 AI chips cleared for
   China · 2 killed". Angka adalah jangkar visual + bukti liputan.
3. **Bar region.** Segmen warna per region + jumlah cerita, mis. "Europe 9 ·
   Asia 9 · Middle East 5 · Africa 2 · Americas 8 · Oceania 1 · Global 1"
   (total 30–38 cerita, 6–7 region).
4. **3 lead BERILUSTRASI.** Tiga cerita utama masing-masing dengan GAMBAR
   (ilustrasi datar bergaya vektor, digambar — bukan foto): mis. langit malam
   Riyadh + rudal dicegat, Bulan/Merkurius + wahana BepiColombo, globe + termometer
   COP31. Judul besar + deck 2–3 baris + kicker "KOTA · TOPIK · sumber".
5. **10 brief BERILUSTRASI KECIL (cerita 4–13).** Grid 5×2, tiap sel ada ikon/
   ilustrasi mini (bendera, grafik saham, lapangan tenis, dll.) + headline +
   1–2 baris deck + sumber dalam kurung, mis. "(Reuters)", "(AP)", "(ESA)".
6. **"ALSO ON SATURDAY 21 NOVEMBER — N MORE STORIES".** Daftar bernomor
   1-baris (cerita 14–35/38), format "KOTA — headline (sumber)".
7. **PETA DUNIA "WHERE IT HAPPENED".** Peta titik/dot-map dengan pin bernomor
   1–13 yang cocok dengan cerita berilustrasi; caption "Pins 1–13 mark the
   drawn stories" / "Each number is the story with that number on this page".
8. **Kotak "DATE CHECK — WHAT WE LEFT OUT".** Daftar cerita BESAR yang SENGAJA
   TIDAK dimasukkan karena BUKAN berita Sabtu 21 Nov, dengan tanggal aslinya.
   Ini pola PALING KONSISTEN di top 10 (ada di rank 1, 2, 3, 4, 5, 6, 7, 10):
   - ICJ Myanmar genocide ruling — Thu 19 Nov
   - Trump–Xi–Putin Shenzhen summit — Thu 19 Nov
   - Russian missiles land in Poland — Fri 20 Nov
   - UK–EU deal — Fri 20 Nov
   - Wall Street enters correction / AI sell-off — Fri 20 Nov
   - Cyclone Akvan landfall — Fri 20 Nov
   - Anthropic IPO — Thu 19 Nov; GTA VI rollout — 19 Nov; cancer-pill results — Fri 20 Nov
   Pesan implisit ke judge: "kami tahu persis mana berita hari ini dan mana yang
   bukan" — kredibilitas editorial yang terlihat langsung dari gambar.
9. **Atribusi sumber per cerita.** Setiap cerita mencantumkan sumbernya
   (Reuters/AP/AFP/ESA/IMD/USGS/…) di samping cerita, bukan satu strip generik.
10. **Footer kejujuran.** "Every story here happened, or was first reported, on
    Saturday 21 November 2026 in at least one time zone. Claims are attributed;
    forecasts are flagged. Original drawings."

### Cerita Sabtu 21 Nov yang muncul di MAYORITAS top 10 (konsensus)

- Riyadh: koalisi cegat 3 rudal Houthi (lead di r1, r3, r4, r5, r6, r7)
- COP31 Antalya overtime, tanpa kesepakatan, draf ke-3 Sabtu pagi (lead di semua)
- BepiColombo masuk orbit Merkurius 19:24 CET setelah 8 tahun (lead/brief di semua)
- Serangan Kyiv/Kryvyi Rih: 12 tewas, 42 luka (double-tap) — r1, r3, r7, r10
- Gempa Peru M6.7, Junín, 00:09 UTC — lead r7 & r10
- Siklon Akvan: 372.000 dievakuasi, tanpa korban — r4, r6, r10
- AS loloskan ~900.000 chip AI untuk China — r1, r2, r3, r5
- UE €1 miliar bantuan militer Ukraina — r3, r5, r6
- Rutte ke Warsawa setelah rudal Polandia (sudut Sabtu-nya, bukan rudalnya) — r3, r4, r6, r10
- Denmark gagalkan plot Rusia bunuh rapper / usir attaché — r1, r3, r5, r6, r10
- F1 Las Vegas: Russell tercepat practice, Verstappen ke stewards — r1, r3, r7, r10
- India vs Selandia Baru kriket 159/1 / 239/1 — r3, r5, r6, r7, r10
- Anthropic IPO / Bayer Roundup $7,25 miliar — r2, r7

### Varian di dalam top 10

- r5 "forest v5", r9 "blue edition v4", r12 "bronze v5", r13 "burgundy v5":
  iterasi warna/tema dari template yang sama — bukti template ini diulang
  sampai menang.
- r6 "THE WORLD TODAY" (bukan "Saturday 21 November"): satu-satunya top 10
  dengan masthead koran klasik; tetap punya stat strip + 3 lead ilustrasi +
  peta + DATE CHECK. Satu pengecualian ini JUSTRU memasukkan "S&P 500 falls
  into correction" (Jumat) sebagai lead — minoritas 1 dari 10; 9 lainnya
  mengeluarkannya.
- r4 (30 cerita) membuktikan kepadatan bukan segalanya: 30 cerita + ilustrasi
  + peta mengalahkan 38 cerita teks saja.

## Entry kita (r1) — dibaca langsung

`entries/news-image-20261121/entry.png` 1024×1024, sha256 caf4fee2…,
36 cerita (2 lead + grid 4×9 bernomor 3–36), build-log.md dibaca.
Kualitas teknis BERSIH: tidak ada teks terpotong (assert TRUNCATION-RISK: none),
layout rapi, masthead "THE WORLD IN ONE DAY" + tanggal, 2 lead + grid bernomor,
strip SOURCES generik di bawah, footer. main.py stdlib-only (verifikasi, bukan
gambar ulang).

### Perbandingan dengan pola top 10

| Elemen pola | Top 10 | Entry kita |
|---|---|---|
| Tanggal sebagai headline raksasa | Ya (9/10) | Tidak — masthead nama koran yang besar, tanggal kecil |
| Strip 6 angka besar | Ya (10/10) | TIDAK ADA |
| Bar region + hitungan | Ya (10/10) | TIDAK ADA (hanya 4 label kategori di atas grid) |
| Lead berilustrasi (3) | Ya (10/10) | TIDAK ADA — lead hanya teks |
| Brief berilustrasi kecil (4–13) | Ya (10/10) | TIDAK ADA — grid teks seragam |
| "ALSO ON" daftar bernomor | Ya (10/10) | Tidak — semua 36 cerita dalam grid seragam |
| Peta dunia + pin bernomor | Ya (10/10) | TIDAK ADA |
| Kotak DATE CHECK / left-out | Ya (8–9/10) | TIDAK ADA |
| Sumber per cerita | Ya (10/10) | Tidak — satu strip generik |
| Kepadatan cerita | 30–38 | 36 ✅ (satu-satunya elemen yang sudah setara) |

### Cacat isi (dari perbandingan langsung dengan DATE CHECK top 10)

Cerita di entry kita yang menurut konsensus top 10 BUKAN berita Sabtu 21 Nov —
termasuk KEDUA lead:

- **#1 (LEAD) "Russian missile hits Poland during NATO exercise"** — rudal
  mendarat di Polandia itu berita JUMAT 20 Nov (DATE CHECK r1/r3/r6/r7).
  Sudut Sabtu yang benar: Rutte terbang ke Warsawa / NATO siaga.
- **#2 (LEAD) "Stocks slide into correction as AI shares plunge"** — koreksi
  Wall Street itu JUMAT 20 Nov (DATE CHECK r1/r3/r7; hanya r6 yang
  memasukkannya, minoritas 1/10).
- **#3 "UK and EU sign food and youth deals"** — deal UK–EU itu JUMAT 20 Nov
  (DATE CHECK r1/r7).
- **#11 "World court: Myanmar committed genocide"** — putusan ICJ itu KAMIS
  19 Nov (DATE CHECK r1/r3/r6/r7).
- **#12 "Trump, Xi, Putin summit ends flat"** — KTT Shenzhen itu KAMIS 19 Nov
  (DATE CHECK r1/r3/r6/r7).
- **#28 "Pill hailed as pancreatic cancer breakthrough"** — hasil pil kanker
  itu JUMAT 20 Nov (DATE CHECK r1).
- #36 "US police warn GTA 6 fans" — terkait rollout GTA VI 19 Nov (DATE CHECK
  r1 mencantumkan GTA VI sebagai left-out); borderline, bukan lead, risiko kecil.

Cerita Sabtu 21 Nov BESAR yang ADA di mayoritas top 10 tapi ABSEN dari entry kita:

- Gempa Peru M6.7 (lead di r7 & r10)
- Serangan Kyiv/Kryvyi Rih 12 tewas / 42 luka (r1, r3, r7, r10)
- Evakuasi Siklon Akvan 372.000 orang (r4, r6, r10)
- AS loloskan ~900.000 chip AI untuk China (r1, r2, r3, r5)
- UE €1 miliar bantuan militer Ukraina (r3, r5, r6)
- Rutte ke Warsawa (sudut Sabtu dari cerita Polandia) — kita punya rudalnya
  (Jumat), bukan kunjungan Rutte (Sabtu)

Cerita kita yang BENAR Sabtu dan sejalan dengan top 10: #4 COP31 overtime,
#14 Saudi cegat rudal Houthi, #27 BepiColombo (tapi terkubur di #27, padahal
ini lead di top 10), #15 Irak vs milisi, #16 vonis plot Sikh 19+ tahun,
#33 F1 Vegas, #31 Alcaraz–Cobolli (catatan: deck "Injured star completes a
perfect ATP Finals group stage" — Alcaraz tidak cedera; frasa "injured star"
meragukan; r10 menulis "Alcaraz beats Cobolli 6-4, 6-1 on Friday" — laganya
sendiri Jumat, tapi top 10 tetap memakainya sebagai brief olahraga).

### Estimasi skor r1 (konservatif, dikalibrasi preseden 20261120)

- Judge: **~94–96% (≈945.000–960.000 mikro)** — sekelas r1 kemarin (94,56%)
  karena formatnya sama (teks saja, tanpa ilustrasi/peta/stat strip) dan
  kebersihan tanggalnya LEBIH BURUK (kedua lead bukan berita Sabtu).
- Rank: **~1.200–1.700 dari ~1.951 entri yang sudah dinilai** (94,56% kemarin
  ≈ rank 1.575/1.951 di papan hari ini) — JAUH di luar garis hadiah top 50
  (98,52%).
- Probabilitas masuk top 50: praktis 0. Nilai submit r1 ini hanya sebagai probe
  berkalibrasi, bukan sebagai penantang hadiah.

## Kesimpulan analisis

Kepadatan sudah setara (36 cerita ✅). Yang memisahkan entry kita dari top 10
BUKAN jumlah cerita, melainkan tiga hal: (1) **kebersihan tanggal** — kedua lead
+ 4 cerita lain bukan berita Sabtu, padahal top 10 menjadikan DATE CHECK
sebagai pembeda utama; (2) **nol elemen visual** — tanpa ilustrasi, tanpa peta,
tanpa strip angka, gambar kita kalah telak dalam duel pairwise melawan halaman
yang kaya gambar; (3) **cerita Sabtu terbesar absen** — gempa Peru, serangan
Kyiv, Akvan, chip AI, bantuan UE €1 miliar tidak ada, sementara cerita
Jumat/Kamis mengisi slot lead.

Perbaikan r2 (1 sesi builder, tetap RINGAN — revisi murah): tukar 6 cerita
Jumat/Kamis dengan 6 cerita Sabtu di atas (Peru, Kyiv, Akvan, chip AI, UE €1bn,
Rutte ke Warsawa sebagai lead pengganti rudal Polandia); tambah strip 6 angka +
bar region; tambah peta titik + pin bernomor; tambah kotak DATE CHECK yang
menyebut eksplisit cerita yang dikeluarkan (ICJ, Shenzhen, rudal Polandia,
UK–EU, Wall Street, pil kanker) + tanggal aslinya; tambah ilustrasi datar
sederhana (PIL: bentuk geometrik) untuk 3 lead + ikon mini untuk brief 4–13;
tulis sumber per cerita; naikkan tanggal "Saturday 21 November 2026" jadi
headline besar di bawah kicker.
