# Catatan Batch Terjemahan Total 04 — M33–M49

## Ruang lingkup

- Unit: M33–M49 (17 unit).
- Lapisan yang diubah: hanya **Lapis 3 Terjemahan** pada `REVISI_AL_QORIN_123.md` dan padanan hasil `clean_translation` pada `AL_QORIN_123_BERSIH.md`.
- Jumlah paragraf pengganti: 33.
- Override: `overrides_terjemahan_total_batch04.json`.
- Applier: `scripts/al_qorin_apply_translation_total_batches.py --batch 4`.
- Bukti ruang lingkup: perbandingan terurai per unit/lapis terhadap commit Batch 03 (`761bd95`) menunjukkan tidak ada perbedaan di luar Lapis 3 M33–M49; Arab, Latin, lapis lain, tabel, rajah, dan crop—termasuk `wafaq_qorin/49.jpg` pada M49—tetap.

## Bukti tiga lapis

Setiap unit diterjemahkan dari Arab final terkunci, dibandingkan dengan:

1. Arab, Latin, Terjemahan lama, Catatan penyunting, Metode, dan Lapis 5 pada master.
2. Halaman cetak buku asli 33–49 dari PDF pindaian `al qorin war riyadhah.pdf` SHA-256 `ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`, halaman PDF 17–25.
3. Aturan `PANDUAN_REVISI_TOTAL_TERJEMAHAN_AL_QORIN.md`: praktik dan hasil supernatural hanya dinisbatkan kepada penulis; tidak ada diagnosis, janji penyembuhan, atau penilaian sanad yang dibuat dalam terjemahan.

## Hitungan retro Lapis 3

| Unit | Paragraf |
|---|---:|
| M33 | 2 |
| M34 | 2 |
| M35 | 2 |
| M36 | 2 |
| M37 | 2 |
| M38 | 2 |
| M39 | 2 |
| M40 | 2 |
| M41 | 2 |
| M42 | 2 |
| M43 | 2 |
| M44 | 2 |
| M45 | 2 |
| M46 | 2 |
| M47 | 1 |
| M48 | 2 |
| M49 | 2 |
| **Total** | **33** |

Jumlah paragraf Lapis 3 lama dipertahankan. Judul Arab yang berdiri sendiri pada M35, M41, M43, M45, dan M48 digabungkan ke paragraf terjemahan pertama sesuai struktur lama.

## Koreksi penting dari terjemahan lama

- M33 mengikuti Arab final *yatanafasu*, *fayunaqqi*, *hadahum*, dan *waq'an*; rangkaian “Allah mengubah jiwa dengan ruh …” tidak dilancarkan karena hubungan katanya di sumber belum jelas.
- M35 mengikuti *latha'if minanihi* (“kelembutan karunia-Nya”) pada Arab final, bukan bacaan Latin lama.
- M36 dan M29 dibaca konsisten: *sya'ir* adalah jelai/barley; frasa *zhahiran wa bathinan* diterjemahkan “lahir dan batin”.
- M39 tidak menambahkan kata “kantuk” yang tidak tertulis pada Arab final; angka *tis'un* dibiarkan menyambung ke kata *yauman* pada M40.
- M40 mempertahankan *min ma'lum* dan *la yuktsir ad-du'aa'* sesuai Arab final. Jadwal disebut 90 hari tetapi rinciannya 4 × 20 hari; selisih ini tidak ditambal.
- M41 mengikuti *al-halaawah fi al-'amal* (“kemanisan dalam amal”) dan *khuluww al-ma'idah aw nishfihaa*.
- M44 mengikuti *al-masyaayikh* dan *yatashaara'uun*; padanan lama “peneliti/musyarikha” dan “saling mendengar” tidak diteruskan.
- M48 mengikuti sudut pandang penulis *aradtu an u'allimaka* (“aku ingin mengajarkan kepadamu”), bukan terjemahan lama yang membalik subjeknya.
- M49 memasukkan subjek lelaki yang ada pada Arab final tetapi hilang dalam terjemahan lama, serta mempertahankan urutan huruf Khatam Sulaiman dan potongan kutipan yang belum dapat dilancarkan.

## Catatan terbuka

- M33: susunan *la yushbiruhu … mani'* dan *la yughayyiru … an-nafs bi-ruhin …* masih belum mantap secara sintaksis.
- M37–M39: gejala jantung berdebar, persendian gelisah, penampakan cahaya, dan klaim melihat Rasulullah adalah pengalaman yang dinisbatkan penulis kepada pelaku riyadhah. Terjemahan tidak menyatakan gejala itu aman, khas, atau bukti pencapaian.
- M38: kalimat penutup mengenai khathir dan ilmu tetap terbuka; diterjemahkan harfiah dengan penanda.
- M40: kata kerja “melihat minyak-minyak”, frasa *min ma'lum*, dan selisih 90 hari versus empat tahap 20 hari tetap tidak dijelaskan oleh sumber.
- M42: equivalensi nama Muhammad—*as-Salam* 131 tidak dihitung ulang dan tidak disahkan.
- M43: atribusi riwayat kepada Muslim dan Ahmad hanya dicatat sebagai atribusi penulis. Bentuk *afaqadti syaithanaki* pada Arab final janggal dan diterjemahkan harfiah.
- M44–M48: klasifikasi qarin, kelompok jin, habitat, jumlah, dan akibat seksual, reproduksi, hewan, maupun manusia adalah klaim penulis. Tidak ada yang dijadikan diagnosis atau dasar menuduh seseorang melakukan sihir.
- M46–M47: klaim mengenai keguguran, kematian anak, kemandulan, dan haid dipertahankan hanya untuk ketepatan tekstual. Teks ini tidak boleh menggantikan pemeriksaan medis dan tidak menyediakan bukti sebab-akibat.
- M49: *at-tawabi'*, *asy-syumukh al-'aliqah*, *as-sabasib*, dan potongan *tazalzala nuzulan* belum pasti. Crop 49 pada Metode tetap berkas pengguna dan tidak digambar ulang dalam Lapis 3.
- Sejumlah halaman pindaian dalam rentang ini memuat baris yang tidak ada pada Arab final terkunci, khususnya lanjutan M37, M38, M42, dan M49. Karena izin batch ini khusus Lapis 3 dari Arab terkunci, baris tersebut tidak ditambahkan; persoalan batas/kelengkapan Arab tetap terbuka untuk audit Arab terpisah.

## Reproduksi

```bash
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 4 --check
.venv/bin/python scripts/al_qorin_apply_translation_total_batches.py --batch 4
```

Dalam pembangunan data terintegrasi, override ini diterapkan oleh `scripts/al_qorin_build_integrated.py` sesudah seluruh tahap Arab final, bersama batch lanjutan lain yang tersedia.
