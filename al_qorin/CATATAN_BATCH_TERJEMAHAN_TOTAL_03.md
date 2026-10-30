# Catatan Batch Terjemahan Total 03 — M16–M32

## Ruang lingkup

- Unit: M16–M32 (17 unit).
- Lapisan yang diubah: hanya **Lapis 3 Terjemahan** pada `REVISI_AL_QORIN_123.md` dan padanan hasil `clean_translation` pada `AL_QORIN_123_BERSIH.md`.
- Jumlah paragraf pengganti: 44.
- Override: `overrides_terjemahan_total_batch03.json`.
- Applier: `scripts/al_qorin_apply_translation_total_batches.py --batch 3`.
- Bukti ruang lingkup: perbandingan terurai per unit/lapis terhadap commit Batch 02 menunjukkan tidak ada perbedaan di luar Lapis 3 M16–M32; Arab, Latin, lapis lain, tabel, rajah, dan crop tetap.

## Bukti tiga lapis

Setiap unit diterjemahkan dari Arab final terkunci, dibandingkan dengan:

1. Isi Arab, Latin, Terjemahan lama, Catatan penyunting, Metode, dan Lapis 5 pada master.
2. Halaman cetak buku asli 16–32 yang dirender dari PDF pindaian `al qorin war riyadhah.pdf` SHA-256 `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`, halaman PDF 9–17.
3. Aturan dalam `PANDUAN_REVISI_TOTAL_TERJEMAHAN_AL_QORIN.md`: istilah teknis dipertahankan secukupnya, klaim kosmologi dan kasyaf dinisbatkan kepada penulis, status hadis yang dikutip tidak ditetapkan tanpa bukti sanad, dan susunan yang belum mantap tidak dilancarkan secara diam-diam.

## Hitungan retro Lapis 3

| Unit | Paragraf |
|---|---:|
| M16 | 3 |
| M17 | 3 |
| M18 | 3 |
| M19 | 2 |
| M20 | 3 |
| M21 | 2 |
| M22 | 2 |
| M23 | 3 |
| M24 | 2 |
| M25 | 3 |
| M26 | 3 |
| M27 | 3 |
| M28 | 2 |
| M29 | 3 |
| M30 | 2 |
| M31 | 2 |
| M32 | 3 |
| **Total** | **44** |

Jumlah paragraf lama setiap unit dipertahankan. Karena pemecahan paragraf Arab judul dan daftar tidak selalu sama dengan pemecahan Lapis 3 lama, cakupan semantik dijaga pada tingkat unit; tidak dipaksakan selaras 1:1:1 yang tidak pernah berlaku untuk seluruh buku.

## Koreksi penting dari terjemahan lama

- M19 mengikuti Arab final *as-sirr* (“rahasia”), bukan bacaan kerja Latin lama yang membawa padanan “burung nasar”.
- M20 mengikuti *al-hal* dan pembacaan Israfil pada Arab final; bagian Lauh Mahfuz dan gerakan yang hubungan katanya belum mantap tetap ditandai.
- M22 mengikuti *al-isytiyaq* (“kerinduan”) pada Arab final.
- M24 mengikuti *hiss ar-ratq*, *al-muhaddatsun*, dan *al-athwar*; padanan lama “lima ratq”, “muhaddatsun”, dan “panjang-panjang” tidak dipertahankan.
- M25 mengikuti *Asma' al-Husna*. Istilah kerja lama *al-khazarnad* tidak terdapat pada Arab final halaman ini dan dikeluarkan dari terjemahan baru, tanpa mengubah Catatan penyunting lama pada lapis lain dalam batch khusus Lapis 3 ini.
- M27 mengikuti kata Arab final *yuzil* (“menghilangkan”) pada penafsiran penulis atas QS Ar-Ra'd 13:17.
- M29 mengikuti *al-maqamat*, niat, tauhid, dan *bi-inqidah*; *sya'ir* diterjemahkan sebagai jelai/barley dan bahan *burgul jarish* tidak dinormalkan.
- M30 mengikuti Arab final yang menyatakan tubuh mengikuti jiwa dan ruh; padanan lama “sumber keduanya” tidak dipakai.

## Catatan terbuka

- M16: frasa *mil'a wajhin lahu* dan rangkaian “kenabian tajalli” belum mantap secara sintaksis.
- M17: bentuk *al-amr al-'ulya*, frasa *ribq al-mitsal*, dan kata dalam kurung siku *[al-jam']* dipertahankan dengan penanda.
- M18: konstruksi “menambah wujud” dan beberapa hubungan predikat pada uraian tauhid masih janggal.
- M19: istilah *qanah* dan rangkaian “tangan-tangan pikiran/pengaturan” belum mempunyai padanan teknis yang pasti.
- M20: subjek dan objek pada kalimat Lauh Mahfuz serta kalimat gerakan belum dapat ditetapkan hanya dari teks yang tersedia.
- M24: maksud *raf' al-qadar* pada kalimat setelah ucapan Abu Yazid tetap terbuka.
- M29: maksud teknis *bi-inqidah* tidak dijelaskan oleh teks halaman ini; padanan harfiah disertai glos ketidakpastian.
- M31: kalimat penutup perbandingan ruh/jiwa/tubuh berulang dan nisbah terakhirnya tidak sepenuhnya jelas.
- M32: scan halaman 32 memuat baris lanjutan setelah titik akhir dua paragraf Arab final yang terkunci. Batch ini khusus Lapis 3 dan tidak menambahkan teks Arab atau terjemahan untuk baris di luar sumber Arab terkunci. Persoalan batas segmen tersebut tetap terbuka untuk audit Arab terpisah bila pengguna menghendaki.
- Ucapan firasat mukmin, ucapan Abu Bakar, ucapan Abu Yazid, ungkapan *man 'arafa nafsahu*, dan keterangan ruh mukmin di bawah Arasy dipertahankan sebagai penisbatan penulis. Batch ini tidak menilai sanad atau kesahihan riwayat.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 3 --check
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 3
```

Setelah data terintegrasi dibangun, applier Batch 02–08 dijalankan oleh `scripts/al_qorin_build_integrated.py` sesudah seluruh penggantian Arab final, sehingga Batch 03 tidak mendahului atau menimpa kunci Arab.
