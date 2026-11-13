# -*- coding: utf-8 -*-
import os, subprocess, sys, json
import pool
from wbcore import font_css, KATEX_CSS, HERE
from solcss import CSS
CIRC = '①②③④⑤'
EXTRA = """.tag{display:inline-block;border:.6pt solid #000;padding:0 4pt;margin-right:4pt;font-family:'GL';font-size:8pt}
.x{color:#c00;font-weight:700}.o{font-weight:700}
.sum td{font-size:8.6pt}"""
o = json.load(open(os.path.join(HERE, 'order.json')))
MC, SA = o['MC'], o['SA']

def ch(c): return c[2:] if c.startswith('T:') else f'\\({c}\\)'

h = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}{EXTRA}</style></head><body>']
h.append('<h1>2학년 (미적분Ⅰ) 오답노트 해설</h1><div class="dot"></div>'
         '<div class="meta">1~5회 모의 중간고사에서 틀리거나 감점된 문항</div>')
# 요약표
rows = ''
for i, k in enumerate(MC):
    f = pool.INFO[k]
    rows += (f'<tr><td>{i+1}</td><td>{f["n"]}회 {f["q"]}번</td><td>{f["pt"]:.1f}</td>'
             f'<td class="x">{CIRC[f["mine"]-1]}</td><td class="o">{CIRC[f["ans"]-1]}</td><td>−{f["pt"]:.1f}</td></tr>')
for i, k in enumerate(SA):
    f = pool.INFO[k]; got = sum(g for *_, g in f['got']); full = sum(m for _, m, _ in f['got'])
    det = ', '.join(f'{s} {g}/{m}' for s, m, g in f['got'] if g < m)
    rows += (f'<tr><td>서답형 {i+1}</td><td>{f["n"]}회 {f["lab"]}</td><td>{full}</td>'
             f'<td colspan="2">{det}</td><td>−{full-got}</td></tr>')
h.append('<table class="sum"><tr><th>오답노트 번호</th><th>원래 문항</th><th>배점</th><th>내 답</th><th>정답</th><th>감점</th></tr>' + rows + '</table>')
h.append('<h2>선택형</h2>')
for i, k in enumerate(MC):
    f = pool.INFO[k]; sol, so, d0, var, d1, wr = f['D']
    note = f['note'].lstrip('· ')
    h.append(f'<div class="p"><div class="hd">{i+1}번 &nbsp; <span class="tag">{f["n"]}회 {f["q"]}번</span>'
             f'내 답 <span class="x">{CIRC[f["mine"]-1]} {ch(f["ch"][f["mine"]-1])}</span> &nbsp;→&nbsp; 정답 {CIRC[f["ans"]-1]} {ch(f["ch"][f["ans"]-1])} &nbsp; [{f["pt"]:.1f}점]</div>'
             f'<div class="r"><div class="k">풀이</div><div class="v">{sol}</div></div>'
             f'<div class="r"><div class="k">틀린 이유</div><div class="v">{note}</div></div>'
             f'<div class="r"><div class="k">오답 함정</div><div class="v">{wr}</div></div>'
             f'<div class="r"><div class="k">출처·난도</div><div class="v">{so} · 난도 {d1}</div></div></div>')
h.append('<h2>서답형</h2>')
for i, k in enumerate(SA):
    f = pool.INFO[k]; sd = f['sd']
    sc = ' · '.join(f'{s} <span class="{"x" if g < m else ""}">{g}/{m}</span>' for s, m, g in f['got'])
    notes = '<br>'.join(x.lstrip('· ') for x in f['note'])
    h.append(f'<div class="p"><div class="hd">서답형 {i+1} &nbsp; <span class="tag">{f["n"]}회 {f["lab"]}</span>내 점수 {sc}</div>'
             f'<div class="r"><div class="k">정답</div><div class="v">{" / ".join(sd["ans"])}</div></div>'
             f'<div class="r"><div class="k">채점기준 풀이</div><div class="v">{"<br>".join(sd["sol"])}</div></div>'
             f'<div class="r"><div class="k">감점 사유</div><div class="v">{notes}</div></div>'
             f'<div class="r"><div class="k">출처</div><div class="v">{sd["src"]}</div></div></div>')
h.append('</body></html>')
open(os.path.join(HERE, 'osol_src.html'), 'w').write(''.join(h))
subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'osol_src.html', 'osol_tmp.pdf', 'bg'], cwd=HERE, check=True)
os.replace(os.path.join(HERE, 'osol_tmp.pdf'), sys.argv[1])
