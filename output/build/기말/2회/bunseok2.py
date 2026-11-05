# -*- coding: utf-8 -*-
"""분석서2: 복습형 회차의 분석집 문항이 분석집의 판정·TIP·변형 방향·예상 함정을 실제로 복습시키는지 대조표.
사용: python3 bunseok2.py <coverage.json> <출력.pdf>
coverage.json은 출제에 참여하지 않은 검토자가 문항을 직접 풀고 판정한 기록(review/bunseok_coverage.json)."""
import os, sys, json, html, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
import content3 as C
A = json.load(open('/home/user/Finale/output/build/기말/지침/analysis.json'))
E = lambda s: html.escape(str(s), quote=False).replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;')
MK = {'O': '<b class="o">O</b>', '△': '<b class="t">△</b>', 'X': '<b class="x">X</b>'}
GR = {'A': '확실히 복습', 'B': '일부 복습', 'C': '복습 효과 약함'}

def mark(m): return MK.get(str(m).strip()[:1], E(m))

def main(cov_path, out):
    cov = json.load(open(cov_path))
    rows, blocks = [], []
    for c in cov:
        n = c['no']; it = C.ITEMS[n]; card = A[it['key']]['study']; traps = A[it['key']]['exam_guide']['traps']
        tr = c.get('traps', [])
        to = sum(1 for t in tr if str(t.get('mark', '')).startswith('O'))
        rows.append(f"<tr><td>{n}번</td><td>{it['key']}</td><td>{E(card['title'])}</td><td>{mark(c['tip']['mark'])}</td>"
                    f"<td>{c['direction'].get('index', '-')} {mark(c['direction']['mark'])}</td><td>{to}/{len(tr)}</td>"
                    f"<td class='g g{c['review_grade']}'>{c['review_grade']} · {GR.get(c['review_grade'], '')}</td></tr>")
        dirs = ''.join(f"<li>{'<b>' if str(i + 1) == str(c['direction'].get('index')) else ''}방향 {i + 1}. {E(d)}{'</b>' if str(i + 1) == str(c['direction'].get('index')) else ''}</li>" for i, d in enumerate(card['directions']))
        trs = ''.join(f"<tr><td>{E(t.get('trap', ''))}</td><td>{mark(t.get('mark', ''))}</td><td>{E(t.get('note', ''))}</td></tr>" for t in tr)
        ch = '  '.join(f"{'①②③④⑤'[i]} {x}" for i, x in enumerate(it['choices']))
        blocks.append(f"""<div class="it"><h2>{n}번 <span>원문 {it['key']} · 분석집: {E(card['title'])}</span> <em class="g g{c['review_grade']}">{c['review_grade']} {GR.get(c['review_grade'], '')}</em></h2>
<div class="q">{C._body(it)}<div class="ch">{ch} &nbsp; <b>[정답 {'①②③④⑤'[it['ans'] - 1]}]</b></div></div>
<table class="t2"><tr><th style="width:23%">분석집 판정·TIP</th><td>{E(card['known'])}</td><td class="m">{mark(c['tip']['mark'])}</td></tr>
<tr><th>이 문항에서 쓰이는 TIP</th><td colspan="2">{E(c['tip'].get('which', ''))}</td></tr>
<tr><th>분석집 변형 방향</th><td><ul>{dirs}</ul>{E(c['direction'].get('how', ''))}</td><td class="m">{mark(c['direction']['mark'])}</td></tr></table>
<table class="t3"><tr><th>분석집·예상 함정</th><th style="width:7%">반영</th><th>이 문항에서</th></tr>{trs}</table>
<p class="why"><b>판정</b> {E(c.get('why', ''))}</p>{f'<p class="fix"><b>보강안</b> {E(c["fix"])}</p>' if c.get('fix') and c['review_grade'] != 'A' else ''}</div>""")
    nA = sum(1 for c in cov if c['review_grade'] == 'A')
    css = """@page{size:A4;margin:14mm 13mm}body{font-family:'HB','GL',serif;font-size:9.6pt;line-height:1.55;color:#111}
h1{font-size:15pt;text-align:center;margin:0 0 4pt}.sub{text-align:center;color:#444;font-size:9pt;margin-bottom:8pt}
table{border-collapse:collapse;width:100%;margin:4pt 0}td,th{border:0.6pt solid #888;padding:3pt 5pt;vertical-align:top}th{background:#f1f1f1;font-weight:700;text-align:left}
.sum td,.sum th{text-align:center}.sum td:nth-child(3){text-align:left}
.it{page-break-inside:avoid;margin-top:10pt;border-top:1.2pt solid #333;padding-top:5pt}h2{font-size:11.5pt;margin:0 0 4pt}h2 span{font-weight:400;font-size:9.5pt;color:#333}
.q{background:#fafafa;border:0.6pt solid #bbb;padding:5pt 7pt;margin:3pt 0 5pt}.q .cond{border:0.6pt solid #999;padding:2pt 6pt;margin:3pt 0}.q .fig{display:none}.ch{margin-top:3pt}
.m{width:7%;text-align:center}ul{margin:0 0 2pt;padding-left:14pt}b.o{color:#0a6a2a}b.t{color:#a46a00}b.x{color:#b0182a}
em.g{font-style:normal;font-size:9pt;padding:1pt 6pt;border-radius:3pt;margin-left:6pt}.gA{background:#dff2e3}.gB{background:#fff1cf}.gC{background:#f9dcdc}
.why,.fix{margin:3pt 0}.fix{color:#5a3b00}.note{font-size:8.8pt;color:#444}"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{css}</style></head><body>'
         '<h1>미적분Ⅰ 기말 2회(복습형) · 분석서2 — 분석집 함정·TIP 복습 대조</h1>'
         '<div class="sub">분석집 방향으로 낸 8문항(1–16번의 절반)이 분석집 카드의 판정·TIP, 변형 방향, 예상 함정을 실제로 쓰게 하는지 · '
         '출제에 참여하지 않은 검토자가 문항을 직접 풀고 판정</div>'
         f'<table class="sum"><tr><th>번호</th><th>원문</th><th>분석집 주제</th><th>TIP</th><th>변형 방향</th><th>함정 반영</th><th>복습 판정</th></tr>{"".join(rows)}</table>'
         f'<p class="note">O = 핵심으로 쓰임 · △ = 쓰이지만 부수적이거나 생략 가능 · X = 쓰이지 않음. 복습 판정: A = 분석집을 공부한 학생이 확실히 보상받음, B = 일부 복습, C = 분석집 없이도 그대로 풀림. 8문항 중 A {nA}개.</p>'
         + ''.join(blocks) + '</body></html>')
    src = os.path.join(HERE, 'bs2_src.html'); open(src, 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'bs2_src.html', 'bs2_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'bs2_tmp.pdf'), out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
