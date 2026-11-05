# Cara menjalankan aplikasi di HP Android

Aplikasi ini adalah situs statis — tidak perlu Play Store, tidak perlu server sendiri.
Pilih salah satu dari tiga cara berikut, dari yang paling cepat.

---

## Cara 1 — Buka tautan pratinjau sesi (paling cepat, sementara)

Kalau Anda sedang berada di sesi Arena ini, dev server sudah berjalan dan punya
alamat publik yang bisa dibuka dari HP:

```
https://5173-ixp5srrha4romp0ji68d6.e2b.app
```

1. Sambungkan HP ke internet (Wi-Fi atau data).
2. Buka tautan di atas dengan **Chrome**.
3. Menu **⋮ → Tambahkan ke layar utama** agar seperti aplikasi.

> Tautan ini hidup selama sesi/sandbox masih berjalan. Kalau ditutup, alamatnya
> tidak bisa diakses lagi — untuk pemakaian sehari-hari pakai Cara 2 atau 3.
> Jangan pakai `localhost:5173` di HP: itu menunjuk ke HP itu sendiri, bukan ke server.

---

## Cara 2 — GitHub Pages (permanen, gratis, tanpa komputer)

Repo sudah disiapkan untuk ini lewat `.github/workflows/pages.yml`.

**Sekali saja, dari browser HP:**

1. Buka `https://github.com/fatimah86-dot/kitab/settings/pages`
2. Bagian **Build and deployment** → **Source** → pilih **GitHub Actions**.
3. Buka tab **Actions** → workflow **Publikasikan aplikasi kitab** → **Run workflow**
   (atau cukup tunggu, workflow berjalan otomatis setiap ada perubahan di `kitab-app/`).
4. Setelah selesai (±2 menit), alamatnya:

   ```
   https://fatimah86-dot.github.io/kitab/
   ```

5. Di Chrome: **⋮ → Tambahkan ke layar utama** → muncul ikon, terbuka seperti aplikasi.

Workflow ini juga menjalankan `npm run check`, jadi situs hanya terbit kalau
data 65 halaman dan semua lapis lolos pemeriksaan.

---

## Cara 3 — Satu berkas HTML, bisa offline (tanpa internet)

Berkas `kitab-app/unduh/kitab-asrar.html` (±2,7 MB) sudah memuat **semua** isi:
teks 65 halaman, tabel wafaq, Arabiyah Center, font Arab, dan gambar sampul —
tanpa perlu koneksi setelah diunduh.

1. Di HP, buka:
   `https://github.com/fatimah86-dot/kitab/blob/arena/77a8dfc7-kitab/kitab-app/unduh/kitab-asrar.html`
2. Tekan tombol **Download raw file** (ikon unduh di kanan atas berkas).
3. Buka **Files / Pengelola Berkas** → folder **Download** → ketuk berkas
   `kitab-asrar.html` → pilih **Chrome**.
   (Kalau yang terbuka hanya kode teks, ganti namanya dulu menjadi
   `kitab-asrar.html` lalu buka lagi dari pengelola berkas.)
4. Bookmark halaman itu, atau **⋮ → Tambahkan ke layar utama**.

Membangun ulang berkas ini di komputer:

```sh
cd kitab-app
npm install
npm run standalone     # menghasilkan unduh/kitab-asrar.html
```

---

## Kalau masih tidak bisa dibuka

| Gejala | Penyebab & solusi |
|---|---|
| “Site can’t be reached” pada `localhost:5173` | `localhost` di HP menunjuk ke HP itu sendiri. Pakai Cara 1 (tautan pratinjau) atau Cara 2. |
| Halaman putih kosong | Berkas terunduh rusak/terpotong. Unduh ulang, atau pakai Cara 1/2. |
| Yang terbuka malah kode HTML | Berkas dibuka dari tautan “raw” di browser. Unduh dulu, lalu buka dari pengelola berkas (Cara 3). |
| Halaman 404 di `github.io/kitab` | Pages belum diaktifkan atau workflow belum selesai. Cek tab **Actions**. |
| Font Arab terlihat biasa | Font ikut di dalam berkas; kalau memakai Cara 2, tunggu sekali muat. |
| Tombol “Tambahkan ke layar utama” tidak ada | Gunakan Chrome (bukan browser bawaan/WebView). |

## Catatan pemakaian di HP

- Tema, ukuran huruf, penanda halaman, dan riwayat baca disimpan di perangkat
  (`localStorage`), jadi tetap ada saat aplikasi dibuka lagi.
- Arabiyah Center berjalan sepenuhnya lokal — tidak mengirim teks ke mana pun.
- Tombol cetak memakai dialog cetak Chrome Android (bisa “Simpan sebagai PDF”).
