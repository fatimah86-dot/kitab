import { useEffect, useMemo, useState } from 'react';
import { Search as SearchIcon, Close } from './Icons.jsx';
import { SUGGESTIONS, searchPages } from '../lib/search.js';
import { findRanges } from '../lib/text.js';

function Highlighted({ text, query }) {
  const parts = useMemo(() => {
    const ranges = findRanges(text, query);
    if (!ranges.length) return [text];
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
  return parts;
}

export default function SearchView({ initialQuery, onOpen, onQueryChange }) {
  const [q, setQ] = useState(initialQuery || '');
  useEffect(() => setQ(initialQuery || ''), [initialQuery]);

  // debounce ringan agar tidak menyaring tiap ketukan
  const [debounced, setDebounced] = useState(q);
  useEffect(() => {
    const t = setTimeout(() => {
      setDebounced(q);
      onQueryChange?.(q);
    }, 180);
    return () => clearTimeout(t);
  }, [q, onQueryChange]);

  const results = useMemo(() => searchPages(debounced), [debounced]);
  const ready = debounced.trim().length >= 2;

  return (
    <div className="wrap narrow" style={{ paddingTop: 24, paddingBottom: 40 }}>
      <div className="section-head">
        <div>
          <h2>Pencarian kitab</h2>
          <p>Telusuri seluruh 65 halaman pada kelima lapis, termasuk tabel wafaq.</p>
        </div>
      </div>

      <div className="search-box">
        <SearchIcon size={18} />
        <input
          autoFocus
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Mis. wafaq, khadim, istinzal, qarin…"
          aria-label="Kata kunci pencarian"
        />
        {q && (
          <button className="icon-btn" onClick={() => setQ('')} aria-label="Bersihkan">
            <Close size={16} />
          </button>
        )}
      </div>

      <div className="tabs" style={{ marginTop: 12 }}>
        {SUGGESTIONS.map((s) => (
          <button key={s} className="tab" onClick={() => setQ(s)}>
            {s}
          </button>
        ))}
      </div>

      {!ready && (
        <div className="empty">
          <div className="big">Ketik minimal dua huruf</div>
          <p>Pencarian mencakup judul, teks Arab, transliterasi, terjemahan, syarah, dan tuntunan praktik.</p>
        </div>
      )}

      {ready && (
        <div style={{ marginTop: 16, color: 'var(--muted)', fontSize: '0.82rem' }}>
          {results.length ? `${results.length} halaman cocok dengan “${debounced.trim()}”` : 'Tidak ada hasil.'}
        </div>
      )}

      <div className="results">
        {results.map(({ page, hits }) => (
          <article className="result" key={page.id} onClick={() => onOpen(page.num)} tabIndex={0} role="button"
            onKeyDown={(e) => (e.key === 'Enter' ? onOpen(page.num) : null)}>
            <div className="result-head">
              <span className="n">HAL {page.label}</span>
              <span className="t">{page.titleDisplay}</span>
              <span className="ar" lang="ar" dir="rtl">
                {page.titleArabic.replace(/\s*—\s*.*$/, '')}
              </span>
            </div>
            {hits.slice(0, 2).map((h) => (
              <div className={`hit${h.layer === 'arab' ? ' is-ar' : ''}`} key={h.layer}>
                <div className="lay">{h.label}</div>
                <p>
                  <Highlighted text={h.snippet} query={debounced} />
                </p>
              </div>
            ))}
          </article>
        ))}
      </div>
    </div>
  );
}
