#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the user's byte-archived Al-Qorin Arabic/Latin text files.

The two files in ``al_qorin/incoming_user_2026-10-28/arab_latin_full/`` are
the user-designated Lapis 1 and Lapis 2 sources for the clean edition.
Only text after the ``SAMPUL`` heading is book content; each file's title
and, for Latin, its prefatory transliteration note are intentionally not
returned as document paragraphs.
"""
import re
from pathlib import Path

ORDER = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
HEADING_RE = re.compile(r"^(SAMPUL|M\d{2,3})(?:\s+—\s+.*)?$")
ARCHIVE_DIR = "al_qorin/incoming_user_2026-10-28/arab_latin_full"
FILES = {
    "arab": "teks arab berharokat.txt",
    "latin": "teks latin.txt",
}


def parse_user_text(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    units = {}
    headings = {}
    current = None
    buffer = []

    def flush():
        nonlocal buffer
        if current is None:
            buffer = []
            return
        paragraphs = []
        block = []
        for line in buffer:
            stripped = line.strip()
            if stripped:
                block.append(stripped)
            elif block:
                paragraphs.append(" ".join(block).strip())
                block = []
        if block:
            paragraphs.append(" ".join(block).strip())
        units[current] = paragraphs
        buffer = []

    for line in text.split("\n"):
        match = HEADING_RE.match(line.strip())
        if match:
            flush()
            current = match.group(1)
            headings[current] = line.strip()
        elif current is not None:
            buffer.append(line)
    flush()
    if list(units) != ORDER:
        missing = [uid for uid in ORDER if uid not in units]
        extra = [uid for uid in units if uid not in ORDER]
        raise ValueError(f"unit order mismatch in {path}: missing={missing} extra={extra}")
    if any(not paragraphs or any(not p for p in paragraphs) for paragraphs in units.values()):
        raise ValueError(f"empty paragraph in {path}")
    return {"headings": headings, "units": units}


def load_user_arab_latin(root):
    root = Path(root)
    return {
        key: parse_user_text(root / ARCHIVE_DIR / filename)
        for key, filename in FILES.items()
    }


def main():
    root = Path(__file__).resolve().parents[1]
    data = load_user_arab_latin(root)
    for key, parsed in data.items():
        paragraphs = sum(len(x) for x in parsed["units"].values())
        print(f"{key}: units={len(parsed['units'])} paragraphs={paragraphs}")


if __name__ == "__main__":
    main()
