"""Structural/compliance tests for the Al-Qorin 123-unit standard pilot.

These tests prove file structure, logged deletions, crop identity, DOCX XML
direction/alignment, and recoverability of the embedded Amiri fonts. They do
not by themselves prove semantic completion of all 123 units.
"""
import hashlib
import json
import re
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
ALQ = ROOT / "al_qorin"
FULL_MD = ALQ / "REVISI_AL_QORIN_123_KERJA.md"
INTEGRATED_MD = ALQ / "REVISI_AL_QORIN_123.md"
PILOT_MD = ALQ / "REVISI_AL_QORIN_PILOT.md"
PILOT_DOCX = ALQ / "AL_QORIN_PILOT_5_LAPIS.docx"
MANIFEST = ALQ / "MANIFEST_WAFAQ_AL_QORIN.md"
USER_MANIFEST_JSON = ALQ / "wafaq_user_manifest.json"
EXPECTED_CROPS = [49, 58, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78,
                  82, 83, 84, 85, 86, 98, 109, 116, 120, 121]
NO_CALC = "«tidak ada hitungan di halaman ini»"
TRANSLATION_B01 = {"SAMPUL", "M01", "M02", "M03", "M04", "M05"}
LAYERS = [
    "1. Arab",
    "2. Latin",
    "3. Terjemahan",
    "4. Metode, Penentuan Jam, dan Catatan Penyunting",
    "5. Khususiyah — Waktu : Media : Bukhur",
]
SUBS = ["1. Metode", "2. Penentuan Jam", "Catatan penyunting"]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
CT = "{http://schemas.openxmlformats.org/package/2006/content-types}"


def unit_blocks(md):
    blocks = []
    for block in re.split(r"(?=^## )", md, flags=re.M):
        m = re.match(r"^##\s+(.+)$", block, flags=re.M)
        if m:
            heading = m.group(1).strip()
            uid = "SAMPUL" if heading == "SAMPUL" else heading.split()[0]
            blocks.append((uid, heading, block))
    return blocks


def subsection(block, heading):
    m = re.search(
        rf"^#### {re.escape(heading)}\n(.*?)(?=^#### |^### |\Z)",
        block,
        flags=re.M | re.S,
    )
    return m.group(1).strip() if m else None


def without_subsection(block, heading):
    return re.sub(
        rf"(^#### {re.escape(heading)}\n)(.*?)(?=^#### |^### |\Z)",
        rf"\1<removed-for-comparison>\n",
        block,
        count=1,
        flags=re.M | re.S,
    )


def without_layer(block, layer):
    return re.sub(
        rf"(^### {re.escape(layer)}\n)(.*?)(?=^### |\Z)",
        rf"\1<removed-for-comparison>\n",
        block,
        count=1,
        flags=re.M | re.S,
    )


H62_ARCHIVE = (
    ALQ / "incoming_user_2026-10-28/arab_replacement_h62/"
    "teks arab pengganti sampai halaman 62.txt"
)
H62_UNITS = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 63)]


def user_arab_replacement_h62():
    replacement = {}
    current = None
    for raw_line in H62_ARCHIVE.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if line == "SAMPUL":
            current = "SAMPUL"
            replacement[current] = []
            continue
        match = re.match(r"^(\d{1,2})\s+—\s+", line)
        if match and 1 <= int(match.group(1)) <= 62:
            current = f"M{int(match.group(1)):02d}"
            replacement[current] = []
            continue
        if current is not None and line:
            replacement[current].append(re.sub(r"^\*\s+", "", line))
    if list(replacement) != H62_UNITS:
        raise AssertionError("H62 replacement headings are incomplete")
    if sum(len(x) for x in replacement.values()) != 277:
        raise AssertionError("H62 replacement paragraph count changed")
    return replacement


def apply_user_arab_replacement_h62(units_by_id):
    replacement = user_arab_replacement_h62()
    for uid, paragraphs in replacement.items():
        if uid in units_by_id:
            units_by_id[uid]["arab"] = list(paragraphs)
    return units_by_id


H63_122_ARCHIVE = (
    ALQ / "incoming_user_2026-10-28/arab_replacement_h63_122/"
    "teks arab pengganti halaman 63-122.txt"
)
H63_122_UNITS = [f"M{i:02d}" for i in range(63, 123)]


def user_arab_replacement_h63_122():
    replacement = {}
    current = None
    for raw_line in H63_122_ARCHIVE.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if line.startswith("Halaman 63,"):
            current = "M63"
            replacement[current] = []
            continue
        match = re.match(r"^(\d{2,3})\s+—\s+", line)
        if match and 64 <= int(match.group(1)) <= 122:
            current = f"M{int(match.group(1)):02d}"
            replacement[current] = []
            continue
        if current is not None and line:
            replacement[current].append(re.sub(r"^\*\s+", "", line))
    if list(replacement) != H63_122_UNITS:
        raise AssertionError("H63-122 replacement headings are incomplete")
    if sum(len(x) for x in replacement.values()) != 267:
        raise AssertionError("H63-122 replacement paragraph count changed")
    return replacement


def apply_user_arab_replacement_h63_122(units_by_id):
    replacement = user_arab_replacement_h63_122()
    for uid, paragraphs in replacement.items():
        if uid in units_by_id:
            units_by_id[uid]["arab"] = list(paragraphs)
    return units_by_id


def clean_user_arab_replacement_h63_122():
    cleaned = {}
    marker_re = re.compile(
        r"\s*\[(?:tidak disalin penuh|bersambung|lanjutan dari segmen|"
        r"baris tidak lengkap)[^\]]*\]",
        re.I,
    )
    for uid, paragraphs in user_arab_replacement_h63_122().items():
        cleaned[uid] = [
            re.sub(r"[ \t]+", " ", marker_re.sub("", paragraph)).strip()
            for paragraph in paragraphs
        ]
    return cleaned


def deobfuscate(data, guid):
    key = bytes.fromhex(guid.strip("{}").replace("-", ""))
    key32 = key[::-1] + key[::-1]
    return bytes(b ^ key32[i] for i, b in enumerate(data[:32])) + data[32:]


class MarkdownStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = FULL_MD.read_text(encoding="utf-8")
        cls.integrated = INTEGRATED_MD.read_text(encoding="utf-8")
        cls.pilot = PILOT_MD.read_text(encoding="utf-8")
        cls.full_blocks = unit_blocks(cls.full)
        cls.integrated_blocks = unit_blocks(cls.integrated)
        cls.pilot_blocks = unit_blocks(cls.pilot)

    def assert_block_shape(self, blocks):
        # Conditional layer rule (2026-10-28): SAMPUL renders layers 1-3,
        # M01 (Muqodimah) and M122 (Khatimah) render layers 1-4, rest 1-5.
        limits = {"SAMPUL": 3, "M01": 4, "M122": 4}
        for uid, _heading, block in blocks:
            expected_layers = LAYERS[:limits.get(uid, 5)]
            self.assertEqual(re.findall(r"^### ([^\n]+)$", block, re.M), expected_layers, uid)
            self.assertEqual(re.findall(r"^#### ([^\n]+)$", block, re.M),
                             [] if uid == "SAMPUL" else SUBS, uid)
            self.assertEqual(block.count(NO_CALC), 0 if uid == "SAMPUL" else 1, uid)
            for layer in expected_layers:
                m = re.search(
                    rf"^### {re.escape(layer)}\n(.*?)(?=^### |\Z)", block, flags=re.M | re.S
                )
                self.assertIsNotNone(m, (uid, layer))
                self.assertGreater(len(m.group(1).strip()), 10, (uid, layer))

    def test_full_123_units_in_order(self):
        expected = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
        self.assertEqual([u for u, _h, _b in self.full_blocks], expected)
        self.assert_block_shape(self.full_blocks)

    def test_integrated_123_and_pilot_substitution(self):
        self.assertEqual([u for u, _h, _b in self.integrated_blocks],
                         [u for u, _h, _b in self.full_blocks])
        self.assert_block_shape(self.integrated_blocks)
        integrated_by_id = {u: b.strip() for u, _h, b in self.integrated_blocks}
        for uid, _h, block in self.pilot_blocks:
            integrated = integrated_by_id[uid]
            pilot = block.strip()
            if uid in TRANSLATION_B01:
                # Total-translation Batch 01 later rewrote only Lapis 3 for
                # SAMPUL and M01-M05; the user's H62 submission later replaced
                # Lapis 1.  Every other rendered part must remain exactly the
                # historical pilot block.
                self.assertEqual(
                    without_layer(without_layer(integrated, LAYERS[0]), LAYERS[2]),
                    without_layer(without_layer(pilot, LAYERS[0]), LAYERS[2]),
                    uid,
                )
                self.assertNotEqual(integrated, pilot, uid)
                continue
            if uid == "M58":
                # Batch M16-M64 later refined only M58's Khususiyah layer and
                # the user's H62 submission later replaced Lapis 1; every
                # other part must remain byte-identical to the pilot.
                self.assertEqual(
                    without_layer(without_layer(integrated, LAYERS[0]), LAYERS[4]),
                    without_layer(without_layer(pilot, LAYERS[0]), LAYERS[4]),
                    uid,
                )
                self.assertIn("wafaq mukhammas 5×5", integrated, uid)
                self.assertIn("crop asli 58.jpg", integrated, uid)
                continue
            if uid in {"M65", "M66", "M67", "M69"}:
                # The user's pages 63-122 submission later replaced only
                # Lapis 1; every other rendered part remains the pilot block.
                self.assertEqual(
                    without_layer(integrated, LAYERS[0]),
                    without_layer(pilot, LAYERS[0]),
                    uid,
                )
                self.assertNotEqual(integrated, pilot, uid)
                continue
            if uid != "M122":
                self.assertEqual(integrated, pilot, uid)
                continue

            # Deliberate post-pilot exceptions: the historical pilot remains
            # unchanged, while integrated M122 may differ inside its Metode
            # subsection and in Lapis 1, which the pages 63-122 submission
            # later replaced. The old Metode summary contradicted M122's own
            # preserved Arab/Terjemahan.
            self.assertEqual(
                without_subsection(without_layer(integrated, LAYERS[0]), "1. Metode"),
                without_subsection(without_layer(pilot, LAYERS[0]), "1. Metode"),
                uid,
            )
            integrated_metode = subsection(integrated, "1. Metode")
            pilot_metode = subsection(pilot, "1. Metode")
            self.assertNotEqual(integrated_metode, pilot_metode, uid)
            for phrase in (
                "salat dua rakaat",
                "berselawat kepada Nabi sepuluh kali",
                "al-Fatihah untuk Syekh Muhammad Sibami",
            ):
                self.assertIn(phrase, integrated_metode, uid)
            for phrase in (
                "berwudu",
                "al-Fatihah sepuluh kali",
                "bertanya kepada",
            ):
                self.assertNotIn(phrase, integrated_metode, uid)

    def test_conditional_layer_rule_and_sampul_notes(self):
        # User decision 2026-10-28: SAMPUL 1-3, M01/M122 1-4, others 1-5.
        integrated_by_id = {u: b for u, _h, b in self.integrated_blocks}
        sampul = integrated_by_id["SAMPUL"]
        self.assertEqual(re.findall(r"^### ([^\n]+)$", sampul, re.M), LAYERS[:3])
        self.assertNotIn("####", sampul)
        for uid in ("M01", "M122"):
            block = integrated_by_id[uid]
            self.assertEqual(re.findall(r"^### ([^\n]+)$", block, re.M), LAYERS[:4], uid)
            self.assertNotIn(LAYERS[4], block, uid)
        # Total rendered layer headings: 123*5 - 2 (SAMPUL) - 1 (M01) - 1 (M122).
        self.assertEqual(len(re.findall(r"^### ", self.integrated, re.M)), 611)
        self.assertEqual(len(re.findall(r"^### ", self.full, re.M)), 611)

        # SAMPUL editor notes must survive at the end of layer 3, marked.
        pilot_path = ALQ / "work/pilot_units.json"
        if not pilot_path.exists():
            self.skipTest("ignored work JSON not present in this checkout")
        pilot = {u["unit_id"]: u for u in json.loads(pilot_path.read_text(encoding="utf-8"))}
        notes = pilot["SAMPUL"]["catatan_penyunting"]
        self.assertGreaterEqual(len(notes), 4)
        layer3 = re.search(
            rf"^### {re.escape(LAYERS[2])}\n(.*?)(?=^### |\Z)", sampul, flags=re.M | re.S
        ).group(1)
        for note in notes:
            self.assertIn("Catatan penyunting sampul: " + note, layer3)
        # The relocated notes must not leak into layer 4/5 of any other unit.
        self.assertEqual(self.integrated.count("Catatan penyunting sampul: "), len(notes))

    def test_full_logged_deletions_and_preserved_labels(self):
        self.assertFalse(any(line.strip().startswith("Qarinah ") for line in self.full.splitlines()))
        self.assertEqual(self.full.count("[CATATAN PENERJEMAH"), 25)
        log = (ALQ / "LOG_RESTRUKTUR_AWAL.md").read_text(encoding="utf-8")
        self.assertIn("= 569", log)
        self.assertIn("Kalimat Qarinah sebaris", log)

    def test_pilot_units_and_crops(self):
        expected = ["SAMPUL", "M01", "M02", "M03", "M04", "M05", "M58", "M65", "M66", "M67", "M69", "M122"]
        self.assertEqual([u for u, _h, _b in self.pilot_blocks], expected)
        self.assert_block_shape(self.pilot_blocks)
        refs = [int(x) for x in re.findall(r"wafaq_qorin/(\d+)\.jpg", self.pilot)]
        self.assertEqual(refs, [58, 65, 66, 67, 69])
        for page in refs:
            self.assertTrue((ALQ / f"wafaq_qorin/{page}.jpg").exists())

    def test_user_crop_manifest_hashes_and_insertion_set(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("Crop Presisi Kiriman Pengguna", manifest)
        rows = []
        for line in manifest.splitlines():
            if re.match(r"^\|\s*\d+\s*\|", line):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        self.assertEqual(len(rows), 26)
        for page, unit, path, _dim, _size, insert, sha in rows:
            self.assertEqual(unit, f"M{int(page):02d}")
            self.assertEqual(insert, "YA")
            p = ROOT / path.strip("`")
            self.assertTrue(p.exists(), path)
            self.assertTrue(hashlib.sha256(p.read_bytes()).hexdigest().startswith(sha.strip("`")))
        data = json.loads(USER_MANIFEST_JSON.read_text(encoding="utf-8"))
        self.assertEqual([c["page"] for c in data["crops"]], EXPECTED_CROPS)
        for c in data["crops"]:
            p = ROOT / c["file"]
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), c["sha256"])
        for md in (self.full, self.integrated):
            refs = [int(x) for x in re.findall(r"wafaq_qorin/(\d+)\.jpg", md)]
            self.assertEqual(refs, EXPECTED_CROPS)

    def test_pilot_source_layers_unchanged_when_work_data_present(self):
        revised_path = ALQ / "work/revised_units.json"
        pilot_path = ALQ / "work/pilot_units.json"
        if not (revised_path.exists() and pilot_path.exists()):
            self.skipTest("ignored work JSON not present in this checkout")
        revised = {u["unit_id"]: u for u in json.loads(revised_path.read_text(encoding="utf-8"))}
        pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
        for u in pilot:
            src = revised[u["unit_id"]]
            for key in ("arab", "latin", "terjemahan", "metode", "rajah_blocks", "jam"):
                self.assertEqual(u[key], src[key], (u["unit_id"], key))

    def test_selective_upload_overrides_are_narrow_when_work_data_present(self):
        override_path = ALQ / "overrides_upload_selektif_2026-10-28.json"
        payload = json.loads(override_path.read_text(encoding="utf-8"))
        selective = payload["units"]
        expected_units = {
            "M68", "M70", "M71", "M104", "M105", "M106", "M107", "M109",
            "M116", "M120", "M121", "M122",
        }
        self.assertEqual(set(selective), expected_units)
        for uid, entry in selective.items():
            self.assertLessEqual(
                set(entry),
                {"dasar", "khususiyah", "catatan_tambah", "metode"},
                uid,
            )
            self.assertTrue(str(entry.get("dasar", "")).strip(), uid)
            if "metode" in entry:
                self.assertEqual(uid, "M122")
            if "khususiyah" in entry:
                self.assertLessEqual(
                    set(entry["khususiyah"]),
                    {"waktu", "media", "bukhur"},
                    uid,
                )

        revised_path = ALQ / "work/revised_units.json"
        pilot_path = ALQ / "work/pilot_units.json"
        integrated_path = ALQ / "work/integrated_units.json"
        if not (revised_path.exists() and pilot_path.exists() and integrated_path.exists()):
            self.skipTest("ignored work JSON not present in this checkout")

        # Reconstruct the exact post-pilot baseline: revised mechanical units
        # with the historical pilot units substituted, before selective edits.
        baseline = {
            u["unit_id"]: json.loads(json.dumps(u, ensure_ascii=False))
            for u in json.loads(revised_path.read_text(encoding="utf-8"))
        }
        for u in json.loads(pilot_path.read_text(encoding="utf-8")):
            baseline[u["unit_id"]] = json.loads(json.dumps(u, ensure_ascii=False))
        # The final integrated work also carries the later user-ordered
        # Arabic replacement through M62; apply that declared stage to the
        # reconstructed baseline before testing this historical stage.
        apply_user_arab_replacement_h62(baseline)
        apply_user_arab_replacement_h63_122(baseline)
        integrated = {
            u["unit_id"]: u
            for u in json.loads(integrated_path.read_text(encoding="utf-8"))
        }
        order = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
        self.assertEqual(set(integrated), set(order))

        change_keys = {"metode", "catatan_penyunting", "khususiyah"}
        # Later semantic batches run after the selective stage, so their units
        # are no longer byte-identical to the post-pilot baseline; they are
        # guarded by dedicated batch tests below. Here we only require that
        # protected fields still match, and for selective units that the final
        # notes/Khususiyah equal the post-selective values after any declared
        # later-batch note selection (M104/M107 appended notes must survive).
        batch_units = {f"M{i:02d}" for i in range(16, 65)}
        batch2_path = ALQ / "overrides_batch_m06_m15_m72_m121.json"
        batch2 = {}
        if batch2_path.exists():
            batch2 = json.loads(batch2_path.read_text(encoding="utf-8"))["units"]
        final_path = ALQ / "overrides_batch_m68_m70_m71.json"
        final_batch = {}
        if final_path.exists():
            final_batch = json.loads(final_path.read_text(encoding="utf-8"))["units"]
        translation_path = ALQ / "overrides_terjemahan_total_batch01.json"
        translation = {}
        if translation_path.exists():
            translation = json.loads(
                translation_path.read_text(encoding="utf-8")
            )["units"]
        later_units = batch_units | set(batch2) | set(final_batch) | set(translation)
        for uid in order:
            base = baseline[uid]
            current = integrated[uid]
            if uid not in expected_units:
                if uid in translation:
                    for key, value in base.items():
                        if key != "terjemahan":
                            self.assertEqual(current[key], value, (uid, key))
                    self.assertEqual(
                        current["terjemahan"],
                        translation[uid]["terjemahan"],
                        uid,
                    )
                elif uid in later_units:
                    for key, value in base.items():
                        if key not in change_keys:
                            self.assertEqual(current[key], value, (uid, key))
                    self.assertEqual(current["jam"], base["jam"], uid)
                else:
                    self.assertEqual(current, base, uid)
                continue

            for key, value in base.items():
                if key not in change_keys:
                    self.assertEqual(current[key], value, (uid, key))
            self.assertEqual(current["jam"], base["jam"], uid)

            entry = selective[uid]
            expected_notes = base["catatan_penyunting"] + list(
                entry.get("catatan_tambah", [])
            )
            later_entries = (batch2.get(uid, {}), final_batch.get(uid, {}))
            for later in later_entries:
                if later.get("notes_groups") is not None:
                    expected_notes = [
                        " ".join(expected_notes[i - 1] for i in g)
                        for g in later["notes_groups"]
                    ]
            self.assertEqual(current["catatan_penyunting"], expected_notes, uid)
            expected_khususiyah = dict(base["khususiyah"])
            expected_khususiyah.update(entry.get("khususiyah", {}))
            for later in later_entries:
                expected_khususiyah.update(later.get("khususiyah", {}))
            self.assertEqual(current["khususiyah"], expected_khususiyah, uid)
            if uid == "M122":
                expected_metode = entry["metode"]
                self.assertNotEqual(current["metode"], base["metode"], uid)
            else:
                expected_metode = base["metode"]
            for later in later_entries:
                if "metode" in later:
                    expected_metode = later["metode"]
                if "metode_first" in later:
                    expected_metode = [later["metode_first"]] + list(
                        expected_metode[1:]
                    )
            self.assertEqual(current["metode"], expected_metode, uid)

        # Guard the two scan-discrepancy notes and the rejected candidate
        # arithmetic. M105's per-name jummal counts remain counts, not an
        # invented hour calculation.
        self.assertEqual(
            integrated["M104"]["catatan_penyunting"][-1],
            selective["M104"]["catatan_tambah"][0],
        )
        self.assertEqual(
            integrated["M107"]["catatan_penyunting"][-1],
            selective["M107"]["catatan_tambah"][0],
        )
        self.assertIn("21 kali", integrated["M107"]["khususiyah"]["waktu"])
        self.assertIn(
            "kata/jenis persisnya tidak dipastikan",
            integrated["M107"]["khususiyah"]["bukhur"],
        )
        self.assertEqual(integrated["M105"]["jam"], [NO_CALC])
        self.assertIn(
            "1072, 535, 1403, 1598, 517, 646, 1813, 1314, 908, dan 1598",
            integrated["M105"]["khususiyah"]["media"],
        )
        self.assertNotIn("11004", " ".join(integrated["M105"]["jam"]))

    def test_batch_m16_m64_overrides_are_narrow_when_work_data_present(self):
        override_path = ALQ / "overrides_batch_m16_m64.json"
        payload = json.loads(override_path.read_text(encoding="utf-8"))
        batch = payload["units"]
        expected_units = {f"M{i:02d}" for i in range(16, 65)}
        metode_allowed = {"M19", "M20", "M21", "M38", "M46"}
        self.assertEqual(set(batch), expected_units)
        for uid, entry in batch.items():
            self.assertLessEqual(
                set(entry),
                {"dasar", "notes_groups", "khususiyah", "metode"},
                uid,
            )
            self.assertTrue(str(entry.get("dasar", "")).strip(), uid)
            self.assertTrue(
                any(k in entry for k in ("notes_groups", "khususiyah", "metode")),
                uid,
            )
            if "metode" in entry:
                self.assertIn(uid, metode_allowed, uid)
                self.assertNotIn(
                    "Petunjuk yang ada dalam sumber:",
                    " ".join(entry["metode"]),
                    uid,
                )
            if "khususiyah" in entry:
                self.assertLessEqual(
                    set(entry["khususiyah"]),
                    {"waktu", "media", "bukhur"},
                    uid,
                )

        revised_path = ALQ / "work/revised_units.json"
        pilot_path = ALQ / "work/pilot_units.json"
        integrated_path = ALQ / "work/integrated_units.json"
        if not (revised_path.exists() and pilot_path.exists() and integrated_path.exists()):
            self.skipTest("ignored work JSON not present in this checkout")

        # Pre-batch baseline for M16-M64 = mechanical units with the pilot
        # substitution (only M58 overlaps); the selective stage does not
        # target any batch unit, so no further adjustment is needed.
        baseline = {
            u["unit_id"]: json.loads(json.dumps(u, ensure_ascii=False))
            for u in json.loads(revised_path.read_text(encoding="utf-8"))
        }
        for u in json.loads(pilot_path.read_text(encoding="utf-8")):
            baseline[u["unit_id"]] = json.loads(json.dumps(u, ensure_ascii=False))
        apply_user_arab_replacement_h62(baseline)
        apply_user_arab_replacement_h63_122(baseline)
        integrated = {
            u["unit_id"]: u
            for u in json.loads(integrated_path.read_text(encoding="utf-8"))
        }

        change_keys = {"metode", "catatan_penyunting", "khususiyah"}
        for uid in sorted(expected_units):
            base = baseline[uid]
            current = integrated[uid]
            entry = batch[uid]
            for key, value in base.items():
                if key not in change_keys:
                    self.assertEqual(current[key], value, (uid, key))
            self.assertEqual(current["jam"], base["jam"], uid)

            groups = entry.get("notes_groups")
            if groups is None:
                expected_notes = base["catatan_penyunting"]
            else:
                flat = [i for g in groups for i in g]
                self.assertEqual(flat, sorted(set(flat)), uid)
                self.assertGreaterEqual(flat[0], 1, uid)
                self.assertLessEqual(flat[-1], len(base["catatan_penyunting"]), uid)
                expected_notes = [
                    " ".join(base["catatan_penyunting"][i - 1] for i in g)
                    for g in groups
                ]
            self.assertEqual(current["catatan_penyunting"], expected_notes, uid)
            # No new note text may appear: every kept paragraph is composed
            # only of whole pre-existing notes.
            for paragraph in current["catatan_penyunting"]:
                for old in base["catatan_penyunting"]:
                    if old in paragraph:
                        break
                else:
                    self.fail(f"{uid}: note paragraph not composed of old notes")

            expected_khususiyah = dict(base["khususiyah"])
            expected_khususiyah.update(entry.get("khususiyah", {}))
            self.assertEqual(current["khususiyah"], expected_khususiyah, uid)
            if uid in metode_allowed:
                self.assertEqual(current["metode"], entry["metode"], uid)
            else:
                self.assertEqual(current["metode"], base["metode"], uid)

        # Spot-check the semantic corrections that motivated the batch.
        unspec = "tidak disebutkan dalam sumber unit ini"
        self.assertTrue(integrated["M19"]["metode"][0].startswith("Tidak ada petunjuk praktik"))
        self.assertTrue(integrated["M46"]["metode"][0].startswith("Tidak ada petunjuk praktik"))
        self.assertTrue(integrated["M38"]["metode"][0].startswith("Peringatan dari sumber"))
        self.assertEqual(integrated["M20"]["khususiyah"]["media"], unspec)
        self.assertIn("tanpa penetapan hari tertentu", integrated["M36"]["khususiyah"]["waktu"])
        self.assertIn("sahur", integrated["M53"]["khususiyah"]["waktu"])
        self.assertIn("wajib menyertai", integrated["M53"]["khususiyah"]["bukhur"])
        self.assertIn("saat tidur", integrated["M50"]["khususiyah"]["waktu"])
        self.assertIn("wafaq mukhammas 5×5", integrated["M58"]["khususiyah"]["media"])
        self.assertIn("crop asli 64.jpg", integrated["M64"]["khususiyah"]["media"])
        self.assertEqual(integrated["M64"]["crop_page"], 64)

    def test_batch_m06_m15_m72_m121_overrides_are_narrow_when_work_data_present(self):
        override_path = ALQ / "overrides_batch_m06_m15_m72_m121.json"
        payload = json.loads(override_path.read_text(encoding="utf-8"))
        batch2 = payload["units"]
        expected_units = (
            {f"M{i:02d}" for i in range(6, 16)}
            | {f"M{i:02d}" for i in range(72, 122)}
        )
        metode_allowed = {"M12", "M79", "M82", "M83"}
        self.assertEqual(set(batch2), expected_units)
        for uid, entry in batch2.items():
            self.assertLessEqual(
                set(entry),
                {"dasar", "notes_groups", "khususiyah", "metode"},
                uid,
            )
            self.assertTrue(str(entry.get("dasar", "")).strip(), uid)
            self.assertTrue(
                any(k in entry for k in ("notes_groups", "khususiyah", "metode")),
                uid,
            )
            if "metode" in entry:
                self.assertIn(uid, metode_allowed, uid)
                self.assertNotIn(
                    "Petunjuk yang ada dalam sumber:",
                    " ".join(entry["metode"]),
                    uid,
                )
            if "khususiyah" in entry:
                self.assertLessEqual(
                    set(entry["khususiyah"]),
                    {"waktu", "media", "bukhur"},
                    uid,
                )

        revised_path = ALQ / "work/revised_units.json"
        pilot_path = ALQ / "work/pilot_units.json"
        integrated_path = ALQ / "work/integrated_units.json"
        selective_path = ALQ / "overrides_upload_selektif_2026-10-28.json"
        batch1_path = ALQ / "overrides_batch_m16_m64.json"
        if not (
            revised_path.exists()
            and pilot_path.exists()
            and integrated_path.exists()
            and selective_path.exists()
            and batch1_path.exists()
        ):
            self.skipTest("ignored work JSON not present in this checkout")

        def cloned(units):
            return {
                u["unit_id"]: json.loads(json.dumps(u, ensure_ascii=False))
                for u in units
            }

        def apply_notes(unit, groups):
            old = unit["catatan_penyunting"]
            unit["catatan_penyunting"] = [
                " ".join(old[i - 1] for i in g) for g in groups
            ]

        # Reconstruct the builder's exact pre-batch2 baseline: mechanical
        # units + pilot substitution + selective overrides + M16-M64 batch.
        baseline = cloned(json.loads(revised_path.read_text(encoding="utf-8")))
        for uid, unit in cloned(
            json.loads(pilot_path.read_text(encoding="utf-8"))
        ).items():
            baseline[uid] = unit
        selective = json.loads(selective_path.read_text(encoding="utf-8"))["units"]
        for uid, entry in selective.items():
            unit = baseline[uid]
            unit["khususiyah"].update(entry.get("khususiyah", {}))
            unit["catatan_penyunting"] += list(entry.get("catatan_tambah", []))
            if "metode" in entry:
                unit["metode"] = list(entry["metode"])
        batch1 = json.loads(batch1_path.read_text(encoding="utf-8"))["units"]
        for uid, entry in batch1.items():
            unit = baseline[uid]
            if entry.get("notes_groups") is not None:
                apply_notes(unit, entry["notes_groups"])
            unit["khususiyah"].update(entry.get("khususiyah", {}))
            if "metode" in entry:
                unit["metode"] = list(entry["metode"])
        apply_user_arab_replacement_h62(baseline)
        apply_user_arab_replacement_h63_122(baseline)

        integrated = {
            u["unit_id"]: u
            for u in json.loads(integrated_path.read_text(encoding="utf-8"))
        }
        order = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
        self.assertEqual(set(integrated), set(order))
        # No spill outside the declared 60-unit batch. The later final batch
        # (M68/M70/M71) is guarded by its own test; here only its protected
        # fields must still match this batch's pre-batch2 baseline.
        final_path = ALQ / "overrides_batch_m68_m70_m71.json"
        final_units = set()
        if final_path.exists():
            final_units = set(
                json.loads(final_path.read_text(encoding="utf-8"))["units"]
            )
        translation_path = ALQ / "overrides_terjemahan_total_batch01.json"
        translation = {}
        if translation_path.exists():
            translation = json.loads(
                translation_path.read_text(encoding="utf-8")
            )["units"]
        change_keys = {"metode", "catatan_penyunting", "khususiyah"}
        for uid in order:
            if uid not in expected_units:
                if uid in translation:
                    for key, value in baseline[uid].items():
                        if key != "terjemahan":
                            self.assertEqual(
                                integrated[uid][key], value, (uid, key)
                            )
                    self.assertEqual(
                        integrated[uid]["terjemahan"],
                        translation[uid]["terjemahan"],
                        uid,
                    )
                elif uid in final_units:
                    for key, value in baseline[uid].items():
                        if key not in change_keys:
                            self.assertEqual(
                                integrated[uid][key], value, (uid, key)
                            )
                    self.assertEqual(
                        integrated[uid]["jam"], baseline[uid]["jam"], uid
                    )
                else:
                    self.assertEqual(integrated[uid], baseline[uid], uid)

        for uid in sorted(expected_units):
            base = baseline[uid]
            current = integrated[uid]
            entry = batch2[uid]
            for key, value in base.items():
                if key not in change_keys:
                    self.assertEqual(current[key], value, (uid, key))
            self.assertEqual(current["jam"], base["jam"], uid)

            groups = entry.get("notes_groups")
            if groups is None:
                expected_notes = base["catatan_penyunting"]
            else:
                flat = [i for g in groups for i in g]
                self.assertEqual(flat, sorted(set(flat)), uid)
                self.assertGreaterEqual(flat[0], 1, uid)
                self.assertLessEqual(
                    flat[-1], len(base["catatan_penyunting"]), uid
                )
                if uid in {"M104", "M107"}:
                    self.assertIn(len(base["catatan_penyunting"]), flat, uid)
                expected_notes = [
                    " ".join(base["catatan_penyunting"][i - 1] for i in g)
                    for g in groups
                ]
            self.assertEqual(current["catatan_penyunting"], expected_notes, uid)
            for paragraph in current["catatan_penyunting"]:
                for old in base["catatan_penyunting"]:
                    if old in paragraph:
                        break
                else:
                    self.fail(f"{uid}: note paragraph not composed of old notes")

            expected_khususiyah = dict(base["khususiyah"])
            expected_khususiyah.update(entry.get("khususiyah", {}))
            self.assertEqual(current["khususiyah"], expected_khususiyah, uid)
            if uid in metode_allowed:
                self.assertEqual(current["metode"], entry["metode"], uid)
            else:
                self.assertEqual(current["metode"], base["metode"], uid)

        # Spot-check the semantic corrections and selective overlaps.
        self.assertIn("kata “hari” tidak ada", integrated["M07"]["khususiyah"]["waktu"])
        self.assertIn("sebelum fajar", integrated["M12"]["metode"][0])
        self.assertIn("delapan puluh hari", integrated["M12"]["metode"][0])
        self.assertIn("kabarbarah", integrated["M75"]["khususiyah"]["bukhur"])
        self.assertIn("pelepah hijau", integrated["M79"]["metode"][0])
        self.assertIn("cendana", integrated["M79"]["khususiyah"]["bukhur"])
        self.assertNotIn("kertas hijau", " ".join(integrated["M79"]["metode"]))
        self.assertIn("dikuburkan di pintu", integrated["M82"]["metode"][0])
        self.assertIn("diasapi", integrated["M83"]["metode"][0])
        self.assertIn("saat baik", integrated["M84"]["khususiyah"]["waktu"])
        self.assertIn("tujuh puluh dua kali", integrated["M84"]["khususiyah"]["media"])
        self.assertIn("mulai hari Ahad", integrated["M98"]["khususiyah"]["waktu"])
        self.assertEqual(integrated["M98"]["crop_page"], 98)
        self.assertEqual(
            integrated["M104"]["catatan_penyunting"][-1],
            selective["M104"]["catatan_tambah"][0],
        )
        self.assertEqual(
            integrated["M107"]["catatan_penyunting"][-1],
            selective["M107"]["catatan_tambah"][0],
        )
        self.assertEqual(integrated["M105"]["jam"], [NO_CALC])
        self.assertIn(
            "1072, 535, 1403, 1598, 517, 646, 1813, 1314, 908, dan 1598",
            integrated["M105"]["khususiyah"]["media"],
        )
        self.assertTrue(
            any(
                "tidak dianjurkan" in n
                for n in integrated["M121"]["catatan_penyunting"]
            )
        )

    def test_final_batch_m68_m70_m71_overrides_are_narrow_when_work_data_present(self):
        override_path = ALQ / "overrides_batch_m68_m70_m71.json"
        payload = json.loads(override_path.read_text(encoding="utf-8"))
        final_batch = payload["units"]
        expected_units = {"M68", "M70", "M71"}
        self.assertEqual(set(final_batch), expected_units)
        for uid, entry in final_batch.items():
            self.assertLessEqual(
                set(entry),
                {"dasar", "notes_groups", "khususiyah", "metode_first"},
                uid,
            )
            self.assertNotIn("metode", entry, uid)
            self.assertTrue(str(entry.get("dasar", "")).strip(), uid)
            self.assertTrue(
                any(
                    k in entry
                    for k in ("notes_groups", "khususiyah", "metode_first")
                ),
                uid,
            )
            if "metode_first" in entry:
                self.assertEqual(uid, "M71")
                self.assertIn("dipanaskan", entry["metode_first"])
                self.assertIn(
                    "zat persisnya tidak dipastikan", entry["metode_first"]
                )
                self.assertNotIn("dibakar dengan lemak", entry["metode_first"])
            if "khususiyah" in entry:
                self.assertLessEqual(
                    set(entry["khususiyah"]),
                    {"waktu", "media", "bukhur"},
                    uid,
                )

        revised_path = ALQ / "work/revised_units.json"
        pilot_path = ALQ / "work/pilot_units.json"
        integrated_path = ALQ / "work/integrated_units.json"
        selective_path = ALQ / "overrides_upload_selektif_2026-10-28.json"
        batch1_path = ALQ / "overrides_batch_m16_m64.json"
        batch2_path = ALQ / "overrides_batch_m06_m15_m72_m121.json"
        if not (
            revised_path.exists()
            and pilot_path.exists()
            and integrated_path.exists()
            and selective_path.exists()
            and batch1_path.exists()
            and batch2_path.exists()
        ):
            self.skipTest("ignored work JSON not present in this checkout")

        def cloned(units):
            return {
                u["unit_id"]: json.loads(json.dumps(u, ensure_ascii=False))
                for u in units
            }

        def apply_notes(unit, groups):
            old = unit["catatan_penyunting"]
            unit["catatan_penyunting"] = [
                " ".join(old[i - 1] for i in g) for g in groups
            ]

        def apply_batch(units_by_id, path):
            entries = json.loads(path.read_text(encoding="utf-8"))["units"]
            for uid, entry in entries.items():
                unit = units_by_id[uid]
                if entry.get("notes_groups") is not None:
                    apply_notes(unit, entry["notes_groups"])
                unit["khususiyah"].update(entry.get("khususiyah", {}))
                if "metode" in entry:
                    unit["metode"] = list(entry["metode"])

        # Reconstruct the builder's exact pre-final baseline: mechanical
        # units + pilot + selective + batch M16-M64 + batch M06-M15/M72-M121.
        baseline = cloned(json.loads(revised_path.read_text(encoding="utf-8")))
        for uid, unit in cloned(
            json.loads(pilot_path.read_text(encoding="utf-8"))
        ).items():
            baseline[uid] = unit
        selective = json.loads(selective_path.read_text(encoding="utf-8"))["units"]
        for uid, entry in selective.items():
            unit = baseline[uid]
            unit["khususiyah"].update(entry.get("khususiyah", {}))
            unit["catatan_penyunting"] += list(entry.get("catatan_tambah", []))
            if "metode" in entry:
                unit["metode"] = list(entry["metode"])
        apply_batch(baseline, batch1_path)
        apply_batch(baseline, batch2_path)
        apply_user_arab_replacement_h62(baseline)
        apply_user_arab_replacement_h63_122(baseline)

        integrated = {
            u["unit_id"]: u
            for u in json.loads(integrated_path.read_text(encoding="utf-8"))
        }
        order = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)]
        self.assertEqual(set(integrated), set(order))
        translation_path = ALQ / "overrides_terjemahan_total_batch01.json"
        translation = {}
        if translation_path.exists():
            translation = json.loads(
                translation_path.read_text(encoding="utf-8")
            )["units"]
        for uid in order:
            if uid not in expected_units:
                if uid in translation:
                    for key, value in baseline[uid].items():
                        if key != "terjemahan":
                            self.assertEqual(
                                integrated[uid][key], value, (uid, key)
                            )
                    self.assertEqual(
                        integrated[uid]["terjemahan"],
                        translation[uid]["terjemahan"],
                        uid,
                    )
                else:
                    self.assertEqual(integrated[uid], baseline[uid], uid)

        change_keys = {"metode", "catatan_penyunting", "khususiyah"}
        for uid in sorted(expected_units):
            base = baseline[uid]
            current = integrated[uid]
            entry = final_batch[uid]
            for key, value in base.items():
                if key not in change_keys:
                    self.assertEqual(current[key], value, (uid, key))
            self.assertEqual(current["jam"], base["jam"], uid)

            groups = entry.get("notes_groups")
            if groups is None:
                expected_notes = base["catatan_penyunting"]
            else:
                flat = [i for g in groups for i in g]
                self.assertEqual(flat, sorted(set(flat)), uid)
                self.assertGreaterEqual(flat[0], 1, uid)
                self.assertLessEqual(
                    flat[-1], len(base["catatan_penyunting"]), uid
                )
                expected_notes = [
                    " ".join(base["catatan_penyunting"][i - 1] for i in g)
                    for g in groups
                ]
            self.assertEqual(current["catatan_penyunting"], expected_notes, uid)
            for paragraph in current["catatan_penyunting"]:
                for old in base["catatan_penyunting"]:
                    if old in paragraph:
                        break
                else:
                    self.fail(f"{uid}: note paragraph not composed of old notes")

            expected_khususiyah = dict(base["khususiyah"])
            expected_khususiyah.update(entry.get("khususiyah", {}))
            self.assertEqual(current["khususiyah"], expected_khususiyah, uid)
            if "metode_first" in entry:
                self.assertEqual(current["metode"][0], entry["metode_first"], uid)
                self.assertEqual(current["metode"][1:], base["metode"][1:], uid)
            else:
                self.assertEqual(current["metode"], base["metode"], uid)

        for uid, crop in (("M68", 68), ("M70", 70), ("M71", 71)):
            self.assertEqual(integrated[uid]["crop_page"], crop)
            self.assertEqual(integrated[uid]["jam"], [NO_CALC])
        self.assertIn("QS al-Kahf 18:25", integrated["M68"]["khususiyah"]["media"])
        self.assertIn("crop asli 68.jpg", integrated["M68"]["khususiyah"]["media"])
        self.assertIn("☆ ف ق ج", integrated["M70"]["khususiyah"]["media"])
        self.assertIn("Yā-Sīn 36:78", integrated["M70"]["khususiyah"]["media"])
        self.assertIn("kabīrah", integrated["M70"]["khususiyah"]["bukhur"])
        self.assertIn("dipanaskan", integrated["M71"]["metode"][0])
        self.assertIn(
            "zat persisnya tidak dipastikan", integrated["M71"]["metode"][0]
        )
        self.assertNotIn(
            "dibakar dengan lemak", " ".join(integrated["M71"]["metode"])
        )
        self.assertTrue(
            integrated["M71"]["metode"][1].startswith(
                "Halaman ini TIDAK memuat wafaq berpetak"
            )
        )
        self.assertIn("delapan posisi ṭā’", integrated["M71"]["khususiyah"]["media"])

    def test_translation_total_batch01_is_terjemahan_only(self):
        override_path = ALQ / "overrides_terjemahan_total_batch01.json"
        payload = json.loads(override_path.read_text(encoding="utf-8"))
        batch = payload["units"]
        self.assertEqual(set(batch), TRANSLATION_B01)
        for uid, entry in batch.items():
            self.assertEqual(set(entry), {"dasar", "terjemahan"}, uid)
            self.assertGreaterEqual(len(entry["dasar"]), 60, uid)

        pilot_path = ALQ / "work/pilot_units.json"
        integrated_path = ALQ / "work/integrated_units.json"
        if not (pilot_path.exists() and integrated_path.exists()):
            self.skipTest("ignored work JSON not present in this checkout")
        pilot = {
            u["unit_id"]: u
            for u in json.loads(pilot_path.read_text(encoding="utf-8"))
        }
        integrated = {
            u["unit_id"]: u
            for u in json.loads(integrated_path.read_text(encoding="utf-8"))
        }
        apply_user_arab_replacement_h62(pilot)
        apply_user_arab_replacement_h63_122(pilot)
        # The six Batch-01 units are historical pilot units and no selective or
        # semantic Lapis-4/5 batch targets them.  After applying the later
        # declared user Arabic replacement stages, their pre-Batch-01 records are
        # exactly the pilot records, so this comparison proves the translation
        # stage changed Lapis 3 and nothing else.
        for uid in TRANSLATION_B01:
            base = pilot[uid]
            current = integrated[uid]
            self.assertEqual(
                current["terjemahan"], batch[uid]["terjemahan"], uid
            )
            self.assertEqual(
                len(current["terjemahan"]), len(base["terjemahan"]), uid
            )
            self.assertEqual(len(current["arab"]), len(current["latin"]), uid)
            self.assertEqual(
                len(current["terjemahan"]), len(current["arab"]), uid
            )
            for key, value in base.items():
                if key != "terjemahan":
                    self.assertEqual(current[key], value, (uid, key))
            label = "[CATATAN PENERJEMAH"
            self.assertEqual(
                " ".join(current["terjemahan"]).count(label),
                " ".join(base["terjemahan"]).count(label),
                uid,
            )
        self.assertEqual(integrated["SAMPUL"]["crop_page"], None)
        self.assertTrue(
            integrated["M01"]["terjemahan"][3].startswith("yang menerangi relung")
        )
        self.assertIn("al-jadīdān", integrated["M03"]["terjemahan"][5])
        self.assertIn("di dunia dan di akhirat", integrated["M04"]["terjemahan"][7])
        self.assertIn("intisyāt", integrated["M05"]["terjemahan"][3])


class IntegratedDocxTests(unittest.TestCase):
    """The 123-unit DOCX is an integrated build, not proof of semantic completion."""

    @classmethod
    def setUpClass(cls):
        cls.path = ALQ / "AL_QORIN_REVISI_123_5_LAPIS.docx"
        if not cls.path.exists():
            raise unittest.SkipTest("integrated DOCX has not been built")
        cls.doc = Document(str(cls.path))
        with zipfile.ZipFile(str(cls.path)) as z:
            cls.names = z.namelist()

    def test_integrated_docx_counts_and_user_media(self):
        self.assertEqual(sum(p.style.name == "Heading 1" for p in self.doc.paragraphs), 123)
        self.assertEqual(sum(p.style.name == "Heading 2" for p in self.doc.paragraphs), 611)
        self.assertEqual(sum(p.style.name == "Heading 3" for p in self.doc.paragraphs), 366)
        self.assertEqual(len(self.doc.tables), 4)
        self.assertEqual(len([n for n in self.names if n.startswith("word/media/")]), 26)
        self.assertEqual(len([n for n in self.names if n.startswith("word/fonts/")]), 4)
        with zipfile.ZipFile(str(self.path)) as z:
            media_hashes = [hashlib.sha256(z.read(f"word/media/image{i}.jpg")).hexdigest()
                            for i in range(1, 27)]
        crop_hashes = [hashlib.sha256((ALQ / f"wafaq_qorin/{p}.jpg").read_bytes()).hexdigest()
                       for p in EXPECTED_CROPS]
        self.assertEqual(media_hashes, crop_hashes)
        texts = [p.text for p in self.doc.paragraphs]
        # SAMPUL renders no layer 4 under the conditional rule, hence 122.
        self.assertEqual(sum(t.count(NO_CALC) for t in texts), 122)
        self.assertEqual(sum(t.count("[CATATAN PENERJEMAH") for t in texts), 25)
        self.assertFalse(any(t.strip().startswith("Qarinah ") for t in texts))

    def test_integrated_direction_and_crop_placement(self):
        def pval(p, tag):
            if p._p.pPr is None:
                return None
            el = p._p.pPr.find(qn(tag))
            return el.get(qn("w:val")) if el is not None else None

        layer = sub = None
        arab = latin = images = arab_brackets = 0
        for p in self.doc.paragraphs:
            if p.style.name == "Heading 1":
                layer = sub = None
                continue
            if p.style.name == "Heading 2":
                layer, sub = p.text.strip(), None
                continue
            if p.style.name == "Heading 3":
                sub = p.text.strip()
                continue
            if p._p.xpath('.//*[local-name()="blip"]'):
                images += 1
                self.assertEqual(sub, "1. Metode", "crop must follow Metode and precede Penentuan Jam")
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("0", "center"))
                continue
            if not p.text.strip():
                continue
            if layer == "1. Arab":
                arab += 1
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("1", "start"), p.text[:80])
                for run in p.runs:
                    bracket_count = sum(run.text.count(ch) for ch in "()[]{}«»")
                    if bracket_count:
                        arab_brackets += bracket_count
                        self.assertIsNotNone(run._r.rPr, run.text)
                        self.assertIsNotNone(
                            run._r.rPr.find(qn("w:rtl")),
                            f"Arabic bracket run is not RTL: {run.text!r}",
                        )
            elif layer == "2. Latin":
                latin += 1
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("0", "left"), p.text[:80])
        self.assertEqual(images, 26)
        self.assertGreater(arab, 500)
        self.assertGreater(latin, 300)
        self.assertEqual(arab_brackets, 468)


class CleanUserEditionTests(unittest.TestCase):
    """The clean edition uses the user's archived Arabic sources and Latin TXT."""

    @classmethod
    def setUpClass(cls):
        cls.md_path = ALQ / "AL_QORIN_123_BERSIH.md"
        cls.docx_path = ALQ / "AL_QORIN_123_BERSIH.docx"
        if not (cls.md_path.exists() and cls.docx_path.exists()):
            raise unittest.SkipTest("clean user edition has not been built")
        cls.md = cls.md_path.read_text(encoding="utf-8")
        cls.blocks = unit_blocks(cls.md)
        cls.doc = Document(str(cls.docx_path))
        with zipfile.ZipFile(str(cls.docx_path)) as z:
            cls.names = z.namelist()

    def test_archived_user_txt_hashes_and_unit_headings(self):
        archive = ALQ / "incoming_user_2026-10-28/arab_latin_full"
        expected = {
            "teks arab berharokat.txt":
                "d28d8f3b1c3887634ea3c3843fb04cea13dc42c7873909a0633d8ef0b9705097",
            "teks latin.txt":
                "538a5959af8880b6094333dbdc68090bada94075a6a6b9e10d55d1b1189f5647",
        }
        for filename, sha in expected.items():
            data = (archive / filename).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), sha, filename)
            headings = re.findall(
                r"^(SAMPUL|M\d{2,3})(?:\s+—\s+.*)?$",
                data.decode("utf-8-sig"),
                flags=re.M,
            )
            self.assertEqual(headings, ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)], filename)

    def test_user_arab_replacement_h62_is_locked_in_both_masters(self):
        archive = (
            ALQ / "incoming_user_2026-10-28/arab_replacement_h62/"
            "teks arab pengganti sampai halaman 62.txt"
        )
        data = archive.read_bytes()
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "2625d048c67ec6f5fd6328bbb2d8a35d63e16909c3c727f1c9b8abbed35448e4",
        )

        replacement = {}
        current = None
        for raw_line in data.decode("utf-8-sig").splitlines():
            line = raw_line.strip()
            if line == "SAMPUL":
                current = "SAMPUL"
                replacement[current] = []
                continue
            match = re.match(r"^(\d{1,2})\s+—\s+", line)
            if match and 1 <= int(match.group(1)) <= 62:
                current = f"M{int(match.group(1)):02d}"
                replacement[current] = []
                continue
            if current is not None and line:
                replacement[current].append(re.sub(r"^\*\s+", "", line))

        expected_order = ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 63)]
        self.assertEqual(list(replacement), expected_order)
        self.assertEqual(sum(len(x) for x in replacement.values()), 277)

        def arab_paragraphs(block):
            match = re.search(
                r"^### 1\. Arab\n(.*?)(?=^###\s+|\Z)", block, re.M | re.S
            )
            self.assertIsNotNone(match)
            return [
                p.strip()
                for p in match.group(1).strip().split("\n\n")
                if p.strip()
            ]

        for path in (self.md_path, ALQ / "REVISI_AL_QORIN_123.md"):
            blocks = {
                uid: block
                for uid, _heading, block in unit_blocks(
                    path.read_text(encoding="utf-8")
                )
            }
            self.assertEqual(
                sum(len(arab_paragraphs(block)) for block in blocks.values()),
                544,
                path.name,
            )
            for uid in expected_order:
                self.assertEqual(
                    arab_paragraphs(blocks[uid]),
                    replacement[uid],
                    f"{path.name}:{uid}",
                )

    def test_user_arab_replacement_h63_122_is_locked_in_both_masters(self):
        data = H63_122_ARCHIVE.read_bytes()
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "b82ea529a6df1bbd9ad8cecbd23573c3722f01fd1b7ef84d1fa44471d81ec189",
        )
        exact = user_arab_replacement_h63_122()
        clean = clean_user_arab_replacement_h63_122()
        self.assertEqual(list(exact), H63_122_UNITS)
        self.assertEqual(sum(len(x) for x in exact.values()), 267)

        def arab_paragraphs(block):
            match = re.search(
                r"^### 1\. Arab\n(.*?)(?=^###\s+|\Z)", block, re.M | re.S
            )
            self.assertIsNotNone(match)
            return [
                p.strip()
                for p in match.group(1).strip().split("\n\n")
                if p.strip()
            ]

        for path, expected in (
            (ALQ / "REVISI_AL_QORIN_123.md", exact),
            (self.md_path, clean),
        ):
            blocks = {
                uid: block
                for uid, _heading, block in unit_blocks(
                    path.read_text(encoding="utf-8")
                )
            }
            self.assertEqual(
                sum(len(arab_paragraphs(block)) for block in blocks.values()),
                544,
                path.name,
            )
            for uid in H63_122_UNITS:
                self.assertEqual(
                    arab_paragraphs(blocks[uid]),
                    expected[uid],
                    f"{path.name}:{uid}",
                )

        # The clean presentation removes only the five Indonesian process
        # markers in M96/M97/M107; it must not silently rewrite anything else.
        changed = {
            uid
            for uid in H63_122_UNITS
            if clean[uid] != exact[uid]
        }
        self.assertEqual(changed, {"M96", "M97", "M107"})
        clean_text = self.md_path.read_text(encoding="utf-8")
        for marker in ("[bersambung]", "[tidak disalin penuh]", "[baris tidak lengkap]"):
            self.assertNotIn(marker, clean_text)

    def test_clean_md_structure_crops_and_no_process_meta(self):
        self.assertEqual(
            [uid for uid, _h, _b in self.blocks],
            ["SAMPUL"] + [f"M{i:02d}" for i in range(1, 123)],
        )
        always = ["1. Arab", "2. Latin", "3. Terjemahan", "4. Syarah"]
        fifth = "5. Khususiyah dan Tatacara Praktik"
        included = []
        for uid, _heading, block in self.blocks:
            layers = re.findall(r"^### ([^\n]+)$", block, re.M)
            self.assertEqual(layers[:4], always, uid)
            self.assertIn(len(layers), (4, 5), uid)
            if len(layers) == 5:
                self.assertEqual(layers[4], fifth, uid)
                included.append(uid)
        self.assertEqual(len(included), 76)
        for uid in ("M04", "M38", "M58", "M71", "M122"):
            self.assertIn(uid, included)
        for uid in ("SAMPUL", "M01", "M16", "M87", "M96"):
            self.assertNotIn(uid, included)
        self.assertEqual(
            [int(x) for x in re.findall(r"wafaq_qorin/(\d+)\.jpg", self.md)],
            EXPECTED_CROPS,
        )
        for phrase in (
            "Build terintegrasi", "STANDAR_MUTLAK", "sumber kerja",
            "segmen berikutnya", "Catatan penyunting", "Penentuan Jam",
            "tidak ada hitungan", "pindaian", "Catatan editorial",
        ):
            self.assertNotIn(phrase, self.md)
        self.assertEqual(self.md.count("[CATATAN PENERJEMAH"), 25)

    def test_clean_docx_counts_direction_media_and_front_matter(self):
        self.assertEqual(sum(p.style.name == "Heading 1" for p in self.doc.paragraphs), 123)
        self.assertEqual(sum(p.style.name == "Heading 2" for p in self.doc.paragraphs), 568)
        self.assertEqual(sum(p.style.name == "Heading 3" for p in self.doc.paragraphs), 0)
        self.assertEqual(len(self.doc.tables), 0)
        self.assertEqual(self.doc.paragraphs[0].text, "AL-QORIN WAR RIYADHAH")
        self.assertEqual(self.doc.paragraphs[1].text, "SAMPUL")
        header = self.doc.sections[0].header.paragraphs[0].text
        footer = self.doc.sections[0].footer.paragraphs[0].text
        self.assertEqual(header, "")
        self.assertNotIn("anjuran", footer)
        self.assertEqual(len([n for n in self.names if n.startswith("word/media/")]), 26)
        self.assertEqual(len([n for n in self.names if n.startswith("word/fonts/")]), 4)
        with zipfile.ZipFile(str(self.docx_path)) as z:
            media_hashes = [
                hashlib.sha256(z.read(f"word/media/image{i}.jpg")).hexdigest()
                for i in range(1, 27)
            ]
        crop_hashes = [
            hashlib.sha256((ALQ / f"wafaq_qorin/{p}.jpg").read_bytes()).hexdigest()
            for p in EXPECTED_CROPS
        ]
        self.assertEqual(media_hashes, crop_hashes)

        def pval(p, tag):
            if p._p.pPr is None:
                return None
            el = p._p.pPr.find(qn(tag))
            return el.get(qn("w:val")) if el is not None else None

        layer = None
        arab = latin = images = arab_brackets = 0
        for p in self.doc.paragraphs:
            if p.style.name == "Heading 1":
                layer = None
                continue
            if p.style.name == "Heading 2":
                layer = p.text.strip()
                continue
            if p._p.xpath('.//*[local-name()="blip"]'):
                images += 1
                self.assertEqual(layer, "4. Syarah")
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("0", "center"))
                continue
            if not p.text.strip():
                continue
            if layer == "1. Arab":
                arab += 1
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("1", "start"), p.text[:80])
                for run in p.runs:
                    bracket_count = sum(run.text.count(ch) for ch in "()[]{}«»")
                    if bracket_count:
                        arab_brackets += bracket_count
                        self.assertIsNotNone(run._r.rPr, run.text)
                        self.assertIsNotNone(
                            run._r.rPr.find(qn("w:rtl")),
                            f"Arabic bracket run is not RTL: {run.text!r}",
                        )
            elif layer == "2. Latin":
                latin += 1
                self.assertEqual((pval(p, "w:bidi"), pval(p, "w:jc")), ("0", "left"), p.text[:80])
        self.assertEqual((arab, latin, images), (544, 315, 26))
        self.assertEqual(arab_brackets, 458)


class PreviewTests(unittest.TestCase):
    def test_preview_counts_and_alias(self):
        canonical = ALQ / "PREVIEW_INDEX_AL_QORIN_123.html"
        alias = ALQ / "PREVIEW_INDEX_HAL01-65.html"
        s = canonical.read_text(encoding="utf-8")
        self.assertEqual(s, alias.read_text(encoding="utf-8"))
        self.assertEqual(len(re.findall(r"<article id=", s)), 123)
        self.assertEqual(len(re.findall(r"<section dir=", s)), 611)
        self.assertEqual(len(re.findall(r'<figure class="wafaq"', s)), 26)
        self.assertEqual([int(x) for x in re.findall(r"wafaq_qorin/(\d+)\.jpg", s)], EXPECTED_CROPS)
        self.assertIn('dir="rtl" class="layer arab"', s)
        self.assertIn('dir="ltr" class="layer"', s)


class PilotDocxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = Document(str(PILOT_DOCX))
        with zipfile.ZipFile(str(PILOT_DOCX)) as z:
            cls.parts = {name: z.read(name) for name in z.namelist()}

    @staticmethod
    def pval(p, tag):
        if p._p.pPr is None:
            return None
        el = p._p.pPr.find(qn(tag))
        return el.get(qn("w:val")) if el is not None else None

    def test_heading_table_and_text_counts(self):
        self.assertEqual(sum(p.style.name == "Heading 1" for p in self.doc.paragraphs), 12)
        # Pilot layer headings: SAMPUL 3 + M01 4 + M122 4 + 9 units x 5 = 56;
        # subsections: 11 units with layer 4 x 3 = 33 (conditional rule).
        self.assertEqual(sum(p.style.name == "Heading 2" for p in self.doc.paragraphs), 56)
        self.assertEqual(sum(p.style.name == "Heading 3" for p in self.doc.paragraphs), 33)
        self.assertEqual([(len(t.rows), len(t.columns)) for t in self.doc.tables],
                         [(1, 2), (4, 3), (2, 10), (5, 4)])
        all_text = [p.text for p in self.doc.paragraphs]
        all_text += [c.text for t in self.doc.tables for r in t.rows for c in r.cells]
        self.assertEqual(sum(t.count(NO_CALC) for t in all_text), 11)
        self.assertFalse(any(t.strip().startswith("Qarinah ") for t in all_text))
        self.assertFalse(any("*" in t or "`" in t for t in all_text))

    def test_arabic_and_latin_direction_flags(self):
        ctx = None
        arab = latin = 0
        for p in self.doc.paragraphs:
            if p.style.name == "Heading 1":
                ctx = None
                continue
            if p.style.name == "Heading 2":
                ctx = p.text.strip()
                continue
            if not p.text.strip():
                continue
            if ctx == "1. Arab":
                arab += 1
                self.assertEqual((self.pval(p, "w:bidi"), self.pval(p, "w:jc")), ("1", "start"), p.text[:80])
            elif ctx == "2. Latin":
                latin += 1
                self.assertEqual((self.pval(p, "w:bidi"), self.pval(p, "w:jc")), ("0", "left"), p.text[:80])
        self.assertGreater(arab, 50)
        self.assertGreater(latin, 40)

    def test_wafaq_images_centered_and_byte_identical(self):
        image_paras = [p for p in self.doc.paragraphs if p._p.xpath('.//*[local-name()="blip"]')]
        self.assertEqual(len(image_paras), 5)
        for p in image_paras:
            self.assertEqual(self.pval(p, "w:jc"), "center")
        media = [self.parts[f"word/media/image{i}.jpg"] for i in range(1, 6)]
        crops = [(ALQ / f"wafaq_qorin/{p}.jpg").read_bytes() for p in (58, 65, 66, 67, 69)]
        self.assertEqual([hashlib.sha256(x).hexdigest() for x in media],
                         [hashlib.sha256(x).hexdigest() for x in crops])

    def test_tables_centered_without_bidi_visual(self):
        for table in self.doc.tables:
            tbl_jc = table._tbl.tblPr.find(qn("w:jc"))
            self.assertIsNotNone(tbl_jc)
            self.assertEqual(tbl_jc.get(qn("w:val")), "center")
            self.assertEqual(len(table._tbl.tblPr.findall(qn("w:bidiVisual"))), 0)
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        self.assertEqual(self.pval(p, "w:jc"), "center")

    def test_amiri_fonts_declared_and_embedded_recoverably(self):
        for style in ("Normal", "Title", "Heading 1", "Heading 2", "Heading 3"):
            self.assertEqual(self.doc.styles[style].font.name, "Amiri", style)
        settings = ET.fromstring(self.parts["word/settings.xml"])
        self.assertIsNotNone(settings.find(f"{W}embedTrueTypeFonts"))
        self.assertIsNone(settings.find(f"{W}saveSubsetFonts"))
        ctypes = ET.fromstring(self.parts["[Content_Types].xml"])
        self.assertTrue(any(el.get("Extension") == "odttf" for el in ctypes.findall(f"{CT}Default")))
        font_table = ET.fromstring(self.parts["word/fontTable.xml"])
        Amiri = None
        for el in font_table.findall(f"{W}font"):
            if el.get(f"{W}name") == "Amiri":
                Amiri = el
                break
        self.assertIsNotNone(Amiri)
        rels = ET.fromstring(self.parts["word/_rels/fontTable.xml.rels"])
        relmap = {el.get("Id"): el.get("Target") for el in rels.findall(f"{REL}Relationship")}
        expected = {
            "embedRegular": "Amiri-Regular.ttf",
            "embedBold": "Amiri-Bold.ttf",
            "embedItalic": "Amiri-Italic.ttf",
            "embedBoldItalic": "Amiri-BoldItalic.ttf",
        }
        for tag, ttf in expected.items():
            emb = Amiri.find(f"{W}{tag}")
            self.assertIsNotNone(emb, tag)
            part = "word/" + relmap[emb.get(f"{R}id")]
            restored = deobfuscate(self.parts[part], emb.get(f"{W}fontKey"))
            self.assertEqual(restored, (ROOT / "fonts" / ttf).read_bytes(), tag)


if __name__ == "__main__":
    unittest.main()
