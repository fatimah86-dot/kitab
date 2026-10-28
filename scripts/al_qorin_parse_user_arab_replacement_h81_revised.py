#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for page 81.

This later one-page submission supersedes only the M81 segment of the
pages 63-122 archive.  Every non-empty body line is one source paragraph.
The revised page contains no wafaq marker and page 81 has no user crop.
"""
from pathlib import Path

ORDER_REVISED = ["M81"]
EXPECTED_COUNT = 6
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/"
    "arab_replacement_h81_revised/"
    "teks arab halaman 81 revisi.txt"
)
HEADING = "Halaman 81"
WAFAQ_MARKER = "[gambar wafak]"


def parse_user_arab_replacement_h81_revised(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    nonempty = [line for line in lines if line]
    if not nonempty or nonempty[0] != HEADING:
        raise ValueError(f"unexpected page-81 heading in {path}")
    paragraphs = nonempty[1:]
    if len(paragraphs) != EXPECTED_COUNT or any(not p for p in paragraphs):
        raise ValueError(f"expected six Arabic paragraphs in {path}")
    if WAFAQ_MARKER in paragraphs:
        raise ValueError("M81: unexpected wafaq marker")
    return {"headings": {"M81": HEADING}, "units": {"M81": paragraphs}}


def load_user_arab_replacement_h81_revised(root):
    return parse_user_arab_replacement_h81_revised(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h81_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(f"arab_replacement_h81_revised: units=1 paragraphs={paragraphs}")


if __name__ == "__main__":
    main()
