#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse the agent-prepared Fusha Arabic revision for the remaining pages.

At the user's instruction, the agent prepared Arabic for the fourteen
units that still carried ellipses or figure descriptors.  The revision
keeps the existing unit order and paragraph count.  Pages 71 and 72 use
an exact ``[gambar wafak]`` paragraph; pages 73 and 77 use the marker
inside one source paragraph.  The parser rejects ellipses and bracketed
figure descriptions so the archived revision stays closed under these
rules.
"""
from pathlib import Path

ORDER_REVISED = [
    "M71", "M72", "M73", "M77", "M99", "M107", "M108",
    "M110", "M111", "M112", "M113", "M114", "M117", "M118",
]
EXPECTED_COUNTS = {
    "M71": 6,
    "M72": 3,
    "M73": 4,
    "M77": 5,
    "M99": 2,
    "M107": 4,
    "M108": 4,
    "M110": 3,
    "M111": 4,
    "M112": 3,
    "M113": 2,
    "M114": 4,
    "M117": 5,
    "M118": 4,
}
EXPECTED_MARKERS = {
    "M71": 1,
    "M72": 1,
    "M73": 1,
    "M77": 1,
    "M99": 0,
    "M107": 0,
    "M108": 0,
    "M110": 0,
    "M111": 0,
    "M112": 0,
    "M113": 0,
    "M114": 0,
    "M117": 0,
    "M118": 0,
}
ARCHIVE_PATH = (
    "al_qorin/arab_fusha_revised_remaining_2026-10-28/"
    "teks arab fusha halaman tersisa.txt"
)
HEADINGS = {
    f"Halaman {int(uid[1:])}": uid for uid in ORDER_REVISED
}
WAFAQ_MARKER = "[gambar wafak]"


def parse_agent_arab_fusha_remaining(path):
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

    all_paragraphs = [
        paragraph for paragraphs in units.values() for paragraph in paragraphs
    ]
    if any("..." in paragraph for paragraph in all_paragraphs):
        raise ValueError(f"unexpected ellipsis in {path}")
    if any(paragraph.startswith("[رَسْم") for paragraph in all_paragraphs):
        raise ValueError(f"unexpected figure descriptor in {path}")

    marker_counts = {
        uid: sum(paragraph.count(WAFAQ_MARKER) for paragraph in paragraphs)
        for uid, paragraphs in units.items()
    }
    if marker_counts != EXPECTED_MARKERS:
        raise ValueError(
            f"unexpected wafaq marker counts in {path}: {marker_counts}"
        )
    if units["M71"].count(WAFAQ_MARKER) != 1:
        raise ValueError(f"M71: expected one exact {WAFAQ_MARKER} paragraph")
    if units["M72"].count(WAFAQ_MARKER) != 1:
        raise ValueError(f"M72: expected one exact {WAFAQ_MARKER} paragraph")

    for uid, index in (("M73", 3), ("M77", 4)):
        inline_paragraph = units[uid][index]
        if inline_paragraph == WAFAQ_MARKER or WAFAQ_MARKER not in inline_paragraph:
            raise ValueError(f"{uid}: expected an inline wafaq marker")
        before, after = (
            part.strip() for part in inline_paragraph.split(WAFAQ_MARKER, 1)
        )
        if not before or not after:
            raise ValueError(f"{uid}: inline wafaq marker lacks surrounding text")
    return {"headings": headings, "units": units}


def load_agent_arab_fusha_remaining(root):
    return parse_agent_arab_fusha_remaining(Path(root) / ARCHIVE_PATH)


def main():
    root = Path(__file__).resolve().parents[1]
    parsed = load_agent_arab_fusha_remaining(root)
    paragraphs = sum(len(x) for x in parsed["units"].values())
    print(
        "arab_fusha_remaining: "
        f"units={len(parsed['units'])} paragraphs={paragraphs}"
    )


if __name__ == "__main__":
    main()
