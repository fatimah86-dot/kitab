# AUDIT SUMBER AL-QORIN — 28 Oktober 2026

**Tujuan:** membuktikan kedua sumber wajib sudah dibaca sebelum menerjemahkan, mengukur pekerjaan revisi 123 artikel, dan mencatat semua celah/konflik terhadap `STANDAR_MUTLAK_AL_QORIN_123.md`.
**Branch:** `arena/47599fd2-kitab` · **Sifat audit:** baca-saja. Tidak ada suntingan pada Google Doc/Drive. Tidak ada inferensi isi PDF scan.

---

## 1. Identitas sumber (terverifikasi lewat Google Drive)

| # | Berkas | ID | Jenis / ukuran | Tanggal ubah (UTC) | Peran menurut pengguna |
|---|---|---|---|---|---|
| A | `AL_QORIN_TEKS_KIRIMAN_SAMPUL_HAL122_DRAF (4).docx` | `1-keEWHFNdn4BancGVZVvdx0yVVezibZx` | DOCX, 562.931 byte | 2026-10-28T02:04:01Z | **Terjemahan yang harus direvisi (target)** |
| B | `al qorin war riyadhah.pdf` | `1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z` | PDF, 7.604.573 byte | 2026-10-14T04:47:42Z | **Kitab aslinya (acuan scan)** |
| C | `KITAB AL-QORIN - EDISI REVISI LENGKAP 5 LAPIS - FINAL KHATAM.docx` | `1sUpIWi143-NRAmtm_GhS7_vlCGYjPjR6` | DOCX, 13.575.733 byte | 2026-10-26T21:16:48Z | Bukan target yang ditunjuk — jangan dipakai tanpa perintah |
| D | `KITAB AL QORIN.docx` | `1jcPcn4IpZeEYz1oMis3_RcMIIPvnFhSt` | DOCX, 70.880 byte | 2026-10-26T18:20:07Z | Draf lama bergaya lain — bukan target |

Hasil baca:

- **A terbaca sebagai teks** (ekstraksi sukses, tidak terpotong oleh API; tampilan tengah terpotong oleh batas konteks alat, sehingga pengukuran dilakukan juga dengan pencarian terarah per istilah). Kop A berbunyi: “AL-QORIN WAR RIYADHAH — draf ekstrak (dibangun ulang dari JSON) / 123 unit = SAMPUL + M01–M122 · 5 bagian per unit · label shorof & hukum baca · penanda elipsis eksplisit”, plus catatan rajah hal.65–73 dan bingkai “tidak dianjurkan, tidak disahkan, tanpa jaminan khasiat”. Unit terakhir terbaca sebagai penutup/الخاتمة; teks A sendiri menegaskan halaman penutup **tanpa nomor halaman yang terbaca** dan “saya tidak memberi nomor 122” — penomoran **M122 adalah nomor unit/modul**, jangan dicampur dengan nomor cetak.
- **B tidak menghasilkan teks sama sekali** (`extraction_status: empty`): scan/foto tanpa lapisan teks. Sesuai batas alat, **isi B tidak diulang-coba dan tidak ditebak**. Akibatnya: pencocokan Arab A terhadap B hanya mungkin per citra halaman; audit ini tidak mengklaim satu huruf pun dari B.
- **C kopnya** menyatakan “121 HALAMAN + PENUTUP”, unit berbasis **halaman cetak**, judul lapis “Lapis 1 — ARAB BERHARAKAT …”, memuat pindai/crop tersemat (sebab ukurannya 13,5 MB), dan menegaskan “Tidak direka halaman cetak 1 atau 122.” Sistem unit C **berbeda** dari sistem M01–M122 pada A/standar pengguna.
- **D kopnya** bergaya lama (“Latin Washal Bunyi”, “Terjemah … Gaya Pesantren”, gabungan HAL 02-03) dan memuat tambahan syarah tanpa sumber yang jelas. D hanya dicatat sebagai arsip pembanding gaya yang **tidak** diikuti.

> Kesimpulan target: perintah pengguna (“SAMPUL + M01-M122 = 123”) cocok **hanya** dengan A. Revisi dikerjakan pada A terhadap acuan B.

---

## 2. Pengukuran draf A (pencarian Google Docs, 28-10-2026)

Dokumen: 1 tab (`t.0`, “Tab 1”). Indeks akhir tidak berhasil diambil (alat `get_document_end_index` mengembalikan `provider_unavailable` dua kali; tidak diulang paksa). Batas bawah panjang teks dari kecocokan terakhir: **≥ 1.072.145 karakter** (`M122` pada indeks 1.072.141).

| Kueri | Total kecocokan | Makna |
|---|---:|---|
| `1. ARAB` | **123** | 123 unit hadir |
| `2. LATIN` | **123** | Lapis 2 lengkap per unit |
| `3. TERJEMAHAN` | **123** | Lapis 3 lengkap per unit |
| `4. SYARAH` | **123** | Lapis 4 lama lengkap (akan dipetakan ulang) |
| `5. PETUNJUK` | **123** | Lapis 5 lama lengkap (akan dipetakan ulang) |
| `M07` | 1 (+ konteks `M07 — BAB PERTAMA, HALAMAN 7`, indeks 69.530) | M adalah nomor modul/unit, kerap merujuk halaman cetak di judulnya |
| `M122` | 2 (kop + `M122 — الخاتمة, halaman penutup kitab (tanpa …`) | Unit penutup ada |
| `Qarinah` (tanpa peka kapital) | **590** | Semua pemakaian kata |
| `Qarinah qabliah` | **285** | Blok/label qabliah |
| `diah:` (ekor `ba‘diah:`) | **285** | Blok/label ba‘diah |
| `CATATAN PENERJEMAH` | **25** | Label wajib dipertahankan; contoh awal pada indeks 848.748 |
| `penjumlahan` | **0** | Format penjumlahan belum ada di A; harus diterapkan bersyarat-angka saat revisi |
| `Shorof:` | **127** | Komponen dikte lama di Lapis 4 lama |
| `Hukum baca:` | **118** | Komponen dikte lama di Lapis 4 lama |

**Soal angka 288:** perintah menyebut “HAPUS 288 paragraf” Qarinah, sedangkan label terukur 285 pasang. Selisih +3 belum dapat dijelaskan dari pencarian kata saja (kemungkinan: bentuk gabungan `Qarinah qabliah/ba‘diah:`, varian `Qarinah:` tunggal di SAMPUL, atau basis hitung paragraf vs label). **Jangan memaksakan 288.** Saat eksekusi, hitung per paragraf, laporkan daftar unitnya, dan selisihnya dinyatakan terbuka.

**Soal 285 > 123:** blok Qarinah ada **per segmen/paragraf di dalam** Lapis 4 lama (rata-rata ±2,3 pasang per unit), bukan satu per unit. Penghapusan harus bedah-paragraf, bukan hapus-per-unit.

---

## 3. Wafaq crop `<halaman>.jpg` — belum ditemukan

Pencarian yang sudah dilakukan (semua negatif untuk nama persis):

- Repo `kitab`: tidak ada berkas `49.jpg`, `58.jpg`, `64.jpg`, … `121.jpg` (pola `[0-9]*.jpg/png` bernomor halaman: nihil).
- Google Drive: kueri nama persis `49.jpg / 58.jpg / 64.jpg / 66.jpg / 69.jpg / 121.jpg` → **0 berkas**.
- Drive: kueri nama mengandung `wafaq/WAFAQ/rajah/crop` → 51 berkas, semuanya dokumen lain / `crop_ContactPhoto-*.jpg` (foto kontak lama), bukan crop halaman Al-Qorin.
- Folder bernama relevan (`wafaq/rajah/QORIN/crop/halaman/Media`) → hanya `Kunci Media` (`1nNflcdYfSq8OUfAqTPFTMY25M2yUyBH1`, 82 berkas media lain; tidak ada crop Al-Qorin).
- Folder induk PDF B (`1g7iRKRQCuKfzWHzENikGIaThPMLHUIHp`) adalah perpustakaan PDF besar (≥100 berkas, ada token halaman berikutnya); bukan folder crop. Folder induk A (`0AGwf6yHr4AZfUk9PVA`) adalah akar My Drive (96 berkas).
- Satu-satunya tempat crop/pindai Al-Qorin **pasti ada** saat ini adalah **tersemat di dalam C** (kop C: “Gambar sumber dan crop langsung dipertahankan pada profil JPEG 70 / skala 1,5×”). Mengekstrak dari C memerlukan izin eksplisit karena C bukan sumber yang ditunjuk.

**Akibat:** aturan “sisip `<hal>.jpg` setelah blok Metode” belum dapat dieksekusi sampai pengguna menunjuk lokasi crop atau mengizinkan ekstraksi. Dilarang menggambar ulang / mengarang crop pengganti.

Catatan rajah bawaan A (dipertahankan apa adanya): hal.65–73 diperiksa 9/23; wafaq berpetak hal.66 & 69; hal.65 & 67 salinan linear; hal.68, 70, 71, 73 tanpa wafaq berpetak; hal.72 tanpa rajah sama sekali.

---

## 4. Keadaan repo & builder lama (mengapa tidak bisa langsung pakai)

Repo berisi 536 berkas (±841 MB di luar `.git`): 205 PNG, 109 MD, 97 HTML, 84 DOCX, 30 JPG, 6 PY, 3 PDF. Isinya adalah dua kitab **lain** yang sudah khatam — Abū Ma‘syar (56 hal. PDF) dan Anwar Mujarobat (65 hal.) — **belum ada** berkas kerja Al-Qorin. Al-Qorin adalah pekerjaan baru di repo ini; dilarang mencampur nomor halamannya dengan Anwar 65 / Abū Ma‘syar.

Pemeriksaan builder Anwar (`scripts/build_final_65.py` + hasil `REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.docx`):

| Syarat standar Al-Qorin | Keadaan builder/hasil lama | Putusan |
|---|---|---|
| Arab `w:jc=start` + `w:bidi` | XML hasil: `jc` hanya `left` 2.105×, `right` 583×, `center` 389×; **`start` 0×** (builder memakai `WD_ALIGN_PARAGRAPH.RIGHT`) | **Belum patuh** — builder Al-Qorin wajib menulis `start` secara harfiah |
| Latin kiri LTR | `left` + `bidi=0` | Patuh secara perilaku; pertahankan |
| Wafaq tengah `w:jc=center` | Paragraf gambar & sel tabel di-center; tabel `WD_TABLE_ALIGNMENT.CENTER` + `bidiVisual` | Patuh; pertahankan |
| Font Amiri tersemat | “Traditional Arabic” 26.156×, **Amiri 0×**; paket hanya `word/fontTable.xml`, tanpa part font tersemat; tidak ada berkas font Amiri di repo/sistem; `python-docx` bahkan belum terpasang di sandbox ini (perlu `.venv` per `CATATAN_REVISI_2026-10-27.md`) | **Belum patuh** — perlu font Amiri + mekanisme penyematan DOCX yang terverifikasi; jangan diklaim sebelum bukti paket ada |
| 5 lapis (judul baru §1 standar) | Judul lama: `arab/latin/Terjemahan/Syarah dan Penjelasan/Khususiyah dan Tatacara Praktik`; tes `tests/test_final_65.py` mengunci 65 blok × 5 judul lama + 16 media | Tes/builder lama **khusus Anwar**; Al-Qorin perlu builder + tes sendiri (123 × 5, judul baru, gerbang §7 standar) |
| Crop `<hal>.jpg` setelah Metode | Builder lama: peta keras `WAFAQ_MAP` 16 berkas `IMG_20261025_*.jpg` dari `rajah_anwar_FINAL_300DPI/`, disisip di bawah tabel Arab | **Tidak dapat dipakai** untuk Al-Qorin (nama, sumber, dan posisi sisip berbeda) |

Template HALAMAN 07: naskah per-berkas `REVISI_HAL07_MAYSARAH_2_3.md` terpotong (Syarah hanya poin 1); versi **master** `REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md` utuh (poin 1 Metode + poin 2 Penentuan Jam + catatan penjumlahan 26 vs 27). Yang dijadikan acuan pola adalah **versi master**, bukan berkas per-halaman.

---

## 5. Risiko & keputusan yang harus diambil pengguna sebelum eksekusi

1. **Target ganda:** A (ditunjuk, sistem M) vs C (sistem halaman cetak + gambar tersemat). Audit merekomendasikan tetap pada A sesuai tautan perintah; C hanya boleh menjadi sumber crop/pembanding bila diizinkan.
2. **Makna “HALAMAN 07”:** bukti terkuat menunjuk HALAMAN 07 Anwar master (sumber satu-satunya pola Metode/Penentuan Jam/penjumlahan/Waktu-Media-Bukhur). Alternatifnya (M07 di A) tidak memuat pola itu. Perlu penegasan satu kata dari pengguna.
3. **Batas “dikte panjang”:** apakah seluruh uraian nahwu/`Shorof:`/`Hukum baca:` dibuang, sementara penanda ketidakpastian bacaan (yang kini menempel di uraian yang sama) dipindah ringkas ke “Catatan penyunting”? Salah batas = kehilangan jejak tahqiq secara permanen.
4. **Sumber crop:** unggahan baru / folder Drive lain / ekstraksi dari C / tunda gambar. Tanpa keputusan ini, hasil hanya boleh berupa teks 5 lapis + daftar crop hilang.
5. **Pemetaan M ↔ halaman cetak ↔ lembar PDF B:** judul unit A menyebut halaman (mis. M07 = halaman 7), kop C memakai pemetaan lembar↔cetaknya sendiri (sampul = lembar 1; cetak 2–3 = lembar 2 kanan/kiri; penutup = lembar 62). Nama crop memakai “halaman tujuan” — harus ditegaskan halaman **apa** (cetak pada kitab / nomor M / urutan Word) agar `49.jpg` tidak salah rumah.
6. **Verifikasi ke scan B:** B tanpa teks; tanpa citra per halaman di ruang kerja, revisi hanya sah sebagai **restrukturisasi draf A**, bukan tahqiq terhadap scan. Klaim hasil harus menyebut batas ini.

---

## 6. Rencana eksekusi yang diusulkan (belum dijalankan)

1. Bekukan salinan kerja A sebagai master teks lokal (ekstrak per unit SAMPUL, M01–M122; buktikan 123 × 5 judul lama sebelum menyentuh isi).
2. Bedah per unit: pertahankan Lapis 1–3; suling Lapis 4 lama + Lapis 5 lama menjadi Lapis 4–5 baru **hanya dari kalimat yang sudah ada**; hapus blok Qarinah per paragraf (log sebelum/sesudah per unit); terapkan aturan penjumlahan bersyarat-angka; pertahankan 25 `[CATATAN PENERJEMAH …]`.
3. Sisipkan crop `<hal>.jpg` (setelah sumbernya sah) di tengah sesudah blok Metode; halaman tanpa crop dicatat.
4. Bangun DOCX baru khusus Al-Qorin: Arab `jc=start`+`bidi` font **Amiri tersemat**, Latin LTR kiri, wafaq `jc=center`; sertakan tes otomatis 123×5 + gerbang §7 standar. Kerjakan **per batch kecil** (mis. pilot SAMPUL+M01–M05 untuk disetujui gayanya) sebelum 123 unit penuh.
5. Unggah hasil sebagai berkas **baru** (jangan menimpa A/C/D tanpa perintah) dan laporkan tautan + ukuran + hasil tes.

*Audit selesai. Penerjemahan/revisi belum dimulai — menunggu penegasan pengguna atas §5.*
