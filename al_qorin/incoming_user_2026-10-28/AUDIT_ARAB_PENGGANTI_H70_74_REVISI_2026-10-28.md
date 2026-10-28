# AUDIT TEKS ARAB HALAMAN 70 DAN 74 REVISI — 28 OKTOBER 2026

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h70_74_revised/teks arab halaman 70 dan 74 revisi.txt` | 3.331 byte | `32d6d753303b27bec06aae4115a7facd3ae3a097c8a2f4c14d28298888e9a87a` |

Sesudah menerima daftar halaman yang masih memuat bagian tidak terbaca,
pengguna mengirim revisi untuk halaman 70 dan 74. Kiriman ini
menggantikan hanya segmen M70 dan M74 dari arsip halaman 63–122;
M71–M73 dan unit lain tidak berubah.

Pesan pengguna memuat isi halaman 70 dua kali dan, sebelum salinan
lengkap halaman 74, sebuah potongan awal halaman 74 yang terputus.
Hanya satu salinan lengkap untuk masing-masing halaman yang diarsipkan
dan diterapkan; duplikasi tempelan dan potongan terputus itu tidak
dimasukkan sebagai isi halaman. Heading `(Halaman 70)` dipetakan ke M70
dan heading `-٧٤- (Halaman 74)` dipetakan ke M74.

Jumlah paragraf sumber berubah dari M70 8 dan M74 7 menjadi M70 7 dan
M74 7. Total paragraf sumber Arab 123 unit menjadi **547**. Setiap
halaman memuat tepat satu paragraf `[gambar wafak]`; sesuai aturan
pengguna, keluaran Markdown/DOCX mengganti penanda itu dengan crop
presisi yang sudah ada untuk halaman yang sama—`70.jpg` pada M70 dan
`74.jpg` pada M74—lalu menghapus lokasi crop lama pada unit yang sama
sehingga 26 crop tetap tampil tepat satu kali. Arsip sumber
mempertahankan `[gambar wafak]`.

Seluruh bacaan, harakat, susunan antarhalaman, bagian tanpa harakat pada
M70, ejaan, tanda, serta angka dan pengulangan pada M74 dipertahankan
sebagaimana kiriman pengguna; tidak ada normalisasi atau hitungan baru
yang ditambahkan. Latin, Terjemahan, Syarah/catatan, Metode/Khususiyah,
tabel, dan pilihan 26 berkas crop tidak diganti. Parser dan
penerapannya adalah
`scripts/al_qorin_parse_user_arab_replacement_h70_74_revised.py` dan
`scripts/al_qorin_apply_arab_replacement_h70_74_revised.py`.

Audit ini mencatat provenans serta ruang lingkup penggantian. Audit ini
tidak menyatakan setiap bacaan revisi telah dibuktikan satu-satu
terhadap pindaian kitab asli.
