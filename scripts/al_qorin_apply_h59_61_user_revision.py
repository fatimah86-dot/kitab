#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 59-61 revision to the final DOCX.

Only the Arabic, Latin, and Indonesian text supplied by the user is
inserted.  Carried-over material from the pasted source is excluded:
the workspace/format introduction, image/source mapping, numbered
section labels, [Halaman ...] markers, markdown bullets, and the
stand-alone external note identifying the moon names.  Non-literal
"Khodam" glosses and "(Malaikat)" after "Empat Pemimpin" are also
omitted.  Existing Media/Langkah/Tujuan blocks remain unchanged.
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

AR59 = [
    "الْقَرِينُ وَعِلَاجُهُ",
    "وَالْمُلُوكُ الرُّوحَانِيَّةُ",
    "أَعْلَمُ أَخِي الْمُؤْمِنَ أَنَّ هُنَاكَ فِي عَالَمِ الْجِنِّ كَمَا هُوَ الْحَالُ فِي عَالَمِ الْإِنْسِ فَعِنْدَهُمَا الْأَطِبَّاءُ وَالشَّيَاطِينُ وَالْعَفَارِيتُ وَهُنَاكَ قَبَائِلُ كَثِيرَةٌ حَصْرُهَا عِنْدَ اللَّهِ وَحْدَهُ وَيُوجَدُ رِجَالٌ وَنِسَاءٌ مِنَ الْإِنْسِ لَا يَعْلَمُونَ شَيْئاً عَنْ هَذَا الْعَالَمِ وَيَدَّعُونَ الْعِلْمَ وَهُمْ دَجَّالُونَ وَكَذَّابُونَ وَيُصَدِّقُونَ أَنْفُسَهُمْ وَمِنْهُمْ مَنْ يَقُولُ إِنَّهُ يُحَارِبُ مَعَ الْجَانِّ جَانٌّ آخَرُ فَهُوَ كَاذِبٌ وَإِذَا نَظَرْتَ إِلَى حَالِهِ الْآنَ تَجِدُهُ مَرِيضاً فَتَقُولُ لَهُ لِمَاذَا لَا يُعَالِجُكَ الْجَانُّ فَيَقُولُ لَكَ إِنَّهُ فِي سَبِيلِهِ إِلَى الشِّفَاءِ لِأَنَّ الْجَانَّ فِعْلًا يُعَالِجُهُ - وَيَسْتَمِرُّ هَكَذَا سِنِينَ دُونَ شِفَاءٍ لِأَنَّهُ كَاذِبٌ وَلَا يَعْرِفُ أَيَّ شَيْءٍ عَنْهُمْ .",
    "وَلِكَيْ تَعْلَمَ يَا أَخِي الْمُؤْمِنَ الْحَقِيقَةَ فَيَجِبُ أَنْ تَعْرِفَ عِدَّةَ أَشْيَاءَ أَوَّلُهَا - الْأَيَّامُ - الْأَبْرَاجُ - أَسْمَاءُ الْقَمَرِ - أَسْمَاءُ السَّلَاطِينِ الْمَلَائِكَةِ - أَسْمَاءُ الْمُلُوكِ السَّبْعَةِ - أَسْمَاءُ الرُّوحَانِيَّةِ السَّبْعَةِ - أَسْمَاءُ الدَّرَارِي السَّبْعَةِ - أَسْمَاءُ",
]
LAT59 = [
    "Al-qarīnu wa ‘ilājuhū wal-mulūkur-rūḥāniyyah.",
    "A‘lamu akhīl-mu'mina anna hunāka fī ‘ālamil-jinni kamā huwal-ḥālu fī ‘ālamil-insi fa‘indahumāl-aṭibbā'u wasy-syayāṭīnu wal-‘afārītu wa hunāka qabā'ilu katsīratun ḥaṣruhā ‘indallāhi waḥdah. Wa yūjadu rijāluw-wa nisā'um-minal-insi lā ya‘lamūna syai'an ‘an hāżal-‘ālami wa yadda‘ūnal-‘ilma wa hum dajjālūna wa każżābūna wa yuṣaddiqūna anfusahum. Wa minhum may-yaqūlu innahū yuḥāribu ma‘al-jānni jānnun ākharu fahuwa kāżibun. Wa iżā naẓarta ilā ḥālihil-āna tajiduhū marīḍan fataqūlu lahū limāżā lā yu‘ālijukal-jānnu fayaqūlu laka innahū fī sabīlihī ilaṣy-syifā'i li'annal-jānna fi‘lan yu‘ālijuhū - wa yastamirru hākadzā sinīna dūna syifā'in li'annahū kāżibuw-wa lā ya‘rifu ayya syai'in ‘anhum.",
    "Wa likai ta‘lama yā akhīl-mu'minal-ḥaqīqata fayajibu an ta‘rifa ‘iddata asyyā'a awwaluhā - al-ayyāmu - al-abrāju - asmā'ul-qamari - asmā'us-salāṭīnil-malā'ikati - asmā'ul-mulūkis-sab‘ati - asmā'ur-rūḥāniyyatis-sab‘ati - asmā'ud-darārīs-sab‘ati - asmā'u...",
]
TERJ59 = [
    "Qarin, Pengobatannya, dan Raja-Raja Spiritual",
    "Ketahuilah wahai saudaraku yang beriman, bahwa di alam jin—sebagaimana halnya di alam manusia—terdapat para tabib (dokter), para setan, dan ifrit. Di sana terdapat kabilah yang sangat banyak, di mana jumlah batasannya hanya diketahui oleh Allah semata. Ada sebagian laki-laki dan perempuan dari kalangan manusia yang sebenarnya tidak mengetahui apa-apa tentang alam ini, namun mereka mengklaim memiliki ilmu. Mereka itu adalah para penipu (dajjal) dan pendusta, tetapi mereka membenarkan (kebohongan) diri mereka sendiri.",
    'Di antara mereka ada yang berkata bahwa dirinya berperang bersama jin melawan jin yang lain, maka ia adalah pendusta. Jika engkau melihat kondisinya sekarang, engkau akan mendapatinya sedang sakit. Lalu jika engkau bertanya kepadanya, "Mengapa jin (kawanmu) itu tidak mengobatimu?" Ia akan menjawab, "Dia (jin itu) sedang dalam proses menyembuhkanku, karena jin itu benar-benar sedang mengobatiku." Ia akan terus berada dalam keadaan (sakit) seperti itu selama bertahun-tahun tanpa ada kesembuhan, karena ia sebenarnya berbohong dan tidak mengetahui apa pun tentang mereka (jin).',
    "Agar engkau mengetahui kebenarannya wahai saudaraku yang beriman, maka engkau wajib mengetahui beberapa hal, yang pertama: Nama-nama Hari, Rasi Bintang (Zodiak), Nama-nama Bulan, Nama-nama Malaikat Penguasa, Nama-nama Tujuh Raja (Jin), Nama-nama Tujuh Entitas Spiritual, Nama-nama Tujuh Bintang yang Beredar (Planet/Tata Surya), Nama-nama...",
]

AR60 = [
    "الرُّؤُوسِ الْأَرْبَعَةِ .",
    '" الْأَيَّامُ " ...',
    "خَلَقَ اللَّهُ الْأَيَّامَ سَبْعَةً .",
    "وَأَوَّلُهُمَا ...",
    "١- الْأَحَدُ - وَهُوَ يَوْمُ الشَّمْسِ - وَمَعْدَنُهُ الذَّهَبُ",
    "٢- الِاثْنَيْنِ - وَهُوَ يَوْمُ الْقَمَرِ - وَمَعْدَنُهُ الْفِضَّةُ",
    "٣- الثُّلَاثَاءِ - وَهُوَ يَوْمُ الْمِرِّيخِ - وَمَعْدَنُهُ الْحَدِيدُ",
    "٤- الْأَرْبِعَاءِ - وَهُوَ يَوْمُ عُطَارِدَ - وَمَعْدَنُهُ الزِّئْبَقُ",
    "٥- الْخَمِيسِ - وَهُوَ يَوْمُ الْمُشْتَرَى - وَمَعْدَنُهُ الْقَصْدِيرُ",
    "٦- الْجُمُعَةِ - وَهُوَ يَوْمُ الزُّهَرَةِ - وَمَعْدَنُهُ النُّحَاسُ",
    "٧- السَّبْتِ - وَهُوَ يَوْمُ زُحَلَ - وَمَعْدَنُهُ الرَّصَاصُ",
    "هَذِهِ هِيَ الْأَيَّامُ وَلِكُلِّ يَوْمٍ دُرٌّ مِنْ الدَّرَارِي السَّبْعَةِ وَالدَّرَارِي السَّبْعَةُ هِيَ الَّتِي تَحْكُمُ مَا يَدُورُ فِي الْأَرْضِ وَفِي الْإِنْسَانِ مِثْلَ الْمَدِّ وَالْجَزْرِ وَغَيْرِهَا .",
    '" الْأَبْرَاجُ " ...',
    "١- بُرْجُ الْحَمَلِ ٢- الثَّوْرِ - ٣- الْجَوْزَاءِ - ٤- السَّرَطَانِ -",
]
LAT60 = [
    "...ar-ru'ūsil-arba‘ah.",
    '"Al-Ayyāmu"...',
    "Khalaqallāhul-ayyāma sab‘atan. Wa awwaluhumā...",
    "1- Al-aḥadu - wa huwa yaumusy-syamsi - wa ma‘dinuhuż-żahabu",
    "2- Al-itsnaini - wa huwa yaumul-qamari - wa ma‘dinuhul-fiḍḍatu",
    "3- Ats-tsulātsā'i - wa huwa yaumul-mirrīkhi - wa ma‘dinuhul-ḥadīdu",
    "4- Al-arbi‘ā'i - wa huwa yaumu ‘uṭārida - wa ma‘dinuhuz-zi'baqu",
    "5- Al-khamīsi - wa huwa yaumul-musytarā - wa ma‘dinuhul-qaṣdīru",
    "6- Al-jumu‘ati - wa huwa yaumuz-zuharati - wa ma‘dinuhun-nuḥāsu",
    "7- As-sabti - wa huwa yaumu zuḥala - wa ma‘dinuhur-raṣāṣu",
    "Hāżihī hiyal-ayyāmu wa likulli yaumin durrum-minad-darārīs-sab‘ati, wad-darārīs-sab‘atu hiya-llatī taḥkumu mā yadūru fil-arḍi wa fil-insāni mitslal-maddi wal-jazri wa ghairihā.",
    '"Al-Abrāju"...',
    "1- Burjūl-ḥamali, 2- Ats-Tsaūri, 3- Al-Jauzā'i, 4- As-Saraṭāni...",
]
TERJ60 = [
    "...Empat Pemimpin.",
    '"Nama-nama Hari"...',
    "Allah menciptakan tujuh hari. Yang pertama adalah...",
    "Ahad - yaitu harinya Matahari - logamnya adalah Emas.",
    "Senin - yaitu harinya Bulan - logamnya adalah Perak.",
    "Selasa - yaitu harinya Mars - logamnya adalah Besi.",
    "Rabu - yaitu harinya Merkurius - logamnya adalah Raksa (Merkuri).",
    "Kamis - yaitu harinya Jupiter - logamnya adalah Timah.",
    "Jumat - yaitu harinya Venus - logamnya adalah Tembaga.",
    "Sabtu - yaitu harinya Saturnus - logamnya adalah Timbal.",
    "Inilah nama-nama hari. Pada setiap hari terdapat mutiara dari tujuh bintang yang beredar (Ad-Darari As-Sab'ah). Tujuh bintang yang beredar inilah yang (dengan izin Allah) mengatur siklus yang terjadi di bumi dan pada diri manusia, seperti pasang surut air laut dan lain sebagainya.",
    '"Rasi Bintang (Al-Abraj)"...',
    "Aries (Domba), 2. Taurus (Banteng), 3. Gemini (Kembar), 4. Cancer (Kepiting), ...",
]

AR61 = [
    "٥- الْأَسَدِ ٦- السُّنْبُلَةِ ٧- الْمِيزَانِ ٨- الْعَقْرَبِ ٩- الْقَوْسِ ١٠- الْجَدْيِ ١١- الدَّلْوِ ١٢- الْحُوتِ .",
    '" أَسْمَاءُ الدَّرَارِي السَّبْعَةِ " ...',
    "١- الشَّمْسِ ٢- الْقَمَرِ ٣- الْمِرِّيخِ ٤- عُطَارِدَ ٥- الْمُشْتَرَى ٦- الزُّهَرَةِ ٧- زُحَلَ .",
    '" أَسْمَاءُ الْقَمَرِ "',
    "لِيَاخِيمٍ",
    "لِيَالْغُورٍ",
    "لِيَافُورٍ",
    "لِيَارُوثٍ",
    "لِيَارُوغٍ",
    "لِيَارُوشٍ",
    "لِيَاشَلْشٍ",
    "أَسْمَاءُ الْقَمَرِ مَقْلُوبَةً",
    "شَلْيَاءُ",
    "سُورَائِيلُ",
    "غُورَائِيلُ",
    "ثُورَائِيلُ",
    "دُوفَائِيلُ",
    "غَلَاسِيلُ",
    "مَخَائِيلُ",
]
LAT61 = [
    "...5- Al-Asadi, 6- As-Sumbulati, 7- Al-Mīzāni, 8- Al-‘Aqrabi, 9- Al-Qausi, 10- Al-Jadyi, 11- Ad-Dalwi, 12- Al-Ḥūti.",
    '"Asmā\'ud-Darārīs-Sab‘ati"...',
    "1- Asy-Syamsi, 2- Al-Qamari, 3- Al-Mirrīkhi, 4- ‘Uṭārida, 5- Al-Musytarā, 6- Az-Zuharati, 7- Zuḥala.",
    '"Asmā\'ul-Qamari"',
    "Liyākhīmin, Liyālghūrin, Liyāfūrin, Liyārūtsin, Liyārūghin, Liyārūsyin, Liyāsyalsyin.",
    "Asmā'ul-Qamari maqlūbatan:",
    "Syalyā'u, Sūrā'īlu, Ghūrā'īlu, Tsūrā'īlu, Dūfā'īlu, Ghalāsīlu, Makhā'īlu.",
]
TERJ61 = [
    "...5. Leo (Singa), 6. Virgo (Gandum/Sumbulah), 7. Libra (Timbangan), 8. Scorpio (Kalajengking), 9. Sagittarius (Pemanah), 10. Capricorn (Kambing Laut/Jady), 11. Aquarius (Timba/Dalw), 12. Pisces (Ikan/Hut).",
    '"Nama-nama Tujuh Bintang yang Beredar"...',
    "Matahari, 2. Bulan, 3. Mars, 4. Merkurius, 5. Jupiter, 6. Venus, 7. Saturnus.",
    '"Nama-nama Bulan"',
    "Liyakhim (لياخيم)",
    "Liyalghur (ليالغور)",
    "Liyafur (ليافور)",
    "Liyaruts (لياروث)",
    "Liyarugh (لياروغ)",
    "Liyarush (لياروش)",
    "Liyashalsh (لياشلش)",
    '"Nama-nama Bulan Dibalik"',
    "Shalya'u",
    "Sura'ilu",
    "Ghura'ilu",
    "Tsura'ilu",
    "Dufa'ilu",
    "Ghalasilu",
    "Makha'ilu",
]

UNITS = {
    59: AR59 + LAT59 + TERJ59,
    60: AR60 + LAT60 + TERJ60,
    61: AR61 + LAT61 + TERJ61,
}
COUNTS = {
    59: (len(AR59), len(LAT59), len(TERJ59)),
    60: (len(AR60), len(LAT60), len(TERJ60)),
    61: (len(AR61), len(LAT61), len(TERJ61)),
}
FORBIDDEN = [
    "arabic-manuscript-translator",
    "Berdasarkan format pola",
    "Pada gambar yang dilampirkan",
    "source 16",
    "source 17",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi Washal",
    "[Halaman",
    "Asma' Ath-Thahathil",
    "(Khodam",
    "Nama Khodam Malaikatnya",
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


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    if any(has_drawing_el(els[i]) for i in range(heads[59], heads[62])):
        raise AssertionError("units 59-61 unexpectedly carry an image")

    media_indices: dict[int, int] = {}
    retained_tails: dict[int, list[str]] = {}
    for n in (59, 60, 61):
        media_i = next(
            i for i in range(heads[n], heads[n + 1]) if texts[i].strip() == "Media:"
        )
        media_indices[n] = media_i
        retained_tails[n] = texts[media_i : heads[n + 1]]

    arab_tpl = deepcopy(els[heads[59] + 1])
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[59], heads[60])
        if texts[i].startswith("Al-qariinu")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[59], heads[60])
        if texts[i].startswith("Qarin dan Pengobatannya")
    )

    body = els[heads[59]].getparent()
    removed = 0
    for n in (59, 60, 61):
        heading_el = els[heads[n]]
        media_el = els[media_indices[n]]
        node = heading_el.getnext()
        while node is not None and node is not media_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        arab_count, latin_count, _ = COUNTS[n]
        unit_texts = UNITS[n]
        for pos, text in enumerate(unit_texts):
            template = (
                arab_tpl
                if pos < arab_count
                else latin_tpl
                if pos < arab_count + latin_count
                else terj_tpl
            )
            media_el.addprevious(make_para(template, text))

    doc.save(TARGET)

    out = Document(TARGET)
    ot = [p.text for p in out.paragraphs]
    oh = find_heads(ot)
    if sorted(oh) != list(range(1, 123)):
        raise AssertionError("headings broken")
    for n in (59, 60, 61):
        got = ot[oh[n] + 1 : oh[n + 1]]
        expected = UNITS[n] + retained_tails[n]
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:120]!r}\n exp: {b[:120]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")

    front = "\n".join(ot[oh[59] : oh[62]])
    for fragment in FORBIDDEN:
        if fragment.lower() in front.lower():
            raise AssertionError(f"carried-over fragment remains: {fragment}")
    if len(out.inline_shapes) != 26:
        raise AssertionError("image count changed")
    if media_hashes(TARGET) != media_hashes(SOURCE_FOR_MEDIA):
        raise AssertionError("media hashes/order changed")

    print(f"removed_old_layer1_paras={removed}")
    print(f"inserted_layer1_paras={sum(len(v) for v in UNITS.values())}")
    print(f"total_paragraphs={len(ot)}")
    print(f"bytes={TARGET.stat().st_size}")
    print(f"sha256={hashlib.sha256(TARGET.read_bytes()).hexdigest()}")
    print("H59_61_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
