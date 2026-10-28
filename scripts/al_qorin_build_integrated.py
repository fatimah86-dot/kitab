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

A second post-pilot stage applies the semantic batch overrides in
``al_qorin/overrides_batch_m16_m64.json`` (M16-M64). It may only select/group
already-salvaged editor notes, rewrite Khususiyah phrases, and replace five
keyword-stub Metode summaries (M19, M20, M21, M38, M46); it is likewise
re-asserted field-by-field against its pre-batch baseline.

A third stage applies ``al_qorin/overrides_batch_m06_m15_m72_m121.json``
(M06-M15 and M72-M121). Its baseline is therefore post-pilot, post-selective,
and post-M16-M64. It may only select/group already-salvaged editor notes,
rewrite Khususiyah phrases, and replace four Metode summaries that are a
keyword stub or contradict the preserved Arab/Terjemahan on concrete material
(M12, M79, M82, M83). The appended selective discrepancy notes on M104/M107
must survive note selection.

A final stage applies ``al_qorin/overrides_batch_m68_m70_m71.json`` to the
three selective-only units that remained. Its baseline is post-batch2. It may
only select already-salvaged editor notes, rewrite Khususiyah phrases, and
replace the first Metode paragraph of M71; M71's transparent rajah paragraphs
after the first must remain byte-identical.
Output: al_qorin/REVISI_AL_QORIN_123.md and al_qorin/work/integrated_units.json
"""
import copy
import json
from pathlib import Path
from al_qorin_transform import render_table, render_unit_md

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

# --- Semantic batch M16-M64 ------------------------------------------------
# Pilot-level curation for one contiguous batch: editor notes may only be
# selected/grouped from the notes already salvaged for that unit (no new note
# text), Khususiyah phrases may be rewritten, and Metode may be replaced only
# where the mechanical keyword stub demonstrably misread a narrative verb as
# an instruction. Everything else is re-asserted against a pre-batch snapshot.
BATCH_OVERRIDES = ROOT / "al_qorin/overrides_batch_m16_m64.json"
BATCH_UNITS = {f"M{i:02d}" for i in range(16, 65)}
BATCH_ENTRY_KEYS = {"dasar", "notes_groups", "khususiyah", "metode"}
BATCH_KHUSUSIYAH_KEYS = {"waktu", "media", "bukhur"}
BATCH_METODE_UNITS = {"M19", "M20", "M21", "M38", "M46"}
BATCH_CHANGE_KEYS = {"metode", "catatan_penyunting", "khususiyah"}


def fail_batch(message):
    raise SystemExit(f"semantic batch M16-M64 override rejected: {message}")


batch_payload = json.loads(BATCH_OVERRIDES.read_text(encoding="utf-8"))
batch_units = batch_payload.get("units")
if not isinstance(batch_units, dict):
    fail_batch("payload has no object field 'units'")
if set(batch_units) != BATCH_UNITS:
    fail_batch(
        "payload units must be exactly M16-M64; "
        f"missing={sorted(BATCH_UNITS - set(batch_units))} "
        f"extra={sorted(set(batch_units) - BATCH_UNITS)}"
    )

pre_batch_baseline = copy.deepcopy(revised)

for uid, entry in batch_units.items():
    if not isinstance(entry, dict):
        fail_batch(f"{uid}: entry is not an object")
    unknown_keys = sorted(set(entry) - BATCH_ENTRY_KEYS)
    if unknown_keys:
        fail_batch(f"{uid}: unsupported keys {unknown_keys}")
    if not str(entry.get("dasar", "")).strip():
        fail_batch(f"{uid}: missing non-empty audit basis ('dasar')")
    if not any(k in entry for k in ("notes_groups", "khususiyah", "metode")):
        fail_batch(f"{uid}: entry declares no curation action")

    unit = revised[uid]
    baseline_notes = pre_batch_baseline[uid]["catatan_penyunting"]
    groups = entry.get("notes_groups")
    if groups is not None:
        if not isinstance(groups, list) or not groups:
            fail_batch(f"{uid}: 'notes_groups' must be a non-empty list")
        flat = []
        for g in groups:
            if (not isinstance(g, list) or not g
                    or any(not isinstance(i, int) or isinstance(i, bool) for i in g)):
                fail_batch(f"{uid}: each notes group must be a non-empty list of integers")
            flat.extend(g)
        if flat != sorted(flat) or len(set(flat)) != len(flat):
            fail_batch(f"{uid}: note indices must be unique and in ascending order")
        if flat[0] < 1 or flat[-1] > len(baseline_notes):
            fail_batch(f"{uid}: note indices out of range (have {len(baseline_notes)})")
        unit["catatan_penyunting"] = [
            " ".join(baseline_notes[i - 1] for i in g) for g in groups
        ]

    khususiyah = entry.get("khususiyah")
    if khususiyah is not None:
        if not isinstance(khususiyah, dict) or not khususiyah:
            fail_batch(f"{uid}: 'khususiyah' must be a non-empty object")
        unknown_khususiyah = sorted(set(khususiyah) - BATCH_KHUSUSIYAH_KEYS)
        if unknown_khususiyah:
            fail_batch(f"{uid}: unsupported Khususiyah keys {unknown_khususiyah}")
        for key, value in khususiyah.items():
            if not isinstance(value, str) or not value.strip():
                fail_batch(f"{uid}: Khususiyah {key} must be non-empty text")
            unit["khususiyah"][key] = value

    metode = entry.get("metode")
    if metode is not None:
        if uid not in BATCH_METODE_UNITS:
            fail_batch(f"{uid}: Metode replacement is allowed only for {sorted(BATCH_METODE_UNITS)}")
        if (not isinstance(metode, list) or not metode
                or any(not isinstance(x, str) or not x.strip() for x in metode)):
            fail_batch(f"{uid}: 'metode' must be a non-empty list of text")
        joined = " ".join(metode)
        if "Petunjuk yang ada dalam sumber:" in joined:
            fail_batch(f"{uid}: replacement Metode still contains the keyword stub")
        if uid in {"M19", "M20", "M21", "M46"} and "Tidak ada petunjuk praktik" not in joined:
            fail_batch(f"{uid}: replacement Metode must state that there is no practice instruction")
        if uid == "M38" and "Peringatan dari sumber" not in joined:
            fail_batch("M38: replacement Metode must be framed as the source's warning")
        unit["metode"] = list(metode)

for uid in order:
    baseline = pre_batch_baseline[uid]
    current = revised[uid]
    if uid not in BATCH_UNITS:
        if current != baseline:
            fail_batch(f"{uid}: unit changed although it is outside M16-M64")
        continue
    for key, baseline_value in baseline.items():
        if key not in BATCH_CHANGE_KEYS and current[key] != baseline_value:
            fail_batch(f"{uid}: protected field changed: {key}")
    if current["jam"] != baseline["jam"]:
        fail_batch(f"{uid}: Penentuan Jam changed")

    entry = batch_units[uid]
    groups = entry.get("notes_groups")
    if groups is None:
        expected_notes = baseline["catatan_penyunting"]
    else:
        expected_notes = [
            " ".join(baseline["catatan_penyunting"][i - 1] for i in g) for g in groups
        ]
    if current["catatan_penyunting"] != expected_notes:
        fail_batch(f"{uid}: editor notes differ beyond declared grouping")
    if uid not in BATCH_METODE_UNITS and current["metode"] != baseline["metode"]:
        fail_batch(f"{uid}: Metode changed outside the stub-correction allow-list")
    expected_khususiyah = dict(baseline["khususiyah"])
    expected_khususiyah.update(entry.get("khususiyah", {}))
    if current["khususiyah"] != expected_khususiyah:
        fail_batch(f"{uid}: Khususiyah differs beyond the declared override")

# --- Semantic batch M06-M15 and M72-M121 ------------------------------------
# This stage runs last so its baseline already contains pilot substitution,
# selective-upload notes/Khususiyah, and the M16-M64 batch. Editor notes may
# only be selected/grouped from that baseline (no new note text), Khususiyah
# phrases may be rewritten, and Metode may be replaced only for one keyword
# stub and three concrete Arab/Terjemahan contradictions. The selective
# discrepancy notes appended to M104/M107 are explicitly required to survive.
BATCH2_OVERRIDES = ROOT / "al_qorin/overrides_batch_m06_m15_m72_m121.json"
BATCH2_UNITS = {f"M{i:02d}" for i in range(6, 16)} | {f"M{i:02d}" for i in range(72, 122)}
BATCH2_ENTRY_KEYS = {"dasar", "notes_groups", "khususiyah", "metode"}
BATCH2_KHUSUSIYAH_KEYS = {"waktu", "media", "bukhur"}
BATCH2_METODE_UNITS = {"M12", "M79", "M82", "M83"}
BATCH2_CHANGE_KEYS = {"metode", "catatan_penyunting", "khususiyah"}
BATCH2_APPENDED_NOTE_UNITS = {"M104", "M107"}


def fail_batch2(message):
    raise SystemExit(f"semantic batch M06-M15/M72-M121 override rejected: {message}")


batch2_payload = json.loads(BATCH2_OVERRIDES.read_text(encoding="utf-8"))
batch2_units = batch2_payload.get("units")
if not isinstance(batch2_units, dict):
    fail_batch2("payload has no object field 'units'")
if set(batch2_units) != BATCH2_UNITS:
    fail_batch2(
        "payload units must be exactly M06-M15 and M72-M121; "
        f"missing={sorted(BATCH2_UNITS - set(batch2_units))} "
        f"extra={sorted(set(batch2_units) - BATCH2_UNITS)}"
    )

pre_batch2_baseline = copy.deepcopy(revised)

for uid, entry in batch2_units.items():
    if not isinstance(entry, dict):
        fail_batch2(f"{uid}: entry is not an object")
    unknown_keys = sorted(set(entry) - BATCH2_ENTRY_KEYS)
    if unknown_keys:
        fail_batch2(f"{uid}: unsupported keys {unknown_keys}")
    if not str(entry.get("dasar", "")).strip():
        fail_batch2(f"{uid}: missing non-empty audit basis ('dasar')")
    if not any(k in entry for k in ("notes_groups", "khususiyah", "metode")):
        fail_batch2(f"{uid}: entry declares no curation action")

    unit = revised[uid]
    baseline_notes = pre_batch2_baseline[uid]["catatan_penyunting"]
    groups = entry.get("notes_groups")
    if groups is not None:
        if not isinstance(groups, list) or not groups:
            fail_batch2(f"{uid}: 'notes_groups' must be a non-empty list")
        flat = []
        for g in groups:
            if (not isinstance(g, list) or not g
                    or any(not isinstance(i, int) or isinstance(i, bool) for i in g)):
                fail_batch2(f"{uid}: each notes group must be a non-empty list of integers")
            flat.extend(g)
        if flat != sorted(flat) or len(set(flat)) != len(flat):
            fail_batch2(f"{uid}: note indices must be unique and in ascending order")
        if flat[0] < 1 or flat[-1] > len(baseline_notes):
            fail_batch2(f"{uid}: note indices out of range (have {len(baseline_notes)})")
        if uid in BATCH2_APPENDED_NOTE_UNITS and len(baseline_notes) not in flat:
            fail_batch2(f"{uid}: appended selective discrepancy note must be retained")
        unit["catatan_penyunting"] = [
            " ".join(baseline_notes[i - 1] for i in g) for g in groups
        ]

    khususiyah = entry.get("khususiyah")
    if khususiyah is not None:
        if not isinstance(khususiyah, dict) or not khususiyah:
            fail_batch2(f"{uid}: 'khususiyah' must be a non-empty object")
        unknown_khususiyah = sorted(set(khususiyah) - BATCH2_KHUSUSIYAH_KEYS)
        if unknown_khususiyah:
            fail_batch2(f"{uid}: unsupported Khususiyah keys {unknown_khususiyah}")
        for key, value in khususiyah.items():
            if not isinstance(value, str) or not value.strip():
                fail_batch2(f"{uid}: Khususiyah {key} must be non-empty text")
            unit["khususiyah"][key] = value

    metode = entry.get("metode")
    if metode is not None:
        if uid not in BATCH2_METODE_UNITS:
            fail_batch2(f"{uid}: Metode replacement is allowed only for {sorted(BATCH2_METODE_UNITS)}")
        if (not isinstance(metode, list) or not metode
                or any(not isinstance(x, str) or not x.strip() for x in metode)):
            fail_batch2(f"{uid}: 'metode' must be a non-empty list of text")
        joined = " ".join(metode)
        if "Petunjuk yang ada dalam sumber:" in joined:
            fail_batch2(f"{uid}: replacement Metode still contains the keyword stub")
        required_by_unit = {
            "M12": ("sebelum fajar", "delapan puluh hari", "bukan anjuran"),
            "M79": ("pelepah hijau", "cendana", "tujuh puluh kali"),
            "M82": ("dikuburkan di pintu", "tiga puluh satu kali"),
            "M83": ("diasapi", "Tidak ada instruksi menggantung"),
        }
        forbidden_by_unit = {
            "M79": ("kertas hijau",),
            "M82": ("penulisan di kuburan",),
            "M83": ("dibakar dan digantung",),
        }
        if any(phrase not in joined for phrase in required_by_unit.get(uid, ())):
            fail_batch2(f"{uid}: replacement Metode is missing a source-bound phrase")
        if any(phrase in joined for phrase in forbidden_by_unit.get(uid, ())):
            fail_batch2(f"{uid}: replacement Metode still contains the old contradiction")
        unit["metode"] = list(metode)

for uid in order:
    baseline = pre_batch2_baseline[uid]
    current = revised[uid]
    if uid not in BATCH2_UNITS:
        if current != baseline:
            fail_batch2(f"{uid}: unit changed although it is outside M06-M15/M72-M121")
        continue
    for key, baseline_value in baseline.items():
        if key not in BATCH2_CHANGE_KEYS and current[key] != baseline_value:
            fail_batch2(f"{uid}: protected field changed: {key}")
    if current["jam"] != baseline["jam"]:
        fail_batch2(f"{uid}: Penentuan Jam changed")

    entry = batch2_units[uid]
    groups = entry.get("notes_groups")
    if groups is None:
        expected_notes = baseline["catatan_penyunting"]
    else:
        expected_notes = [
            " ".join(baseline["catatan_penyunting"][i - 1] for i in g) for g in groups
        ]
    if current["catatan_penyunting"] != expected_notes:
        fail_batch2(f"{uid}: editor notes differ beyond declared grouping")
    if uid not in BATCH2_METODE_UNITS and current["metode"] != baseline["metode"]:
        fail_batch2(f"{uid}: Metode changed outside the correction allow-list")
    expected_khususiyah = dict(baseline["khususiyah"])
    expected_khususiyah.update(entry.get("khususiyah", {}))
    if current["khususiyah"] != expected_khususiyah:
        fail_batch2(f"{uid}: Khususiyah differs beyond the declared override")

# --- Final semantic batch M68, M70, M71 -------------------------------------
# These were the only selective-only units left after the earlier batches.
# The baseline is post-batch2 (hence already post-selective). Notes may only
# be selected from that baseline, Khususiyah phrases may be rewritten, and
# M71 may replace only its first Metode paragraph: the transparent rajah
# description paragraphs that follow are protected byte-for-byte.
FINAL_OVERRIDES = ROOT / "al_qorin/overrides_batch_m68_m70_m71.json"
FINAL_UNITS = {"M68", "M70", "M71"}
FINAL_ENTRY_KEYS = {"dasar", "notes_groups", "khususiyah", "metode_first"}
FINAL_KHUSUSIYAH_KEYS = {"waktu", "media", "bukhur"}
FINAL_METODE_FIRST_UNITS = {"M71"}
FINAL_CHANGE_KEYS = {"metode", "catatan_penyunting", "khususiyah"}


def fail_final(message):
    raise SystemExit(f"final semantic batch M68/M70/M71 override rejected: {message}")


final_payload = json.loads(FINAL_OVERRIDES.read_text(encoding="utf-8"))
final_units = final_payload.get("units")
if not isinstance(final_units, dict):
    fail_final("payload has no object field 'units'")
if set(final_units) != FINAL_UNITS:
    fail_final(
        "payload units must be exactly M68, M70, and M71; "
        f"missing={sorted(FINAL_UNITS - set(final_units))} "
        f"extra={sorted(set(final_units) - FINAL_UNITS)}"
    )

pre_final_baseline = copy.deepcopy(revised)

for uid, entry in final_units.items():
    if not isinstance(entry, dict):
        fail_final(f"{uid}: entry is not an object")
    unknown_keys = sorted(set(entry) - FINAL_ENTRY_KEYS)
    if unknown_keys:
        fail_final(f"{uid}: unsupported keys {unknown_keys}")
    if not str(entry.get("dasar", "")).strip():
        fail_final(f"{uid}: missing non-empty audit basis ('dasar')")
    if not any(k in entry for k in ("notes_groups", "khususiyah", "metode_first")):
        fail_final(f"{uid}: entry declares no curation action")

    unit = revised[uid]
    baseline_notes = pre_final_baseline[uid]["catatan_penyunting"]
    groups = entry.get("notes_groups")
    if groups is not None:
        if not isinstance(groups, list) or not groups:
            fail_final(f"{uid}: 'notes_groups' must be a non-empty list")
        flat = []
        for g in groups:
            if (not isinstance(g, list) or not g
                    or any(not isinstance(i, int) or isinstance(i, bool) for i in g)):
                fail_final(f"{uid}: each notes group must be a non-empty list of integers")
            flat.extend(g)
        if flat != sorted(flat) or len(set(flat)) != len(flat):
            fail_final(f"{uid}: note indices must be unique and in ascending order")
        if flat[0] < 1 or flat[-1] > len(baseline_notes):
            fail_final(f"{uid}: note indices out of range (have {len(baseline_notes)})")
        unit["catatan_penyunting"] = [
            " ".join(baseline_notes[i - 1] for i in g) for g in groups
        ]

    khususiyah = entry.get("khususiyah")
    if khususiyah is not None:
        if not isinstance(khususiyah, dict) or not khususiyah:
            fail_final(f"{uid}: 'khususiyah' must be a non-empty object")
        unknown_khususiyah = sorted(set(khususiyah) - FINAL_KHUSUSIYAH_KEYS)
        if unknown_khususiyah:
            fail_final(f"{uid}: unsupported Khususiyah keys {unknown_khususiyah}")
        for key, value in khususiyah.items():
            if not isinstance(value, str) or not value.strip():
                fail_final(f"{uid}: Khususiyah {key} must be non-empty text")
            unit["khususiyah"][key] = value

    metode_first = entry.get("metode_first")
    if metode_first is not None:
        if uid not in FINAL_METODE_FIRST_UNITS:
            fail_final(
                f"{uid}: Metode first-paragraph replacement is allowed only for "
                f"{sorted(FINAL_METODE_FIRST_UNITS)}"
            )
        if not isinstance(metode_first, str) or not metode_first.strip():
            fail_final(f"{uid}: 'metode_first' must be non-empty text")
        baseline_metode = pre_final_baseline[uid]["metode"]
        if len(baseline_metode) < 2:
            fail_final(f"{uid}: baseline Metode has no protected suffix")
        required = ("109 kali", "dipanaskan", "zat persisnya tidak dipastikan")
        forbidden = ("dibakar dengan lemak", "pada enam sisi")
        if any(phrase not in metode_first for phrase in required):
            fail_final("M71: replacement first Metode paragraph is missing a source-bound phrase")
        if any(phrase in metode_first for phrase in forbidden):
            fail_final("M71: replacement first Metode paragraph still contains the old contradiction")
        unit["metode"] = [metode_first] + list(baseline_metode[1:])

for uid in order:
    baseline = pre_final_baseline[uid]
    current = revised[uid]
    if uid not in FINAL_UNITS:
        if current != baseline:
            fail_final(f"{uid}: unit changed although it is outside M68/M70/M71")
        continue
    for key, baseline_value in baseline.items():
        if key not in FINAL_CHANGE_KEYS and current[key] != baseline_value:
            fail_final(f"{uid}: protected field changed: {key}")
    if current["jam"] != baseline["jam"]:
        fail_final(f"{uid}: Penentuan Jam changed")

    entry = final_units[uid]
    groups = entry.get("notes_groups")
    if groups is None:
        expected_notes = baseline["catatan_penyunting"]
    else:
        expected_notes = [
            " ".join(baseline["catatan_penyunting"][i - 1] for i in g) for g in groups
        ]
    if current["catatan_penyunting"] != expected_notes:
        fail_final(f"{uid}: editor notes differ beyond declared selection")
    if "metode_first" in entry:
        expected_metode = [entry["metode_first"]] + list(baseline["metode"][1:])
        if current["metode"] != expected_metode:
            fail_final(f"{uid}: Metode differs beyond the first-paragraph replacement")
    elif current["metode"] != baseline["metode"]:
        fail_final(f"{uid}: Metode changed outside the M71 first-paragraph exception")
    expected_khususiyah = dict(baseline["khususiyah"])
    expected_khususiyah.update(entry.get("khususiyah", {}))
    if current["khususiyah"] != expected_khususiyah:
        fail_final(f"{uid}: Khususiyah differs beyond the declared override")

# --- Total translation revision, Batch 01: SAMPUL, M01-M05 ------------------
# This user-ordered phase follows the Anwar translation style.  Batch 01 may
# rewrite only Lapis 3.  It was scan-checked against the cover and printed
# pages 2-5, but no Arab/Latin correction was sufficiently certain to replace
# the canonical layers, so both remain byte-identical here.  Paragraph counts
# and translator labels are hard guards; Lapis 4/5 and all graphic data are
# protected.
translation_path = ROOT / "al_qorin/overrides_terjemahan_total_batch01.json"
translation_data = json.loads(translation_path.read_text(encoding="utf-8"))
translation_units = translation_data["units"]
expected_translation_units = ["SAMPUL", "M01", "M02", "M03", "M04", "M05"]


def fail_translation(message):
    raise SystemExit(f"translation batch01 validation: {message}")


if list(translation_units) != expected_translation_units:
    fail_translation("targets must be exactly SAMPUL, M01, M02, M03, M04, M05")

pre_translation = copy.deepcopy(revised)
for uid, entry in translation_units.items():
    if set(entry) != {"dasar", "terjemahan"}:
        fail_translation(f"{uid}: Batch 01 may declare only dasar + terjemahan")
    if not isinstance(entry["dasar"], str) or len(entry["dasar"]) < 60:
        fail_translation(f"{uid}: dasar must record the scan/style basis")
    baseline = pre_translation[uid]
    replacement = entry["terjemahan"]
    if (
        not isinstance(replacement, list)
        or not replacement
        or any(not isinstance(x, str) or not x.strip() for x in replacement)
    ):
        fail_translation(f"{uid}: terjemahan must be a non-empty string list")
    if len(replacement) != len(baseline["terjemahan"]):
        fail_translation(f"{uid}: Terjemahan paragraph count changed")
    if len(baseline["arab"]) != len(baseline["latin"]) or len(replacement) != len(baseline["arab"]):
        fail_translation(f"{uid}: Lapis 1-3 paragraph alignment is not 1:1:1")
    label = "[CATATAN PENERJEMAH"
    if " ".join(replacement).count(label) != " ".join(baseline["terjemahan"]).count(label):
        fail_translation(f"{uid}: translator-label count changed")
    changed = dict(baseline)
    changed["terjemahan"] = list(replacement)
    revised[uid] = changed

for uid in order:
    baseline = pre_translation[uid]
    current = revised[uid]
    if uid not in translation_units:
        if current != baseline:
            fail_translation(f"{uid}: spill outside Batch 01")
        continue
    for key, value in baseline.items():
        if key == "terjemahan":
            if current[key] != translation_units[uid]["terjemahan"]:
                fail_translation(f"{uid}: Terjemahan differs from Batch 01 payload")
        elif current[key] != value:
            fail_translation(f"{uid}: protected field changed: {key}")

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
      "paket unggahan 2026-10-28; batch semantik M16–M64, M06–M15/M72–M121, dan batch "
      "terakhir M68/M70/M71 telah dikurasi setingkat pilot (catatan dipilih dari catatan "
      "lama, Khususiyah tingkat frasa, stub/kontradiksi Metode yang terbukti dikoreksi), "
      "sehingga seluruh 123 unit telah masuk pilot atau salah satu batch semantik. Revisi "
      "total terjemahan bergaya Anwar telah dimulai dengan Batch 01 untuk SAMPUL dan "
      "M01–M05 (hanya Lapis 3 yang ditulis ulang; Arab/Latin dipertahankan). Crop "
      "wafaq adalah crop presisi kiriman pengguna, bukan ekstraksi FINAL KHATAM. Aturan lapis "
      "kondisional 2026-10-28: SAMPUL tampil 3 lapis (catatan sampul di akhir Terjemahan), "
      "M01 (Muqodimah) dan M122 (Khatimah) tampil 4 lapis, unit lain 5 lapis.", "",
      "> Dokumen ini adalah revisi terjemahan dokumenter. Metode yang dinisbatkan kepada penulis "
      "kitab tidak disajikan sebagai anjuran, terapi, atau jaminan hasil, dan bukan pengganti "
      "penanganan medis.", ""]
md += source_header + [""]
for u in units:
    md += render_unit_md(u)

(ROOT / "al_qorin/REVISI_AL_QORIN_123.md").write_text("\n".join(md), encoding="utf-8")
print(
    f"integrated units={len(units)} pilot_substituted={len(pilot)} "
    f"selective_overrides={len(selective_units)} "
    f"batch_m16_m64={len(batch_units)} "
    f"batch_m06_m15_m72_m121={len(batch2_units)} "
    f"batch_final_m68_m70_m71={len(final_units)} "
    f"terjemahan_total_b01={len(translation_units)} "
    f"crops={sum(bool(u['crop_page']) for u in units)}"
)
