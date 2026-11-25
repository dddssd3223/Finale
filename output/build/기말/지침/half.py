# -*- coding: utf-8 -*-
"""하프 모의고사(오답 재출제) 시험지·정답 PDF: python3 half.py <회차 폴더> <시험지.pdf> <정답및풀이.pdf> "<제목>"
parts/*.py의 ITEMS(1–10)·SITEMS(S1)를 2단 시험지로 찍는다. 선택형 4점, 서답형은 subs 배점."""
import sys, os, re, json, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE)
RD = os.path.abspath(sys.argv[1]); OUT, OUTA, TITLE = os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3]), sys.argv[4]
FONTS = os.path.join(B, 'fonts'); KATEX_CSS = os.path.join(B, 'node_modules', 'katex', 'dist', 'katex.min.css')
ITEMS, SITEMS = {}, {}
for f in sorted(glob.glob(os.path.join(RD, 'parts', '*.py'))):
    if os.path.basename(f).startswith('verify'): continue
    ns = {'_P': os.path.dirname(f)}; exec(open(f).read(), ns); ITEMS.update(ns.get('ITEMS', {})); SITEMS.update(ns.get('SITEMS', {}))
CS = '①②③④⑤'
MAP = json.load(open(os.path.join(RD, 'map.json'))) if os.path.exists(os.path.join(RD, 'map.json')) else {}
fu = lambda n: 'file://' + os.path.join(FONTS, n)
CSS = f"""
@font-face{{font-family:'MJ';src:url('{fu('9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf')}')}}
@font-face{{font-family:'GL';src:url('{fu('gulim_web.ttf')}')}}
@font-face{{font-family:'HB';src:url('{fu('hbatang_web.ttf')}')}}
@font-face{{font-family:'HCRB';src:url('{fu('hcrbatang.ttf')}')}}
@font-face{{font-family:'HYEQ';src:url('{fu('hyhwpeq_web.ttf')}')}}
@page{{size:A4;margin:14mm 13mm 16mm}}
body{{font-family:'HB','MJ',serif;font-size:9.2pt;line-height:1.8;color:#000;word-break:keep-all;margin:0}}
.hd{{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:2pt solid #000;padding-bottom:3pt;margin-bottom:2pt}}
.hd .t{{font-family:'HCRB';font-size:19pt;letter-spacing:-.5pt}} .hd .s{{font-family:'GL';font-size:8.5pt}}
.sub{{display:flex;justify-content:space-between;font-family:'GL';font-size:8.5pt;border-bottom:.6pt solid #000;padding:2pt 0 3pt;margin-bottom:8pt}}
.cols{{column-count:2;column-gap:20pt;column-rule:.6pt solid #000}}
.q{{break-inside:avoid;margin-bottom:26pt;text-align:justify}}
.q .n{{font-family:'HB';font-weight:700;font-style:italic;font-size:10pt;margin-right:3pt}}
.pt{{white-space:nowrap}}
.cond{{border:.6pt solid #000;padding:2pt 6pt;margin:4pt 0;line-height:1.5}}
.bogi{{border:.6pt solid #000;padding:1pt 6pt 4pt;margin:4pt 0}} .bogi .bh{{text-align:center;font-family:'GL'}}
.ch{{display:flex;flex-wrap:wrap;margin-top:3pt}} .ch>span{{width:50pt;white-space:nowrap}} .ch.g>span{{width:76pt}}
.fig{{text-align:center;margin:4pt 0}} .fig img{{width:150pt}}
.katex{{font-size:1em}} .katex-display{{margin:2pt 0 2pt;padding-left:22pt;text-align:left}} .katex-display>.katex{{text-align:left}}
.katex .mfrac>span>span{{text-align:center}}
.sec{{font-family:'HCRB';font-size:12pt;border-top:1.4pt solid #000;padding-top:4pt;margin:6pt 0 6pt;column-span:all}}
.s .subq{{margin:6pt 0 30pt}}
.ans table{{border-collapse:collapse;margin:6pt 0 14pt}} .ans td,.ans th{{border:.6pt solid #000;padding:3pt 10pt;font-family:'GL';text-align:center}}
.sol{{break-inside:avoid;margin-bottom:12pt}} .sol .h{{font-family:'GL';font-weight:700}}
"""

def body_html(it):
    b = re.sub(r'src="(fig_[^"]+)"', lambda m: f'src="file://{RD}/{m.group(1)}"', it['body'])
    if it.get('cond'):
        b += '<div class="cond">' + ''.join(f'<div>{"㈎㈏㈐㈑"["가나다라".index(a)]} {t}</div>' for a, t in it['cond']) + '</div>'
    if it.get('after'): b += it['after']
    if it.get('bogi'):
        b += '<div class="bogi"><div class="bh">&lt;보 기&gt;</div>' + ''.join(f'<div>{k}. {t}</div>' for k, t in it['bogi']) + '</div>'
    return b

def choice_html(ch):
    txt = [x[2:] if str(x).startswith('T:') else '\\(' + str(x) + '\\)' for x in ch]
    g = ' g' if any(str(x).startswith('T:') or len(str(x)) > 8 for x in ch) else ''
    return f'<div class="ch{g}">' + ''.join(f'<span>{CS[i]} {t}</span>' for i, t in enumerate(txt)) + '</div>'

qs = ''.join(f'<div class="q"><span class="n">{n}.</span>{body_html(ITEMS[n])} <span class="pt">[4점]</span>{choice_html(ITEMS[n]["choices"])}</div>' for n in sorted(ITEMS))
sa = ''
for k, it in SITEMS.items():
    subs = ''.join(f'<div class="subq">({i+1}) {t} <span class="pt">[{p.split(",")[0]}]</span></div>' for i, (t, p) in enumerate(it['subs']))
    sa += f'<div class="q s"><span class="n">서답형 {k[1]}.</span>{it["body"]}{subs}</div>'
tot = 4 * len(ITEMS) + sum(int(re.match(r'\d+', p).group()) for it in SITEMS.values() for _, p in it['subs'])
head = (f'<div class="hd"><span class="t">2학년 미적분Ⅰ {TITLE}</span><span class="s">선택형 {len(ITEMS)}문항 · 서답형 {len(SITEMS)}문항 · {tot}점 · 35분</span></div>'
        f'<div class="sub"><span>오답 재출제: 8–10회에서 틀린 문항을 숫자만 바꿔 다시 냄</span><span>이름 ________</span></div>')
doc = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{CSS}</style></head><body>{head}<div class="cols">{qs}<div class="sec">서답형</div>{sa}</div></body></html>'

# 정답 및 풀이
rows = '<tr>' + ''.join(f'<th>{n}</th>' for n in sorted(ITEMS)) + '</tr><tr>' + ''.join(f'<td>{CS[ITEMS[n]["ans"]-1]}</td>' for n in sorted(ITEMS)) + '</tr>'
sans = ''.join(' &nbsp; '.join(a if isinstance(a, list) else it['ans']) for it in SITEMS.values() for a in [it['ans']])
sols = ''.join(f'<div class="sol"><div class="h">{n}번 · 정답 {CS[ITEMS[n]["ans"]-1]} <span style="font-weight:400;color:#555">(원래 {MAP.get(str(n),"")})</span></div>{ITEMS[n].get("sol","")}<div style="color:#555">오답: {ITEMS[n].get("wrong","")}</div></div>' for n in sorted(ITEMS))
sols += ''.join(f'<div class="sol"><div class="h">서답형 {k[1]} <span style="font-weight:400;color:#555">(원래 {MAP.get(k,"")})</span></div>{it.get("sol","")}</div>' for k, it in SITEMS.items())
adoc = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{CSS}</style></head><body>'
        f'<div class="hd"><span class="t">{TITLE} 정답 및 풀이</span><span class="s">원래 문항과 같은 판단을 다시 확인하자</span></div>'
        f'<div class="ans"><table>{rows}</table><div>서답형: {sans}</div></div><div class="cols">{sols}</div></body></html>')
fx = lambda s: re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), s)
for d, o in ((doc, OUT), (adoc, OUTA)):
    src = o + '.src.html'; open(src, 'w').write(fx(d))
    subprocess.run(['node', os.path.join(HERE, 'half.js'), src, o], check=True); os.remove(src)
print(OUT, OUTA)
