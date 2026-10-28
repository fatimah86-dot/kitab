#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for page 11.

This later one-page submission supersedes only the M11 segment of the
through-page-62 archive.  Its single heading maps to ``M11`` and every
non-empty body line is one Arabic paragraph.
"""
from pathlib import Path

ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/arab_replacement_h11_revised/"
    "teks arab halaman 11 revisi.txt"
)
HEADING = "-١١- (Halaman 11)"


def parse_user_arab_replacement_h11_revised(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    nonempty = [line for line in lines if line]
    if not nonempty or nonempty[0] != HEADING:
        raise ValueError(f"unexpected page-11 heading in {path}")
    paragraphs = nonempty[1:]
    if len(paragraphs) != 3 or any(not p for p in paragraphs):
        raise ValueError(f"expected three Arabic paragraphs in {path}")
    return {"headings": {"M11": HEADING}, "units": {"M11": paragraphs}}


def load_user_arab_replacement_h11_revised(root):
    return parse_user_arab_replacement_h11_revised(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h11_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(f"arab_replacement_h11_revised: units=1 paragraphs={paragraphs}")


if __name__ == "__main__":
    main()
