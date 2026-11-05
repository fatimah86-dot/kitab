import { useMemo } from 'react';
import { findRanges, tokenize, RAJAH_NOTE } from '../lib/text.js';

/** Sorot semua kemunculan query pada teks. */
function Highlight({ text, query }) {
  const parts = useMemo(() => {
    const ranges = query ? findRanges(text, query) : [];
    if (!ranges.length) return null;
    const out = [];
    let last = 0;
    for (const [s, e] of ranges) {
      if (s > last) out.push(text.slice(last, s));
      out.push(<mark key={`${s}-${e}`}>{text.slice(s, e)}</mark>);
      last = e;
    }
    if (last < text.length) out.push(text.slice(last));
    return out;
  }, [text, query]);

  if (!parts) return text;
  return parts;
}

/** Inline: tebal, miring, kode, dan penanda rajah. */
function renderToken(tok, query, key) {
  if (tok.t === 'code') return <code key={key}>{tok.v}</code>;

  // Pisahkan penanda rajah agar tampil sebagai label, bukan teks mentah.
  const chunks = tok.v.split(RAJAH_NOTE);
  let inner = chunks.map((chunk, j) => (
    <span key={j}>
      <Highlight text={chunk} query={query} />
      {j < chunks.length - 1 && <span className="rajah-note">Rajah huruf — lihat scan</span>}
    </span>
  ));
  if (tok.bold) inner = <strong key={`b${key}`}>{inner}</strong>;
  if (tok.italic) inner = <em key={`i${key}`}>{inner}</em>;
  return <span key={key}>{inner}</span>;
}

function Inline({ text, query }) {
  const tokens = useMemo(() => tokenize(text), [text]);
  return tokens.map((tok, i) => renderToken(tok, query, i));
}

function isNumericCell(cells) {
  return cells.every((c) => /^[\d٠-٩\s.,/×+-]+$/.test(c)) && cells.some((c) => /\d|[\u0660-\u0669]/.test(c));
}

/** Tabel wafaq: kotak huruf/angka, arah RTL, tanpa header terpisah. */
export function WafaqTable({ head, rows, query, index = 0 }) {
  const all = [head, ...rows];
  const cols = Math.max(...all.map((r) => r.length));
  const big = all.length > 6 || cols > 6;
  const numeric = isNumericCell(all.flat());
  const cellText = (c) => c;

  return (
    <div className="wafaq-wrap">
      <div className="wafaq-cap">
        <span>Wafaq · {all.length} × {cols}{numeric ? ' · angka' : ' · huruf'}</span>
        <span className="line" />
      </div>
      <div
        className={`wafaq${big ? ' many' : ''}`}
        style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}
        role="table"
        aria-label={`Tabel wafaq ${index + 1}, ${all.length} baris ${cols} kolom`}
      >
        {all.flatMap((row, r) =>
          Array.from({ length: cols }, (_, c) => (
            <div key={`${r}-${c}`} className={`cell${numeric ? ' num' : ''}`} role="cell">
              {row[c] ? <Highlight text={cellText(row[c])} query={query} /> : ''}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

/** Render seluruh blok pada satu lapis. */
export default function Blocks({ blocks, query }) {
  let tableIndex = 0;
  return blocks.map((b, i) => {
    if (b.type === 'h') {
      return (
        <p key={i} style={{ fontWeight: 650, color: 'var(--ink)', margin: '0 0 0.6em' }}>
          <Inline text={b.text} query={query} />
        </p>
      );
    }
    if (b.type === 'table') {
      tableIndex += 1;
      return <WafaqTable key={i} head={b.head} rows={b.rows} query={query} index={tableIndex - 1} />;
    }
    if (b.type === 'ol' || b.type === 'ul') {
      const Tag = b.type;
      return (
        <Tag key={i}>
          {b.items.map((item, j) => {
            const m = b.type === 'ol' ? item.match(/^(\d+)[.)]\s*(.*)$/) : null;
            return (
              <li key={j} value={m ? Number(m[1]) : undefined}>
                <Inline text={m ? m[2] : item} query={query} />
              </li>
            );
          })}
        </Tag>
      );
    }
    return (
      <p key={i}>
        <Inline text={b.text} query={query} />
      </p>
    );
  });
}
