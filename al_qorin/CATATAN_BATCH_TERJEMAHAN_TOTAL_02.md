# CATATAN BATCH 02 — REVISI TOTAL TERJEMAHAN AL-QORIN

Tanggal kerja: 29 Oktober 2026. Batch ini melanjutkan revisi total
terjemahan bergaya Anwar setelah seluruh tahap penggantian Arab dan revisi
Fusha selesai; karena itu terjemahannya dibuat terhadap **Arab final yang
telah terkunci**, bukan terhadap Arab pada saat audit awal.

## Ruang lingkup

- Unit: **M06–M15**.
- Bidang yang berubah: **hanya Lapis 3 (Terjemahan)** melalui
  `overrides_terjemahan_total_batch02.json`.
- Penerapan Markdown memakai
  `scripts/al_qorin_apply_translation_total_batches.py --batch 2`.
- Builder terintegrasi menerapkan batch ini sesudah semua tahap Arab final.
  Edisi bersih memperoleh hasil yang sama melalui fungsi presentasi
  `clean_translation` yang memang dipakai builder bersih.
- Jumlah paragraf Lapis 3 dipertahankan per unit:
  M06=8, M07=7, M08=7, M09=6, M10=4, M11=3, M12=3, M13=3, M14=3, M15=3.
- Arab, Latin, Metode, Penentuan Jam, Catatan penyunting/Syarah,
  Khususiyah, tabel, `rajah_blocks`, dan seluruh crop tidak diubah.

## Pindaian yang diperiksa

PDF buku asli `al qorin war riyadhah.pdf` diambil kembali dari Drive dan
dihash: SHA-256
`ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`.
Render kerja 3× dibuat untuk halaman cetak berikut:

- PDF hlm. 4: halaman cetak 6–7;
- PDF hlm. 5: halaman cetak 8–9;
- PDF hlm. 6: halaman cetak 10–11;
- PDF hlm. 7: halaman cetak 12–13;
- PDF hlm. 8: halaman cetak 14–15.

Pindaian dipakai untuk memahami kesinambungan antarsisi halaman dan konteks.
Tidak ada koreksi Arab/Latin yang diterapkan dalam batch ini, karena tugas
batch adalah Lapis 3 dan Arab final telah dikunci oleh tahap sebelumnya.

## Penajaman terjemahan utama

- M06–M07 kini membedakan kerusakan daya pikir/khayalan, klaim cahaya dari
  setan, dan mujahadah yang menurut penulis bukan riyadhah, tanpa mengubah
  pengakuan sumber menjadi klaim penerjemah.
- Penahapan 40, 60, 90, satu pekan, dan dua pekan pada M07 dipertahankan
  tanpa penafsiran numerik tambahan. Kutipan kisah Musa diperlakukan sebagai
  ayat yang dikutip penulis.
- M08–M09 menandai istilah *sawā’ tanah liatnya*, *‘alayhim al-mubghiḍīn*, dan
  kelompok istilah pada gambaran jiwa sebagai susunan yang belum sepenuhnya
  mantap, bukan doktrin baru yang dihaluskan.
- M10 menerjemahkan seluruh lima belas baris Arab final dalam empat paragraf
  Lapis 3 yang sudah ada. Istilah *at-tamkhīkh* dipertahankan transliterasinya.
- M11–M13 mempertahankan seluruh jumlah makanan, rakaat, pengulangan Ayat
  Kursi, tahapan pekanan, 80 hari, bacaan yang ditentukan, dan urutan waktu.
  Pengalaman batin serta keakuratan firasat dinisbatkan kepada penulis.
- M14 mengikuti Arab final untuk *Yā Fattāḥ* dan *li-ṭamsi adz-dzikr*, walau
  catatan kerja lama membicarakan kandidat lain. Perbedaan itu tetap terbuka
  untuk audit Arab tersendiri dan tidak diubah secara diam-diam di Lapis 3.
- M15 menerjemahkan syarat pertama secara harfiah sebagai yang *ma‘lūm*
  (telah diketahui) dan menyatakan rujukannya tidak lengkap. Teks yang
  menyebut enam syarat tetapi memuat tujuh klausa dipertahankan apa adanya.

## Batas yang tetap terbuka

- Maksud tepat *bil-‘urf* pada M06, frasa *jasm māddat asy-syahwah* pada M11,
  *talqiyatan* pada M12, dan *fayahtasib* pada M13 belum ditetapkan.
- Perbedaan bacaan kerja lama dan Arab final pada M14 tidak merupakan izin
  untuk mengubah Arab dalam batch terjemahan ini.
- Batch berikutnya adalah **Batch 03 — M16–M32**.
