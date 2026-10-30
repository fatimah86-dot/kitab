#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage the user's precision wafaq crops into the canonical Al-Qorin folder.

The filename is the destination printed page; no page is inferred or shifted.
All copies are byte-identical. This replaces the earlier FINAL-KHATAM-derived
crop set at the user's explicit instruction.
Outputs:
- al_qorin/wafaq_qorin/<page>.jpg
- al_qorin/wafaq_user_manifest.json
- al_qorin/MANIFEST_WAFAQ_AL_QORIN.md
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [49, 58, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78,
            82, 83, 84, 85, 86, 98, 109, 116, 120, 121]
CANONICAL = ROOT / "al_qorin/wafaq_qorin"
CAPTION = ("crop presisi kiriman pengguna; nama berkas sama dengan halaman tujuan; "
           "bukan ekstraksi FINAL KHATAM dan bukan gambar ulang")


def collect(source_dirs):
    found = {}
    for directory in source_dirs:
        if not directory.exists():
            continue
        for page in EXPECTED:
            p = directory / f"{page}.jpg"
            if not p.exists():
                continue
            data = p.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            if page in found and found[page][1] != sha:
                raise SystemExit(f"conflicting bytes for {page}.jpg between upload sources")
            found[page] = (data, sha, str(p))
    # Canonical files are only a fallback for manifest regeneration after the
    # uploads have already been staged; they must never override fresh uploads.
    for page in EXPECTED:
        if page not in found:
            p = CANONICAL / f"{page}.jpg"
            if p.exists():
                data = p.read_bytes()
                found[page] = (data, hashlib.sha256(data).hexdigest(), str(p))
    missing = [p for p in EXPECTED if p not in found]
    if missing:
        raise SystemExit(f"missing user crops: {missing}")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", action="append", default=[],
                    help="source directory; may be repeated")
    args = ap.parse_args()
    defaults = [Path("/tmp/arena-coding-uploads"),
                ROOT / "al_qorin/wafaq_upload_user_pending"]
    sources = [Path(x) for x in args.source] or defaults
    found = collect(sources)
    CANONICAL.mkdir(parents=True, exist_ok=True)

    crops = []
    for page in EXPECTED:
        data, sha, src = found[page]
        out = CANONICAL / f"{page}.jpg"
        out.write_bytes(data)
        with Image.open(out) as im:
            dims = list(im.size)
            fmt = im.format
        if fmt != "JPEG":
            raise SystemExit(f"{out} is not JPEG: {fmt}")
        crops.append({
            "page": page,
            "unit_id": f"M{page:02d}",
            "file": f"al_qorin/wafaq_qorin/{page}.jpg",
            "dims": dims,
            "bytes": len(data),
            "sha256": sha,
            "insert": True,
            "caption": CAPTION,
            "source_observed": src,
        })

    extra = sorted(p.name for p in CANONICAL.glob("*.jpg") if int(p.stem) not in EXPECTED)
    if extra:
        raise SystemExit(f"unexpected files in canonical wafaq folder: {extra}")

    manifest = {
        "source": "user-uploaded precision crops in Arena chat",
        "rule": "filename number equals destination printed page and M-unit number",
        "insertion": "centered after the Metode block, before Penentuan Jam",
        "crops": crops,
    }
    (ROOT / "al_qorin/wafaq_user_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [
        "# MANIFEST WAFAQ AL-QORIN — Crop Presisi Kiriman Pengguna",
        "",
        "Sumber gambar: 26 berkas JPG yang diunggah pengguna di chat Arena. "
        "Seluruhnya disalin byte-identik ke `al_qorin/wafaq_qorin/`; tidak ada "
        "resize, re-encode, gambar ulang, atau ekstraksi dari FINAL KHATAM.",
        "Aturan mutlak: nama berkas = halaman cetak tujuan = nomor unit M pada "
        "rentang ini. Sisip di tengah sesudah blok `1. Metode` dan sebelum "
        "`2. Penentuan Jam`.",
        "",
        "| Hal. | Unit | Berkas | Dimensi | Byte | Sisip? | SHA-256 (12) |",
        "|---:|---|---|---:|---:|:---:|---|",
    ]
    for c in crops:
        lines.append(
            f"| {c['page']} | {c['unit_id']} | `{c['file']}` | "
            f"{c['dims'][0]}x{c['dims'][1]} | {c['bytes']} | YA | `{c['sha256'][:12]}` |")
    lines += ["", f"Total crop pengguna: {len(crops)}; seluruhnya disisipkan.", ""]
    (ROOT / "al_qorin/MANIFEST_WAFAQ_AL_QORIN.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"staged={len(crops)}")
    for c in crops:
        print(c["page"], c["unit_id"], f"{c['dims'][0]}x{c['dims'][1]}", c["bytes"], c["sha256"][:12])


if __name__ == "__main__":
    main()
