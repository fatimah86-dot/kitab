# CATATAN BATCH 01 — REVISI TOTAL TERJEMAHAN AL-QORIN

Tanggal kerja: 28 Oktober 2026. Batch ini memulai fase revisi total yang
diminta pengguna sesudah menyatakan terjemahan lama “masih tidak sempurna”.
Contoh gaya ialah dokumen **Anwar Asy-syaikh Al-Basyir** yang ditunjuk
pengguna. Adaptasi gaya dan batas-batasnya dicatat di
`PANDUAN_REVISI_TOTAL_TERJEMAHAN_AL_QORIN.md`; inventaris seluruh unit ada di
`AUDIT_REVISI_TOTAL_TERJEMAHAN_123.md`.

## Ruang lingkup Batch 01

Unit: **SAMPUL, M01, M02, M03, M04, M05**.

Bidang yang berubah: **hanya Lapis 3 (Terjemahan)** melalui
`overrides_terjemahan_total_batch01.json`. Arab, Latin, Metode, Penentuan
Jam, Catatan penyunting, Khususiyah, `rajah_blocks`, tabel/label, dan crop
dipertahankan byte-identik oleh penjaga builder dan test khusus.

## Pindaian yang diperiksa

Dari PDF buku asli (`al qorin war riyadhah.pdf`) dibuat render kerja pada
folder terabaikan `al_qorin/work/scan_split/`:

- PDF hlm. 1: sampul;
- PDF hlm. 2: halaman cetak 2–3 (mukadimah);
- PDF hlm. 3: halaman cetak 4–5 (penutup mukadimah dan Bab Pertama).

Pindaian menguatkan susunan umum Arab kanonis pada enam unit ini. Tidak ada
koreksi huruf Arab/Latin yang cukup pasti untuk menimpa lapisan kanonis pada
batch ini. Karena itu batch ini tidak mengklaim telah menyelesaikan bacaan
yang rusak; ia hanya menerjemahkan bacaan kerja yang sudah ada dengan lebih
lengkap dan wajar, sambil mempertahankan penanda ragu.

## Penajaman terjemahan utama

- Mukadimah M01–M03 kini dibaca sebagai rangkaian hamdalah yang mengalir,
  bukan potongan harfiah yang berulang. Istilah *muqarrabīn*, *‘ārif*,
  *muḥaqqiq*, *sālik*, *waḥdāniyyah*, *aḥadiyyah*, dan *ṣamadiyyah*
  dipertahankan dengan glos singkat.
- *Al-jadīdān* pada M03 diberi makna idiomatik “siang dan malam”, bukan
  dibiarkan sebagai “kedua yang selalu baru”.
- Penutup M04 memakai padanan wajar “di awal dan di akhir (di dunia dan di
  akhirat)”. Frasa *‘alā rabbi al-‘ulamā’* tidak dipaksa menjadi terjemahan
  lancar karena susunannya tetap belum mantap.
- Judul M05 kini menegaskan bentuk cetak *ar-Riyāḍiyyāt al-Kubrā* sambil
  menerjemahkan maksud siyaq sebagai riyadhah besar. Kata *intisyāt* dan
  penutup gramatikal rusak *li-takun takūna al-imārata amruhu* tetap ditandai
  belum dapat ditetapkan.

## Audit total yang mendahului batch

Script `scripts/al_qorin_audit_translation.py` menginventarisasi 123 unit.
Hasil mekanis awal: 27 unit memuat 45 penanda “tidak disalin penuh” dan
seluruh Terjemahan memuat 85 elipsis. Prioritas audit ialah P1=33, P2=4,
P3=86. Angka ini bukan vonis kualitas; ia adalah antrean kerja. Batch
berikutnya mengikuti urutan pada `AUDIT_REVISI_TOTAL_TERJEMAHAN_123.md`,
dimulai dari M06–M15.

## Batas yang tetap terbuka

- Bacaan *man/min*, *bīyah*, frasa kehambaan, penutup salawat M03,
  *aṣwāl*, frasa pembuka M04, serta *intisyāt* M05 belum diselesaikan.
- Judul sampul dalam kaligrafi dan beberapa kata mukadimah masih memerlukan
  pembacaan palaeografis lebih tajam sebelum Arab boleh diubah.
- Batch ini belum meninjau kesesuaian Metode/Khususiyah terhadap terjemahan
  baru; tidak ditemukan kontradiksi material pada enam unit pembuka.
- Revisi total **belum khatam**: 117 unit lain masih memakai terjemahan
  baseline dan menunggu Batch 02–08.
