#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's replacement Arabic text for pages 63-122.

The archived complete code-block submission starts with the unnumbered
heading ``Halaman 63, ...``; subsequent headings are ``64``--``122``.  They
map one-to-one to units ``M63``--``M122``.  Every non-empty body line is one
Arabic paragraph, matching the supplied layout.  A leading Markdown-style
``*`` marker is list punctuation from the submission, not part of the Arabic
sentence, and is removed by the parser.
"""
import re
from pathlib import Path

ORDER_H63_122 = [f"M{i:02d}" for i in range(63, 123)]
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/arab_replacement_h63_122/"
    "teks arab pengganti halaman 63-122.txt"
)
FIRST_HEADING_RE = re.compile(r"^Halaman 63,[ ].*$")
HEADING_RE = re.compile(r"^(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-2])\s+—\s+.*$")


def parse_user_arab_replacement_h63_122(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    units = {}
    headings = {}
    current = None

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if FIRST_HEADING_RE.match(line):
            current = "M63"
            if current in units:
                raise ValueError(f"duplicate heading for {current} in {path}")
            units[current] = []
            headings[current] = line
            continue
        match = HEADING_RE.match(line)
        if match:
            current = f"M{int(match.group(1)):02d}"
            if current in units:
                raise ValueError(f"duplicate heading for {current} in {path}")
            units[current] = []
            headings[current] = line
            continue
        if current is None or not line:
            continue
        paragraph = re.sub(r"^\*\s+", "", line)
        units[current].append(paragraph)

    if list(units) != ORDER_H63_122:
        missing = [uid for uid in ORDER_H63_122 if uid not in units]
        extra = [uid for uid in units if uid not in ORDER_H63_122]
        raise ValueError(
            f"unit order mismatch in {path}: missing={missing} extra={extra}"
        )
    if any(not paragraphs or any(not p.strip() for p in paragraphs)
           for paragraphs in units.values()):
        raise ValueError(f"empty Arabic paragraph in {path}")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h63_122(root):
    return parse_user_arab_replacement_h63_122(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h63_122(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        f"arab_replacement_h63_122: units={len(parsed['units'])} "
        f"paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
