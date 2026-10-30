#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the navigable HTML preview for the integrated Al-Qorin master.

Canonical output: al_qorin/PREVIEW_INDEX_AL_QORIN_123.html
Requested alias:  al_qorin/PREVIEW_INDEX_HAL01-65.html (same 123-unit preview;
                  the root file of that name belongs to Anwar and is untouched)
"""
import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
ALQ = ROOT / "al_qorin"
MD = ALQ / "REVISI_AL_QORIN_123.md"
OUT = ALQ / "PREVIEW_INDEX_AL_QORIN_123.html"
ALIAS = ALQ / "PREVIEW_INDEX_HAL01-65.html"

text = MD.read_text(encoding="utf-8")
blocks = []
for block in re.split(r"(?=^## )", text, flags=re.M):
    m = re.match(r"^##\s+(.+)$", block, flags=re.M)
    if m:
        blocks.append((m.group(1).strip(), block))
assert len(blocks) == 123, len(blocks)

articles = []
nav_options = []
total_layers = 0
figures = {}
fig_n = 0

def protect_figures(body):
    global fig_n
    def repl(m):
        global fig_n
        fig_n += 1
        key = f"@@WAFAQFIG{fig_n}@@"
        src, caption = m.group(1), "[Crop" + m.group(2) + "]"
        figures[key] = (
            f'<figure class="wafaq" dir="ltr"><img loading="lazy" src="{html.escape(src, quote=True)}" '
            f'alt="{html.escape(caption, quote=True)}"><figcaption>{html.escape(caption)}</figcaption></figure>'
        )
        return f"\n\n{key}\n\n"
    return re.sub(r"!\[[^\]]*\]\(([^)]+)\)\s*\n\s*\[Crop([^\]]+)\]", repl, body)

for idx, (heading, block) in enumerate(blocks):
    uid = "SAMPUL" if heading == "SAMPUL" else heading.split()[0]
    slug = uid.lower()
    nav_options.append(f'<option value="{idx}">{html.escape(uid)} — {html.escape(heading[:90])}</option>')
    layer_html = []
    for m in re.finditer(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", block, flags=re.M | re.S):
        name, body = m.group(1).strip(), m.group(2)
        total_layers += 1
        body = protect_figures(body)
        content = markdown.markdown(body, extensions=["tables"])
        for key, fig in figures.items():
            content = content.replace(f"<p>{key}</p>", fig).replace(key, fig)
        is_arab = name.startswith("1.")
        cls = "layer arab" if is_arab else "layer"
        direction = "rtl" if is_arab else "ltr"
        layer_html.append(
            f'<section dir="{direction}" class="{cls}"><h3 dir="ltr">{html.escape(name)}</h3>{content}</section>'
        )
    # Conditional layer rule (2026-10-28): SAMPUL 3 layers, M01/M122 4, rest 5.
    expected_layers = {"SAMPUL": 3, "M01": 4, "M122": 4}.get(uid, 5)
    assert len(layer_html) == expected_layers, (uid, len(layer_html), expected_layers)
    hidden = "" if idx == 0 else " hidden"
    articles.append(
        f'<article id="{slug}" data-idx="{idx}"{hidden}><h2 dir="ltr">{html.escape(heading)}</h2>'
        + "".join(layer_html) + "</article>"
    )

assert total_layers == 611, total_layers
assert fig_n == 26, fig_n

out = f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Al-Qorin war Riyadhah — Preview Revisi 123 Artikel</title>
<style>
@font-face {{font-family:'AmiriLocal';src:url('../fonts/Amiri-Regular.ttf') format('truetype');font-weight:400;font-style:normal}}
@font-face {{font-family:'AmiriLocal';src:url('../fonts/Amiri-Bold.ttf') format('truetype');font-weight:700;font-style:normal}}
@font-face {{font-family:'AmiriLocal';src:url('../fonts/Amiri-Italic.ttf') format('truetype');font-weight:400;font-style:italic}}
@font-face {{font-family:'AmiriLocal';src:url('../fonts/Amiri-BoldItalic.ttf') format('truetype');font-weight:700;font-style:italic}}
*{{box-sizing:border-box}}body{{margin:0;background:#f5f5ef;color:#23342c;font:17px/1.8 'AmiriLocal',serif}}
header{{position:sticky;top:0;background:#124735;color:#fff;padding:14px 5%;z-index:3}}h1{{font-size:21px;margin:0 0 8px}}a{{color:inherit}}
nav{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}button,select{{padding:8px;border-radius:5px;border:1px solid #aaa;max-width:min(620px,82vw);font:14px system-ui,sans-serif}}
main{{max-width:980px;margin:28px auto;padding:0 16px}}.notice{{background:#fff8e6;border:1px solid #d8bd72;border-radius:8px;padding:14px 18px;margin:18px 0}}
article h2{{font-size:25px;line-height:1.45}}.layer{{background:#fff;border:1px solid #ddd;padding:24px;margin:20px 0;border-radius:8px;overflow-wrap:break-word}}
.layer h3{{font:600 16px system-ui,sans-serif;color:#176348;border-bottom:1px solid #ddd;padding-bottom:10px}}.layer h4{{font:600 17px system-ui,sans-serif;color:#315c4b;margin:22px 0 6px}}
.arab{{text-align:right;font-size:27px;line-height:2.05}}.arab h3{{text-align:left}}
table{{border-collapse:collapse;margin:20px auto;direction:ltr;max-width:100%}}td,th{{border:1px solid #477359;padding:8px 11px;text-align:center}}
figure.wafaq{{text-align:center;margin:22px auto}}figure.wafaq img{{max-width:100%;max-height:560px;object-fit:contain;background:#fff}}
figure.wafaq figcaption{{font:13px/1.6 system-ui,sans-serif;color:#59665e;margin-top:6px}}code{{font:inherit;color:#125135}}
article[hidden]{{display:none}}footer{{max-width:980px;margin:24px auto;padding:0 16px 32px;color:#59665e;font-size:14px}}
@media print{{header{{display:none}}article[hidden]{{display:block}}article{{break-before:page}}}}
</style>
</head>
<body>
<header>
<h1>Al-Qorin war Riyadhah · Preview Revisi 123 Artikel</h1>
<nav><button type="button" onclick="go(cur-1)">←</button><select id="sel" onchange="go(+this.value)">{''.join(nav_options)}</select><button type="button" onclick="go(cur+1)">→</button><a href="AL_QORIN_REVISI_123_5_LAPIS.docx" download>Unduh DOCX</a><a href="REVISI_AL_QORIN_123.md">Master Markdown</a></nav>
<small>SAMPUL + M01–M122 · 5 lapis per unit (SAMPUL 3 lapis, M01 &amp; M122 4 lapis) · crop wafaq presisi kiriman pengguna.</small>
</header>
<main>
<div class="notice" dir="ltr"><strong>Status:</strong> build terintegrasi 123 unit; 12 unit pilot telah dikurasi manual, penajaman selektif Lapis 4/5 diterapkan pada 12 unit sasaran terverifikasi, dan batch semantik M16–M64, M06–M15/M72–M121, serta batch terakhir M68/M70/M71 telah dikurasi setingkat pilot (catatan dipilih, Khususiyah tingkat frasa, stub/kontradiksi Metode yang terbukti dikoreksi). Seluruh 123 unit kini telah masuk pilot atau salah satu batch semantik. Audit revisi total terjemahan 123 unit telah selesai dan Batch 01 bergaya Anwar (SAMPUL, M01–M05) telah diterapkan pada Lapis 3; batch berikutnya mengikuti antrean audit. Isi tetap dinisbatkan kepada penulis kitab dan disajikan sebagai dokumen terjemahan—bukan anjuran, terapi, atau jaminan hasil.</div>
{''.join(articles)}
</main>
<footer dir="ltr">Pratinjau dibuat dari <code>REVISI_AL_QORIN_123.md</code>. Nama berkas alias <code>PREVIEW_INDEX_HAL01-65.html</code> di folder ini menunjuk isi yang sama; berkas root dengan nama itu adalah pratinjau Anwar dan tidak ditimpa.</footer>
<script>
let cur=0; const arts=[...document.querySelectorAll('article')];
function go(n){{if(n<0||n>=arts.length)return; arts.forEach(x=>x.hidden=true); arts[n].hidden=false; cur=n; document.getElementById('sel').value=n; history.replaceState(null,'','#'+arts[n].id); window.scrollTo(0,0);}}
const start=arts.findIndex(x=>x.id===location.hash.slice(1)); go(start>=0?start:0);
</script>
</body>
</html>
"""

OUT.write_text(out, encoding="utf-8")
ALIAS.write_text(out, encoding="utf-8")
print(f"Preview Al-Qorin: {len(blocks)} units, {total_layers} layers, {fig_n} user-crop figures")
print(OUT)
print(ALIAS)
