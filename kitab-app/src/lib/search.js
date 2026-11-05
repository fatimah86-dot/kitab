/* Indeks pencarian ringan di sisi klien (65 halaman, tanpa server). */
import { norm, snippet } from './text.js';
import kitab from '../data/kitab.json';

const index = kitab.pages.map((p) => ({
  page: p,
  haystack: norm(`${p.titleDisplay} ${p.titleArabic} ${p.section} ${p.text}`),
  layerText: {
    arab: norm(textOfLayer(p, 'arab')),
    latin: norm(textOfLayer(p, 'latin')),
    terjemahan: norm(textOfLayer(p, 'terjemahan')),
    syarah: norm(textOfLayer(p, 'syarah')),
    khususiyah: norm(textOfLayer(p, 'khususiyah')),
  },
}));

function textOfLayer(p, key) {
  const blocks = p.layers[key]?.blocks || [];
  return blocks
    .map((b) => (b.type === 'table' ? b.head.concat(...b.rows).join(' ') : b.type === 'ol' || b.type === 'ul' ? b.items.join(' ') : b.text || ''))
    .join(' ');
}

const LAYER_LABEL = { arab: 'Arab', latin: 'Latin', terjemahan: 'Terjemahan', syarah: 'Syarah', khususiyah: 'Khususiyah' };

/**
 * Cari di seluruh lapis. Query dipecah per kata; semua kata harus muncul (AND).
 * @returns {{page, score, hits: {layer,label,snippet}[]}[]}
 */
export function searchPages(query, { limit = 40 } = {}) {
  const q = norm(query);
  if (!q || q.length < 2) return [];
  const words = q.split(' ').filter(Boolean);
  const results = [];

  for (const entry of index) {
    if (!words.every((w) => entry.haystack.includes(w))) continue;
    const hits = [];
    let score = 0;
    for (const [layer, text] of Object.entries(entry.layerText)) {
      if (!text) continue;
      const matches = words.filter((w) => text.includes(w)).length;
      if (!matches) continue;
      score += matches * (layer === 'terjemahan' ? 3 : layer === 'arab' ? 2 : 1);
      hits.push({
        layer,
        label: LAYER_LABEL[layer],
        snippet: snippet(textOfLayer(entry.page, layer), query),
      });
    }
    if (norm(entry.page.titleDisplay).includes(q) || norm(entry.page.titleArabic).includes(q)) score += 10;
    results.push({ page: entry.page, score, hits });
  }

  return results.sort((a, b) => b.score - a.score || a.page.num - b.page.num).slice(0, limit);
}

/** Daftar istilah yang sering muncul untuk saran pencarian. */
export const SUGGESTIONS = ['wafaq', 'khadim', 'istinzal', 'hizib', 'huruf nuraniyyah', 'asma', 'riyadhah', 'tadmir zhalim', 'qarin', 'mimpi'];
