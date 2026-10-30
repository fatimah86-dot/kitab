#!/usr/bin/env python3
"""Apply the user's cleaned Halaman 64-65 revision to the final DOCX.

Excludes carried-over material: code fence, workspace/format
introduction, image/source mapping, numbered section labels,
[Halaman ...] markers, the label "(Ekstraksi Ritual)", and the
translation-side editorial aside "(Lanjutan dari penangkal
sebelumnya)".  Markdown asterisks in the practice section are
normalized to the document's "- " bullets.  Keeps each precision
wafaq image after its page's Terjemahan and places the supplied
combined Tata Cara Praktik after Halaman 65.
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

AR64 = [
    "وَالنَّظْرَةِ السُّوءِ وَالرَّجْفَةِ وَالْعَكْسِ وَالسِّحْرِ وَالتَّعْطِيلِ وَسِحْرِ وَسَاحِرَةٍ وَمَكْرِ مَاكِرَةٍ وَمِنْ سَائِرِ الْجِنِّ وَالشَّيَاطِينِ وَجُنُودِ إِبْلِيسَ أَجْمَعِينَ وَالتَّوَابِعِ وَالْقَرَائِنِ وَبِحَقِّ مَنْ قَالَ وَقَوْلُهُ الْحَقُّ قَالَ مُوسَى مَا جِئْتُمْ بِهِ السِّحْرُ إِنَّ اللَّهَ سَيُبْطِلُهُ إِنَّ اللَّهَ لَا يُصْلِحُ عَمَلَ الْمُفْسِدِينَ .",
    "وَقَدِمْنَا إِلَى مَا عَمِلُوا مِنْ عَمَلٍ فَجَعَلْنَاهُ هَبَاءً مَنْثُوراً إِلَى يَصْعَدُ الْكَكْلِمُ الطَّيِّبُ وَالْعَمَلُ الصَّالِحُ يَرْفَعُهُ .",
    "اللَّهُمَّ اصْرِفْ وَارْفَعْ وَاذْهَبْ عَنْ فُلَانٍ كُلَّ سِحْرٍ وَصَدْدٍ كَرَاهِيَةٍ وَتَبْطِيلٍ وَمَنْ كُلَّ مَا يُؤْدِيهِ مَاذَا جَاءَ وَعَدَ رَبِّي جَعَلَهُ دَكّاً . وَعَدَ رَبِّي جَعَلَهُ دَكّاً ، وَكَانَ وَعْدُ رَبِّي حَقّاً وَبِحَقِّ هَذِهِ الْأَسْمَاءِ",
    "خَاتَمُ سُلَيْمَانَ ✡ /|\\ م # ١١١١ هـ و",
    "وَالْحَوْقَلَةِ وَصَلَّى اللَّهُ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ وَسَلَّمَ .",
    "يُكْتَبُ وَيُحْمَلُ بِمِسْكٍ وَزَعْفَرَانٍ وَمَاءِ وَرْدٍ .",
    "مُجَرَّبٌ صَحِيحٌ .",
]
LAT64 = [
    "Wan-naẓratis-sū'i war-rajfati wal-‘aksi was-siḥri wat-ta‘ṭīli wa siḥri wa sāḥiratin wa makri mākiratin wa min sā'iril-jinni wasy-syayāṭīni wa junūdi iblīsa ajma‘īna wat-tawābi‘ati wal-qarā'ini wa biḥaqqi man qāla wa qauluhul-ḥaqqu: qāla mūsā mā ji'tum bihis-siḥru innallāha sayubṭiluhū, innallāha lā yuṣliḥu ‘amalal-mufsidin.",
    "Wa qadimnā ilā mā ‘amilū min ‘amalin faja‘alnāhū habā'am manthūran. (Yas‘adal-kalimuth-thayyibu wal-‘amalus-ṣāliḥu yarfa‘uh).",
    "Allāhumma iṣrif warfa‘ ważhab ‘an fulāni kullu siḥrin wa ṣaddin karāhiyatin wa tabṭīlin wa min kulli mā yu'dīhi māżā jā'a wa‘ada rabbī ja‘alahu dakkā'. Wa‘ada rabbī ja‘alahu dakkā', wa kāna wa‘du rabbī ḥaqqā, wa biḥaqqi hāżihil-asmā'i:",
    "Khātamu sulaimāna (✡ /|\\ m # ١١١١ هـ و)",
    "Wal-ḥauqalatu wa ṣallallāhu ‘alā sayyidinā muḥammadin wa ‘alā ālihī wa ṣaḥbihī wa sallam.",
    "Yuktabu wa yuḥmalu bimiskin wa za‘farānin wa mā'i wardin.",
    "Mujarrabun ṣaḥīḥ.",
]
TERJ64 = [
    "... Dan (dari gangguan) pandangan mata jahat (nazhratus-su'), gemetar, pembalikan keadaan, sihir, penelantaran (ta'thil), sihir penyihir, tipu daya wanita penyihir, dari seluruh jin, setan, bala tentara Iblis sekalian, tawabi' (jin pengikut), dan qarin (pendamping). Demi hak Zat yang berfirman dan firman-Nya adalah benar: Musa berkata: \"Apa yang kamu lakukan itulah sihir, sesungguhnya Allah akan membatalkannya, sesungguhnya Allah tidak membiarkan perbuatan orang-orang yang berbuat kerusakan.\" (QS. Yunus: 81).",
    "Dan Kami hadapi segala amal yang mereka kerjakan, lalu Kami jadikan amal itu bagaikan debu yang berterbangan. (QS. Al-Furqan: 23). Kepada-Nya lah naik perkataan-perkataan yang baik dan amal saleh akan mengangkatnya.",
    "\"Ya Allah, palingkanlah, angkatlah, dan lenyapkanlah dari si Fulan (nama pasien) segala bentuk sihir, hambatan, kebencian, pembatalan, dan segala hal yang menyakitkannya... Apabila janji Tuhanku datang, Dia akan menjadikannya hancur luluh. Dan janji Tuhanku adalah benar.\"",
    "Beserta dengan hak nama-nama ini: Khatam Sulaiman (✡ /|\\ م # ١١١١ هـ و), dan bacaan Hauqalah, serta semoga selawat dan salam senantiasa tercurah kepada junjungan kita Nabi Muhammad, beserta keluarga dan para sahabatnya.",
    "(Azimat ini) ditulis dan dibawa (dikalungkan) dengan (tinta) musk, za'faran, dan air mawar.",
    "(Ini adalah ilmu yang) Mujarab lagi Shahih.",
]

AR65 = [
    "( لِلتَّدَاوِي مِنَ الْمَرَضِ )",
    "يُكْتَبُ فِي إِنَاءٍ صِينِيٍّ بِزَعْفَرَانٍ وَمَاءِ وَرْدٍ وَيُحْمَى بِمَاءٍ بِئْرٍ لَا يَرَاهُ النِّيرَيْنِ .",
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ ذَلِكَ تَخْفِيفٌ مِنْ رَبِّكُمْ وَرَحْمَتُهُ يُرِيدُ اللَّهُ أَنْ يُخَفِّفَ عَنْكُمْ وَخُلِقَ الْإِنْسَانُ ضَعِيفاً وَله مَا سَكَنَ فِي اللَّيْلِ وَالنَّهَارِ وَهُوَ السَّمِيعُ الْعَلِيمُ وَلَوْ شَاءَ لَجَعَلَهُ سَاكِناً أَنْ يَشَأْ يُسْكِنِ الرِّيحَ فَيَظْلَلْنَ رَوَاكِدَ عَلَى ظَهْرِهَا .",
    "الم الم المص الر الر الر الر كهيعص طه طسم الم الم الم الم يس ص حم حم حم حم حم عسق حم حم حم حم حم ق ن",
    "بِسْمِ اللَّهِ الْعَظِيمِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَجَعَلَ فِيهِ رَحْمَةً وَشِفَاءً اللَّهُمَّ اشْفِنِي أَنْتَ الشَّافِي الْمُعَافِي مِنْ كُلِّ عِلَّةٍ وَمَرَضٍ شِفَاءً لَا يُغَادَرُ سَقَماً وَلَا أَلَمَا بِالَّذِي لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ وَصَلَّى اللَّهُ عَلَى سَيِّدِنَا مُحَمَّدٍ وَعَلَى آلِهِ وَصَحْبِهِ أَجْمَعِينَ .",
    "خَاتَمُ سُلَيْمَانَ ✡ /|\\ م # ١١١١ هـ و",
]
LAT65 = [
    "(Lit-tadāwī minal-maraḍ)",
    "Yuktabu fī inā'in ṣīniyyin biza‘farānin wa mā'i wardin wa yuḥmā bimā'i bi'rin lā yarāhun-nīraini.",
    "Bismillāhir-raḥmānir-raḥīm. Żālika takhفīfum-mir-rabbikum wa raḥmatuh, yurīdullāhu an yukhaffifa ‘ankum wa khuliqal-insānu ḍَعīfā. Wa lahū mā sakana fil-laili wan-nahāri wa huwas-samī‘ul-‘alīmu. Wa lau syā'a laja‘alahū sākinan ay-yasyā' yuskinir-rīḥa fayaẓlalna rawākida ‘alā ẓahrihā.",
    "Alif Lām Mīm, Alif Lām Mīm Ṣād, Alif Lām Rā, Alif Lām Rā, Alif Lām Rā, Alif Lām Rā, Kāf Hā Yā ‘Aīn Ṣād, Ṭā Hā, Ṭā Sīn Mīm, Alif Lām Mīm, Alif Lām Mīm, Alif Lām Mīm, Yā Sīn, Ṣād, Hā Mīm, Hā Mīm, Hā Mīm, Hā Mīm, Hā Mīm, ‘Aīn Sīn Qāf, Hā Mīm, Hā Mīm, Hā Mīm, Hā Mīm, Hā Mīm, Qāf, Nūn.",
    "Bismillāhil-‘aẓīmil-lażī lā yaḍurru ma‘asmihī syai'un fil-arḍi wa lā fis-samā'i wa ja‘ala fīhi raḥmatan wa syifā'a. Allāhummasy-finī antasy-syāfī al-mu‘āfī min kulli ‘illatin wa maraḍin syifā'an lā yughādiru saqaman wa lā alamā, bial-lażī lā ḥaula wa lā quwwata illā billāhil-‘aliyyil-‘aẓīm. Wa ṣallallāhu ‘alā sayyidinā muḥammadin wa ‘alā ālihī wa ṣaḥbihī ajma‘īn.",
    "Khātamu sulaimāna (✡ /|\\ m # ١١١١ هـ و)",
]
TERJ65 = [
    "(Untuk Pengobatan dari Penyakit)",
    "Ditulis di dalam wadah porselen (inā' ṣīniyy) dengan (tinta) za'faran dan air mawar, lalu dilarutkan/direndam dengan air sumur yang tidak pernah melihat dua cahaya (matahari dan bulan - yakni diambil pada malam hari atau tempat tertutup dari sinar langsung).",
    "Dengan menyebut nama Allah Yang Maha Pengasih lagi Maha Penyayang. Allah hendak memberikan keringanan kepadamu, dan manusia dijadikan bersifat lemah. (QS. An-Nisa: 28). Dan kepunyaan-Nya lah segala apa yang diamati di malam dan siang hari, dan Dialah Yang Maha Mendengar lagi Maha Mengetahui. (QS. Al-An'am: 13). Dan jika Allah menghendaki, niscaya Dia jadikan angin itu tenang, maka jadilah kapal-kapal itu terdiam kaku di atas permukaan laut. (QS. Asy-Syura: 33).",
    "(Dilanjutkan dengan pembacaan huruf-huruf muqatha'ah): Alif Lam Mim, Alif Lam Mim Shad, Alif Lam Ra... hingga akhir rangkaian huruf terputus.",
    "Dengan menyebut nama Allah Yang Maha Agung, yang bersama nama-Nya tidak ada satu pun yang membahayakan di bumi maupun di langit, dan Dia menjadikan padanya rahmat dan kesembuhan. Ya Allah, sembuhkanlah aku, Engkaulah Yang Maha Penyembuh lagi Maha Menyehatkan dari segala penyakit dan penderitaan, dengan kesembuhan yang tidak meninggalkan rasa sakit dan tidak pula kepedihan, dengan perantara (zat) yang tiada daya dan tiada kekuatan melainkan dengan pertolongan Allah Yang Maha Tinggi lagi Maha Agung. Semoga selawat Allah tercurah kepada junjungan kita Nabi Muhammad, beserta keluarga dan para sahabatnya sekalian.",
    "Khatam Sulaiman (✡ /|\\ م # ١١١١ هـ و).",
]

TATACARA = [
    "4. Tata Cara Praktik",
    "Berdasarkan Halaman 64 dan 65, bab ini mencakup dua metode pengobatan utama: Azimat Pelindung/Penolak Sihir (Halaman 64) dan Air Larutan Obat Penyakit Medis/Non-medis (Halaman 65).",
    "Metode 1: Penulisan Azimat Penolak Sihir & Ain (Halaman 64)",
    "- Bahan Tulis: Gunakan tinta campuran Misk (kasturi), Za'faran, dan Air Mawar.",
    "- Media: Ditulis pada kertas putih atau media yang sesuai, kemudian dilipat dan dijadikan azimat untuk dibawa/dikalungkan (yaktubu wa yuḥmalu) oleh pasien yang terkena sihir, ain, 'aks (pembalikan nasib/keadaan), atau gangguan jin.",
    "- Kandungan Teks: Berisi ayat-ayat pembatal sihir (QS. Yunus: 81, QS. Al-Furqan: 23), doa pencabutan sihir/kebencian, ditutup dengan simbol Khatam Sulaiman dan Selawat.",
    "Metode 2: Terapi Air Larutan Porselen untuk Penyakit (Halaman 65)",
    "- Media Penulisan: Siapkan wadah atau piring porselen putih yang bersih (inā' ṣīniyy).",
    "- Tinta & Formula: Tuliskan seluruh ayat, rangkaian huruf muqatha'ah, dan doa penyembuhan yang tertera di Halaman 65 menggunakan campuran Za'faran dan Air Mawar.",
    "- Air Rendaman (Al-Mahwu): Lunturkan tulisan tersebut menggunakan air sumur khusus yang diambil pada kondisi di mana air tersebut tidak pernah tersentuh/terkena sinar matahari dan bulan secara langsung (la yarāhun-nīraini - biasanya diambil malam hari atau dari sumur tertutup).",
    "- Penggunaan: Air lunturan rajah/ayat porselen tersebut kemudian diminumkan kepada orang yang sakit untuk menyembuhkan segala jenis penyakit atas izin Allah SWT.",
]

LAYERS = {
    64: (AR64, LAT64, TERJ64),
    65: (AR65, LAT65, TERJ65),
}
FORBIDDEN = [
    "arabic-manuscript-translator",
    "Berdasarkan format pola",
    "Pada gambar yang dilampirkan",
    "source 11",
    "Teks Arab (Transkripsi",
    "Cara Baca (Transliterasi",
    "[Halaman",
    "Sisi Kanan",
    "Sisi Kiri",
    "(Ekstraksi Ritual)",
    "Lanjutan dari penangkal sebelumnya",
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


def expected_texts(page: int) -> list[str]:
    ar, la, te = LAYERS[page]
    result = ar + la + te + [""]
    if page == 65:
        result += TATACARA
    return result + [""]


def main() -> int:
    doc = Document(TARGET)
    paras = list(doc.paragraphs)
    texts = [p.text for p in paras]
    heads = find_heads(texts)
    els = [p._element for p in paras]

    arab_tpl = deepcopy(els[heads[64] + 1])
    latin_tpl = next(
        deepcopy(els[i])
        for i in range(heads[64], heads[65])
        if texts[i].startswith("Wan nazhratus saw-u")
    )
    terj_tpl = next(
        deepcopy(els[i])
        for i in range(heads[64], heads[65])
        if texts[i].startswith("“… dan pandangan buruk")
    )
    blank_tpl = deepcopy(els[heads[65] - 1])
    if texts[heads[65] - 1].strip() != "":
        raise AssertionError("blank template mismatch")
    templates = {"ar": arab_tpl, "la": latin_tpl, "te": terj_tpl}

    images: dict[int, object] = {}
    for n in (64, 65):
        found = [
            deepcopy(els[i])
            for i in range(heads[n], heads[n + 1])
            if has_drawing_el(els[i])
        ]
        if len(found) != 1:
            raise AssertionError(f"unit {n} image count {len(found)} != 1")
        images[n] = found[0]

    body = els[heads[64]].getparent()
    removed = 0
    inserted = 0
    for n in (64, 65):
        heading_el = els[heads[n]]
        next_heading_el = els[heads[n + 1]]
        node = heading_el.getnext()
        while node is not None and node is not next_heading_el:
            nxt = node.getnext()
            if node.tag == qn("w:p"):
                body.remove(node)
                removed += 1
            node = nxt

        sequence: list[tuple[str, str | None]] = []
        ar, la, te = LAYERS[n]
        sequence += [("ar", x) for x in ar]
        sequence += [("la", x) for x in la]
        sequence += [("te", x) for x in te]
        sequence.append(("img", None))
        if n == 65:
            sequence += [("te", x) for x in TATACARA]

        for kind, text in sequence:
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

    for n in (64, 65):
        got_idx = list(range(oh[n] + 1, oh[n + 1]))
        got = [ot[i] for i in got_idx]
        expected = expected_texts(n)
        if got != expected:
            for a, b in zip(got, expected):
                if a != b:
                    print(f"UNIT {n} MISMATCH:\n got: {a[:140]!r}\n exp: {b[:140]!r}")
            raise AssertionError(f"unit {n} mismatch len {len(got)} vs {len(expected)}")
        ar, la, te = LAYERS[n]
        image_pos = len(ar) + len(la) + len(te)
        image_positions = [
            j for j, i in enumerate(got_idx) if has_drawing_el(out.paragraphs[i]._element)
        ]
        if image_positions != [image_pos]:
            raise AssertionError(f"unit {n} image positions {image_positions}, expected {[image_pos]}")

    revised = "\n".join(ot[oh[64] : oh[66]])
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
    print("H64_65_CLEAN_REVISION_QA_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
