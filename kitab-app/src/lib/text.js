/* Utilitas teks: penanda inline, sorotan pencarian, dan penanda "Rajah Huruf". */

export const RAJAH_NOTE = '[Rajah Huruf — tidak diterjemahkan]';

/** Bersihkan penanda editorial yang memang perlu ditampilkan apa adanya. */
export function tidy(text) {
  return String(text ?? '')
    .replace(/\u200f|\u200e/g, '')
    .replace(/[ \t]+$/gm, '')
    .trim();
}

/**
 * Parser markdown-lite. Mengembalikan potongan:
 *  { t:'text', v, bold, italic } | { t:'code', v }
 * Mendukung penanda bertumpuk seperti **tebal *miring* tebal**, ***miring tebal***,
 * dan `kode` — termasuk kasus penutup *** (miring lalu tebal).
 */
export function tokenize(text) {
  const src = tidy(text);
  const out = [];
  let buf = '';
  let bold = false;
  let italic = false;
  const flush = () => {
    if (buf) out.push({ t: 'text', v: buf, bold, italic });
    buf = '';
  };

  let i = 0;
  while (i < src.length) {
    const ch = src[i];
    if (ch === '`') {
      const end = src.indexOf('`', i + 1);
      if (end > i + 1) {
        flush();
        out.push({ t: 'code', v: src.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
    }
    if (ch === '*') {
      let n = 1;
      while (src[i + n] === '*') n += 1;
      if (n >= 3) {
        flush();
        const on = !(bold && italic);
        bold = on;
        italic = on;
        i += n;
        continue;
      }
      if (n === 2) {
        flush();
        bold = !bold;
        i += 2;
        continue;
      }
      const next = src[i + 1] || ' ';
      const prev = src[i - 1] || ' ';
      if (!italic && /\S/.test(next)) {
        flush();
        italic = true;
        i += 1;
        continue;
      }
      if (italic && /\S/.test(prev)) {
        flush();
        italic = false;
        i += 1;
        continue;
      }
    }
    buf += ch;
    i += 1;
  }
  flush();
  return out;
}

export function stripInline(text) {
  return tidy(text)
    .replace(/\*\*/g, '')
    .replace(/`/g, '')
    .replace(/\*([^*\n]+)\*/g, '$1')
    .replace(/\*/g, '');
}

/** Normalisasi untuk pencarian: buang diakritik Latin, samakan bentuk Arab. */
export function norm(s) {
  return String(s ?? '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // diakritik Latin (ā, ī, ḥ, ...)
    .replace(/[\u064b-\u065f\u0670\u06d6-\u06ed]/g, '') // harakat Arab
    .replace(/[إأآا]/g, 'a')
    .replace(/[ىي]/g, 'y')
    .replace(/ة/g, 'h')
    .replace(/[ًٌٍْ]/g, '')
    .replace(/[’'`ʼ]/g, "'")
    .replace(/[^\p{L}\p{N}'\s]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Cari kemunculan query di teks asli; kembalikan rentang [start,end]. */
export function findRanges(text, query) {
  const q = norm(query);
  if (!q) return [];
  // Petakan tiap karakter asli ke posisi pada teks ternormalisasi.
  const map = [];
  let acc = '';
  for (let i = 0; i < text.length; i++) {
    const n = norm(text[i]);
    if (!n) continue;
    for (let k = 0; k < n.length; k++) {
      map.push(i);
      acc += n[k];
    }
    if (n === ' ' || n === ' ') continue;
  }
  const ranges = [];
  let from = 0;
  for (;;) {
    const idx = acc.indexOf(q, from);
    if (idx === -1) break;
    const start = map[idx];
    const end = map[Math.min(idx + q.length - 1, map.length - 1)] + 1;
    ranges.push([start, end]);
    from = idx + q.length;
    if (ranges.length > 300) break;
  }
  return ranges;
}

export function snippet(text, query, radius = 90) {
  const r = findRanges(text, query)[0];
  if (!r) return text.slice(0, radius * 2) + '…';
  const start = Math.max(0, r[0] - radius);
  const end = Math.min(text.length, r[1] + radius);
  return (start > 0 ? '…' : '') + text.slice(start, end).trim() + (end < text.length ? '…' : '');
}

export function formatDate(iso) {
  try {
    return new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
  } catch {
    return iso;
  }
}
