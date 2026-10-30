# AUDIT ARAB KIRIMAN CHAT PENGGUNA — 28 OKTOBER 2026

## Identitas kiriman

- Judul kiriman: **“AL-QORIN — ARAB BERHAROKAT FULL KHATAM 123 — SHAHIH — KAIDAH MIN/MINNA/MAN”**.
- Bentuk penerimaan: teks ditempel langsung pada chat, bukan DOCX/MD/TXT/Google Docs.
  Karena itu kiriman ini **tidak mempunyai berkas byte-persis yang dapat di-hash**
  di workspace. Audit ini mencatat keputusan penyuntingan, bukan mengklaim telah
  mengarsipkan byte pesan chat.
- Cakupan heading pada pesan: SAMPUL dan M01–M122 tampak lengkap.
- Keputusan: **diterima sebagai salinan/konfirmasi atas Lapis 1 yang sedang
  berjalan; ditolak sebagai sumber koreksi Arab baru atau sebagai master.**

## Temuan utama: kiriman adalah Lapis 1 kanonis saat ini

Kiriman secara material sama dengan bidang `arab` pada master terintegrasi
(`al_qorin/REVISI_AL_QORIN_123.md` / data kerja `integrated_units.json`), bukan
transkripsi independen baru dari pindaian. Bukti sidik jari yang diperiksa:

- Judul unit sama dengan judul editorial master, termasuk judul modern/internal
  yang tidak mungkin berasal dari halaman Arab cetak, misalnya M10, M24 dengan
  frasa **“(akhir target halaman 24)”**, M49, M58, dan M88.
- Paragraf-paragraf M01, M52, M58, M65, M66, M67, M69, M71, M88, M90, M102,
  M107, M110, dan M122 sama dengan Arab kanonis, termasuk tanda baca dan
  deskriptor gambar dalam kurung siku.
- Placeholder kerja berbahasa Indonesia yang memang sudah berada di bidang Arab
  kanonis ikut tersalin: **“tidak disalin penuh pada sumber kerja” 4 kali**
  (M11, M61, M97) dan **“bersambung ke segmen berikutnya” 9 kali**
  (M60, M61, M62, M63, M96); total `«…»` 14 kali pada M11, M60–M63, M96,
  M97, dan M112.
- Deskriptor rajah Arab pada M58 dan M71 juga sama persis dengan master;
  deskriptor bukan isi sel wafaq dan tidak menggantikan `rajah_blocks`
  maupun 26 crop pengguna.

Dengan demikian kiriman ini tidak menambah bukti baca baru terhadap pindaian.
Menimpakan Lapis 1 dengannya hanya akan menulis ulang teks yang sama sambil
berisiko menghilangkan tabel `rajah_blocks`, segmentasi paragraf, dan penjaga
builder yang sudah teruji.

## Mengapa belum dapat disebut “full berharokat shahih”

1. **Kaidah MIN/MINNA/MAN belum diterapkan pada M03.** Kata kuncinya tetap
   `من` tanpa harakat, sehingga belum ditetapkan sebagai `مِنْ`, `مَنَّ`, atau
   `مَنْ`. Kata `بية` dan `اصوال` juga tetap tanpa vokalisasi dan belum
   terpecahkan.
2. **Masih ada celah salinan.** M11, M60–M63, M96, M97, dan M112 tetap memuat
   elipsis/placeholder segmen, sehingga paket ini belum khatam sebagai matan
   Arab bersih.
3. **Masih ada rangkaian tidak berharakat**, misalnya M74
   `اكتب هذه الأسماء`, baris nama pada M88, dan pengulangan `الله` tanpa
   harakat pada M102 serta M110.
4. **Bacaan rusak lama dipertahankan**, antara lain M25 `الْخَزَرْنَد`,
   M44 `الْمُشَارِ يخ` (kata terbelah), M51 `فَعَالِجَةً`, M58 `وَاخْوِقْلَهُ`,
   serta kutipan M90 `افَتَخَذُونِي` yang tidak sama dengan lafaz Al-Qur'an.
5. **M107 tidak menyelesaikan selisih pindaian yang sudah tercatat.** Kiriman
   tetap memuat frasa rusak dan `١ مَرَّةً`; catatan beda bacaan terhadap
   pindaian (21 kali sesudah fardu) tetap berlaku dan tidak boleh ditimpa
   diam-diam.
6. **Tabel dan gambar tidak ditranskripsikan penuh.** M65–M69, M98, M109,
   dan M121 masih berupa deskriptor halaman. Isi visual tetap harus memakai
   `rajah_blocks` kanonis dan crop pengguna, bukan deskriptor kiriman.

## Lokus yang harus diselesaikan oleh Arab koreksi yang benar-benar baru

Versi koreksi independen minimal harus memberi bacaan dan dasar pindaian untuk:

- M03: `من`, `بية`, `اصوال`, susunan kehambaan, dan penutup salawat;
- M04: `على رب العلماء`; M05: `انتشات` dan penutup gramatikalnya;
- celah M11, M60–M63, M96, M97, dan elipsis lain pada audit 123 unit;
- M25 `الخزرند`, M44 `المشار يخ`, M51 `فعالجة`, M58 `واخوقله`;
- M74 baris tidak berharakat, M88 baris nama pengarang iklan, M90 kutipan ayat;
- M107 `١ مرة` terhadap bukti pindaian; dan
- seluruh kata/rumus talismani yang harakatnya tidak boleh ditebak hanya agar
  tampak lengkap.

## Tindak lanjut

- **Tidak ada perubahan kanonis** dari kiriman ini: DOCX, Markdown, preview,
  Lapis 1–5, dan 26 crop tidak berubah; checkpoint terakhir tetap commit
  `3a77f6f`.
- Apabila pengguna memang bermaksud **menyetujui Lapis 1 yang sekarang** apa
  adanya, persetujuan itu dapat dicatat sebagai penguncian baseline kerja,
  tetapi status editorialnya tetap “bacaan kerja dengan lokus ragu”, bukan
  “shahih final”.
- Apabila pengguna memiliki versi koreksi independen, kirim sebagai **berkas**
  DOCX/MD/TXT atau tautan Google Docs agar dapat diarsipkan byte-persis,
  di-hash, dan di-diff mesin per paragraf terhadap master serta pindaian.
