#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the integrated 123-unit Al-Qorin Markdown master.

Starts from the logged mechanical restructure and substitutes the 12
hand-curated pilot units. It asserts that pilot substitution did not alter
Arab/Latin/Terjemahan/Metode/Jam/table material; only editor-note grouping,
Khususiyah phrases, and crop provenance may differ.

After pilot substitution, a deliberately narrow post-pilot stage applies the
verified selective-upload overrides in
``al_qorin/overrides_upload_selektif_2026-10-28.json``. That stage may change
only Khususiyah, append editor notes, and replace the demonstrably mismatched
M122 Metode summary. Every protected layer/field is re-asserted against a
post-pilot baseline before anything is rendered.
Output: al_qorin/REVISI_AL_QORIN_123.md and al_qorin/work/integrated_units.json
"""
import copy
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

# --- Post-pilot selective upload overrides ---------------------------------
# The uploaded MD/DOCX were audited as candidate supplements, not masters.
# This stage is intentionally allow-listed and field-limited.
SELECTIVE_OVERRIDES = ROOT / "al_qorin/overrides_upload_selektif_2026-10-28.json"
SELECTIVE_UNITS = {
    "M68", "M70", "M71", "M104", "M105", "M106", "M107", "M109",
    "M116", "M120", "M121", "M122",
}
SELECTIVE_ENTRY_KEYS = {"dasar", "khususiyah", "catatan_tambah", "metode"}
SELECTIVE_KHUSUSIYAH_KEYS = {"waktu", "media", "bukhur"}
SELECTIVE_CHANGE_KEYS = {"metode", "catatan_penyunting", "khususiyah"}


def fail_selective(message):
    raise SystemExit(f"selective upload override rejected: {message}")


selective_payload = json.loads(SELECTIVE_OVERRIDES.read_text(encoding="utf-8"))
selective_units = selective_payload.get("units")
if not isinstance(selective_units, dict):
    fail_selective("payload has no object field 'units'")
unknown_units = sorted(set(selective_units) - SELECTIVE_UNITS)
if unknown_units:
    fail_selective(f"units outside the audited allow-list: {unknown_units}")
missing_units = sorted(SELECTIVE_UNITS - set(selective_units))
if missing_units:
    fail_selective(f"audited selective units missing from payload: {missing_units}")

# Snapshot exactly what pilot substitution produced. The selective stage is
# compared field-by-field with this baseline, so an override can never smuggle
# in an Arab/Latin/Terjemahan, Jam, table, heading, page, or crop change.
post_pilot_baseline = copy.deepcopy(revised)

for uid, entry in selective_units.items():
    if not isinstance(entry, dict):
        fail_selective(f"{uid}: entry is not an object")
    unknown_keys = sorted(set(entry) - SELECTIVE_ENTRY_KEYS)
    if unknown_keys:
        fail_selective(f"{uid}: unsupported keys {unknown_keys}")
    if not str(entry.get("dasar", "")).strip():
        fail_selective(f"{uid}: missing non-empty audit basis ('dasar')")

    unit = revised[uid]
    khususiyah = entry.get("khususiyah")
    if khususiyah is not None:
        if not isinstance(khususiyah, dict) or not khususiyah:
            fail_selective(f"{uid}: 'khususiyah' must be a non-empty object")
        unknown_khususiyah = sorted(set(khususiyah) - SELECTIVE_KHUSUSIYAH_KEYS)
        if unknown_khususiyah:
            fail_selective(f"{uid}: unsupported Khususiyah keys {unknown_khususiyah}")
        for key, value in khususiyah.items():
            if not isinstance(value, str) or not value.strip():
                fail_selective(f"{uid}: Khususiyah {key} must be non-empty text")
            unit["khususiyah"][key] = value

    notes_add = entry.get("catatan_tambah")
    if notes_add is not None:
        if not isinstance(notes_add, list) or not notes_add:
            fail_selective(f"{uid}: 'catatan_tambah' must be a non-empty list")
        for note in notes_add:
            if not isinstance(note, str) or not note.strip():
                fail_selective(f"{uid}: appended editor note must be non-empty text")
            if note in unit["catatan_penyunting"]:
                fail_selective(f"{uid}: appended editor note already present")
            unit["catatan_penyunting"].append(note)

    metode = entry.get("metode")
    if metode is not None:
        # M122 is the sole deliberate exception: its old summary contradicted
        # the unit's own preserved Arab/Terjemahan. No other Metode may move.
        if uid != "M122":
            fail_selective(f"{uid}: Metode replacement is allowed only for M122")
        if (not isinstance(metode, list) or not metode
                or any(not isinstance(x, str) or not x.strip() for x in metode)):
            fail_selective("M122: 'metode' must be a non-empty list of text")
        joined = " ".join(metode)
        required = (
            "salat dua rakaat",
            "berselawat kepada Nabi sepuluh kali",
            "al-Fatihah untuk Syekh Muhammad Sibami",
        )
        forbidden = ("berwudu", "al-Fatihah sepuluh kali", "bertanya kepada")
        if any(phrase not in joined for phrase in required):
            fail_selective("M122: corrected Metode is missing a source-bound phrase")
        if any(phrase in joined for phrase in forbidden):
            fail_selective("M122: corrected Metode still contains the old mismatch")
        unit["metode"] = list(metode)

for uid in order:
    baseline = post_pilot_baseline[uid]
    current = revised[uid]
    if uid not in SELECTIVE_UNITS:
        if current != baseline:
            fail_selective(f"{uid}: unit changed although it is outside the allow-list")
        continue
    for key, baseline_value in baseline.items():
        if key not in SELECTIVE_CHANGE_KEYS and current[key] != baseline_value:
            fail_selective(f"{uid}: protected field changed: {key}")
    if current["jam"] != baseline["jam"]:
        fail_selective(f"{uid}: Penentuan Jam changed")

    entry = selective_units[uid]
    baseline_notes = baseline["catatan_penyunting"]
    expected_notes = baseline_notes + list(entry.get("catatan_tambah", []))
    if current["catatan_penyunting"] != expected_notes:
        fail_selective(f"{uid}: editor notes were not append-only")
    if uid != "M122" and current["metode"] != baseline["metode"]:
        fail_selective(f"{uid}: Metode changed outside the M122 exception")
    expected_khususiyah = dict(baseline["khususiyah"])
    expected_khususiyah.update(entry.get("khususiyah", {}))
    if current["khususiyah"] != expected_khususiyah:
        fail_selective(f"{uid}: Khususiyah differs beyond the declared override")

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
      "restrukturisasi terlog dari draf (4); 12 unit pilot telah dikurasi manual. Sesudah pilot, "
      "penajaman selektif Lapis 4/5 diterapkan hanya pada 12 unit sasaran yang terverifikasi dari "
      "paket unggahan 2026-10-28; unit lain masih menunggu penyelesaian semantik per batch. Crop "
      "wafaq adalah crop presisi kiriman pengguna, bukan ekstraksi FINAL KHATAM.", "",
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
print(
    f"integrated units={len(units)} pilot_substituted={len(pilot)} "
    f"selective_overrides={len(selective_units)} "
    f"crops={sum(bool(u['crop_page']) for u in units)}"
)
