#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for pages 93 and 96.

This later submission supersedes only those two segments of the pages
63-122 archive.  Every non-empty body line is one source paragraph.
Neither page contains a wafaq marker or user crop.  The first M93
paragraph begins with a literal asterisk; Markdown renderers escape
only that leading character in generated Markdown so Word/HTML display
the asterisk instead of treating it as list or emphasis markup.
"""
from pathlib import Path

ORDER_REVISED = ["M93", "M96"]
EXPECTED_COUNTS = {"M93": 6, "M96": 7}
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h93_96_revised/"
    "teks arab halaman 93 dan 96 revisi.txt"
)
HEADINGS = {
    "Halaman 93": "M93",
    "Halaman 96": "M96",
}
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h93_96_revised(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    units = {}
    headings = {}
    current = None
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if line in HEADINGS:
            current = HEADINGS[line]
            if current in units:
                raise ValueError(f"duplicate heading for {current} in {path}")
            units[current] = []
            headings[current] = line
            continue
        if current is None or not line:
            continue
        units[current].append(line)

    if list(units) != ORDER_REVISED:
        raise ValueError(f"unit order mismatch in {path}")
    counts = {uid: len(paragraphs) for uid, paragraphs in units.items()}
    if counts != EXPECTED_COUNTS or any(
        not paragraph for paragraphs in units.values() for paragraph in paragraphs
    ):
        raise ValueError(f"unexpected paragraph counts in {path}: {counts}")
    if any(
        WAFAQ_MARKER in paragraph
        for paragraphs in units.values()
        for paragraph in paragraphs
    ):
        raise ValueError(f"unexpected {WAFAQ_MARKER} marker in {path}")
    if not units["M93"][0].startswith("* "):
        raise ValueError("M93: expected a literal leading asterisk")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h93_96_revised(root):
    return parse_user_arab_replacement_h93_96_revised(
        Path(root) / ARCHIVE_PATH
    )


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h93_96_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        "arab_replacement_h93_96_revised: "
        f"units={len(parsed['units'])} paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
