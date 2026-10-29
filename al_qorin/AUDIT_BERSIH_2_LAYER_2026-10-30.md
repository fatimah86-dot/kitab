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

### Layer 1

- Badan **Arab** seluruh unit dan badan **Latin/Terjemahan** selain
  Halaman 58 disalin dari sumber bersih Halaman tanpa penggantian
  kata, harakat, transliterasi, terjemahan, urutan paragraf, tabel,
  atau label penerjemah. Pada Halaman 58, Arab tetap sama dengan
  sumber, sedangkan Latin dan Terjemahan diganti persis dengan pola
  lengkap pengguna: Latin kini membaca `wahfazh-hu` dan `yumhaa`,
  menambah transliterasi deskriptor wafaq, dan Terjemahan memakai
  redaksi literal yang diberikan. Transkripsi angka tabel tidak lagi
  berada dalam Terjemahan Halaman 58 karena pola barunya menempatkan
  lima baris itu pada Layer 2.
- Dengan demikian “Arab asli” pada konversi ini berarti Arab final
  yang sudah terkunci dalam master sumber, disalin persis. Konversi
  format ini **tidak** melakukan transkripsi ulang dari foto dan tidak
  menambah/menghapus harakat.
- Heading lama `4. Syarah` dan `5. Khususiyah dan Tatacara Praktik`
  tidak muncul lagi.
- 26 rujukan crop sama persis dan dalam urutan yang sama dengan
  sumber. Tujuh belas crop yang sudah berada pada Arab tetap pada
  posisinya. Sembilan crop yang dahulu berada dalam Syarah dipindah
  ke akhir Terjemahan/Layer 1 agar tidak hilang ketika heading Syarah
  dihapus: Halaman 49, 58, 64, 65, 86, 109, 116, 120, dan 121.

### Footnote ketidakjelasan

Builder hanya membuat footnote bila segmen Syarah lama memuat
kata/frasa Arab dalam `«…»` bersama penanda eksplisit seperti “tidak
dapat dipastikan”, “belum pasti”, “tidak terbaca”, “tidak jelas”,
“bacaan/persoalan terbuka”, “tidak dikenali”, atau “tercetak rusak”.
Maksimal tiga istilah pertama yang memenuhi syarat ditulis dalam
satu baris:

```text
*[Footnote: kata/frasa «…» cetakan/bacaannya tidak jelas, dibiarkan.]*
```

Hasilnya **58 footnote** pada Halaman 10–14, 16, 17, 19–23, 25, 27,
29, 31–33, 35, 38, 44, 45, 49, 50, 54, 56, 58, 67, 68, 70, 73–77,
79–83, 86, 88, 89, 96, 99, 101, 107, dan 110–122 dengan pengecualian
Halaman 116 dan 120. Catatan Syarah yang bersifat penjelasan editorial
lain, penilaian akidah, verifikasi, atau usul koreksi tanpa penanda
ketidakjelasan eksplisit pada segmen yang sama tidak diubah menjadi
footnote; seluruhnya dikeluarkan dari keluaran.

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
| `AL_QORIN_123_BERSIH_2_LAYER.md` | 618.341 byte | `195fc7eb2af4d6de6dac3d8a5b3dd2caa36a64cf4e72c04331fdcde393f46ea4` |
| `AL_QORIN_123_BERSIH_2_LAYER.docx` | 6.904.714 byte | `163397d9d05317fea5f165677de33626f397689dda4ce5fb35a58c5010cbd17c` |

Builder Markdown menolak menulis selain nama berakhiran
`_2_LAYER.md` dan menolak jalur master kanonis/turunan yang dilindungi.
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
- badan Arab setiap unit sama byte-for-byte dengan sumber setelah
  pemangkasan baris kosong tepi. Badan Latin/Terjemahan selain
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
- 58 footnote dan semuanya satu baris;
- daftar 26 rujukan crop sama persis dengan sumber; 9 crop Syarah
  berpindah ke Layer 1 dan tidak ada crop yang hilang atau diganti.
  Khusus Halaman 64/65, rujukan serta hash kedua crop terbukti tetap
  terpisah dan tidak berubah;
- parser DOCX memberi konteks Arab pada paragraf pertama di bawah
  semua label `1. Arab:`, konteks Latin pada semua `2. Latin:`, dan
  konteks Terjemahan pada semua `3. Terjemahan:`;
- DOCX memuat 1 Title, 123 Heading 1, 196 Heading 2
  (123 Layer 1 + 73 Layer 2), 369 Heading 3 untuk label Layer 1,
  2.407 paragraf Normal, 26 gambar inline/media, dan 4 bagian font
  tertanam; tidak ada label lama `Langkah N:` dan tidak ada paragraf
  DOCX yang masih diawali penanda blockquote `>`. Bullet Media
  dipertahankan renderer Word sebagai awalan `- `, sama seperti pola
  mentah sebelumnya;
- dibandingkan dengan keluaran Pola 64+65 pada commit `2b7cd92`,
  tepat 71 unit berubah pada Markdown: 69 halaman yang sebelumnya
  memakai konversi generik (termasuk penyusunan manual baru
  Halaman 109, 116, dan 121) ditambah normalisasi label Halaman 64
  dan 65. Sebanyak 52 unit identik, termasuk SAMPUL, semua unit
  tanpa Layer 2, Pola 49, dan Pola 58. Segmen dari heading unit
  sampai sebelum Layer 2 identik pada seluruh 123 unit, sehingga
  tidak ada badan Layer 1, crop, atau footnote yang berubah pada
  khatam pola ini;
- hash media DOCX sama dengan himpunan hash 26 berkas crop sumber;
- XML DOCX memuat penanda arah `w:bidi` dan `w:rtl`; parser konteks
  menghasilkan 580 paragraf Arab, 316 paragraf Latin, 380 paragraf
  Terjemahan, dan 983 paragraf Layer 2 non-Arab-murni. Ke-31 paragraf
  Layer 2 berbahasa Arab murni—Pola 49 (5), Pola 58 (3), Pola 64 (2),
  Pola 65 (1), Halaman 109 (3), 116 (8), 120 (1), dan 121 (8)—
  mempunyai arah RTL/kanan serta `w:rtl` pada run teksnya. Kenaikan
  20 paragraf Arab berasal dari kutipan Arab manual yang kini berdiri
  sebagai paragraf tersendiri, bukan dari Layer 1;
- pembangunan Markdown diulang dan menghasilkan SHA-256 yang sama;
- discovery test repo: 40 test terdaftar, 33 lulus, dan 7 dilewati
  karena work JSON ter-ignore tidak hadir;
- hash berkas lama yang diperiksa kembali tetap:
  `AL_QORIN_123_BERSIH.md` `4fa012922f050cb0275a4cd370a2dcc3512021e95d399a36973a790610f9fb20`,
  `AL_QORIN_123_BERSIH.docx` `0b41b67591e163a21af7b8e54d7d4c3351f44bde809557092df4104587d13f60`,
  dan DOCX bersih Halaman `dd94686623649ad3d8a62e64fff4d8af9a9d9fb7f2107d0cf0fbcc98d76d59bd`.

## Batasan yang dipertahankan

Selain penggantian Latin/Terjemahan Halaman 58 yang eksplisit dari
pengguna, konversi ini adalah perubahan format turunan, bukan
penyuntingan ulang isi Layer 1. Khatam gaya pola pada 66 blok
renderer generik juga merupakan normalisasi penyajian: Media,
badan langkah, urutan, dan Tujuan lama dipertahankan kata demi
kata, bukan diaudit ulang satu per satu terhadap Layer 1. Hanya
tiga halaman kunci 109, 116, dan 121 disusun ulang manual, dengan
ketidakjelasan sumber dipertahankan. Karena itu batas-batas
berikut tetap terlihat apa adanya:

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

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_build_bersih_2layer.py
.venv/bin/python scripts/build_docx_al_qorin.py --clean \
  --input al_qorin/AL_QORIN_123_BERSIH_2_LAYER.md \
  --output al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx
```
