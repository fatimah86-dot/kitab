# Revisi 5 Lapis Bersih — 27 Oktober 2026

## Hasil

- Master Markdown dan Word mencakup halaman sumber 01–65 dengan lima lapis per halaman.
- Bagian 22–24 dipisah menurut halaman sumber: awal sampai ayat 12, ayat 13–29, dan wafaq.
- Daftar isi Word mencakup seluruh 65 nomor halaman sumber. Jumlah halaman cetak terjemahan dapat lebih banyak dari 65.
- Arab memakai arah paragraf RTL; Latin/Indonesia memakai LTR. Tabel wafaq RTL disajikan satu kali pada lapis Arab, bukan tiga salinan.
- Enam belas gambar wafaq disematkan tanpa resize/re-encode berkas sumber. Satu PNG memiliki CRC metadata eXIf tidak valid; builder memperbaiki CRC dalam memori tanpa mengubah piksel atau berkas sumber.
- Kolofon halaman 65 dipertahankan sesuai teks sumber (permohonan doa untuk suami/anak dan al-Fatihah bagi orang tua), bukan diganti penutup baru.
- Placeholder dan markup Markdown tidak ditampilkan mentah dalam Word.

## Pemeriksaan dan batasan

Pengujian otomatis memeriksa struktur, jumlah lapis, tabel/gambar, dan markup. Pengujian ini **bukan** pengesahan seluruh harakat, nahwu-sharaf, klaim khasiat, atau kesetiaan setiap baris terhadap scan. Penelaahan ahli bahasa Arab dan penyunting naskah tetap diperlukan sebelum penerbitan. Klaim pengobatan dan perkara gaib merupakan isi tradisi/naskah, bukan bukti medis atau jaminan hasil.

Perbedaan hitungan halaman 07 (26 menurut penjumlahan biasa, 27 pada matan) ditandai sebagai perbedaan yang belum dapat dipastikan, bukan diberi alasan baru tanpa sumber.

## Drive

- Hasil pengganti: https://docs.google.com/document/d/1yuiyFn5x1byVv8sTErCz5RDiZsLkO8af/edit
- Ukuran hasil: 1.809.170 byte.
- Berkas lama ID `1Bz1iekUz8E1oyaOgBF1MkUp1sCO0VTlo` dipindah ke Trash setelah unggahan hasil berhasil, sesuai pilihan pengguna. Tidak dihapus permanen. Tautan baru berbeda dari tautan lama.

## Reproduksi

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-editorial.txt
.venv/bin/python scripts/build_final_65.py
.venv/bin/python scripts/build_preview_65.py
.venv/bin/python -m unittest discover -s tests -v
```

Master yang digunakan hanya `REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md`; berkas batch lama merupakan arsip dan tidak disinkronkan massal.
