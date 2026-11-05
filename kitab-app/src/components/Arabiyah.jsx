import { useMemo, useRef, useState } from 'react';
import {
  ARABIC_KEYS,
  FEATURES,
  generateSmartResponse,
} from '../lib/arabiyah.js';
import { tidy } from '../lib/text.js';

function Sidebar({ activeFeature, onSelect }) {
  return (
    <aside className="ar-sidebar">
      <div className="ar-brand">
        <div className="ar-brand-mark" aria-hidden="true">
          ✺
        </div>
        <div>
          <p className="ar-brand-title">ARABIYAH</p>
          <p className="ar-brand-sub">CENTER AI</p>
        </div>
      </div>

      <p className="ar-side-label">RUANG BELAJAR</p>

      <nav className="ar-nav">
        {FEATURES.map((feature) => (
          <button
            type="button"
            key={feature.id}
            onClick={() => onSelect(feature.id)}
            aria-current={feature.id === activeFeature}
            className="ar-nav-btn"
          >
            <span className="ar-nav-icon ar-arabic" aria-hidden="true">
              {feature.icon}
            </span>
            <span className="ar-nav-text">
              <span className="ar-nav-title">{feature.title}</span>
              <span className="ar-nav-sub">{feature.subtitle}</span>
            </span>
          </button>
        ))}
      </nav>

      <div className="ar-side-card">
        <b>Belajar mandiri 24/7</b>
        <p>Jelajahi bahasa Arab, satu kata dan satu kaidah pada satu waktu.</p>
      </div>
    </aside>
  );
}

function FeatureTabs({ activeFeature, onSelect }) {
  return (
    <div className="ar-tabs" role="tablist" aria-label="Mode belajar">
      {FEATURES.map((feature) => (
        <button
          type="button"
          key={feature.id}
          role="tab"
          aria-selected={feature.id === activeFeature}
          onClick={() => onSelect(feature.id)}
          className="ar-tab"
        >
          {feature.title}
        </button>
      ))}
    </div>
  );
}

function ArabKeyboard({ onType, onBackspace, onClear }) {
  return (
    <div className="ar-keyboard">
      <div className="ar-keyboard-head">
        <b>Keyboard Hijaiyah</b>
        <div className="ar-keyboard-actions">
          <button type="button" onClick={onBackspace} className="ar-kb-btn" aria-label="Hapus karakter terakhir">
            Hapus ⌫
          </button>
          <button type="button" onClick={onClear} className="ar-kb-btn">
            Bersihkan
          </button>
        </div>
      </div>

      <div className="ar-keys">
        {ARABIC_KEYS.map((key) => (
          <button
            type="button"
            key={key}
            onClick={() => onType(key)}
            className="ar-key"
            aria-label={`Masukkan huruf ${key}`}
          >
            {key}
          </button>
        ))}
        <button type="button" onClick={() => onType(' ')} className="ar-key is-space">
          Spasi
        </button>
      </div>
    </div>
  );
}

/** Ambil kutipan Arab dari halaman kitab yang sedang dibaca (jika ada). */
function pageQuote(page) {
  if (!page) return '';
  const first = page.layers?.arab?.blocks?.find((b) => b.type === 'p' && b.text);
  const body = first ? tidy(first.text) : '';
  return body.length > 140 ? `${body.slice(0, 140)}…` : body;
}

export default function Arabiyah({ page, onOpenPage }) {
  const [activeFeature, setActiveFeature] = useState('kamus');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState(() => [
    {
      id: 1,
      role: 'assistant',
      text: 'أهلًا وسهلًا! Selamat datang di Arabiyah Center. Pilih mode belajar di sidebar, ketik teks Arab, atau tekan tombol contoh cepat untuk memulai.',
    },
  ]);
  const inputRef = useRef(null);

  const selectedFeature = FEATURES.find((f) => f.id === activeFeature) ?? FEATURES[0];
  const quote = useMemo(() => pageQuote(page), [page]);

  // Susun contoh cepat: contoh bawaan mode + kutipan halaman kitab (bila ada).
  const samples = useMemo(() => {
    const list = [{ label: `Contoh ${selectedFeature.title}`, text: selectedFeature.sample }];
    if (quote) list.push({ label: `Dari kitab · halaman ${page.label}`, text: quote });
    return list;
  }, [selectedFeature, quote, page]);

  const appendText = (text) => {
    const el = inputRef.current;
    const start = el?.selectionStart ?? input.length;
    const end = el?.selectionEnd ?? input.length;
    setInput(input.slice(0, start) + text + input.slice(end));
    requestAnimationFrame(() => {
      if (!el) return;
      const cursor = start + text.length;
      el.focus();
      el.setSelectionRange(cursor, cursor);
    });
  };

  const backspace = () => {
    const el = inputRef.current;
    const start = el?.selectionStart ?? input.length;
    const end = el?.selectionEnd ?? input.length;
    if (start !== end) {
      setInput(input.slice(0, start) + input.slice(end));
      requestAnimationFrame(() => {
        el?.focus();
        el?.setSelectionRange(start, start);
      });
      return;
    }
    if (start > 0) {
      setInput(input.slice(0, start - 1) + input.slice(end));
      requestAnimationFrame(() => {
        el?.focus();
        el?.setSelectionRange(start - 1, start - 1);
      });
    }
  };

  const sendMessage = (override) => {
    const text = (override ?? input).trim();
    if (!text) return;
    const answer = generateSmartResponse(text, selectedFeature);
    setMessages((current) => [
      ...current,
      { id: Date.now(), role: 'user', text },
      { id: Date.now() + 1, role: 'assistant', text: answer },
    ]);
    setInput('');
    requestAnimationFrame(() => inputRef.current?.focus());
  };

  return (
    <div className="ar-root">
      <div className="ar-shell">
        <Sidebar activeFeature={activeFeature} onSelect={setActiveFeature} />

        <div className="ar-main">
          <header className="ar-head">
            <div>
              <p className="ar-head-eyebrow">PUSAT PEMBELAJARAN BAHASA ARAB</p>
              <h1>Belajar lebih dekat dengan bahasa Arab</h1>
            </div>
            <div className="ar-badge">✦ EDUKASI · MANDIRI · 24/7</div>
          </header>

          <div className="ar-body">
            <FeatureTabs activeFeature={activeFeature} onSelect={setActiveFeature} />

            <section className="ar-chat">
              <div className="ar-chat-top">
                <div>
                  <b>Asisten Bahasa Arab</b>
                  <p className="ar-chat-mode">
                    Mode aktif: <span>{selectedFeature.title}</span>
                  </p>
                </div>
                <span className="ar-status">
                  <i /> MODE LOKAL
                </span>
              </div>

              <div className="ar-chat-log" aria-live="polite">
                {messages.map((message) => (
                  <div key={message.id} className={`ar-msg${message.role === 'user' ? ' is-user' : ''}`}>
                    <div className="ar-msg-bubble">
                      <p className="ar-msg-role">{message.role === 'user' ? 'Kamu' : 'Arabiyah Center'}</p>
                      <p className="ar-msg-text" dir={message.role === 'user' ? 'rtl' : 'auto'}>
                        {message.text}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="ar-composer">
                <div>
                  <div className="ar-sample-head">
                    <b>Contoh cepat · {selectedFeature.title}</b>
                    <span>Klik untuk langsung dianalisis</span>
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {samples.map((s, i) => (
                      <button
                        type="button"
                        key={i}
                        onClick={() => sendMessage(s.text)}
                        className="ar-sample"
                        dir="rtl"
                        title={`${s.label}: ${s.text}`}
                      >
                        <span className="ar-arabic">{s.text}</span>
                      </button>
                    ))}
                    {page && (
                      <button type="button" className="ar-sample" onClick={() => onOpenPage?.(page.num)} title="Buka halaman kitab">
                        <span style={{ fontFamily: 'var(--sans)', fontSize: '0.72rem', direction: 'ltr', display: 'inline-block' }}>
                          ↗ Buka halaman {page.label} di kitab
                        </span>
                      </button>
                    )}
                  </div>
                </div>

                <div className="ar-input-row">
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(event) => setInput(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === 'Enter' && !event.shiftKey) {
                        event.preventDefault();
                        sendMessage();
                      }
                    }}
                    rows={2}
                    dir="auto"
                    placeholder="اكتب كلمة أو جملة بالعربية…"
                    className="ar-input"
                    aria-label="Tulis teks Arab"
                  />
                  <button type="button" onClick={() => sendMessage()} className="ar-send" disabled={!input.trim()}>
                    Analisis
                  </button>
                </div>

                <ArabKeyboard
                  onType={appendText}
                  onBackspace={backspace}
                  onClear={() => {
                    setInput('');
                    inputRef.current?.focus();
                  }}
                />

                <p className="ar-note">
                  Respons bersifat edukatif dan dihasilkan secara lokal; periksa kembali analisis untuk kebutuhan akademik.
                </p>
              </div>
            </section>
          </div>

          <footer className="ar-foot">
            <p>Untuk Pelajar · Mahasiswa · Santri · Ustadz &amp; Guru · Dosen · Penerjemah · Peneliti · Pecinta Bahasa Arab</p>
            <p className="gold">Belajar mandiri 24/7</p>
          </footer>
        </div>
      </div>
    </div>
  );
}
