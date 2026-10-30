#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for page 76.

This later one-page submission supersedes only the M76 segment of the
pages 63-122 archive.  Every non-empty body line is one source paragraph,
including an exact ``[gambar wafak]`` marker paragraph.  Renderers convert
that marker into the unit's existing user crop.
"""
from pathlib import Path

ORDER_REVISED = ["M76"]
EXPECTED_COUNT = 8
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h76_revised/"
    "teks arab halaman 76 revisi.txt"
)
HEADING = "Halaman 76"
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h76_revised(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    nonempty = [line for line in lines if line]
    if not nonempty or nonempty[0] != HEADING:
        raise ValueError(f"unexpected page-76 heading in {path}")
    paragraphs = nonempty[1:]
    if len(paragraphs) != EXPECTED_COUNT or any(not p for p in paragraphs):
        raise ValueError(f"expected eight Arabic paragraphs in {path}")
    if paragraphs.count(WAFAQ_MARKER) != 1:
        raise ValueError(f"M76: expected exactly one {WAFAQ_MARKER} marker")
    return {"headings": {"M76": HEADING}, "units": {"M76": paragraphs}}


def load_user_arab_replacement_h76_revised(root):
    return parse_user_arab_replacement_h76_revised(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h76_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(f"arab_replacement_h76_revised: units=1 paragraphs={paragraphs}")


if __name__ == "__main__":
    main()
