#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 76-77 revision to the final DOCX.

Retains each existing precision wafaq image: Halaman 76 after the
paragraph carrying "[ada wafaq]", and Halaman 77 after its Arabic
block.  Excludes the introductory/layout text, numbered section
labels, [Halaman ...] markers, and "(Ekstraksi Ritual)".  Markdown
asterisks are normalized to document bullets or removed from textual
lists.  Places the combined Tata Cara Praktik at the end of
Halaman 77.
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

AR76 = [
    "ثم انظر بوجهك على اليمين وتقول :",
    "اعان الله من اعانى على خير من أرواح الجن المؤمنين عدد ٧",
    "ثم تلتفت بوجهك الى الجهة الشمال وتقول بصيفديش ٣ بقطلميد يش عدد ٧ فانك تسمع صوتا يقول لك السلام عليك ورحمة الله فرد عليه السلام وأساله فيما تريده.",
    "باب لرفع النزيف :",
    "وهو من المجربات يكتب ما يأتى على ثلاثة اوراق بيض بالمسك الاسود ويبخر كل ليلة بورقة وهكذا مدة ثلاثة ليالى متواليات فان الدم يرتفع باذن الله تعالى وهذا ما يكتب على الاوراق [ada wafaq]",
    "ارفعوا الدم النازل من فرج كذا الساعة بامرالله تعالى",
    "وما محمد الا رسول قد خلت من قبله الرسل افاين مات او قتل انقلبتم علي اعقابكم انقلبكم انقلب يادم",
    "وله ما سكن فى الليل والنهار",
]
LAT76 = [
    "Tsumma unẓur bi-wajhika ‘alal-yamīni wa taqūlu:",
    "A‘ānallāhu man a‘ānī ‘alā khairin min arwāḥil-jinni-l-mu'minīna ‘adada 7.",
    "Tsumma taltaftu bi-wajhika ilal-jihati-s-syamāli wa taqūlu biṣaifidīsyin (3x) bi-qaṭlamīdin yasyin ‘adada 7 fa-innaka tasma‘u ṣaudan yaqūlu laka as-salāmu ‘alaika wa raḥmatullāhi fa-ruddu ‘alaihi as-salāma wa as-s-alhu fīmā turīduh.",
    "Bābun li-raf‘in-nazīf:",
    "Wa huwa minal-mujarrabāti yaktubu mā yātī ‘alā َtsalāthati aurāqin baiḍa bil-miskil-aswadi wa yubakharu kulla lailatin bi-waraqatin wa hākadzā muddata َtsalāthati layālin mutawāliyatin fa-innal-dama yartafi‘u bi-iżnillāhi ta‘ālā wa hāżā mā yuktubu ‘alal-aurāq ( [ada wafaq] ):",
    "Irfa‘ū-d-dama-n-nāzila min farji każā as-sā‘ata bi-amrillāhi ta‘ālā.",
    "Wa mā muḥammadun illā rasūlun qad khalat min qablihi-r-rusulu af-ain māta au qutila anqalabtum ‘alā a‘qābikum anqalabukum anqalibu yā dam",
    "Wa lahū mā sakana fil-laili wan-nahār.",
]
TERJ76 = [
    'Lalu arahkan wajahmu ke sebelah kanan dan ucapkan: "Semoga Allah menolong orang yang menolongku kepada kebaikan dari golongan roh-roh jin mukmin sebanyak 7 kali."',
    "Kemudian palingkan wajahmu ke arah utara dan ucapkan: Bishaifidisy (3 kali), Bi-Qatlamid Yasy (7 kali), maka sesungguhnya engkau akan mendengar suara yang berkata kepadamu: 'Alaikas-salam warahmatullah, maka balaslah salamnya dan mintalah kepadanya apa yang engkau kehendaki.",
    "Bab untuk Menghentikan Pendarahan (Nazif):",
    "Termasuk ilmu yang teruji (mujarrab), dituliskan apa yang berikut ini pada tiga lembar kertas putih menggunakan minyak kasturi hitam (misK aswad). Setiap malam dibakar satu lembar kertas sebagai bukhur selama tiga malam berturut-turut, maka darah akan berhenti dengan izin Allah Ta'ala. Inilah yang dituliskan pada kertas:",
    "[ada wafaq]",
    '"Angkatlah dan hentikanlah darah yang turun dari kemaluan si Fulan pada saat ini dengan perintah Allah Ta\'ala."',
    '"Dan Muhammad tidak lain hanyalah seorang rasul..." (penggalan QS. Ali Imran: 144), "...Maka apakah jika dia wafat atau dibunuh kamu berbalik ke belakang (murtad)?... Berbaliklah dan membawahlah, berhenti dan keringlah wahai darah!"',
    '"Dan kepunyaan-Nya lah segala apa yang diamati di malam dan siang hari." (QS. Al-An\'am: 13).',
]

AR77 = [
    "وارتفع من فرج كذا بحق هذه الاسماء والآية العظيمة لكل نبأ مستقر.",
    "باب لرفع النزيف :",
    "يكتب ما يأتي في اناء نظيف بمسك اسود ويحمى ويسقى فان الدم يرفع باذن الله تعالى وهذا ما يكتب بسم الله الرحمن الرحيم الم ذلك الكتاب الحكيم هدى ورحمة للمحسنين الذين يقيمون الصلاة ويؤتون الزكاة وهم بالاخرة هم يوقنون يادم يوقنون يادم دمدم بحق حواء وادم وموسى انقطع يادم من فرج كذا وارتفع بحق هذه الاسماء ٩٩ طه ٩٣ لمن ٤ ص د انقطع يا دم ولا تعود بحق الرب المعبود وبالف لاحول ولا قوة الا بالله العلي العظيم.",
    "ابواب لزوال الصداع المزمن :",
    "يكتب ما يأتي ويحمل على الراس فان الصداع والضارب يسكن باذن الله تعالى وهذه ما يكتب البسمله والتصليه [ada wafaq].",
]
LAT77 = [
    "Wa irtafa‘a min farji każā biḥaqqi hāżihil-asmā'i wal-āyatil-‘aẓīmati likulli naba'im-mustaqirrun.",
    "Bābun li-raf‘in-nazīf:",
    "Yaktubu mā yātī fī inā'in naẓīfin bi-miskin aswadin wa yuḥmā wa yusqā fa-innal-dama yartafi‘u bi-iżnillāhi ta‘ālā wa hāżā mā yuktubu: Bismillāhir-rahmānir-raḥīm. Alif lām mīm. Żālika-l-kitābu lā raība fīhi hudan lil-muḥsinīn. Al-lażīna yuqīmūna-ṣ-ṣalāta wa yu'tūna-z-zakāta wa hum bil-ākhirati hum yūqinūn. Yā damu yūqinūn, yā damu damdam, biḥaqqi ḥawā'a wa ādam, wa mūsā inqaṭa‘a yā damu min farji każā wa irtafa‘a biḥaqqi hāżihil-asmā'i 99 Ṭā Hā 93 liman 4 Ṣād Dāl inqaṭa‘a yā damu wa lā ta‘ūdu biḥaqqi-r-rabbi-l-ma‘būdi wa bil-alfi lā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīم.",
    "Abwābun li-zawāli-ṣ-ṣudā‘il-muzmin:",
    "Yaktubu mā yātī wa yuḥmalu ‘alā-r-raasi fa-inna-ṣ-ṣudā‘a waḍ-ḍāriba yaskunu bi-iżnillāhi ta‘ālā wa hāżā mā yuktubu al-basmalatu wat-taṣliyatu ( [ada wafaq] ).",
]
TERJ77 = [
    '"Dan terangkatlah serta berhentilah (darah) dari kemaluan si Fulan demi hak nama-nama ini dan ayat yang agung: \'Bagi setiap berita ada tempat kedepannya (waktunya).\'" (QS. Al-An\'am: 67).',
    "Bab untuk Menghentikan Pendarahan (Cara Kedua):",
    "Dituliskan pada wadah yang bersih dengan misk aswad, lalu dilarutkan (direndam dengan air) dan diminumkan, maka darah akan berhenti dengan izin Allah Ta'ala. Kalimat yang ditulis meliputi Basmalah, penggalan Surah Al-Baqarah, serta azimah penyumpahan darah dengan menyebut nama Nabi Adam, Hawa, dan Nabi Musa, agar darah segera terhenti dan tidak kembali lagi atas izin Allah.",
    "Bab untuk Menghilangkan Sakit Kepala Menengah (Shuda' Muzmin):",
    "Dituliskan apa yang berikut ini dan dikalungkan/diikatkan di kepala, maka sakit kepala sebelah maupun berdenyut akan mereda dengan izin Allah Ta'ala. Yang ditulis meliputi Basmalah, selawat, serta rajah:",
    "[ada wafaq].",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Protokol Komunikasi Khofiyah / Pemanggilan Khodam Golongan Jin Mukmin (Hal. 76):",
    "- Menghadap ke arah kanan sambil membaca doa pertolongan khusus kepada ruhaniyyah jin mukmin sebanyak 7 kali.",
    "- Menoleh ke arah utara dan membaca asma' khusus (Bishaifidisy 3x, Bi-Qatlamid Yasy 7x) sampai mendengar salam, lalu berinteraksi secara batin untuk meminta hajat.",
    "- Terapi Pengasapan Kertas Pendarahan / Nazif (Hal. 76):",
    "- Menuliskan teks doa penghenti darah beserta rajah pada 3 lembar kertas putih menggunakan misk aswad.",
    "- Dilakukan pengasapan (bukhur) dengan membakar satu lembar kertas setiap malam selama 3 hari berturut-turut.",
    "- Terapi Air Lunturan Wadah untuk Pendarahan (Hal. 77): Menuliskan ayat Al-Qur'an dan doa sumpah darah pada piring/wadah bersih dengan tinta misk aswad, meluturkannya dengan air, lalu meminumkannya kepada pasien yang mengalami pendarahan hebat.",
    "- Azimat Pengikat Kepala untuk Migrain / Sakit Kepala (Hal. 77): Menuliskan rajah dan doa kesembuhan di atas media, lalu diikatkan atau ditaruh di kepala pasien untuk meredakan sakit kepala kronis (shuda' muzmin).",
]

FORBIDDEN = [
    "Berikut adalah transkripsi",
    "ringkasan terjemahan",
    "berdasarkan gambar naskah",
    "Pada tata letak manuskrip",
    "Sisi Kanan",
    "Sisi Kiri",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "(Ekstraksi Ritual)",
    "&amp;",
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
    if page == 76:
        return (
            [("ar", x) for x in AR76[:5]]
            + [("img", None)]
            + [("ar", x) for x in AR76[5:]]
            + [("la", x) for x in LAT76]
            + [("te", x) for x in TERJ76]
        )
    return (
        [("ar", x) for x in AR77]
        + [("img", None)]
        + [("la", x) for x in LAT77]
        + [("te", x) for x in TERJ77]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 76:
        return AR76[:5] + [""] + AR76[5:] + LAT76 + TERJ76 + [""]
    return AR77 + [""] + LAT77 + TERJ77 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return 5


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[76] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[76] + 1].startswith("ثُمَّ انْظُرْ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[76], heads[77])
        if texts[i].startswith("Tsumma unzhur biwajhika 'alal yamiini")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[76], heads[77])
        if texts[i].startswith("Kemudian penulis mengarahkan pelaku")
    )
    blank_tpl = deepcopy(els[heads[77] - 1])
    if texts[heads[77] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (76, 77):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[76]].getparent()
    removed = 0
    inserted = 0
    for n in (76, 77):
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

    for n in (76, 77):
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

    revised = "\n".join(ot[oh[76] : oh[78]])
    if revised.count("[ada wafaq]") != 6:
        raise AssertionError(f"[ada wafaq] count {revised.count('[ada wafaq]')} != 6")
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
    print("H76_77_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
