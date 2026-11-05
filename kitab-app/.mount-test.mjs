import { JSDOM } from 'jsdom';
const dom = new JSDOM('<!doctype html><html><body><div id="root"></div></body></html>', { url: 'http://localhost:5173/#/arabiyah', pretendToBeVisual: true });
const w = dom.window;
globalThis.window = w; globalThis.document = w.document;
Object.defineProperty(globalThis, 'navigator', { value: w.navigator, configurable: true });
globalThis.location = w.location; globalThis.HTMLElement = w.HTMLElement; globalThis.Node = w.Node;
globalThis.localStorage = w.localStorage;
globalThis.requestAnimationFrame = (cb) => setTimeout(cb, 0);
globalThis.cancelAnimationFrame = clearTimeout;
w.scrollTo = () => {};
w.HTMLElement.prototype.scrollIntoView = () => {};
globalThis.IS_REACT_ACT_ENVIRONMENT = false;
await import('./.mount-bundle.mjs');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
await sleep(400);
const root = w.document.getElementById('root');
const log = (label, cond) => console.log((cond ? '  ✓ ' : '  ✗ ') + label);
log('Arabiyah tampil', root.innerHTML.includes('PUSAT PEMBELAJARAN BAHASA ARAB'));
log('6 mode belajar', (root.innerHTML.match(/class="ar-nav-btn"/g) || []).length === 6);
const keyEls = w.document.querySelectorAll('.ar-keys .ar-key');
log(`keyboard 32 huruf + spasi (${keyEls.length})`, keyEls.length === 33);
log('contoh kitab tersedia', root.innerHTML.includes('Dari kitab'));

// klik mode nahwu
const tabs = [...w.document.querySelectorAll('.ar-tab')];
tabs.find((t) => t.textContent.includes('NAHWU')).click();
await sleep(150);
log('ganti mode ke Nahwu', w.document.querySelector('.ar-nav-btn[aria-current="true"]').textContent.includes("NAHWU"));

// contoh cepat -> kirim
w.document.querySelector('.ar-sample').click();
await sleep(250);
const bubbles = w.document.querySelectorAll('.ar-msg');
log(`pesan bertambah (${bubbles.length})`, bubbles.length === 3);
const answer = bubbles[bubbles.length - 1].textContent;
log('respons memuat panduan mode', answer.includes('MODE NAHWU & I\'RAB') || answer.includes('MODE NAHWU'));
log('respons memuat panduan belajar', answer.includes('Gunakan uraian ini sebagai pendamping belajar'));
log('respons memuat teks contoh', answer.includes('الْعِلْمُ نُورٌ'));

// keyboard virtual
const inp = w.document.querySelector('.ar-input');
[...w.document.querySelectorAll('.ar-key')].find((b) => b.textContent === 'ب').click();
await sleep(120);
log(`keyboard menyisipkan huruf ("${w.document.querySelector('.ar-input').value}")`, w.document.querySelector('.ar-input').value.includes('ب'));

// kirim via tombol Analisis
w.document.querySelector('.ar-send').click();
await sleep(250);
log('kirim via tombol Analisis', w.document.querySelectorAll('.ar-msg').length === 5);
log('input dikosongkan', w.document.querySelector('.ar-input').value === '');

// navigasi ke halaman kitab
w.location.hash = '#/hal-18';
await sleep(300);
log('pembaca tetap berfungsi', (root.innerHTML.match(/class="layer" data-layer/g) || []).length === 5);
