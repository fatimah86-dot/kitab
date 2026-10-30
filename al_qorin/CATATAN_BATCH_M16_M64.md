# CATATAN BATCH SEMANTIK AL-QORIN — M16–M64 (28 Oktober 2026)

Batch ini menerapkan kurasi setingkat pilot pada 49 unit M16–M64 di dalam
master terintegrasi 123 unit, dengan pakem yang sudah terkunci: SAMPUL tampil
3 lapis, M01 (Muqodimah) dan M122 (Khatimah) tampil 4 lapis, unit lain
5 lapis; Arab kanan (`w:bidi=1`, `w:jc=start`), Latin kiri (`w:bidi=0`),
wafaq center dari crop presisi asli kiriman pengguna sesudah Metode.
Tampilan strip Khatam Sulaiman pada pindaian halaman cetak 64–65 menjadi
acuan visual bahwa lambang tidak digambar ulang: M64 memakai `64.jpg` dan
M65 (di luar batch, unit pilot) memakai `65.jpg`.

## Mekanisme reproduksibel

- Keputusan per unit dicatat di `overrides_batch_m16_m64.json` (setiap entri
  wajib memiliki `dasar` audit).
- `scripts/al_qorin_build_integrated.py` menerapkannya sebagai tahap
  pasca-pilot kedua dan membandingkannya dengan snapshot pra-batch. Tahap
  ini **menolak** perubahan apa pun di luar: (a) pemilihan/pengelompokan
  Catatan penyunting dari catatan lama unit yang sama, (b) penulisan ulang
  frasa Khususiyah, dan (c) penggantian Metode hanya pada M19, M20, M21,
  M38, dan M46.
- Arab, Latin, Terjemahan, Penentuan Jam, tabel/blok rajah, heading, nomor
  halaman, label `[CATATAN PENERJEMAH]`, dan crop ditegaskan tidak berubah.

## Kaidah kurasi catatan

Catatan mekanis hasil restrukturisasi berselang-seling antara catatan
bacaan substantif (ketidakpastian huruf/kata, identifikasi ayat/hadis,
status atribusi, observasi pindaian) dan catatan transisi yang hanya
mengulang boilerplate harakat editorial. Batch ini mempertahankan yang
pertama dan membuang yang kedua, termasuk catatan usang seperti “halaman
berikutnya belum dikerjakan”. Tidak ada teks catatan baru yang dibuat:
test membuktikan setiap paragraf catatan hasil batch tersusun hanya dari
paragraf catatan lama utuh. Untuk M58 (unit pilot) catatan tidak diubah;
hanya Khususiyahnya ditajamkan, sehingga blok terintegrasi M58 berbeda dari
pilot historis hanya pada Lapis 5.

## Koreksi Metode (lima stub kata-kunci)

Lima ringkasan mekanis terbukti membaca kata kerja naratif sebagai perintah
praktik dan diganti dengan kalimat yang setia pada isi unit:

- **M19** — «الوضع» adalah uraian kosmologis tentang Kursi, bukan perintah
  meletakkan.
- **M20** — «يكتب» adalah predikat uraian ilmu qadari/Lauh Mahfuz, bukan
  perintah menulis; media Khususiyahnya dikembalikan ke “tidak disebutkan”.
- **M21** — «حمله» merujuk delapan malaikat pemikul Arasy, bukan perintah
  membawa.
- **M38** — «أضعف» bukan petunjuk meletakkan; isi unit adalah peringatan
  penulis agar tidak terhijab oleh tanda/cahaya dalam rangkaian riyadhah.
- **M46** — «عقد» menjelaskan klaim “terikat”, bukan perintah mengikat;
  halaman ini daftar klaim kelompok jin, bukan petunjuk untuk pembaca.

Ringkasan Metode draf pada 44 unit batch lainnya dipertahankan apa adanya.

## Penajaman Khususiyah (contoh penentu)

- **M29/M36–M42 (riyadhah/khalwat):** durasi dan sarana dipisah dengan tepat,
  termasuk penegasan M36 bahwa riyadhah ini *tanpa penetapan hari tertentu*,
  tanda sepuluh hari pertama pada M37, tahap 90 hari pada M40, dan contoh
  zikir 131 kali pada M42 yang hitungannya tidak diverifikasi.
- **M49:** Khatam Sulaiman bertanduk tujuh pada tangan kanan dan rajah akhir
  halaman dirujuk ke crop asli `49.jpg`.
- **M50:** sumbu biru bertuliskan ayat tiga kali, ter (qaṭrān), surah al-Jinn,
  tujuh barawāt yang dibakhurkan saat tidur, dan tulisan gantung.
- **M51–M54 (syarat pengobatan):** aturan siang–malam, bakhur menurut
  golongan (M51), bakhur wajib menyertai azimat serta waktu pagi/Asar/
  Magrib/sahur (M53), dan bakhur hadir mengepul pada ringkasan syarat (M54).
- **M55–M57:** hijab dan susunan bacaan al-Baqarah–Yāsīn, pengulangan tiga
  kali, dan doa panjang dicatat sebagai bacaan penulis, bukan jaminan medis.
- **M58:** wafaq mukhammas 5×5 dirujuk ke crop asli `58.jpg` dengan
  ketidakpastian sel dinyatakan.
- **M59–M63:** daftar hari/planet/logam, buruj, nama bulan, sulthan malaikat,
  tujuh raja menurut hari, empat kepala dan tujuh ruhani diperlakukan sebagai
  kerangka rujukan penulis; ejaan nama tidak dikoreksi diam-diam.
- **M64:** tulisan yang dibawa dengan misik, za‘farān, dan air mawar serta
  baris lambang Khatam Sulaiman dirujuk ke crop asli `64.jpg`.

## Batas kejujuran batch ini

Batch ini **tidak** menerjemahkan ulang Arab/Latin/Terjemahan, tidak
mengarang hitungan jam (semua Penentuan Jam tetap sebagaimana sebelumnya),
tidak menggambar ulang rajah, dan tidak mengesahkan khasiat apa pun. Isi
praktik tetap dinisbatkan kepada penulis kitab sebagai dokumen terjemahan —
bukan anjuran, bukan terapi, dan bukan pengganti penanganan medis. Unit di
luar pilot dan batch ini masih menunggu batch semantik berikutnya; lihat
`STATUS_AL_QORIN.md`.
