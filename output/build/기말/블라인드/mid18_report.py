# -*- coding: utf-8 -*-
"""중간고사 18번 원문(C30) · 블라인드 변형 · 실제 2학기 중간 18번 비교"""
import os, sys, re, json, subprocess
RUN, OUT = sys.argv[1], sys.argv[2]          # RUN: build3.py, render3.js, ../fonts 가 있는 빌드 폴더
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN); from build3 import font_css, KATEX_CSS
sys.path.insert(0, '/home/user/Finale/template/db/parts'); sys.path.insert(0, '/home/user/Finale/template/db')
from items_common import COND

ns = {}; exec(open(os.path.join(HERE, 'p_mid18.py')).read(), ns); it = ns['ITEMS'][18]
src = open('/home/user/Finale/template/db/parts/items_p4.py').read()
I = {}; exec(src[src.index("I['C30']"):src.index("I['C31']")], {'COND': COND, 'I': I}); orig = I['C30']
C = '①②③④⑤'

def chs(ch, a):
    return '<div class="chs">' + ''.join(f'<span class="{"ok" if i == a else ""}">{C[i-1]} \\({c}\\)</span>' for i, c in enumerate(ch, 1)) + '</div>'

ORIG = orig[0] + chs(orig[1], C.index(orig[2]) + 1)
MINE = it['body'] + COND(it['cond']) + it['after'] + chs(it['choices'], it['ans'])
REAL = (r"최고차항의 계수가 \(1\)인 사차함수 \(f(x)\)에 대하여 함수 \(g(x)=\dfrac{f(x)}{f(x^2)}\)가 다음 조건을 만족시킨다." + COND([
    ('가', r"서로 다른 세 실수 \(a\), \(b\), \(c\)에 대하여 함수 \(g(x)\)는 \(x=a\), \(x=b\), \(x=c\)에서만 불연속이다."),
    ('나', r"\(\displaystyle\lim_{x\to p}g(x)\)의 값이 존재하지 않는 실수 \(p\)의 값은 오직 한 개다."),
    ('다', r"\(\displaystyle\lim_{x\to-3}g(x)=0\)")]) + r"\(f(2)\)의 값은? [5.2점]" + chs(['24', '26', '28', '30', '32'], 4))

ROWS = [
    ('원본에서 남긴 것', r"이차함수 \(f\), 두 함수 \(g=\dfrac{x}{f(x^2+4)}\), \(h=\dfrac{f(x-4)}{f(x^2)}\)의 식, 조건 (가) 문장",
     r"분모가 \(f(x^2)\)인 분수 꼴, '\(f(x^2)=0\)의 근 \(\pm\sqrt r\)과 분자에 의한 약분' 판정"),
    ('함수 교체', r"없음 (이차함수, \(g\)와 \(h\) 그대로)", r"이차 → 사차, 두 함수 → \(\dfrac{f(x)}{f(x^2)}\) 하나 (분자와 분모가 같은 \(f\))"),
    ('조건 변경', r"(나) \(h\)의 불연속점 2개와 극한 존재 → \(g(h(x))\)의 불연속점 3개",
     r"불연속점 1개·2개 → 불연속점 3개 + 극한이 없는 점 1개 + \(\displaystyle\lim_{x\to-3}g(x)=0\)"),
    ('바뀐 판정 원리', r"합성함수의 불연속점 = \(h\)가 정의되지 않는 점 + \(h(x)=a\)인 점. 분자의 근이 분모의 근과 겹치는지로 개수를 셈",
     r"\(x=0\)에서 차수 비교(\(f(x^2)\)이 \(x\)를 두 배로 가짐)로 \(f(0)=0\), 양의 근이 하나뿐임을 결정"),
    ('조건 수', '2개', '3개'),
    ('구하는 것', r"가능한 모든 \(f(1)\)의 값의 합 (함수 3개, 원본의 함수 포함)", r"\(f(2)\) 하나"),
    ('답', r"② \(-21\)", r"④ \(30\) (\(f(x)=x(x-1)(x+1)(x+3)\))"),
    ('난도', '원본보다 어려워짐: 경우 4가지를 나눠야 함. 원본 틀이 많이 남아 공부한 학생에게는 익숙함',
     '어려워짐: 사차함수에 조건 셋, 차수 비교라는 새 단계. 1등급 변별 문항'),
]
TAB = ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in ROWS)
CONCL = ("실제 학교 18번은 원본에서 '분모 \\(f(x^2)\\)의 근과 약분' 판정만 남기고 함수 교체(이차 → 사차)와 두 함수 통합, 조건 세 개로 거의 새로 짰다. "
         "블라인드 변형은 원본의 \\(f\\), \\(g\\), \\(h\\)와 조건 (가)를 그대로 두고 (나)의 판정 원리 하나만 바꿨다. "
         "그래서 지침서의 변형 거리(원본 틀 유지 + 원리 하나 교체)는 학교 18번보다 한 단계 약하다. "
         "학교 수준에 맞추려면 17·18번은 '원리 교체'에 '함수 교체(차수 올리기·두 식 합치기)'를 하나 더 얹어야 한다.")

body = ('<h1>중간고사 18번 원문 · 블라인드 변형 · 실제 시험 비교</h1>'
        '<div class="sub">원문: 2024년 수능완성 [24054-0106] (부교재 C30, Level Up) · 블라인드 변형은 실제 18번을 보지 않고 출제 지침서(0-4 변형 거리, 0-6 말투, 17–18번 규칙)로 작성</div>'
        f'<div class="three"><div class="col"><div class="lab">부교재 원문 (C30)</div>{ORIG}</div>'
        f'<div class="col"><div class="lab">블라인드 변형 (지침서대로)</div>{MINE}</div>'
        f'<div class="col"><div class="lab">실제 2학기 중간 18번</div>{REAL}</div></div>'
        f'<table class="cmp"><tr><th></th><th>블라인드 변형</th><th>실제 중간고사 18번</th></tr>{TAB}</table>'
        f'<div class="box"><div class="lab">비교 결과</div>{CONCL}</div>'
        f'<div class="box"><div class="lab">블라인드 변형 풀이</div>{it["sol"]}'
        f'<div class="lab" style="margin-top:3pt">빠른 풀이</div>{it["fast"]}'
        f'<div class="lab" style="margin-top:3pt">원본 대비</div>{it["note"]}'
        f'<div class="lab" style="margin-top:3pt">오답 설계</div>{it["wrong"]}</div>')

CSS = r"""@page{size:A4;margin:11mm 10mm}body{font-family:'HB','MJ';font-size:8.8pt;line-height:1.55;margin:0}
.katex{font-family:'TN','KaTeX_Main'}.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
h1{font-family:'GL';font-weight:400;font-size:14pt;text-align:center;margin:0 0 1mm}.sub{text-align:center;font-family:'GL';font-size:7.8pt;color:#555;margin-bottom:3mm}
.three{display:grid;grid-template-columns:1fr 1fr 1fr;border:.8pt solid #333;font-size:8pt}.col{padding:4pt 6pt;min-width:0}.col+.col{border-left:.6pt solid #999}
.lab{font-family:'GL';font-size:7.8pt;color:#1f4e9a;margin-bottom:2pt}.chs{display:flex;flex-wrap:wrap;gap:1pt 9pt;margin-top:3pt}.ok{color:#c0392b}
.cond{border:.6pt solid #000;padding:2pt 4pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}.ck{margin-right:3pt}.dm{text-align:center;margin:2pt 0}
.box{border:.6pt solid #999;padding:4pt 7pt;margin-top:3mm}table.cmp{border-collapse:collapse;width:100%;margin-top:3mm}
.cmp th,.cmp td{border:.5pt solid #999;padding:3pt 5pt;font-size:8.2pt;vertical-align:top;text-align:left}.cmp th{font-family:'GL';font-weight:400;background:#eef0f3;white-space:nowrap}
.cmp td{width:44%}"""

fix = lambda s: re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div class="dm">\\(\\displaystyle ' + m.group(1) + '\\)</div>', s)
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{fix(body)}</body></html>'
h = re.sub(r'\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), h)
open(os.path.join(RUN, 'm18_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(RUN, 'render3.js'), 'm18_src.html', 'm18_tmp.pdf', 'bg'], cwd=RUN, check=True)
os.replace(os.path.join(RUN, 'm18_tmp.pdf'), OUT)
