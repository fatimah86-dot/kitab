import { NextResponse } from "next/server";

export const runtime = "nodejs";

/**
 * Proxy tashkeel (diacritization) HarfScript.
 * API key tidak pernah dikirim ke browser — hanya dibaca dari env server.
 *
 * Setup:
 *   1. Di proyek Next.js, taruh file ini di app/api/diacritize/route.ts
 *   2. Isi .env.local:  HARFSCRIPT_API_KEY=***
 *   3. POST { "text": "..." } ke /api/diacritize
 *   Respons sukses: { "text": "..." }
 */
export async function POST(request: Request) {
  const apiKey = process.env.HARFSCRIPT_API_KEY;AQ.Ab8RN6JR2861ObnrfI6NkMnj-OhTQaf8koGV2BOx2E-cv8Le1A

  if (!apiKey) {
    return NextResponse.json(
      { error: "HARFSCRIPT_API_KEY belum dikonfigurasi di server." },
      { status: 500 },
    );
  }

  try {
    const body = await request.json();

    const text = typeof body.text === "string" ? body.text.trim() : "";

    if (!text) {
      return NextResponse.json(
        { error: "Teks Arab wajib diisi." },
        { status: 400 },
      );
    }

    if (text.length > 10_000) {
      return NextResponse.json(
        { error: "Teks terlalu panjang. Batasnya 10.000 karakter." },
        { status: 413 },
      );
    }

    const response = await fetch("https://api.harfscript.com/v1/diacritize", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, mode: "full" }),
      cache: "no-store",
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      return NextResponse.json(
        { error: data?.error ?? "Layanan tashkeel gagal memproses teks." },
        { status: response.status },
      );
    }

    if (typeof data?.text !== "string") {
      return NextResponse.json(
        { error: "Format respons tashkeel tidak dikenali." },
        { status: 502 },
      );
    }

    return NextResponse.json({ text: data.text });
  } catch {
    return NextResponse.json(
      { error: "Tidak dapat menghubungi layanan tashkeel." },
      { status: 502 },
    );
  }
}
