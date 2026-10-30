#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for pages 84 and 85.

This later submission supersedes only those two segments of the pages
63-122 archive.  Every non-empty body line is one source paragraph.
M84 contains one exact ``[gambar wafak]`` marker paragraph, while the
single M85 marker occurs inside its third paragraph.  Renderers split
that paragraph around the marker and insert the existing user crop
without changing the archived source paragraph.
"""
from pathlib import Path

ORDER_REVISED = ["M84", "M85"]
EXPECTED_COUNTS = {"M84": 8, "M85": 4}
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h84_85_revised/"
    "teks arab halaman 84 dan 85 revisi.txt"
)
HEADINGS = {
    "Halaman 84": "M84",
    "Halaman 85": "M85",
}
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h84_85_revised(path):
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

    marker_counts = {
        uid: sum(paragraph.count(WAFAQ_MARKER) for paragraph in paragraphs)
        for uid, paragraphs in units.items()
    }
    if marker_counts != {"M84": 1, "M85": 1}:
        raise ValueError(f"unexpected wafaq marker counts in {path}: {marker_counts}")
    if units["M84"].count(WAFAQ_MARKER) != 1:
        raise ValueError(f"M84: expected one exact {WAFAQ_MARKER} paragraph")

    inline_paragraph = units["M85"][2]
    if inline_paragraph == WAFAQ_MARKER or WAFAQ_MARKER not in inline_paragraph:
        raise ValueError("M85: expected its marker inside the third paragraph")
    before, after = (
        part.strip() for part in inline_paragraph.split(WAFAQ_MARKER, 1)
    )
    if not before or not after:
        raise ValueError("M85: inline wafaq marker lacks surrounding text")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h84_85_revised(root):
    return parse_user_arab_replacement_h84_85_revised(
        Path(root) / ARCHIVE_PATH
    )


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h84_85_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        "arab_replacement_h84_85_revised: "
        f"units={len(parsed['units'])} paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
