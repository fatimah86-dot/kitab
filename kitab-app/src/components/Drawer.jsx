import { useEffect, useMemo, useRef } from 'react';
import { Close, Search, Star } from './Icons.jsx';

/** Laci daftar isi dengan pengelompokan per bagian. */
export default function Drawer({ open, pages, current, onSelect, onClose, onSearch }) {
  const ref = useRef(null);
  const activeRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    activeRef.current?.scrollIntoView({ block: 'center' });
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [open, onClose]);

  const groups = useMemo(() => {
    const map = new Map();
    for (const p of pages) {
      const key = p.section || 'Kitab';
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(p);
    }
    return [...map.entries()];
  }, [pages]);

  if (!open) return null;

  return (
    <>
      <div className="scrim" onClick={onClose} aria-hidden="true" />
      <aside className="drawer" role="dialog" aria-modal="true" aria-label="Daftar isi" ref={ref}>
        <div className="drawer-head">
          <h2>Daftar isi</h2>
          <button className="icon-btn" onClick={onClose} aria-label="Tutup daftar isi">
            <Close />
          </button>
        </div>
        <div className="drawer-body">
          <button
            className="btn"
            style={{ width: '100%', marginBottom: 10 }}
            onClick={() => {
              onClose();
              onSearch();
            }}
          >
            <Search size={15} /> Cari di seluruh kitab
          </button>
          {groups.map(([section, items]) => (
            <div className="toc-section" key={section}>
              <div className="cap">
                <Star size={9} style={{ verticalAlign: '-1px' }} /> {section} · {items.length} halaman
              </div>
              {items.map((p) => (
                <button
                  key={p.id}
                  className="toc-item"
                  ref={current === p.num ? activeRef : null}
                  aria-current={current === p.num}
                  onClick={() => {
                    onSelect(p.num);
                    onClose();
                  }}
                >
                  <span className="n">{p.label}</span>
                  <span className="t">{p.titleDisplay}</span>
                  <span className="ar" lang="ar" dir="rtl">
                    {p.titleArabic.replace(/\s*\(.*$/, '')}
                  </span>
                </button>
              ))}
            </div>
          ))}
        </div>
      </aside>
    </>
  );
}
