# Audit revisi Arab Fusha halaman tersisa

Tanggal: 28 Oktober 2026.

## Dasar dan ruang lingkup

Pengguna meminta agen mengerjakan sendiri revisi 14 halaman yang masih
menyisakan elipsis atau deskriptor gambar pada Lapis 1, sesuai kaidah
Arab Fusha. Halaman/unit yang diganti hanya M71, M72, M73, M77, M99,
M107, M108, M110, M111, M112, M113, M114, M117, dan M118. Lapisan Latin,
Terjemahan, Syarah/catatan, Metode/Khususiyah, tabel, unit tetangga,
dan berkas crop tidak diganti atau diselaraskan ulang dalam tahap ini.

Teks hasil revisi disimpan sebagai sumber terkunci di
`al_qorin/arab_fusha_revised_remaining_2026-10-28/teks arab fusha halaman tersisa.txt`.
Arsip itu berisi 14 unit dan 53 paragraf sumber, 133 baris, 33.917 byte,
dengan SHA-256
`74a56f2282db552e9d05f87d1811a107f86f7b323a81d4c2cec2a3c85d3adcb9`.

Pembanding utama adalah Lapis 1 yang sudah terkunci sebelumnya dan
pindaian kitab asli `al qorin war riyadhah.pdf` dari Google Drive
(ID `1rj8FQydrOM1PlXoDvQmg5HPfzQw9FQ-Z`; salinan lokal terverifikasi
7.604.573 byte, SHA-256
`ac5ec9fc703df8434ea6c0e0363ecec38fd68dad170200d12d73dfbb4ae4c5c1`).
Halaman sasaran dibaca dari hamparan dua halaman pada PDF dan
dibandingkan per unit dengan teks Lapis 1 lama.

## Kaidah penyuntingan

- Urutan kata, pembagian halaman/unit, dan jumlah paragraf lama
  dipertahankan; total sasaran tetap 53 paragraf sumber.
- Ejaan, hamzah, harakat, dan i'rab dinormalkan menurut Fusha.
- Kesalahan konsonan hasil ekstraksi hanya diperbaiki bila pindaian,
  konteks kalimat, atau kutipan Qur'an/hadis yang dikenali mendukungnya.
- Singkatan kutipan kitab tidak diperluas menjadi ayat lengkap di luar
  petunjuk awal/akhir kutipan yang memang tertulis.
- Elipsis yang hanya menandai patah halaman atau bagian yang tidak
  terbaca dihapus setelah sambungan kalimatnya dipulihkan dari
  pindaian/konteks; arsip baru tidak memuat `...`.
- Nama diri, istilah asing, dan rangkaian talismanik yang tidak dapat
  diputuskan hanya dari kaidah Fusha dipertahankan dari bacaan lama
  atau konsonan pindaian. Revisi ini bukan klaim bahwa setiap nama
  asing telah terverifikasi secara filologis.

## Gambar wafak

Deskriptor gambar lama pada M71 dan M72 diganti paragraf persis
`[gambar wafak]`; pada M73 dan M77 penanda yang sama ditempatkan di
dalam paragraf pada posisi lambang dalam pindaian. Penanda dirender
menjadi crop presisi pengguna bernomor sama (`71.jpg`, `72.jpg`,
`73.jpg`, dan `77.jpg`) tepat satu kali. Sepuluh unit sasaran lain tidak
memuat penanda atau crop baru. Dengan tahap ini unit berpenanda menjadi
17; seluruh sisipan crop dalam kitab tetap 26.

## Batas verifikasi

Revisi ini adalah hasil kerja agen atas instruksi pengguna, bukan
ekstrak baru yang dikirim pengguna dan bukan transkripsi diplomatik
yang netral dari setiap huruf cetak. Cetakan asal sendiri mengandung
singkatan kutipan, ejaan lama, dan beberapa rangkaian nama/lambang
yang kabur. Karena itu hasil diposisikan sebagai teks baca Fusha yang
terkunci dan terdokumentasi, dengan ketidakpastian nama asing dan
rangkaian talismanik tetap diakui dalam audit ini.
