#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 72-73 revision to the final DOCX.

Existing precision wafaq images are retained: Halaman 72 at its
rajah row after the opening quotation sequence, and Halaman 73 after
the line containing "[ada wafaq]".  Excludes carried-over
introductory/layout text, numbered section labels, [Halaman ...]
markers, and "(Ekstraksi Ritual)".  Markdown asterisks are
normalized to document bullets or removed from textual lists.
Places the combined Tata Cara Praktik at the end of Halaman 73.
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

AR72 = [
    "فَإِنَّهَا تَحْمِلُ بِإِذْنِ اللَّهِ تَعَالَى وَهَذَا مَا يُكْتَبُ ( يَكْتُبُ أَيْضاً وَيَحْمِلُ ) الْبَسْمَلَةَ وَالنَّصْلِيَةَ وَالْفَاتِحَةَ فَ جَ شَ ثَ ظَ خَ زْ جَبَّارٌ شَكُورٌ ثَابِتٌ ظَهِيرٌ خَبِيرٌ وَصَلِّ اللَّهُ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلَّمَ.",
    "جَبَّارٌ شَكُورٌ ثَابِتٌ ظَهِيرٌ خَبِيرٌ وَصَلِّ اللَّهُ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلَّمَ.",
    "( البسملة وحولها بسم الله الرحمن الرحيم الم الله لا اله الا هو الحي القيوم الى العزيز ) - فَتَقَبَّلَهَا رَبُّهَا بِقَبُولٍ حَسَنٍ إِلَى حِسَابٍ ( سورة آل عمران ) قَالَ رَبِّ اني يكون لى غلام وقد بلغنى الكبر وامرآتى عاقر قال كذلك الله يفعل ما يشاء قال رب اجعل لى آية قال آيتك الا تكلم الناس ثلاثة ايام الا رمزا الى ( آل عمران ) ( وهذا الذي خلقكم من نفس واحدة وجعل منها زوجها ليسكن اليها فلما تغشاها حملت حملا خفيفا فمرت به ) الشاكِرين ( الاعراف ) كهيعص.",
    "ذكْرُ رَحْمَةِ رَبِّكَ زَكَرِيَّا إِلَى مَقْضِيّاً فحملته بحملته باذَن الله حملته بقدره الله حملته بلطف الله حملته بلا حول ولا قوة الا بالله العلى العظيم حملته الى منسيا او لم يرا الذين كفروا ان السموات والارض كانتا رتقا ففتقناهما الى يؤمنون.",
    "وزكريا اذ نادى ربه رب لا تذرنى فردا وانت خير الوارثين.",
]
LAT72 = [
    "Fa-innahā taḥmalu bi-iżnillāhi ta‘ālā wa hāżā mā yuktubu (yaktubu aiḍan wa yaḥmilu) al-basmalata wan-naṣliyata wal-fātiḥata fā' jīm syīn tsā' ẓā' khā' zāy jabbārun syakūrun tsābitun ẓahīrun khabīrun wa ṣallallāhu ‘alā sayyidinā muḥammadin wa ‘alā ālihī wa ṣaḥbihī wa sallam.",
    "(Al-basmalatu wa ḫaulahā bismillāhir-raḥmānir-raḥīm alif lām mīm allāhu lā ilāha illā huwal-ḥayyul-qayyūmu ilā al-‘azīzi) - fa-taqabbalahā rabbuhā biqabūlin ḥasanin ilā ḥisābin (sūratu āli ‘imrān) qāla rabbi annī yakūnu lī ghulāmun wa qad balaghanial-kibaru wa amra'atī ‘āqirun qāla każālikallāhu yaf’alu mā yasyā'u qāla rabbi ij‘al lī āyatan qāla āyatuka alā tukalliman-nāsatsalātsata ayyāmin illā ramzan ilā (āli ‘imrān) (wa huwal-lażī khalaqakum min nafsin wāḥidatin wa ja‘ala minhā zaujahā liyaskuna ilaihā falammā taghasyāhā ḥamalat ḥamlan khafīfan famarrat bih) asy-syākirīn (al-‘arāf) kāf hā yā ‘aīn ṣād.",
    "Żikru raḥmati rabbika zakariyyā ilā maqḍiyyā, fa-ḥamalat-hu bi-iżnillāh ḥamalat-hu bi-qudratillāh ḥamalat-hu bi-luṭfillāh ḥamalat-hu bilā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīm ḥamalat-hu ilā mansiyyan au lam yara allażīna kafarū anna-ssamāwāti wal-arḍa kāntata ratْqan fa-fataqnāhumā ilā yu'minūn.",
    "Wa zakariyyā iż nādā rabbahu rabbi lā تَżarnī fardan wa anta khairul-wāritīn.",
]
TERJ72 = [
    "Maka sesungguhnya ia akan hamil dengan izin Allah Ta'ala, dan inilah yang ditulis (juga ditulis dan dibawa): Al-Basmalah, An-Nashliyah, Al-Fatihah, (F J Sy Ts Zh Kh Z), Jabbarun Syakuurun Tsabitum Zhahiirun Khabiirun, serta selawat dan salam semoga tercurah kepada junjungan kita Nabi Muhammad, keluarga, dan para sahabatnya.",
    "(Dilanjutkan dengan kutipan ayat-ayat penjagaan dan kehamilan dari Al-Qur'an): Mulai dari Surah Al-Imran ayat 37, 40, 41, Surah Al-A'raf ayat 189, pembukaan Surah Maryam (Kaf Ha Ya 'Ain Shad), kisah Nabi Zakaria, hingga Surah Al-Anbiya' ayat 89 (Rabbi la tadzarni fardan wa anta khairul waritsin).",
]

AR73 = [
    "ايها الناس ان كنتم في ريب من البعث الى الخالقين هو الذي خلقكم من تراب ثم من نطفة ثم من علقة ثم نخرجكم طفلا ثم لتكونوا شيُوخا الم تك نطفة من مني يمنى ثم كان علقة مخلقه فسوى وصوره لم يكن كلما . وتَحْمِلُهَا عَلَى بَطْنِهَا أَوْ عَلَى ظَهْرِهَا مُجَرَّبٌ.",
    "فَائِدَةٌ لِلْحَمْلِ :",
    "تَكْتُبُ مَا يَاتِي فِي صَحْنٍ صِينِيٍّ فِي وَقْتِ التَّطَهُّرِ مِنَ الْحَيْضِ وَتُمْحَى الْكِتَابَةِ بِلَبَنِ عَنْزَةٍ سَوْدَاءَ فَإِنَّ اللَّهَ تَعَالَى يَجْعَلُ فِيهَا الْحَمْلَ وَهَذَا مَا تَكْتُبُ :",
    "الْبَسْمَلَةُ وصلعم وسورة الفَاتِحَة فَجِشَ تَظْتَخِرْ [ada wafaq].",
    "والحوقلة و اول سورة آل عمران الى الحكيم . فتقبلها ربها بقبول حسن الي غير حساب \" قال رب اني يكون غلام الي الابصار ( آل عمران ) هُو الَّذِي خَلَقَكُم مِّن نَّفْسٍ وَاحِدَةٍ وَجَعَلَ مِنْهَا زَوْجَهَا لِيَسْكُنَ إِلَيْهَا ( الاعراف ) كهيعص الي وعشيا ( مريم ) قال انما انا رسول ربك الي حملته باذن الله فحملته بقدرة الله فحملته بلطف الله.",
]
LAT73 = [
    "Ayyuhan-nāsu in kuntum fī raibim-minal-ba‘tsi ilā al-khāliqīna huwal-lażī khalaqakum min turābin tsumma min nuṭfatin tsumma min ‘alaqatin tsumma nukhrijukum ْṭiflan tsumma litakūnū syuyūkhan alam tak nuṭfatan min miniyyin yumnā tsumma kāna ‘alaqatan mukhalaqatan fasawā wa ṣūrahum lam yakun kullā. Wa taḥmuhuhā ‘alā baṭnihā au ‘alā ẓahrihā mujarrab.",
    "Fā'idatun lil-ḥaml:",
    "Taktubu mā yātī fī ṣaḥnin ṣīniyyin fī waqtit-taṭahhuri minal-ḥaiḍi wa tumḥal-kitābatu bilabani ‘anzatin saudā'a fa-innal-laha ta‘ālā yaj‘alu fīhil-ḥamla wa hāżā mā taktubu:",
    "Al-basmalatu wa ṣal-‘am wa sūratul-fātiḥatu fā' jīm syīn taẓtakhir ( [ada wafaq] ).",
    "Wal-ḥauqolatu wa awwalu sūrati āli ‘imrāna ilā al-ḥakīm. Fa-taqabbalahā rabbuhā biqabūlin ḥasanin ilā ghairi ḥisābin \"qāla rabbi annī yakūnu ghulāmun ilal-abṣār (āli ‘imrān) huwal-lażī khalaqakum min nafsin wāḥidatin wa ja‘ala minhā zaujahā liyaskuna ilaihā (al-‘arَāf) kāf hā yā ‘aīn ṣād ilā ‘asyiyyan (maryam) qāla innamā anā rasūlu rabbika ilā ḥamalat-hu bi-iżnillāhi fa-ḥamalat-hu bi-qudratillāhi fa-ḥamalat-hu bi-luṭfillāh.",
]
TERJ73 = [
    '"Hai manusia, jika kamu dalam keraguan tentang kebangkitan (maka ketahuilah) sesungguhnya Kami telah menjadikan kamu dari tanah, kemudian dari setetes mani, kemudian dari segumpal darah, kemudian dari segumpal daging yang sempurna penciptaannya dan yang tidak sempurna..." (QS. Al-Hajj: 5). Dan dibawanya (dikalungkan) pada perutnya atau pada punggungnya, ini sudah teruji (mujarab).',
    "Faedah untuk Kehamilan:",
    "Tulislah apa yang berikut ini pada piring porselen pada waktu suci dari haid, lalu lunturkan tulisannya dengan susu kambing hitam, maka sesungguhnya Allah Ta'ala akan menjadikan kehamilan padanya. Dan inilah yang harus ditulis:",
    "Al-Basmalah, Shal'am, Surah Al-Fatihah, Fajis Tazhtakhir, [ada wafaq].",
    "Serta bacaan Hauqalah, awal Surah Al-Imran hingga kata Al-Hakim, penggalan ayat-ayat kehamilan dari Surah Al-Imran, Al-A'raf, dan Maryam (Qāla innamā anā rasūlu rabbika... hingga akhir).",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "- Azimat Kalung Perut/Punggung (Hal. 72 & 73): Penulisan rangkaian ayat-ayat Al-Qur'an tentang penciptaan janin (seperti QS. Al-Hajj: 5) dan doa-doa nabi (Zakaria) pada media kertas/kulit, lalu dikalungkan di bagian perut atau punggung sang istri sebagai ikhtiar batin agar lekas mendapatkan keturunan.",
    "- Terapi Air Lunturan Porselen Susu Kambing Hitam (Hal. 73):",
    "- Menyiapkan media piring porselen putih (shaḥn ṣīniyy).",
    "- Menuliskan rangkaian Basmalah, huruf rajah, Surah Al-Fatihah, awal Surah Al-Imran, dan ayat-ayat kehamilan di atas piring tersebut pada masa suci dari haid.",
    "- Melunturkan/membasuh tulisan tersebut menggunakan susu kambing hitam murni.",
    "- Meminum air lunturan susu tersebut untuk merangsang kesuburan dan terjadinya kehamilan dengan izin Allah Ta'ala.",
]

FORBIDDEN = [
    "Berikut adalah transkripsi",
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
    if page == 72:
        return (
            [("ar", x) for x in AR72[:3]]
            + [("img", None)]
            + [("ar", x) for x in AR72[3:]]
            + [("la", x) for x in LAT72]
            + [("te", x) for x in TERJ72]
        )
    return (
        [("ar", x) for x in AR73[:4]]
        + [("img", None)]
        + [("ar", x) for x in AR73[4:]]
        + [("la", x) for x in LAT73]
        + [("te", x) for x in TERJ73]
        + [("te", x) for x in TATACARA]
    )


def expected_texts(page: int) -> list[str]:
    if page == 72:
        return AR72[:3] + [""] + AR72[3:] + LAT72 + TERJ72 + [""]
    return AR73[:4] + [""] + AR73[4:] + LAT73 + TERJ73 + TATACARA + [""]


def expected_image_position(page: int) -> int:
    return 3 if page == 72 else 4


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[72] + 1])
    if has_drawing_el(arab_tpl) or not texts[heads[72] + 1].startswith("فَإِنَّهَا تَحْمِلُ"):
        raise AssertionError("Arabic template mismatch")
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[72], heads[73])
        if texts[i].startswith("Fa-innahaa tahmilu bi-idznillaahi")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[72], heads[73])
        if texts[i].startswith("Penulis melanjutkan klaimnya:")
    )
    blank_tpl = deepcopy(els[heads[73] - 1])
    if texts[heads[73] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (72, 73):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[72]].getparent()
    removed = 0
    inserted = 0
    for n in (72, 73):
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

    for n in (72, 73):
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

    revised = "\n".join(ot[oh[72] : oh[74]])
    if revised.count("[ada wafaq]") != 3:
        raise AssertionError(f"[ada wafaq] count {revised.count('[ada wafaq]')} != 3")
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
    print("H72_73_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
