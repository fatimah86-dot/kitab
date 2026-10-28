"""Build safe, navigable preview from the master Markdown (no external assets)."""
from pathlib import Path
import re, html, json
import markdown
from build_final_65 import WAFAQ_MAP
ROOT=Path(__file__).resolve().parents[1]
md=(ROOT/'REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.md').read_text()
blocks=re.split(r'(?=^## HALAMAN )',md,flags=re.M)
pages=[]
for b in filter(str.strip,blocks):
    n=int(re.search(r'^## HALAMAN (\d+)',b).group(1))
    title=b.splitlines()[0][3:]
    layers=[]
    for m in re.finditer(r'^### ([^\n]+)\n(.*?)(?=^### |\Z)',b,re.M|re.S):
        name,body=m.groups()
        # Source is trusted local Markdown; isolate direction at layer boundary.
        body=body.replace('\u200e','').replace('\u200f','')
        content=markdown.markdown(body,extensions=['tables'])
        if name=='arab':
            for (pn,idx),(fname,cap,width) in WAFAQ_MAP.items():
                if pn==n:
                    content+=f'<figure dir="ltr"><img loading="lazy" src="rajah_anwar_FINAL_300DPI/{fname}" alt="{html.escape(cap)}"><figcaption>{html.escape(cap)}</figcaption></figure>'
        layers.append(f'<section dir="{"rtl" if name=="arab" else "ltr"}" class="layer {"arab" if name=="arab" else ""}"><h3>{html.escape(name)}</h3>{content}</section>')
    pages.append(f'<article id="hal{n:02}" hidden><h2>{html.escape(title)}</h2>'+''.join(layers)+'</article>')
nav=''.join(f'<option value="{n}">Halaman {n:02}</option>' for n in range(1,66))
out='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Anwar — 5 Lapis Bersih 01–65</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f5ef;color:#23342c;font:17px/1.8 system-ui,sans-serif}header{position:sticky;top:0;background:#124735;color:white;padding:14px 5%;z-index:2}h1{font-size:20px;margin:0}a{color:inherit}nav{display:flex;gap:12px;align-items:center;flex-wrap:wrap}button,select{padding:8px;border-radius:5px;border:1px solid #aaa}main{max-width:950px;margin:32px auto;padding:0 16px}.layer{background:white;border:1px solid #ddd;padding:24px;margin:20px 0;border-radius:8px}.arab{text-align:right;font:25px/2 'Traditional Arabic',serif}.layer h3{font:600 15px system-ui;color:#176348;border-bottom:1px solid #ddd;padding-bottom:12px}table{border-collapse:collapse;margin:20px auto;direction:rtl}td,th{border:1px solid #477359;padding:8px 13px;text-align:center}figure{text-align:center}img{max-width:100%;max-height:450px;object-fit:contain}figcaption{font:13px system-ui;color:#59665e}code{font:inherit;color:#125135}article[hidden]{display:none}@media print{header{display:none}article[hidden]{display:block}article{break-before:page}}
</style><header><h1>Anwārusy-Syaikh al-Basyīr · 5 Lapis Bersih</h1><nav><button onclick="go(cur-1)">←</button><select id="sel" onchange="go(+this.value)">'''+nav+'''</select><button onclick="go(cur+1)">→</button><a href="REVISI_FINAL_5_LAPIS_BERSIH_HAL01-65.docx" download>Unduh Word</a></nav><small>Nomor 01–65 mengikuti halaman naskah sumber, bukan jumlah halaman cetak terjemahan.</small></header><main>'''+''.join(pages)+'''</main><script>let cur=1;function go(n){if(n<1||n>65)return;document.querySelectorAll('article').forEach(x=>x.hidden=true);document.getElementById('hal'+String(n).padStart(2,'0')).hidden=false;cur=n;document.getElementById('sel').value=n;history.replaceState(null,'','#hal'+String(n).padStart(2,'0'));window.scrollTo(0,0)}go(Math.max(1,Math.min(65,Number(location.hash.replace('#hal',''))||1)));</script></html>'''
(ROOT/'PREVIEW_INDEX_HAL01-65.html').write_text(out)
print('Preview: 65 pages, 325 layers, 16 original images')
