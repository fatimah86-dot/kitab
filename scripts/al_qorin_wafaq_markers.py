#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move an existing user crop to a ``[gambar wafak]`` marker.

User-revised Arabic pages use the literal ``[gambar wafak]`` marker to
show where the already supplied precision crop belongs.  The marker may
be a whole paragraph or may occur inside one paragraph; in generated
Markdown the surrounding text is preserved around the same unit's
existing image line (and, in the research master, its crop caption).
The legacy image location is removed so each crop still appears exactly
once.
"""
import argparse
import json
import re
from pathlib import Path

WAFAQ_MARKER = "[gambar wafak]"
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(wafaq_qorin/(\d+)\.jpg\)$")
CAPTION_RE = re.compile(r"^\[Crop halaman \d+ — .*\]$")
ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "al_qorin/wafaq_user_manifest.json"


def _crop_manifest():
    return {
        crop["page"]: crop
        for crop in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["crops"]
    }


def render_wafaq_marker_paragraphs(uid, paragraphs, research):
    """Convert a source marker to the edition's Markdown crop blocks."""
    marker_count = sum(paragraph.count(WAFAQ_MARKER) for paragraph in paragraphs)
    if marker_count == 0:
        return list(paragraphs)
    if marker_count != 1 or not uid.startswith("M"):
        raise ValueError(f"{uid}: invalid {WAFAQ_MARKER} marker")
    page = int(uid[1:])
    manifest = _crop_manifest()
    if page not in manifest:
        raise ValueError(f"{uid}: no existing user crop for page {page}")

    rendered = []
    for paragraph in paragraphs:
        if WAFAQ_MARKER not in paragraph:
            rendered.append(paragraph)
            continue
        before, after = (
            part.strip() for part in paragraph.split(WAFAQ_MARKER, 1)
        )
        if before:
            rendered.append(before)
        if research:
            rendered.append(f"![Crop halaman {page}](wafaq_qorin/{page}.jpg)")
            rendered.append(f"[Crop halaman {page} — {manifest[page]['caption']}]")
        else:
            rendered.append(f"![Wafaq halaman {page}](wafaq_qorin/{page}.jpg)")
        if after:
            rendered.append(after)
    return rendered


def _normalize_blank_runs(lines):
    normalized = []
    blank_run = 0
    for line in lines:
        if line == "":
            blank_run += 1
            if blank_run > 1:
                continue
        else:
            blank_run = 0
        normalized.append(line)
    return normalized


def _following_caption(lines, image_idx):
    for idx in range(image_idx + 1, len(lines)):
        candidate = lines[idx].strip()
        if not candidate:
            continue
        if CAPTION_RE.match(candidate):
            return idx, candidate
        break
    return None, None


def _transform_unit(lines):
    if not lines or not lines[0].startswith("## "):
        return lines, None
    heading = lines[0][3:].strip()
    uid = "SAMPUL" if heading == "SAMPUL" else heading.split()[0]

    try:
        arab_start = lines.index("### 1. Arab")
    except ValueError:
        return lines, None
    arab_end = len(lines)
    for idx in range(arab_start + 1, len(lines)):
        if lines[idx].startswith("### "):
            arab_end = idx
            break

    marker_positions = [
        idx
        for idx in range(arab_start + 1, arab_end)
        if WAFAQ_MARKER in lines[idx]
    ]
    marker_count = sum(
        lines[idx].count(WAFAQ_MARKER)
        for idx in range(arab_start + 1, arab_end)
    )
    legacy_images = [
        idx
        for idx, line in enumerate(lines)
        if not (arab_start < idx < arab_end) and IMAGE_RE.match(line.strip())
    ]

    if not marker_positions:
        arab_images = [
            idx
            for idx in range(arab_start + 1, arab_end)
            if IMAGE_RE.match(lines[idx].strip())
        ]
        if not arab_images or not legacy_images:
            return lines, None
        if len(arab_images) != 1 or len(legacy_images) != 1:
            raise ValueError(f"{uid}: duplicate crop layout is ambiguous")
        arab_page = int(IMAGE_RE.match(lines[arab_images[0]].strip()).group(1))
        legacy_page = int(
            IMAGE_RE.match(lines[legacy_images[0]].strip()).group(1)
        )
        if arab_page != legacy_page:
            raise ValueError(f"{uid}: Lapis 1 and legacy crops differ")
        caption_idx, _caption = _following_caption(lines, legacy_images[0])
        remove = {legacy_images[0]}
        if caption_idx is not None:
            remove.add(caption_idx)
        transformed = [
            line for idx, line in enumerate(lines) if idx not in remove
        ]
        return _normalize_blank_runs(transformed), uid

    if len(marker_positions) != 1 or marker_count != 1:
        raise ValueError(f"{uid}: expected exactly one {WAFAQ_MARKER} marker")
    if len(legacy_images) != 1:
        raise ValueError(
            f"{uid}: expected exactly one existing crop outside Lapis 1, "
            f"found {len(legacy_images)}"
        )
    image_idx = legacy_images[0]
    image_line = lines[image_idx].strip()
    page = int(IMAGE_RE.match(image_line).group(1))
    expected_page = int(uid[1:]) if uid.startswith("M") else None
    if expected_page is not None and page != expected_page:
        raise ValueError(f"{uid}: existing crop page is {page}, not {expected_page}")

    caption_idx, caption_line = _following_caption(lines, image_idx)
    remove = {image_idx}
    if caption_idx is not None:
        remove.add(caption_idx)
    marker_idx = marker_positions[0]
    before, after = (
        part.strip()
        for part in lines[marker_idx].strip().split(WAFAQ_MARKER, 1)
    )
    replacement = []
    if before:
        replacement += [before, ""]
    replacement.append(image_line)
    if caption_line:
        replacement += ["", caption_line]
    if after:
        replacement += ["", after]

    transformed = []
    for idx, line in enumerate(lines):
        if idx in remove:
            continue
        if idx == marker_idx:
            transformed.extend(replacement)
        else:
            transformed.append(line)
    return _normalize_blank_runs(transformed), uid


def transform_markdown_wafaq_markers(text):
    lines = text.splitlines()
    starts = [idx for idx, line in enumerate(lines) if line.startswith("## ")]
    if not starts:
        return text, []

    output = lines[: starts[0]]
    moved = []
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        transformed, uid = _transform_unit(lines[start:end])
        output.extend(transformed)
        if uid:
            moved.append(uid)
    return "\n".join(output).rstrip() + "\n", moved


def apply_to_markdown(path, check=False):
    path = Path(path)
    old_text = path.read_text(encoding="utf-8")
    new_text, moved = transform_markdown_wafaq_markers(old_text)
    changed = new_text != old_text
    if changed and not check:
        path.write_text(new_text, encoding="utf-8")
    return {"path": str(path), "changed": changed, "moved": moved}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path in (
        ROOT / "al_qorin/REVISI_AL_QORIN_123.md",
        ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
    ):
        result = apply_to_markdown(path, check=args.check)
        print(
            f"markdown {result['path']} changed={result['changed']} "
            f"moved={','.join(result['moved'])}"
        )


if __name__ == "__main__":
    main()
