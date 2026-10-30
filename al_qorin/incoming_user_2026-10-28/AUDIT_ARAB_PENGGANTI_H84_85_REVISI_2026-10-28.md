# AUDIT TEKS ARAB HALAMAN 84 DAN 85 REVISI — 28 OKTOBER 2026

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h84_85_revised/teks arab halaman 84 dan 85 revisi.txt` | 3.845 byte | `d94990129c37c79a575ba0d398ff9bf7ec2fb1c188b74d9a020b56b6112db06a` |

Sesudah menerima daftar halaman yang masih memuat bagian tidak terbaca,
pengguna mengirim revisi untuk halaman 84 dan 85. Kiriman ini
menggantikan hanya segmen M84 dan M85 dari arsip halaman 63–122; M83,
M86, dan unit lain tidak berubah.

Heading `Halaman 84` dipetakan ke M84 dan heading `Halaman 85`
dipetakan ke M85. Jumlah paragraf sumber berubah dari M84 6 dan M85 5
menjadi M84 8 dan M85 4. Total paragraf sumber Arab 123 unit menjadi
**553**. Elipsis pada versi lama M84 dan M85 tidak ada pada revisi ini;
kalimat terakhir M84 berlanjut langsung ke paragraf pertama M85.

Kedua halaman masing-masing memuat tepat satu `[gambar wafak]`.
Penanda M84 berdiri sebagai satu paragraf, sedangkan penanda M85
berada di tengah paragraf ketiga. Arsip dan data sumber mempertahankan
bentuk tersebut. Sesuai aturan pengguna, keluaran Markdown/DOCX
mengganti setiap penanda dengan crop presisi yang sudah ada untuk
halaman yang sama, `84.jpg` dan `85.jpg`, serta menghapus lokasi crop
lama pada unit masing-masing sehingga 26 crop tetap tampil tepat satu
kali. Khusus M85, pemisahan teks sebelum dan sesudah crop hanya terjadi
pada penyajian keluaran; paragraf sumbernya tetap satu.

Seluruh bacaan, harakat, pembagian paragraf, ejaan, tanda, dan susunan
antarhalaman dipertahankan sebagaimana kiriman pengguna; tidak ada
normalisasi atau tambahan editorial. Latin, Terjemahan, Syarah/catatan,
Metode/Khususiyah, tabel, dan pilihan 26 berkas crop tidak diganti.
Parser dan penerapannya adalah
`scripts/al_qorin_parse_user_arab_replacement_h84_85_revised.py` dan
`scripts/al_qorin_apply_arab_replacement_h84_85_revised.py`; renderer
penanda bersama kini mendukung penanda yang berdiri sendiri maupun di
tengah paragraf.

Audit ini mencatat provenans serta ruang lingkup penggantian. Audit ini
tidak menyatakan setiap bacaan revisi telah dibuktikan satu-satu
terhadap pindaian kitab asli.
