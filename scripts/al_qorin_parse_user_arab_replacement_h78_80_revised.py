#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for pages 78 and 80.

This later submission supersedes only those two segments of the pages
63-122 archive.  Every non-empty body line is one source paragraph,
including an exact ``[gambar wafak]`` marker paragraph on M78.  Renderers
convert that marker into the unit's existing user crop.
"""
from pathlib import Path

ORDER_REVISED = ["M78", "M80"]
EXPECTED_COUNTS = {"M78": 3, "M80": 5}
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h78_80_revised/"
    "teks arab halaman 78 dan 80 revisi.txt"
)
HEADINGS = {
    "Halaman 78": "M78",
    "Halaman 80": "M80",
}
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h78_80_revised(path):
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
    if units["M78"].count(WAFAQ_MARKER) != 1:
        raise ValueError(f"M78: expected exactly one {WAFAQ_MARKER} marker")
    if WAFAQ_MARKER in units["M80"]:
        raise ValueError("M80: unexpected wafaq marker")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h78_80_revised(root):
    return parse_user_arab_replacement_h78_80_revised(
        Path(root) / ARCHIVE_PATH
    )


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h78_80_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        "arab_replacement_h78_80_revised: "
        f"units={len(parsed['units'])} paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
