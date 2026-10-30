#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's replacement Arabic text for SAMPUL through page 62.

The archived chat submission begins with one prefatory Indonesian sentence.
Only material from the ``SAMPUL`` heading onward is book content.  Numeric
headings ``1``--``62`` map one-to-one to units ``M01``--``M62``.  Every
non-empty body line is one Arabic paragraph, matching the layout supplied by
the user; a leading Markdown-style ``*`` list marker on pages 52--54 is not
part of the Arabic sentence and is removed by the parser.
"""
import re
from pathlib import Path

ORDER_H62 = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 63)]
ARCHIVE_PATH = (
    "al_qorin/incoming_user_2026-10-28/arab_replacement_h62/"
    "teks arab pengganti sampai halaman 62.txt"
)
HEADING_RE = re.compile(r"^(SAMPUL|[1-9]|[1-5][0-9]|6[0-2])(?:\s+—\s+.*)?$")


def parse_user_arab_replacement_h62(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    units = {}
    headings = {}
    current = None

    for raw_line in text.split("\n"):
        line = raw_line.strip()
        match = HEADING_RE.match(line)
        if match:
            token = match.group(1)
            current = "SAMPUL" if token == "SAMPUL" else f"M{int(token):02d}"
            if current in units:
                raise ValueError(f"duplicate heading for {current} in {path}")
            units[current] = []
            headings[current] = line
            continue
        if current is None or not line:
            continue
        paragraph = re.sub(r"^\*\s+", "", line)
        units[current].append(paragraph)

    if list(units) != ORDER_H62:
        missing = [uid for uid in ORDER_H62 if uid not in units]
        extra = [uid for uid in units if uid not in ORDER_H62]
        raise ValueError(
            f"unit order mismatch in {path}: missing={missing} extra={extra}"
        )
    if any(not paragraphs or any(not p.strip() for p in paragraphs)
           for paragraphs in units.values()):
        raise ValueError(f"empty Arabic paragraph in {path}")
    return {"headings": headings, "units": units}


def load_user_arab_replacement_h62(root):
    return parse_user_arab_replacement_h62(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_user_arab_replacement_h62(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(f"arab_replacement_h62: units={len(parsed['units'])} paragraphs={paragraphs}")


if __name__ == "__main__":
    main()
