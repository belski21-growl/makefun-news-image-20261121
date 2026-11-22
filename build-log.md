# Build log — news-image-20261121

Kompetisi: "Sum up 21 November's world news in one image" ($100, deadline
23 Nov 2026 00:00 UTC = 23 Nov 07:00 WIB). Kuota live saat build:
entries_made 0, day left 3, hard left 20, can_submit TRUE (≥2 ronde →
strategi submit-cepat; build ini HANYA build — tidak submit, tidak buat repo).

## Classification
- classification: **ringan** (gambar, 1 sesi builder, revisi murah)
- effort_estimate: 1 sesi builder. Alasan: entry gambar statis, digambar
  sekali dengan PIL dari daftar cerita tetap; sekali revisi = edit teks +
  re-render, murah; tidak butuh box, trial, atau multi-milestone.

## Langkah
1. Baca kit fresh (`RULES.txt`, `competition.yaml`, `kit.json`) + template
   README dari `GET /api/competitions/news-image-20261121/requirements`
   (`how_to_submit.readme_template`, `repo_about`).
2. Riset berita 21 Nov 2026 via web search (BBC/Reuters/AP/AFP/ESA):
   3 batch pencarian (headline umum, Asia/Afrika/Timur Tengah/COP31,
   olahraga, sains) + verifikasi silang antar-sumber untuk angka.
3. Tulis `generate.py` (PIL + DejaVu, tool build lokal — TIDAK dijalankan
   grader): front page koran 1024x1024, masthead + 2 lead + grid 4×9
   berisi 34 cerita bernomor + strip sumber. Total 36 cerita.
4. Render v1 → tinjau visual: headline lead menabrak deck; banyak
   headline/deck terpotong "...". Perbaiki: lead ditinggikan (128→136px,
   headline 26→24px, deck dipindah ke posisi tetap), semua headline
   dipendekkan (≤44 karakter) dan deck (≤68 karakter), font grid 15→14px
   dan deck 12→11px.
5. Render v2 → tinjau visual: masih ada 3 pemotongan (#5, #7, #33).
   Pendekkan ketiganya; render v3 + assert otomatis: tidak ada headline/
   deck yang butuh >2 baris (TRUNCATION-RISK: none).
6. Tulis `main.py` dari nol di sesi ini (pesan asisten 1: file lengkap;
   pesan asisten 2: tambah pengecekan byte-equality output vs source).
   Program stdlib-only: verifikasi entry.png (ukuran + SHA-256 + signature
   PNG + IEND), salin ke output dir, verifikasi ulang hasil salinan.
7. Tulis `LICENSE` (MIT + SPDX), `README.md` (3 badge live + link bounty
   dari template requirements), `build-log.md` ini.
8. Validasi (lihat bawah).

## Fakta yang diverifikasi + sumber
- Rudal Rusia jatuh di Polandia saat latihan NATO; PM Tusk: provokasi
  disengaja; NATO: pelanggaran berat wilayah udara — BBC.
- S&P 500 & Dow masuk koreksi; saham AS jatuh ~3,7% Jumat; Nvidia
  −22,9% dalam 5 sesi, minggu terburuk sejak Okt 2008 — BBC.
- ICJ: Myanmar melakukan genosida terhadap Rohingya — BBC/OneTurn.
- UK–EU sepakati 3 deal (pangan, karbon, youth mobility), PM Andy
  Burnham, Brussels — BBC.
- COP31 Antalya overtime; draf hapus kata fossil fuel; teks ke-3 Sabtu
  pagi; Okt 2026 1,8°C di atas pra-industri (Berkeley Earth) — AP/Reuters.
- KTT trilateral Trump–Xi–Putin pertama di Shenzhen, hasil konkret
  minim — OneTurn/BBC.
- Perang Iran bulan ke-9; Trump tak buru-buru, mungkin putuskan 2027 —
  OneTurn.
- Koalisi Saudi cegat 3 rudal Houthi di atas Riyadh, serang Hodeidah —
  OneTurn.
- Polisi Prancis divonis atas pemukulan produser Michel Zecler 2020,
  rasisme sebagai pemberat — BBC.
- Mamdani umumkan rencana tutup penjara Rikers Island 2032 — BBC.
- Juri LA vonis Jonathan Rinderknecht bersalah membakar Palisades Fire
  — OneTurn.
- Harry Kane cedera ligamen pergelangan kaki, absen berbulan-bulan;
  Bayern 1–1 Köln — BBC/NewKerala.
- Alcaraz kalahkan Cobolli 6–4, 6–1; grup ATP Finals sempurna — BBC.
- BepiColombo masuk orbit Merkurius 21 Nov setelah 8 tahun; sains mulai
  Apr 2027; MPO/Mio pisah 9–10 Des — ESA/SciAm/NatGeo.
- Pill terobosan kanker pankreas; klaim AI bantu bukti Riemann
  Hypothesis (disajikan sebagai klaim/debat, bukan fakta) — BBC/Threads.
- ANC lawan pertahankan kota-kota kunci Afsel pasca-kekalahan pemilu;
  ~600 perempuan dibunuh di Afsel dalam 3 bulan — BBC.
- Estonia tutup perbatasan dengan Rusia; Denmark gagalkan plot Rusia
  bunuh rapper AS-Ukraina; mogok sektor publik Portugal; deal
  kepemimpinan ECB Prancis–Jerman; Lufthansa pangkas 1.000 pekerjaan;
  operasi Irak vs milisi pro-Iran; lelang tambang laut dalam Pasifik AS;
  vonis 19+ tahun plot bunuh pemimpin separatis Sikh; PM Nepal Balendra
  Shah uji India; perang Sudan & pendidikan anak disabilitas; eksekusi
  Texas >1 jam; Trump soal sistem penerbangan AS; UFO dideklasifikasi;
  Price kalahkan Kotaskova; F1 Vegas Russell–Verstappen; Kim hole-in-one
  LPGA; Inggris vs All Blacks; polisi AS peringatkan fans GTA 6 —
  BBC/Daily Debrief/Global24.
- Angka yang dipakai di gambar HANYA yang terlihat di sumber di atas
  (3,7%; 22,9%/5 sesi; 1.000; 19 tahun; 600/3 bulan; 8 tahun; 6–4, 6–1;
  1–1). Tidak ada angka karangan. Pelajaran ronde lalu (Nikkei vs Kospi)
  dihindari: tidak ada klaim soal Nikkei/Kospi sama sekali.

## Validasi
- entry.png: PNG 1024x1024, 182137 byte (≤1 MiB), PIL decode OK.
- sha256 entry.png: caf4fee284de925e1a6c990e613f09f2d5a332c471904203e8194e975a3f62f8
- main.py 2x run ke dir berbeda: byte-identik (sha256 sama dengan
  entry.png di kedua run).
- main.py: stdlib-only (hashlib, os, sys, pathlib); tanpa network;
  tanpa timestamp/random → deterministik.
- README: 3 badge live make.fun kompetisi ini + link bounty (template
  requirements, owner belski21-growl, repo makefun-news-image-20261121,
  ref quick-lynx-56).
- LICENSE MIT + baris SPDX-License-Identifier.
- Tidak ada submit; tidak ada repo GitHub dibuat (parent yang urus).

## ROUND 2 — revisi Goldfish (21 Nov 2026 ~14:30 WIB)
Goldfish review r1 (lihat submissions.md): LAYAK LANJUT, BELUM LAYAK SUBMIT —
5 blocker (B1–B5) + 4 major (M1–M4). r2 memperbaiki semuanya; generate.py
ditulis ulang mengikuti template top-10 ("The World in One Day").

### Perubahan vs r1
- B1/B2 — 6 cerita Jumat/Kamis DIGANTI (lead + grid lama dibuang):
  keluar: rudal Polandia (Jumat), koreksi Wall Street (Jumat), deal UK–EU
  (Jumat), putusan ICJ Myanmar (Kamis), KTT Shenzhen (Kamis), pil kanker
  pankreas (Jumat). Masuk: Rutte ke Warsawa (lead 1), gempa Peru M6.7
  (lead 2), serangan Kyiv/Kryvyi Rih 12 tewas 42 luka (lead 3), evakuasi
  Siklon Akvan 372.000 (#7), AS loloskan ~900.000 chip AI (#8), UE €1 miliar
  bantuan Ukraina (#9). Total tetap 36 cerita: 3 lead + 10 brief (4–13) +
  23 "ALSO ON SATURDAY" (14–36).
- Cerita ke-36 (tambahan, bukan pengganti): India 239/1 vs Selandia Baru
  (#12, kriket Test hari ke-3 Sabtu — terverifikasi AP/PTI).
- B3 — cerita Sabtu terbesar kini hadir semua: Peru, Kyiv/Kryvyi Rih,
  Akvan, chip AI, UE €1bn, Rutte — plus COP31, Riyadh, BepiColombo.
- B4 — elemen visual baru: ilustrasi datar PIL untuk 3 lead (skyline
  Warsawa + bintang NATO; Andes + seismograf; langit malam Kyiv +
  ledakan); 10 ikon mini untuk brief 4–13 (planet, globe, perisai,
  siklon, chip, euro, kaca pembesar, bendera kotak, kriket, tenis);
  peta dunia + 13 pin bernomor (lead merah, brief biru; #4 BepiColombo
  "in orbit" di sudut peta); strip 6 angka besar; bar region
  (Europe 13 · Asia 4 · Middle East 3 · Africa 3 · Americas 9 ·
  Oceania 1 · Global 3 = 36).
- B5 — kotak DATE CHECK baru: 7 cerita yang SENGAJA dikeluarkan +
  tanggal aslinya (rudal Polandia, Wall Street, UK–EU, pil kanker —
  Jumat 20 Nov; ICJ Myanmar, KTT Shenzhen — Kamis 19 Nov; GTA VI
  rollout — 19 Nov).
- M1 — tanggal "Saturday 21 November 2026" kini headline terbesar
  (serif 46px) di bawah kicker "THE WORLD IN ONE DAY" + sub-headline
  3 cerita utama.
- M2 — sumber per cerita: kicker tiap lead/brief mencantumkan sumber
  (AP/Reuters/BBC/ESA/USGS/IMD/EU Council); tiap item ALSO ON diakhiri
  (sumber); strip SOURCES di bawah.
- M3 — hierarki visual: 3 lead besar → 10 brief berikon → daftar
  "ALSO ON SATURDAY — 23 MORE STORIES" → peta → DATE CHECK.
  BepiColombo naik dari #27 (r1) ke #4 (brief).
- M4 — deck Alcaraz diperbaiki: "Injured star completes a perfect..."
  → "Alcaraz beats Cobolli 6-4, 6-1 / Perfect group stage at the ATP
  Finals in Turin." (Alcaraz tidak cedera.) GTA 6 keluar dari daftar
  cerita, masuk DATE CHECK sebagai left-out (rollout 19 Nov).

### Verifikasi tanggal 6 cerita pengganti (web search, 21 Nov ~14:25 WIB)
- Peru M6.7: 00:09 UTC Sabtu 21 Nov (19:09 Jumat waktu Peru), 30 km
  dari Junin, tanpa korban — USGS/AP. ✅ Sabtu (UTC).
- Kyiv/Kryvyi Rih: serangan semalam 20→21 Nov; toll diperbarui Sabtu
  pagi — 12 tewas, 42 luka, double-tap Kryvyi Rih, 3 jembatan Kyiv
  rusak — Reuters/AP/Kyiv Independent. ✅ (angka 12/42 sesuai konsensus
  top-10 r1/r3/r7/r10.)
- Rutte ke Warsawa: kunjungan Sabtu 21 Nov, bertemu Tusk — AP/Reuters. ✅
- Akvan: landfall Jumat 20 Nov pagi, TAPI outcome zero-casualty +
  372.000 dievakuasi dilaporkan Sabtu; top-10 r4/r6/r10 memasukkannya
  sebagai cerita Sabtu. Deck ditulis jujur tanpa klaim tanggal landfall.
  ⚠️ nuansa dicatat di sini, bukan disembunyikan.
- Chip AI ~900.000: disclosure Komite DPR AS Kamis 19 Nov (Reuters),
  dilaporkan luas Jumat–Sabtu; top-10 r1/r2/r3/r5 memasukkannya.
  Deck: "House panel: 879,000 Nvidia, AMD chips approved in six months."
  ⚠️ nuansa dicatat di sini.
- UE €1 miliar: diputuskan Dewan UE Jumat 20 Nov, dilaporkan Sabtu pagi
  (rilis Consilium 20 Nov; liputan 21 Nov 08:07 WIB); top-10 r3/r5/r6
  memasukkannya. ⚠️ nuansa dicatat di sini.
- Kriket India–NZ: 239/1 saat makan siang hari ke-3, Sabtu 21 Nov,
  Rahul 93*, Padikkal 53*, NZ 368 — AP/PTI. ✅
- BepiColombo 19:24 CET, COP31 draf ke-3 Sabtu, Riyadh 3 rudal —
  sudah terverifikasi di r1 (build-log atas).

### Validasi r2
- entry.png: PNG 1024x1024, 184167 byte (≤1 MiB), PIL decode OK.
- sha256 entry.png: 311e9294f741ada4c6cc7fcbab35ca6ac7ad50c078b0c1476a49d765e7722b0f
- main.py diperbarui ke ukuran + sha256 r2; 2x run ke dir berbeda:
  byte-identik (sha256 sama dengan entry.png di kedua run).
- generate.py: TRUNCATION-RISK: none (assert otomatis tiap render).
- Tinjau visual 3x (halaman penuh + zoom peta 2x): tidak ada teks
  terpotong; pin 1–13 terbaca (pin 1/3 sempat bersentuhan → nudges
  diperbaiki; pin 7 sempat di laut → semenanjung India ditambah;
  pin 12 sempat di laut → blob Selandia Baru ditambah).
- main.py tetap stdlib-only, deterministik; tidak ada submit; tidak ada
  repo GitHub dibuat (parent yang urus). Menunggu Goldfish re-review r2.

## Revisi mini r3 (21 Nov ~15:10 WIB — sesi ini, per Goldfish re-review r2)
- Konteks: Goldfish re-review r2 (14:42 WIB): semua B1–B5 + M1–M4 TERTUTUP,
  tapi 1 blocker baru (N1 pin 8) + 1 minor baru (N2 dateline). Perbaiki
  HANYA 2 hal itu — tidak ada perubahan lain.
- N1 — pin 8 (Washington, cerita chip AI #8) di r2 salah koordinat:
  `(8, 116.4, 39.9)` = Beijing, Tiongkok — itulah sebabnya pin 8
  mendarat di tengah blob Eurasia. Diperbaiki ke `(8, -77.0, 38.9)` =
  Washington DC (lon −77,0, lat 38,9). Pin 11 Las Vegas (−115,1, 36,2)
  tidak disentuh.
- N1 tambahan (murah, tanpa regresi): pin 5 Antalya dy +4 → −6 — kini
  duduk di celah Mediterania antara blob Eropa dan Afrika, bukan lagi di
  dalam blob Afrika. Blob Selandia Baru diperbesar sedikit
  (0.94–0.975 → 0.935–0.982) supaya pin 12 lebih terbaca.
- N2 — kicker cerita #12 "WELLINGTON  •  AP" → "GUWAHATI  •  AP"
  (Test India vs Selandia Baru dimainkan di Guwahati, India).
  grep: "WELLINGTON" 0 kemunculan, "GUWAHATI" 1; "116.4" tidak ada lagi.
- Edit generate.py dalam 2 pesan asisten terpisah (PINS + blob NZ, lalu
  kicker Guwahati); main.py hanya di-update ukuran + sha256 (logika
  tidak berubah, tetap stdlib-only).

### Validasi r3
- entry.png: PNG 1024x1024, 184256 byte (≤1 MiB), PIL decode OK.
- sha256 entry.png: 02b55055f71cfaa279dc0c3ba59abe609db748753574cd1766e8b77d7fa8ebf8
- main.py diperbarui ke ukuran + sha256 r3; 2x run ke dir berbeda
  (/tmp/val-r3a, /tmp/val-r3b): byte-identik (sha256 sama dengan
  entry.png di kedua run) — DETERMINISTIK-OK.
- generate.py: TRUNCATION-RISK: none.
- Tinjau visual (halaman penuh + zoom peta 2x + zoom brief 12):
  pin 8 di Amerika Utara, pantai timur, di kanan pin 11 (Las Vegas);
  pin 11 tetap benar; pin 5 di celah Mediterania; pin 12 di blob NZ
  yang diperbesar; kicker #12 terbaca "GUWAHATI  •  AP"; tidak ada
  teks terpotong di halaman penuh.
- main.py tetap stdlib-only, deterministik; tidak ada submit; tidak ada
  repo GitHub dibuat (parent yang urus). Sesuai catatan Goldfish:
  setelah r3 TIDAK perlu Goldfish full review lagi — parent cukup
  verifikasi zoom peta + sha baru, lalu lapor siap-submit ke user.

## Micro-fix r2 (22 Nov ~14:10 WIB — sesi ini, per Goldfish re-review r2)
- Konteks: Goldfish re-review r2 (14:05 WIB): B1–B4 TERTUTUP, B5 SEBAGIAN (chip cuma di 3 lead), N1 tabrakan label UTC "quake05:00", N2 pin 1 tertutup pin 6. Estimasi apa adanya rank ~100–250, peluang top 50 ~20–35%; setelah micro-fix ~25–40%.
- Fix (5 edit generate.py):
  1. N1 — label UTC pertama "Peru M6.7 quake" → "Peru quake" (tabrakan hilang, terverifikasi visual crop UTC).
  2. B5 — chip_small() baru (10px, SANS_B 7, right-aligned) + chip CONFIRMED/OFFICIAL di tiap brief 4–13 di baris celah antara kicker dan headline (y+17); kicker penuh jadi chip tidak muat di baris kicker (diukur: semua kicker 87–134px, chip 51–64px). Terverifikasi visual crop briefs: 5 chip pertama terbaca (OFFICIAL/CONFIRMED).
  3. N2 — pin 1 Bahrain dx/dy 0,0 → +12,-10 (jarak ke pin 6 Riyadh ~19px, keduanya terbaca; terverifikasi visual crop peta).
  4. N3 — deck #2 "30 km from Junin" → "near Carhuamayo" (hindari ambiguitas kedalaman vs 108–129 km).
  5. main.py diperbarui ke ukuran + sha256 baru.
- Validasi: entry.png baru 196.311 B, sha 89e401cef5d135cc44a7828bdfe49abc9d2f21cb6be314cdc4b009aa072bd865, SOI/IEND OK, full decode OK (1024×1024 RGB), TRUNCATION-RISK: none. main.py lolos cek venv TANPA PIL (python3 -P -s, exit 0, 2 run byte-identical, PIL tidak bisa di-import di venv).
- M1 (ilustrasi mini brief) TIDAK dikerjakan — layout tidak muat, sudah diputuskan (plafon skor tetap di bawah garis hadiah tanpa M1).

## Rebuild art r3c (22 Nov ~15:00 WIB — sesi ini, per perintah tegas user)

- Konteks: Goldfish r3b LAYAK LANJUT (borderline) — rank ~25–60 (tengah ~30–50),
  peluang top 50 ~45–60%, top 25 ~30–45%, top 10 ~5–10%. Gap tersisa KUALITAS
  ART, bukan struktur (M4 brief masih bentuk datar primitif, M5 COP31 masih
  ikon, M6 peta blob). User 14:56 WIB: "tingkatkan kualitas artnya, kalo perlu
  rebuild ulang. Pegang aturan tegas itu, gak ada alasan ketinggalan kualitas
  art." + aturan FOKUS TIDAK DIBATASI (22 Nov ~14:58 WIB): kejar SEMUA
  kekurangan yang menghalangi top 10, bukan cuma satu area.
- Skill art yang dipakai (semua dibaca penuh): canvas-design (adegan bercerita,
  depth berlapis, craftsmanship), design-dna (token + style + effects),
  algorithmic-art (pola deterministik, tanpa randomness), image-entry
  (verifikasi SOI/EOI + full decode + 2-run byte-identical).
- Studi art top 1/10/20 dilihat langsung + ditulis di top10-analysis.md
  (bagian "Studi ART top 1/10/20"): adegan bukan ikon, depth berlapis,
  objek dikenali, data sebagai visual, kontras gelap/terang, peta dikenali.
- Rebuild (modul BARU art_scenes.py, ditulis dari nol):
  1. Lead #1 Teluk: kanal laut berlapis (depth bands), kapal tanker dikenali
     (lambung + superstruktur + cerobong + asap) x2, busur rudal x2, label
     KHASAB ditambahkan.
  2. Lead #2 Gempa: pegunungan berlapis (salju + sisi teduh), marker episentrum
     (cincin konsentris + bintang merah).
  3. Lead #3 COP31: ADEGAN DATA ala rank 1 — grid tanggal 9–21 (21 merah) +
     "NOV 9–20 SCHEDULED" + "+1 DAY" + termometer 1.5°C + globe + delegasi.
  4. Brief 4–13: tiap strip jadi adegan mini berlapis — #4 satelit panel surya
     biru + Merkurius berkawah, #5 api berlapis + skyline (jendela dijauhkan
     dari teks, m1 TERTUTUP), #6 rudal + jet dikenali, #7 borgol + sorot lampu
     + badge FBI, #8 papan sirkuit + chip emas, #9 medali € + cincin bintang,
     #10 kaca pembesar + figur bayangan + X merah, #11 bendera kotak berkibar +
     mobil F1, #12 bat + bola berjahit + stumps, #13 jet putih + skyline
     Warsawa + bintang NATO.
  5. M6 peta: poligon benua ditulis ulang dengan lebih banyak titik (Amerika
     Utara/Selatan, Afrika, Eropa, Asia + India + Jepang + Madagaskar,
     Australia) — kini dikenali, setara rank 20.
  6. Struktur/fakta/DATE CHECK/UTC/stat strip TIDAK disentuh.
- Validasi visual: halaman penuh + crop 3x (Teluk, COP31, gempa, brief 4/5/7/13,
  baris brief 1+2, peta) — 0 tabrakan, 0 teks terpotong; m1 (kotak kuning #5)
  TERTUTUP; grid COP31 9–21 terbaca penuh; semua label lead terbaca.
- Validasi: entry.png baru 217.521 B, sha 343479fff05ad69936c1a951c0f6fbd076fb8d9fd004e8e7a7537e511d932e72, SOI/IEND OK, full decode OK (1024×1024 RGB), TRUNCATION-RISK: none. main.py lolos cek venv TANPA PIL (python3 -P -s, exit 0, 2 run byte-identical, py_compile OK).

## Poles art r3d (22 Nov 2026 ~15:30 WIB — sesi ini, per Goldfish r3c §3)

- Konteks: Goldfish r3c LAYAK SUBMIT borderline atas — rank ~12–35
  (tengah ~20), top-50 70–85%, top-10 15–25%. Sisa gap art: M8 depth,
  M9 peta blob, M10 #11/#6 kasar, minor m2/m4/m5/m6. Aturan tegas:
  CHASE-TOP-10 (target rank TOP 10, lantai 25, top-50 >=30% target
  50%+), FOKUS TIDAK DIBATASI, SANGGUP-SANGGUPIN. Edit dalam 3 pesan
  asisten terpisah (modul baru -> generate.py -> art_scenes.py).
- Modul BARU art_polish_r3d.py (ditulis dari nol): helper
  soft_vertical_gradient (per-baris, tanpa garis blok), soft_shadow
  (3 elips konsentris), sea_glints, sea_edge_vignette, CONTINENTS_V2
  (186 titik vs 101 r3c), strip_shield_v2, strip_flag_v2.
  generate.py: import modul baru, peta pakai CONTINENTS_V2, strip #6/#11
  pakai v2, legenda + REPORTED. art_scenes.py: hanya call-site +
  import (scene_gulf + scene_cop31). Struktur/fakta/DATE CHECK/UTC/
  stat strip/ALSO ON/teks headline/deck TIDAK disentuh; lead #2 TIDAK
  disentuh; PINS tidak disentuh/digeser.
- M8 — TERTUTUP (sebagian besar): COP31 latar kini gradasi vertikal
  halus mint -> mint muda -> nyaris putih (digambar dulu, objek tetap
  di atas) + bayangan lembut di bawah globe; Teluk: bayangan lembut di
  bawah kedua tanker + 2 kilau air tipis + vignette sangat tipis di
  tepi kiri/kanan zona laut (atas/bawah sengaja tidak disentuh:
  label IRAN di atas, daratan tan di bawah). Efeknya sengaja halus —
  terbaca di crop 2x sebagai kedalaman, bukan sebagai blok gelap.
- M9 — TERTUTUP: CONTINENTS_V2 — Amerika Utara (lekuk Hudson Bay,
  Alaska, lancip Meksiko), Amerika Selatan meruncing, Afrika
  (tonjolan barat + meruncing selatan), Eropa dikenali (Skandinavia,
  Rusia, Iberia, tumit Italia, Anatolia), Asia (Melayu + India +
  Arabia + lekuk Teluk Persia), Australia, Greenland, Madagaskar,
  Jepang, Britania, Selandia Baru dipertahankan. TEMUAN PENTING:
  diuji point-in-polygon, di r3c pin 1/3/5/6/9 (posisi digambar)
  jatuh di LAUT; V2 menutup celah itu — kini 12/12 pin darat di atas
  daratan (uji otomatis + visual crop 2x). Benua kini dikenali.
- M10 — TERTUTUP: #11 F1 kini 2 roda hitam besar + hub putih +
  kanopi putih + sayap belakang jelas (kontras di latar gelap,
  terbaca sebagai mobil F1); #6 jet kini putih/perak terang +
  jendela kokpit gelap.
- m4 — TERTUTUP, dengan koreksi jujur: diukur PIL, "3 DOWN" berakhir
  x+94.6 dan "W" di 57.8–78.7 — starburst lama (x 54–70) menabrak W,
  dan geser literal +5px (59–75) MASIH di dalam W. Jadi starburst
  pertama dipindah ke (x+102, y+21) r7, di ujung trail misil-2 —
  "3 DOWN" kini utuh bersih tanpa sentuhan oranye (crop 2x).
- m2 — TERTUTUP: legenda kini "... OFFICIAL = official source  •
  REPORTED = single source" — 480,5px, muat satu baris (batas 626px),
  terverifikasi visual satu baris penuh.
- m5 — TERTUTUP: kedua tanker lead #1 dibesarkan ~20% (40x9 -> 48x11,
  34x8 -> 41x10), tetap terbaca + KHASAB utuh.
- m6 — TERTUTUP: garis meja COP31 ditebalkan + 2 lembar dokumen putih
  di depan siluet delegasi (terbaca sebagai kertas di meja).
- Catatan jujur: asap cerobong tanker-1 masih menjorok ~11px di atas
  tepi panel (SUDAH ADA di r3c, bukan cacat baru, Goldfish tidak
  flag) — tidak disentuh supaya tidak merombak _ship.
- Validasi visual (halaman penuh + crop 2x lead #1, lead #3, peta,
  strip #6, strip #11, legenda): gradasi COP31 terbaca (atas mint,
  bawah nyaris putih); bayangan globe ada; bayangan/kilau Teluk
  halus tapi ada; semua label lead terbaca penuh (IRAN, BAHRAIN,
  KHASAB, 2 TANKERS HIT, STRAIT OF HORMUZ); benua dikenali; roda +
  kokpit F1 terbaca; jet #6 putih; "3 DOWN" bersih; tier REPORTED
  ada; 0 tabrakan/teks terpotong baru; TRUNCATION-RISK: none.
- Validasi: entry.png baru 219.699 B, sha
  6f49c2475a6303dce728fd46d68e5ab9c1db7ed6b930b6e3dd5f5662029cc70e,
  SOI/IEND OK, full decode OK (1024x1024 RGB). main.py HANYA
  ARTWORK_SIZE + ARTWORK_SHA256; cek venv TANPA PIL (venv baru
  ~/workspace/tmp-workspace/venv-nopil-r3d — /tmp/venv-nopil lama
  sudah tidak ada): python3 -P -s main.py exit 0, 2 run ke dir
  berbeda byte-identical dengan entry.png. TIDAK commit/bundle/check
  kit — urusan koordinator.
