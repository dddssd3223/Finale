# -*- coding: utf-8 -*-
"""중간고사 18번 원문(C30) 블라인드 변형 ↔ 실제 2학기 중간 18번 비교 1장"""
import os, sys, re, json, subprocess, html
RUN = sys.argv[1]            # 빌드 환경 폴더 (build3.py, render3.js, ../fonts 있는 곳)
OUT = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN); from build3 import font_css, KATEX_CSS
sys.path.insert(0, '/home/user/Finale/template/db/parts'); sys.path.insert(0, '/home/user/Finale/template/db')
ns = {}; exec(open(os.path.join(HERE, 'p_mid18.py')).read(), ns); it = ns['ITEMS'][18]
src = open('/home/user/Finale/template/db/parts/items_p4.py').read()
from items_common import COND
I = {}; exec(src[src.index("I['C30']"):src.index("I['C31']")], {'COND': COND, 'I': I}); orig = I['C30']
real = [x for x in json.load(open('/home/user/Finale/output/build/분석_정기고사3회_변형/s2_mid.json')) if str(x['no']) == '18'][0]
E = html.escape; C = '①②③④⑤'
fix = lambda s: re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div class="dm">\\(\\displaystyle ' + m.group(1) + '\\)</div>', s)
def chs(ch, a): return '<div class="chs">' + ''.join(f'<span class="{"ok" if i == a else ""}">{C[i-1]} \\({c}\\)</span>' for i, c in enumerate(ch, 1)) + '</div>'
mine = it['body'] + COND(it['cond']) + it['after'] + chs(it['choices'], it['ans'])
o = orig[0] + chs(orig[1], C.index(orig[2]) + 1)
rows = [('남긴 것', '이차함수 \\(f\\), 두 함수 \\(g=\\dfrac{x}{f(x^2+4)}\\), \\(h=\\dfrac{f(x-4)}{f(x^2)}\\), 조건 (가) 그대로', '\\(f(x^2)\\)가 분모인 분수 꼴 함수와 불연속점 판정'),
        ('바꾼 판정 원리', '(나)를 \\(h\\)의 불연속점 → 합성함수 \\(g(h(x))\\)의 불연속점으로. (가)의 \\(a=0\\)이 (나)로 이어져 분자의 근이 분모의 근과 겹치는지로 판정', '이차 → 사차, 두 함수를 \\(g=\\dfrac{f(x)}{f(x^2)}\\) 하나로 합침. \\(x=0\\)에서 차수 비교라는 새 단계'),
        ('조건 수', '2개 (가)(나)', '3개 (가)(나)(다)'),
        ('구하는 것', '가능한 모든 \\(f(1)\\)의 합 (함수 3개, 원본의 함수 포함)', '\\(f(2)\\) 하나'),
        ('답', f'{C[it["ans"]-1]} \\({it["choices"][it["ans"]-1]}\\)', f'{E(real["answer"])}'),
        ('난도 인상', '원본보다 어려워짐(경우 4가지). 원본 틀이 더 많이 남아 공부한 학생에게 익숙', E(real['diff_effect']))]
tab = ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
body = (f'<h1>중간고사 18번 원문 블라인드 변형 · 실제 시험과 비교</h1>'
        f'<div class="sub">원문: 2024년 수능완성 [24054-0106] (부교재 C30, Level Up) · 변형은 실제 18번을 보지 않고 출제 지침서(0-4 변형 거리, 0-6 말투, 17–18번 규칙)만으로 작성</div>'
        f'<div class="two"><div class="col"><div class="lab">부교재 원문</div>{o}</div><div class="col"><div class="lab">블라인드 변형 (18번, 5.2점)</div>{mine}</div></div>'
        f'<div class="box"><div class="lab">실제 2학기 중간 18번 (요약)</div>{E(real["exam"])}</div>'
        f'<table class="cmp"><tr><th></th><th>블라인드 변형</th><th>실제 중간고사 18번</th></tr>{tab}</table>'
        f'<div class="box"><div class="lab">블라인드 변형 풀이</div>{it["sol"]}<div class="lab" style="margin-top:3pt">빠른 풀이</div>{it["fast"]}<div class="lab" style="margin-top:3pt">원본 대비</div>{it["note"]}<div class="lab" style="margin-top:3pt">오답 설계</div>{it["wrong"]}</div>')
css = r"""@page{size:A4;margin:12mm 11mm}body{font-family:'HB','MJ';font-size:9pt;line-height:1.55;margin:0}
.katex{font-family:'TN','KaTeX_Main'}.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
h1{font-family:'GL';font-weight:400;font-size:14pt;text-align:center;margin:0 0 1mm}.sub{text-align:center;font-family:'GL';font-size:8pt;color:#555;margin-bottom:4mm}
.two{display:grid;grid-template-columns:1fr 1fr;border:.8pt solid #333}.col{padding:5pt 7pt;min-width:0}.col+.col{border-left:.6pt solid #999}
.lab{font-family:'GL';font-size:8pt;color:#1f4e9a;margin-bottom:2pt}.chs{display:flex;flex-wrap:wrap;gap:2pt 12pt;margin-top:3pt}.ok{color:#c0392b}
.cond{border:.6pt solid #000;padding:2pt 5pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}.ck{margin-right:3pt}.dm{text-align:center;margin:2pt 0}
.box{border:.6pt solid #999;padding:4pt 7pt;margin-top:4mm}table.cmp{border-collapse:collapse;width:100%;margin-top:4mm}
.cmp th,.cmp td{border:.5pt solid #999;padding:3pt 5pt;font-size:8.4pt;vertical-align:top;text-align:left}.cmp th{font-family:'GL';font-weight:400;background:#eef0f3;white-space:nowrap}"""
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{css}</style></head><body>{fix(body)}</body></html>'
h = re.sub(r'\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), h)
open(os.path.join(RUN, 'm18_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(RUN, 'render3.js'), 'm18_src.html', 'm18_tmp.pdf', 'bg'], cwd=RUN, check=True)
os.replace(os.path.join(RUN, 'm18_tmp.pdf'), OUT)
