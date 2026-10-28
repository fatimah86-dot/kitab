#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit all 123 Al-Qorin units before the total translation revision.

The audit is intentionally mechanical and honest: it inventories truncation
markers, unresolved-reading signals already present in editor notes, crop
units, translator labels, and rough layer-length ratios. It does not claim
that a unit with no marker is semantically perfect; it creates a priority
queue for scan-checked revision batches.

Input preference: al_qorin/work/integrated_units.json (current output), else
al_qorin/work/revised_units.json. Output:
al_qorin/AUDIT_REVISI_TOTAL_TERJEMAHAN_123.md
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "al_qorin/work"
OUT = ROOT / "al_qorin/AUDIT_REVISI_TOTAL_TERJEMAHAN_123.md"
ORDER = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]

TRUNCATION = "tidak disalin penuh"
UNCERTAIN_TERMS = (
    "belum pasti",
    "tidak pasti",
    "belum ditetapkan",
    "tidak dapat saya pastikan",
    "tidak dapat dipastikan",
    "rusak",
    "belum mantap",
    "tidak terbaca",
    "belum diverifikasi",
)
PLACEHOLDER_RE = re.compile(r"\[[^\]]*(?:belum|rajah|gambar|pindaian|CATATAN PENERJEMAH)[^\]]*\]", re.I)


def joined(unit, key):
    return " ".join(unit.get(key) or [])


def main():
    integrated = WORK / "integrated_units.json"
    revised = WORK / "revised_units.json"
    source = integrated if integrated.exists() else revised
    if not source.exists():
        raise SystemExit("work JSON not present; run the Al-Qorin builders first")
    units = {u["unit_id"]: u for u in json.loads(source.read_text(encoding="utf-8"))}
    if set(units) != set(ORDER):
        raise SystemExit("unit set is not exactly SAMPUL + M01-M122")

    rows = []
    totals = {
        "truncation_units": 0,
        "truncation_markers": 0,
        "ellipsis": 0,
        "label_units": 0,
        "labels": 0,
        "crop_units": 0,
        "p1": 0,
        "p2": 0,
        "p3": 0,
    }
    for uid in ORDER:
        u = units[uid]
        arab = joined(u, "arab")
        latin = joined(u, "latin")
        terjemahan = joined(u, "terjemahan")
        notes = joined(u, "catatan_penyunting")
        trunc = terjemahan.count(TRUNCATION)
        ellipsis = terjemahan.count("…") + terjemahan.count("...")
        placeholders = len(PLACEHOLDER_RE.findall(terjemahan))
        uncertain_notes = sum(notes.lower().count(term) for term in UNCERTAIN_TERMS)
        labels = (
            arab.count("[CATATAN PENERJEMAH")
            + latin.count("[CATATAN PENERJEMAH")
            + terjemahan.count("[CATATAN PENERJEMAH")
        )
        ratio = (len(terjemahan) / len(arab)) if arab else 0.0
        flags = []
        if trunc:
            flags.append(f"potongan:{trunc}")
        if placeholders:
            flags.append(f"placeholder:{placeholders}")
        if ellipsis:
            flags.append(f"elipsis:{ellipsis}")
        if uncertain_notes:
            flags.append(f"catatan-ragu:{uncertain_notes}")
        if labels:
            flags.append(f"label:{labels}")
        if u.get("crop_page"):
            flags.append(f"crop:{u['crop_page']}")
        if u.get("rajah_blocks"):
            flags.append(f"rajah_blocks:{len(u['rajah_blocks'])}")
        if ratio and (ratio < 0.75 or ratio > 1.9):
            flags.append(f"rasio:{ratio:.2f}")

        if trunc or placeholders >= 2:
            priority = "P1"
        elif uncertain_notes >= 3 or ellipsis >= 2:
            priority = "P2"
        else:
            priority = "P3"
        totals[priority.lower()] += 1
        totals["truncation_units"] += bool(trunc)
        totals["truncation_markers"] += trunc
        totals["ellipsis"] += ellipsis
        totals["label_units"] += bool(labels)
        totals["labels"] += labels
        totals["crop_units"] += bool(u.get("crop_page"))
        rows.append(
            {
                "uid": uid,
                "page": u.get("page") or "-",
                "arab": len(arab),
                "latin": len(latin),
                "terjemahan": len(terjemahan),
                "notes": len(u.get("catatan_penyunting") or []),
                "priority": priority,
                "flags": ", ".join(flags) if flags else "-",
            }
        )

    lines = [
        "# AUDIT REVISI TOTAL TERJEMAHAN AL-QORIN — 123 UNIT",
        "",
        "Audit ini dibuat sebelum revisi total Lapis 1–3. Ia menginventarisasi",
        "seluruh SAMPUL + M01–M122 dari output terintegrasi saat ini. Penanda",
        "prioritas bersifat mekanis: P1 berarti ada potongan/placeholder yang",
        "harus dibuka kembali ke pindaian; P2 berarti banyak keraguan bacaan",
        "yang sudah dicatat penyunting; P3 bukan berarti sempurna, hanya tidak",
        "menonjol secara mekanis dan tetap wajib dibaca ulang per batch.",
        "",
        "## Ringkasan",
        "",
        f"- Unit diaudit: **{len(rows)}**",
        f"- Prioritas: **P1={totals['p1']}**, **P2={totals['p2']}**, **P3={totals['p3']}**",
        f"- Unit dengan penanda “tidak disalin penuh”: **{totals['truncation_units']}** "
        f"(total penanda **{totals['truncation_markers']}**)",
        f"- Total elipsis pada Terjemahan: **{totals['ellipsis']}**",
        f"- Unit berlabel `[CATATAN PENERJEMAH]`: **{totals['label_units']}** "
        f"(total label pada Lapis 1–3: **{totals['labels']}**; label tidak boleh hilang)",
        f"- Unit ber-crop wafaq pengguna: **{totals['crop_units']}** "
        "(crop tidak diganti dan tidak diambil dari FINAL KHATAM)",
        "",
        "## Antrean batch yang dipakai",
        "",
        "1. **Batch 01 — SAMPUL, M01–M05:** menetapkan gaya Anwar pada sampul,",
        "   mukadimah, dan bab pertama; Arab/Latin tidak diubah tanpa bukti pindaian.",
        "2. **Batch 02 — M06–M15:** riyadhah awal dan unit berpenanda potongan M10–M12.",
        "3. **Batch 03 — M16–M32:** termasuk unit P1 M18, M20, M23, M28, M32.",
        "4. **Batch 04 — M33–M49:** termasuk M38 dan awal unit ber-crop M49.",
        "5. **Batch 05 — M50–M71:** unit praktik, tabel, dan crop padat; cek silang",
        "   Metode/Khususiyah hanya bila terjemahan yang diperbaiki membuktikannya.",
        "6. **Batch 06 — M72–M86:** unit rajah/crop dan penanda potongan M74, M80–M85.",
        "7. **Batch 07 — M87–M103:** daftar nama dan bab M93, M96–M98.",
        "8. **Batch 08 — M104–M122:** menutup selisih pindaian M104/M107 tanpa",
        "   menimpa catatan beda bacaan secara diam-diam, lalu khatimah.",
        "",
        "Setiap batch wajib: membaca pindaian asli halaman terkait, mempertahankan",
        "jumlah paragraf Lapis 1–3 kecuali ada dasar tertulis, mempertahankan label",
        "`[CATATAN PENERJEMAH]`, tabel, `rajah_blocks`, Penentuan Jam, dan crop; lalu",
        "membangun ulang MD/DOCX/preview dan menjalankan test.",
        "",
        "## Tabel audit per unit",
        "",
        "| Unit | Hal. | Arab | Latin | Terjemahan | Catatan | Prioritas | Penanda |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['uid']} | {r['page']} | {r['arab']} | {r['latin']} | "
            f"{r['terjemahan']} | {r['notes']} | {r['priority']} | {r['flags']} |"
        )
    lines += [
        "",
        "## Batas audit",
        "",
        "Panjang karakter dan penanda teks tidak membuktikan benar/salahnya suatu",
        "terjemahan. Keputusan perubahan Arab/Latin hanya boleh diambil dari",
        "pindaian asli; keraguan yang tidak terselesaikan harus tetap tampak pada",
        "Catatan penyunting, bukan dihaluskan menjadi kepastian palsu.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"audit units={len(rows)} p1={totals['p1']} p2={totals['p2']} p3={totals['p3']} output={OUT}")


if __name__ == "__main__":
    main()
