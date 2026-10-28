# CATATAN BATCH SEMANTIK AL-QORIN — M06–M15 dan M72–M121 (28 Oktober 2026)

Batch ini menerapkan kurasi setingkat pilot pada 60 unit M06–M15 dan
M72–M121 di dalam master terintegrasi 123 unit, dengan pakem yang sudah
terkunci: 123 unit total; SAMPUL tampil 3 lapis; M01 (Muqodimah) dan M122
(Khatimah) tampil 4 lapis; unit lain 5 lapis; Arab kanan (`w:bidi=1`,
`w:jc=start`), Latin kiri (`w:bidi=0`), dan wafaq center dari crop presisi
asli kiriman pengguna sesudah Metode.

Crop yang berada di dalam rentang batch ini tetap dirujuk ke berkas asli
pengguna: `72.jpg`, `73.jpg`, `74.jpg`, `76.jpg`, `77.jpg`, `78.jpg`,
`82.jpg`, `83.jpg`, `84.jpg`, `85.jpg`, `86.jpg`, `98.jpg`, `109.jpg`,
`116.jpg`, `120.jpg`, dan `121.jpg`. Tidak ada crop pada M06–M15.

## Mekanisme reproduksibel

- Keputusan per unit dicatat di `overrides_batch_m06_m15_m72_m121.json`
  (setiap entri wajib memiliki `dasar` audit).
- `scripts/al_qorin_build_integrated.py` menerapkannya sebagai tahap ketiga
  sesudah pilot, integrasi selektif unggahan, dan batch M16–M64. Baseline
  tahap ini karena itu adalah hasil **pasca-selektif**, bukan unit mekanis
  mentah.
- Tahap ini menolak perubahan apa pun di luar: (a) pemilihan Catatan
  penyunting dari catatan lama unit yang sama, (b) penulisan ulang frasa
  Khususiyah, dan (c) penggantian Metode hanya pada M12, M79, M82, dan M83.
- Arab, Latin, Terjemahan, Penentuan Jam, tabel/blok rajah, heading, nomor
  halaman, label `[CATATAN PENERJEMAH]`, dan crop ditegaskan tidak berubah.
- Unit yang tumpang tindih dengan integrasi selektif (M104, M105, M106,
  M107, M109, M116, M120, M121) tidak ditimpa dari baseline lama. Catatan
  beda pindaian yang ditambahkan secara selektif pada M104 dan M107 wajib
  dipertahankan oleh builder dan test.

## Kaidah kurasi catatan

Catatan lama dipilih, bukan ditulis ulang. Catatan bacaan substantif
(ketidakpastian huruf/kata, identifikasi ayat/hadis, status atribusi,
observasi pindaian, dan peringatan editorial) dipertahankan. Boilerplate
generik harakat/rajah yang berulang, fragmen Latin yang terselip sebagai
catatan, catatan transisi/alur-kerja kosong, dan fragmen dikte saraf dibuang.
Tidak ada teks catatan baru: test membuktikan setiap paragraf catatan hasil
batch tersusun hanya dari paragraf catatan lama utuh pada baseline
pasca-selektif.

Pada M06–M09 sebagian besar catatan memang filologis substantif; pengecualian
jelas adalah fragmen Latin M07 dan fragmen hubungan yang belum jelas pada
M08. Pada M97–M102 dan M121 peringatan editorial tentang atribusi/tidak
dianjurkan dipertahankan.

## Koreksi Metode (satu stub, tiga kontradiksi material)

- **M12** — stub kata kunci diganti ringkasan jadwal yang benar-benar ada
  pada Terjemahan: zikir sebelum fajar, Subuh, zikir hingga terbit, isyraq,
  zawal, Zuhur/Asar/Magrib, perlakuan, dan tahapan pekan hingga 80 hari,
  dengan bingkai dokumenter/non-medis.
- **M79** — ringkasan lama menyebut kertas hijau dan kemenyan generik.
  Arab/Terjemahan unit menyebut pelepah hijau bertuliskan al-‘Ādiyāt dan
  cendana pada mangkuk pembakar baru sesudah Isya.
- **M82** — frasa lama “penulisan di kuburan” menyesatkan. Terjemahan unit
  menyebut tulisan dikuburkan di pintu pihak sasaran; unit juga memuat
  al-Fātiḥah 31 kali dan pembuka bab talbīs al-juttsah.
- **M83** — Arab unit memakai perintah mengasapi kertas faidah rasa takut
  dengan lubbān dzakar, jāwī, mastika, dan kayu ‘ūd. Tidak ada instruksi
  menggantung pada unit ini.

Ringkasan Metode draf pada 56 unit batch lainnya dipertahankan apa adanya.

## Penajaman Khususiyah (contoh penentu)

- **M07:** empat puluh dan kelipatannya dipertahankan, tetapi caveat bahwa
  kata “hari” tidak ada pada frasa kunci tidak dihapus.
- **M11–M15:** jadwal dan sarana riyadhah dipisahkan pada tingkat frasa:
  makan ±24 ūqiyah/roti hangat dan Ayat al-Kursi (M11), jadwal harian 80
  hari (M12), berbuka sesudah Isya dan pengurangan setengah dirham (M13),
  respons wudu/mandi dan nama zikir menurut tabir (M14), serta syarat salik
  dengan ketidaksesuaian enam/tujuh frasa dicatat (M15).
- **M72–M74:** tulisan/rajah kehamilan dirujuk ke crop asli masing-masing;
  waktu bersih dari haid dan mangkuk porselen/susu kambing hitam pada M73
  dipertahankan sebagai bunyi Metode kanonis unit itu.
- **M75:** redaksi waktu “pada waktu matahari terbenam, sebelum terbenam”
  dipertahankan; bakhur laba-laba dan kabarbarah dicatat dengan istilah
  bahan tidak dipastikan.
- **M79–M86:** pelepah/cendana M79, Kamis–kekuatan bulan dan bakhur M81,
  bahan serta penguburan di pintu pada M82, pengasapan M83, saat baik dan
  bakhur wangi M84, dan hijab persalinan M86 ditulis sebagai frasa sumber,
  bukan parafrase bebas.
- **M87–M96/M110/M114:** unit daftar nama atau pembahasan tanpa instruksi
  praktik tidak dipaksa memiliki waktu/media/bakhur; klaim pagi pada M114
  tidak diubah menjadi waktu praktik.
- **M97–M99:** syarat hari tanpa angin/hujan/awan, khatam di telapak/tangan
  kiri, cendana merah, puasa tujuh hari mulai Ahad (M98), dan rangkaian dua
  hari (M99) dinyatakan terpisah dari peringatan editorial bab.
- **M104–M121 tumpang tindih selektif:** Khususiyah selektif yang sudah
  terverifikasi tidak ditimpa; batch ini hanya mengkurasi catatan pada unit
  tumpang tindih tersebut dan mempertahankan caveat/catatan beda pindaian.

## Batas kejujuran batch ini

Batch ini **tidak** menerjemahkan ulang Arab/Latin/Terjemahan, tidak
mengarang hitungan jam (semua Penentuan Jam tetap sebagaimana sebelumnya),
tidak menggambar ulang rajah, dan tidak mengesahkan khasiat apa pun. Isi
praktik tetap dinisbatkan kepada penulis kitab sebagai dokumen terjemahan —
bukan anjuran, bukan terapi, dan bukan pengganti penanganan medis. Sisa
batch semantik Lapis 4/5 terutama M68, M70, dan M71; lihat
`STATUS_AL_QORIN.md`.
