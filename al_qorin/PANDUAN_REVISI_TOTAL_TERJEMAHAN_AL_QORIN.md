# PANDUAN REVISI TOTAL TERJEMAHAN AL-QORIN — ADAPTASI GAYA ANWAR

Panduan ini adalah amendemen kerja untuk fase revisi total terjemahan
Al-Qorin. Ia **tidak membatalkan** `STANDAR MUTLAK AL-QORIN 123` dan aturan
lapis kondisional 2026-10-28. Contoh gaya yang ditunjuk pengguna ialah
dokumen **Anwar Asy-syaikh Al-Basyir** (Google Doc
`1XG5U88PiSFfAEwygrpD5aifRPzhsO5YD`), dibandingkan juga dengan master lokal
`REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md`.

## Hal dari Anwar yang diadopsi

1. **Keselarasan baris/paragraf 1 : 1 : 1.** Paragraf Arab, Latin, dan
   Terjemahan dipertahankan berurutan dan sejajar; terjemahan tidak boleh
   melompati kalimat sumber, menggabungkan dua klausa penting menjadi
   ringkasan bebas, atau menghilangkan pengulangan sumber.
2. **Bahasa Indonesia lengkap dan mengalir.** Kalimat boleh disusun ulang
   sesuai tata bahasa Indonesia, subjek ganti yang jelas dari konteks boleh
   dinyatakan, dan penghubung Arab seperti *wa*, *fa*, *tsumma*, *idza*,
   *hatta* diterjemahkan secara wajar, bukan dipaksakan harfiah.
3. **Istilah teknis dipertahankan lalu diberi glos singkat bila perlu.**
   Contoh pola: *baṣīrah* (mata batin), *al-qisṭās* (neraca), *inābah*
   (kembali kepada Allah), *sulūk* (perjalanan ruhani). Glos tidak boleh
   menjadi ceramah panjang di Lapis 3.
4. **Judul/nama diri diperlakukan stabil.** Judul boleh memuat transliterasi
   judul cetak dan terjemahan maksudnya; nama orang/lembaga tidak diubah
   menjadi padanan bebas tanpa dasar.
5. **Perintah/seruan penulis tetap terasa sebagai suara penulis**, tetapi
   dokumen akhir tetap dokumenter: klaim khasiat, perjumpaan gaib, dan hasil
   amalan dinisbatkan kepada teks/penulis, bukan dinyatakan telah terbukti.

## Hal dari Anwar yang TIDAK diimpor mentah-mentah

1. Anwar memuat bab **Syarah Nahwu-Shorof** dan tafsiran hisab yang panjang.
   Al-Qorin tetap tunduk pada larangan mengarang ulang gaya dikte panjang,
   Qarinah qabliah/ba‘diah, dan hitungan Jam yang tidak ada pada halaman.
   Penjelasan nahwu yang benar-benar menentukan bacaan cukup diletakkan
   ringkas pada Catatan penyunting.
2. Khususiyah Anwar kadang imperatif sebagai tata cara praktik. Al-Qorin
   tetap dokumenter: tidak menganjurkan, tidak menjamin hasil, tidak
   menyajikan klaim medis sebagai terapi.
3. Transliterasi Anwar memakai campuran diakritik dan ejaan Indonesia.
   Al-Qorin tidak mengganti seluruh sistem Latin hanya demi gaya; Latin
   diubah bila terbukti salah membaca pindaian/huruf Arab kanonis, atau bila
   ada keputusan standardisasi latin tersendiri yang dicatat.
4. Gaya lancar tidak boleh menutup teks rusak. Frasa yang secara nahwu atau
   pindaian belum mantap diterjemahkan sedekat mungkin dan ditandai singkat
   dalam kurung siku; uraian bukti tetap di Catatan penyunting.

## Aturan perubahan Lapis 1–3 pada fase ini

- **Arab:** hanya diubah bila pindaian asli membuktikan huruf/bacaan berbeda;
  setiap perubahan dicatat pada file catatan batch. Ejaan cetak yang janggal
  tetapi nyata tidak dihaluskan diam-diam.
- **Latin:** hanya diubah mengikuti Arab kanonis/pindaian atau untuk
  memperbaiki alih aksara yang nyata keliru; tidak ada konversi gaya massal
  tanpa keputusan terpisah.
- **Terjemahan:** boleh ditulis ulang dari Arab kanonis dengan gaya di atas,
  dengan jumlah paragraf dipertahankan. Label `[CATATAN PENERJEMAH ...]`,
  deskriptor gambar, tabel, dan rujukan crop tidak boleh hilang.
- **Lapis 4/5:** tidak berubah otomatis karena terjemahan diperbaiki. Bila
  terjemahan baru membuktikan Metode/Khususiyah lama bertentangan, perubahan
  Lapis 4/5 harus dideklarasikan sebagai override terpisah berpenjaga.
- **Wafaq/rajah:** hanya 26 crop pengguna di `wafaq_qorin/`; tidak digambar
  ulang, tidak diambil dari FINAL KHATAM, tidak digeser dari halaman tujuan.

## Pola kalimat yang dipakai

- Kalimat pembuka panjang Arab boleh dipecah dengan titik koma mengikuti
  paragraf sumber, selama tidak ada klausa yang hilang.
- Kata ganti *-nya* yang rujukannya jelas boleh diganti nama rujukannya
  sesekali agar tidak ambigu; penambahan kata penjelas yang tidak ada pada
  sumber harus minimal dan, bila menentukan makna, diberi kurung biasa.
- Terjemahan istilah *riyāḍah* memakai “riyadhah (latihan ruhani)” pada
  kemunculan penting, lalu “riyadhah” saja; *‘azīmah*, *qasam*, *wafaq*,
  *khatam*, *Bukhur*, dan nama-nama teknis tidak dipadankan secara bebas.
- Angka, urutan hari/jam, nama surat/ayat, jumlah pengulangan, bahan, dan
  arah/tindakan pada sumber tidak boleh berubah karena parafrasa.

## Verifikasi tiap batch

1. Baca halaman pindaian asli yang bersangkutan, bukan hanya JSON kerja.
2. Override disimpan sebagai JSON terpisah; builder menolak unit di luar
   daftar, perubahan jumlah paragraf, hilangnya label, dan perubahan bidang
   terlindungi.
3. Bangun ulang Markdown terintegrasi, DOCX, dan dua preview identik.
4. Jalankan seluruh test repository.
5. Catat di `STATUS_AL_QORIN.md` dan file catatan batch: unit, halaman
   pindaian yang dilihat, bidang yang berubah, dan keraguan yang tetap terbuka.
