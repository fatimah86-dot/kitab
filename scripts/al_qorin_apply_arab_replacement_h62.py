#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the user's SAMPUL-M62 Arabic replacement to Markdown/JSON outputs.

Only the body under ``### 1. Arab`` is replaced, and only for the 63 units in
the archived replacement.  Headings and every other layer are preserved.
This utility lets the tracked Markdown/DOCX outputs be rebuilt in a checkout
where the ignored full-build work JSON is absent; the long-term source lock
is also wired into ``al_qorin_build_integrated.py``.
"""
import argparse
import copy
import json
import re
from pathlib import Path

from al_qorin_parse_user_arab_replacement_h62 import (
    ORDER_H62,
    load_user_arab_replacement_h62,
)

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
UNIT_HEADING_RE = re.compile(r"^##\s+(.+)$", re.M)
ARAB_SECTION_RE = re.compile(
    r"(### 1\. Arab\n)(.*?)(?=^###\s+|\Z)", re.M | re.S
)


def _uid_from_heading(heading):
    heading = heading.strip()
    return "SAMPUL" if heading == "SAMPUL" else heading.split()[0]


def _split_units(text):
    matches = list(UNIT_HEADING_RE.finditer(text))
    if not matches:
        raise ValueError("no unit headings found")
    prefix = text[:matches[0].start()]
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((_uid_from_heading(match.group(1)), text[match.start():end]))
    if [uid for uid, _block in blocks] != ORDER:
        raise ValueError("markdown unit order is not SAMPUL + M01-M122")
    return prefix, blocks


def _arab_paragraphs(block):
    match = ARAB_SECTION_RE.search(block)
    if not match:
        raise ValueError("missing ### 1. Arab section")
    body = match.group(2).strip()
    return [p.strip() for p in body.split("\n\n") if p.strip()]


def replace_arab_in_markdown(text, replacement_units):
    prefix, blocks = _split_units(text)
    old_counts = {}
    output = [prefix]
    for uid, block in blocks:
        old_counts[uid] = len(_arab_paragraphs(block))
        if uid not in replacement_units:
            output.append(block)
            continue
        match = ARAB_SECTION_RE.search(block)
        if not match:
            raise ValueError(f"{uid}: missing ### 1. Arab section")
        replacement = (
            match.group(1) + "\n" + "\n\n".join(replacement_units[uid]) + "\n\n"
        )
        output.append(block[:match.start()] + replacement + block[match.end():])
    new_text = "".join(output)
    # Verify by reparsing the result: target Arabic must match exactly and
    # the unit order must remain the locked 123-unit order.
    _prefix, check_blocks = _split_units(new_text)
    for uid, block in check_blocks:
        if uid in replacement_units and _arab_paragraphs(block) != replacement_units[uid]:
            raise ValueError(f"{uid}: replacement verification failed")
    return new_text, old_counts


def apply_to_markdown(path, replacement_units, check=False):
    path = Path(path)
    old_text = path.read_text(encoding="utf-8")
    new_text, old_counts = replace_arab_in_markdown(old_text, replacement_units)
    changed = new_text != old_text
    if changed and not check:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "old_target_paragraphs": sum(old_counts[uid] for uid in ORDER_H62),
        "new_target_paragraphs": sum(len(replacement_units[uid]) for uid in ORDER_H62),
    }


def apply_to_json(path, replacement_units, check=False):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or [u.get("unit_id") for u in data] != ORDER:
        raise ValueError(f"{path}: JSON unit order is not SAMPUL + M01-M122")
    before = copy.deepcopy(data)
    for unit in data:
        uid = unit["unit_id"]
        if uid in replacement_units:
            unit["arab"] = list(replacement_units[uid])
    for old, new in zip(before, data):
        for key, value in old.items():
            if key != "arab" and new.get(key) != value:
                raise ValueError(f"{path}: protected field changed: {old['unit_id']}:{key}")
    changed = data != before
    if changed and not check:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"path": str(path), "changed": changed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="append", default=[])
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    replacement = load_user_arab_replacement_h62(ROOT)["units"]
    markdown_paths = args.markdown or [
        str(ROOT / "al_qorin/REVISI_AL_QORIN_123.md"),
        str(ROOT / "al_qorin/AL_QORIN_123_BERSIH.md"),
    ]
    for path in markdown_paths:
        result = apply_to_markdown(path, replacement, check=args.check)
        print(
            f"markdown {result['path']} changed={result['changed']} "
            f"target_paragraphs={result['old_target_paragraphs']}->"
            f"{result['new_target_paragraphs']}"
        )
    for path in args.json:
        result = apply_to_json(path, replacement, check=args.check)
        print(f"json {result['path']} changed={result['changed']}")


if __name__ == "__main__":
    main()
