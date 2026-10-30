#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply guarded Al-Qorin total-translation batches to both Markdown masters.

A batch may rewrite only ``### 3. Terjemahan``.  The research master receives
the JSON paragraphs exactly; the clean master receives the same paragraphs
after the clean edition's established ``clean_translation`` presentation
transform.  Existing Lapis-3 paragraph counts and translator-label counts are
hard guards in both masters.  Arabic, Latin, Syarah/Catatan, Metode,
Khususiyah, tables, crop figures and every non-target unit remain untouched.
"""
import argparse
import json
import re
from pathlib import Path

from al_qorin_build_clean_user_edition import clean_translation

ROOT = Path(__file__).resolve().parents[1]
ALQ = ROOT / "al_qorin"
MASTERS = (
    ALQ / "REVISI_AL_QORIN_123.md",
    ALQ / "AL_QORIN_123_BERSIH.md",
)
BATCH_UNITS = {
    2: [f"M{i:02d}" for i in range(6, 16)],
    3: [f"M{i:02d}" for i in range(16, 33)],
    4: [f"M{i:02d}" for i in range(33, 50)],
    5: [f"M{i:02d}" for i in range(50, 72)],
    6: [f"M{i:02d}" for i in range(72, 87)],
    7: [f"M{i:02d}" for i in range(87, 104)],
    8: [f"M{i:02d}" for i in range(104, 123)],
}
LABEL = "[CATATAN PENERJEMAH"
SECTION_RE = re.compile(
    r"(^### 3\. Terjemahan\n\n)(.*?)(?=^### |\Z)",
    flags=re.M | re.S,
)


def batch_path(number):
    return ALQ / f"overrides_terjemahan_total_batch{number:02d}.json"


def paragraphs(section):
    return [part.strip() for part in section.strip().split("\n\n") if part.strip()]


def load_batch(number):
    path = batch_path(number)
    payload = json.loads(path.read_text(encoding="utf-8"))
    units = payload.get("units")
    expected = BATCH_UNITS[number]
    if not isinstance(units, dict) or list(units) != expected:
        raise SystemExit(
            f"batch {number:02d}: units must be exactly {expected}, got "
            f"{list(units) if isinstance(units, dict) else type(units).__name__}"
        )
    for uid, entry in units.items():
        if not isinstance(entry, dict) or set(entry) != {"dasar", "terjemahan"}:
            raise SystemExit(f"batch {number:02d} {uid}: only dasar+terjemahan allowed")
        if not isinstance(entry["dasar"], str) or len(entry["dasar"].strip()) < 60:
            raise SystemExit(f"batch {number:02d} {uid}: dasar is too short")
        replacement = entry["terjemahan"]
        if (
            not isinstance(replacement, list)
            or not replacement
            or any(not isinstance(x, str) or not x.strip() for x in replacement)
        ):
            raise SystemExit(f"batch {number:02d} {uid}: invalid terjemahan list")
        for paragraph in replacement:
            if "\n" in paragraph or paragraph.startswith(("#", "!", "|")):
                raise SystemExit(
                    f"batch {number:02d} {uid}: paragraph contains a line break or markup"
                )
    return payload


def split_blocks(markdown):
    return re.split(r"(?=^## )", markdown, flags=re.M)


def block_uid(block):
    match = re.match(r"^##\s+(.+)$", block, flags=re.M)
    if not match:
        return None
    heading = match.group(1).strip()
    return "SAMPUL" if heading == "SAMPUL" else heading.split()[0]


def transform_for_master(path, replacement):
    if path.name == "AL_QORIN_123_BERSIH.md":
        transformed = [clean_translation(x) for x in replacement]
        transformed = [x for x in transformed if x]
        return transformed
    return list(replacement)


def apply_to_markdown(path, number, payload, check=False):
    old_text = path.read_text(encoding="utf-8")
    targets = payload["units"]
    output = []
    seen = []
    changed = False
    for block in split_blocks(old_text):
        uid = block_uid(block)
        if uid not in targets:
            output.append(block)
            continue
        seen.append(uid)
        match = SECTION_RE.search(block)
        if not match:
            raise SystemExit(f"{path.name} {uid}: Lapis 3 section not found")
        old_paragraphs = paragraphs(match.group(2))
        replacement = transform_for_master(path, targets[uid]["terjemahan"])
        if len(replacement) != len(old_paragraphs):
            raise SystemExit(
                f"{path.name} {uid}: Lapis-3 paragraph count would change "
                f"{len(old_paragraphs)}->{len(replacement)}"
            )
        old_labels = " \n".join(old_paragraphs).count(LABEL)
        new_labels = " \n".join(replacement).count(LABEL)
        if old_labels != new_labels:
            raise SystemExit(
                f"{path.name} {uid}: translator-label count would change "
                f"{old_labels}->{new_labels}"
            )
        rendered = "\n\n".join(replacement) + "\n\n"
        new_block = block[: match.start(2)] + rendered + block[match.end(2) :]
        changed = changed or new_block != block
        output.append(new_block)
    if seen != BATCH_UNITS[number]:
        raise SystemExit(f"{path.name}: batch units not found in order: {seen}")
    new_text = "".join(output)
    changed = new_text != old_text
    if changed and not check:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "units": len(seen),
        "paragraphs": sum(len(v["terjemahan"]) for v in targets.values()),
    }


def apply_to_json(path, payload, check=False):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"{path}: expected a unit list")
    by_id = {unit.get("unit_id"): unit for unit in data if isinstance(unit, dict)}
    changed = False
    for uid, entry in payload["units"].items():
        unit = by_id.get(uid)
        if unit is None:
            raise SystemExit(f"{path}: missing unit {uid}")
        old = unit.get("terjemahan")
        replacement = entry["terjemahan"]
        if not isinstance(old, list) or len(old) != len(replacement):
            raise SystemExit(f"{path} {uid}: Lapis-3 paragraph count would change")
        if " \n".join(map(str, old)).count(LABEL) != " \n".join(replacement).count(LABEL):
            raise SystemExit(f"{path} {uid}: translator-label count would change")
        if old != replacement:
            unit["terjemahan"] = list(replacement)
            changed = True
    if changed and not check:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
    return {"path": str(path), "changed": changed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True, choices=sorted(BATCH_UNITS))
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = load_batch(args.batch)
    for path in MASTERS:
        result = apply_to_markdown(path, args.batch, payload, check=args.check)
        print(
            f"markdown {result['path']} changed={result['changed']} "
            f"units={result['units']} replacement_paragraphs={result['paragraphs']}"
        )
    for path in args.json:
        result = apply_to_json(path, payload, check=args.check)
        print(f"json {result['path']} changed={result['changed']}")


if __name__ == "__main__":
    main()
