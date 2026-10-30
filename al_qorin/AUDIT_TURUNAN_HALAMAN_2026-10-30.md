# Audit Turunan “Halaman” Al-Qorin — 2026-10-30

## Status

Berkas dalam catatan ini adalah **edisi turunan terpisah**. Edisi
khatam kanonis pada commit `621563f` tidak diganti, tidak dibangun
ulang dari turunan ini, dan crop pengguna tidak diubah.

Sumber kanonis:

| Berkas | SHA-256 |
|---|---|
| `REVISI_AL_QORIN_123.md` | `7f850a55ad469effa0dd04aef80b972586bde58940d1b412f4c69c449bce9888` |
| `AL_QORIN_123_BERSIH.md` | `4fa012922f050cb0275a4cd370a2dcc3512021e95d399a36973a790610f9fb20` |
| `AL_QORIN_REVISI_123_5_LAPIS.docx` | `d0ed610e93bea7b0a56197cce045115e2719114405ab3f4a81181e9504f1ad0e` |
| `AL_QORIN_123_BERSIH.docx` | `0b41b67591e163a21af7b8e54d7d4c3351f44bde809557092df4104587d13f60` |

## Transformasi yang diterapkan

Skrip `scripts/al_qorin_build_halaman_derived.py` membaca salinan
kedua master dan menolak menulis ke jalur inputnya. Aturan hasil
klarifikasi pengguna adalah:

1. Judul unit `M<angka>` diganti menjadi satu label `Halaman <angka>`.
   Bila judul lama sudah memuat `Halaman <angka yang sama>` di awal
   atau `, HALAMAN <angka yang sama>` di akhir, pengulangan itu
   dibuang. Contoh: `M10 — Halaman 10, pembuka...` menjadi
   `Halaman 10 — pembuka...`.
2. Rujukan mandiri `M<angka>` di badan teks diganti menjadi
   `Halaman <angka>`; angka ditulis tanpa nol di depan.
3. Seluruh kalimat yang memuat `klaim penulis` secara tidak peka
   huruf dihapus. Frasa tumpang-tindih dalam `diklaim penulis` ikut
   terhitung sebagai kemunculan substring `klaim penulis`.
4. Seluruh kalimat yang memuat `Batch <angka>` secara tidak peka
   huruf dihapus.
5. Label `[CATATAN PENERJEMAH: ...]`, judul lapisan/subbagian,
   struktur sel tabel, tautan gambar, dan rujukan 26 crop dijaga.
6. Sesudah tahap di atas, daftar penggantian eksak berpenjaga
   memperbaiki penanda eksplisit belum-selesai pada Lapis 2 (Latin)
   turunan dan menyelaraskan sempit kalimat Terjemahan/catatan yang
   menempel pada titik Halaman 3 dan 11. Rincian serta batasannya ada
   pada bagian “Revisi penanda Latin” di bawah.

Penghapusan dilakukan pada granularitas kalimat, bukan sampai akhir
baris. Karena beberapa kalimat lama menggabungkan isi dan frasa
`klaim penulis`, sebagian isi kalimat itu memang ikut hilang sesuai
pilihan ruang lingkup yang ditetapkan. Ini salah satu alasan hasil
disimpan sebagai turunan, bukan pengganti edisi khatam.

## Revisi penanda Latin (turunan saja)

Inventaris awal menemukan 29 paragraf Lapis 2 penelitian dan 28
paragraf Lapis 2 bersih yang memuat penanda eksplisit: placeholder
Arab/vokalisasi, `«…»`, “tidak disalin penuh pada sumber kerja”, atau
kurung proses bersambung/lanjutan. Builder kini menerapkan 37
penggantian eksak penelitian dan 36 bersih. Jumlah itu terdiri atas
31/30 penggantian pada Lapis 2—beberapa paragraf mempunyai dua
penanda—ditambah enam penyelarasan sempit pada Terjemahan/catatan
Halaman 3 dan 11. Setiap string lama wajib muncul tepat satu kali;
bila tidak, pembangunan berhenti dan tidak menulis keluaran yang
salah.

Perlakuan per titik adalah:

- **Halaman 3:** Arab final menetapkan `manna biriwaaqit takwiini`,
  `bi-aayatil 'ajzi`, dan `ushuulil-mawjuudaati`. Terjemahan dan
  catatan yang masih menyebut bacaan itu belum pasti diganti sebatas
  frasa/kalimat terkaitnya.
- **Halaman 11:** frasa wadah tertutup dan klausa tangan dari bawah
  penutup ditransliterasikan dari Arab final; catatan lama yang
  menyebut kata sesudah wadah sebagai elipsis diselaraskan. Ujung
  halaman tetap potongan asli dan hanya ditulis `wastidaamati...`.
- **Halaman 12, 18, dan 32:** penanda segmen dibuang karena paragraf
  Latin berikutnya memang sudah memuat sambungannya.
- **Halaman 12 (paragraf 3), 14, 16, 23, 26, 27, 35, dan 112:**
  potongan tepi halaman tidak dilengkapi dengan karangan; penanda
  proses diganti elipsis polos `...`. Kurung `[ts-tsaanii]` pada
  Halaman 14 bukan celah karena mencerminkan kurung Arab `[الثاني]`.
- **Halaman 60–63:** residu “tidak disalin penuh” sesudah judul daftar
  dibuang karena daftar Latinnya langsung mengikuti. Judul Halaman 61
  dinormalkan menjadi `Asmaa-ul qamari bi-maqluubihii`.
- **Halaman 71 penelitian:** glif `ط` dalam deskriptor gambar Lapis 2
  diganti nama Latin `thaa`; transkripsi rajah pada lapisan lain tidak
  diubah.
- **Halaman 74:** ringkasan “sembilan … yah yah yah (berulang)” diganti
  deret persis Arab final: 13 digit `9` tanpa spasi, diikuti 13 kali
  `yah`.
- **Halaman 96:** dua penanda di antara bagian bait yang sudah
  tertransliterasi diganti pemisah bait `/`, bukan diisi kata baru.
- **Halaman 97:** penanda internal sesudah `sarii'atul ijaabati`
  dibuang. Bacaan sesudah `wa khalaqa` dilengkapi dari Arab final unit
  itu, termasuk `ajiibii ajiibii` dan `uuhiya ilayya aakhirihaa`;
  transliterasi lama pada awal Latin Halaman 98 tidak disalin karena
  membawa bacaan warisan yang berbeda. Segmentasi lintas halaman yang
  sudah ada tidak direstrukturisasi, sehingga sisa bacaan tersebut
  tetap juga muncul pada Latin Halaman 98 sebagaimana struktur lama.
- **Halaman 98:** paragraf yang sebelumnya berisi prosa Indonesia
  belum selesai pada Lapis 2 diganti transliterasi judul dan paragraf
  Arab final tentang **Najmah**. Penelitian mempertahankan deskriptor
  jadwal dalam kurung di depannya; Terjemahan Indonesia tetap berada
  pada Lapis 3.
- Arab final, judul unit, urutan/segmentasi paragraf selain teks pada
  titik penggantian, tautan gambar, dan 26 crop tidak diubah.

Revisi ini **bukan** penyejajaran ulang seluruh Latin terhadap Arab
final. Ketidakselarasan atau bacaan warisan tanpa penanda eksplisit
dalam inventaris tidak ditulis ulang. Satu batas yang dicatat secara
khusus: Halaman 63 paragraf Latin 2 masih berhenti sesudah tujuh nama
bertanda `?`, sedangkan Arabnya berlanjut ke klausa `بِحَقِّ هَذِهِ
الْأَسْمَاءِ…`. Itu tidak mempunyai penanda elipsis/kurung/placeholder
dalam inventaris yang dikerjakan, jadi tidak diperluas diam-diam pada
revisi ini.

## Hasil transformasi Markdown

| Keluaran | Judul halaman | Rujukan badan diganti | Kalimat klaim dihapus | Kalimat Batch bernomor dihapus | Baris berubah pada tahap label/kalimat | Baris menjadi kosong | Penggantian eksak Latin + penyelarasan sempit |
|---|---:|---:|---:|---:|---:|---:|---:|
| `REVISI_AL_QORIN_123_HALAMAN.md` | 122 | 23 | 28 | 1 | 161 | 0 | 37 |
| `AL_QORIN_123_BERSIH_HALAMAN.md` | 122 | 12 | 18 | 0 | 151 | 0 | 36 |

Dua rujukan `M01–M05` pada master penelitian tidak dihitung sebagai
penggantian badan karena berada di kalimat `Batch 01` yang dihapus.

Hash dan ukuran Markdown turunan:

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `REVISI_AL_QORIN_123_HALAMAN.md` | 757.955 byte | `d57c97c5e6cd75159593bf4ba3ec11ab6d296ea83172441b54ad99df7c024997` |
| `AL_QORIN_123_BERSIH_HALAMAN.md` | 673.303 byte | `8a59040ba8a1a3b6fc466b1f0490e5efcd6c1fad1ad0e15847ac0ca9437d2db7` |

## Keluaran DOCX

DOCX dibangun dengan builder kanonis yang sama, dengan `--clean`
khusus untuk edisi bersih:

| Berkas | Ukuran | SHA-256 |
|---|---:|---|
| `AL_QORIN_REVISI_123_5_LAPIS_HALAMAN.docx` | 6.984.837 byte | `4bdd44a67193be61345b6bed3fe6631ccdfbfef0d9a9d0885fef5e6afb4c89c0` |
| `AL_QORIN_123_BERSIH_HALAMAN.docx` | 6.934.453 byte | `dd94686623649ad3d8a62e64fff4d8af9a9d9fb7f2107d0cf0fbcc98d76d59bd` |

## QA

Pemeriksaan terprogram atas Markdown dan DOCX turunan membuktikan:

- 123 judul unit pada masing-masing keluaran: SAMPUL diikuti urutan
  tepat Halaman 1–122;
- 123 Heading 1 unit di masing-masing DOCX;
- 26 rujukan gambar Markdown dan 26 bagian media DOCX; daftar
  rujukan gambar sama persis dengan master kanonis;
- 25 label catatan penerjemah pada masing-masing master, sama
  dengan jumlah sumber;
- tidak ada subbagian daun yang kosong;
- jumlah struktur tidak berubah dari sumber masing-masing: penelitian
  123 unit/611 judul lapisan/366 judul subbagian dan bersih 123
  unit/568 judul lapisan/0 judul subbagian;
- pada Lapis 2 kedua keluaran tidak tersisa `«…»`,
  `[tidak disalin penuh pada sumber kerja]`,
  `[bersambung ke segmen berikutnya]`,
  `[lanjutan dari segmen sebelumnya]`, frasa “vokalisasi/bacaan belum
  ditetapkan”, `(bersambung ke halaman 98)`, `huruf «ط»`, atau karakter
  aksara Arab lain; elipsis polos hanya tersisa satu kali pada potongan
  tepi Halaman 11, 12, 14, 16, 23, 26, 27, 35, dan 112;
- `«…»` yang masih ada di luar Lapis 2 hanya empat kemunculan pada
  catatan penelitian dan satu pada Syarah bersih, semuanya sebagai
  penyebutan konvensi editorial dalam prosa catatan, bukan placeholder
  Latin;
- cuplikan kunci perbaikan (`manna biriwaaqit`, `bi-aayatil 'ajzi`,
  `ushuulil-mawjuudaati`, `aaniyatin mughaththaatin`, deret Halaman 74,
  `Ajiibii ajiibii`, dan `Baabu istikhdaami najmata`) masing-masing
  muncul satu kali dalam teks kedua DOCX;
- tidak ada rujukan mandiri `M<angka>`, frasa `klaim penulis`, atau
  `Batch <angka>` yang tersisa dalam Markdown maupun teks DOCX
  (termasuk tabel serta header/footer);
- tidak ada perubahan Git pada master kanonis, DOCX khatam,
  direktori `wafaq_qorin/`, manifest crop, atau berkas crop;
- pembangunan Markdown turunan diulang dan menghasilkan SHA-256
  yang sama; discovery test repo mencatat 40 test terdaftar dengan
  33 lulus dan 7 dilewati karena work JSON ter-ignore tidak hadir.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_build_halaman_derived.py
.venv/bin/python scripts/build_docx_al_qorin.py \
  --input al_qorin/REVISI_AL_QORIN_123_HALAMAN.md \
  --output al_qorin/AL_QORIN_REVISI_123_5_LAPIS_HALAMAN.docx
.venv/bin/python scripts/build_docx_al_qorin.py --clean \
  --input al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md \
  --output al_qorin/AL_QORIN_123_BERSIH_HALAMAN.docx
```

Hasil ini tidak mengubah kesimpulan edisi khatam: versi kanonis
tetap 123 unit, 611 lapisan penelitian, dan 26 crop. Versi turunan
mengganti label unit menjadi “Halaman”, menghapus kalimat-kalimat
yang masuk dua pola di atas, dan—hanya pada salinan turunannya—
memperbaiki penanda eksplisit Lapis 2 serta menyelaraskan sempit
kalimat hilir pada Halaman 3 dan 11 sebagaimana dirinci dalam audit
ini.
