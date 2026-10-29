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
   Teks pola lengkap baru untuk Halaman 109, 116, dan 121 belum
   diberikan, sehingga ketiga halaman itu tetap memakai Layer 2
   generik sebelumnya.

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
Media: …
Langkah 1: …
Langkah 2: …
Tujuan: …
```

Pola label generik ini mengikuti contoh **HAL 49 FINAL 2 LAYER** dari
pengguna dan berlaku pada 71 unit Layer 2 selain Halaman 49 dan 58.
Layer 1 tetap memuat seluruh badan Arab, Latin, dan Terjemahan
halaman; contoh tindakan di dalamnya tidak memotong keterangan
halaman menjadi hanya kutipan praktik. Khusus Halaman 49, bagian
sesudah heading Layer 2 adalah blok verbatim berjudul *TATACARA
PRAKTIK LENGKAP MENURUT NASKAH HAL 49*. Khusus Halaman 58, Layer 2
memakai blok pola lengkap pengguna yang dimulai dengan daftar
`Media:` dan memakai label `Langkah ke-1` sampai `Langkah ke-3`.

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
mempertahankan **73 Layer 2** dengan total **265 langkah praktik**:
259 label generik `Langkah N:` pada 71 unit, tiga label
`Langkah ke-1` sampai `Langkah ke-3` dalam blok Pola 49, dan tiga
label yang sama dalam blok Pola 58. Ada 72 baris yang dimulai
`Media:` (71 blok generik ditambah daftar media Pola 58) dan 71
label generik `Tujuan:`; Halaman 49 dan 58 memakai subbagian tujuan
tertulis dalam blok lengkapnya sendiri. Tiga bagian lama tidak
dijadikan Layer 2 karena prosanya sendiri menyatakan tidak ada
tatacara/praktik baru pada halaman itu:

- Halaman 103;
- Halaman 113;
- Halaman 118.

Aturan konversinya:

- `Media:` memakai field Media lama. Field Bukhur dilipat ke Media
  sebagai `Bukhur: …`. Tujuh unit tanpa field Media diberi isi hanya
  dari medium/rujukan yang sudah dinyatakan pada bagiannya: Halaman
  4, 7, 38, 61, 62, 107, dan 122.
- `Langkah N:` menyusun prosa praktik lama berdasarkan urutan
  kalimat/klausa. Kalimat dokumenter seperti atribusi, “bukan
  anjuran”, “tidak ada jaminan”, “tidak diverifikasi”, dan penilaian
  sumber akidah tidak dibawa ke langkah.
- Field Waktu tidak dibuat sebagai heading keempat. Bila isinya belum
  tercakup secara substansial oleh prosa langkah, ia dimasukkan pada
  `Langkah 1:` dengan awalan “Waktu yang dinyatakan: …”.
- `Tujuan:` memakai pemetaan eksplisit per halaman di builder,
  berdasarkan tujuan/topik yang dinyatakan prosa praktik lama atau
  judul bab yang dikutip di dalamnya. Halaman 7, 41, dan 105 ditulis
  “Tidak dinyatakan secara tersendiri pada halaman ini” karena bagian
  praktik lamanya tidak menyatakan tujuan tersendiri.
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
  dengan sel `١٠٤` pada Baris 4 ditandai tidak pasti. Halaman 64
  dan 65 tetap memakai override pola FINAL pendek.
- Halaman 98 dan 105 hanya mempunyai field Waktu/Media (Halaman 105
  prosanya hanya kalimat dokumenter), sehingga langkahnya dibentuk
  langsung dari kedua field tersebut tanpa menambah bahan atau hasil.
- Inventaris murni titik/bentuk rajah pada praktik lama Halaman 68,
  72, dan 74 tidak dijadikan langkah. Crop rajahnya tetap tampil di
  Layer 1; Media tetap menyebut rajah/tulisan yang relevan.
- Tidak ada Syarah akidah dan tidak ada penjelasan panjang baru di
  Layer 1 atau pada 71 Layer 2 generik. Pengecualian hanya pada
  konteks/catatan dalam blok Pola 49 dan rincian tabel dalam blok
  Pola 58 yang diberikan pengguna. Tujuan dicatat sebagai tujuan
  atau klaim yang dirumuskan naskah, bukan sebagai pengesahan hasil
  atau anjuran medis.

## Keluaran

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_123_BERSIH_2_LAYER.md` | 610.261 byte | `cdc2a2921dba356340ff9723ac23770d8cf8e8e5604ec3ea225fd5bde83dd15c` |
| `AL_QORIN_123_BERSIH_2_LAYER.docx` | 6.896.403 byte | `f881db0a1334a7b530650f8ab3d4b70df740f4033216a948518244a1b3697bca` |

Builder Markdown menolak menulis selain nama berakhiran
`_2_LAYER.md` dan menolak jalur master kanonis/turunan yang dilindungi.
Parser DOCX memakai cabang konteks untuk heading `LAYER …` dan label
polos `1. Arab:`, `2. Latin:`, serta `3. Terjemahan:`. Untuk blok
Pola 49, parser membuang penanda blockquote Markdown `>` sebelum teks
masuk ke Word. Parser juga memberi konteks Arab RTL/kanan kepada
paragraf Layer 2 yang seluruh hurufnya Arab—lima paragraf pada Pola
49 dan tiga paragraf pada Pola 58; perilaku heading lama
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
- 73 heading Layer 2; 71 blok generik mempunyai `Media:`,
  `Langkah 1:`, langkah lanjutan yang berurutan, dan `Tujuan:` dalam
  urutan itu. Blok Halaman 49 dan 58 sama persis dengan konstanta
  pola lengkap masing-masing, memuat `Langkah ke-1` sampai
  `Langkah ke-3` secara berurutan, dan redaksi pendek kedua halaman
  sebelumnya tidak ditemukan lagi. Tujuan Halaman 64 dan 65 tetap
  ditemukan dalam Markdown dan DOCX;
- 58 footnote dan semuanya satu baris;
- daftar 26 rujukan crop sama persis dengan sumber; 9 crop Syarah
  berpindah ke Layer 1 dan tidak ada crop yang hilang atau diganti;
- parser DOCX memberi konteks Arab pada paragraf pertama di bawah
  semua label `1. Arab:`, konteks Latin pada semua `2. Latin:`, dan
  konteks Terjemahan pada semua `3. Terjemahan:`;
- DOCX memuat 123 Heading 1, 196 Heading 2 (123 Layer 1 + 73 Layer 2),
  369 Heading 3 untuk label Layer 1, 72 paragraf yang dimulai
  `Media:`, 259 paragraf generik `Langkah N:`, 71 paragraf
  `Tujuan:`, enam subjudul `Langkah ke-N` pada Pola 49 dan 58, 26
  gambar inline/media, dan 4 bagian font tertanam; tidak ada
  paragraf DOCX yang masih diawali penanda blockquote `>`;
- dibandingkan dengan keluaran Pola 49 sebelumnya, hanya unit
  Halaman 58 yang berubah pada Markdown dan DOCX; Arab Halaman 58
  identik, sedangkan seluruh unit lain identik;
- hash media DOCX sama dengan himpunan hash 26 berkas crop sumber;
- XML DOCX memuat penanda arah `w:bidi` dan `w:rtl`; parser konteks
  menghasilkan 557 paragraf Arab, 316 paragraf Latin, 380 paragraf
  Terjemahan, dan 451 paragraf Layer 2 non-Arab-murni. Lima paragraf
  Arab murni dalam Pola 49 dan tiga dalam Pola 58 mempunyai
  `w:bidi=1`, `w:jc=start`, dan `w:rtl` pada run teksnya;
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
penyuntingan ulang isi Layer 1. Karena itu dua batas dari sumber
bersih Halaman tetap terlihat apa adanya:

1. Latin Halaman 63 paragraf 2 masih berhenti sesudah tujuh nama
   bertanda `?`, sedangkan Arab berlanjut ke klausa sesudahnya.
   Perbaikan penanda eksplisit sebelumnya tidak memperluas ruang
   lingkup ke penghentian tanpa penanda itu.
2. Sisa bacaan Halaman 97 yang pada turunan Halaman dilengkapi dari
   Arab final tetap juga muncul dalam transliterasi warisan di awal
   Latin Halaman 98 karena segmentasi lintas halaman sumber tidak
   direstrukturisasi.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_build_bersih_2layer.py
.venv/bin/python scripts/build_docx_al_qorin.py --clean \
  --input al_qorin/AL_QORIN_123_BERSIH_2_LAYER.md \
  --output al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx
```
