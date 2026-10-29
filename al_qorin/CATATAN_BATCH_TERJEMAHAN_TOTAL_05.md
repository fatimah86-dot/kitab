# Catatan Batch Terjemahan Total 05 — M50–M71

## Ruang lingkup

- Unit: M50–M71 (22 unit).
- Lapisan yang diubah: hanya **Lapis 3 Terjemahan** pada `REVISI_AL_QORIN_123.md` dan padanan hasil `clean_translation` pada `AL_QORIN_123_BERSIH.md`.
- Jumlah paragraf pengganti: 42.
- Override: `overrides_terjemahan_total_batch05.json`.
- Applier: `scripts/al_qorin_apply_translation_total_batches.py --batch 5`.
- Bukti ruang lingkup: scope-proof terhadap commit Batch 04 (`5ee0541`) menunjukkan tidak ada perbedaan di luar Lapis 3 M50–M71. Arab, Latin, Lapis 4/5, tabel deskriptif rajah, serta crop pengguna M58 dan M64–M71 tidak diubah.

## Bukti tiga lapis

Setiap unit diterjemahkan dari Arab final terkunci, dibandingkan dengan:

1. Arab, Latin, Terjemahan lama, Catatan penyunting, Metode, dan Lapis 5 pada master.
2. Halaman cetak 50–71 dari PDF `al qorin war riyadhah.pdf` SHA-256 `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`, halaman PDF 26–36.
3. Panduan revisi total Anwar: daftar dan angka dipertahankan, istilah asing diberi glos secukupnya, nama tak transparan ditransliterasikan, dan semua janji kesembuhan/kehamilan hanya dinisbatkan kepada penulis.

## Hitungan retro Lapis 3

| Rentang | Jumlah |
|---|---:|
| M50–M51 | 2 paragraf per unit |
| M52 | 1 |
| M53 | 2 |
| M54 | 1 |
| M55–M71 | 2 paragraf per unit |
| **Total** | **42** |

Arab final sering memecah judul, butir daftar, deskriptor rajah, dan crop menjadi paragraf tersendiri; struktur satu atau dua paragraf Lapis 3 lama dipertahankan dengan cakupan semantik tingkat unit.

## Koreksi penting dari terjemahan lama

- M50 memakai ayat lengkap tentang orang mati yang dihidupkan dan diberi cahaya dari Arab final; terjemahan lama yang hanya menyisakan fragmen Latin “atau siapa yang mati kepada manusia” diganti.
- M51 mengikuti *al-'azimah wa az-zajr bi-syiddah* dan *al-mustakah as-sa'ilah* pada Arab final.
- M56 menautkan *ila akhirihi* pada potongan Surah al-Hasyr, bukan pada akhir al-Ikhlas dan al-Mu‘awwidzatain.
- M58 mengikuti *yumha wa yusyfa*; angka wafaq 5×5 dipertahankan sebagai deskriptor tanpa menghitung atau membuktikan pola numeriknya.
- M59 menerjemahkan judul *al-mamlakah ar-ruhaniyyah* sebagai “Kerajaan Ruhani”.
- M61 menransliterasikan nama bulan langsung dari ejaan Arab final dan menggunakan *Liyasylisy* serta *Duqanil* sesuai bunyi final, dengan ketidakpastian huruf dinyatakan.
- M63 mengikuti *Qasurah* dan *Inba'il* dan kini memuat bagian imperatif ‘azimah sesudah daftar nama, yang sebelumnya tidak tercakup.
- M65 menerjemahkan *yumha* sebagai dihapus/dilarutkan, bukan dipanaskan.
- M66 tidak mengganti bentuk tak jelas *wa-khumma* dalam Arab final dengan bacaan Latin lama; kata itu ditandai.
- M68 mengikuti *Shadday* pada Arab final, bukan padanan lama *Syaray*.
- M70 tidak menambahkan rangkaian *maa baani* dari Latin/pindaian lama karena tidak terdapat pada Arab final terkunci; *kuzbarah* diterjemahkan ketumbar.
- M71 mengikuti *tumha bi-laban ma'iz* sebagai dihapus/dilarutkan dengan susu kambing, bukan “dipanaskan dengan lemak kambing”.

## Wafaq dan crop

- M58: paragraf kedua tetap memuat deskriptor numerik wafaq 5×5 dari crop `58.jpg`. Sel `١٠٤` dan sebagian susunan baris bawah tetap rendah kepastiannya; tidak ada gambar ulang di Lapis 3.
- M64–M65: deskriptor Khatam Sulaiman dipertahankan; crop `64.jpg` dan `65.jpg` di lapis lain tetap.
- M66–M71: crop Lapis 1 disebutkan secara netral (“di titik ini … melalui crop pengguna”) tanpa orang pertama, tanpa menafsirkan huruf/angka/sel, dan tanpa mengubah tabel deskriptif pada Metode. Semua crop tetap byte-identik dari manifest.

## Catatan terbuka dan batas keselamatan

- M52: penomoran syarat melompat dari pertama ke ketiga; syarat kedua tidak dikarang.
- M53: instruksi memegang dan mendudukkan orang, pembedaan pendamping menurut jenis kelamin, serta larangan hubungan selama “pengobatan” dilaporkan sebagai redaksi penulis, bukan anjuran penerjemah.
- M57: judul “segala penyakit” tidak membuktikan rangkaian doa itu mengobati semua penyakit.
- M58: oksida/tinta, prosedur penghapusan tulisan, dan wafaq tidak dinilai aman atau efektif.
- M60–M63: pemetaan hari, logam, planet, buruj, raja, ruhani, dan nama-nama `Liyakhim` dsb. adalah kerangka penulis. Ejaan sejumlah nama talismanik tidak dapat diverifikasi secara leksikal.
- M63: kalimat “Kami mencukupkan dengan kadar ini dalam kitab lain” dan fungsi penanda `٢` sesudah nama tetap tidak tegas.
- M64: klausa “dari apa yang datang” dan pengulangan janji Tuhan berhancur-luluh dipertahankan apa adanya.
- M66: *wa-khumma* belum dapat ditetapkan; tidak digunakan untuk merekonstruksi prosedur.
- M68–M71: tulisan/rajah, gantungan, percobaan pada ayam, air tulisan, dan susu kambing yang diminum diklaim berhubungan dengan kehamilan atau pencegahan keguguran. Tidak ada klaim itu yang disahkan; teks tidak boleh menggantikan pemeriksaan atau perawatan medis.
- M69: kata pertama *takhluqkum* pada Arab final tidak lengkap secara tata bahasa walaupun konteks ayat jelas. Batch Lapis 3 tidak menambalnya dan tidak mengubah Arab.
- M70: *athbaq* dan *yunajjamu* tidak dijelaskan cukup rinci oleh teks; padanan benda/prosedurnya dinyatakan terbuka.
- M71: jumlah 109 dipertahankan persis dari Arab final, tetapi keamanan maupun keberhasilan faedah janin tidak dinilai.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 5 --check
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 5
```

Pada pembangunan terintegrasi, Batch 05 diterapkan sesudah seluruh penggantian Arab dan kunci Fusha, bersama batch lanjutan lain yang tersedia.
