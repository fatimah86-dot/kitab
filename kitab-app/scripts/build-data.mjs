#!/usr/bin/env node
/**
 * build-data.mjs
 * Mengubah master `REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md` menjadi
 * `src/data/kitab.json` yang dipakai aplikasi pembaca.
 *
 * Sumber tunggal: berkas master. Tidak ada teks yang ditulis ulang di sini —
 * parser hanya memecah struktur (judul, 5 lapis, tabel wafaq, daftar) dan
 * menyimpan seluruh isi apa adanya.
 *
 * Jalankan: node kitab-app/scripts/build-data.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..'); // root repo kitab
const SRC = process.env.KITAB_MASTER
  ? path.resolve(process.env.KITAB_MASTER)
  : path.join(root, 'REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md');
const OUT_DIR = path.join(here, '..', 'src', 'data');
const OUT = path.join(OUT_DIR, 'kitab.json');

const LAYER_KEYS = {
  arab: 'arab',
  latin: 'latin',
  terjemahan: 'terjemahan',
  'syarah dan penjelasan': 'syarah',
  'khususiyah dan tatacara praktik': 'khususiyah',
};

const LAYER_META = [
  { key: 'arab', label: 'Arab', short: 'AR', dir: 'rtl', lang: 'ar' },
  { key: 'latin', label: 'Latin', short: 'LT', dir: 'ltr', lang: 'id' },
  { key: 'terjemahan', label: 'Terjemahan', short: 'TR', dir: 'ltr', lang: 'id' },
  { key: 'syarah', label: 'Syarah dan Penjelasan', short: 'SY', dir: 'ltr', lang: 'id' },
  { key: 'khususiyah', label: 'Khususiyah dan Tatacara Praktik', short: 'KH', dir: 'ltr', lang: 'id' },
];

// Peta judul Latin & bagian, disusun dari preview HTML yang sudah ada di repo
// (judul Latin tiap halaman) agar daftar isi mudah dipindai.
function loadTitles() {
  const file = path.join(here, 'titles.txt');
  const map = new Map();
  if (!fs.existsSync(file)) return map;
  for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
    const [num, latin, section] = line.split('|');
    if (!num || !latin) continue;
    map.set(Number(num), { latin: latin.trim(), section: (section || '').trim() });
  }
  return map;
}

const TITLES = loadTitles();

const clean = (s) =>
  s
    .replace(/\u200f/g, '') // RLM
    .replace(/\u200e/g, '') // LRM
    .replace(/\u00a0/g, ' ')
    .trim();

/** Pisahkan blok paragraf dengan baris kosong, tapi jaga baris berurutan sebagai satu blok. */
function toBlocks(raw) {
  const lines = raw.split('\n');
  const blocks = [];
  let buf = [];
  let kind = null;

  const flush = () => {
    if (!buf.length) return;
    blocks.push({ type: kind, lines: buf.slice() });
    buf = [];
    kind = null;
  };

  for (const line of lines) {
    const t = clean(line);
    if (!t) {
      flush();
      continue;
    }
    let nextKind;
    if (/^\|/.test(t)) nextKind = 'table';
    else if (/^#{4,}\s/.test(t)) nextKind = 'heading';
    else if (/^\d+[.)]\s/.test(t)) nextKind = 'ol';
    else if (/^[-*]\s/.test(t)) nextKind = 'ul';
    else nextKind = 'p';

    // tabel: biarkan semua baris tabel menyatu
    if (kind && kind !== nextKind && !(kind === 'table' && nextKind === 'table')) flush();
    kind = nextKind;
    buf.push(line.replace(/\u200f/g, '').replace(/^\uFEFF/, ''));
  }
  flush();
  return blocks;
}

function parseTable(lines) {
  const rows = lines
    .map((l) => clean(l))
    .filter(Boolean)
    .map((l) =>
      l
        .replace(/^\|/, '')
        .replace(/\|$/, '')
        .split('|')
        .map((c) => c.trim())
    );
  const body = rows.filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c)));
  if (!body.length) return null;
  return { type: 'table', head: body[0], rows: body.slice(1) };
}

/** Ubah blok markdown sederhana jadi model kecil yang dirender React. */
function renderBlocks(raw, { stripTable = false } = {}) {
  const out = [];
  for (const b of toBlocks(raw || '')) {
    if (b.type === 'table') {
      const t = parseTable(b.lines);
      if (t && !stripTable) out.push(t);
      continue;
    }
    if (b.type === 'heading') {
      out.push({ type: 'h', text: clean(b.lines.join(' ')).replace(/^#+\s*/, '') });
      continue;
    }
    if (b.type === 'ol' || b.type === 'ul') {
      const items = b.lines.map((l) => clean(l)).filter(Boolean);
      out.push({ type: b.type === 'ol' ? 'ol' : 'ul', items });
      continue;
    }
    const text = b.lines.map((l) => clean(l)).filter(Boolean).join('\n');
    if (text) out.push({ type: 'p', text });
  }
  return out;
}

function plainText(raw) {
  // Untuk indeks pencarian: buang markup ringan, gabung jadi satu baris.
  return clean(
    (raw || '')
      .replace(/\|/g, ' ')
      .replace(/`/g, '')
      .replace(/\*\*/g, '')
      .replace(/^\s*[-*]\s+/gm, '')
      .replace(/\s+/g, ' ')
  );
}

/** Deteksi apakah lapis memuat wafaq (tabel huruf/angka). */
function tableInfo(blocks) {
  const tables = blocks.filter((b) => b.type === 'table');
  return { tables: tables.length, hasTable: tables.length > 0 };
}

function parseMaster(md) {
  const lines = md.split('\n');
  const pages = [];
  let cur = null;
  let bucket = null;
  let buf = [];

  const pushBuf = () => {
    if (cur && bucket) cur.raw[bucket] = (cur.raw[bucket] ? cur.raw[bucket] + '\n\n' : '') + buf.join('\n');
    buf = [];
  };
  const finish = () => {
    pushBuf();
    if (!cur) return;
    pages.push(cur);
    cur = null;
    bucket = null;
  };

  for (const line of lines) {
    const h2 = line.match(/^##\s+HALAMAN\s+(\d+)\s*[—–-]\s*(.*)$/);
    const h3 = line.match(/^###\s+(.*)$/);
    if (h2) {
      finish();
      const num = h2[1];
      const title = clean(h2[2]);
      // Judul berformat: `judul arab — judul latin`. Pisahkan pada pemisah pertama.
      let arabPart = title;
      let latinPart = '';
      const sep = title.search(/\s[—–]\s/);
      if (sep > 0) {
        arabPart = clean(title.slice(0, sep));
        latinPart = clean(title.slice(sep + 3));
      }
      cur = {
        id: `hal-${num}`,
        num: Number(num),
        label: num,
        titleArabic: arabPart,
        titleLatin: latinPart,
        raw: {},
      };
      bucket = null;
      continue;
    }
    if (cur && h3) {
      pushBuf();
      const name = clean(h3[1]).toLowerCase();
      bucket = LAYER_KEYS[name] || null;
      if (bucket) cur.raw[bucket] = cur.raw[bucket] || '';
      continue;
    }
    if (cur && bucket) buf.push(line);
  }
  finish();

  return pages.map((p) => {
    const layers = {};
    const indexParts = [];
    for (const meta of LAYER_META) {
      const raw = p.raw[meta.key] || '';
      const blocks = meta.key === 'syarah' || meta.key === 'khususiyah' ? renderBlocks(raw) : renderBlocks(raw);
      // Lapis Arab/Latin/Terjemahan tidak ditampilkan tabelnya (tabel wafaq
      // hanya disajikan sekali di lapis Arab? -> master menyimpan tabel di
      // lapis yang memang memuatnya; kita pertahankan pada lapis tersebut).
      const info = tableInfo(blocks);
      layers[meta.key] = { ...meta, blocks, ...info };
      indexParts.push(plainText(raw));
      if (raw.includes('Rajah Huruf')) layers[meta.key].hasRajahNote = true;
    }
    const extra = TITLES.get(p.num) || {};
    const title = extra.latin || p.titleLatin || p.titleArabic;
    return {
      id: p.id,
      num: p.num,
      label: p.label,
      titleArabic: p.titleArabic,
      titleLatin: p.titleLatin,
      title,
      titleDisplay: extra.latin || p.titleLatin || '',
      section: extra.section || '',
      layers,
      text: plainText(`${p.titleLatin} ${p.titleArabic} ${indexParts.join(' ')}`),
      hasTable: LAYER_META.some((m) => layers[m.key].hasTable),
      words: plainText(indexParts.join(' ')).split(/\s+/).filter(Boolean).length,
    };
  });
}

const md = fs.readFileSync(SRC, 'utf8');
const pages = parseMaster(md);

if (pages.length !== 65) {
  console.error(`PERINGATAN: jumlah halaman terparse ${pages.length}, diharapkan 65.`);
}
for (const p of pages) {
  for (const m of LAYER_META) {
    if (!p.layers[m.key].blocks.length) console.error(`PERINGATAN: ${p.id} lapis ${m.key} kosong.`);
  }
}

const data = {
  meta: {
    title: 'Asrār Rūḥāniyyah',
    titleArabic: 'أَسْرَارُ الرُّوحَانِيَّة',
    subtitle: 'Pembaca 5 lapis — Arab · Latin · Terjemahan · Syarah · Khususiyah',
    source: path.basename(SRC),
    sourceBytes: Buffer.byteLength(md),
    builtAt: new Date().toISOString().slice(0, 10),
    pages: pages.length,
    layers: LAYER_META.map(({ key, label, short }) => ({ key, label, short })),
    missingFolios: [14, 36, 37, 40, 48, 56, 62, 72],
    notice:
      'Teks disalin apa adanya dari master editorial 5 lapis. Klaim khasiat dan perkara gaib di dalamnya merupakan isi tradisi/naskah, bukan bukti medis atau jaminan hasil.',
  },
  pages,
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(data));
const kb = (fs.statSync(OUT).size / 1024).toFixed(0);
console.log(`✔ ${pages.length} halaman → ${path.relative(root, OUT)} (${kb} KB)`);
console.log(`  lapis per halaman: ${LAYER_META.length} · tabel wafaq pada ${pages.filter((p) => p.hasTable).length} halaman`);
