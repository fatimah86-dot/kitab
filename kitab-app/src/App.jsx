import { useCallback, useEffect, useMemo, useState } from 'react';
import data from './data/kitab.json';
import { useStore } from './lib/store.js';
import Home from './components/Home.jsx';
import Reader from './components/Reader.jsx';
import SearchView from './components/SearchView.jsx';
import SettingsView from './components/SettingsView.jsx';
import Arabiyah from './components/Arabiyah.jsx';
import Drawer from './components/Drawer.jsx';
import { Book, Bookmark, Layers, Menu, Moon, Search, Settings, Sepia, Sun, Sparkle } from './components/Icons.jsx';

const CYCLE = ['light', 'sepia', 'dark'];
const MODE_ICON = { light: Sun, sepia: Sepia, dark: Moon };

/** Router sederhana berbasis hash: #/ , #/hal-12 , #/cari , #/pengaturan */
function parseHash() {
  const h = (location.hash || '#/').replace(/^#\/?/, '');
  if (!h) return { view: 'home' };
  if (h === 'cari') return { view: 'search' };
  if (h === 'pengaturan' || h === 'penanda') return { view: 'settings' };
  if (h === 'arabiyah' || h === 'belajar') return { view: 'arabiyah' };
  const m = h.match(/^hal-(\d{1,3})$/);
  if (m) return { view: 'page', num: Number(m[1]) };
  return { view: 'home' };
}

export default function App() {
  const store = useStore();
  const { prefs } = store;
  const [route, setRoute] = useState(parseHash);
  const [tocOpen, setTocOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [toast, setToast] = useState('');

  const pages = data.pages;
  const meta = data.meta;

  useEffect(() => {
    const onHash = () => setRoute(parseHash());
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  // Tema, ukuran huruf, dan font dipasang pada elemen root.
  useEffect(() => {
    const root = document.documentElement;
    root.dataset.theme = prefs.mode;
    root.style.setProperty('--arab-size', `${1.55 * prefs.scale}rem`);
    root.style.setProperty('--text-size', `${prefs.textScale}rem`);
    root.style.setProperty('--arab', prefs.font === 'system' ? "'Scheherazade New', 'Traditional Arabic', 'Noto Naskh Arabic', serif" : "'Amiri', 'Scheherazade New', serif");
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if (metaTheme) metaTheme.setAttribute('content', prefs.mode === 'dark' ? '#0c1412' : prefs.mode === 'sepia' ? '#ece0c8' : '#f6f1e6');
  }, [prefs.mode, prefs.scale, prefs.textScale, prefs.font]);

  const go = useCallback((hash) => {
    if (location.hash === hash) return;
    location.hash = hash;
  }, []);

  const openPage = useCallback(
    (num) => {
      go(`#/hal-${num}`);
      store.setLastPage(num);
    },
    [go, store]
  );

  useEffect(() => {
    const onKey = (e) => {
      if (e.target instanceof HTMLElement && /input|textarea|select/i.test(e.target.tagName)) return;
      if (e.key === '/') {
        e.preventDefault();
        go('#/cari');
      }
      if (e.key === 'Escape') setTocOpen(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [go]);

  // Simpan halaman terakhir saat membuka halaman.
  useEffect(() => {
    if (route.view === 'page') store.setLastPage(route.num);
  }, [route]);

  const page = route.view === 'page' ? pages.find((p) => p.num === route.num) : null;
  const activePage = page || pages.find((p) => p.num === store.lastPage) || pages[0];
  const notFound = route.view === 'page' && !page;

  const toggleLayer = useCallback(
    (key) => {
      store.setLayer(key, !prefs.layers[key]);
    },
    [store, prefs.layers]
  );

  const cycleMode = () => {
    const i = CYCLE.indexOf(prefs.mode);
    store.setPrefs({ mode: CYCLE[(i + 1) % CYCLE.length] });
  };

  const ModeIcon = MODE_ICON[prefs.mode] || Sun;
  const marked = page ? store.isBookmarked(page.num) : false;

  const onToggleBookmark = () => {
    if (!page) return;
    store.toggleBookmark(page.num);
    setToast(marked ? `Penanda halaman ${page.label} dihapus` : `Halaman ${page.label} ditandai`);
    setTimeout(() => setToast(''), 1700);
  };

  const section = useMemo(() => (page ? page.section : ''), [page]);

  return (
    <div className="app">
      <header className="topbar">
        <button className="brand" onClick={() => go('#/')} aria-label="Beranda">
          <span className="brand-mark" aria-hidden="true">
            <Layers size={20} />
          </span>
          <span className="brand-text">
            <span className="brand-title">Asrār Rūḥāniyyah</span>
            <span className="brand-sub">Pembaca 5 lapis</span>
          </span>
        </button>

        <div style={{ display: 'flex', gap: 4, marginLeft: 8 }}>
          <button className="icon-btn" onClick={() => setTocOpen(true)} aria-label="Buka daftar isi" title="Daftar isi">
            <Menu />
          </button>
          {route.view === 'page' && (
            <span className="chip" style={{ alignSelf: 'center' }}>
              {section}
            </span>
          )}
        </div>

        <div className="topbar-search">
          <div className="search-box">
            <Search size={16} />
            <input
              placeholder="Cari seluruh kitab…  (tekan /)"
              value={route.view === 'search' ? searchQuery : ''}
              onFocus={() => go('#/cari')}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                go('#/cari');
              }}
              aria-label="Cari seluruh kitab"
            />
          </div>
        </div>

        <div className="topbar-actions">
          <button
            className={`btn small arabiyah-link${route.view === 'arabiyah' ? ' is-active' : ''}`}
            onClick={() => go('#/arabiyah')}
            aria-pressed={route.view === 'arabiyah'}
            title="Arabiyah Center — ruang belajar bahasa Arab"
          >
            <span className="arabiyah-glyph" aria-hidden="true">
              <Sparkle size={15} />
            </span>
            <span className="arabiyah-link-text">Arabiyah</span>
          </button>
          <button className="icon-btn" onClick={cycleMode} title={`Tema: ${prefs.mode}`} aria-label="Ganti tema">
            <ModeIcon />
          </button>
          <button
            className="icon-btn"
            onClick={() => go('#/pengaturan')}
            aria-pressed={route.view === 'settings'}
            title="Pengaturan"
            aria-label="Pengaturan"
          >
            <Settings />
          </button>
          <button
            className="icon-btn"
            onClick={() => go('#/cari')}
            aria-pressed={route.view === 'search'}
            title="Cari"
            aria-label="Cari"
            style={{ display: 'none' }}
          >
            <Search />
          </button>
        </div>
      </header>

      <main className="main">
        {route.view === 'home' && (
          <Home
            meta={meta}
            pages={pages}
            bookmarks={store.bookmarks}
            lastPage={store.lastPage}
            onOpen={openPage}
            onOpenBookmarks={() => go('#/pengaturan')}
            onOpenArabiyah={() => go('#/arabiyah')}
          />
        )}

        {route.view === 'page' && page && (
          <Reader
            page={page}
            pages={pages}
            prefs={prefs}
            onNavigate={openPage}
            onBack={() => go('#/')}
            onOpenToc={() => setTocOpen(true)}
            isBookmarked={marked}
            onToggleBookmark={onToggleBookmark}
            onToggleLayer={toggleLayer}
            onStudy={() => go('#/arabiyah')}
          />
        )}

        {notFound && (
          <div className="wrap narrow">
            <div className="empty">
              <div className="big">Halaman tidak ditemukan</div>
              <p>Kitab ini memiliki halaman 1 sampai {meta.pages}.</p>
              <button className="btn primary" onClick={() => go('#/')} style={{ marginTop: 12 }}>
                <Book size={16} /> Kembali ke daftar
              </button>
            </div>
          </div>
        )}

        {route.view === 'search' && (
          <SearchView
            initialQuery={searchQuery}
            onQueryChange={setSearchQuery}
            onOpen={(num) => {
              openPage(num);
            }}
          />
        )}

        {route.view === 'arabiyah' && <Arabiyah page={activePage} onOpenPage={openPage} />}

        {route.view === 'settings' && (
          <SettingsView
            meta={meta}
            prefs={prefs}
            setPrefs={store.setPrefs}
            setLayer={store.setLayer}
            resetPrefs={store.resetPrefs}
            bookmarks={store.bookmarks}
            pages={pages}
            onOpen={openPage}
            onRemoveBookmark={(num) => store.toggleBookmark(num)}
          />
        )}
      </main>

      <Drawer
        open={tocOpen}
        pages={pages}
        current={route.view === 'page' ? route.num : null}
        onSelect={openPage}
        onClose={() => setTocOpen(false)}
        onSearch={() => go('#/cari')}
      />

      {toast && <div className="toast">{toast}</div>}

      <footer className="footer">
        <div className="footer-inner">
          <span>
            <Bookmark size={13} filled style={{ verticalAlign: '-2px' }} /> {meta.pages} halaman · 5 lapis · dari{' '}
            <code>{meta.source}</code>
          </span>
          <span>
            Teks disalin apa adanya. Klaim khasiat adalah isi naskah, bukan bukti medis. ·{' '}
            <a href="#/pengaturan">Tentang</a>
          </span>
        </div>
      </footer>
    </div>
  );
}
