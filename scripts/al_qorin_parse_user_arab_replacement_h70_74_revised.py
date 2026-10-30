#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for pages 70 and 74.

This later submission supersedes only those two segments of the pages
63-122 archive.  Every non-empty body line is one source paragraph,
including an exact ``[gambar wafak]`` marker paragraph.  Renderers convert
that marker into the unit's existing user crop.
"""
from pathlib import Path

ORDER_REVISED = ["M70", "M74"]
EXPECTED_COUNTS = {"M70": 7, "M74": 7}
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h70_74_revised/"
    "teks arab halaman 70 dan 74 revisi.txt"
)
HEADINGS = {
    "(Halaman 70)": "M70",
    "-٧٤- (Halaman 74)": "M74",
}
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h70_74_revised(path):
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
    for uid in ORDER_REVISED:
        if units[uid].count(WAFAQ_MARKER) != 1:
            raise ValueError(f"{uid}: expected exactly one {WAFAQ_MARKER} marker")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h70_74_revised(root):
    return parse_user_arab_replacement_h70_74_revised(
        Path(root) / ARCHIVE_PATH
    )


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h70_74_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        "arab_replacement_h70_74_revised: "
        f"units={len(parsed['units'])} paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
