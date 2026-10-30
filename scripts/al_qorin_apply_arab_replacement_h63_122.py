#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the user's M63-M122 Arabic replacement to Markdown/JSON outputs.

The integrated research master receives the archived paragraphs exactly.
The clean reading edition receives the same paragraphs after its existing
``strip_work_markers`` presentation step, which removes only explicit
Indonesian extraction/process notes such as ``[bersambung]``.  Headings and
every layer other than ``### 1. Arab`` are preserved.
"""
import argparse
from pathlib import Path

from al_qorin_apply_arab_replacement_h62 import apply_to_json, replace_arab_in_markdown
from al_qorin_build_clean_user_edition import strip_work_markers
from al_qorin_parse_user_arab_replacement_h63_122 import (
    ORDER_H63_122,
    load_user_arab_replacement_h63_122,
)

ROOT = Path(__file__).resolve().parents[1]


def clean_replacement_units(units):
    cleaned = {}
    for uid in ORDER_H63_122:
        paragraphs = [strip_work_markers(p) for p in units[uid]]
        if any(not p for p in paragraphs):
            raise ValueError(f"{uid}: clean presentation produced an empty paragraph")
        cleaned[uid] = paragraphs
    return cleaned


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
        "old_target_paragraphs": sum(old_counts[uid] for uid in ORDER_H63_122),
        "new_target_paragraphs": sum(
            len(replacement_units[uid]) for uid in ORDER_H63_122
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    exact_units = load_user_arab_replacement_h63_122(ROOT)["units"]
    jobs = [
        (ROOT / "al_qorin/REVISI_AL_QORIN_123.md", exact_units, "exact"),
        (
            ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
            clean_replacement_units(exact_units),
            "clean",
        ),
    ]
    for path, replacement_units, mode in jobs:
        result = apply_to_markdown(path, replacement_units, check=args.check)
        print(
            f"markdown[{mode}] {result['path']} changed={result['changed']} "
            f"target_paragraphs={result['old_target_paragraphs']}->"
            f"{result['new_target_paragraphs']}"
        )
    for path in args.json:
        result = apply_to_json(path, exact_units, check=args.check)
        print(f"json {result['path']} changed={result['changed']}")


if __name__ == "__main__":
    main()
