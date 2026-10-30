# Audit Edisi Bersih 2 Layer Al-Qorin — 2026-10-30

## Status dan keputusan ruang lingkup

Berkas ini mencatat **edisi baru terpisah**:

- `AL_QORIN_123_BERSIH_2_LAYER.md`
- `AL_QORIN_123_BERSIH_2_LAYER.docx`

Edisi kanonis `AL_QORIN_123_BERSIH.md/.docx`, turunan
`AL_QORIN_123_BERSIH_HALAMAN.md/.docx`, edisi penelitian, master lain,
manifest crop, dan 26 berkas crop **tidak ditimpa**.

Sumber konversi adalah turunan bersih Halaman yang sudah memuat
perbaikan penanda Latin pada commit `a95cfa6`:

| Berkas sumber | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_123_BERSIH_HALAMAN.md` | 673.303 byte | `8a59040ba8a1a3b6fc466b1f0490e5efcd6c1fad1ad0e15847ac0ca9437d2db7` |

Keputusan format yang diterapkan:

1. Buat edisi `_2_LAYER` baru; berkas lama tetap utuh.
2. Layer 2 ditiadakan pada unit yang naskahnya tidak memuat tatacara
   praktik.
3. Seluruh heading dan isi utama Syarah dihapus. Yang boleh tersisa
   hanya footnote satu baris untuk kata/frasa Arab yang pada Syarah
   lama secara eksplisit dinyatakan tidak jelas cetakan/bacaannya.
4. Instruksi khusus Halaman 49 mengganti override pendeknya dengan
   blok **Pola 49 TATACARA PRAKTIK LENGKAP** yang diberikan pengguna
   secara verbatim, termasuk konteks, pemetaan tujuh tanduk, tujuan
   tertulis, dan `CATATAN PENERJEMAH` di dalamnya. Pengecualian ini
   tidak mengubah Layer 1 Halaman 49.
5. Instruksi berikutnya khusus Halaman 58 mengganti Latin dan
   Terjemahan unit itu serta override Layer 2 pendeknya dengan pola
   lengkap yang diberikan pengguna, hanya dalam edisi `_2_LAYER`.
   Arab Halaman 58 tetap memakai badan terkunci dari sumber; crop
   wafaq 5×5 dan footnote ketidakjelasan lama tetap dipertahankan.
6. Pola nyambung Halaman 64+65 mengganti hanya Layer 2 kedua unit.
   Keduanya tetap unit terpisah dan rajahnya tidak digabung. Teks
   Layer 1 yang menyertai pola itu bersifat ringkasan dan menghilangkan
   pengulangan pada Arab terkunci, sehingga Layer 1 penuh kedua
   halaman tidak diganti. Urutan huruf pada Layer 2 Halaman 65
   dilengkapi dari Arab terkunci halaman itu. Catatan alur kerja
   `crop y2=96%` tidak dimasukkan ke dokumen dan tidak ada pembuatan
   crop ulang; crop presisi pengguna Halaman 64 dan 65 yang sudah
   terkunci tetap dipakai terpisah.
7. Instruksi khatam terakhir menerapkan gaya pola lengkap yang sama
   kepada seluruh edisi dua layer. Semua blok generik kini memakai
   `Media:` berbullet, heading `Langkah ke-N` terpisah, dan heading
   `Tujuan:` terpisah. Halaman 109, 116, dan 121 disusun manual dari
   Layer 1 terkunci dan crop masing-masing. Pola 49 dan 58 tetap
   persis; pada Pola 64/65 hanya label langkah dan letak `Tujuan:`
   diseragamkan tanpa mengganti isinya. Seluruh Layer 1 tetap utuh.
8. Aturan koreksi foto berikutnya menimpa edisi `_2_LAYER` secara
   bertahap, sekitar sepuluh halaman per batch dengan DOCX diperbarui
   pada setiap batch. Sumbernya adalah PDF foto asli
   `al qorin war riyadhah.pdf` (7.604.573 byte, SHA-256
   `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`).
   Arab disalin persis sebagaimana tercetak—tanpa harakat, hamzah,
   ejaan, atau perbaikan editorial tambahan; cetakan yang tidak jelas
   dibiarkan dan diberi footnote satu baris. Latin adalah
   transliterasi dari Arab foto itu dan Terjemahan adalah terjemahan
   literalnya. **Batch 01** mencakup SAMPUL dan Halaman 1–10, disimpan
   reproduksibel dalam `scripts/al_qorin_foto_layer1.json` dengan
   kunci halaman `0`–`10`. Halaman 11–122 belum diaudit foto pada
   tahap ini.

## Format keluaran

Setiap unit memakai struktur:

```text
## Halaman N — …
### LAYER 1 - KETERANGAN HALAMAN:
1. Arab:
2. Latin:
3. Terjemahan:
[crop bila crop lama berada pada Syarah]
*[Footnote: …]*                  (bila ada)
### LAYER 2 - TATACARA PRAKTIK:   (kondisional)
Media:
- …
Langkah ke-1:
…
Langkah ke-2:
…
Tujuan:
…
```

Pola label ini mengikuti gaya pola lengkap yang telah diterapkan
pada Halaman 49, 58, dan 64/65. Ia kini dipakai oleh 66 blok hasil
renderer generik serta blok mentah Halaman 49, 58, 64, 65, 109, 116,
dan 121. Layer 1 tetap memuat seluruh badan Arab, Latin, dan
Terjemahan halaman; contoh tindakan di dalamnya tidak memotong
keterangan halaman menjadi hanya kutipan praktik. Khusus Halaman 49,
bagian sesudah heading Layer 2 tetap blok verbatim berjudul
*TATACARA PRAKTIK LENGKAP MENURUT NASKAH HAL 49*, dengan subbagian
Media dan Tujuan di dalam format bernomornya sendiri. Halaman 58
tetap memakai blok pola lengkap pengguna. Pada Halaman 64/65 label
inline lama `Langkah N:` diubah menjadi subjudul `Langkah ke-N - …:`
dan `Tujuan:` ditempatkan pada baris sendiri; isi langkah dan tujuan
tidak berubah. Halaman 109, 116, dan 121 memakai blok manual dengan
subjudul langkah deskriptif serta kutipan Arab dari Layer 1
masing-masing.

Untuk unit yang tercantum dalam `FOTO_CORRECTIONS`, ketiga badan
Layer 1 dan footnote-nya tidak lagi diambil dari turunan bersih
Halaman, melainkan dari `scripts/al_qorin_foto_layer1.json`. Pada
Batch 01, pemetaan isi yang dipertahankan adalah ruang lingkup unit
lama: Halaman 1 dan 2 sama-sama berada pada halaman cetak ٢;
Halaman 3 memuat baris terakhir halaman cetak ٢ dan seluruh halaman
cetak ٣; sedangkan awal Halaman 4–10 teramati sejajar dengan awal
halaman cetak bernomor sama. Unit di luar JSON masih mengikuti
warisan konversi sebelumnya sampai batch foto berikutnya dikerjakan.

### Layer 1

- Untuk unit yang **belum** tercantum dalam `FOTO_CORRECTIONS`,
  badan **Arab** dan badan **Latin/Terjemahan** selain Halaman 58
  masih disalin dari sumber bersih Halaman tanpa penggantian kata,
  harakat, transliterasi, terjemahan, urutan paragraf, tabel, atau
  label penerjemah. Pada Halaman 58, Arab tetap sama dengan sumber,
  sedangkan Latin dan Terjemahan diganti persis dengan pola lengkap
  pengguna: Latin kini membaca `wahfazh-hu` dan `yumhaa`, menambah
  transliterasi deskriptor wafaq, dan Terjemahan memakai redaksi
  literal yang diberikan. Transkripsi angka tabel tidak lagi berada
  dalam Terjemahan Halaman 58 karena pola barunya menempatkan lima
  baris itu pada Layer 2.
- Untuk **Batch 01 (SAMPUL dan Halaman 1–10)**, ketiga badan Layer 1
  diganti persis dengan isi `scripts/al_qorin_foto_layer1.json`.
  Arabnya ditranskripsi dari foto cetak tanpa menambah harakat,
  hamzah, ejaan, atau perbaikan editorial; hanya tanda yang memang
  terlihat tercetak yang dipertahankan. Dalam 11 unit batch ini
  hanya terdapat 14 glyph tashkeel yang terhitung pada rentang
  `U+064B`–`U+065F`/`U+0670`, sedangkan badan Latinnya tidak memuat
  glyph Arab. Paragraf dikelompokkan menurut heading dan titik akhir
  visual pada halaman cetak, dengan jumlah paragraf Arab, Latin, dan
  Terjemahan yang dicerminkan satu sama lain pada setiap unit.
- Dengan demikian, pernyataan lama bahwa konversi ini tidak
  melakukan transkripsi ulang dari foto kini hanya berlaku bagi
  unit yang belum masuk batch foto. Unit Batch 01 adalah
  transkripsi foto baru; Halaman 11–122 belum dapat disebut sudah
  diaudit terhadap foto.
- Heading lama `4. Syarah` dan `5. Khususiyah dan Tatacara Praktik`
  tidak muncul lagi.
- 26 rujukan crop sama persis dan dalam urutan yang sama dengan
  sumber. Tujuh belas crop yang sudah berada pada Arab tetap pada
  posisinya. Sembilan crop yang dahulu berada dalam Syarah dipindah
  ke akhir Terjemahan/Layer 1 agar tidak hilang ketika heading Syarah
  dihapus: Halaman 49, 58, 64, 65, 86, 109, 116, 120, dan 121.

### Footnote ketidakjelasan

Untuk unit yang **belum** masuk `FOTO_CORRECTIONS`, builder hanya
membuat footnote bila segmen Syarah lama memuat kata/frasa Arab
dalam `«…»` bersama penanda eksplisit seperti “tidak dapat
dipastikan”, “belum pasti”, “tidak terbaca”, “tidak jelas”,
“bacaan/persoalan terbuka”, “tidak dikenali”, atau “tercetak rusak”.
Pada jalur warisan itu, maksimal tiga istilah pertama yang memenuhi
syarat ditulis dalam satu baris. Untuk unit foto, footnote hasil
ekstraksi Syarah **diganti seluruhnya** oleh field `footnote` dalam
JSON foto: string kosong berarti tidak ada footnote, sedangkan teks
non-kosong harus berformat satu baris yang sama:

```text
*[Footnote: kata/frasa «…» cetakan/bacaannya tidak jelas, dibiarkan.]*
```

Sesudah Batch 01 hasilnya **65 footnote**: delapan footnote foto
pada Halaman 1, 3, 4, 5, 6, 7, 8, dan 9, ditambah 57 footnote
warisan pada unit yang belum diaudit foto, yaitu Halaman 11–14,
16, 17, 19–23, 25, 27, 29, 31–33, 35, 38, 44, 45, 49, 50, 54, 56,
58, 67, 68, 70, 73–77, 79–83, 86, 88, 89, 96, 99, 101, 107, dan
110–122 dengan pengecualian Halaman 116 dan 120. Footnote warisan
yang sebelumnya melekat pada Halaman 10 tidak lagi dipakai karena
unit itu kini memakai data foto tanpa footnote. Catatan Syarah yang
bersifat penjelasan editorial lain, penilaian akidah, verifikasi,
atau usul koreksi tanpa penanda ketidakjelasan eksplisit pada segmen
yang sama tetap tidak diubah menjadi footnote pada jalur warisan;
seluruhnya dikeluarkan dari keluaran.

Contoh Halaman 49:

```text
*[Footnote: kata/frasa «التَّوَاقِيفِ», «السَّبَاسِبِ», «وَالشُّمُوخِ الْعَلِيقِ» cetakan/bacaannya tidak jelas, dibiarkan.]*
```

Footnote diwujudkan sebagai satu paragraf miring pada akhir Layer 1;
builder DOCX yang dipakai tidak membuat catatan kaki Word bawaan.

### Layer 2

Sumber bersih Halaman mempunyai 76 bagian praktik lama. Keluaran
mempertahankan **73 Layer 2** dengan total **268 langkah praktik**:
239 langkah pada 66 blok renderer generik, tiga langkah pada Pola
49, tiga pada Pola 58, empat pada Pola 64, lima pada Pola 65, tiga
pada blok manual Halaman 109, enam pada Halaman 116, dan lima pada
Halaman 121. Ada 72 baris mandiri `Media:`; Halaman 49 memakai
subbagian Media di dalam blok verbatim bernomornya. Ada pula 72
baris mandiri `Tujuan:`/`Tujuan tertulis:`; Halaman 49 memakai
`*7. Tujuan tertulis:*` dalam blok verbatimnya. Tiga bagian lama
tidak dijadikan Layer 2 karena prosanya sendiri menyatakan tidak
ada tatacara/praktik baru pada halaman itu:

- Halaman 103;
- Halaman 113;
- Halaman 118.

Pada Batch 01, Layer 2 tidak ditulis ulang. Dua halaman batch yang
mempunyai Layer 2, yaitu Halaman 4 dan 7, tetap sama persis dengan
keluaran sebelumnya setelah jangkar tindakannya ditemukan pada teks
foto terkoreksi: pembacaan al-Fatihah sebelum memulai pada Halaman
4, serta masa riyadhah/khalwah empat puluh hari, seminggu, dan dua
minggu pada Halaman 7. Dengan begitu, kesaksian foto pada batch ini
mencakup verifikasi bahwa tindakan tersebut memang tertulis pada
halaman, tetapi belum merupakan audit redaksional ulang atas setiap
rumusan ringkasan Layer 2.

Aturan konversinya:

- `Media:` berdiri pada baris sendiri, diikuti bullet. Pada 66 blok
  renderer generik, bullet dibentuk hanya dengan membagi field Media
  lama pada titik koma tingkat atas; tidak ada kata isi yang
  ditambah, diganti, atau dibuang selain titik akhir kalimat Media.
  Field Bukhur tetap dilipat ke Media sebagai `Bukhur: …`. Tujuh unit
  tanpa field Media diberi isi hanya dari medium/rujukan yang sudah
  dinyatakan pada bagiannya: Halaman 4, 7, 38, 61, 62, 107, dan 122.
- Setiap `Langkah ke-N:` berdiri sebagai heading paragraf sendiri
  dan badan langkah lama diletakkan utuh di bawahnya. Renderer ini
  menyusun prosa praktik lama berdasarkan urutan kalimat/klausa.
  Kalimat dokumenter seperti atribusi, “bukan anjuran”, “tidak ada
  jaminan”, “tidak diverifikasi”, dan penilaian sumber akidah tidak
  dibawa ke langkah.
- Field Waktu tidak dibuat sebagai heading keempat. Bila isinya belum
  tercakup secara substansial oleh prosa langkah, ia tetap dimasukkan
  ke badan `Langkah ke-1` dengan awalan “Waktu yang dinyatakan: …”.
- `Tujuan:` berdiri pada baris sendiri dan isi tujuan generik lama
  diletakkan utuh di bawahnya. Ia memakai pemetaan eksplisit per
  halaman di builder, berdasarkan tujuan/topik yang dinyatakan prosa
  praktik lama atau judul bab yang dikutip di dalamnya. Halaman 7,
  41, dan 105 ditulis “Tidak dinyatakan secara tersendiri pada
  halaman ini” karena bagian praktik lamanya tidak menyatakan tujuan
  tersendiri. Label generik tetap `Tujuan:`, bukan dipaksakan menjadi
  `Tujuan tertulis:`, karena sebagian isi tujuan berupa topik/tema
  atau pernyataan bahwa tujuan tersendiri tidak dinyatakan.
- Halaman 49 memakai blok **Pola 49 TATACARA PRAKTIK LENGKAP** dari
  pengguna secara verbatim; override pendek sebelumnya telah dihapus
  dari builder. Blok itu memuat judul dan teks Arab rujukan, konteks
  tawabi'/sabasib, media antara dua mata dan tangan kanan, tiga
  langkah, pemetaan Tanduk 1–7 termasuk catatan delapan huruf untuk
  tujuh tanduk, penutup, tujuan `عِلَاجِ الصَّرْعِ`, dan catatan
  penerjemah yang membingkainya sebagai dokumentasi serta merujuk
  kasus sakit/kerasukan kepada tenaga medis dan ulama.
- Halaman 58 memakai blok pola lengkap pengguna; override pendek
  sebelumnya juga telah dihapus. Blok itu memuat daftar media,
  penutup doa dengan qasam Nuh dan bahteranya, penulisan wafaq
  mukhammas 5×5, lima baris isi tabel dari kanan ke kiri, cara pakai
  `يُمْحَى وَيُشْفَى` sebagai klaim naskah, dan tujuan tertulis
  `لِجَمِيعِ الْأَمْرَاضِ`. Lima baris angka disalin persis dari pola
  yang diberikan dan crop asli tetap ditampilkan di Layer 1 untuk
  pemeriksaan visual; sumber bersih lama memuat urutan yang sama,
  dengan sel `١٠٤` pada Baris 4 ditandai tidak pasti.
- Halaman 64 dan 65 memakai pola nyambung pengguna sebagai dua blok
  Layer 2 terpisah; kedua override FINAL pendek sebelumnya dihapus.
  Halaman 64 adalah versi yang ditulis lalu dibawa (`yuktabu wa
  yuḥmalu`) dengan empat langkah, sedangkan Halaman 65 adalah versi
  yang ditulis dalam wadah porselen lalu dihapus/dilarutkan
  (`yumḥā`) dengan lima langkah. Layer 1 ringkas yang menyertai pola
  tidak dipakai untuk memotong badan penuh: pengulangan
  `وَعِنْدَ رَبِّي جَعَلَهُ دَكَّاءَ` pada Halaman 64 dan seluruh
  pengulangan rangkaian huruf pada Halaman 65 tetap utuh. Rangkaian
  huruf di `Langkah ke-2` Halaman 65 disalin lengkap dari Arab
  terkunci halaman itu. Pada khatam pola, hanya label kedua blok
  diseragamkan menjadi `Langkah ke-N - …:` dan `Tujuan:` dipisah ke
  baris sendiri; isi sesudah label terbukti sama dengan blok
  sebelumnya. Crop Khatam Sulaiman Halaman 64 dan 65 tetap berkas
  presisi pengguna yang berbeda dan tidak digabung atau dibuat ulang.
- Halaman 109 kini memakai blok manual tiga langkah: bacaan lanjutan
  kepada Awtad, perintah menghadap keperluan, dan penjelasan untuk
  mengenali satu dari delapan arah menurut hari/bulan pada da'irah
  bergambar dengan angka Hindi. Label atau angka yang terputar/tidak
  jelas pada crop lingkaran tidak ditranskripsi berdasarkan tebakan;
  langkahnya merujuk gambar Halaman 109 yang tetap tampil di Layer 1.
- Halaman 116 kini memakai blok manual enam langkah: menulis wafaq
  Basmalah al-Untsa pada kertas putih, menulis lingkaran huruf,
  menulis rangkaian `كَهْو لَهُو`, menulis seluruh ayat penjagaan
  dan bacaan-bacaan yang dinamai, mengasapi lalu membawa tulisan,
  kemudian mencatat pembuka bab qarinah kedua. Redaksi terkunci
  memuat hitungan 100 kali dan 41 kali dalam satu rangkaian; blok
  manual mengutip keduanya apa adanya dan secara eksplisit tidak
  memutuskan hubungan kedua hitungan itu. Isi yang ditulis pada bab
  kedua dinyatakan berlanjut ke Halaman 117, bukan disalin mundur ke
  Halaman 116.
- Halaman 121 kini memakai blok manual lima langkah: menulis wafaq
  Basmalah al-Untsa, menulis huruf alif–ẓā' di sekelilingnya, menulis
  rangkaian `كَهْو لَهُو`, menulis ayat penjagaan dan
  al-Mu'awwidzatain, lalu merujuk wafaq mutsallats 3×3 pada gambar.
  Frasa `مِائَةَ جِيمٍ` dipertahankan sebagai bacaan tidak jelas dan
  tidak dilancarkan menjadi `مِائَةَ مَرَّةٍ`; hitungan 41 kali dan
  kata `وَصِلْهُمْ` yang rujukannya tidak dirinci juga dipertahankan
  apa adanya. Isi sel wafaq tidak ditranskripsi ulang selain
  deskriptor 3×3/Basmalah yang sudah terkunci pada Layer 1.
- Halaman 98 dan 105 hanya mempunyai field Waktu/Media (Halaman 105
  prosanya hanya kalimat dokumenter), sehingga langkahnya dibentuk
  langsung dari kedua field tersebut tanpa menambah bahan atau hasil.
- Inventaris murni titik/bentuk rajah pada praktik lama Halaman 68,
  72, dan 74 tidak dijadikan langkah. Crop rajahnya tetap tampil di
  Layer 1; Media tetap menyebut rajah/tulisan yang relevan.
- Tidak ada Syarah akidah dan tidak ada penjelasan panjang baru di
  Layer 1 atau pada 66 Layer 2 hasil renderer generik. Blok mentah
  Pola 49, 58, 64, dan 65 berasal dari pola yang diberikan pengguna;
  blok mentah Halaman 109, 116, dan 121 disusun dari Layer 1
  terkunci/crop masing-masing untuk khatam gaya pola ini. Tujuan
  dicatat sebagai tujuan atau klaim yang dirumuskan naskah, bukan
  sebagai pengesahan hasil atau anjuran medis.

## Keluaran

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_123_BERSIH_2_LAYER.md` | 609.515 byte | `25ca936cccfce2aa1a18892160e972f0b0106de96ed2f6174a49076912090ddc` |
| `AL_QORIN_123_BERSIH_2_LAYER.docx` | 6.903.075 byte | `97b4ef753d3f33bc0af57581b9b72a7fce9cd5e4d1c71baab04dae37713da4f1` |

Builder Markdown menolak menulis selain nama berakhiran
`_2_LAYER.md` dan menolak jalur master kanonis/turunan yang dilindungi.
Builder juga memuat `scripts/al_qorin_foto_layer1.json` melalui
`_load_foto_corrections()`; halaman yang tercantum di dalamnya
menimpa badan Arab, Latin, Terjemahan, dan footnote hasil jalur
lama, lalu divalidasi agar sama persis dengan data JSON tersebut.
Halaman di luar JSON tetap divalidasi terhadap sumber bersih
Halaman yang terkunci.
Parser DOCX memakai cabang konteks untuk heading `LAYER …` dan label
polos `1. Arab:`, `2. Latin:`, serta `3. Terjemahan:`. Untuk blok
Pola 49, parser membuang penanda blockquote Markdown `>` sebelum teks
masuk ke Word. Parser juga memberi konteks Arab RTL/kanan kepada
31 paragraf Layer 2 yang seluruh hurufnya Arab—lima pada Pola 49,
tiga pada Pola 58, dua pada Pola 64, satu pada Pola 65, tiga pada
Halaman 109, delapan pada Halaman 116, satu pada langkah Halaman
120, dan delapan pada Halaman 121; perilaku heading lain
dipertahankan.

## QA

Pemeriksaan builder dan pemeriksaan independen membuktikan:

- 123 unit dengan heading yang sama persis: SAMPUL diikuti Halaman
  1–122;
- 123 heading Layer 1 dan masing-masing 123 label `1. Arab:`,
  `2. Latin:`, dan `3. Terjemahan:`; tidak ada heading `####` atau
  label Media/Langkah/Tujuan berbold yang tersisa;
- untuk SAMPUL dan Halaman 1–10, badan Arab dan Latin sama persis
  dengan `scripts/al_qorin_foto_layer1.json`, sedangkan badan
  Terjemahan diawali persis oleh teks JSON sebelum footnote foto
  bila ada; jumlah paragraf ketiga badan pada setiap unit batch
  sama dan badan Latinnya tidak memuat glyph Arab. Untuk Halaman
  11–122, badan Arab tetap sama byte-for-byte dengan sumber setelah
  pemangkasan baris kosong tepi, dan badan Latin/Terjemahan selain
  Halaman 58 juga sama atau menjadi awalan persis sebelum
  crop/footnote tambahan; pada Halaman 58 keduanya sama persis
  dengan konstanta `POLA_58_LATIN` dan `POLA_58_TERJEMAHAN`;
- 73 heading Layer 2 dan 268 langkah. Pada 66 blok renderer
  generik, Media yang direkonstruksi dari bullet dengan `; ` dan
  titik akhir sama persis dengan Media lama; badan setiap langkah
  dan isi Tujuan juga sama persis serta tetap dalam urutan semula.
  Blok Halaman 49 dan 58 tetap sama persis dengan konstanta pola
  lengkap masing-masing. Blok Halaman 64 dan 65 sama persis dengan
  konstanta pola nyambungnya dan—setelah transformasi label
  `Langkah N:` menjadi `Langkah ke-N - …:` serta pemisahan
  `Tujuan:`—sama persis dengan keluaran sebelumnya. Blok manual
  Halaman 109, 116, dan 121 sama persis dengan konstanta buildernya
  dan penomoran `Langkah ke-N` di semua blok berurutan tanpa lompati
  nomor;
- 65 footnote dan semuanya satu baris: delapan footnote foto pada
  Halaman 1, 3–9 serta 57 footnote warisan pada unit yang belum
  diaudit foto; SAMPUL, Halaman 2, dan Halaman 10 tidak mempunyai
  footnote foto;
- daftar 26 rujukan crop sama persis dengan sumber; 9 crop Syarah
  berpindah ke Layer 1 dan tidak ada crop yang hilang atau diganti.
  Khusus Halaman 64/65, rujukan serta hash kedua crop terbukti tetap
  terpisah dan tidak berubah;
- parser DOCX memberi konteks Arab pada paragraf pertama di bawah
  semua label `1. Arab:`, konteks Latin pada semua `2. Latin:`, dan
  konteks Terjemahan pada semua `3. Terjemahan:`;
- DOCX memuat 1 Title, 123 Heading 1, 196 Heading 2
  (123 Layer 1 + 73 Layer 2), 369 Heading 3 untuk label Layer 1,
  2.310 paragraf Normal, 26 gambar inline/media, dan 4 bagian font
  tertanam; tidak ada label lama `Langkah N:` dan tidak ada paragraf
  DOCX yang masih diawali penanda blockquote `>`. Bullet Media
  dipertahankan renderer Word sebagai awalan `- `, sama seperti pola
  mentah sebelumnya;
- dibandingkan dengan keluaran khatam pola pada commit `1aebee2`,
  tepat 11 unit berubah pada Markdown Batch 01 ini: SAMPUL dan
  Halaman 1–10. Sebanyak 112 unit Halaman 11–122 identik. Seluruh
  segmen Layer 2, termasuk Halaman 4 dan 7, juga identik; urutan
  dan rujukan 26 crop tidak berubah;
- perbandingan kata antara Arab foto Batch 01 dan Arab lama yang
  tashkeel-nya dilucuti menghasilkan 259 operasi selisih dan 396
  posisi kata berubah. Jumlah operasi per unit adalah SAMPUL 3,
  Halaman 1: 16, Halaman 2: 2, Halaman 3: 28, Halaman 4: 30,
  Halaman 5: 27, Halaman 6: 38, Halaman 7: 33, Halaman 8: 32,
  Halaman 9: 35, dan Halaman 10: 15. Sebagian besar berupa ejaan
  cetak seperti hamzah/alif maqsurah/ta marbutah, tetapi di dalamnya
  juga terdapat pembacaan lama yang substantif berbeda dari foto;
- hash media DOCX sama dengan himpunan hash 26 berkas crop sumber;
- XML DOCX memuat penanda arah `w:bidi` dan `w:rtl`; parser konteks
  menghasilkan 538 paragraf Arab, 285 paragraf Latin, 356 paragraf
  Terjemahan, dan 983 paragraf Layer 2 non-Arab-murni. Ke-31 paragraf
  Layer 2 berbahasa Arab murni—Pola 49 (5), Pola 58 (3), Pola 64 (2),
  Pola 65 (1), Halaman 109 (3), 116 (8), 120 (1), dan 121 (8)—
  mempunyai arah RTL/kanan serta `w:rtl` pada run teksnya. Penurunan
  jumlah paragraf Layer 1 dari hitungan sebelum Batch 01 berasal
  dari pengelompokan ulang paragraf SAMPUL dan Halaman 1–10 menurut
  halaman cetak, bukan dari perubahan Layer 2;
- DOCX memuat cuplikan terkoreksi seperti pembuka Halaman 1 tanpa
  harakat editorial lama dan nama pengarang SAMPUL
  `محمد سامى محمد احمد`; bentuk lama berharakat penuh untuk pembuka
  tersebut tidak lagi ditemukan. Berkas PDF foto yang dipakai juga
  terverifikasi ber-SHA-256
  `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`;
- pembangunan Markdown diulang dan menghasilkan SHA-256 yang sama;
- discovery test repo: 40 test terdaftar, 33 lulus, dan 7 dilewati
  karena work JSON ter-ignore tidak hadir;
- hash berkas lama yang diperiksa kembali tetap:
  `AL_QORIN_123_BERSIH.md` `4fa012922f050cb0275a4cd370a2dcc3512021e95d399a36973a790610f9fb20`,
  `AL_QORIN_123_BERSIH.docx` `0b41b67591e163a21af7b8e54d7d4c3351f44bde809557092df4104587d13f60`,
  dan DOCX bersih Halaman `dd94686623649ad3d8a62e64fff4d8af9a9d9fb7f2107d0cf0fbcc98d76d59bd`.

## Batasan yang dipertahankan

Sesudah Batch 01, status edisi ini terbagi dua. SAMPUL dan Halaman
1–10 sudah diganti dengan transkripsi foto beserta Latin dan
Terjemahan turunannya. Selain penggantian Latin/Terjemahan Halaman
58 yang eksplisit dari pengguna, Halaman 11–122 masih merupakan
hasil konversi format turunan dan belum penyuntingan ulang isi
Layer 1 berdasarkan foto. Khatam gaya pola pada 66 blok renderer
generik juga merupakan normalisasi penyajian: Media, badan langkah,
urutan, dan Tujuan lama dipertahankan kata demi kata, bukan diaudit
ulang satu per satu terhadap Layer 1. Hanya tiga halaman kunci 109,
116, dan 121 disusun ulang manual dari Layer 1 terkunci/crop
sebelumnya, dengan ketidakjelasan sumber dipertahankan; ketiganya
belum masuk batch foto. Karena itu batas-batas berikut tetap
terlihat apa adanya:

1. Latin Halaman 63 paragraf 2 masih berhenti sesudah tujuh nama
   bertanda `?`, sedangkan Arab berlanjut ke klausa sesudahnya.
   Perbaikan penanda eksplisit sebelumnya tidak memperluas ruang
   lingkup ke penghentian tanpa penanda itu.
2. Sisa bacaan Halaman 97 yang pada turunan Halaman dilengkapi dari
   Arab final tetap juga muncul dalam transliterasi warisan di awal
   Latin Halaman 98 karena segmentasi lintas halaman sumber tidak
   direstrukturisasi.
3. Pada Halaman 109, nama/angka dalam crop da'irah yang terputar
   atau tidak jelas tidak ditranskripsi satu per satu; pola manual
   hanya mencatat metode delapan arah dan angka Hindi yang
   dinyatakan oleh prosa terkunci.
4. Pada Halaman 116, hubungan hitungan 100 kali dan 41 kali tetap
   tidak diputuskan. Pada Halaman 121, `مِائَةَ جِيمٍ` dan rujukan
   `وَصِلْهُمْ` tetap tidak dilancarkan.
5. Audit foto belum mencakup Halaman 11–122. Pada batch berikutnya,
   batas unit tidak boleh diasumsikan selalu sama dengan batas
   halaman cetak: Batch 01 sendiri menunjukkan bahwa Halaman 1 dan
   2 berbagi halaman cetak ٢, sedangkan Halaman 3 melintasi halaman
   cetak ٢–٣. Batch ini mempertahankan ruang lingkup dan heading
   unit yang sudah ada, bukan melakukan segmentasi ulang.
6. Layer 2 Halaman 4 dan 7 dipertahankan persis setelah jangkar
   tindakannya ditemukan pada teks foto, tetapi rumusan ringkasnya
   belum diaudit ulang baris demi baris. Khusus Halaman 7, frasa
   warisan “empat puluh hari dan kelipatannya” masih merupakan
   ringkasan umum atas rangkaian masa yang tertulis pada halaman;
   penyelarasan redaksional penuh Layer 2 terhadap foto harus
   dinyatakan sebagai ruang lingkup tersendiri bila hendak
   dikerjakan.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_build_bersih_2layer.py
.venv/bin/python scripts/build_docx_al_qorin.py --clean \
  --input al_qorin/AL_QORIN_123_BERSIH_2_LAYER.md \
  --output al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx
```
