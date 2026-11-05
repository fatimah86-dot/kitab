# Asrār Rūḥāniyyah — Pembaca 5 Lapis

Aplikasi web (PWA-ready, React + Vite) untuk membaca master editorial
`REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md` dari repo ini.

Setiap halaman disajikan dalam lima lapis: **Arab · Latin · Terjemahan · Syarah · Khususiyah**,
tanpa menulis ulang teks — parser hanya memecah struktur master.

## Menjalankan

```sh
cd kitab-app
npm install
npm run dev      # http://localhost:5173
```

Perintah lain:

| Perintah | Fungsi |
|---|---|
| `npm run data` | Bangun ulang `src/data/kitab.json` dari master Markdown |
| `npm run build` | Bangun data + bundel produksi ke `dist/` |
| `npm run preview` | Sajikan hasil build |
| `npm run check` | Uji data, pencarian, dan render seluruh blok (tanpa browser) |
| `npm run standalone` | Bangun `unduh/kitab-asrar.html` — satu berkas untuk dibuka offline di HP |

Master dibaca dari `../REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md`. Untuk memakai berkas lain:

```sh
KITAB_MASTER=/jalur/ke/master.md npm run data
```

## Menjalankan di HP Android

Tidak perlu server sendiri. Tiga pilihan, dijelaskan langkah demi langkah pada
**[CARA-ANDROID.md](./CARA-ANDROID.md)**:

1. **Tautan pratinjau sesi** — buka alamat preview di Chrome HP (sementara).
2. **GitHub Pages** — aktifkan *Settings → Pages → Source: GitHub Actions*, lalu buka
   `https://fatimah86-dot.github.io/kitab/` (permanen, gratis).
3. **Satu berkas offline** — `unduh/kitab-asrar.html` (±2,7 MB) berisi seluruh teks,
   font, sampul, dan Arabiyah; buka langsung dari pengelola berkas Chrome.

Berkas mandiri dibangun ulang dengan `npm run standalone`.

## Fitur

- **Daftar halaman** dengan saring per bagian (Pembuka, Faedah, Doa & Riyadhah, Pelajaran), penanda wafaq, dan pencarian judul.
- **Pembaca lima lapis**: tiap lapis bisa ditampilkan/disembunyikan; preferensi disimpan di perangkat.
- **Tabel wafaq** dirender sebagai kotak huruf/angka RTL (terdeteksi otomatis huruf vs angka), bukan tabel markdown datar.
- **Pencarian penuh** di 65 halaman × 5 lapis, di sisi klien, dengan sorotan dan cuplikan per lapis.
- **Penanda halaman** dan **lanjut baca** tersimpan di `localStorage`.
- **Tema** terang / sepia / malam, pengatur ukuran huruf Arab dan Latin, pilihan font Arab (Amiri atau sistem).
- **Salin halaman**, **cetak** (gaya cetak khusus), daftar isi berbentuk laci, pintasan `←` `→` dan `/`.
- Nada dan struktur mengikuti naskah: klaim khasiat ditandai sebagai isi tradisi, bukan bukti medis.

## Arabiyah Center (ruang belajar bahasa Arab)

Rute `#/arabiyah` (tombol **Arabiyah** di bilah atas). Dibangun dari komponen
"Arabiyah Center" yang diberikan, di-port dari Tailwind/Next.js ke CSS modul
aplikasi ini tanpa mengubah perilaku maupun naskah panduannya:

- Enam mode: **Kamus · Nahwu & I'rab · Sharaf & Wazan · Balaghah · Imla' & Kitabah · Arudh & Qafiyah**.
- Panel sidebar + tab mode, kartu percakapan, contoh cepat, textarea Arab,
  dan **keyboard hijaiyah** 32 tombol (dengan hapus, bersihkan, spasi, sisip di posisi kursor).
- Respons dihasilkan **lokal** oleh `src/lib/arabiyah.js` (`generateSmartResponse`),
  termasuk panduan umum belajar dan panduan per mode — bukan model bahasa.
- Integrasi kitab: contoh cepat tambahan **"Dari kitab · halaman N"** memakai kutipan
  Arab halaman yang sedang dibaca, dan tombol bulan-bintang di pembaca membuka
  Arabiyah dengan konteks halaman tersebut.
- `npm run check` menguji 6 mode, 32 tombol keyboard, format setiap respons,
  dan render komponennya.

## Struktur

```
kitab-app/
├── scripts/
│   ├── build-data.mjs   # master .md  →  src/data/kitab.json
│   ├── titles.txt       # judul Latin & bagian per halaman
│   └── check.mjs        # uji data + pencarian + render
├── src/
│   ├── components/      # Home, Reader, Blocks, SearchView, SettingsView, Drawer, Arabiyah, Icons
│   ├── lib/             # text.js, search.js, store.js, arabiyah.js (aturan respons belajar)
│   ├── data/kitab.json  # hasil parser (dibangun, ikut repo agar app langsung jalan)
│   ├── App.jsx          # router hash + topbar + tema
│   ├── index.css        # tema pembaca kitab
│   └── arabiyah.css     # tema gelap-hijau/emas ruang belajar
└── public/art/sampul.jpg
```

## Catatan editorial yang dipertahankan

- Teks ditampilkan apa adanya, termasuk penanda `[konfirmasi editorial: ٤]` dan
  `[Rajah Huruf — tidak diterjemahkan]` (yang terakhir ditampilkan sebagai label kecil, bukan teks mentah).
- Halaman master 01–65 dipetakan ke folio cetak pada naskah; delapan folio yang tidak tersedia pada
  pindaian (14, 36–37, 40, 48, 56, 62, 72) dicatat di halaman Tentang aplikasi.
- Aplikasi ini alat baca, bukan pengesahan harakat, nahwu-sharaf, maupun khasiat.
