# CATATAN BATCH SEMANTIK TERAKHIR AL-QORIN — M68, M70, M71 (28 Oktober 2026)

Batch ini menutup kurasi semantik Lapis 4/5 untuk tiga unit yang sebelumnya
baru menerima penajaman selektif: M68, M70, dan M71. Pakem tetap terkunci:
123 unit total; SAMPUL tampil 3 lapis; M01 (Muqodimah) dan M122 (Khatimah)
tampil 4 lapis; unit lain 5 lapis; Arab kanan (`w:bidi=1`, `w:jc=start`),
Latin kiri (`w:bidi=0`), dan wafaq center dari crop presisi asli kiriman
pengguna sesudah Metode.

Dengan batch ini, seluruh 123 unit telah masuk pilot atau salah satu batch
semantik: pilot 12 unit, M16–M64, M06–M15/M72–M121, dan terakhir
M68/M70/M71.

## Mekanisme reproduksibel

- Keputusan per unit dicatat di `overrides_batch_m68_m70_m71.json`
  (setiap entri wajib memiliki `dasar` audit).
- `scripts/al_qorin_build_integrated.py` menerapkannya sebagai tahap final
  sesudah pilot, integrasi selektif, batch M16–M64, dan batch
  M06–M15/M72–M121. Baseline tahap ini karena itu adalah hasil
  **pasca-selektif dan pasca-batch sebelumnya**, bukan unit mekanis mentah.
- Tahap ini menolak perubahan apa pun di luar: (a) pemilihan Catatan
  penyunting dari catatan lama baseline, (b) penulisan ulang frasa
  Khususiyah, dan (c) penggantian hanya paragraf pertama Metode M71.
- Arab, Latin, Terjemahan, Penentuan Jam, `rajah_blocks`, heading, nomor
  halaman, label `[CATATAN PENERJEMAH]`, dan crop ditegaskan tidak berubah.
- Paragraf Metode M71 sesudah paragraf pertama — yakni deskripsi transparan
  rajah yang menyatakan bentuk tidak digambar ulang dan bagian tengah tidak
  diisi tebakan — dipertahankan byte-identik.

## Kaidah kurasi catatan

Ketiga unit memiliki pola catatan yang sama: catatan pertama dan keempat
substantif, sedangkan catatan kedua/ketiga adalah boilerplate generik
harakat dan rajah. Batch ini mempertahankan catatan substantif dan membuang
boilerplate generik karena deskripsi transparan rajah serta crop asli
(`68.jpg`, `70.jpg`, `71.jpg`) sudah hadir pada Metode/Lapis 4. Tidak ada
teks catatan baru: test membuktikan setiap catatan hasil batch adalah
paragraf catatan lama utuh dari baseline pasca-selektif.

## Penajaman per unit

- **M68:** Media diperinci menjadi rajah dua baris huruf/lambang sesudah
  kata «taktubu» (crop asli `68.jpg`, unsur berkeyakinan rendah dirujuk ke
  Metode/Catatan), bacaan ‘azm pengusiran dengan nama orang dan ibunya
  serta penanda tiga kali, dan QS al-Kahf 18:25 plus «Alif Lām Mīm» yang
  ditulis lalu digantungkan. Waktu dan Bukhur tetap tidak disebutkan.
- **M70:** Waktu menyatakan urutan langsung sesudah bersih dari haid, satu
  aṭbāq diminum tiap hari sebelum berbuka, dan ḥirz penutup digantung
  sesudah bersih dari haid. Media memuat tiga aṭbāq yang dijemur, tulisan
  spesifik telapak kanan («mā bānī» ☆ ف ق ج) dan kiri (☆ م خ م ت), bacaan
  QS Yā-Sīn 36:78 sampai akhir surah, serta rajah tiga baris pada crop
  `70.jpg`. Bukhur ditulis sebagai tiga istilah sesudah kata al-bukhūr —
  jāwī, kabīrah, kundur — dengan padanan harfiah Terjemahan kanonis untuk
  unsur tengah dinyatakan, bukan dipastikan sebagai nama bahan modern.
- **M71:** Waktu memisahkan faidah janin pada bulan ketiga (lalu tulisan
  dipindahkan kepada bayi sesudah lahir) dari faidah kehamilan pada waktu
  Zuhur di hari yang baik dan pemakaian sesudah bersih dari haid. Media
  menyebut ayat penjagaan, «ṭa sīn mīm» 109 kali, basmalah, dan rajah
  persegi panjang berbelah ketupat dengan delapan posisi ṭā’ pada crop
  `71.jpg`; bagian tengah dinyatakan kosong pada pindaian.

## Satu koreksi Metode: paragraf pertama M71

Paragraf pertama lama menyebut ayat faidah kehamilan “dibakar dengan lemak
kambing hitam”. Arab/Terjemahan unit memakai makna **dipanaskan**, dan kata
Arab untuk bahan dari kambing hitam sudah ditandai tidak pasti pada catatan
lama. Paragraf pengganti karena itu berbunyi pada pokoknya: ayat dipanaskan
dengan bahan dari kambing hitam yang **zat persisnya tidak dipastikan**
(Terjemahan kanonis menyebut lemak). Ini tidak menyelesaikan bacaan sumber
secara diam-diam; ketidakpastian justru dipertahankan.

Metode M68 dan M70 tidak diganti. Seluruh paragraf deskripsi transparan
rajah pada ketiga unit juga tidak diganti.

## Batas kejujuran batch ini

Batch ini **tidak** menerjemahkan ulang Arab/Latin/Terjemahan, tidak
mengarang hitungan jam, tidak menggambar ulang rajah, dan tidak
mengesahkan khasiat apa pun. Isi praktik tetap dinisbatkan kepada penulis
kitab sebagai dokumen terjemahan — bukan anjuran, bukan terapi, dan bukan
pengganti penanganan medis.
