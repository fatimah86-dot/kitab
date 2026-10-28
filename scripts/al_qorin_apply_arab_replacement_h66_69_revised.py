#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the user's revised M66-M69 Arabic text to both Markdown masters.

The archived source paragraphs replace ``### 1. Arab`` for M66-M69.  The
shared wafaq-marker transform then moves each unit's existing user crop to
its exact ``[gambar wafak]`` marker and removes the legacy crop location.
"""
import argparse
from pathlib import Path

from al_qorin_apply_arab_replacement_h62 import apply_to_json, replace_arab_in_markdown
from al_qorin_parse_user_arab_replacement_h66_69_revised import (
    ORDER_H66_69_REVISED,
    load_user_arab_replacement_h66_69_revised,
)
from al_qorin_wafaq_markers import (
    render_wafaq_marker_paragraphs,
    transform_markdown_wafaq_markers,
)

ROOT = Path(__file__).resolve().parents[1]


def apply_to_markdown(path, replacement_units, check=False):
    path = Path(path)
    old_text = path.read_text(encoding="utf-8")
    research = path.name == "REVISI_AL_QORIN_123.md"
    rendered_units = {
        uid: render_wafaq_marker_paragraphs(uid, paragraphs, research)
        for uid, paragraphs in replacement_units.items()
    }
    replaced_text, old_counts = replace_arab_in_markdown(
        old_text, rendered_units
    )
    new_text, moved = transform_markdown_wafaq_markers(replaced_text)
    changed = new_text != old_text
    if changed and not check:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "moved": moved,
        "old_target_paragraphs": sum(
            old_counts[uid] for uid in ORDER_H66_69_REVISED
        ),
        "new_target_paragraphs": sum(
            len(replacement_units[uid]) for uid in ORDER_H66_69_REVISED
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    replacement_units = load_user_arab_replacement_h66_69_revised(ROOT)["units"]
    for path in (
        ROOT / "al_qorin/REVISI_AL_QORIN_123.md",
        ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
    ):
        result = apply_to_markdown(path, replacement_units, check=args.check)
        print(
            f"markdown {result['path']} changed={result['changed']} "
            f"target_paragraphs={result['old_target_paragraphs']}->"
            f"{result['new_target_paragraphs']} moved={','.join(result['moved'])}"
        )
    for path in args.json:
        result = apply_to_json(path, replacement_units, check=args.check)
        print(f"json {result['path']} changed={result['changed']}")


if __name__ == "__main__":
    main()
