#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the integrated 123-unit Al-Qorin Markdown master.

Starts from the logged mechanical restructure and substitutes the 12
hand-curated pilot units. It asserts that pilot substitution did not alter
Arab/Latin/Terjemahan/Metode/Jam/table material; only editor-note grouping,
Khususiyah phrases, and crop provenance may differ.
Output: al_qorin/REVISI_AL_QORIN_123.md and al_qorin/work/integrated_units.json
"""
import json
from pathlib import Path
from al_qorin_transform import render_table

ROOT = Path(__file__).resolve().parents[1]
work = ROOT / "al_qorin/work"
revised = {u["unit_id"]: u for u in json.loads((work / "revised_units.json").read_text(encoding="utf-8"))}
pilot = {u["unit_id"]: u for u in json.loads((work / "pilot_units.json").read_text(encoding="utf-8"))}
order = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]

for uid, pu in pilot.items():
    src = revised[uid]
    for key in ("heading", "page", "arab", "latin", "terjemahan", "metode", "rajah_blocks", "jam", "crop_page"):
        if pu[key] != src[key]:
            raise SystemExit(f"pilot substitution would alter protected field {uid}.{key}")
    revised[uid] = pu

units = [revised[uid] for uid in order]
(work / "integrated_units.json").write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")

full_lines = (ROOT / "al_qorin/REVISI_AL_QORIN_123_KERJA.md").read_text(encoding="utf-8").splitlines()
source_header = []
take = False
for line in full_lines:
    if line.startswith("> Catatan sumber"):
        take = True
    if take:
        if line.startswith(">"):
            source_header.append(line)
        else:
            break

md = ["# AL-QORIN WAR RIYADHAH — REVISI 123 ARTIKEL", "",
      "> Build terintegrasi mengikuti `../STANDAR_MUTLAK_AL_QORIN_123.md`: 123 unit hasil "
      "restrukturisasi terlog dari draf (4); 12 unit pilot telah dikurasi manual, unit lain "
      "menunggu penyelesaian semantik per batch. Crop wafaq adalah crop presisi kiriman "
      "pengguna, bukan ekstraksi FINAL KHATAM.", "",
      "> Dokumen ini adalah revisi terjemahan dokumenter. Metode yang dinisbatkan kepada penulis "
      "kitab tidak disajikan sebagai anjuran, terapi, atau jaminan hasil, dan bukan pengganti "
      "penanganan medis.", ""]
md += source_header + [""]
for u in units:
    md += [f"## {u['heading']}", "", "### 1. Arab", ""]
    md += [x + "\n" for x in u["arab"]]
    md += ["### 2. Latin", ""] + [x + "\n" for x in u["latin"]]
    md += ["### 3. Terjemahan", ""] + [x + "\n" for x in u["terjemahan"]]
    md += ["### 4. Metode, Penentuan Jam, dan Catatan Penyunting", "", "#### 1. Metode", ""]
    md += [x + "\n" for x in u["metode"]]
    if u["crop_page"]:
        md += [f"![Crop halaman {u['crop_page']}](wafaq_qorin/{u['crop_page']}.jpg)", "",
               f"[Crop halaman {u['crop_page']} — {u['crop_caption']}]", ""]
    for blk in u["rajah_blocks"]:
        for b in blk:
            md += [b["md"] + "\n"] if b["type"] == "p" else [render_table(b["rows"]), ""]
    md += ["#### 2. Penentuan Jam", ""] + [x + "\n" for x in u["jam"]]
    md += ["#### Catatan penyunting", ""]
    md += [x + "\n" for x in u["catatan_penyunting"]] or ["Tidak ada catatan penyunting tambahan pada unit ini.\n"]
    k = u["khususiyah"]
    md += ["### 5. Khususiyah — Waktu : Media : Bukhur", "",
           f"Waktu: {k['waktu']} : Media: {k['media']} : Bukhur: {k['bukhur']}", ""]

(ROOT / "al_qorin/REVISI_AL_QORIN_123.md").write_text("\n".join(md), encoding="utf-8")
print(f"integrated units={len(units)} pilot_substituted={len(pilot)} crops={sum(bool(u['crop_page']) for u in units)}")
