#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build derived Al-Qorin Markdown editions with page labels.

The transformer never writes to its input.  It implements the requested
presentation-level cleanup on a copy:

* Markdown unit headings ``M10`` become a single ``Halaman 10`` label;
  repeated page wording already present in the heading is removed.
* Other standalone ``M<digits>`` references become ``Halaman <digits>``.
* A whole sentence containing ``klaim penulis`` (case-insensitive,
  including the overlapped substring in ``diklaim penulis``) or
  ``Batch <digits>`` is removed.
* ``[CATATAN PENERJEMAH: ...]`` labels, image lines, layer headings,
  tables' cell structure, and crop references are preserved.

This is a derived-edition builder only; the canonical Khatam masters
and DOCX files are intentionally not modified.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAIRS = (
    (
        ROOT / "al_qorin/REVISI_AL_QORIN_123.md",
        ROOT / "al_qorin/REVISI_AL_QORIN_123_HALAMAN.md",
    ),
    (
        ROOT / "al_qorin/AL_QORIN_123_BERSIH.md",
        ROOT / "al_qorin/AL_QORIN_123_BERSIH_HALAMAN.md",
    ),
)

LABEL_RE = re.compile(r"\[CATATAN PENERJEMAH:[^\]]*\]")
KLAIM_RE = re.compile(r"klaim\s+penulis", re.IGNORECASE)
BATCH_RE = re.compile(r"\bBatch\s+\d+\b", re.IGNORECASE)
TARGET_RES = (KLAIM_RE, BATCH_RE)
MREF_RE = re.compile(r"\bM(\d+)\b")
UNIT_HEADING_RE = re.compile(r"^(##\s+)M(\d{2,3})\s+—\s+(.+)$")
IMAGE_LINE_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$")
PREFIX_RE = re.compile(r"^(\s*(?:>\s*)?(?:[-*+]\s+|\d+[.)]\s+)?)(.*)$")
ABBREVIATIONS = {
    "a", "an", "ay", "b", "c", "cet", "cit", "dll", "dr", "dsb", "dst",
    "ed", "hal", "hlm", "ibid", "loc", "mis", "no", "prof", "qs", "s",
    "terj", "ttg", "vol",
}
TERMINALS = ".!?؟"
CLOSERS = "”’\"'»›)]}*"
OPENERS = "“«\"'([{*"


@dataclass
class Stats:
    headings_changed: int = 0
    body_refs_changed: int = 0
    sentences_removed_klaim: int = 0
    sentences_removed_batch: int = 0
    lines_changed: int = 0
    lines_emptied: int = 0
    removed_sentences: list[str] = field(default_factory=list)

    @property
    def sentences_removed(self) -> int:
        return self.sentences_removed_klaim + self.sentences_removed_batch


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_arabic(char: str) -> bool:
    return bool(char and re.match(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]", char))


def _starts_sentence(char: str) -> bool:
    return bool(char and (char.isupper() or char.isdigit() or char in OPENERS or _is_arabic(char)))


def _preceding_token(text: str, end: int) -> str:
    start = end
    while start > 0 and text[start - 1].isalpha():
        start -= 1
    return text[start:end]


def _is_sentence_boundary(text: str, punct_at: int, after_closers: int) -> bool:
    """Return True when the punctuation at punct_at plausibly ends a sentence."""

    if after_closers >= len(text):
        return True

    punct = text[punct_at]
    following = text[after_closers]

    if punct == ".":
        # Decimal points and alphanumeric strings such as file suffixes.
        if punct_at > 0 and text[punct_at - 1].isdigit() and following.isdigit():
            return False
        token = _preceding_token(text, punct_at)
        if token.lower() in ABBREVIATIONS:
            return False
        if len(token) == 1 and token.isupper():
            return False

    probe = after_closers
    while probe < len(text) and text[probe].isspace():
        probe += 1
    if probe >= len(text):
        return True
    return _starts_sentence(text[probe])


def split_sentences(text: str) -> list[str]:
    """Split one Markdown paragraph line into conservative sentence spans."""

    sentences: list[str] = []
    start = 0
    i = 0
    while i < len(text):
        char = text[i]
        if char not in TERMINALS:
            i += 1
            continue

        # An ellipsis is normally a continuation marker in this corpus.
        if char == "." and text.startswith("...", i):
            i += 3
            continue
        if char == "…":
            i += 1
            continue

        end = i + 1
        # Consume combined terminal punctuation such as ?! before closers.
        while end < len(text) and text[end] in "!?؟":
            end += 1
        while end < len(text) and text[end] in CLOSERS:
            end += 1

        if _is_sentence_boundary(text, i, end):
            sentence = text[start:end].strip()
            if sentence:
                sentences.append(sentence)
            start = end
            while start < len(text) and text[start].isspace():
                start += 1
            i = start
        else:
            i = end

    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences


def remove_target_sentences(text: str, stats: Stats) -> str:
    if not any(pattern.search(text) for pattern in TARGET_RES):
        return text

    kept: list[str] = []
    for sentence in split_sentences(text):
        has_klaim = bool(KLAIM_RE.search(sentence))
        has_batch = bool(BATCH_RE.search(sentence))
        if has_klaim or has_batch:
            if has_klaim:
                stats.sentences_removed_klaim += 1
            if has_batch:
                stats.sentences_removed_batch += 1
            stats.removed_sentences.append(sentence)
            continue
        kept.append(sentence)
    return " ".join(kept).strip()


def replace_body_refs(text: str, stats: Stats) -> str:
    def repl(match: re.Match[str]) -> str:
        stats.body_refs_changed += 1
        return f"Halaman {int(match.group(1))}"

    return MREF_RE.sub(repl, text)


def transform_text_span(text: str, stats: Stats) -> str:
    """Apply sentence removal and M-reference renaming outside labels."""

    if not text:
        return text

    pieces = LABEL_RE.split(text)
    labels = LABEL_RE.findall(text)
    if not labels:
        return replace_body_refs(remove_target_sentences(text, stats), stats)

    out: list[str] = []
    for index, piece in enumerate(pieces):
        transformed = replace_body_refs(
            remove_target_sentences(piece.strip(), stats), stats
        )
        if transformed:
            out.append(transformed)
        if index < len(labels):
            out.append(labels[index])
    return " ".join(out).strip()


def transform_line_body(body: str, stats: Stats) -> str:
    prefix_match = PREFIX_RE.match(body)
    if not prefix_match:
        return transform_text_span(body, stats)
    prefix, content = prefix_match.group(1), prefix_match.group(2)
    transformed = transform_text_span(content, stats)
    if not transformed:
        return ""
    return f"{prefix}{transformed}" if prefix else transformed


def split_table_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    body = stripped[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return re.split(r"(?<!\\)\|", body)


def transform_table_line(line: str, stats: Stats) -> str | None:
    cells = split_table_cells(line)
    if cells is None:
        return None
    transformed = [transform_text_span(cell.strip(), stats) for cell in cells]
    return "| " + " | ".join(transformed) + " |"


def transform_heading(line: str, stats: Stats) -> str | None:
    match = UNIT_HEADING_RE.match(line)
    if not match:
        return None
    number = int(match.group(2))
    title = match.group(3).strip()
    title = re.sub(
        rf"^Halaman\s+0*{number}\s*[,—:-]\s*", "", title, flags=re.IGNORECASE
    )
    title = re.sub(
        rf"\s*,\s*HALAMAN\s+0*{number}\s*$", "", title, flags=re.IGNORECASE
    )
    stats.headings_changed += 1
    return f"## Halaman {number} — {title}"


def transform_markdown(text: str, stats: Stats) -> str:
    out_lines: list[str] = []
    in_fence = False

    for original in text.splitlines():
        line = original.rstrip("\n")
        stripped = line.lstrip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        heading = transform_heading(line, stats)
        if heading is not None:
            changed = heading
        elif IMAGE_LINE_RE.match(line):
            changed = line
        elif line.startswith("#"):
            # Layer/subsection headings are structural.  Only standalone
            # references in top-level/front-matter headings are renamed.
            changed = replace_body_refs(line, stats) if line.startswith("# ") else line
        elif stripped.startswith("|"):
            changed = transform_table_line(line, stats) or line
        else:
            changed = transform_line_body(line, stats)

        if changed != line:
            stats.lines_changed += 1
            if line.strip() and not changed.strip():
                stats.lines_emptied += 1
        out_lines.append(changed)

    result = "\n".join(out_lines)
    if text.endswith("\n"):
        result += "\n"
    return result


def structural_counts(text: str) -> dict[str, int]:
    return {
        "unit_or_page_headings": len(re.findall(r"^##\s+", text, flags=re.M)),
        "layer_headings": len(re.findall(r"^###\s+", text, flags=re.M)),
        "subsection_headings": len(re.findall(r"^####\s+", text, flags=re.M)),
        "images": len(re.findall(r"^\s*!\[[^\]]*\]\([^)]+\)\s*$", text, flags=re.M)),
        "translator_labels": len(LABEL_RE.findall(text)),
        "remaining_m_refs": len(MREF_RE.findall(text)),
        "remaining_klaim_penulis": len(KLAIM_RE.findall(text)),
        "remaining_batch_numbered": len(BATCH_RE.findall(text)),
    }


def build_one(source: Path, output: Path) -> dict[str, object]:
    source = source.resolve()
    output = output.resolve()
    if source == output:
        raise ValueError("output must not overwrite its input")

    source_bytes = source.read_bytes()
    source_text = source_bytes.decode("utf-8")
    before = structural_counts(source_text)
    stats = Stats()
    output_text = transform_markdown(source_text, stats)
    after = structural_counts(output_text)

    invariant_keys = (
        "unit_or_page_headings",
        "layer_headings",
        "subsection_headings",
        "images",
        "translator_labels",
    )
    for key in invariant_keys:
        if before[key] != after[key]:
            raise AssertionError(f"structural count changed for {key}: {before[key]} -> {after[key]}")
    if after["remaining_m_refs"] != 0:
        raise AssertionError(f"standalone M references remain: {after['remaining_m_refs']}")
    if after["remaining_klaim_penulis"] != 0:
        raise AssertionError(
            f"'klaim penulis' remains after sentence removal: {after['remaining_klaim_penulis']}"
        )
    if after["remaining_batch_numbered"] != 0:
        raise AssertionError(
            f"numbered Batch references remain: {after['remaining_batch_numbered']}"
        )
    if stats.headings_changed != 122:
        raise AssertionError(f"expected 122 transformed page headings, got {stats.headings_changed}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output_bytes = output_text.encode("utf-8")
    output.write_bytes(output_bytes)

    return {
        "source": str(source),
        "output": str(output),
        "source_sha256": sha256_bytes(source_bytes),
        "output_sha256": sha256_bytes(output_bytes),
        "headings_changed": stats.headings_changed,
        "body_refs_changed": stats.body_refs_changed,
        "sentences_removed_klaim": stats.sentences_removed_klaim,
        "sentences_removed_batch": stats.sentences_removed_batch,
        "sentences_removed_total": stats.sentences_removed,
        "lines_changed": stats.lines_changed,
        "lines_emptied": stats.lines_emptied,
        "before": before,
        "after": after,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="single Markdown input; requires --output")
    parser.add_argument("--output", type=Path, help="single derived Markdown output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if bool(args.input) ^ bool(args.output):
        raise SystemExit("--input and --output must be supplied together")

    pairs = ((args.input, args.output),) if args.input else DEFAULT_PAIRS
    for source, output in pairs:
        if source is None or output is None:
            continue
        result = build_one(source, output)
        print(
            "derived "
            f"source={result['source']} output={result['output']} "
            f"headings={result['headings_changed']} body_refs={result['body_refs_changed']} "
            f"removed_klaim_sentences={result['sentences_removed_klaim']} "
            f"removed_batch_sentences={result['sentences_removed_batch']} "
            f"lines_changed={result['lines_changed']} lines_emptied={result['lines_emptied']} "
            f"sha256={result['output_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
