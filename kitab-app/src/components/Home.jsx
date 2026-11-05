import { useMemo, useState } from 'react';
import { Book, Bookmark, Grid, Info, Search, Star } from './Icons.jsx';
import { formatDate, tidy } from '../lib/text.js';

const SECTION_ORDER = ['Pembuka', 'Faedah', 'Doa & Riyadhah', 'Pelajaran'];

function PageCard({ page, onOpen, marked }) {
  return (
    <button className="page-card" onClick={() => onOpen(page.num)}>
      <span className="num">HALAMAN {page.label}</span>
      <span className="ttl">{page.titleDisplay}</span>
      <span className="ar" lang="ar" dir="rtl">
        {tidy(page.titleArabic)}
      </span>
      <span className="foot">
        {page.section && <span className="chip">{page.section}</span>}
        {page.hasTable && <span className="chip gold">Wafaq</span>}
        {marked && <span className="chip green">Ditandai</span>}
      </span>
    </button>
  );
}

export default function Home({ meta, pages, onOpen, bookmarks, onOpenBookmarks, onOpenArabiyah, lastPage }) {
  const [tab, setTab] = useState('Semua');
  const [q, setQ] = useState('');
  const [showAll, setShowAll] = useState(false);

  const marked = useMemo(() => new Set(bookmarks.map((b) => b.num)), [bookmarks]);

  const filtered = useMemo(() => {
    let list = pages;
    if (tab !== 'Semua') {
      if (tab === 'Wafaq') list = list.filter((p) => p.hasTable);
      else if (tab === 'Ditandai') list = list.filter((p) => marked.has(p.num));
      else list = list.filter((p) => p.section === tab);
    }
    if (q.trim()) {
      const needle = q.trim().toLowerCase();
      list = list.filter((p) => (p.titleDisplay + ' ' + p.titleArabic).toLowerCase().includes(needle));
    }
    return list;
  }, [pages, tab, q, marked]);

  const visible = showAll ? filtered : filtered.slice(0, 24);
  const last = pages.find((p) => p.num === lastPage);

  return (
    <>
      <section className="hero wrap">
        <div>
          <span className="hero-eyebrow">
            <Star size={12} /> Edisi digital · {meta.pages} halaman
          </span>
          <h1>Asrār Rūḥāniyyah</h1>
          <p className="hero-arabic" lang="ar" dir="rtl">
            {meta.titleArabic}
          </p>
          <p className="lead">
            Lima lapis bacaan pada setiap halaman — teks Arab, transliterasi Latin, terjemahan Indonesia, syarah, dan tuntunan
            praktik. Disusun langsung dari master editorial <code>{meta.source}</code>.
          </p>
          <div className="hero-actions">
            <button className="btn primary" onClick={() => onOpen(lastPage)}>
              <Book size={16} /> Lanjut baca · hal. {last?.label ?? 1}
            </button>
            <button className="btn" onClick={onOpenBookmarks}>
              <Bookmark size={16} /> Penanda ({bookmarks.length})
            </button>
            <button className="btn" onClick={onOpenArabiyah}>
              <Star size={16} /> Arabiyah Center
            </button>
          </div>
        </div>
        <div className="hero-cover">
          <img src="./art/sampul.jpg" alt="Ilustrasi sampul Asrār Rūḥāniyyah" width="600" height="800" />
        </div>
      </section>

      <div className="wrap">
        <div className="stats">
          <div className="stat">
            <b>{meta.pages}</b>
            <span>halaman master</span>
          </div>
          <div className="stat">
            <b>5</b>
            <span>lapis tiap halaman</span>
          </div>
          <div className="stat">
            <b>{pages.filter((p) => p.hasTable).length}</b>
            <span>halaman berwafaq</span>
          </div>
          <div className="stat">
            <b>{meta.missingFolios.length}</b>
            <span>folio kosong ditandai</span>
          </div>
        </div>

        <div className="section-head">
          <div>
            <h2>Daftar halaman</h2>
            <p>Saring menurut bagian, atau cari judulnya langsung.</p>
          </div>
          <div className="search-box" style={{ maxWidth: 300, width: '100%' }}>
            <Search size={16} />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Cari judul halaman…"
              aria-label="Cari judul halaman"
            />
          </div>
        </div>

        <div className="tabs" role="tablist" aria-label="Saring halaman">
          {['Semua', ...SECTION_ORDER, 'Wafaq', 'Ditandai'].map((t) => (
            <button key={t} className="tab" role="tab" aria-selected={tab === t} onClick={() => { setTab(t); setShowAll(false); }}>
              {t}
            </button>
          ))}
        </div>

        <div className="page-grid">
          {visible.map((page) => (
            <PageCard key={page.id} page={page} onOpen={onOpen} marked={marked.has(page.num)} />
          ))}
        </div>

        {!filtered.length && (
          <div className="empty">
            <div className="big">Tidak ada halaman yang cocok</div>
            <p>Coba kata kunci lain atau pilih tab “Semua”.</p>
          </div>
        )}

        {filtered.length > visible.length && (
          <div style={{ textAlign: 'center', margin: '-16px 0 40px' }}>
            <button className="btn" onClick={() => setShowAll(true)}>
              <Grid size={16} /> Tampilkan semua {filtered.length} halaman
            </button>
          </div>
        )}

        <div className="info-grid">
          <div className="info-card">
            <h3>Cara membaca</h3>
            <p>
              Gunakan lima tombol lapis di atas halaman untuk menampilkan atau menyembunyikan Arab, Latin, terjemahan, syarah, dan
              tuntunan praktik. Preferensi ini tersimpan di perangkat Anda.
            </p>
            <p>Pintasan: ← dan → untuk berpindah halaman, / untuk mencari.</p>
          </div>
          <div className="info-card">
            <h3>Arabiyah Center</h3>
            <p>
              Ruang belajar bahasa Arab dengan enam mode: kamus, nahwu &amp; i'rab, sharaf, balaghah, imla', serta arudh.
              Tersedia keyboard hijaiyah dan contoh cepat dari halaman kitab yang sedang dibaca.
            </p>
            <button className="btn small" onClick={onOpenArabiyah} style={{ marginTop: 6 }}>
              <Star size={14} /> Buka ruang belajar
            </button>
          </div>
          <div className="info-card">
            <h3>Tentang sumber teks</h3>
            <p>
              Dibangun {formatDate(meta.builtAt)} dari <code>{meta.source}</code> ({(meta.sourceBytes / 1024).toFixed(0)} KB,{' '}
              {meta.pages} halaman). Tidak ada teks yang ditulis ulang oleh aplikasi.
            </p>
          </div>
          <div className="info-card">
            <h3>Catatan penting</h3>
            <p>{meta.notice}</p>
            <p style={{ color: 'var(--muted)', fontSize: '0.78rem' }}>
              Folio yang tidak tersedia pada pindaian: {meta.missingFolios.join(', ')}.
            </p>
          </div>
        </div>
      </div>

      <div className="wrap">
        <div className="callout">
          <Info size={18} />
          <div>
            Aplikasi ini adalah pembaca. Untuk penelaahan bahasa Arab, harakat, dan ketepatan setiap baris terhadap pindaian,
            tetap diperlukan penelaahan ahli dan penyunting naskah.
          </div>
        </div>
      </div>
    </>
  );
}
