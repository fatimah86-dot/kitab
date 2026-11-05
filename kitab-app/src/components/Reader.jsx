import { useEffect, useMemo, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Copy, Bookmark, ArrowLeft, Check, Print, Layers as LayersIcon, Sparkle } from './Icons.jsx';
import Blocks from './Blocks.jsx';
import { stripInline, tidy } from '../lib/text.js';

const LAYER_ORDER = ['arab', 'latin', 'terjemahan', 'syarah', 'khususiyah'];

export default function Reader({
  page,
  pages,
  prefs,
  onNavigate,
  onBack,
  onOpenToc,
  isBookmarked,
  onToggleBookmark,
  onToggleLayer,
  onStudy,
  query,
}) {
  const prev = pages.find((p) => p.num === page.num - 1);
  const next = pages.find((p) => p.num === page.num + 1);
  const [copied, setCopied] = useState(false);
  const topRef = useRef(null);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
  }, [page.num]);

  useEffect(() => {
    const onKey = (e) => {
      if (e.target instanceof HTMLElement && /input|textarea/i.test(e.target.tagName)) return;
      if (e.key === 'ArrowLeft' && prev) onNavigate(prev.num);
      if (e.key === 'ArrowRight' && next) onNavigate(next.num);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [prev, next, onNavigate]);

  const copyPage = async () => {
    const parts = [`${page.titleDisplay} (Halaman ${page.label})`, page.titleArabic, ''];
    for (const key of LAYER_ORDER) {
      if (!prefs.layers[key]) continue;
      const layer = page.layers[key];
      const body = layer.blocks
        .map((b) => {
          if (b.type === 'table') return [b.head, ...b.rows].map((r) => r.join(' | ')).join('\n');
          if (b.type === 'ol' || b.type === 'ul') return b.items.join('\n');
          return stripInline(b.text || '');
        })
        .join('\n\n');
      parts.push(`— ${layer.label} —`, body, '');
    }
    try {
      await navigator.clipboard.writeText(parts.join('\n'));
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard ditolak browser */
    }
  };

  const visibleLayers = LAYER_ORDER.filter((k) => prefs.layers[k]);
  const totalTables = useMemo(
    () => page.layers.arab.tables + page.layers.latin.tables + page.layers.terjemahan.tables + page.layers.syarah.tables + page.layers.khususiyah.tables,
    [page]
  );

  return (
    <div className="reader wrap narrow" ref={topRef}>
      <div className="reader-head">
        <div className="badge" aria-hidden="true">
          {page.label}
        </div>
        <div className="reader-title">
          <div className="eyebrow">
            Halaman {page.label} · {page.section || 'Kitab'}
            {totalTables ? ` · ${totalTables} tabel wafaq` : ''}
          </div>
          <h1>{page.titleDisplay || page.titleLatin || `Halaman ${page.label}`}</h1>
          <p className="ar" lang="ar" dir="rtl">
            {tidy(page.titleArabic)}
          </p>
        </div>
        <div className="reader-tools">
          <button className="icon-btn" onClick={onOpenToc} title="Daftar isi" aria-label="Daftar isi">
            <LayersIcon />
          </button>
          <button
            className="icon-btn"
            aria-pressed={isBookmarked}
            onClick={onToggleBookmark}
            title={isBookmarked ? 'Hapus penanda' : 'Tandai halaman'}
            aria-label={isBookmarked ? 'Hapus penanda' : 'Tandai halaman'}
          >
            <Bookmark filled={isBookmarked} />
          </button>
          <button className="icon-btn" onClick={copyPage} title="Salin halaman" aria-label="Salin halaman">
            {copied ? <Check /> : <Copy />}
          </button>
          <button className="icon-btn" onClick={() => window.print()} title="Cetak" aria-label="Cetak">
            <Print />
          </button>
          <button
            className="icon-btn"
            onClick={() => onStudy?.(page.num)}
            title="Belajar halaman ini di Arabiyah Center"
            aria-label="Belajar halaman ini di Arabiyah Center"
          >
            <Sparkle />
          </button>
        </div>
      </div>

      <div className="layer-bar">
        {LAYER_ORDER.filter((k) => page.layers[k].blocks.length).map((key) => {
          const meta = page.layers[key];
          return (
            <button
              key={key}
              className="layer-pill"
              aria-pressed={!!prefs.layers[key]}
              onClick={() => onToggleLayer(key)}
              title={`${prefs.layers[key] ? 'Sembunyikan' : 'Tampilkan'} lapis ${meta.label}`}
            >
              <span className="dot">{meta.short}</span>
              {meta.label}
            </button>
          );
        })}
        <div className="layer-actions">
          <button className="btn small ghost" onClick={() => onBack()}>
            <ArrowLeft size={15} /> Daftar
          </button>
        </div>
      </div>

      {visibleLayers.map((key) => {
        const layer = page.layers[key];
        if (!layer.blocks.length) return null;
        return (
          <section className="layer" data-layer={key} key={key} aria-labelledby={`layer-${key}`}>
            <header>
              <span className={`chip ${key === 'arab' ? 'green' : ''}`}>{layer.short}</span>
              <h2 id={`layer-${key}`}>{layer.label}</h2>
              <span className="line" />
            </header>
            <div className="body" dir={layer.dir} lang={layer.lang}>
              <Blocks blocks={layer.blocks} query={query} />
            </div>
          </section>
        );
      })}

      {!visibleLayers.length && (
        <div className="empty">
          <div className="big">Semua lapis disembunyikan</div>
          <p>Aktifkan minimal satu lapis pada bilah di atas.</p>
        </div>
      )}

      <nav className="pager" aria-label="Navigasi halaman">
        <button onClick={() => prev && onNavigate(prev.num)} disabled={!prev}>
          <span className="cap">Sebelumnya</span>
          <span className="lbl">
            {prev ? <><ChevronLeft size={14} style={{ verticalAlign: '-2px' }} /> {prev.titleDisplay || prev.label}</> : 'Awal kitab'}
          </span>
        </button>
        <button className="next" onClick={() => next && onNavigate(next.num)} disabled={!next}>
          <span className="cap">Berikutnya</span>
          <span className="lbl">
            {next ? <>{next.titleDisplay || next.label} <ChevronRight size={14} style={{ verticalAlign: '-2px' }} /></> : 'Akhir kitab'}
          </span>
        </button>
      </nav>
    </div>
  );
}
