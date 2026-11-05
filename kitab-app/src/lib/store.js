/* Penyimpanan lokal: bookmark, halaman terakhir, preferensi tampilan. */
import { useCallback, useEffect, useState } from 'react';

const KEY = 'kitab-asrar-v1';

const DEFAULTS = {
  bookmarks: [], // [{num, at}]
  lastPage: 1,
  prefs: {
    mode: 'light', // light | sepia | dark
    scale: 1, // skala huruf Arab
    textScale: 1, // skala huruf Latin/terjemahan
    layers: { arab: true, latin: true, terjemahan: true, syarah: true, khususiyah: true },
    showNotes: true,
    font: 'amiri', // amiri | system
  },
};

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return DEFAULTS;
    const parsed = JSON.parse(raw);
    return {
      ...DEFAULTS,
      ...parsed,
      prefs: { ...DEFAULTS.prefs, ...(parsed.prefs || {}), layers: { ...DEFAULTS.prefs.layers, ...(parsed.prefs?.layers || {}) } },
    };
  } catch {
    return DEFAULTS;
  }
}

let state = read();
const listeners = new Set();

function commit(next) {
  state = next;
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    /* penyimpanan penuh / mode privat — abaikan */
  }
  listeners.forEach((fn) => fn(state));
}

export function useStore() {
  const [, force] = useState(0);
  useEffect(() => {
    const fn = () => force((n) => n + 1);
    listeners.add(fn);
    return () => listeners.delete(fn);
  }, []);

  const setPrefs = useCallback((patch) => {
    commit({ ...state, prefs: { ...state.prefs, ...patch } });
  }, []);

  const setLayer = useCallback((key, value) => {
    commit({
      ...state,
      prefs: { ...state.prefs, layers: { ...state.prefs.layers, [key]: value } },
    });
  }, []);

  const setLastPage = useCallback((num) => {
    if (state.lastPage === num) return;
    commit({ ...state, lastPage: num });
  }, []);

  const toggleBookmark = useCallback((num) => {
    const has = state.bookmarks.some((b) => b.num === num);
    const bookmarks = has
      ? state.bookmarks.filter((b) => b.num !== num)
      : [...state.bookmarks, { num, at: Date.now() }].sort((a, b) => a.num - b.num);
    commit({ ...state, bookmarks });
  }, []);

  const resetPrefs = useCallback(() => {
    commit({ ...state, prefs: DEFAULTS.prefs });
  }, []);

  return {
    ...state,
    isBookmarked: (num) => state.bookmarks.some((b) => b.num === num),
    setPrefs,
    setLayer,
    setLastPage,
    toggleBookmark,
    resetPrefs,
  };
}
