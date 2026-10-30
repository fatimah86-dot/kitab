#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 68-69 revision to the final DOCX.

Excludes carried-over material: introductory confirmation/format
paragraph, numbered section labels, [Halaman ...] markers, the
translation-side description "(Rangkaian tlasim dan asror)", and
"(Ekstraksi Ritual)".  Markdown asterisks are normalized to the
document's bullets or removed from textual lists.  Keeps all
"[ada wafaq]" markers and each precision wafaq image at the marker
position in its Arabic block.  Places the combined Tata Cara
Praktik at the end of Halaman 69.
"""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "al_qorin/AL_QORIN_123_FINAL_KELUHAN_SELESAI.docx"
SOURCE_FOR_MEDIA = ROOT / "al_qorin/AL_QORIN_123_BERSIH_2_LAYER.docx"

AR68 = [
    "تَكْتُبُ",
    "[ada wafaq]",
    "أَهْمَصَمْ ... عَهْنِي رَصَرْطَ فَقَهْشِي رَا وَ لْ فَ قْ حَ مْ خْ نْ تْ",
    "انْزِلْ يَا فَارِسُ وَأَنْتَ يَا خَادِمَ هَذَا الْيَوْمِ وَاصْرِفُوا وَاطْرُدُوا الْأَرْوَاحَ السُّوءَ وَالْعَوَارِضَ وَالْقَرَائِينَ وَالتَّوَابِعَ وَالْمَرَضَ وَكُلَّ شَغَبٍ وَسِحْرٍ وَعَكْسٍ وَعَيْنٍ وَنَفْسٍ وَرِيحٍ أَحْمَرَ وَدَاءِ أَكْبَرَ وَنَظْرَةِ سُوءٍ عَنْ هَذِهِ الْجُثَّةِ الْبَشَرِيَّةِ جُثَّةِ فُلَانِ بْنِ فُلَانَةَ أَوْ فُلَانَةَ بِنْتِ فُلَانَةَ بِحَقِّ سَيْهِكٍ لَهْكٍ وَصَكٍ دَهْكٍ رَهْكٍ أَنُوخٍ يَنُوخٍ بَنُوخٍ وَبِحَقِّ الْاسْمِ الْأَعْظَمِ أَهْيَا شَرَاهِيَا أَدُونَايَّ أَصْبَاوْتِ آلِ شَرَايَّ وَبِحَقِّ بَطْرِ زَهْجٍ وَاجٍ الْعَجْلَ ٢ السَّاعَةَ الْوَاحَا ٣ .",
    "فَائِدَةٌ لِلْحَمْلِ :",
    "تَكْتُبُ هَذِهِ الْآيَاتِ وَتُعَلِّقُهَا الْمَرْأَةُ عَلَيْهَا وَيُجَامِعُهَا زَوْجُهَا فَإِنَّهَا تَحْمَلُ بِإِذْنِ اللَّهِ تَعَالَى وَهَذِهِ الْآيَاتُ :",
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ -",
    "وَلَبِثُوا فِي كَهْفِهِمْ ثَلَاثَ مِائَةٍ سِنِينَ وَازْدَادُوا تِسْعاً . الم",
]
LAT68 = [
    "Taktubu...",
    "( [ada wafaq] )",
    "Ahmamasy... 'ahnī rasarṭa faqahsyī rā wal fā qāf ḥā' mīm khā' nūn tān.",
    "Unzul yā fārisu wa anta yā khādima hāżal-yaumi wa iṣrufū wa uṭrudul-arwāḥas-sū'a wal-‘awāriḍa wal-qarā'īna wat-tawābi‘a wal-maraḍa wa kulla syaghbin wa siḥrin wa ‘aksin wa ‘ainin wa nafsin wa rīḥin aḥmara wa dā'in akbara wa nazhrati sū'in ‘an hāżihil-jutsatil-basyariyyati jutsati fulāni bnu fulānata au fulānata bintu fulānata biḥaqqi sayahikin lahikin washakin dahikin rahakin anukhin yanukhin banukhin wa biḥaqqil-ismil-‘aẓīmi āhyān syarāhiyān adūnāyya aṣbā'ūti āli syarāyya wa biḥaqqi baṭrin zahajin wājin al-‘ajala (marratain) as-سā‘atal-wāḥā (tsalātsa marrāt).",
    "Fā'idatun lil-ḥaml:",
    "Taktub hāżihil-āyāte wa tu‘alliquhal-mar'atu ‘alaihā wa yujāmi‘uhā zaujuhā fa-innahā taḥmalu bi-iżnillāhi ta‘ālā wa hāżihil-āyātu:",
    "Bismillāhir-raḥmānir-raḥīm.",
    "Wa labiṯū fī kahfihim tsalātsa mi'atin sinīna wazdādū tis‘ā. Alif Lām Mīm.",
]
TERJ68 = [
    "Engkau menulis: [ada wafaq]",
    '"Turunlah wahai Farris (Pemberani) dan engkau wahai khodam hari ini, palingkanlah dan usirlah segala bentuk roh-roh jahat, gangguan (\'awarid), qarin, tawabi\', penyakit, segala kekacauan, sihir, pembalikan keadaan (\'aks), \'ain, gangguan jiwa (nafs), angin merah (rih ahmar), penyakit berat, dan pandangan buruk dari jasad manusia ini, yaitu jasad Fulan bin Fulanah atau Fulanah binti Fulanah. Demi hak Sayahikin, Lahikin, Washikin, Dahikin, Rahakin, Anukhin, Yanukhin, Banukhin, dan demi hak Asma\'ul-Azhim: Ahiya Syarahiya Adonay Asba\'t El-Syaray, dan demi hak Bathrin, Zahajin, Wajin, datanglah segera (2x), pada saat ini (3x)."',
    "Faedah untuk Kehamilan:",
    "Tulislah ayat-ayat ini, lalu dikalungkan oleh perempuan tersebut, kemudian suaminya mendatanginya (berhubungan), maka sesungguhnya ia akan hamil dengan izin Allah Ta'ala. Dan inilah ayat-ayatnya:",
    "Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang.",
    '"Dan mereka tinggal dalam gua mereka tiga ratus tahun dan ditambah sembilan tahun." (QS. Al-Kahfi: 25). Alif Lam Mim.',
]

AR69 = [
    "تَخْلُقُكُم مِّن مَّاءِ مَهِينٍ فَجَعَلْنَاهُ فِي قَرَارٍ مَّكِينٍ إِلَى قَدَرٍ مَّعْلُومٍ فَقَدَرْنَا فَنِعْمَ الْقَادِرُونَ .",
    "فَائِدَةٌ لِلْحَمْلِ مَرَّةً أُخْرَى :",
    "وَإِذَا أَرَدْتَ التَّجْرِبَةَ عَلِّقْهَا عَلَى دَجَاجَةٍ فَإِنَّهَا تَبِيضُ وَهِيَ تَحْمِلُ لِأَنَّهَا سِرٌّ عَجِيبٌ وَهَذَا مَا تَكْتُبُ وَيُحْمَلُ بَعْدَ الطُّهْرِ مِنَ الْحَيْضِ .",
    "[ada wafaq]",
    "[ada wafaq]",
    "[ada wafaq]",
    "[ada wafaq]",
    "أَنَّ اللَّهَ فَالِقُ الْحَبِّ وَالنَّوَى يُخْرِجُ الْحَيَّ مِنَ الْمَيِّتِ وَيُخْرِجُ الْمَيِّتَ مِنَ الْحَيِّ ...",
]
LAT69 = [
    "Khalaqakum mim-mā'in mahīnin faja‘alnāhu fī qarārin makīnin ilā qadarin ma‘lūmin faqadarnā fani‘mal-قādirūn.",
    "Fā'idatun lil-ḥaml marratan ukhro:",
    "Wa iżā aradta-t-tajribata ‘alliqhā ‘alā dajājatin fa-innahā tabiḍḍu wa hiya taḥmalu li-annahā sirrun ‘ajībun wa hāżā mā yuktubu wa yuḥmalu ba‘daṭ-ṭuhri minal-ḥaiḍi.",
    "( [ada wafaq] )",
    "( [ada wafaq] )",
    "( [ada wafaq] )",
    "( [ada wafaq] )",
    "Anna-llāha fāliqul-ḥabbi wan-nawā yukhrijul-ḥayya minal-mayyiti wa yukhrijul-mayyita minal-ḥayy...",
]
TERJ69 = [
    '"Kami menciptakan kamu dari air yang hina, kemudian Kami menjadikannya dalam tempat yang kokoh (rahim) sampai waktu yang ditentukan, lalu Kami tentukan (bentuknya), maka Dialah Sebaik-baik Yang Menentukan." (QS. Al-Mursalat: 20-23).',
    "Faedah untuk Kehamilan (Cara Lain):",
    "Dan apabila engkau ingin menguji kebenarannya, gantungkan tulisan ini pada seekor ayam, maka ia akan bertelur dan ia membawa rahasia yang ajaib. Dan inilah apa yang harus ditulis, lalu dibawa setelah suci dari haid:",
    "[ada wafaq]",
    "[ada wafaq]",
    "[ada wafaq]",
    "[ada wafaq]",
    '"Sesungguhnya Allah menumbuhkan butir tumbuh-tumbuhan dan biji-bijian. Dia mengeluarkan yang hidup dari yang mati dan mengeluarkan yang mati dari yang hidup..." (QS. Al-An\'am: 95).',
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Pembersihan & Ruqyah Tubuh (Hal. 68): Ditulis untuk membersihkan pasien dari gangguan gaib (sihir, 'ain, angin merah, qarin) menggunakan azimah pemanggilan khodam penolak bala dan penyebutan nama target secara spesifik.",
    "- Azimat Kesuburan / Cepat Hamil (Hal. 68 & 69):",
    "- Menuliskan ayat-ayat penjagaan dan penciptaan manusia (Al-Kahfi: 25, Al-Mursalat: 20-23, Al-An'am: 95) beserta wafaq rajah khusus.",
    "- Azimat wajib ditulis dan mulai dikalungkan setelah wanita tersebut suci dari haid.",
    "- Setelah dikalungkan, dilanjutkan dengan hubungan suami istri untuk mengaktifkan wasilah kehamilan atas izin Allah SWT.",
]

FORBIDDEN = [
    "standar dan kaidah tersebut telah dicatat",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "Rangkaian tlasim dan asror",
    "(Ekstraksi Ritual)",
]


def has_drawing_el(el) -> bool:
    return bool(el.xpath('.//*[local-name()="drawing"]'))


def make_para(template_el, text: str):
    el = deepcopy(template_el)
    runs = el.findall(qn("w:r"))
    donor = deepcopy(runs[0]) if runs else None
    for child in list(el):
        if child.tag != qn("w:pPr"):
            el.remove(child)
    if donor is not None:
        texts = [t for t in donor.iter() if t.tag == qn("w:t")]
        for t in texts:
            t.text = ""
        if texts:
            texts[0].text = text
            texts[0].set(qn("xml:space"), "preserve")
            for extra in texts[1:]:
                extra.getparent().remove(extra)
        el.append(donor)
    return el


def media_hashes(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.startswith("word/media/")]
        return [hashlib.sha256(z.read(n)).hexdigest() for n in names]


def find_heads(paragraph_texts: list[str]) -> dict[int, int]:
    heads: dict[int, int] = {}
    for i, text in enumerate(paragraph_texts):
        m = re.match(r"^=== Halaman (\d+) — (.+) ===$", text.strip())
        if m:
            heads[int(m.group(1))] = i
    return heads


def build_sequence(page: int) -> list[tuple[str, str | None]]:
    if page == 68:
        return (
            [("ar", x) for x in AR68[:2]]
            + [("img", None)]
            + [("ar", x) for x in AR68[2:]]
            + [("la", x) for x in LAT68]
            + [("te", x) for x in TERJ68]
        )
    return (
        [("ar", x) for x in AR69[:7]]
        + [("img", None)]
        + [("ar", x) for x in AR69[7:]]
        + [("la", x) for x in LAT69]
        + [("te", x) for x in TERJ69]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 68:
        return AR68[:2] + [""] + AR68[2:] + LAT68 + TERJ68 + [""]
    return AR69[:7] + [""] + AR69[7:] + LAT69 + TERJ69 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return 2 if page == 68 else 7


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[68] + 2])
    if has_drawing_el(arab_tpl) or not texts[heads[68] + 2].startswith("انْزِلْ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[68], heads[69])
        if texts[i].startswith("Taktubu. Inzil yaa faarisu")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[68], heads[69])
        if texts[i].startswith("Di awal halaman Lapis 1 memuat rajah halaman 68")
    )
    blank_tpl = deepcopy(els[heads[69] - 1])
    if texts[heads[69] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (68, 69):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[68]].getparent()
    removed = 0
    inserted = 0
    for n in (68, 69):
        heading_el = els[heads[n]]
        next_heading_el = els[heads[n + 1]]
        node = heading_el.getnext()
        while node is not None and node is not next_heading_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        for kind, text in build_sequence(n):
            if kind == "img":
                next_heading_el.addprevious(deepcopy(images[n]))
            else:
                next_heading_el.addprevious(make_para(templates[kind], str(text)))
            inserted += 1
        next_heading_el.addprevious(make_para(blank_tpl, ""))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = find_heads(ot)
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")

    for n in (68, 69):
        got_idx = list(range(oh[n] + 1, oh[n + 1]))
        got = [ot[i] for i in got_idx]
        expected = expected_texts(n)
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:140]!r}\n exp: {b[:140]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")
        image_positions = [
            j for j, i in enumerate(got_idx) if has_drawing_el(out.paragraphs[i]._element)
        ]
        if image_positions != [expected_image_position(n)]:
            raise AssertionError(
                f"unit {n} image positions {image_positions}, expected {[expected_image_position(n)]}"
            )

    revised = "\n".join(ot[oh[68] : oh[70]])
    if revised.count("[ada wafaq]") != 15:
        raise AssertionError(f"[ada wafaq] count {revised.count('[ada wafaq]')} != 15")
    for fragment in FORBIDDEN:
        if fragment.lower() in revised.lower():
            raise AssertionError(f"carried-over fragment remains: {fragment}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")

    print(f"removed_old_paras={removed}")
    print(f"inserted_paras={inserted}")
    print(f"total_paragraphs={len(ot)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H68_69_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
