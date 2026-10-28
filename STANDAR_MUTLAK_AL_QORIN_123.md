# STANDAR MUTLAK AL-QORIN — 123 ARTIKEL (TERKUNCI)

**Status:** TERKUNCI — wajib dibaca dan dipatuhi sebelum menerjemahkan/merevisi unit mana pun. Jangan dilanggar.
**Tanggal kunci:** 28 Oktober 2026
**Branch kerja:** `arena/47599fd2-kitab`
**Pasangan audit:** `AUDIT_SUMBER_AL_QORIN_2026-10-28.md`

---

## 0. Sumber wajib (baca dulu, baru bekerja)

| Peran | Berkas | ID / tautan | Fakta terverifikasi 28-10-2026 |
|---|---|---|---|
| Terjemahan yang harus direvisi | `AL_QORIN_TEKS_KIRIMAN_SAMPUL_HAL122_DRAF (4).docx` | `1-keEWHFNdn4BancGVZVvdx0yVVezibZx` — https://docs.google.com/document/d/1-keEWHFNdn4BancGVZVvdx0yVVezibZx/edit | DOCX 562.931 byte; 1 tab (`t.0`); teks ≥ 1.072.141 karakter; kop: “123 unit = SAMPUL + M01–M122 · 5 bagian per unit” |
| Kitab asli | `al qorin war riyadhah.pdf` | `1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z` — https://drive.google.com/file/d/1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z/view | PDF 7.604.573 byte; **scan gambar tanpa lapisan teks** (ekstraksi teks = kosong). Isinya **tidak boleh ditebak**; verifikasi huruf-harakat terhadap scan hanya sah dari citra halaman, bukan dari OCR/tebakan. |

Berkas lain di Drive (`KITAB AL-QORIN - EDISI REVISI LENGKAP 5 LAPIS - FINAL KHATAM.docx`, `KITAB AL QORIN.docx`) **bukan** sumber yang ditunjuk. Dilarang diam-diam beralih target ke berkas-berkas itu.

---

## 1. Struktur baku 123 artikel

- **Total = SAMPUL + M01–M122 = 123 unit.** Tidak boleh kurang, tidak boleh lebih, tidak boleh ada unit ganda.
- Setiap unit **WAJIB 5 lapis berurutan**, gaya **HALAMAN 07** menjadi template (lihat §6):
  1. **Lapis 1 — Arab (kanan)**
  2. **Lapis 2 — Latin (kiri)**
  3. **Lapis 3 — Terjemahan**
  4. **Lapis 4 — 1. Metode / 2. Penentuan Jam / Catatan penyunting**
  5. **Lapis 5 — Khususiyah — Waktu : Media : Bukhur**
- Urutan lapis tidak boleh ditukar. Lapis kosong tidak boleh dibiarkan tanpa keterangan baku (lihat aturan “tidak ada …” pada §3).
- **Amandemen aturan lapis kondisional (keputusan pengguna, 2026-10-28):** tiga unit
  dikecualikan dari kewajiban 5 lapis berdasarkan jenis isinya yang terbukti dari teks:
  **SAMPUL hanya Lapis 1–3** (teks sampul: القرين والرياضات / تأليف / دار الفكر; catatan
  penyunting sampul tidak dibuang, melainkan dipindah ke akhir Lapis 3 dengan penanda
  “Catatan penyunting sampul:”), **M01 hanya Lapis 1–4** (Muqodimah — berjudul eksplisit
  مُقَدِّمَةٌ, memuat بسم الله/الحمد لله, tanpa تكتب), dan **M122 hanya Lapis 1–4**
  (Khatimah — الخاتمة, tanpa تكتب). Untuk M01/M122 yang dihilangkan hanya Lapis 5 yang
  seluruh isinya “tidak disebutkan”; Metode dan Catatan penyunting tetap tampil penuh.
  Klasifikasi ini adalah daftar tetap terverifikasi, **bukan** uji kata kunci mekanis:
  pengujian harfiah atas Arab kanonis terbukti menyesatkan (mis. وَفَّقَنِي di M122 memuat
  “وفق”; unit bercrop M58/M85/M98 tidak memuat kata kerja daftar; 72 unit tidak masuk
  kategori mana pun). 120 unit lain tetap 5 lapis; total judul lapis tampil = **611**.
  Data JSON unit tidak berubah — pembatasan hanya pada render Markdown/DOCX/HTML.

### Pemetaan dari judul lapis lama di draf (agar tidak mengarang)

Draf saat ini memakai `1. ARAB / 2. LATIN / 3. TERJEMAHAN / 4. SYARAH DAN PENJELASAN / 5. PETUNJUK YANG ADA DALAM SUMBER` (masing-masing terhitung **123×**). Revisi memetakan isinya — **tanpa mengarang ulang** — sebagai berikut:

| Lapis baru | Diambil dari | Isi yang sah |
|---|---|---|
| 1. Arab | `1. ARAB` lama | Teks Arab apa adanya dari draf; koreksi hanya bila dapat ditunjuk pada scan asli. |
| 2. Latin | `2. LATIN` lama | Transliterasi yang sudah ada; tidak membuat sistem latin baru. |
| 3. Terjemahan | `3. TERJEMAHAN` lama | Terjemahan yang sudah ada; label `[CATATAN PENERJEMAH …]` dipertahankan persis (§3). |
| 4. Metode / Penentuan Jam / Catatan penyunting | Hanya bahan metode, hitungan jam, dan catatan ketidakpastian yang **sudah ada** di `4. SYARAH…` + `5. PETUNJUK…` lama | Lihat §2–§3. Sisa dikte panjang dibuang (§2). |
| 5. Khususiyah Waktu:Media:Bukhur | Hanya keterangan waktu/media/bukhur yang **sudah ada** di `5. PETUNJUK…` lama (dan matan unit itu) | Bila sumber unit tidak menyebutnya, jangan diada-adakan. |

---

## 2. Yang dihapus total

1. **Qarinah qabliah/ba‘diah = HAPUS.** Perintah menyebut **288 paragraf**. Hasil ukur pada draf `(4)` tanggal 28-10-2026: `Qarinah qabliah` **285×**, `ba‘diah:` **285×**, kata `Qarinah/qarinah` total **590×** (termasuk bentuk gabungan `Qarinah qabliah/ba‘diah:` dan pemakaian kata di dalam kalimat syarah). Selisih 285 vs 288 **wajib dihitung ulang per paragraf saat eksekusi** dan dilaporkan; yang dihapus adalah **paragraf/blok Qarinah**-nya, bukan sekadar kata “qarinah” di tengah kalimat yang bukan blok Qarinah — kecuali bila pengguna menegaskan lain. Sesudah revisi, blok Qarinah qabliah/ba‘diah harus **0**.
2. **Gaya dikte panjang = HAPUS.** Yang dimaksud: uraian bertele-tele di lapis syarah lama (termasuk label berulang `Shorof:` **127×** dan `Hukum baca:` **118×** pada draf) tidak dipertahankan sebagai dikte panjang di Lapis 4 baru. Lapis 4 baru hanya memuat **Metode, Penentuan Jam, Catatan penyunting** (§1). Batas persis “dikte panjang” yang dibuang vs catatan ketidakpastian yang wajib dipertahankan harus mengikuti penegasan pengguna; penanda ketidakpastian bacaan tidak boleh hilang diam-diam.
3. **Jangan dikarang ulang.** Dilarang menulis metode, jam, media, bukhur, khasiat, dalil, atau penjelasan baru yang tidak ada di draf/scan unit tersebut. Bila ragu, tuliskan sebagai belum pasti — jangan mengisi kekosongan dengan karangan.

---

## 3. Yang dipertahankan mutlak

1. **Wafaq tetap tengah** — `w:jc=center` (paragraf gambar/tabel wafaq di tengah).
2. **Arab kanan** — `w:jc=start` **+** `w:bidi` pada paragraf Arab, dan `w:rtl` pada seluruh run Arab termasuk tanda baca netral/tanda kurung agar tanda penjodoh tidak terbalik penempatannya. (Catatan audit: builder Anwar lama memakai `right`, bukan `start` — untuk Al-Qorin wajib `start` sesuai standar ini.)
3. **Latin kiri** — `direction:ltr` (paragraf Latin/Indonesia LTR, rata kiri).
4. **Font Amiri tersemat.** Font Arab = **Amiri** dan disematkan (embedded) pada DOCX hasil. (Catatan audit: builder lama memakai “Traditional Arabic” tanpa penyematan font — wajib diganti; keberhasilan penyematan harus dibuktikan dari isi paket DOCX, bukan diklaim.)
5. **Label `[CATATAN PENERJEMAH …]` dipertahankan.** Pada draf terhitung **25×** (mulai sekitar indeks 848.748). Jumlah dan bunyinya tidak boleh berkurang/berubah tanpa catatan.
6. **Penjumlahan jam bersyarat angka:**
   - Format baku: **“penjumlahan … = …, bukan …”** — **HANYA** bila di halaman/unit itu memang ada angka hitungan pada sumbernya.
   - Bila tidak ada angka, tulis persis: **«tidak ada hitungan di halaman ini»**.
   - Dilarang memaksakan hitungan pada unit tanpa angka. (Pada draf Al-Qorin kata `penjumlahan` saat ini **0×** — aturan ini adalah pemeriksaan baru saat revisi, meniru pola HALAMAN 07 Anwar: “penjumlahan biasa 6 + 1 + 5 + 4 + 10 menghasilkan 26, bukan 27”.)

---

## 4. Aturan wafaq crop

- **Nama file = halaman tujuan.** Contoh: `49.jpg` = halaman 49, `58.jpg` = halaman 58, `64.jpg` = halaman 64, dan seterusnya sampai `121.jpg`.
- **Sisip di tengah halaman, setelah blok Metode** (di dalam Lapis 4, sesudah subblok “1. Metode”, sebelum “2. Penentuan Jam”), dengan paragraf tengah (`w:jc=center`).
- Jangan menggambar ulang wafaq/rajah. Jangan menyisipkan crop ke halaman yang bukan tujuannya.
- **Status ketersediaan (audit 28-10-2026):** file bernama persis `49.jpg/58.jpg/64.jpg/66.jpg/69.jpg/121.jpg` **tidak ditemukan** di repo maupun lewat pencarian Drive; folder `Kunci Media` tidak berisi crop tersebut. Sumber crop (folder Drive / unggahan / ekstraksi dari berkas lain) harus ditegaskan pengguna sebelum penyisipan. Selama belum ada, unit dikerjakan tanpa mengarang gambar, dan kekurangan crop dicatat per halaman.
- **Pembaruan pelaksanaan (28-10-2026):** pengguna kemudian mengunggah 26 crop presisi (`49, 58, 64–74, 76–78, 82–86, 98, 109, 116, 120, 121`) dan memerintahkan agar crop tersebut yang dipakai, **bukan** ekstraksi dari FINAL KHATAM. Set FINAL turunan pada tahap sebelumnya dinyatakan tergantikan; manifest kanonis sekarang adalah `al_qorin/wafaq_user_manifest.json` dan berkasnya di `al_qorin/wafaq_qorin/`.
- **Penanda `[gambar wafak]` pada revisi pengguna:** bila Lapis 1 revisi memuat paragraf persis `[gambar wafak]`, crop tujuan yang sudah ada disisipkan di tengah pada posisi penanda itu di dalam Lapis 1. Lokasi lama crop pada unit yang sama dihapus agar crop tetap tampil tepat satu kali; arsip teks sumber tetap menyimpan penandanya.
- Rujukan isi draf tentang rajah: “Rajah diperiksa: hal.65–73 (9 dari 23 halaman). Wafaq berpetak: hal.66 & 69; hal.65 & 67 salinan linear; hal.68, 70, 71, 73 tanpa wafaq berpetak; hal.72 tanpa rajah sama sekali.” — keterangan ini dipertahankan sebagai catatan sumber, bukan diganti klaim baru.

---

## 5. Batas kejujuran editorial (mengikat)

- Praktik/isi dinisbatkan kepada penulis kitab; edisi ini **mencatat dan menerjemahkan sebagai dokumen** — tidak menganjurkan, tidak mengesahkan, tanpa jaminan khasiat/keselamatan, bukan pengganti pertolongan medis. Bingkai ini sudah ada di kop draf dan pada `[CATATAN PENERJEMAH …]`; jangan dihapus.
- Harakat/tanda baca Arab dari draf bersifat editorial/kerja; jangan diklaim sebagai bacaan final tanpa pemeriksaan scan.
- Nama/gelar/organisasi pada sampul dicatat apa adanya, bukan verifikasi. Perbedaan bacaan yang belum pasti (mis. nama penulis pada penutup) dipertahankan sebagai catatan, bukan “dirapikan” diam-diam.

---

## 6. Template HALAMAN 07 — tafsir terkunci (menunggu penegasan akhir pengguna)

Bukti berkas menunjukkan “HALAMAN 07” yang memuat persis pola standar ini adalah **HALAMAN 07 pada master Anwar `REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md`** (Ṭarīqatul-Maysarah 2):

- Lapis Syarah poin 1 = **Metode …**; poin 2 = **Penentuan Jam Amalan (Sā‘atul-‘Amal)** berisi: “Catatan penyunting: penjumlahan biasa `6 + 1 + 5 + 4 + 10` menghasilkan `26`, bukan `27`. Angka `27` dan sisa `6` dipertahankan sebagai bacaan matan; alasan perbedaan ini belum dapat dipastikan.”
- Lapis Khususiyah poin 1 = **Waktu, Media Tulis, dan Bukhur**.

Pola itulah yang digeneralisasi menjadi Lapis 4–5 pada §1. (Di draf Al-Qorin sendiri, `M07 — BAB PERTAMA, HALAMAN 7` masih memakai judul lapis lama dan kata `penjumlahan` 0×, sehingga format penjumlahan tidak mungkin berasal dari M07 draf.) Bila pengguna bermaksud template lain, standar ini direvisi **sebelum** eksekusi massal — bukan di tengah jalan.

### Kerangka unit hasil (untuk builder & pemeriksa)

```text
## [SAMPUL | M01..M122] — <judul unit apa adanya dari draf>

### 1. Arab
<paragraf Arab: jc=start + bidi, font Amiri>

### 2. Latin
<paragraf Latin: LTR rata kiri>

### 3. Terjemahan
<terjemahan; [CATATAN PENERJEMAH …] dipertahankan bila ada>

### 4. Metode, Penentuan Jam, dan Catatan Penyunting
1. Metode: <hanya dari sumber unit>
   [crop wafaq <hal>.jpg di tengah — hanya bila file tujuan halaman ini ada]
2. Penentuan Jam: <hanya bila sumber unit memuat hitungan jam>
   penjumlahan … = …, bukan …   |   atau: «tidak ada hitungan di halaman ini»
Catatan penyunting: <ketidakpastian/perbedaan bacaan apa adanya; tanpa karangan>

### 5. Khususiyah — Waktu : Media : Bukhur
Waktu: … : Media: … : Bukhur: …   <hanya yang disebut sumber unit>
```

---

## 7. Gerbang periksa (gagal satu = belum selesai)

1. Jumlah unit = **123** (SAMPUL + M01–M122, berurutan, tanpa ganda/hilang).
2. Setiap unit tepat **5 lapis** berurutan sesuai §1, kecuali pengecualian kondisional §1 (SAMPUL 3 lapis; M01 dan M122 4 lapis), sehingga total judul lapis tampil = **611**.
3. Blok **Qarinah qabliah/ba‘diah = 0**; laporan hitung sebelum–sesudah dilampirkan (termasuk penjelasan selisih 285 vs 288).
4. `[CATATAN PENERJEMAH` tetap **25×** dengan bunyi sama (atau selisihnya dicatat & disetujui).
5. Setiap unit dengan angka memakai format `penjumlahan … = …, bukan …`; setiap unit tanpa angka memuat persis `«tidak ada hitungan di halaman ini»`; tidak ada unit yang keduanya/mengarang.
6. XML DOCX: paragraf Arab `w:jc=start` + `w:bidi`, seluruh run Arab `w:rtl` termasuk run tanda kurung; Latin LTR kiri; wafaq `w:jc=center`; font Arab **Amiri** + bukti penyematan font di paket DOCX.
7. Crop: setiap `<hal>.jpg` hanya muncul satu kali di halaman tujuannya dan di tengah—setelah blok Metode, kecuali unit revisi berpenanda `[gambar wafak]`, yang cropnya berada pada posisi penanda di Lapis 1; daftar halaman tanpa crop dilaporkan, bukan diisi gambar karangan.
8. Tidak ada metode/jam/media/bukhur/khasiat/dalil baru di luar draf/scan unit bersangkutan (“jangan dikarang ulang”).

---

## 8. Riwayat kunci

- 2026-10-28 — Standar diterima dari pengguna dan dikunci menjadi berkas ini **sebelum** penerjemahan/revisi apa pun. Pada tanggal ini Google Doc sumber hanya **dibaca** (metadata, ekstraksi teks, pencarian hitung); belum ada suntingan.
- 2026-10-28 — Pengguna menegaskan sumber crop: 26 berkas crop presisi unggahan pengguna menggantikan ekstraksi FINAL KHATAM; `116.jpg` termasuk set wajib sisip.
- 2026-10-28 — Amandemen lapis kondisional: pengguna memutuskan SAMPUL tampil 1–3, Muqodimah (M01) dan Khatimah (M122) tampil 1–4, unit amalan/lainnya tetap 1–5 lengkap dengan crop wafaq center; catatan sampul dipindah ke akhir Lapis 3 (lihat §1). Berkas M65 unggahan sesi lain diaudit dan diarsipkan tanpa menimpa M65 kanonis (lihat `al_qorin/incoming_user_2026-10-28/AUDIT_M65_UPLOAD.md`).
- 2026-10-28 — Fase revisi total terjemahan dibuka atas penilaian pengguna bahwa terjemahan sebelumnya belum sempurna. Dokumen Anwar Asy-syaikh Al-Basyir yang ditunjuk pengguna menjadi contoh gaya, dengan adaptasi dan batas yang mengikat dicatat di `al_qorin/PANDUAN_REVISI_TOTAL_TERJEMAHAN_AL_QORIN.md`; audit 123 unit di `al_qorin/AUDIT_REVISI_TOTAL_TERJEMAHAN_123.md`. Arab/Latin hanya boleh diubah dengan bukti pindaian, ketidakpastian tidak boleh dihaluskan, dan wafaq hanya dari 26 crop pengguna. Batch 01 diterapkan pada Lapis 3 SAMPUL dan M01–M05; aturan lapis, arah Arab/Latin, Jam, dan crop pada standar ini tidak berubah.

---

## 9. Amandemen edisi bersih pengguna (2026-10-28)

Pengguna kemudian mengirim dua berkas TXT dan memerintahkan pemakaiannya
sebagai Lapis 1–2. Berkas byte-persisnya diarsipkan di
`al_qorin/incoming_user_2026-10-28/arab_latin_full/` dan diaudit di
`AUDIT_ARAB_LATIN_TXT_2026-10-28.md`. Perintah ini dilaksanakan sebagai
**edisi bersih terpisah** (`AL_QORIN_123_BERSIH.md/.docx`) tanpa menghapus
master riset 611 lapis di §1:

1. Lapis 1–2 diambil dari TXT pengguna sesudah heading `SAMPUL`; judul/meta
   sebelum heading itu tidak masuk Word.
2. Setiap unit tampil `1. Arab`, `2. Latin`, `3. Terjemahan`, dan `4. Syarah`.
3. `5. Khususiyah dan Tatacara Praktik` hanya tampil bila unit benar-benar
   memuat Khasiat atau amalan dengan bilangan/tata cara yang ditentukan;
   bila tidak ada, heading itu tidak ditampilkan.
4. Front matter, header, footer, catatan proses perbaikan, dan kalimat
   percakapan kerja tidak dimasukkan ke DOCX bersih. Khususiyah tetap dari
   Arab/Terjemahan/Metode sumber unit; tidak ada Khasiat atau bilangan baru.
5. Dua puluh enam crop pengguna tetap menjadi satu-satunya gambar dan
   ditengah pada Lapis 4 Syarah unit tujuannya, kecuali unit revisi
   berpenanda `[gambar wafak]`, yang cropnya tampil satu kali pada posisi
   penanda di Lapis 1.

**Pembaruan Lapis 1 seluruh kitab (perintah pengguna berikutnya,
2026-10-28):** teks Arab kiriman chat yang diarsipkan di
`arab_replacement_h62/` menggantikan Lapis 1 SAMPUL dan M01–M62, lalu teks
di `arab_replacement_h63_122/` menggantikan Lapis 1 M63–M122, pada master
terintegrasi maupun edisi bersih; kiriman revisi berikutnya di
`arab_replacement_h63_revised/` kemudian menggantikan hanya Lapis 1 M63,
`arab_replacement_h66_69_revised/` menggantikan hanya Lapis 1 M66–M69,
dan `arab_replacement_h82_83_97_98_revised/` menggantikan hanya Lapis 1
M82, M83, M97, dan M98. Kalimat pengantar/meta sebelum isi tidak masuk
dokumen; pada edisi bersih penanda proses ekstraksi berbahasa Indonesia
dalam kiriman halaman 63–122 juga tidak ditampilkan. Latin, Terjemahan,
Syarah/catatan, Metode/Khususiyah, tabel, dan pilihan berkas crop tidak
diganti oleh tahap-tahap ini; hanya posisi crop unit berpenanda mengikuti
aturan `[gambar wafak]` pada §4. Auditnya:
`AUDIT_ARAB_PENGGANTI_H62_2026-10-28.md`,
`AUDIT_ARAB_PENGGANTI_H63_122_2026-10-28.md`,
`AUDIT_ARAB_PENGGANTI_H63_REVISI_2026-10-28.md`,
`AUDIT_ARAB_PENGGANTI_H66_69_REVISI_2026-10-28.md`, dan
`AUDIT_ARAB_PENGGANTI_H82_83_97_98_REVISI_2026-10-28.md`.
