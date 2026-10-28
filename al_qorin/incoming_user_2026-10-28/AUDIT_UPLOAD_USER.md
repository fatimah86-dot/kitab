# AUDIT UPLOAD USER — 28 Oktober 2026

Status: **TIDAK DITIMPAKAN sebagai master.** Berkas unggahan diamankan apa
adanya di folder ini. Sesudah pengguna memilih integrasi selektif aman, hanya
temuan Lapis 4/5 yang terverifikasi terhadap master kanonis dan pindaian kitab
asli yang dimasukkan melalui berkas override terpisah.

## Berkas diterima

| Berkas lokal | Asal unggahan | Byte | SHA-256 |
|---|---|---:|---|
| `REVISI_AL_QORIN_123_USER_UPLOAD.md` | `REVISI_x5f_AL_x5f_QORIN_x5f_123.md` | 262022 | `228685b93310c8d003a62d0ca204599fa818b6d7098863c282d775082de5dc8f` |
| `STATUS_AL_QORIN_USER_UPLOAD.md` | `STATUS_x5f_AL_x5f_QORIN.md` | 719 | `bc56e570d328b4a3b135e2ab9357984ffd65da39aa2b63032c0ab01f38b6623a` |
| `M104-M122_FINAL_V2_DARI_PINDAIAN_ASLI.docx` | berkas `.docx.txt` unggahan | 41584 | `8507a8b60f201f2cb9c4b3715fc9c07d49abca410e1f7fe0e23d2c3a43eb9bc5` |

Path persis pada perintah (`/tmp/REVISI_AL_QORIN_123.md` dan
`/tmp/STATUS_AL_QORIN.md`) tidak ada; Arena menyimpan lampiran di
`/tmp/arena-coding-uploads/` dengan nama berenkode `_x5f_`.

## Hasil gerbang periksa terhadap MD unggahan

| Gerbang standar | Wajib | Terukur pada unggahan | Hasil |
|---|---:|---:|---|
| Unit SAMPUL+M01–M122 | 123 blok | 89 blok `##` | gagal |
| Unit dengan lima lapis markdown | 123 | 79 | gagal |
| Crop `wafaq_qorin/<hal>.jpg` | 26 | 0 | gagal |
| `[CATATAN PENERJEMAH]` | 25 | 0 | gagal |
| Blok Qarinah mandiri | 0 | 0 | lolos hitung ini |
| Placeholder kosong | 0 | pola `[Text Arab]`, `[Latin]`, `[Terjemahan]`, `[Metode]`, `[Catatan]` berulang | gagal |
| Satu unit per artikel | 123 | ada gabungan M72-74, M75-76, M77-78, M79-82, M83-86, M87-96, M97-103, M111-115, M116-121 | gagal |

SAMPUL–M64 pada unggahan berupa templat lapis baru yang diikuti potongan lapis
lama dan terpotong; M65–M103 memuat ringkasan tambahan tetapi banyak unit
digabung; M104–M122 memakai format polos tanpa heading lapis markdown dan
sebagian Arab/Latin/Terjemahan disingkat dengan elipsis.

DOCX `M104-M122...` ternyata hanya berisi empat blok judul:
M104, M105, M106-M107, dan M108-M109. Ia tidak memuat blok terpisah sampai
M122. Isinya tetap diamankan sebagai bahan audit/kandidat koreksi M104–M109,
bukan sebagai master final.

STATUS unggahan juga belum dapat ditimpakan apa adanya: rentang
“SAMPUL-M15 + M65-M122” bukan 23 unit, sedangkan klaim 25 label dan 26 media
tidak cocok dengan isi MD unggahan di atas.

## Keputusan dan tindak lanjut

Pengguna memilih **integrasi selektif aman**. Master kanonis
(`../REVISI_AL_QORIN_123.md`) tetap menjadi dasar karena memuat 123 unit, 615
lapis, 25 label, empat tabel, dan 26 crop pengguna. Paket unggahan tidak
disalin mentah ke Markdown, DOCX, STATUS, atau berkas `.html`.

Penajaman pasca-pilot yang diterima dicatat secara reproduksibel di
`../overrides_upload_selektif_2026-10-28.json` dan diterapkan oleh
`../../scripts/al_qorin_build_integrated.py` hanya pada M68, M70, M71, M104,
M105, M106, M107, M109, M116, M120, M121, dan M122:

- Khususiyah ditajamkan pada M68, M70, M71, M105, M106, M107, M109, M116,
  M120, dan M121 berdasarkan frasa Arab/Terjemahan/Catatan kanonis.
- Catatan penyunting hanya ditambah pada M104 dan M107 untuk menyatakan
  selisih bacaan terhadap pindaian asli; Lapis 1–3 tidak diganti.
- Metode M122 dikoreksi agar cocok dengan Arab/Terjemahannya: salat dua
  rakaat, selawat kepada Nabi sepuluh kali, lalu al-Fatihah untuk Syekh
  Muhammad Sibami. Versi pilot historis tetap dipertahankan apa adanya;
  hanya blok Metode terintegrasi M122 yang berbeda dari pilot.
- Penentuan Jam tidak diubah. Aritmetika kandidat seperti M105 `11004`,
  M107 `11+21=32`, M110 `300+40+5=345`, dan gabungan M116–M121
  `100+41=141` ditolak karena bukan penjumlahan jam yang dibuktikan oleh
  unit masing-masing.

Builder membandingkan hasil selektif dengan snapshot pasca-pilot dan menolak
perubahan di luar Khususiyah, penambahan Catatan penyunting, serta pengecualian
Metode M122. Dengan begitu Arab, Latin, Terjemahan, Penentuan Jam, tabel,
heading, nomor halaman, label yang tertanam dalam teks, dan crop tetap sama.

Sesudah integrasi, DOCX serta dua preview HTML dibangun ulang dari master.
Pengecekan akhir menghasilkan 123 unit, 615 lapis, 26 figure crop, dan seluruh
18 test lulus. Integrasi ini adalah penajaman sebagian Lapis 4/5, bukan klaim
bahwa 123 unit telah selesai dikurasi semantik secara manual.
