# STATUS PELAKSANAAN AL-QORIN — 28 Oktober 2026

Status ini membedakan dengan tegas antara (a) restrukturisasi mekanis 123 unit,
(b) pilot 12 unit yang diselesaikan manual, dan (c) penyelesaian semantik yang
belum dikerjakan. **Belum ada klaim 123/123 selesai semantik.**

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
   - 123 unit × 5 lapis baru dalam urutan terkunci.
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
   `REVISI_AL_QORIN_123.md` setelah test memastikan Arab, Latin, Terjemahan,
   Metode, Penentuan Jam, tabel, dan nomor crop tidak berubah oleh substitusi.
6. **Builder Al-Qorin terpisah** (`scripts/build_docx_al_qorin.py`):
   Arab memakai `w:bidi=1` + `w:jc=start`; Latin memakai `w:bidi=0` +
   `w:jc=left`; paragraf crop dan sel tabel memakai `w:jc=center`; tabel
   draf tidak diberi `bidiVisual` karena tabel sumber tidak memilikinya.
   Amiri Regular/Bold/Italic/BoldItalic dari `fonts/` tertanam sebagai
   `word/fonts/*.odttf`; test memulihkan keempatnya byte-identik dari paket
   DOCX dan membandingkannya dengan TTF lokal. Keluaran utama:
   `AL_QORIN_REVISI_123_5_LAPIS.docx`.
7. **Preview HTML** (`scripts/build_preview_al_qorin.py`):
   `PREVIEW_INDEX_AL_QORIN_123.html` memuat 123 artikel, 615 lapis, dan 26
   figure crop pengguna. Alias yang diminta,
   `PREVIEW_INDEX_HAL01-65.html`, dibuat di folder `al_qorin/` dengan isi sama;
   berkas root berjudul sama milik Anwar tidak ditimpa.
8. **Test** (`tests/test_al_qorin_pilot.py`): struktur 123 unit, log
   penghapusan, manifest/hash crop pengguna, substitusi pilot, DOCX
   terintegrasi, preview, arah/alignment XML, tabel, media, dan embedding
   font. Test lama Anwar tetap dijalankan.

## Yang belum selesai

- Penyelesaian semantik manual untuk 111 unit di luar pilot: perapian Metode
  mengikuti gaya HALAMAN 07, kurasi akhir Catatan penyunting, Khususiyah
  tingkat frasa, dan pemeriksaan ulang Penentuan Jam terhadap Arab serta
  pindai halaman — per batch, bukan klaim massal.
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
