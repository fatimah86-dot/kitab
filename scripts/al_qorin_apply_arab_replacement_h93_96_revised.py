#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the user's revised M93/M96 Arabic text to both Markdown masters.

Only the ``### 1. Arab`` subsections of M93 and M96 are replaced.  JSON
application receives the raw archived paragraphs.  For Markdown, a
paragraph-initial literal ``*`` is written as ``\*`` so downstream
Markdown, HTML, and DOCX renderers display the asterisk rather than
interpreting it as list or emphasis markup.
"""
import argparse
from pathlib import Path

from al_qorin_apply_arab_replacement_h62 import apply_to_json, replace_arab_in_markdown
from al_qorin_parse_user_arab_replacement_h93_96_revised import (
    ORDER_REVISED,
    load_user_arab_replacement_h93_96_revised,
)

ROOT = Path(__file__).resolve().parents[1]


def render_markdown_paragraph(paragraph):
    if paragraph.startswith("* "):
        return "\\*" + paragraph[1:]
    return paragraph


def apply_to_markdown(path, replacement_units, check=False):
    path = Path(path)
    old_text = path.read_text(encoding="utf-8")
    rendered_units = {
        uid: [render_markdown_paragraph(paragraph) for paragraph in paragraphs]
        for uid, paragraphs in replacement_units.items()
    }
    new_text, old_counts = replace_arab_in_markdown(old_text, rendered_units)
    changed = new_text != old_text
    if changed and not check:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "old_target_paragraphs": sum(old_counts[uid] for uid in ORDER_REVISED),
        "new_target_paragraphs": sum(
            len(replacement_units[uid]) for uid in ORDER_REVISED
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    replacement_units = load_user_arab_replacement_h93_96_revised(ROOT)[
        "units"
    ]
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
