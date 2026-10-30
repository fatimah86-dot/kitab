#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the agent-prepared Fusha Arabic revision to both masters.

Only the ``### 1. Arab`` subsections of M71, M72, M73, M77, M99, M107,
M108, M110, M111, M112, M113, M114, M117, and M118 are replaced.  For
M71, M72, M73, and M77, the source ``[gambar wafak]`` marker becomes
that unit's existing user crop in generated Markdown; the shared
transform removes the legacy crop placement so every crop appears once.
"""
import argparse
from pathlib import Path

from al_qorin_apply_arab_replacement_h62 import apply_to_json, replace_arab_in_markdown
from al_qorin_parse_agent_arab_fusha_remaining import (
    ORDER_REVISED,
    load_agent_arab_fusha_remaining,
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

    replacement_units = load_agent_arab_fusha_remaining(ROOT)["units"]
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
