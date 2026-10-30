# AUDIT TEKS ARAB HALAMAN 82, 83, 97, DAN 98 REVISI FINAL — 28 OKTOBER 2026

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h82_83_97_98_revised/teks arab halaman 82-83-97-98 revisi final.txt` | 11.385 byte | `0fb678e62f9da6b0f18f9e058dde6d954c4b539eecba0b035f58e8de72ef2a8f` |

Pengguna memerintahkan halaman 82, 83, 97, dan 98 diganti dengan revisi
final yang dikirim. Heading halaman dipetakan ke M82, M83, M97, dan M98.
Setiap baris isi yang tidak kosong menjadi satu paragraf sumber Lapis 1.

Jumlah paragraf sumber berubah dari M82 5, M83 7, M97 4, dan M98 4
menjadi M82 7, M83 9, M97 7, dan M98 3. Total paragraf sumber Arab 123
unit menjadi **548**. Blok “dari kehalusan rahasia … keamanan dari
ketakutan” yang muncul dua kali berurutan pada kiriman M83 dipertahankan
dua kali; tidak ada deduplikasi editorial.

Pengguna juga menetapkan bahwa pada semua halaman revisi, paragraf persis
`[gambar wafak]` berarti crop wafaq pengguna yang sudah ada disisipkan
pada posisi itu. Karena itu Markdown/DOCX keluaran mengganti penanda
tersebut dengan crop unit yang bersangkutan dan menghapus lokasi crop
lama pada unit yang sama, sehingga setiap crop tetap tampil tepat satu
kali. Aturan ini diterapkan pada M66–M69 dari revisi sebelumnya serta
M82, M83, dan M98 dari kiriman ini. Arsip sumber tetap mempertahankan
penanda `[gambar wafak]`; transformasinya dilakukan reproduksibel oleh
`scripts/al_qorin_wafaq_markers.py` dan renderer kedua edisi.

Latin, Terjemahan, Syarah/catatan, Metode/Khususiyah, tabel, dan pilihan
26 berkas crop tidak diganti. Yang berubah hanya Lapis 1 empat halaman
sasaran dan posisi tampil crop pada unit berpenanda. Parser dan
penerapannya adalah
`scripts/al_qorin_parse_user_arab_replacement_h82_83_97_98_revised.py`
dan `scripts/al_qorin_apply_arab_replacement_h82_83_97_98_revised.py`.

Audit ini mencatat provenans serta ruang lingkup penggantian. Audit ini
tidak menyatakan setiap bacaan revisi telah dibuktikan satu-satu terhadap
pindaian kitab asli, dan teks antarhalaman dipertahankan persis
sebagaimana dikirim pengguna.
