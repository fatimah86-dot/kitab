#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's revised Arabic text for pages 66-69.

This later four-page submission supersedes only the M66-M69 segments of the
pages 63-122 archive.  Headings ``Halaman 66``--``Halaman 69`` map to
``M66``--``M69``, and every non-empty body line is one Arabic paragraph.
"""
import re
from pathlib import Path

ORDER_H66_69_REVISED = ["M66", "M67", "M68", "M69"]
EXPECTED_COUNTS = {"M66": 5, "M67": 6, "M68": 5, "M69": 5}
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/arab_replacement_h66_69_revised/"
    "teks arab halaman 66-69 revisi.txt"
)
HEADING_RE = re.compile(r"^Halaman (66|67|68|69),[ ].*$")


def parse_user_arab_replacement_h66_69_revised(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    units = {}
    headings = {}
    current = None

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        match = HEADING_RE.match(line)
        if match:
            current = f"M{match.group(1)}"
            if current in units:
                raise ValueError(f"duplicate heading for {current} in {path}")
            units[current] = []
            headings[current] = line
            continue
        if current is None or not line:
            continue
        units[current].append(line)

    if list(units) != ORDER_H66_69_REVISED:
        raise ValueError(f"unit order mismatch in {path}")
    counts = {uid: len(paragraphs) for uid, paragraphs in units.items()}
    if counts != EXPECTED_COUNTS or any(
        not paragraph for paragraphs in units.values() for paragraph in paragraphs
    ):
        raise ValueError(f"unexpected paragraph counts in {path}: {counts}")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h66_69_revised(root):
    return parse_user_arab_replacement_h66_69_revised(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h66_69_revised(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        f"arab_replacement_h66_69_revised: units={len(parsed['units'])} "
        f"paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
