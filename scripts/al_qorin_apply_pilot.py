#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the hand-finished pilot overrides to the mechanical Al-Qorin work data.

The overrides only (a) select/group already-salvaged editor-note sentences,
(b) replace two notes with their own critical clauses, and (c) set Lapis 5
particulars from source phrases. Arab/Latin/Terjemahan and Metode stay as
transformed from the source draft.
Outputs: al_qorin/work/pilot_units.json, al_qorin/REVISI_AL_QORIN_PILOT.md,
al_qorin/CATATAN_PILOT.md
"""
import json
from pathlib import Path
from al_qorin_transform import render_table

ROOT = Path(__file__).resolve().parents[1]
UNITS = {u["unit_id"]: u for u in json.loads((ROOT / "al_qorin/work/revised_units.json").read_text(encoding="utf-8"))}
OV = json.loads((ROOT / "al_qorin/overrides_pilot.json").read_text(encoding="utf-8"))
FULL_MD = (ROOT / "al_qorin/REVISI_AL_QORIN_123_KERJA.md").read_text(encoding="utf-8").splitlines()

def source_header_lines():
    out = []
    take = False
    for line in FULL_MD:
        if line.startswith("> Catatan sumber"):
            take = True
        if take:
            if line.startswith(">"):
                out.append(line)
            else:
                break
    return out

pilot = []
for uid in OV["pilot_units"]:
    if uid not in UNITS:
        raise SystemExit(f"unknown pilot unit {uid}")
    u = json.loads(json.dumps(UNITS[uid], ensure_ascii=False))  # deep copy
    ov = OV["units"].get(uid, {})
    notes = list(u["catatan_penyunting"])
    for idx, replacement in ov.get("notes_replace", {}).items():
        notes[int(idx) - 1] = replacement
    groups = ov.get("notes_groups")
    if groups:
        flat = [i for g in groups for i in g]
        bad = [i for i in flat if i < 1 or i > len(notes)]
        if bad:
            raise SystemExit(f"{uid}: note indices out of range {bad} (have {len(notes)})")
        u["catatan_penyunting"] = [" ".join(notes[i - 1] for i in g) for g in groups]
    if ov.get("notes_add"):
        u["catatan_penyunting"] += ov["notes_add"]
    if ov.get("khususiyah"):
        u["khususiyah"].update(ov["khususiyah"])
    if ov.get("metode"):
        u["metode"] = ov["metode"]
    u["pilot_status"] = "selesai manual (pilot); Arab/Latin/Terjemahan verbatim dari draf (4)"
    pilot.append(u)

(ROOT / "al_qorin/work/pilot_units.json").write_text(json.dumps(pilot, ensure_ascii=False, indent=1), encoding="utf-8")

md = ["# AL-QORIN WAR RIYADHAH — PILOT REVISI STANDAR 123 ARTIKEL", "",
      "> Cakupan pilot: SAMPUL, M01–M05, M58, M65–M67, M69, M122. Ini contoh penyelesaian "
      "mengikuti `../STANDAR_MUTLAK_AL_QORIN_123.md`, bukan edisi final 123 unit.", "",
      "> Dokumen ini adalah revisi terjemahan dokumenter. Metode yang dinisbatkan kepada penulis "
      "kitab tidak disajikan sebagai anjuran, terapi, atau jaminan hasil, dan bukan pengganti "
      "penanganan medis.", ""]
md += source_header_lines() + [""]
for u in pilot:
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
(ROOT / "al_qorin/REVISI_AL_QORIN_PILOT.md").write_text("\n".join(md), encoding="utf-8")

status = ["# CATATAN PILOT AL-QORIN", "",
          "Unit pilot yang diselesaikan manual: " + ", ".join(OV["pilot_units"]) + ".", "",
          "- Arab/Latin/Terjemahan: verbatim dari draf (4) (hanya pemisahan lapis).",
          "- Metode: kalimat Petunjuk lama dari draf (4), tanpa kalimat Qarinah sebaris.",
          "- Catatan penyunting: kalimat ketidakpastian/tashih dari Syarah lama yang dipilih dan "
          "dikelompokkan lewat `overrides_pilot.json`; dikte nahwu/Shorof/Hukum-baca tidak dibawa.",
          "- Crop: disisipkan sesudah blok Metode dari `wafaq_qorin/<halaman>.jpg` "
          "(ekstraksi byte-identik FINAL KHATAM; lihat manifest).",
          "- Empat tabel transkripsi draf (M65/M66/M67/M69) dipertahankan pada unitnya; "
          "tabel M65/M67/M69 ikut pilot, M66 termasuk tabel 4x3-nya.",
          "- 111 unit lain baru selesai pada tingkat restrukturisasi mekanis terlog "
          "(`REVISI_AL_QORIN_123_KERJA.md`) dan masih menunggu penyelesaian semantik per batch.", ""]
(ROOT / "al_qorin/CATATAN_PILOT.md").write_text("\n".join(status), encoding="utf-8")
print("pilot units:", len(pilot))
for u in pilot:
    print(u["unit_id"], "notes", len(u["catatan_penyunting"]), "crop", u["crop_page"], "rajah_blocks", len(u["rajah_blocks"]))
