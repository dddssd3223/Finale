# -*- coding: utf-8 -*-
"""미적분Ⅰ 서답형 답안지: 학교 실제 서답형 답안지(통합사회2, 2026 2학기 중간) 양식을 그대로 옮김. 좌표(pt)는 원본 스캔 실측.
사용: python3 answer_sheet.py <출력 PDF> <나눔고딕 폴더> [제목 과목] [고사] [학년]"""
import sys, os, subprocess
OUT, FD = sys.argv[1], sys.argv[2]
SUBJ = sys.argv[3] if len(sys.argv) > 3 else '미적분Ⅰ'
EXAM = sys.argv[4] if len(sys.argv) > 4 else '기말고사'
GRADE = sys.argv[5] if len(sys.argv) > 5 else '2학년'
# 행 구성: (번호, [(소문항 라벨, 높이 pt, 배점)], 합계)  — 서답형1 풀이 서술 4+6, 서답형2 답만 4+4+2
ROWS = [('1', [('(1)', 178, '4'), ('(2)', 196, '6')], '10'),
        ('2', [('(1)', 40, '4'), ('(2)', 40, '4'), ('(3)', 41, '2')], '10')]
X = dict(L=54.5, N=91.5, B1=407.3, B2=433.9, C1=460.7, C2=500.4, R=540.5)
TOP, HDR = 214.8, 45.5
f = lambda n: 'file://' + os.path.join(FD, n)
css = f"""@font-face{{font-family:'NG';src:url('{f('NanumGothic-Regular.ttf')}')}}
@font-face{{font-family:'NG';src:url('{f('NanumGothic-Bold.ttf')}');font-weight:700}}
@page{{size:595pt 841pt;margin:0}}body{{margin:0}}
.pg{{position:relative;width:595pt;height:841pt;font-family:'NG';color:#111}}
.a{{position:absolute}}.c{{display:flex;align-items:center;justify-content:center}}
.hl{{position:absolute;height:0;border-top:.8pt solid #222}}.vl{{position:absolute;width:0;border-left:.8pt solid #222}}
.th{{border-top-width:1.4pt}}.tv{{border-left-width:1.4pt}}
.hole{{position:absolute;width:6.2pt;height:6.2pt;border:.7pt solid #333;border-radius:50%}}
b{{font-weight:700}}"""
h = []
def hl(x0, x1, y, thick=False): h.append(f'<div class="hl{" th" if thick else ""}" style="left:{x0}pt;top:{y}pt;width:{x1-x0}pt"></div>')
def vl(x, y0, y1, thick=False): h.append(f'<div class="vl{" tv" if thick else ""}" style="left:{x}pt;top:{y0}pt;height:{y1-y0}pt"></div>')
def box(x0, y0, x1, y1, txt, size=9.5, bold=True, align='center', pad=0):
    jc = {'center': 'center', 'left': 'flex-start'}[align]
    h.append(f'<div class="a c" style="left:{x0}pt;top:{y0}pt;width:{x1-x0}pt;height:{y1-y0}pt;justify-content:{jc};padding-left:{pad}pt;box-sizing:border-box;font-size:{size}pt;font-weight:{700 if bold else 400}">{txt}</div>')
# 펀치 구멍 표시와 절취 점선
for x in (106, 141, 272, 307, 440, 476): h.append(f'<div class="hole" style="left:{x}pt;top:54pt"></div>')
for x in (119, 152, 438, 471): h.append(f'<div class="hole" style="left:{x}pt;top:175pt"></div>')
h.append('<div class="a" style="left:55pt;top:190pt;width:486pt;border-top:.7pt dotted #444"></div>')
# 제목·인적 사항
box(0, 82, 595, 112, f'{SUBJ}과&nbsp;&nbsp;서답형&nbsp;&nbsp;답안지', size=17)
h.append('<div class="a" style="left:55.5pt;top:140pt;width:470pt;height:29pt;border:1.3pt solid #222;box-sizing:border-box"></div>')
box(55.5, 140, 525, 169, f'2026년도&nbsp;&nbsp;&nbsp;2학기&nbsp;&nbsp;&nbsp;{EXAM}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{GRADE}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;반&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;번&nbsp;&nbsp;&nbsp;이름:', size=10.5, align='left', pad=11)
# 표 머리
y = TOP
hl(X['L'], X['R'], y, True); hl(X['C1'], X['R'], y + HDR / 2); hl(X['L'], X['R'], y + HDR)
box(X['L'], y, X['N'], y + HDR, '번호', 10); box(X['N'], y, X['B1'], y + HDR, '답&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;란', 10)
box(X['B1'], y, X['C1'], y + HDR, '배점', 10); box(X['C1'], y, X['R'], y + HDR / 2, '채점', 10)
box(X['C1'], y + HDR / 2, X['C2'], y + HDR, '초검', 9); box(X['C2'], y + HDR / 2, X['R'], y + HDR, '재검', 9)
y += HDR
for no, subs, tot in ROWS:
    y0 = y
    for i, (lab, ht, pt) in enumerate(subs):
        box(X['N'] + 6, y + 4, X['N'] + 40, y + (22 if ht > 60 else ht - 4), lab, 10, align='left', pad=0)
        box(X['B1'], y, X['B2'], y + ht, pt, 8.5, bold=False)
        if i < len(subs) - 1: hl(X['N'], X['B2'], y + ht)
        y += ht
    box(X['L'], y0, X['N'], y, no, 11); box(X['B2'], y0, X['C1'], y, tot, 10)
    hl(X['L'], X['R'], y, y == TOP + HDR + sum(s[1] for r in ROWS for s in r[1]))
for k, x in X.items():
    y_start = TOP + HDR if k == 'B2' else (TOP + HDR / 2 if k == 'C2' else TOP)
    vl(x, y_start, y, k in ('L', 'R'))
# 점수 칸
S = dict(L=229.3, a=338.3, b=361.1, c=443.2, d=463.4, R=540.4); sy0, sy1 = 773.6, 835
h.append(f'<div class="a" style="left:{S["L"]}pt;top:{sy0}pt;width:{S["R"]-S["L"]}pt;height:{sy1-sy0}pt;border:1.3pt solid #222;box-sizing:border-box"></div>')
for k in ('a', 'b', 'c', 'd'): vl(S[k], sy0, sy1)
box(S['L'], sy0, S['a'], sy1, '점&nbsp;&nbsp;&nbsp;수', 11); box(S['a'], sy0, S['b'], sy1, '초<br>검', 9); box(S['c'], sy0, S['d'], sy1, '재<br>검', 9)
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="pg">{"".join(h)}</div></body></html>'
src = os.path.splitext(OUT)[0] + '_src.html'; open(src, 'w').write(html)
js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{src}');await p.waitForTimeout(400);await p.pdf({{path:'{OUT}',width:'210mm',height:'297mm',printBackground:true}});await b.close()}})()"
subprocess.run(['node', '-e', js], check=True); os.remove(src)
