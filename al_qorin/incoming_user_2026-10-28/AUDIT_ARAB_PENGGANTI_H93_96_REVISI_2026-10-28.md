# AUDIT TEKS ARAB HALAMAN 93 DAN 96 REVISI — 28 OKTOBER 2026

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h93_96_revised/teks arab halaman 93 dan 96 revisi.txt` | 4.975 byte | `b6e7e4c4387cf6f3a8d154c9650254c2747c61a284cbef150d6813f781e2d01b` |

Sesudah menerima daftar halaman yang masih memuat bagian tidak terbaca,
pengguna mengirim revisi untuk halaman 93 dan 96. Kiriman ini
menggantikan hanya segmen M93 dan M96 dari arsip halaman 63–122; M92,
M94, M95, M97, dan unit lain tidak berubah.

Heading `Halaman 93` dipetakan ke M93 dan heading `Halaman 96`
dipetakan ke M96. Jumlah paragraf sumber berubah dari M93 3 dan M96 3
menjadi M93 6 dan M96 7. Total paragraf sumber Arab 123 unit menjadi
**560**. Elipsis pada versi lama M93 dan M96 tidak ada pada revisi ini.
Dua penanda proses `[bersambung]` pada M96 lama di master riset juga
hilang karena bait pembukanya kini tersusun sebagai tiga paragraf.
Kedua halaman tidak memuat `[gambar wafak]`, dan halaman 93 serta 96
memang tidak termasuk 26 halaman crop presisi pengguna.

Paragraf pertama M93 diawali asterisk literal. Arsip dan data sumber
mempertahankan `*`; Markdown keluaran menulisnya sebagai `\*` hanya
sebagai escape penyajian agar renderer Markdown, HTML, dan DOCX
menampilkan asterisk tersebut, bukan menafsirkannya sebagai daftar
atau penekanan miring. Escape itu tidak mengubah bacaan sumber.

Seluruh bacaan, harakat, pembagian paragraf, ejaan, tanda, dan susunan
antarhalaman dipertahankan sebagaimana kiriman pengguna; tidak ada
normalisasi atau tambahan editorial. Latin, Terjemahan, Syarah/catatan,
Metode/Khususiyah, tabel, dan pilihan 26 berkas crop tidak diganti.
Parser dan penerapannya adalah
`scripts/al_qorin_parse_user_arab_replacement_h93_96_revised.py` dan
`scripts/al_qorin_apply_arab_replacement_h93_96_revised.py`.

Audit ini mencatat provenans serta ruang lingkup penggantian. Audit ini
tidak menyatakan setiap bacaan revisi telah dibuktikan satu-satu
terhadap pindaian kitab asli.
