# Audit Turunan “Halaman” Al-Qorin — 2026-10-30

## Status

Berkas dalam catatan ini adalah **edisi turunan terpisah**. Edisi
khatam kanonis pada commit `621563f` tidak diganti, tidak dibangun
ulang dari turunan ini, dan crop pengguna tidak diubah.

Sumber kanonis:

| Berkas | SHA-256 |
|---|---|
| `REVISI_AL_QORIN_123.md` | `7f850a55ad469effa0dd04aef80b972586bde58940d1b412f4c69c449bce9888` |
| `AL_QORIN_123_BERSIH.md` | `4fa012922f050cb0275a4cd370a2dcc3512021e95d399a36973a790610f9fb20` |
| `AL_QORIN_REVISI_123_5_LAPIS.docx` | `d0ed610e93bea7b0a56197cce045115e2719114405ab3f4a81181e9504f1ad0e` |
| `AL_QORIN_123_BERSIH.docx` | `0b41b67591e163a21af7b8e54d7d4c3351f44bde809557092df4104587d13f60` |

## Transformasi yang diterapkan

Skrip `scripts/al_qorin_build_halaman_derived.py` membaca salinan
kedua master dan menolak menulis ke jalur inputnya. Aturan hasil
klarifikasi pengguna adalah:

1. Judul unit `M<angka>` diganti menjadi satu label `Halaman <angka>`.
   Bila judul lama sudah memuat `Halaman <angka yang sama>` di awal
   atau `, HALAMAN <angka yang sama>` di akhir, pengulangan itu
   dibuang. Contoh: `M10 — Halaman 10, pembuka...` menjadi
   `Halaman 10 — pembuka...`.
2. Rujukan mandiri `M<angka>` di badan teks diganti menjadi
   `Halaman <angka>`; angka ditulis tanpa nol di depan.
3. Seluruh kalimat yang memuat `klaim penulis` secara tidak peka
   huruf dihapus. Frasa tumpang-tindih dalam `diklaim penulis` ikut
   terhitung sebagai kemunculan substring `klaim penulis`.
4. Seluruh kalimat yang memuat `Batch <angka>` secara tidak peka
   huruf dihapus.
5. Label `[CATATAN PENERJEMAH: ...]`, judul lapisan/subbagian,
   struktur sel tabel, tautan gambar, dan rujukan 26 crop dijaga.

Penghapusan dilakukan pada granularitas kalimat, bukan sampai akhir
baris. Karena beberapa kalimat lama menggabungkan isi dan frasa
`klaim penulis`, sebagian isi kalimat itu memang ikut hilang sesuai
pilihan ruang lingkup yang ditetapkan. Ini salah satu alasan hasil
disimpan sebagai turunan, bukan pengganti edisi khatam.

## Hasil transformasi Markdown

| Keluaran | Judul halaman | Rujukan badan diganti | Kalimat klaim dihapus | Kalimat Batch bernomor dihapus | Baris berubah | Baris menjadi kosong |
|---|---:|---:|---:|---:|---:|---:|
| `REVISI_AL_QORIN_123_HALAMAN.md` | 122 | 23 | 28 | 1 | 161 | 0 |
| `AL_QORIN_123_BERSIH_HALAMAN.md` | 122 | 12 | 18 | 0 | 151 | 0 |

Dua rujukan `M01–M05` pada master penelitian tidak dihitung sebagai
penggantian badan karena berada di kalimat `Batch 01` yang dihapus.

Hash dan ukuran Markdown turunan:

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `REVISI_AL_QORIN_123_HALAMAN.md` | 757.516 byte | `4e7761bb173b9357c563bf3d44ac46218e0278a286d9065bddd681e8150660b1` |
| `AL_QORIN_123_BERSIH_HALAMAN.md` | 671.777 byte | `4444f0c528aaffb79a6d75ef4a36672ed1979ff407e3f4d13ad85469543bbd20` |

## Keluaran DOCX

DOCX dibangun dengan builder kanonis yang sama, dengan `--clean`
khusus untuk edisi bersih:

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_REVISI_123_5_LAPIS_HALAMAN.docx` | 6.984.638 byte | `70151b0431c4eb0b668b0125bd6c2772d1725bf9e9e11b65e6c40282ee7e2d37` |
| `AL_QORIN_123_BERSIH_HALAMAN.docx` | 6.933.809 byte | `f594c2316e2b094c4efdc67bcb853211db9040591b1d0762094d7bd7a47f3749` |

## QA

Pemeriksaan terprogram atas Markdown dan DOCX turunan membuktikan:

- 123 judul unit pada masing-masing keluaran: SAMPUL diikuti urutan
  tepat Halaman 1–122;
- 123 Heading 1 unit di masing-masing DOCX;
- 26 rujukan gambar Markdown dan 26 bagian media DOCX; daftar
  rujukan gambar sama persis dengan master kanonis;
- 25 label catatan penerjemah pada masing-masing master, sama
  dengan jumlah sumber;
- tidak ada subbagian daun yang kosong;
- tidak ada rujukan mandiri `M<angka>`, frasa `klaim penulis`, atau
  `Batch <angka>` yang tersisa dalam Markdown maupun teks DOCX
  (termasuk tabel serta header/footer);
- tidak ada perubahan Git pada master kanonis, DOCX khatam,
  direktori `wafaq_qorin/`, manifest crop, atau berkas crop;
- pembangunan Markdown turunan diulang dan menghasilkan SHA-256
  yang sama; discovery test repo mencatat 40 test terdaftar dengan
  33 lulus dan 7 dilewati karena work JSON ter-ignore tidak hadir.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_build_halaman_derived.py
.venv/bin/python scripts/build_docx_al_qorin.py \
  --input al_qorin/REVISI_AL_QORIN_123_HALAMAN.md \
  --output al_qorin/AL_QORIN_REVISI_123_5_LAPIS_HALAMAN.docx
.venv/bin/python scripts/build_docx_al_qorin.py --clean \
  --input al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md \
  --output al_qorin/AL_QORIN_123_BERSIH_HALAMAN.docx
```

Hasil ini tidak mengubah kesimpulan edisi khatam: versi kanonis
tetap 123 unit, 611 lapisan penelitian, dan 26 crop. Versi turunan
hanya mengganti label unit menjadi “Halaman” dan menghapus
kalimat-kalimat yang masuk dua pola di atas.
