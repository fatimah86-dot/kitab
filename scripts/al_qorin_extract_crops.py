#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract FINAL KHATAM images byte-identically.

Outputs:
- al_qorin/wafaq_qorin/<page>.jpg       : wafaq/rajah/deret/lingkaran crops to insert
- al_qorin/crop_lain/<page>.jpg         : daftar-only crops (extracted, not inserted)
- al_qorin/work/final_full/*.jpg        : per-page source scans ('Pindai sumber')
- al_qorin/MANIFEST_WAFAQ_AL_QORIN.md   : manifest with hashes and mapping
- al_qorin/work/crop_manifest.json
"""
import hashlib, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "google_drive/KITAB AL-QORIN - EDISI REVISI LENGKAP 5 LAPIS - FINAL KHATAM.docx"
MAP = ROOT / "al_qorin/work/final_media_map.json"
WAFAQ_DIR = ROOT / "al_qorin/wafaq_qorin"
LAIN_DIR = ROOT / "al_qorin/crop_lain"
FULL_DIR = ROOT / "al_qorin/work/final_full"
for d in (WAFAQ_DIR, LAIN_DIR, FULL_DIR):
    d.mkdir(parents=True, exist_ok=True)

def page_of(heading):
    m = re.search(r"Halaman cetak (\d+)", heading or "")
    return int(m.group(1)) if m else None

def caption_of(e):
    prev = [t for t in e.get("prev_texts", []) if t.strip()]
    return prev[-1].strip() if prev else ""

events = json.loads(MAP.read_text(encoding="utf-8"))
z = zipfile.ZipFile(str(FINAL))
manifest, full = [], []
for e in events:
    f = e["file"]
    data = z.read("word/media/" + f)
    sha = hashlib.sha256(data).hexdigest()
    page = page_of(e["page_heading"])
    cap = caption_of(e)
    is_pindai = any("Pindai sumber" in t for t in e.get("prev_texts", []))
    if is_pindai:
        if (e["page_heading"] or "").startswith("Sampul"):
            key = "sampul"
        elif (e["page_heading"] or "").startswith("Penutup"):
            key = "penutup"
        else:
            key = f"cetak{page:03d}" if page else "unknown"
        out = FULL_DIR / f"{key}.jpg"
        out.write_bytes(data)
        full.append({"key": key, "src": f, "page_heading": e["page_heading"], "sha256": sha})
        continue
    # crop event
    daftar_only = cap.lower().startswith("daftar")
    target_dir = LAIN_DIR if daftar_only else WAFAQ_DIR
    out = target_dir / f"{page}.jpg"
    out.write_bytes(data)
    manifest.append({
        "page": page, "unit_id": (f"M{page:02d}" if page and 5 <= page <= 121 else None),
        "src_file": f, "dims": e.get("dims"), "bytes": len(data), "sha256": sha,
        "caption": cap, "insert": (not daftar_only),
        "out": str(out.relative_to(ROOT)),
    })

manifest.sort(key=lambda x: x["page"])
(ROOT / "al_qorin/work/crop_manifest.json").write_text(
    json.dumps({"crops": manifest, "full_scans": full}, ensure_ascii=False, indent=1), encoding="utf-8")

lines = [
    "# MANIFEST WAFAQ AL-QORIN — Ekstraksi dari FINAL KHATAM",
    "",
    "Sumber gambar: `KITAB AL-QORIN - EDISI REVISI LENGKAP 5 LAPIS - FINAL KHATAM.docx` "
    "(`word/media/*`, disalin byte-identik, tanpa resize/re-encode).",
    "Nama berkas = halaman cetak tujuan; untuk halaman >= 5 nomor unit M sama dengan nomor halaman cetak.",
    "Crop berkategori daftar saja diekstrak ke `crop_lain/` dan **tidak disisipkan** sebagai wafaq "
    "(teks FINAL sendiri menyatakan tidak tampak wafaq/rajah pada halaman-halaman itu).",
    "",
    "| Hal. | Unit | Berkas | Dimensi | Byte | Sisip? | Keterangan FINAL | SHA-256 (12) |",
    "|---:|---|---|---|---:|:---:|---|---|",
]
for m in manifest:
    dims = f"{m['dims'][0]}x{m['dims'][1]}" if m["dims"] else "-"
    lines.append(f"| {m['page']} | {m['unit_id'] or '-'} | `{m['out']}` | {dims} | {m['bytes']} | "
                 f"{'YA' if m['insert'] else 'tidak'} | {m['caption']} | `{m['sha256'][:12]}` |")
lines += ["", f"Total crop: {len(manifest)}; disisipkan: {sum(m['insert'] for m in manifest)}; "
          f"pindai halaman penuh ter ekstrak ke `al_qorin/work/final_full/` (tidak di-commit): {len(full)}.", ""]
(ROOT / "al_qorin/MANIFEST_WAFAQ_AL_QORIN.md").write_text("\n".join(lines), encoding="utf-8")
print(f"crops={len(manifest)} insert={sum(m['insert'] for m in manifest)} full_scans={len(full)}")
for m in manifest:
    print(m["page"], m["unit_id"], "INSERT" if m["insert"] else "daftar", m["out"])
