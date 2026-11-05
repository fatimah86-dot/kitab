import { Bookmark, Check, Info, Layers as LayersIcon, Moon, Sepia, Sun, Type } from './Icons.jsx';

const MODES = [
  { id: 'light', label: 'Terang', icon: Sun },
  { id: 'sepia', label: 'Sepia', icon: Sepia },
  { id: 'dark', label: 'Malam', icon: Moon },
];

const LAYER_LABEL = {
  arab: 'Arab',
  latin: 'Latin',
  terjemahan: 'Terjemahan',
  syarah: 'Syarah',
  khususiyah: 'Khususiyah',
};

function Switch({ checked, onChange, label }) {
  return (
    <button className="switch" role="switch" aria-checked={checked} aria-label={label} onClick={() => onChange(!checked)} />
  );
}

export default function SettingsView({ meta, prefs, setPrefs, setLayer, resetPrefs, bookmarks, pages, onOpen, onRemoveBookmark }) {
  return (
    <div className="wrap narrow" style={{ paddingTop: 24, paddingBottom: 40 }}>
      <div className="section-head">
        <div>
          <h2>Pengaturan & penanda</h2>
          <p>Semua pilihan tersimpan di perangkat ini saja.</p>
        </div>
        <button className="btn small ghost" onClick={resetPrefs}>
          Kembalikan awal
        </button>
      </div>

      <div className="panel">
        <h2>Tampilan</h2>
        <p className="hint">Pilih suasana baca yang nyaman untuk mata.</p>
        <div className="row">
          <div>
            <div className="label">Tema</div>
            <div className="sub">Terang, sepia (kertas tua), atau malam</div>
          </div>
          <div className="segmented">
            {MODES.map(({ id, label, icon: Icon }) => (
              <button key={id} aria-pressed={prefs.mode === id} onClick={() => setPrefs({ mode: id })}>
                <Icon size={14} style={{ verticalAlign: '-2px', marginRight: 4 }} />
                {label}
              </button>
            ))}
          </div>
        </div>
        <div className="row">
          <div>
            <div className="label">Ukuran huruf Arab</div>
            <div className="sub">{Math.round(prefs.scale * 100)}%</div>
          </div>
          <input
            type="range"
            min="0.8"
            max="1.8"
            step="0.05"
            value={prefs.scale}
            onChange={(e) => setPrefs({ scale: Number(e.target.value) })}
            aria-label="Ukuran huruf Arab"
          />
        </div>
        <div className="row">
          <div>
            <div className="label">Ukuran huruf Latin & terjemahan</div>
            <div className="sub">{Math.round(prefs.textScale * 100)}%</div>
          </div>
          <input
            type="range"
            min="0.85"
            max="1.45"
            step="0.05"
            value={prefs.textScale}
            onChange={(e) => setPrefs({ textScale: Number(e.target.value) })}
            aria-label="Ukuran huruf Latin dan terjemahan"
          />
        </div>
        <div className="row">
          <div>
            <div className="label">Font Arab</div>
            <div className="sub">Amiri (naskah) atau font bawaan sistem</div>
          </div>
          <div className="segmented">
            <button aria-pressed={prefs.font === 'amiri'} onClick={() => setPrefs({ font: 'amiri' })}>
              Amiri
            </button>
            <button aria-pressed={prefs.font === 'system'} onClick={() => setPrefs({ font: 'system' })}>
              Sistem
            </button>
          </div>
        </div>
      </div>

      <div className="panel">
        <h2>Lapis yang ditampilkan</h2>
        <p className="hint">Berlaku untuk semua halaman. Bilah lapis di halaman baca juga bisa dipakai.</p>
        {Object.keys(LAYER_LABEL).map((key) => (
          <div className="row" key={key}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <span className="chip">{LAYER_LABEL[key]}</span>
              <span className="sub">
                {meta.layers.find((l) => l.key === key)?.short} · lapis {key === 'syarah' || key === 'khususiyah' ? 'penjelasan' : 'utama'}
              </span>
            </div>
            <Switch checked={!!prefs.layers[key]} onChange={(v) => setLayer(key, v)} label={`Tampilkan lapis ${LAYER_LABEL[key]}`} />
          </div>
        ))}
      </div>

      <div className="panel">
        <h2>
          <Bookmark size={15} filled style={{ verticalAlign: '-2px', marginRight: 6, color: 'var(--gold)' }} />
          Penanda halaman ({bookmarks.length})
        </h2>
        <p className="hint">Tekan ikon penanda pada halaman baca untuk menambah atau menghapus.</p>
        {!bookmarks.length && <div className="sub">Belum ada halaman yang ditandai.</div>}
        <div className="bookmark-list" style={{ margin: '10px 0 0' }}>
          {bookmarks.map((b) => {
            const page = pages.find((p) => p.num === b.num);
            if (!page) return null;
            return (
              <div className="bookmark-item" key={b.num}>
                <span className="n">{page.label}</span>
                <div className="info">
                  <div className="ttl">{page.titleDisplay}</div>
                  <div className="sub">{page.section}</div>
                </div>
                <button className="btn small" onClick={() => onOpen(page.num)}>
                  Buka
                </button>
                <button className="icon-btn" onClick={() => onRemoveBookmark(page.num)} aria-label="Hapus penanda">
                  <Check size={16} />
                </button>
              </div>
            );
          })}
        </div>
      </div>

      <div className="panel">
        <h2>
          <LayersIcon size={15} style={{ verticalAlign: '-2px', marginRight: 6 }} />
          Tentang data
        </h2>
        <div className="row">
          <span className="label">Sumber master</span>
          <span className="sub" style={{ fontFamily: 'ui-monospace, monospace' }}>
            {meta.source}
          </span>
        </div>
        <div className="row">
          <span className="label">Jumlah halaman / lapis</span>
          <span className="sub">
            {meta.pages} halaman × {meta.layers.length} lapis
          </span>
        </div>
        <div className="row">
          <span className="label">Ukuran teks sumber</span>
          <span className="sub">{(meta.sourceBytes / 1024).toFixed(0)} KB</span>
        </div>
        <div className="row">
          <span className="label">Dibangun</span>
          <span className="sub">{meta.builtAt}</span>
        </div>
        <div className="row">
          <span className="label">Folio tidak tersedia</span>
          <span className="sub">{meta.missingFolios.join(', ')}</span>
        </div>
      </div>

      <div className="callout">
        <Info size={18} />
        <div>
          <strong>Catatan.</strong> {meta.notice}
        </div>
      </div>

      <p style={{ fontSize: '0.76rem', color: 'var(--muted)', display: 'flex', gap: 8, alignItems: 'center' }}>
        <Type size={14} /> Font Arab: Amiri (SIL Open Font License) · Antarmuka: Plus Jakarta Sans.
      </p>
    </div>
  );
}
