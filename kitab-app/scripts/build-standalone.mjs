#!/usr/bin/env node
/**
 * build-standalone.mjs
 * Membangun SATU berkas HTML mandiri yang bisa dibuka langsung di Chrome Android
 * tanpa server, tanpa internet, dan tanpa install.
 *
 * Semua JS, CSS, font, dan gambar sampul di-inline ke dalam satu berkas
 * `unduh/kitab-asrar.html`.
 *
 * Jalankan: npm run standalone
 */
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(here, '..');
const dist = path.join(appDir, 'dist');
const outDir = path.join(appDir, 'unduh');
const outFile = path.join(outDir, 'kitab-asrar.html');

const log = (m) => console.log(m);
const kb = (n) => `${(n / 1024 / 1024).toFixed(2)} MB`;

// 1. Build Vite dengan semua aset di-inline ke CSS/JS.
log('▸ membangun bundel (aset di-inline)…');
execSync('npx vite build --logLevel warn', {
  cwd: appDir,
  stdio: 'inherit',
  env: { ...process.env, STANDALONE: '1' },
});

let html = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');

// 2. Inline setiap <link rel="stylesheet"> dan <script src>.
html = html.replace(/<link[^>]+rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/g, (m, href) => {
  const file = path.join(dist, href.replace(/^\.\//, ''));
  if (!fs.existsSync(file)) return m;
  return `<style>\n${fs.readFileSync(file, 'utf8')}\n</style>`;
});

html = html.replace(/<script([^>]*)\ssrc="([^"]+)"([^>]*)><\/script>/g, (m, pre, src, post) => {
  const file = path.join(dist, src.replace(/^\.\//, ''));
  if (!fs.existsSync(file)) return m;
  const code = fs.readFileSync(file, 'utf8').replace(/<\/script>/gi, '<\\/script>');
  return `<script${pre}${post}>\n${code}\n</script>`;
});

// 3. Inline gambar sampul (public/art/sampul.jpg) sebagai data URI.
const cover = path.join(dist, 'art', 'sampul.jpg');
if (fs.existsSync(cover)) {
  const uri = `data:image/jpeg;base64,${fs.readFileSync(cover).toString('base64')}`;
  html = html.replaceAll('./art/sampul.jpg', uri).replaceAll('art/sampul.jpg', uri);
} else {
  console.warn('⚠ sampul tidak ditemukan di dist/art/sampul.jpg');
}

// 4. Tambahkan manifest PWA inline + meta agar bisa "Tambahkan ke layar utama".
const manifest = {
  name: 'Asrār Rūḥāniyyah — Pembaca 5 Lapis',
  short_name: 'Asrār Rūḥāniyyah',
  start_url: '.',
  display: 'standalone',
  background_color: '#f6f1e6',
  theme_color: '#0b3b33',
  orientation: 'portrait-primary',
  icons: [
    {
      src:
        'data:image/svg+xml,' +
        encodeURIComponent(
          `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#0b3b33"/><path d="M256 96l53 107 118 14-87 80 24 116-108-55-108 55 24-116-87-80 118-14z" fill="#d9b463"/></svg>`
        ),
      sizes: '512x512',
      type: 'image/svg+xml',
      purpose: 'any maskable',
    },
  ],
};
const manifestUri = `data:application/manifest+json,${encodeURIComponent(JSON.stringify(manifest))}`;
html = html.replace(
  '</head>',
  `    <link rel="manifest" href="${manifestUri}" />\n    <meta name="mobile-web-app-capable" content="yes" />\n    <meta name="apple-mobile-web-app-capable" content="yes" />\n    <meta name="apple-mobile-web-app-status-bar-style" content="default" />\n  </head>`
);

// 5. Catatan kecil di komentar agar jelas berkas ini hasil build.
html = `<!-- Asrār Rūḥāniyyah — berkas mandiri (offline). Dibangun ${new Date().toISOString().slice(0, 10)}. -->\n${html}`;

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outFile, html);

const size = fs.statSync(outFile).size;
log(`✔ ${path.relative(appDir, outFile)} (${kb(size)})`);
log('  Buka berkas ini di Chrome Android → menu ⋮ → “Tambahkan ke layar utama”.');
