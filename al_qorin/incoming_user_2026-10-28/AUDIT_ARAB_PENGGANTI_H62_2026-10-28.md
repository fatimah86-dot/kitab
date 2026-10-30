# AUDIT TEKS ARAB PENGGANTI SAMPAI HALAMAN 62 — 28 OKTOBER 2026

## Berkas yang diarsipkan

| Berkas arsip | Ukuran | SHA-256 |
|---|---:|---|
| `arab_replacement_h62/teks arab pengganti sampai halaman 62.txt` | 129.958 byte | `2625d048c67ec6f5fd6328bbb2d8a35d63e16909c3c727f1c9b8abbed35448e4` |

Teks diterima lewat chat dan disalin ke arsip di atas. Kalimat pengantar
sebelum heading `SAMPUL` disimpan dalam arsip tetapi tidak dimasukkan ke
Lapis 1 atau dokumen Word.

## Hasil parse dan pemetaan

- Heading `SAMPUL` dan nomor `1`–`62` terurut lengkap: **63 unit**.
- Nomor halaman dipetakan satu-satu ke unit yang sudah ada: `1 → M01`,
  `2 → M02`, …, `62 → M62`.
- Tiap baris isi yang tidak kosong diperlakukan sebagai satu paragraf Arab.
  Tanda `*` di awal butir halaman 52–54 adalah penanda daftar kiriman dan
  tidak dirender sebagai bagian kalimat Arab.
- Total hasil parse: **277 paragraf Arab**.
- Sebagai pembanding, Lapis 1 lama pada rentang yang sama berjumlah
  279 paragraf. Selisih dua paragraf berasal dari penggabungan paragraf
  pada M12 dan M32 dalam kiriman baru, bukan penghapusan satu unit.
- Sesudah penggantian, total paragraf Arab seluruh 123 unit menjadi
  **538**: 277 paragraf baru sampai M62 + 261 paragraf lama M63–M122.

## Keputusan pemakaian

Sesuai perintah pengguna, teks ini menggantikan Lapis 1 untuk SAMPUL dan
M01–M62 pada master terintegrasi serta edisi bersih. Lapis 2 Latin,
Terjemahan, Syarah/catatan, Metode/Khususiyah, tabel, dan 26 crop pengguna
tidak diganti oleh tahap ini. Arab M63–M122 tetap berasal dari arsip TXT
pengguna yang dikunci pada commit `bcb7f5d`.

Parser reproduksibelnya adalah
`scripts/al_qorin_parse_user_arab_replacement_h62.py`; penerapan ke
Markdown keluaran memakai
`scripts/al_qorin_apply_arab_replacement_h62.py`.

## Batas audit

Penggantian ini adalah keputusan provenans dari pengguna. Audit di sini
memverifikasi kelengkapan heading, pemetaan unit, jumlah paragraf, dan
bahwa hanya Lapis 1 yang berubah; audit ini tidak menyatakan bahwa setiap
perbaikan harakat/typo dalam kiriman telah dibuktikan satu-satu terhadap
pindaian kitab asli.
