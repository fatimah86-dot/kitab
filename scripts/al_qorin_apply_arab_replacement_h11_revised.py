#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the user's revised M11 Arabic text to both Markdown masters.

Only the ``### 1. Arab`` subsection of M11 is replaced.  The revised page
contains no clean-edition process markers, so the same three paragraphs are
used in the integrated research master and the clean reading edition.
"""
import argparse
from pathlib import Path

from al_qorin_apply_arab_replacement_h62 import apply_to_json, replace_arab_in_markdown
from al_qorin_parse_user_arab_replacement_h11_revised import (
    load_user_arab_replacement_h11_revised,
)

ROOT = Path(__file__).resolve().parents[1]


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
        "old_target_paragraphs": old_counts["M11"],
        "new_target_paragraphs": len(replacement_units["M11"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    replacement_units = load_user_arab_replacement_h11_revised(ROOT)["units"]
    for path in (
        ROOT / "al_qorin/REVISI_AL_QORIN_123.md",
        ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
    ):
        result = apply_to_markdown(path, replacement_units, check=args.check)
        print(
            f"markdown {result['path']} changed={result['changed']} "
            f"target_paragraphs={result['old_target_paragraphs']}->"
            f"{result['new_target_paragraphs']}"
        )
    for path in args.json:
        result = apply_to_json(path, replacement_units, check=args.check)
        print(f"json {result['path']} changed={result['changed']}")


if __name__ == "__main__":
    main()
