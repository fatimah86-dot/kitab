# STATUS PELAKSANAAN AL-QORIN — 28 Oktober 2026

Status ini membedakan dengan tegas antara (a) restrukturisasi mekanis 123 unit,
(b) pilot 12 unit yang diselesaikan manual, (c) penajaman selektif sebagian
Lapis 4/5 pada 12 unit sasaran dari paket unggahan 2026-10-28, dan
(d) penyelesaian semantik menyeluruh yang belum dikerjakan. **Belum ada klaim
123/123 selesai semantik.**

Acuan terkunci: `../STANDAR_MUTLAK_AL_QORIN_123.md`.
Dokumen ini adalah revisi terjemahan dokumenter; praktik yang dinisbatkan
kepada penulis kitab tidak disajikan sebagai anjuran, terapi, atau jaminan
hasil, dan bukan pengganti penanganan medis.

## Sumber yang dipakai

- Teks yang direvisi: draf (4), Drive ID `1-keEWHFNdn4BancGVZVvdx0yVVezibZx`.
  Salinan lokal: 562.931 byte; SHA-256
  `27a66e84e8332f685b4ac944fe48feb6c5152033d327646ace003bb486ddeb71`.
- Kitab asli: PDF pindai 62 halaman citra, Drive ID
  `1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z` (tanpa lapisan teks). Salinan lokal:
  7.604.573 byte; SHA-256
  `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`.
- Crop wafaq: **26 berkas JPG presisi yang diunggah pengguna di chat**. FINAL
  KHATAM tidak lagi dipakai sebagai sumber crop.
- Paket pengganti yang diunggah pengguna pada 2026-10-28 disimpan di
  `incoming_user_2026-10-28/` sebagai **bahan kandidat/audit**, bukan master.
  Auditnya menunjukkan MD unggahan hanya mempunyai 89 blok, 0 crop, dan 0
  label, sedangkan DOCX pendamping hanya benar-benar memuat M104–M109 dalam
  empat blok; karena itu paket tersebut tidak menimpa master kanonis.
- Berkas biner Drive tidak di-commit; skrip mengharapkan salinan lokal draf dan
  PDF di `google_drive/` dengan nama yang sama seperti di Drive.

## Yang sudah selesai

1. **Struktur draf (4) terverifikasi**: SAMPUL + M01–M122 = 123 unit; setiap
   unit mempunyai tepat lima lapis lama; empat tabel terjangkar menurut urutan
   badan DOCX pada lapis lama 5 unit M65, M66, M67, dan M69.
2. **Crop presisi pengguna terpasang** (`scripts/al_qorin_stage_user_crops.py`):
   49, 58, 64–74, 76–78, 82–86, 98, 109, 116, 120, dan 121 — total 26.
   Semuanya disalin byte-identik ke `wafaq_qorin/<halaman>.jpg`, diverifikasi
   terhadap berkas unggahan, dan dicatat di `wafaq_user_manifest.json` serta
   `MANIFEST_WAFAQ_AL_QORIN.md`. Nama berkas dipakai persis sebagai halaman
   tujuan/unit M; `116.jpg` ditambahkan pada M116. Crop lama turunan FINAL,
   folder `crop_lain/`, skrip ekstraksi FINAL, dan DOCX kerja lama telah
   dikeluarkan dari pohon kerja saat ini.
3. **Restrukturisasi mekanis terlog** (`scripts/al_qorin_transform.py`) menjadi
   `REVISI_AL_QORIN_123_KERJA.md`:
   - 123 unit × 5 lapis baru dalam urutan terkunci (sejak amandemen lapis
     kondisional 2026-10-28: SAMPUL tampil 3 lapis, M01 dan M122 tampil
     4 lapis, sehingga total judul lapis tampil 611; data JSON tidak berubah).
   - Paragraf mandiri Qarinah yang dihapus: 569 (284 qabliah + 284 ba‘diah +
     1 paragraf gabungan di M01), ditambah 3 kalimat Qarinah sebaris dari
     paragraf campuran. Basis hitung terhadap angka perintah “288 paragraf”
     dicatat di `LOG_RESTRUKTUR_AWAL.md`. Kata qarinah sebagai pokok bahasan
     dalam Terjemahan tidak dihapus.
   - Label `[CATATAN PENERJEMAH ...]` utuh: 25.
   - Catatan ketidakpastian dari Syarah lama yang terselamatkan secara
     mekanis: 565 paragraf; dikte nahwu/Shorof/Hukum-baca tidak dibawa utuh.
   - Crop pengguna tersisip sesudah blok Metode: 26.
   - Saringan awal Penentuan Jam pada Arab/Latin/Terjemahan + Metode:
     3 unit memuat istilah jam, 0 unit memuat pola aritmetika penjumlahan,
     0 unit memenuhi keduanya; karena itu 123 unit sementara memakai teks
     persis «tidak ada hitungan di halaman ini». Kata `penjumlahan` pada draf
     sumber berjumlah 0, sehingga tidak ada penjumlahan jam yang dikarang.
4. **Pilot selesai manual** (`scripts/al_qorin_apply_pilot.py`,
   `overrides_pilot.json`) untuk SAMPUL, M01–M05, M58, M65–M67, M69, M122:
   Arab/Latin/Terjemahan/Metode tetap dari draf; Catatan penyunting dipilih
   dan dikelompokkan manual; Khususiyah unit wafaq diperbaiki pada tingkat
   frasa sumber; empat tabel transkripsi dipertahankan. Keluaran:
   `REVISI_AL_QORIN_PILOT.md` dan `AL_QORIN_PILOT_5_LAPIS.docx`.
5. **Master terintegrasi 123 unit** (`scripts/al_qorin_build_integrated.py`):
   12 unit pilot menggantikan versi mekanisnya di
   `REVISI_AL_QORIN_123.md` setelah builder memastikan Arab, Latin,
   Terjemahan, Metode, Penentuan Jam, tabel, dan nomor crop tidak berubah oleh
   substitusi pilot. Sesudah tahap pilot, builder menerapkan penajaman
   selektif terbatas dari `overrides_upload_selektif_2026-10-28.json` hanya
   pada M68, M70, M71, M104, M105, M106, M107, M109, M116, M120, M121, dan
   M122. Tahap ini hanya boleh mengubah frasa Khususiyah, menambahkan Catatan
   penyunting pada M104/M107, dan mengoreksi Metode M122 yang semula tidak
   cocok dengan Arab/Terjemahannya. Snapshot pasca-pilot dipakai untuk
   menegaskan bahwa heading, nomor halaman, Arab, Latin, Terjemahan,
   Penentuan Jam, tabel/blok rajah, label yang tertanam dalam teks, dan crop
   tidak berubah. Dengan pengecualian yang disengaja itu, blok terintegrasi
   M122 berbeda dari pilot historis hanya pada subbagian Metode.
6. **Builder Al-Qorin terpisah** (`scripts/build_docx_al_qorin.py`):
   Arab memakai `w:bidi=1` + `w:jc=start`; Latin memakai `w:bidi=0` +
   `w:jc=left`; paragraf crop dan sel tabel memakai `w:jc=center`; tabel
   draf tidak diberi `bidiVisual` karena tabel sumber tidak memilikinya.
   Amiri Regular/Bold/Italic/BoldItalic dari `fonts/` tertanam sebagai
   `word/fonts/*.odttf`; test memulihkan keempatnya byte-identik dari paket
   DOCX dan membandingkannya dengan TTF lokal. Keluaran utama:
   `AL_QORIN_REVISI_123_5_LAPIS.docx`.
7. **Preview HTML** (`scripts/build_preview_al_qorin.py`):
   `PREVIEW_INDEX_AL_QORIN_123.html` memuat 123 artikel, 611 lapis tampil, dan 26
   figure crop pengguna. Alias yang diminta,
   `PREVIEW_INDEX_HAL01-65.html`, dibuat di folder `al_qorin/` dengan isi sama;
   berkas root berjudul sama milik Anwar tidak ditimpa.
8. **Test** (`tests/test_al_qorin_pilot.py`): struktur 123 unit, log
   penghapusan, manifest/hash crop pengguna, substitusi pilot, batas sempit
   override selektif pasca-pilot, DOCX terintegrasi, preview,
   arah/alignment XML, tabel, media, dan embedding font. Test lama Anwar
   tetap dijalankan; seluruh 22 test lulus sesudah integrasi selektif,
   amandemen lapis kondisional, batch semantik M16–M64, batch semantik
   M06–M15/M72–M121, dan batch terakhir M68/M70/M71.
9. **Amandemen lapis kondisional + arsip unggahan M65** (2026-10-28): sesuai
   keputusan pengguna, SAMPUL kini tampil 3 lapis (empat catatan sampul
   dipindah ke akhir Lapis 3), M01 (Muqodimah) dan M122 (Khatimah) tampil
   4 lapis, dan 120 unit lain tetap 5 lapis; diterapkan reproduksibel lewat
   `LAYER_LIMITS`/`render_unit_md` bersama di `scripts/al_qorin_transform.py`.
   Dua DOCX M65 dan gambar Khatam Sulaiman dari sesi lain diaudit lalu
   diarsipkan di `incoming_user_2026-10-28/` (lihat `AUDIT_M65_UPLOAD.md`)
   tanpa menimpa M65 kanonis, yang sudah memuat crop yang sama pada resolusi
   lebih tinggi.
10. **Batch semantik M16–M64** (`overrides_batch_m16_m64.json`, tahap
    pasca-pilot kedua di `scripts/al_qorin_build_integrated.py`): 49 unit
    dikurasi setingkat pilot. Catatan penyunting hanya dipilih/dikelompokkan
    dari catatan lama yang terselamatkan (tanpa teks catatan baru; transisi
    berboilerplate dan catatan usang dibuang), Khususiyah ditulis ulang pada
    tingkat frasa dari Arab/Terjemahan/Metode unit (termasuk aturan
    siang–malam dan bakhur M50–M54 serta crop M49/M58/M64), dan lima stub
    Metode kata-kunci positif-palsu (M19, M20, M21, M38, M46) dikoreksi.
    Builder menegaskan Arab/Latin/Terjemahan, Penentuan Jam, tabel/blok
    rajah, dan crop tidak berubah; ringkasan Metode draf selain lima stub itu
    dipertahankan. Rincian: `CATATAN_BATCH_M16_M64.md`.
11. **Batch semantik M06–M15 dan M72–M121**
    (`overrides_batch_m06_m15_m72_m121.json`, tahap ketiga sesudah pilot,
    selektif, dan M16–M64): 60 unit dikurasi setingkat pilot. Catatan
    penyunting hanya dipilih dari catatan lama (tanpa teks catatan baru;
    boilerplate generik, fragmen Latin, dan dikte saraf dibuang; peringatan
    editorial serta catatan beda pindaian M104/M107 dipertahankan).
    Khususiyah ditulis pada tingkat frasa dari Arab/Terjemahan unit,
    termasuk jadwal riyadhah M11–M15, waktu terbenam dan bakhur M75,
    saat baik/bakhur M84, dan mulai Ahad M98. Empat Metode dikoreksi hanya
    karena stub atau kontradiksi material terbukti: M12 (stub kata kunci →
    jadwal 80 hari), M79 (pelepah hijau + cendana, bukan kertas/kemenyan),
    M82 (dikuburkan di pintu sasaran), dan M83 (kertas diasapi; tidak ada
    instruksi menggantung). Builder/test menegaskan Arab/Latin/Terjemahan,
    Penentuan Jam, `rajah_blocks`, dan crop tidak berubah; unit tumpang-tindih
    selektif memakai baseline pasca-selektif. Rincian:
    `CATATAN_BATCH_M06_M15_M72_M121.md`.
12. **Batch terakhir M68, M70, M71** (`overrides_batch_m68_m70_m71.json`,
    tahap final sesudah semua batch sebelumnya): ketiga unit yang semula
    hanya menerima penajaman selektif kini dikurasi setingkat pilot. Catatan
    substantif dipilih dari baseline pasca-selektif; Khususiyah diperinci
    dari Arab/Terjemahan dan crop `68.jpg`, `70.jpg`, `71.jpg`, termasuk QS
    al-Kahf 18:25 (M68), tulisan spesifik kedua telapak dan bakhur (M70),
    serta delapan posisi ṭā’ (M71). Satu koreksi Metode dibatasi pada
    paragraf pertama M71: ayat disebut **dipanaskan** (bukan dibakar) dengan
    bahan dari kambing hitam yang zat persisnya tidak dipastikan; paragraf
    deskripsi transparan rajah sesudahnya dipertahankan byte-identik.
    Dengan batch ini seluruh 123 unit telah masuk pilot atau salah satu
    batch semantik Lapis 4/5. Rincian: `CATATAN_BATCH_TERAKHIR_M68_M70_M71.md`.

## Yang belum selesai

- Tidak ada lagi unit yang menunggu batch semantik Lapis 4/5: seluruh 123
  unit telah masuk pilot atau salah satu batch semantik. Batas kejujuran
  tetap berlaku: pemeriksaan Penentuan Jam terhadap Arab serta pindai
  halaman bersifat dokumenter dan tidak mengarang hitungan; selisih bacaan
  M104 dan M107 sengaja belum dipakai untuk mengganti Lapis 1–3. Semua
  batch semantik tidak menerjemahkan ulang Lapis 1–3, tidak menggambar
  ulang rajah, dan tidak menulis ulang ringkasan Metode draf selain stub/
  kontradiksi yang terbukti pada daftar izin masing-masing batch.
- Pemetaan halaman cetak individual M01–M04 belum dibuktikan; tidak ada crop
  pada rentang itu. Untuk M05–M121 nomor unit sama dengan halaman cetak, dan
  M122 adalah penutup tanpa nomor terbaca.
- Proof visual di Microsoft Word/LibreOffice belum dilakukan di lingkungan
  ini; verifikasi DOCX saat ini berbasis python-docx dan inspeksi XML/paket.
- Tidak ada berkas hasil yang diunggah kembali ke Google Drive dan tidak ada
  dokumen Drive yang ditimpa.

## Perintah reproduksi

```bash
.venv/bin/python scripts/al_qorin_stage_user_crops.py
.venv/bin/python scripts/al_qorin_transform.py
.venv/bin/python scripts/al_qorin_apply_pilot.py
.venv/bin/python scripts/al_qorin_build_integrated.py
.venv/bin/python scripts/build_docx_al_qorin.py
.venv/bin/python scripts/build_docx_al_qorin.py \
  --input al_qorin/REVISI_AL_QORIN_123.md \
  --output al_qorin/AL_QORIN_REVISI_123_5_LAPIS.docx
.venv/bin/python scripts/build_preview_al_qorin.py
.venv/bin/python -m unittest discover -s tests -v
```
