# AUDIT TEKS ARAB PENGGANTI HALAMAN 63–122 — 28 OKTOBER 2026

## Berkas yang diarsipkan

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h63_122/teks arab pengganti halaman 63-122.txt` | 122.022 byte | `b82ea529a6df1bbd9ad8cecbd23573c3722f01fd1b7ef84d1fa44471d81ec189` |

Pesan chat memuat salinan awal halaman 63–78 dan heading 79 yang terpotong,
lalu satu blok kode lengkap halaman 63–122. Arsip di atas memakai **blok
kode lengkap** itu; salinan awal yang terduplikasi tidak ikut diparse.

## Hasil parse dan pemetaan

- Heading pertama `Halaman 63, ...` dan heading bernomor `64`–`122`
  terurut lengkap: **60 unit**.
- Nomor halaman dipetakan satu-satu ke unit yang sudah ada:
  `63 → M63`, `64 → M64`, …, `122 → M122`.
- Tiap baris isi yang tidak kosong diperlakukan sebagai satu paragraf Arab.
  Tanda `*` di awal beberapa baris adalah penanda tampilan kiriman dan
  tidak dirender sebagai bagian kalimat Arab.
- Total hasil parse: **267 paragraf Arab**.
- Lapis 1 lama pada rentang yang sama berjumlah 261 paragraf. Perubahan
  segmentasi per unit ialah M68 7→6, M70 7→8, M110 5→3, M112 2→3,
  M114 2→4, M115 2→3, M117 3→5, dan M118 2→4; bersihnya **+6 paragraf**.
- Sesudah penggantian, total paragraf Arab seluruh 123 unit menjadi
  **544**: 277 paragraf kiriman SAMPUL–M62 + 267 paragraf M63–M122.

## Keputusan pemakaian

Teks ini menggantikan Lapis 1 untuk M63–M122 pada master terintegrasi dan
edisi bersih. Dengan tahap sebelumnya, seluruh Lapis 1 SAMPUL–M122 kini
berasal dari dua arsip kiriman chat pengguna. Lapis 2 Latin tetap berasal
dari arsip TXT pengguna; Terjemahan, Syarah/catatan, Metode/Khususiyah,
tabel, dan 26 crop pengguna tidak diganti oleh tahap ini.

Master riset memakai paragraf arsip persis. Edisi bersih menerapkan aturan
presentasinya yang sudah ada: lima penanda proses berbahasa Indonesia pada
empat paragraf — `[bersambung]` 2× di M96, `[tidak disalin penuh]` di dua
paragraf M97, dan `[baris tidak lengkap]` di M107 — tidak ditampilkan.
Selain penghilangan penanda proses itu, paragraf edisi bersih sama dengan
arsip.

Parser reproduksibelnya adalah
`scripts/al_qorin_parse_user_arab_replacement_h63_122.py`; penerapan ke
Markdown keluaran memakai
`scripts/al_qorin_apply_arab_replacement_h63_122.py`.

## Batas audit

Penggantian ini adalah keputusan provenans dari pengguna. Audit di sini
memverifikasi kelengkapan heading, pemetaan unit, jumlah paragraf, arah
run DOCX, dan bahwa hanya Lapis 1 yang berubah. Audit ini tidak menyatakan
bahwa setiap perbaikan bacaan/harakat dalam kiriman telah dibuktikan
satu-satu terhadap pindaian kitab asli, dan tidak menyelaraskan ulang
Latin/Terjemahan/Syarah terhadap bacaan Arab yang berubah.
