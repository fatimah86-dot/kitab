#!/usr/bin/env node
/**
 * check.mjs — uji cepat data & perilaku inti (tanpa browser).
 * 1. Data: 65 halaman, tiap halaman punya 5 lapis berisi teks.
 * 2. Pencarian: istilah tertentu menemukan halaman yang benar.
 * 3. Render: semua blok tiap halaman dapat dirender React (SSR) tanpa error.
 */
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><html><body></body></html>', { url: 'http://localhost/' });
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
globalThis.HTMLElement = dom.window.HTMLElement;
globalThis.localStorage = dom.window.localStorage;
globalThis.location = dom.window.location;

// esbuild menangani impor JSON saat membundel skrip ini.
import data from '../src/data/kitab.json';
const { searchPages, SUGGESTIONS } = await import('../src/lib/search.js');
const React = (await import('react')).default;
const { renderToString } = await import('react-dom/server');
const Blocks = (await import('../src/components/Blocks.jsx')).default;

let fail = 0;
const ok = (cond, msg) => {
  if (!cond) {
    fail += 1;
    console.error('  ✗ ' + msg);
  } else {
    console.log('  ✓ ' + msg);
  }
};

console.log('Data');
ok(data.pages.length === 65, `65 halaman terparse (dapat ${data.pages.length})`);
ok(data.meta.layers.length === 5, '5 lapis terdaftar');
const keys = ['arab', 'latin', 'terjemahan', 'syarah', 'khususiyah'];
let emptyLayer = [];
for (const p of data.pages) {
  for (const k of keys) if (!p.layers[k]?.blocks?.length) emptyLayer.push(`${p.num}/${k}`);
}
ok(emptyLayer.length === 0, `semua lapis berisi (kosong: ${emptyLayer.join(', ') || 'tidak ada'})`);
ok(data.pages.every((p) => p.titleDisplay && p.titleArabic), 'semua halaman punya judul Latin & Arab');
ok(data.pages.filter((p) => p.hasTable).length === 15, '15 halaman memuat tabel wafaq');
const totalTables = data.pages.reduce((n, p) => n + keys.reduce((m, k) => m + p.layers[k].tables, 0), 0);
ok(totalTables >= 15, `total tabel wafaq: ${totalTables}`);
ok(data.pages.every((p) => p.words > 5), 'setiap halaman punya isi teks bermakna');

console.log('Pencarian');
const cases = [
  ['wafaq', 8],
  ['istinzal', 13],
  ['qarin', 21],
  ['tadmir', 19],
  ['khadim sufli', 55],
];
for (const [q, expectPage] of cases) {
  const res = searchPages(q);
  ok(res.length > 0, `“${q}” menghasilkan ${res.length} halaman`);
  ok(
    res.some((r) => r.page.num === expectPage),
    `“${q}” menemukan halaman ${expectPage}`
  );
}
ok(searchPages('a').length === 0, 'query satu huruf tidak dijalankan');
for (const s of SUGGESTIONS) ok(searchPages(s).length >= 0, `saran “${s}” dapat diproses`);

console.log('Render blok');
let renderedPages = 0;
for (const p of data.pages) {
  for (const k of keys) {
    const html = renderToString(React.createElement(Blocks, { blocks: p.layers[k].blocks, query: 'wafaq' }));
    if (!html) throw new Error(`render kosong: ${p.num}/${k}`);
    if (html.includes('**') || html.includes('`')) {
      fail += 1;
      console.error(`  ✗ markup mentah tampil di halaman ${p.num}/${k}`);
      break;
    }
    if (/^#+\s/m.test(html)) {
      fail += 1;
      console.error(`  ✗ judul markdown mentah di halaman ${p.num}/${k}`);
      break;
    }
  }
  renderedPages += 1;
}
ok(renderedPages === 65, `65 halaman dirender (5 lapis × 65)`);
const wafqHtml = renderToString(React.createElement(Blocks, { blocks: data.pages.find((p) => p.hasTable).layers.arab.blocks }));
ok(wafqHtml.includes('class="wafaq'), 'tabel wafaq dirender sebagai kotak wafaq');

console.log('Arabiyah Center');
const { FEATURES, ARABIC_KEYS, generateSmartResponse } = await import('../src/lib/arabiyah.js');
ok(FEATURES.length === 6, '6 mode belajar terdaftar');
ok(ARABIC_KEYS.length === 32, '32 tombol keyboard hijaiyah');
ok(FEATURES.every((f) => f.sample && f.title && f.subtitle), 'setiap mode punya contoh & deskripsi');
for (const f of FEATURES) {
  const res = generateSmartResponse(f.sample, f);
  ok(res.startsWith(`MODE ${f.title}`), `respons mode ${f.id} berawalan penanda mode`);
  ok(res.includes(f.sample) || f.id === 'kamus', `respons mode ${f.id} mengutip teks masukan`);
  ok(res.includes('Gunakan uraian ini sebagai pendamping belajar'), `respons mode ${f.id} memuat panduan belajar`);
}
const cancer = generateSmartResponse(FEATURES[0].sample, FEATURES[0]);
ok(cancer.includes("nā'ib al-fā'il"), 'contoh khusus kanker memuat analisis naib fa il');
ok(generateSmartResponse('   ', FEATURES[1]).includes('MODE'), 'masukan kosong tidak membuat respons rusak');
const { default: Arabiyah } = await import('../src/components/Arabiyah.jsx');
const arabiyahHtml = renderToString(React.createElement(Arabiyah, { page: data.pages[0], onOpenPage: () => {} }));
ok(arabiyahHtml.includes('PUSAT PEMBELAJARAN BAHASA ARAB'), 'komponen Arabiyah dirender');
ok(arabiyahHtml.includes('Dari kitab'), 'komponen Arabiyah memakai konteks halaman kitab');

console.log(fail ? `\n${fail} pemeriksaan GAGAL` : '\nSemua pemeriksaan lulus');
process.exit(fail ? 1 : 0);
