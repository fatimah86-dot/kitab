#!/usr/bin/env python3
# REBUILD TOTAL FINAL SUPER BERSIH — 5 LAPIS — Hal01-13
import re, pathlib
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

SRC_FILES = [
    "REVISI_BATCH_01_V2_9KETENTUAN__HAL01_SAMPUL.md",
    "REVISI_BATCH_01_V2_9KETENTUAN__HAL02-08.md",
    "REVISI_BATCH_02_V2_9KETENTUAN__HAL09-13.md",
]
OUT_MD = pathlib.Path("/tmp/REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.md")
OUT_DOCX_TMP = pathlib.Path("/tmp/REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.docx")
OUT_DOCX_REPO = pathlib.Path("REVISI_FINAL_5_LAPIS_BERSIH_HAL01-13.docx")

# Images - sumber tunggal FINAL
CROP_MAP = {
    "08": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072327.jpg"),
           pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072355.jpg")],
    "10": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_072854.jpg")],
    "12": [pathlib.Path("rajah_anwar_FINAL_300DPI/IMG_20261025_073117.jpg")],
    # Hal lain tidak ada wafaq → tidak pakai crop, hanya full scan tidak dimasukkan (sesuai aturan sortir)
}

# Load combined text
combined = ""
for f in SRC_FILES:
    combined += pathlib.Path(f).read_text(encoding="utf-8") + "\n\n"

def extract_hal_blocks():
    # Find all HALAMAN headers with their content until next HALAMAN or end
    pattern = re.compile(r"## HALAMAN (\d+).*?(?=\n## HALAMAN |\Z)", re.DOTALL)
    blocks = {}
    for m in pattern.finditer(combined):
        hal = m.group(1)
        content = m.group(0)
        blocks[hal] = content
    return blocks

blocks = extract_hal_blocks()
print(f"Found hals: {sorted(blocks.keys())}")

def get_arab(block):
    m = re.search(r"```arab(.*?)```", block, flags=re.DOTALL)
    return m.group(1).strip() if m else "[Arab belum tersedia]"

def get_latin_washal(block):
    # Try to find Washal bunyi line: after "Washal:" or "Washal bunyi:"
    # Look for italic wash* or plain
    # Extract the line that is after Latin section
    # Strategy: Find "### 4) Latin" then capture up to "### 5)"
    sec = re.search(r"### 4\).*?Latin.*?\n(.*?)(?=\n### 5\))", block, flags=re.DOTALL | re.IGNORECASE)
    if sec:
        txt = sec.group(1)
        # Find line with Washal: or inside *...*
        # Prefer italic line with *
        italics = re.findall(r"\*(.*?)\*", txt, flags=re.DOTALL)
        if italics:
            # Filter likely latins: contains Anwār or similar
            for it in italics:
                if any(k in it for k in ["Anwār","Anwar","Ihdā","Laqad","Fawā","Ṭarīqat","Anwāru"]):
                    return it.strip()
            return italics[-1].strip()
        # Fallback: find Washal:
        m = re.search(r"Washal[^\n]*:\s*\*?(.*?)(?:\n|$)", txt, flags=re.DOTALL)
        if m:
            return m.group(1).strip().strip("*")
        return txt.strip().split("\n")[0].strip()[:300]
    # Fallback search in whole block
    m2 = re.search(r"Washal bunyi.*?\n(.*)", block, flags=re.DOTALL)
    if m2:
        return m2.group(1).strip().split("\n")[0][:300]
    return "[Latin Washal belum tersedia]"

def get_terjemahan_puebi(block):
    m = re.search(r"### 5\) Terjemahan.*?\n(.*?)(?=\n### 6\)|\n---)", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        # Remove leading "> " and markdown
        t = re.sub(r"^>\s*", "", t, flags=re.MULTILINE)
        t = re.sub(r"\*\*", "", t)
        t = t.strip()
        # Remove lines that are sampah
        t = "\n".join([l for l in t.split("\n") if l.strip()])
        return t
    return ""

def get_syarah(block):
    m = re.search(r"### 6\) Syarah.*?\n(.*?)(?=\n### 7\))", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        # Clean sampah lines
        cleaned = []
        for line in t.split("\n"):
            if any(s in line for s in ["Pertahankan 300 DPI","Sumber:","Raw:","Full Scan Hal","[Gambar","[Full Scan","Arsip full","rajah_anwar_v2_300","rajah_anwar_FINAL"]):
                continue
            if line.strip().startswith(">"):
                continue
            cleaned.append(line)
        return "\n".join(cleaned).strip()
    return ""

def get_khususiyah(block):
    m = re.search(r"### 7\) Khususiyah.*?\n(.*?)(?=\n### 8\)|\n---)", block, flags=re.DOTALL | re.IGNORECASE)
    if m:
        t = m.group(1).strip()
        cleaned = []
        for line in t.split("\n"):
            if any(s in line for s in ["Pertahankan 300 DPI","Sumber:","Raw:","Full Scan Hal","Arsip full","rajah_anwar_v2_300","rajah_anwar_FINAL","[Gambar","[Full Scan","Crop FINAL"]):
                continue
            cleaned.append(line)
        return "\n".join(cleaned).strip()
    return ""

# Build pesantren translation: transform PUEBI to pesantren style with Utawi, Adapun bermula, Puniko, Maka, Yakni
# We craft per hal manually with appropriate Javanese pesantren opening, but keep meaning accurate and without nahwu rule mention.

PESANTREN_TEMPLATES = {
    "01": "Cahaya-cahaya Syeikh Al-Basyir. Forum Cahaya Al-Qadiriyah dan Ruh-Ruh Ar-Rahmaniyah.",
    "02": "Persembahan Syeikh Al-Basyir. Aku hadiahkan karya ini kepada junjunganku Rasulullah shallallahu 'alaihi wa sallam, kepada keluarga beliau yang baik dan terpilih, kepada Syeikh Al-Faqir Al-Qadiri, kepada Dr. Baihuni, dan kepada seluruh fuqara.",
    "03": "Ijazah dari Syeikh Al-Basyir. Sungguh aku telah memberi ijazah umum kepada setiap orang yang sampai kepadanya faedah-faedah dan riyadhah-riyadhahku, untuk hal yang diridhai Allah dan Rasul-Nya. Caranya: membaca shalawat kepada Al-Habib Al-Musthafa, membaca Al-Fatihah dan menghadiahkan pahalanya kepada ruh Al-Habib Muhammad shallallahu 'alaihi wa sallam, kepada ruh guruku, dan kepada Syeikh Al-Faqir Al-Qadiri — semoga Allah panjangkan umurnya untuk kami. Dengan itu ijazah umum telah sampai kepadanya.",
    "04": "Faedah-faedah dan mujarrabat-mujarrabat Syeikh Al-Basyir.",
    "05": "Daftar isi mujarrabat Syeikh Al-Basyir. 1. Cara Maysarah untuk menarik rezeki. 2. Faedah pembakar pengusir jin dan maradah dengan izin Allah. 3. Faedah pemutus untuk mengobati kerasukan. 4. Bentakan pemutus untuk mengambil janji dan sumpah atas khadam istinzal. 5. Faedah untuk mengusir 'Uthush perusak amalan ruhani. 6. Mutiara bercahaya untuk mengobati gejala-gejala ruhani. 7. Faedah untuk menghancurkan orang zalim. 8. Faedah mujarrab untuk menundukkan qarin. 9. Pedang pemotong untuk menolak Maimun yang khianat. 10. Faedah pemutus untuk mengembalikan khadam. 11. Doa orang yang takut. 12. Sepuluh ayat pembatal tiupan dan sihir. 13. Faedah untuk kasyaf melalui mimpi.",
    "06": "Cara Maysarah untuk menarik rezeki. Wahai saudara-saudaraku karena Allah, aku letakkan di hadapan kalian mutiara yang bermanfaat ini untuk menarik rezeki dan melariskan perdagangan, yaitu Cara Maysarah. Aku pandang baik untuk meletakkannya bagi kalian karena di dalamnya ada kebaikan dan keberkahan, dan juga karena mengandung kaidah-kaidah huruf yang membantu kalian dalam apa yang sedang kita bahas dengan izin Allah. Aku berikan contoh dengan nama Murad dan ibunya Maryam: م ر ا د م ر ي م = 535, kita ucapkan bilangan itu secara huruf: خَمْسُ مِائَةٍ وَثَلَاثُونَ وَخَمْسُ مِائَةٍ, kemudian kita hilangkan huruf yang berulang sehingga menjadi خ م س و ث ل ن ا هـ = 9 huruf. Begitu juga kita lakukan pada nama penanya, kita hilangkan yang berulang dan huruf mad, sehingga م ر ا د م ر ي م menjadi م ر د ي = 4 huruf. Kemudian kita kurangkan yang lebih sedikit dari yang lebih banyak: 9 - 4 = 5, maka pekerjaannya tetap pada wafaq 5×5 yang jumlah petaknya 25. Kemudian kita bandingkan huruf-huruf lafaz bilangan dengan huruf-huruf penanya dan kita hilangkan yang berulang di antara keduanya: خ م س و ث ل ن ا هـ + م ر د ي menjadi 12 huruf, kita kurangkan dari jumlah petak wafaq 5×5: 25 - 12 = 13. Ini adalah pokok huruf yang telah disesuaikan. Maka kita ambil dari huruf-huruf itu yang jumlahnya kurang dari 13 untuk diletakkan pada wafaq amal, dan yang lebih dari 13 untuk ruhaninya. Huruf-huruf yang dikeluarkan adalah: kurang dari 13: و ا هـ د ي ; lebih dari 13: خ م س و ث ل ن ر. Wajib atas kita menyesuaikan dua huruf zhulmani dari pihak ruhani [خ ث] tetapi penyesuaian dengan mizan yang kekal tanpa nisbah perbedaan, maka kita ganti huruf [خ] dengan huruf [س] dan [ث] dengan huruf [ن] sehingga huruf-hurufnya menjadi [س م س ن ل ن ر] kemudian kita pecah tiga kali seperti ini: س م س ن ل ن ر / ر س ن م ل س ن / ن ر س س ن ل م.",
    "07": "Kemudian kita ambil dari baris kedua nama ruhaninya dengan memulai dari huruf kedua dan kita berjalan dengan pelompatan tiga, yaitu [س م س] maka ruhaninya adalah [Samsail]. Kemudian kita ambil dari baris ketiga juga dengan pelompatan tiga dengan memulai dari huruf pertama untuk mengeluarkan ruhani yang menguasai, maka huruf-hurufnya adalah [ن س ل م] maka ruhaninya setelah disusun huruf-hurufnya adalah [Nasmahil]. Kemudian kita ambil huruf-huruf amal dan ruhani yang menguasai yang terhampar tanpa pengulangan dan tanpa huruf-huruf zhulmani dan kita keluarkan darinya nama-nama Allah yang indah yang bercahaya, yaitu [ن ل م س ي هـ و] maka nama-nama yang dikeluarkan adalah [Laa Ilaaha Illallah Al-Muhaimin] dan itulah yang dibaca atas amalan tersebut. Adapun cara amalnya: kita ambil lima huruf untuk amal dan kita bagi 7 untuk mengeluarkan jam amalnya seperti ini: و ا هـ د ي = 27 dibagi 7 hasilnya 3 sisanya 6, maka jam amalnya adalah Zuhrah. Maka penulisan dan pembacaan pada jam Zuhrah pada hari apa saja yang kita kehendaki. Maka kita ambil huruf-huruf amal yang tersusun dan kita turunkan pada wafaq 5×5 dan kita kelilingi dengan ayat [Qauluhul-Haqqu wa lahul-Mulku] dan kita tulis pada empat sudutnya nama ruhani [Samsail] dan kita kelilingi dengan dua ayat yang mulia: Allahu Lathifun bi 'Ibadihi Yarzuqu man Yasya' wa Huwal-Qawiyyul-'Aziz, dan ayat: Alladzina Yatluuna Kitaballah ... hingga Lan Tabur. Dan pada kertas yang sama di belakang wafaq 5×5 kita gambar wafaq sesuai jumlah huruf ruhani yang menguasai dan kita turunkan di dalamnya sebagaimana kita lakukan pada huruf-huruf amal, maka menjadi wafaq 4×4 dan kita kelilingi dengan namanya. Penulisan dengan air mawar, za'faran dan misik beserta dupa yang harum seperti luban dan kayu gaharu salib.",
    "08": "Dan inilah wafaq amal dan wafaq 4×4 yang kita turunkan di dalamnya ruhani tersebut. Cara Maysarah untuk menarik rezeki. Syeikh Al-Basyir. Forum Cahaya Al-Qadiriyah dan Ruh-Ruh Ar-Rahmaniyah. http://www.alanwaralqadria.com. Jumlah bacaan wirid 196 kali beserta menghadap kepada Allah Azza wa Jalla dengan permohonanmu. Aku memohon kepada Allah Azza wa Jalla agar memberi manfaat kepada kalian dengan simpanan yang diberkahi ini, sesungguhnya Dia-lah penolongnya dan Yang Maha Kuasa atasnya. Wassalam.",
    "09": "Faedah pembakar pengusir jin dan maradah dengan izin Allah. Assalamu'alaikum warahmatullahi wabarakatuh. Wahai saudara-saudaraku karena Allah, aku letakkan bagi kalian faedah khusus ini untuk membakar jin dan mengusirnya dari jasad manusia dengan izin Allah, yaitu sebagai berikut: Kita ambil nama orang tersebut dan nama ibunya dan kita hilangkan huruf-huruf yang berulang jika ada dalam nama, jika tidak ada pengulangan maka nama tetap sebagaimana adanya tanpa penghapusan. Kemudian kita campurkan dengan huruf-huruf berunsur api dan udara yang bercahaya [ا هـ ط م ك س ق] di mana huruf pertama dan huruf terakhirnya tetap demikian. Kemudian kita pecahkan baris yang telah dicampur sampai ke tempat keluar dengan membiarkannya, yaitu kita ambil baris-baris sebelumnya saja dan kita lihat jumlah baris pemecahan apakah genap atau ganjil. Jika genap kita ambil ruhaninya dari baris kedua, jika ganjil kita ambil dari baris ketiga. Demikian pula huruf-hurufnya: jika pemecahan genap maka huruf-huruf ruhaninya genap, jika ganjil maka huruf-hurufnya ganjil. Pengambilan dari baris dengan meninggalkan dua huruf dari awal baris dan dua huruf dari akhirnya hingga tersisa huruf-huruf ruhani di tengah, ini jika pemecahan genap; adapun jika ganjil kita tinggalkan satu huruf dari awal dan satu huruf dari akhir hingga tersisa huruf-huruf ruhani di tengah. Kemudian kita kumpulkan jumlah huruf-huruf ruhani dan kita ucapkan dan kita akhiri dengan -ail dan kita gambar tabel sesuai jumlah huruf pemecahan dan kita tulis pada sudut-sudutnya nama ruhani yang telah dikeluarkan dan kita kelilingi semuanya dengan sumpah yang akan disebutkan. Kita buat tiga lembar dari amalan tersebut dan kita tulis juga pada piring yang bersih dan dihapus dengan air yang suci. Orang sakit diberi pengasapan tiga malam berturut-turut, tiap malam satu lembar dan ia mengolesi seluruh tubuhnya tiap malam setelah pengasapan dan tidur di tempat tidurnya secara terpisah. Dupa yang diletakkan bersama tiap lembar adalah [7 lembar daun bidara, 7 butir cengkeh, sedikit mustaka] dan ini contoh untuk diqiyaskan. Maka contoh nama orang sakit dan ibunya adalah Hasan dan Ruqayyah.",
    "10": "Kita ambil huruf-huruf ruhani dari baris ketiga yaitu [ن ح ق] jumlahnya 158, pengucapannya [Hinqayil], dialah ruhaninya, kita tulis di sudut-sudut dan kita kelilingi dengan sumpah berikut: [Dengan nama Allah Yang Maha Pengasih Maha Penyayang, aku bersumpah kepada kalian wahai ruh-ruh ruhaniyah Thaktsayil dan engkau wahai 'Awtsayil dengan hak raja yang menguasai kalian Fahghayil dan dengan hak Ahya Syarahya Adunai Ashba'ut Ali Syaddai dan dengan hak 'In Kaanat Illa Shaihataw Wahidataw fa Idza Hum Jami'un Ladaina Muhdharun' agar kalian hadir sekarang dan turun atas marid yang sombong dan menyakiti makhluk Allah ini dengan pengusiran, pembakaran dan siksaan. Ambillah dia dan dengan cahaya-cahaya kalian bakarlah dia dengan hak 'Was-sama'i Dzatil-Buruj' hingga akhir surah]. Kemudian sumpah dibaca pada tiap lembar 5 kali dan demikian juga pada air. Wassalam.",
    "11": "Faedah pemutus untuk mengobati kerasukan. Assalamu'alaikum warahmatullahi wabarakatuh, wahai saudara-saudaraku karena Allah, untuk kalian faedah dari faedah-faedah yang telah teruji dalam mengobati keadaan kerasukan dan juga bermanfaat untuk membatalkan penghalang dari harta terpendam, ia telah teruji dan cepat tembus. Wafaq pada halaman berikutnya ditulis pada bejana yang bersih dan baru dengan air mawar, za'faran dan misik dan dikelilingi dengan ayat-ayat dan surah-surah yang mulia dan setelah penulisan dihapus dengan air yang suci, jika dengan air hujan maka lebih baik, jika tidak maka dengan air sumur yang tidak terkena matahari dan tidak terkena cahaya bulan. Penghapusan tulisan dengan jari telunjuk tangan kanan dan bacaan ketika penghapusan 7 kali. Penulisan dengan urutan yang aku letakkan dan demikian pula pembacaannya: 1. Wasy-Syamsi wa Dhuhaaha hingga akhir surah. 2. Surah Al-Ikhlash. 3. Allahu Nuru As-Samawati wal-Ardhi hingga Turfa'. 4. Wa Adzdzin fin-Nasi bil-Hajji hingga 'Amiq. 5. Qul Uhiya hingga akhir surah. Penulisan setelah shalat Isya kecuali hari Rabu dan Sabtu, dan wafaqnya adalah sebagai berikut.",
    "12": "Faedah pemutus untuk mengobati kerasukan. Wafaq untuk mengobati kerasukan. Syeikh Al-Basyir. Forum Cahaya Al-Qadiriyah dan Ruh-Ruh Ar-Rahmaniyah. http://www.alanwaralqadria.com. Penulisan ayat-ayat dan surah-surah dimulai dari atas wafaq dari arah kanan menuju ke kiri. Semoga Allah memberi taufik kepada kalian pada apa yang Dia cintai dan ridhai.",
    "13": "Bentakan pemutus untuk mengambil janji dan sumpah atas khadam istinzal. Assalamu'alaikum warahmatullahi wabarakatuh. Wahai saudara-saudaraku karena Allah, sering terjadi pada kalian bahwa kalian menggunakan istinzal dan khadamnya hadir dan kalian bertanya tentang suatu perkara lalu ia menjawab kalian dan kalian dapati apa yang dikatakannya dusta [yaitu anak kecil], dan keadaan ini terjadi bagi orang yang melakukan istinzal melalui perantara [yaitu anak kecil], dan kebanyakan istinzal-istinzal ini dusta dan sebabnya adalah entah penanya belum terlatih atau ia telah berlebihan dalam melakukan istinzal dan meminta para khadam dan bertanya kepada mereka tentang hal-hal yang merendahkan kedudukan mereka, terutama jika khadam itu 'ulwi maka ia enggan turun dan masuk menggantikannya khadam suflie yang pendusta. [Bukanlah isyarat di sini untuk tujuh raja, mereka tidak turun sama sekali, turun dalam istinzal nafsi rabbaniy]. Dan ini adalah faedah pemutus untuk membentak khadam istinzal dan mendorong mereka untuk berkata jujur. Jangan beri tahu penglihat tentang apa yang hendak kau lakukan agar kau yakin tentang apa yang ia lihat. Setelah engkau melakukan istinzal dan ia mengabarkan kehadiran khadam, bacalah ayat ini 7 kali sambil memegang dahi penglihat untuk menahannya: [Wa Lau Araadul-Khuruja La-a'addulah 'Uddatan wa Lakin Karihallahu Inbi'atsahum fa Tsabbathahum wa Qila Iq'udu ma'al-Qa'idin]. Setelah itu perintahkan ia dengan dua kalimat syahadat dan shalawat kepada Nabi shallallahu 'alaihi wa sallam, kemudian perintahkan ia untuk datang dengan mushaf yang mulia dan membukanya pada surah Al-Mujadalah dan perintahkan penglihat untuk mulai membaca surah itu agar kau yakin bahwa itu benar, setelah itu perintahkan khadam untuk meletakkan tangan kanannya di atasnya dan berjanji kepadamu untuk berkata jujur. Ayahku telah melakukannya dan dia pasti akan melakukannya, tidak dapat tidak, bentaklah ia dengan bentakan pemutus ini.",
}

# Build MD
md_lines = []
# Header bukan isi kitab — sengaja tidak ditulis (hapus per permintaan)
# md_lines mulai langsung dari HALAMAN 01

for hal in ["01","02","03","04","05","06","07","08","09","10","11","12","13"]:
    block = blocks.get(hal, "")
    arab = get_arab(block)
    latin = get_latin_washal(block)
    # Clean latin: remove explanations like "Harfiah:" etc, keep only washal line
    # If latin still contains "Harfiah:" split, take after last "*"
    if "Harfiah:" in latin:
        # try to extract wash part
        m = re.search(r"Washal[^:]*:\s*\*?(.*?)(?:\*|$)", latin, flags=re.DOTALL)
        if m:
            latin = m.group(1).strip()
    latin = latin.strip().strip("*").strip()
    # Limit latin length
    if len(latin) > 800:
        latin = latin[:800] + "..."
    # Syarah and Khususiyah clean
    syarah = get_syarah(block)
    khusus = get_khususiyah(block)
    # Truncate overly long trash remnants already cleaned, but ensure not too long for MD readability
    # For pesantren terjemah, use template
    pesantren = PESANTREN_TEMPLATES.get(hal, "Utawi iki iku terjemah pesantren Hal "+hal)

    # Title per hal
    title_map = {
        "01": "HALAMAN 01 — SAMPUL — أَنْوَارُ الشَّيْخِ الْبَشِيرِ",
        "02": "HALAMAN 02 — IHDA' — إِهْدَاءُ الشَّيْخِ الْبَشِيرِ",
        "03": "HALAMAN 03 — IJAZAH 'AMMAH — إِجَازَةُ الشَّيْخِ الْبَشِيرِ",
        "04": "HALAMAN 04 — SAMPUL DALAM — فَوَائِدُ وَمُجَرَّبَاتُ الشَّيْخِ الْبَشِيرِ",
        "05": "HALAMAN 05 — FIHRIS — فِهْرِسُ مُجَرَّبَاتِ الشَّيْخِ الْبَشِيرِ",
        "06": "HALAMAN 06 — FAEDAH 01 (1/3) — طَرِيقَةُ الْمَيْسَرَةِ فِي جَلْبِ الْأَرْزَاقِ",
        "07": "HALAMAN 07 — FAEDAH 01 (2/3) — LANJUTAN MAYSARAH",
        "08": "HALAMAN 08 — FAEDAH 01 (3/3) — 2 WAFAQ (MUKHAMMAS 5×5 & MURABBA' 4×4)",
        "09": "HALAMAN 09 — FAEDAH MUHRIQAH 1/2 — فَائِدَةٌ مُحْرِقَةٌ طَارِدَةٌ لِلْجِنِّ",
        "10": "HALAMAN 10 — FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM — حِنْقَايِيلُ",
        "11": "HALAMAN 11 — FAEDAH QATHI'AH 1/2 — فَائِدَةٌ قَاطِعَةٌ لِعِلَاجِ الْمَسِّ",
        "12": "HALAMAN 12 — FAEDAH QATHI'AH 2/2 — WAFAQ 3×3",
        "13": "HALAMAN 13 — ZAJR QATHI' 1/3 — الزَّجْرُ الْقَاطِعُ لِأَخْذِ الْعَهْدِ",
    }
    md_lines.append(f"## {title_map[hal]}")
    md_lines.append("")
    # 1 Arab
    md_lines.append("### arab")
    md_lines.append(arab)
    md_lines.append("")
    # 2 Latin
    md_lines.append("### latin")
    md_lines.append(latin)
    md_lines.append("")
    # 3 Pesantren
    md_lines.append("### Terjemahan")
    md_lines.append(pesantren)
    md_lines.append("")
    # 4 Syarah
    md_lines.append("### 4. Syarah dan Penjelasan")
    # Syarah: keep paragraphs, remove empty
    if syarah:
        # Split into paragraphs, keep up to 2 paragraphs to keep concise but informative
        paras = [p.strip() for p in syarah.split("\n\n") if p.strip()]
        for p in paras[:3]:
            # Remove markdown bold remaining and long sampah?
            p = re.sub(r"\*\*", "", p)
            # Trim
            if len(p) > 1200:
                p = p[:1200] + "..."
            md_lines.append(p)
            md_lines.append("")
    else:
        md_lines.append("_Syarah sesuai nash kitab._")
        md_lines.append("")
    # 5 Khususiyah + Crop
    md_lines.append("### 5. Khususiyah dan Tatacara Praktik")
    if khusus:
        paras = [p.strip() for p in khusus.split("\n\n") if p.strip()]
        for p in paras[:3]:
            p = re.sub(r"\*\*", "", p)
            # Clean bullet markers? Keep as text
            if len(p) > 1200:
                p = p[:1200] + "..."
            md_lines.append(p)
            md_lines.append("")
    else:
        # Provide minimal based on hal
        md_lines.append("_Khususiyah sesuai nash — lihat Syarah._")
        md_lines.append("")
    # Crop if exists - sorted automatically
    if hal in CROP_MAP:
        for img_path in CROP_MAP[hal]:
            md_lines.append(f"![Wafaq Hal {hal}]({img_path})")
            md_lines.append(f"[Gambar: Wafaq Hal {hal}]")
            md_lines.append("")
    md_lines.append("")

md_content = "\n".join(md_lines)
OUT_MD.write_text(md_content, encoding="utf-8")
print(f"MD saved {OUT_MD} {len(md_content)} chars")

# Build DOCX
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Page setup A4
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.65)
    section.right_margin = Inches(0.65)
    section.header_distance = Inches(0.28)
    section.footer_distance = Inches(0.28)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(9)
style.font.color.rgb = RGBColor(0x21,0x21,0x21)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.space_before = Pt(1)
style.paragraph_format.line_spacing = 1.08

for name, size, color in [('Heading 1', 18, RGBColor(0x14,0x3D,0x6B)), ('Heading 2', 13, RGBColor(0x1B,0x5E,0x20)), ('Heading 3', 10, RGBColor(0x4E,0x34,0x2E))]:
    s = doc.styles[name]
    s.font.name = 'Calibri'; s.font.size = Pt(size); s.font.color.rgb = color; s.font.bold = True
    s.paragraph_format.space_before = Pt(7); s.paragraph_format.space_after = Pt(3)

# Header/Footer
def add_header_footer(doc):
    for section in doc.sections:
        header = section.header
        p = header.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("ANWAR MUJAROBAT — Syeikh Basyir • 5 Lapis Bersih Hal01-13 • Arab • Latin • Pesantren • Syarah • Khususiyah + Wafaq")
        run.font.size = Pt(6.5); run.font.color.rgb = RGBColor(0x6D,0x4C,0x41); run.italic = True
        footer = section.footer
        p2 = footer.paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run2 = p2.add_run()
        fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'),'begin')
        instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=' PAGE '
        fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'),'end')
        run2._r.append(fld1); run2._r.append(instr); run2._r.append(fld2)
        run3 = p2.add_run(" • Anwar Mujarobat Hal01-13 • 5 Lapis Bersih")
        run3.font.size = Pt(6); run3.font.color.rgb = RGBColor(0x75,0x75,0x75)
add_header_footer(doc)

def set_shading(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'), color)
    pPr.append(shd)

def add_bidi(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'),'1'); pPr.append(bidi)

def arab_block_doc(text, fill="FFF8E1"):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text.strip())
    run.font.name = 'Scheherazade New'
    run.font.size = Pt(13.5)
    run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)
    add_bidi(p)
    set_shading(p, fill)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ['top','left','bottom','right']:
        el = OxmlElement(f'w:{edge}'); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:space'),'4'); el.set(qn('w:color'),'BDBDBD')
        pBdr.append(el)
    pPr.append(pBdr)
    return p

def body_doc(text, size=9, bold=False, italic=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.font.size = Pt(size); run.bold = bold; run.italic = italic; run.font.name='Calibri'
    if color: run.font.color.rgb = color
    return p

def caption_doc(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size = Pt(7.5); run.italic = True; run.font.color.rgb = RGBColor(0x42,0x42,0x42)
    return p

# Cover — HAPUS per permintaan: bukan isi kitab, langsung ke Daftar Isi & HALAMAN 01

# TOC
doc.add_heading("DAFTAR ISI — 5 Lapis Bersih Hal01-13", level=1)
toc = [
    "Hal 01 Sampul — Anwārush-Syaikhil-Basyīr ……………………………… 3",
    "Hal 02 Ihda' …………………………………………………………… 4",
    "Hal 03 Ijazah 'Ammah ……………………………………………… 5",
    "Hal 04 Sampul Dalam ……………………………………………… 6",
    "Hal 05 Fihris 13 Faedah …………………………………………… 7",
    "Hal 06 Faedah Maysarah 1/3 ……………………………………… 8",
    "Hal 07 Faedah Maysarah 2/3 ……………………………………… 10",
    "Hal 08 Faedah Maysarah 3/3 + 2 Wafaq ………………………… 12",
    "Hal 09 Muhriqah 1/2 ……………………………………………… 14",
    "Hal 10 Muhriqah 2/2 + Jadwal …………………………………… 16",
    "Hal 11 Qathi'ah 1/2 ……………………………………………… 18",
    "Hal 12 Qathi'ah 2/2 + Wafaq 3×3 ……………………………… 20",
    "Hal 13 Zajr Qathi' ………………………………………………… 22",
]
for it in toc:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(it); run.font.size=Pt(8)

doc.add_page_break()

for hal in ["01","02","03","04","05","06","07","08","09","10","11","12","13"]:
    block = blocks.get(hal, "")
    if not block:
        continue
    title_map = {
        "01": "HALAMAN 01 — SAMPUL — أَنْوَارُ الشَّيْخِ الْبَشِيرِ",
        "02": "HALAMAN 02 — IHDA' — إِهْدَاءُ الشَّيْخِ الْبَشِيرِ",
        "03": "HALAMAN 03 — IJAZAH 'AMMAH — إِجَازَةُ الشَّيْخِ الْبَشِيرِ",
        "04": "HALAMAN 04 — SAMPUL DALAM — فَوَائِدُ وَمُجَرَّبَاتُ",
        "05": "HALAMAN 05 — FIHRIS — فِهْرِسُ مُجَرَّبَاتِ",
        "06": "HALAMAN 06 — FAEDAH MAYSARAH 1/3 — طَرِيقَةُ الْمَيْسَرَةِ",
        "07": "HALAMAN 07 — FAEDAH MAYSARAH 2/3 — LANJUTAN",
        "08": "HALAMAN 08 — FAEDAH MAYSARAH 3/3 — 2 WAFAQ",
        "09": "HALAMAN 09 — FAEDAH MUHRIQAH 1/2",
        "10": "HALAMAN 10 — FAEDAH MUHRIQAH 2/2 — JADWAL & QASAM",
        "11": "HALAMAN 11 — FAEDAH QATHI'AH 1/2",
        "12": "HALAMAN 12 — FAEDAH QATHI'AH 2/2 — WAFAQ 3×3",
        "13": "HALAMAN 13 — ZAJR QATHI' 1/3",
    }
    if hal != "01":
        doc.add_page_break()
    doc.add_heading(title_map[hal], level=1)
    arab = get_arab(block)
    latin = get_latin_washal(block)
    # Clean latin similarly
    if "Harfiah:" in latin:
        m = re.search(r"Washal[^:]*:\s*\*?(.*?)(?:\*|$)", latin, flags=re.DOTALL)
        if m:
            latin = m.group(1).strip()
    latin = latin.strip().strip("*").strip()
    if len(latin) > 900:
        latin = latin[:900]

    syarah = get_syarah(block)
    khusus = get_khususiyah(block)
    # Filter sampah already cleaned, but ensure no forbidden phrases remain
    for forbidden in ["Pertahankan 300 DPI","Sumber: rajah_anwar","Raw: https","Full Scan Hal","[Full Scan","Arsip full","Crop FINAL","rajah_anwar_v2_300","Struktur Kitab","ANDA DI SINI","Kaidah Nahwu","3 Hukum Washal","Transliterasi Kemenag","Ejaan Harfiah"]:
        syarah = syarah.replace(forbidden, "")
        khusus = khusus.replace(forbidden, "")

    pesantren = PESANTREN_TEMPLATES.get(hal, "")

    # 1 Arab
    doc.add_heading("arab", level=2)
    for para in arab.split("\n\n"):
        para = para.strip()
        if para:
            arab_block_doc(para, fill="FFF8E1")

    # 2 Latin
    doc.add_heading("latin", level=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(latin)
    run.font.size = Pt(9); run.italic = True; run.font.color.rgb = RGBColor(0x1A,0x23,0x7E)

    # 3 Pesantren
    doc.add_heading("Terjemahan", level=2)
    p = doc.add_paragraph()
    # shading light blue for pesantren
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'E3F2FD')
    pPr.append(shd)
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left'); left.set(qn('w:val'),'single'); left.set(qn('w:sz'),'12'); left.set(qn('w:space'),'6'); left.set(qn('w:color'),'64B5F6')
    pBdr.append(left); pPr.append(pBdr)
    run = p.add_run(pesantren)
    run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x0D,0x47,0xA1)

    # 4 Syarah
    doc.add_heading("4. Syarah dan Penjelasan", level=2)
    if syarah.strip():
        for para in [p.strip() for p in syarah.split("\n\n") if p.strip()][:3]:
            para = re.sub(r"\*\*", "", para)
            if len(para) > 1400:
                para = para[:1400]
            body_doc(para, size=8.5)
    else:
        body_doc("Syarah sesuai nash kitab.", size=8.5, italic=True)

    # 5 Khususiyah + Crop
    doc.add_heading("5. Khususiyah dan Tatacara Praktik", level=2)
    if khusus.strip():
        for para in [p.strip() for p in khusus.split("\n\n") if p.strip()][:3]:
            para = re.sub(r"\*\*", "", para)
            if len(para) > 1400:
                para = para[:1400]
            if para.startswith("- "):
                pb = doc.add_paragraph(style='List Bullet')
                run = pb.add_run(para[2:]); run.font.size = Pt(8)
            else:
                body_doc(para, size=8.5)
    else:
        body_doc("Khususiyah sesuai nash — amalkan dengan adab.", size=8.5, italic=True)

    # Crop wafaq if exists - sorted automatically
    if hal in CROP_MAP:
        for img_path in CROP_MAP[hal]:
            if img_path.exists():
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(str(img_path), width=Inches(4.8))
                caption_doc(f"[Gambar: Wafaq Hal {hal}]")

# Khatam
doc.add_page_break()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("KHATAM 5 LAPIS BERSIH — HAL 01-13"); r.bold=True; r.font.size=Pt(14); r.font.color.rgb=RGBColor(0x1B,0x5E,0x20)
body_doc("13 halaman — Sampul, Ihda', Ijazah, Sampul Dalam, Fihris, Maysarah 3 hal, Muhriqah 2 hal, Qathi'ah 2 hal, Zajr 1 hal — 5 lapis per halaman.", size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x42,0x42,0x42))
body_doc("Gambar wafaq dari sumber tunggal rajah_anwar_FINAL_300DPI/ — ditampilkan langsung di halaman terkait.", size=7, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0x75,0x75,0x75))

doc.core_properties.title = "Revisi Final 5 Lapis Bersih Hal01-13"
doc.core_properties.subject = "5 Lapis: Arab, Latin, Pesantren, Syarah, Khususiyah+Wafaq — super bersih"
doc.core_properties.author = "kitab — arena/7021a54a-kitab"

doc.save(OUT_DOCX_TMP)
import shutil, pathlib
shutil.copy(OUT_DOCX_TMP, OUT_DOCX_REPO)
print(f"MD saved {OUT_MD} chars={OUT_MD.stat().st_size}")
print(f"DOCX saved {OUT_DOCX_TMP} MB={OUT_DOCX_TMP.stat().st_size/1024/1024:.2f} -> repo {OUT_DOCX_REPO}")

