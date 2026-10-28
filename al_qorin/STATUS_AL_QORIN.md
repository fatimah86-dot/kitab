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
- Kitab asli: PDF pindai 62 halaman citra, Drive ID
  `1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z` (tanpa lapisan teks).
- Sumber crop saja: FINAL KHATAM, Drive ID
  `1sUpIWi143-NRAmtm_GhS7_vlCGYjPjR6`.
- Berkas biner sumber tidak di-commit; skrip mengharapkan salinan lokalnya di
  `google_drive/` dengan nama yang sama seperti di Drive.

## Yang sudah selesai

1. **Ingest lossless draf (4)** (`scripts/al_qorin_ingest.py`):
   SAMPUL + M01–M122 = 123 unit; setiap unit mempunyai tepat lima lapis lama;
   empat tabel ditemukan dan jangkarnya diverifikasi menurut urutan badan
   DOCX pada lapis lama 5 unit M65, M66, M67, dan M69.
2. **Ekstraksi crop FINAL KHATAM** (`scripts/al_qorin_extract_crops.py`):
   154 citra tertanam dipetakan; 122 adalah pindai halaman penuh dan 32 adalah
   crop/detail. Sebanyak 25 crop wafaq/rajah/deret/lingkaran disalin
   byte-identik ke `wafaq_qorin/<halaman>.jpg`. Tujuh crop yang oleh FINAL
   sendiri disebut daftar dan tidak tampak wafaq/rajah (halaman 60, 61, 62,
   63, 103, 105, 113) diekstrak terpisah ke `crop_lain/` dan **tidak**
   disisipkan sebagai wafaq. Lihat `MANIFEST_WAFAQ_AL_QORIN.md`.
3. **Restrukturisasi mekanis terlog** (`scripts/al_qorin_transform.py`) menjadi
   `REVISI_AL_QORIN_123_KERJA.md` dan DOCX kerja
   `AL_QORIN_123_KERJA_5_LAPIS.docx`:
   - 123 unit × 5 lapis baru dalam urutan terkunci.
   - Paragraf mandiri Qarinah yang dihapus: 569 (284 qabliah + 284 ba‘diah +
     1 paragraf gabungan di M01), ditambah 3 kalimat Qarinah sebaris dari
     paragraf campuran. Ini berbeda dari angka perintah “288 paragraf”;
     basis hitung terukur dicatat di `LOG_RESTRUKTUR_AWAL.md`. Kata qarinah
     sebagai pokok bahasan dalam Terjemahan tidak dihapus.
   - Label `[CATATAN PENERJEMAH ...]` utuh: 25.
   - Catatan ketidakpastian dari Syarah lama yang terselamatkan secara
     mekanis: 565 paragraf; dikte nahwu/Shorof/Hukum-baca tidak dibawa utuh.
   - Crop tersisip sesudah blok Metode: 25.
   - Saringan awal Penentuan Jam pada Arab/Latin/Terjemahan + Metode:
     3 unit memuat istilah jam, 0 unit memuat pola aritmetika penjumlahan,
     0 unit memenuhi keduanya; karena itu 123 unit sementara memakai teks
     persis «tidak ada hitungan di halaman ini». Kata `penjumlahan` pada draf
     sumber berjumlah 0, sehingga tidak ada penjumlahan jam yang dikarang.
4. **Pilot selesai manual** (`scripts/al_qorin_apply_pilot.py`,
   `overrides_pilot.json`) untuk SAMPUL, M01–M05, M58, M65–M67, M69, M122:
   Arab/Latin/Terjemahan/Metode tetap dari draf; Catatan penyunting dipilih
   dan dikelompokkan manual; Khususiyah unit wafaq diperbaiki pada tingkat
   frasa sumber; empat tabel transkripsi M65/M66/M67/M69 dipertahankan.
   Keluaran: `REVISI_AL_QORIN_PILOT.md` dan `AL_QORIN_PILOT_5_LAPIS.docx`.
5. **Builder Al-Qorin terpisah** (`scripts/build_docx_al_qorin.py`):
   Arab memakai `w:bidi=1` + `w:jc=start`; Latin memakai `w:bidi=0` +
   `w:jc=left`; paragraf crop dan sel tabel memakai `w:jc=center`; tabel
   draf tidak diberi `bidiVisual` karena tabel sumber tidak memilikinya.
   Amiri Regular/Bold/Italic/BoldItalic dari `fonts/` tertanam sebagai
   `word/fonts/*.odttf`; test memulihkan keempatnya byte-identik dari paket
   DOCX (de-obfuscation XOR) dan membandingkannya dengan TTF lokal.
6. **Test** (`tests/test_al_qorin_pilot.py`): struktur 123 unit, log
   penghapusan, hash crop, pilot, arah/alignment XML, tabel, media, dan
   embedding font. Test lama Anwar (`tests/test_final_65.py`) tetap lolos.

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
- Tujuh crop daftar menunggu keputusan bila hendak diperlakukan sebagai
  gambar jadwal; sampai ada keputusan, mereka tidak disebut wafaq dan tidak
  disisipkan.

## Perintah reproduksi

```bash
.venv/bin/python scripts/al_qorin_ingest.py
.venv/bin/python scripts/al_qorin_extract_crops.py
.venv/bin/python scripts/al_qorin_transform.py
.venv/bin/python scripts/al_qorin_apply_pilot.py
.venv/bin/python scripts/build_docx_al_qorin.py
.venv/bin/python scripts/build_docx_al_qorin.py \
  --input al_qorin/REVISI_AL_QORIN_123_KERJA.md \
  --output al_qorin/AL_QORIN_123_KERJA_5_LAPIS.docx
.venv/bin/python -m unittest discover -s tests -v
```
