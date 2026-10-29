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

## Format keluaran

Setiap unit memakai struktur:

```text
## Halaman N — …
### LAYER 1 - KETERANGAN HALAMAN
#### 1. Arab
#### 2. Latin
#### 3. Terjemahan
#### [crop bila crop lama berada pada Syarah]
#### [footnote satu baris bila ada]
### LAYER 2 - TATACARA PRAKTIK   (kondisional)
**Media:** …
**Langkah:**
1. …
2. …
**Tujuan:** …
```

### Layer 1

- Badan **Arab**, **Latin**, dan **Terjemahan** disalin dari sumber
  bersih Halaman tanpa penggantian kata, harakat, transliterasi,
  terjemahan, urutan paragraf, tabel, atau label penerjemah.
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
mempertahankan **73 Layer 2** dengan total **263 langkah bernomor**.
Tiga bagian lama tidak dijadikan Layer 2 karena prosanya sendiri
menyatakan tidak ada tatacara/praktik baru pada halaman itu:

- Halaman 103;
- Halaman 113;
- Halaman 118.

Aturan konversinya:

- `**Media:**` memakai field Media lama. Field Bukhur dilipat ke
  Media sebagai `Bukhur: …`. Tujuh unit tanpa field Media diberi isi
  hanya dari medium/rujukan yang sudah dinyatakan pada bagiannya:
  Halaman 4, 7, 38, 61, 62, 107, dan 122.
- `**Langkah:**` menyusun prosa praktik lama menjadi langkah bernomor
  berdasarkan urutan kalimat/klausa. Kalimat dokumenter seperti
  atribusi, “bukan anjuran”, “tidak ada jaminan”, “tidak
  diverifikasi”, dan penilaian sumber akidah tidak dibawa ke langkah.
- Field Waktu tidak dibuat sebagai heading keempat. Bila isinya belum
  tercakup secara substansial oleh prosa langkah, ia dimasukkan
  sebagai langkah pertama berlabel “Waktu yang dinyatakan: …”.
- `**Tujuan:**` memakai pemetaan eksplisit per halaman di builder,
  berdasarkan tujuan/topik yang dinyatakan prosa praktik lama atau
  judul bab yang dikutip di dalamnya. Halaman 7, 41, dan 105 ditulis
  “Tidak dinyatakan secara tersendiri pada halaman ini” karena bagian
  praktik lamanya tidak menyatakan tujuan tersendiri.
- Halaman 98 dan 105 hanya mempunyai field Waktu/Media (Halaman 105
  prosanya hanya kalimat dokumenter), sehingga langkahnya dibentuk
  langsung dari kedua field tersebut tanpa menambah bahan atau hasil.
- Inventaris murni titik/bentuk rajah pada praktik lama Halaman 68,
  72, dan 74 tidak dijadikan langkah. Crop rajahnya tetap tampil di
  Layer 1; Media tetap menyebut rajah/tulisan yang relevan.
- Tidak ada Syarah akidah dan tidak ada penjelasan panjang baru di
  Layer 1 atau Layer 2. Tujuan dicatat sebagai tujuan yang dirumuskan
  naskah, bukan sebagai pengesahan hasil.

## Keluaran

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_123_BERSIH_2_LAYER.md` | 606.158 byte | `97a62d12fc0e116cd7cd6a424fd9c6f21a116c09b0ddb490c6b594c6183aa244` |
| `AL_QORIN_123_BERSIH_2_LAYER.docx` | 6.893.816 byte | `03d6c7ae72dc824bc284daa6a614093f9f8c961c9fa0397d1d0a8ba0046de3b3` |

Builder Markdown menolak menulis selain nama berakhiran
`_2_LAYER.md` dan menolak jalur master kanonis/turunan yang dilindungi.
Parser DOCX hanya ditambah cabang konteks untuk heading `LAYER …`;
perilaku heading lama dipertahankan.

## QA

Pemeriksaan builder dan pemeriksaan independen membuktikan:

- 123 unit dengan heading yang sama persis: SAMPUL diikuti Halaman
  1–122;
- 123 heading Layer 1 dan masing-masing 123 subheading Arab, Latin,
  dan Terjemahan;
- badan Arab dan Latin setiap unit sama byte-for-byte dengan sumber
  setelah pemangkasan baris kosong tepi; badan Terjemahan merupakan
  awalan persis dari badan keluaran sebelum crop/footnote tambahan;
- 73 heading Layer 2; setiap blok mempunyai Media, Langkah, dan Tujuan
  dalam urutan itu, dengan nomor langkah berurutan mulai dari 1;
- 58 footnote dan semuanya satu baris;
- daftar 26 rujukan crop sama persis dengan sumber; 9 crop Syarah
  berpindah ke Layer 1 dan tidak ada crop yang hilang atau diganti;
- parser DOCX memberi konteks Arab pada paragraf pertama di bawah
  semua subheading `1. Arab`, konteks Latin pada semua `2. Latin`, dan
  konteks Terjemahan pada semua `3. Terjemahan`;
- DOCX memuat 123 Heading 1, 196 Heading 2 (123 Layer 1 + 73 Layer 2),
  369 Heading 3, 26 gambar inline/media, dan 4 bagian font tertanam;
- hash media DOCX sama dengan himpunan hash 26 berkas crop sumber;
- XML DOCX memuat penanda arah `w:bidi` dan `w:rtl`; parser konteks
  menghasilkan 549 paragraf Arab, 315 paragraf Latin, 379 paragraf
  Terjemahan, dan 292 paragraf Layer 2;
- pembangunan Markdown diulang dan menghasilkan SHA-256 yang sama;
- discovery test repo: 40 test terdaftar, 33 lulus, dan 7 dilewati
  karena work JSON ter-ignore tidak hadir;
- hash berkas lama yang diperiksa kembali tetap:
  `AL_QORIN_123_BERSIH.md` `4fa012922f050cb0275a4cd370a2dcc3512021e95d399a36973a790610f9fb20`,
  `AL_QORIN_123_BERSIH.docx` `0b41b67591e163a21af7b8e54d7d4c3351f44bde809557092df4104587d13f60`,
  dan DOCX bersih Halaman `dd94686623649ad3d8a62e64fff4d8af9a9d9fb7f2107d0cf0fbcc98d76d59bd`.

## Batasan yang dipertahankan

Konversi ini adalah perubahan format turunan, bukan penyuntingan
ulang isi Layer 1. Karena itu dua batas dari sumber bersih Halaman
tetap terlihat apa adanya:

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
