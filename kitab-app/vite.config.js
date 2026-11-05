import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: false,
    // Preview Arena memakai host berbasis port; izinkan semua host/origin.
    allowedHosts: true,
    cors: true,
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    allowedHosts: true,
  },
  build: {
    target: 'es2020',
    // `STANDALONE=1` (dipakai scripts/build-standalone.mjs) menaruh semua aset
    // di dalam JS/CSS agar hasilnya bisa di-inline menjadi satu berkas HTML.
    assetsInlineLimit: process.env.STANDALONE ? 100_000_000 : 4096,
    cssCodeSplit: !process.env.STANDALONE,
    chunkSizeWarningLimit: 4000,
  },
});
