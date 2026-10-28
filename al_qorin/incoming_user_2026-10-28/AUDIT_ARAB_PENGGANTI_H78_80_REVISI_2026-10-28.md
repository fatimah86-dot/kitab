# AUDIT TEKS ARAB HALAMAN 78 DAN 80 REVISI — 28 OKTOBER 2026

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h78_80_revised/teks arab halaman 78 dan 80 revisi.txt` | 3.598 byte | `5ecfb8b6839a54f8467c3076bba8697bd28edffa1043d6c4d8b3d06073a44845` |

Sesudah menerima daftar halaman yang masih memuat bagian tidak terbaca,
pengguna mengirim revisi untuk halaman 78 dan 80. Kiriman ini
menggantikan hanya segmen M78 dan M80 dari arsip halaman 63–122; M77,
M79, M81, dan unit lain tidak berubah.

Heading `Halaman 78` dipetakan ke M78 dan heading `Halaman 80`
dipetakan ke M80. Jumlah paragraf sumber berubah dari M78 3 dan M80 4
menjadi M78 3 dan M80 5. Total paragraf sumber Arab 123 unit menjadi
**551**. Elipsis di awal M78 dan akhir M80 pada versi lama tidak ada
pada revisi ini.

M78 memuat tepat satu paragraf `[gambar wafak]`; sesuai aturan
pengguna, keluaran Markdown/DOCX mengganti penanda itu dengan crop
presisi yang sudah ada untuk halaman yang sama, `78.jpg`, lalu
menghapus lokasi crop lama pada unit yang sama sehingga 26 crop tetap
tampil tepat satu kali. M80 tidak memuat penanda atau crop. Arsip sumber
mempertahankan `[gambar wafak]` pada M78.

Seluruh bacaan, harakat, pembagian paragraf, ejaan, tanda, dan susunan
antarhalaman dipertahankan sebagaimana kiriman pengguna; tidak ada
normalisasi atau tambahan editorial. Latin, Terjemahan, Syarah/catatan,
Metode/Khususiyah, tabel, dan pilihan 26 berkas crop tidak diganti.
Parser dan penerapannya adalah
`scripts/al_qorin_parse_user_arab_replacement_h78_80_revised.py` dan
`scripts/al_qorin_apply_arab_replacement_h78_80_revised.py`.

Audit ini mencatat provenans serta ruang lingkup penggantian. Audit ini
tidak menyatakan setiap bacaan revisi telah dibuktikan satu-satu
terhadap pindaian kitab asli.
