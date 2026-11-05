"use client";

import { ChangeEvent, PointerEvent, useEffect, useRef, useState } from "react";

type Passage = {
  id: number;
  title: string;
  original: string;
  vowelled: string;
  latin: string;
  translation: string;
  note: string;
};

type Crop = {
  dataUrl: string;
  page: number;
};

type Selection = {
  x: number;
  y: number;
  width: number;
  height: number;
};

const emptyPassage = (): Passage => ({
  id: Date.now(),
  title: "Pasal baru",
  original: "",
  vowelled: "",
  latin: "",
  translation: "",
  note: "",
});

export default function Page() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pdfDocumentRef = useRef<any>(null);
  const dragStartRef = useRef<{ x: number; y: number } | null>(null);

  const [pdfBytes, setPdfBytes] = useState<Uint8Array | null>(null);
  const [pdfDocument, setPdfDocument] = useState<any>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageCount, setPageCount] = useState(0);
  const [pdfName, setPdfName] = useState("");
  const [loadingPdf, setLoadingPdf] = useState(false);
  const [pdfError, setPdfError] = useState("");

  const [selection, setSelection] = useState<Selection | null>(null);
  const [crops, setCrops] = useState<Crop[]>([]);
  const [passages, setPassages] = useState<Passage[]>([emptyPassage()]);
  const [activePassageId, setActivePassageId] = useState<number | null>(
    null,
  );

  const [tashkeelLoading, setTashkeelLoading] = useState(false);

  const [tashkeelError, setTashkeelError] = useState("");

  const activePassage =
    passages.find((passage) => passage.id === activePassageId) ?? passages[0];

  useEffect(() => {
    if (!pdfBytes) {
      pdfDocumentRef.current = null;
      setPdfDocument(null);
      setPageCount(0);
      return;
    }

    let cancelled = false;
    const bytes = pdfBytes;

    async function openPdf() {
      setLoadingPdf(true);
      setPdfError("");

      try {
        const pdfjs = await import("pdfjs-dist/legacy/build/pdf.mjs");
        pdfjs.GlobalWorkerOptions.workerSrc = new URL(
          "pdfjs-dist/legacy/build/pdf.worker.mjs",
          import.meta.url,
        ).toString();
        const document = await pdfjs.getDocument({
          data: bytes,
        }).promise;

        if (cancelled) return;

        pdfDocumentRef.current = document;
        setPdfDocument(document);
        setPageCount(document.numPages);
        setPageNumber(1);
        setSelection(null);
        setCrops([]);
      } catch {
        if (!cancelled) {
          setPdfError(
            "PDF tidak dapat dibuka. Coba file PDF lain atau ekspor ulang PDF tersebut.",
          );
        }
      } finally {
        if (!cancelled) setLoadingPdf(false);
      }
    }

    void openPdf();

    return () => {
      cancelled = true;
    };
  }, [pdfBytes]);

  useEffect(() => {
    let cancelled = false;

    async function renderPage() {
      const canvas = canvasRef.current;
      if (!pdfDocument || !canvas) return;

      try {
        const page = await pdfDocument.getPage(pageNumber);
        if (cancelled) return;

        // Skala 300/72 menghasilkan dimensi piksel setara render 300 DPI.
        const viewport = page.getViewport({ scale: 300 / 72 });
        const context = canvas.getContext("2d");

        if (!context) return;

        canvas.width = Math.ceil(viewport.width);
        canvas.height = Math.ceil(viewport.height);

        await page.render({
          canvasContext: context,
          viewport,
        }).promise;

        if (!cancelled) setSelection(null);
      } catch {
        if (!cancelled) {
          setPdfError("Halaman PDF gagal dirender.");
        }
      }
    }

    void renderPage();

    return () => {
      cancelled = true;
    };
  }, [pdfDocument, pageNumber]);

  function handlePdfUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setPdfError("Pilih file PDF.");
      return;
    }

    setPdfName(file.name);
    setPdfError("");
    setPdfBytes(null);

    void file.arrayBuffer().then((buffer) => {
      setPdfBytes(new Uint8Array(buffer));
    });

    // Agar file yang sama bisa dipilih ulang.
    event.target.value = "";
  }

  function pointerPosition(event: PointerEvent<HTMLDivElement>) {
    const canvas = canvasRef.current;
    const rect = event.currentTarget.getBoundingClientRect();

    if (!canvas || !rect.width || !rect.height) {
      return { x: 0, y: 0 };
    }

    return {
      x: Math.max(
        0,
        Math.min(
          canvas.width,
          ((event.clientX - rect.left) / rect.width) * canvas.width,
        ),
      ),
      y: Math.max(
        0,
        Math.min(
          canvas.height,
          ((event.clientY - rect.top) / rect.height) * canvas.height,
        ),
      ),
    };
  }

  function handlePointerDown(event: PointerEvent<HTMLDivElement>) {
    if (!pdfDocument) return;

    event.currentTarget.setPointerCapture(event.pointerId);
    const point = pointerPosition(event);
    dragStartRef.current = point;
    setSelection({
      x: point.x,
      y: point.y,
      width: 0,
      height: 0,
    });
  }

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (!dragStartRef.current) return;

    const point = pointerPosition(event);
    const start = dragStartRef.current;

    setSelection({
      x: Math.min(start.x, point.x),
      y: Math.min(start.y, point.y),
      width: Math.abs(point.x - start.x),
      height: Math.abs(point.y - start.y),
    });
  }

  function handlePointerUp() {
    dragStartRef.current = null;
  }

  function cropSelectedArea() {
    const source = canvasRef.current;

    if (!source || !selection || selection.width < 5 || selection.height < 5) {
      setPdfError("Tarik kotak di atas halaman PDF untuk memilih area crop.");
      return;
    }

    const output = document.createElement("canvas");
    output.width = Math.round(selection.width);
    output.height = Math.round(selection.height);

    const context = output.getContext("2d");
    if (!context) return;

    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, output.width, output.height);
    context.drawImage(
      source,
      Math.round(selection.x),
      Math.round(selection.y),
      output.width,
      output.height,
      0,
      0,
      output.width,
      output.height,
    );

    setCrops((current) => [
      ...current,
      {
        dataUrl: output.toDataURL("image/png"),
        page: pageNumber,
      },
    ]);
    setSelection(null);
    setPdfError("");
  }

  function updatePassage<K extends keyof Passage>(
    key: K,
    value: Passage[K],
  ) {
    if (!activePassage) return;

    setPassages((current) =>
      current.map((passage) =>
        passage.id === activePassage.id
          ? { ...passage, [key]: value }
          : passage,
      ),
    );
  }

  async function addAutomaticHarakat() {
    const sourceText = activePassage?.original.trim();

    if (!sourceText) {
      setTashkeelError("Isi teks Arab asli terlebih dahulu.");
      return;
    }

    setTashkeelLoading(true);
    setTashkeelError("");

    try {
      const response = await fetch("/api/diacritize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: sourceText }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error ?? "Gagal memberi harakat.");
      }

      updatePassage("vowelled", data.text);
    } catch (error) {
      setTashkeelError(
        error instanceof Error ? error.message : "Terjadi kesalahan.",
      );
    } finally {
      setTashkeelLoading(false);
    }
  }

  function addPassage() {
    const passage = emptyPassage();
    setPassages((current) => [...current, passage]);
    setActivePassageId(passage.id);
  }

  function downloadCrop(crop: Crop, index: number) {
    const link = document.createElement("a");
    link.href = crop.dataUrl;
    link.download = `crop-halaman-${crop.page}-${index + 1}.png`;
    link.click();
  }

  function exportProject() {
    const project = {
      app: "Arabiyah Center — Pembaca Kitab",
      sourcePdf: pdfName,
      passages,
      crops: crops.map((crop) => ({
        page: crop.page,
        imageDataUrl: crop.dataUrl,
      })),
      exportedAt: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(project, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "proyek-baca-kitab.json";
    link.click();
    URL.revokeObjectURL(url);
  }

  function printPassages() {
    window.print();
  }

  const selectionStyle = selection
    ? {
        left: `${(selection.x / (canvasRef.current?.width || 1)) * 100}%`,
        top: `${(selection.y / (canvasRef.current?.height || 1)) * 100}%`,
        width: `${(selection.width / (canvasRef.current?.width || 1)) * 100}%`,
        height: `${(selection.height / (canvasRef.current?.height || 1)) * 100}%`,
      }
    : undefined;

  return (
    <main className="min-h-screen bg-[#0a2518] text-[#fef9e8]">
      <header className="border-b border-[#d4af37]/25 bg-[#081b12] px-4 py-4 md:px-8">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs tracking-[0.2em] text-[#d4af37]">
              ARABIYAH CENTER
            </p>
            <h1 className="mt-1 text-xl font-semibold">
              Pembaca Kitab Arab Gundul
            </h1>
          </div>
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={exportProject} className="action-button">
              Ekspor proyek
            </button>
            <button type="button" onClick={printPassages} className="action-button">
              Cetak pasal
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-5 p-4 md:grid-cols-[minmax(0,1.1fr)_minmax(360px,0.9fr)] md:p-8">
        <section className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-[#0d2b1d] p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="font-semibold">Halaman sumber PDF</h2>
                <p className="mt-1 text-xs text-[#b8c2b1]">
                  Unggah kitab, lalu tarik kotak untuk memilih gambar rajah,
                  tabel, atau bagian halaman.
                </p>
              </div>

              <label className="action-button cursor-pointer">
                Pilih PDF
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handlePdfUpload}
                  className="hidden"
                />
              </label>
            </div>

            {pdfName && (
              <p className="mt-3 truncate text-xs text-[#d4af37]">{pdfName}</p>
            )}

            {pdfError && (
              <p role="alert" className="mt-3 text-sm text-red-300">
                {pdfError}
              </p>
            )}

            {loadingPdf && (
              <p className="mt-4 text-sm text-[#d4af37]">Membuka PDF…</p>
            )}

            {pdfDocument && (
              <>
                <div className="my-4 flex items-center justify-between">
                  <button
                    type="button"
                    className="action-button"
                    disabled={pageNumber <= 1}
                    onClick={() => setPageNumber((page) => Math.max(1, page - 1))}
                  >
                    ← Sebelumnya
                  </button>
                  <span className="text-sm text-[#e9dfb1]">
                    Halaman {pageNumber} dari {pageCount}
                  </span>
                  <button
                    type="button"
                    className="action-button"
                    disabled={pageNumber >= pageCount}
                    onClick={() =>
                      setPageNumber((page) => Math.min(pageCount, page + 1))
                    }
                  >
                    Berikutnya →
                  </button>
                </div>

                <div className="max-h-[75vh] overflow-auto rounded-xl bg-[#f7f4e9] p-2">
                  <div
                    className="relative mx-auto w-fit max-w-full select-none"
                    onPointerDown={handlePointerDown}
                    onPointerMove={handlePointerMove}
                    onPointerUp={handlePointerUp}
                    onPointerCancel={handlePointerUp}
                    style={{ touchAction: "none" }}
                  >
                    <canvas
                      ref={canvasRef}
                      className="block h-auto max-w-full"
                    />
                    {selection && (
                      <div
                        className="pointer-events-none absolute border-2 border-red-500 bg-red-400/20"
                        style={selectionStyle}
                      />
                    )}
                  </div>
                </div>

                <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
                  <p className="text-xs text-[#b8c2b1]">
                    Crop memakai render 300 DPI; resolusi ekspor mengikuti
                    ukuran piksel area yang dipilih.
                  </p>
                  <button
                    type="button"
                    onClick={cropSelectedArea}
                    className="action-button-gold"
                  >
                    Simpan crop
                  </button>
                </div>
              </>
            )}
          </div>

          <div className="rounded-2xl border border-white/10 bg-[#0d2b1d] p-4">
            <h2 className="font-semibold">Crop tersimpan</h2>
            {crops.length === 0 ? (
              <p className="mt-2 text-sm text-[#aeb9a8]">
                Belum ada crop. Unggah PDF dan pilih area halaman.
              </p>
            ) : (
              <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3">
                {crops.map((crop, index) => (
                  <figure
                    key={`${crop.page}-${index}`}
                    className="rounded-xl border border-white/10 bg-[#081b12] p-2"
                  >
                    {/* Gambar berasal dari canvas PDF yang dipilih pengguna. */}
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={crop.dataUrl}
                      alt={`Crop halaman ${crop.page}`}
                      className="max-h-44 w-full bg-white object-contain"
                    />
                    <figcaption className="mt-2 flex items-center justify-between gap-2 text-xs">
                      <span>Halaman {crop.page}</span>
                      <button
                        type="button"
                        onClick={() => downloadCrop(crop, index)}
                        className="text-[#d4af37] underline"
                      >
                        Unduh
                      </button>
                    </figcaption>
                  </figure>
                ))}
              </div>
            )}
          </div>
        </section>

        <section className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-[#0d2b1d] p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="font-semibold">Teks pasal</h2>
                <p className="mt-1 text-xs text-[#b8c2b1]">
                  Isi dan periksa tiap blok secara terpisah.
                </p>
              </div>

              <button type="button" onClick={addPassage} className="action-button">
                + Pasal
              </button>
            </div>

            {passages.length > 1 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {passages.map((passage, index) => (
                  <button
                    type="button"
                    key={passage.id}
                    onClick={() => setActivePassageId(passage.id)}
                    className={`rounded-full border px-3 py-1.5 text-xs ${
                      activePassageId === passage.id ||
                      (!activePassageId && index === 0)
                        ? "border-[#d4af37] bg-[#d4af37] text-[#0a2518]"
                        : "border-white/10 text-[#e9dfb1]"
                    }`}
                  >
                    {passage.title || `Pasal ${index + 1}`}
                  </button>
                ))}
              </div>
            )}

            {activePassage && (
              <div className="mt-4 space-y-4">
                <label className="block">
                  <span className="field-label">Judul pasal</span>
                  <input
                    value={activePassage.title}
                    onChange={(event) =>
                      updatePassage("title", event.target.value)
                    }
                    className="text-field"
                    placeholder="Contoh: Pasal pertama"
                  />
                </label>

                <label className="block">
                  <span className="field-label">
                    [Teks Arab Asli] — salin apa adanya
                  </span>
                  <textarea
                    dir="rtl"
                    value={activePassage.original}
                    onChange={(event) =>
                      updatePassage("original", event.target.value)
                    }
                    className="text-field arabic-field"
                    placeholder="اكتب النص العربي الأصلي هنا"
                  />
                </label>

                <div className="block">
                  <span className="field-label">
                    [Teks Arab Berharakat] — hasil tashih
                  </span>
                  <button
                    type="button"
                    onClick={addAutomaticHarakat}
                    disabled={tashkeelLoading || !activePassage?.original.trim()}
                    className="action-button-gold mb-2 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {tashkeelLoading ? "Memproses…" : "Beri harakat otomatis"}
                  </button>

                  <textarea
                    dir="rtl"
                    value={activePassage.vowelled}
                    onChange={(event) =>
                      updatePassage("vowelled", event.target.value)
                    }
                    className="text-field arabic-field"
                    placeholder="أدخل النص بعد ضبط الحركات ومراجعته"
                  />
                  {tashkeelError && (
                    <p role="alert" className="mb-2 text-sm text-red-300">
                      {tashkeelError}
                    </p>
                  )}
                </div>

                <label className="block">
                  <span className="field-label">
                    [Transliterasi Latin Fonetik] — periksa aturan washal
                  </span>
                  <textarea
                    dir="ltr"
                    value={activePassage.latin}
                    onChange={(event) =>
                      updatePassage("latin", event.target.value)
                    }
                    className="text-field"
                    placeholder="Masukkan transliterasi lengkap pasal"
                  />
                </label>

                <label className="block">
                  <span className="field-label">
                    [Terjemahan Bahasa Indonesia]
                  </span>
                  <textarea
                    dir="ltr"
                    value={activePassage.translation}
                    onChange={(event) =>
                      updatePassage("translation", event.target.value)
                    }
                    className="text-field"
                    placeholder="Masukkan terjemahan bahasa Indonesia"
                  />
                </label>

                <label className="block">
                  <span className="field-label">Catatan pemeriksaan / rujukan</span>
                  <textarea
                    dir="ltr"
                    value={activePassage.note}
                    onChange={(event) =>
                      updatePassage("note", event.target.value)
                    }
                    className="text-field min-h-20"
                    placeholder="Catat halaman, sumber, koreksi, atau keterangan editor"
                  />
                </label>
              </div>
            )}
          </div>

          <div className="rounded-2xl border border-[#d4af37]/25 bg-[#d4af37]/[0.06] p-4 text-xs leading-6 text-[#ddd5b6]">
            <strong className="text-[#d4af37]">Penting:</strong> aplikasi ini
            menyediakan editor dan crop PDF, bukan tashih otomatis. Harakat,
            transliterasi, dan terjemahan perlu diperiksa oleh pembaca yang
            menguasai teks dan kaidah yang digunakan. Jangan menganggap hasil
            OCR atau pembacaan otomatis sebagai teks kitab yang sudah sahih.
          </div>
        </section>
      </div>

      <section className="print-area mx-auto hidden max-w-4xl px-8 py-6">
        {passages.map((passage) => (
          <article key={passage.id} className="mb-8 break-inside-avoid">
            <h2 className="mb-4 text-xl font-bold">{passage.title}</h2>

            <h3 className="font-bold">[Teks Arab Asli]</h3>
            <p dir="rtl" className="arabic-print">
              {passage.original}
            </p>

            <h3 className="font-bold">[Teks Arab Berharakat]</h3>
            <p dir="rtl" className="arabic-print">
              {passage.vowelled}
            </p>

            <h3 className="font-bold">[Transliterasi Latin Fonetik]</h3>
            <p>{passage.latin}</p>

            <h3 className="font-bold">[Terjemahan Bahasa Indonesia]</h3>
            <p>{passage.translation}</p>

            {passage.note && (
              <>
                <h3 className="font-bold">Catatan</h3>
                <p>{passage.note}</p>
              </>
            )}
          </article>
        ))}
      </section>

      <style jsx global>{`
        .action-button,
        .action-button-gold {
          border-radius: 0.75rem;
          padding: 0.65rem 0.9rem;
          font-size: 0.8rem;
          transition: 150ms ease;
        }

        .action-button {
          border: 1px solid rgba(255, 255, 255, 0.14);
          color: #fef9e8;
          background: rgba(255, 255, 255, 0.04);
        }

        .action-button:hover:not(:disabled) {
          border-color: rgba(212, 175, 55, 0.65);
          background: rgba(212, 175, 55, 0.08);
        }

        .action-button:disabled {
          cursor: not-allowed;
          opacity: 0.4;
        }

        .action-button-gold {
          background: #d4af37;
          color: #0a2518;
          font-weight: 700;
        }

        .action-button-gold:hover {
          background: #e2c457;
        }

        .action-button-gold:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

        .field-label {
          display: block;
          margin-bottom: 0.45rem;
          font-size: 0.75rem;
          font-weight: 600;
          color: #e9dfb1;
        }

        .text-field {
          width: 100%;
          min-height: 7rem;
          resize: vertical;
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 0.85rem;
          background: #081b12;
          padding: 0.85rem;
          color: #fef9e8;
          outline: none;
          line-height: 1.8;
        }

        .text-field:focus {
          border-color: rgba(212, 175, 55, 0.7);
        }

        .arabic-field,
        .arabic-print {
          font-family: "Amiri", "Noto Naskh Arabic", "Traditional Arabic", serif;
          font-size: 1.5rem;
          line-height: 2.1;
        }

        @media print {
          body {
            background: white !important;
            color: black !important;
          }

          body * {
            visibility: hidden;
          }

          .print-area,
          .print-area * {
            visibility: visible;
          }

          .print-area {
            display: block !important;
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            color: black;
            background: white;
          }
        }
      `}</style>
    </main>
  );
}
