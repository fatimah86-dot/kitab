# AUDIT FILE ARAB–LATIN TXT KIRIMAN PENGGUNA — 28 OKTOBER 2026

## Berkas yang diarsipkan byte-persis

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_latin_full/teks arab berharokat.txt` | 252.499 byte | `d28d8f3b1c3887634ea3c3843fb04cea13dc42c7873909a0633d8ef0b9705097` |
| `arab_latin_full/teks latin.txt` | 132.877 byte | `538a5959af8880b6094333dbdc68090bada94075a6a6b9e10d55d1b1189f5647` |

Kedua berkas UTF-8. Baris judul pada masing-masing berkas dan paragraf
“Kaidah Latin Shahih …” sebelum `SAMPUL` tidak dimasukkan ke dokumen bersih;
hanya isi sesudah heading `SAMPUL` yang diperlakukan sebagai Lapis 1–2.

## Hasil parse dan keputusan pemakaian

- Arab: **123 unit** berurutan SAMPUL + M01–M122, **540 paragraf**.
- Latin: **123 unit** berurutan SAMPUL + M01–M122, **315 paragraf**.
- Sesuai perintah pengguna terbaru, kedua berkas dipakai sebagai sumber
  Lapis 1–2 edisi bersih. Parser reproduksibel:
  `scripts/al_qorin_parse_user_arab_latin.py`.
- Nilai paragraf hasil parse saat ini sama dengan Lapis 1–2 master
  terintegrasi sebelumnya pada 123/123 unit, sehingga penguncian sumber ini
  tidak mengubah bunyi Arab/Latin yang sudah tampil; perubahan pengguna
  terlihat pada struktur edisi bersih, bukan pada isi kedua lapis itu.
- Jumlah paragraf Latin tidak selalu sama dengan Arab karena berkas kiriman
  sendiri mengelompokkan beberapa paragraf Arab ke paragraf Latin yang lebih
  panjang. Pengelompokan file pengguna dipertahankan apa adanya.

## Wafaq

Edisi bersih hanya menyisipkan 26 crop pengguna dari `al_qorin/wafaq_qorin/`
pada unit tujuan 49, 58, 64–74, 76–78, 82–86, 98, 109, 116, 120, dan 121.
Tidak ada crop dari FINAL KHATAM dan tidak ada gambar ulang.

## Batas yang tidak diubah oleh audit ini

Penguncian file pengguna sebagai sumber Lapis 1–2 adalah keputusan
provenans/pemakaian. Ia tidak dengan sendirinya membuktikan setiap harakat
terhadap pindaian; lokus-lokus yang sudah tercatat pada audit sebelumnya
tetap tidak boleh diklaim selesai tanpa bukti baca baru. Catatan proses tidak
dibawa ke DOCX bersih; audit ini disimpan terpisah di repository.
