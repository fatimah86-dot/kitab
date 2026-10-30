# AUDIT UNGGAHAN M65 — 28 Oktober 2026

Status: **DIARSIPKAN, tidak ditimpakan.** Pengguna memutuskan berkas-berkas ini
disimpan sebagai bahan audit; unit M65 kanonis tidak diubah karena sudah lebih
lengkap dan sudah memakai crop yang sama pada resolusi lebih tinggi.

## Berkas diterima (gelombang kedua, 28 Oktober 2026)

| Berkas lokal | Asal unggahan | Byte | SHA-256 |
|---|---|---:|---|
| `M65_DENGAN_WAFQ_ASLI_KHATAM_SULAIMAN.docx` | `M65_x5f_DENGAN_x5f_WAFQ_x5f_ASLI_x5f_KHATAM_x5f_SULAIMAN.docx.txt` | 132569 | `b40068432aebc7668e7f2a8e4eb7a8295c51480654b6ed76d68b456e3431e56c` |
| `FINAL_M65_PAKAI_CROP_RAJAH_ANDA.docx` | `FINAL_x5f_M65_x5f_PAKAI_x5f_CROP_x5f_RAJAH_x5f_ANDA.docx (1).txt` | 59038 | `957d25b691f725473d9d781fea1b35ad185b7cf1125d56ef7222d931c61f59f5` |
| `KHATAM_SULAIMAN_UPLOAD_1080x167.jpg` | berkas JPG bernama acak `AQPz...jpg` | 11142 | `18c9a2da1ad627c419218cd94f13ff8cccffdf1ddfe7fd5b44f091dbc3f94b0b` |

## Temuan audit

1. Gambar JPG yang diunggah (1080×167) adalah strip **خاتم سليمان** yang sama
   dengan crop kanonis `../wafaq_qorin/65.jpg` (1631×253) yang sudah terpasang
   center sesudah Metode pada M65 — hanya resolusinya lebih rendah. Gambar yang
   sama juga tertanam sebagai `word/media/image1.jpeg` di
   `M65_DENGAN_WAFQ_ASLI_KHATAM_SULAIMAN.docx` (byte-identik) dan dalam bentuk
   terkompresi ulang di `FINAL_M65_PAKAI_CROP_RAJAH_ANDA.docx`.
2. `M65_DENGAN_WAFQ_ASLI_KHATAM_SULAIMAN.docx`: 16 paragraf, 0 tabel. Arab dan
   Latin terpotong dengan `...`; Lapis 4 memakai nama lama “Syarah dan
   Penjelasan”, bukan struktur Metode/Penentuan Jam/Catatan penyunting pada
   standar terkunci. Berkas ini juga menyematkan foto pindaian dua halaman
   (cetak 64–65) sebagai referensi; foto itu menegaskan strip Khatam Sulaiman
   tercetak di halaman 64 **dan** 65. Keduanya sudah tercakup oleh crop presisi
   pengguna `64.jpg` dan `65.jpg`.
3. `FINAL_M65_PAKAI_CROP_RAJAH_ANDA.docx`: 9 paragraf, 0 tabel. Judul Lapis 3
   ada tetapi isi terjemahannya kosong; Lapis 4 hilang seluruhnya. Tidak layak
   menjadi sumber teks.
4. M65 kanonis adalah unit pilot yang dikurasi manual: Arab/Latin/Terjemahan
   penuh dari draf (4), Metode, Catatan penyunting terpilih, tabel transkripsi
   lambang 1×2, Khususiyah tingkat frasa, dan crop `65.jpg` center sesudah
   Metode. Tidak ada materi dari kedua DOCX unggahan yang melebihi atau
   mengoreksi isi kanonis, sehingga tidak ada yang diintegrasikan.

## Aturan lapis kondisional yang menyertai unggahan

Bersama berkas ini pengguna menyampaikan aturan jenis-unit: SAMPUL hanya
Lapis 1–3; Muqodimah/Khatimah hanya Lapis 1–4 bila tanpa `تكتب`; unit amalan
Lapis 1–5 lengkap dengan crop wafaq center; Arab kanan `w:bidi=1`, Latin kiri
`w:bidi=0` (arah ini sudah diterapkan dan diuji).

Pengujian kata kunci harfiah atas Arab kanonis (sesudah harakat dilucuti)
menghasilkan 43 unit “amalan”, 7 unit mirip muqodimah/Khatimah, dan 72 unit di
luar semua kategori — termasuk positif palsu (M122 terhitung amalan hanya
karena `وَفَّقَنِي` memuat `وفق`) dan negatif palsu (unit bercrop M58, M85, M98
tanpa kata kerja daftar). Karena itu aturan diterapkan sebagai daftar tetap
terverifikasi sesuai keputusan pengguna: **SAMPUL → 1–3** (catatan sampul
dipindah ke akhir Lapis 3), **M01 (Muqodimah) → 1–4**, **M122 (Khatimah) →
1–4**, dan 120 unit lain tetap 5 lapis. Amandemen dicatat di
`../../STANDAR_MUTLAK_AL_QORIN_123.md` §1/§7/§8 dan diterapkan reproduksibel
lewat `LAYER_LIMITS` + `render_unit_md` di `../../scripts/al_qorin_transform.py`.
Total judul lapis tampil berubah 615 → 611; data JSON unit tidak berubah.
