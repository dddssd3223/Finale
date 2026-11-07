# -*- coding: utf-8 -*-
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'r20'))
from build3 import font_css, KATEX_CSS

PT = {n: p for n, p in zip(range(1, 21), [4.0]*4 + [4.2]*4 + [4.4]*2 + [4.5]*2 + [4.7]*3 + [4.9] + [5.2]*2 + [10, 10])}
# n: (구조, 난이도 0기본/1=2등급/2=1등급, 출처, 적중 'A'원본/'B'유형/'X', 모의고사 이력, 비교 대상 이미지, 비교 라벨, 변형 비교)
R = {
1: ('그래프와 좌·우극한', 0, '부교재 01 함수의 극한 49번 유형<br>(2027학년도 6월 모의평가 4번)', 'B', '16회 1번', 'mock_16-1', '16회 1번',
    r"같은 질문 틀: 그래프에서 \(x=-1\), \(x=1\)의 한쪽 극한 두 개를 더하거나 빼기. 실제 시험은 그래프를 새로 그렸어요."),
2: ('연속과 미정계수', 0, '유형 대표 문항', 'B', '9회 3번, 16회 6번, 20회 6번', 'mock_20-6', '20회 6번',
    r"실제 \(\dfrac{x^2+ax-2}{x-1}\), 모의 \(\dfrac{x^2-ax+2}{x-2}\). 묻는 값 \(a+b\)까지 같아요."),
3: ('평균값 정리', 0, '부교재 수록 2022 수능특강 [22009-0051] 유형', 'X', '—', None, None, ''),
4: ('평균값 정리 응용', 0, '부교재 외 (DB 미수록)', 'X', '—', None, None, ''),
5: ('함수의 극한의 대소 관계', 0, '부교재 01 함수의 극한 29번<br>(2022 수능완성 [22054-0103])', 'A', '15회 10번', 'mock_15-10', '15회 10번',
    r"실제는 \(x\to\infty\), 모의는 \(x\to2\)에서 부등식으로 \(\dfrac{f}{g}\)의 극한을 정한 뒤 식에 대입. 풀이 구조 동일."),
6: ('사잇값 정리', 0, '부교재 02 함수의 연속 34번<br>(2025 수능특강 [25009-0048])', 'B', '7회 서술, 12회 16번, 18회 서술', 'mock_18-S2', '18회 서술형',
    r"실근이 존재하는 구간을 사잇값 정리로 판단. 18회 서술형에서 같은 논리(부호가 바뀌는 구간)를 3단계로 연습했어요."),
7: ('삼차함수 결정', 0, '부교재 p.62 37번<br>(2024 수능특강 [24009-0069])', 'A', '2회 12번, 5회 13번, 10회 13번', 'mock_10-13', '10회 13번',
    r"실제 \(\{x\mid f(x)=2\}=\{-2a,\,-a,\,a\}\), \(f'(1)=-2\). 모의 \(\{-a,\,a,\,3a\}\), \(f'(1)=-4\). 집합 원소 배치만 바뀌었어요."),
8: ('곱의 미분법', 0, '부교재 p.59 29번<br>(2022 수능완성 [22054-0129])', 'A', '3회 7번, 5회 3번', 'mock_5-3', '5회 3번',
    r"실제 \((x+2)(x-2)g(x)=f(x)+3\), 모의 \((x^2-9)g(x)=f(x)+1\). 대입해서 \(f\)의 값, 미분해서 \(g\)의 값을 구하는 순서 동일."),
9: ('정수 조건 부등식과 삼차함수', 1, '부교재 p.73 63번<br>(2025학년도 9월 모의평가 21번)', 'A', '4회 서술, 16회 15번', 'mock_16-15', '16회 15번',
    r"실제 \(6k-6\le\dfrac{f(k+1)-f(k-1)}2\le3k^2-9k+12\), 모의 \(4k-6\le\dfrac{f(k+2)-f(k)}2\le4k^2-6\). 양 끝이 같아지는 정수에서 등호를 쓰는 핵심 동일."),
10: ('∞꼴 극한과 다항함수 결정', 0, '부교재 01 함수의 극한 58번<br>(2010학년도 6월 모의평가 가형 19번)', 'A', '11회 11번 (유사: 10회 10번, 17회 8번)', 'mock_11-11', '11회 11번',
    r"실제 \(\displaystyle\lim_{x\to0+}\frac{x^3f(1/x)-5}{x^3+5x}=5\), 모의 \(\displaystyle\lim_{x\to0+}\frac{x^3f(1/x)-2}{x^3+x}=3\). 두 번째 극한으로 근을 정하는 흐름 동일."),
11: ('좌·우극한과 함수의 곱', 0, '부교재 01 함수의 극한 33번<br>(2021 수능특강 [21009-0014])', 'A', '10회 9번', 'mock_10-9', '10회 9번',
    r"실제 \(f=\{-x+2a,\ x+2\}\), \(g=\{f(x)+1\}\{f(-x)+a\}\). 모의 \(f=\{-x+3a,\ x+2\}\), \(g=f(x)\{f(-x)+2a\}\). 거의 같은 식이에요."),
12: ('함수의 곱의 연속', 1, '부교재 02 함수의 연속 9번<br>(2014학년도 수능 A형 28번)', 'A', '13회 12번 (같은 발상: 14회 12번, 18회 10번)', 'mock_13-12', '13회 12번',
    r"\(f(x)f(x-a)\)의 연속. 점프가 상쇄되는 특수한 \(a\)(실제 \(a=0,\,2\))를 따로 확인하는 함정까지 14·18회에서 연습했어요."),
13: ('대칭축과 미분계수의 합', 0, '부교재 p.67 47번<br>(2025 수능특강 [25009-0076])', 'A', '4회 11번, 11회 13번, 17회 12번', 'mock_17-12', '17회 12번',
    r"실제 \(f(2x-1)=f(11-2x)\)로 대칭축 \(x=5\), 모의 \(f'(x)+f'(6-x)=0\)으로 대칭축 \(x=3\). 극한의 합 \(=-f(0)\) 구조 동일."),
14: ('도형과 극한', 0, '부교재 외 (DB 미수록)', 'B', '15회 14번, 16회 4번, 20회 4번', 'mock_20-4', '20회 4번',
    r"실제는 두 원 사이 최소 거리, 모의는 선분 길이. 둘 다 \(\sqrt{\ }\) 꼴 차를 유리화해서 극한을 구하는 계산이에요."),
15: ('접선과 도형', 1, '부교재 p.78 1번<br>(2024학년도 수능 20번)', 'A', '3회 15번, 5회 17번, 8회 14번, 18회 15번', 'mock_18-15', '18회 15번',
    r"원점에서의 접선이 곡선과 다시 만나는 점 A, A에서의 접선이 \(x\)축과 만나는 점 B. 실제는 \(\overline{\mathrm{OA}}=\overline{\mathrm{AB}}\), 모의는 \(\angle\mathrm{OAB}=90^\circ\)."),
16: ('함숫값을 따로 정의한 함수의 극한', 1, '부교재 02 함수의 연속 54번<br>(2024학년도 9월 모의평가 15번)', 'A', '13회 15번, 17회 13번', 'mock_17-13', '17회 13번',
    r"\(f(\cdot)=\)상수인 점에서만 함숫값을 따로 정의. 극한과 함숫값의 차이로 \(f\)의 근을 찾는 핵심 동일."),
17: ('합성함수의 극한', 2, '부교재 외 (DB 미수록)', 'X', '—', None, None, ''),
18: ('\\(f(x)/f(x^2)\\)의 불연속', 2, '부교재 02 함수의 연속 30번 유형<br>(2024 수능완성 [24054-0106])', 'B', '3회 단답형, 9회 서술, 12회 서술', 'mock_12-S2', '12회 서술형',
    r"분모에 \(f(x^2)\)가 있는 함수의 불연속점·극한 존재 조건. 12회 서술 \(h=\dfrac{f(x-3)}{f(x^2)}\)와 같은 분석이에요."),
19: ('절댓값 함수의 연속·미분가능성', 0, '기본 (교과서 수준)', 'B', '16회 12번, 20회 12·16번', 'mock_20-16', '20회 16번',
    r"꺾인 점에서 좌미분계수와 우미분계수를 비교하는 기본 논리. 모의고사 여러 회차에서 반복했어요."),
20: ('\\(f(\\text{일차식})/f(\\text{일차식})\\)의 극한', 2, '부교재 01 함수의 극한 68번<br>(2025학년도 수능 21번)', 'A', '8회 16번, 17회 17번, 20회 18번', 'mock_20-18', '20회 18번',
    r"실제 \(\dfrac{f(4x+4)}{f(2x+3)}\), 모의 \(\dfrac{f(3x+2)}{f(x)}\). 실근이 고정점 하나뿐이고 나머지 이차식은 판별식 \(<0\)이라는 핵심이 같아요. 실제 (3) \(f(1)\)의 최댓값까지 동일."),
}
DIF = [('기본 유형', '#888'), ('2등급 변별 문항', '#1f3fd6'), ('1등급 변별 문항', '#e01b24')]
HIT = {'A': ('원본 적중', '#0b7a35'), 'B': ('유형 적중', '#b36b00'), 'X': ('미적중', '#999')}

def tot(c): return sum(PT[n] for n in R if R[n][3] == c)
na, nb, nx = (sum(1 for n in R if R[n][3] == c) for c in 'ABX')

CSS = r"""
@page{size:A4;margin:13mm 12mm 12mm 12mm}
html,body{margin:0;background:#fff}
body{font-family:'GL';font-size:9pt;color:#111}
.katex{font-size:1em}
h1{font-size:16pt;text-align:center;margin:0 0 2pt;letter-spacing:.5pt;-webkit-text-stroke:.35pt #000}
.sub{text-align:center;font-size:9.5pt;color:#444;margin-bottom:8pt}
.tag{display:inline-block;background:#111;color:#fff;padding:2pt 8pt;font-size:9pt;letter-spacing:1pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
table{border-collapse:collapse;width:100%}
th,td{border:.6pt solid #999;padding:1.6pt 3pt;text-align:center;vertical-align:middle;line-height:1.25}
.main td,.main th{font-size:7.9pt}
.nw{white-space:nowrap}
th{background:#eee;font-weight:400;-webkit-text-stroke:.2pt #000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
td.src{font-size:7.4pt;text-align:center;line-height:1.25}
.dot{display:inline-block;width:7pt;height:7pt;border-radius:50%;margin-right:4pt;vertical-align:-0.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.hit{font-weight:700}
.sum{display:flex;gap:8pt;margin:6pt 0}
.sum div{flex:1;border:1pt solid #ccc;border-radius:4pt;padding:6pt 8pt}
.sum b{font-size:13pt;display:block;margin-top:1pt}
h2{font-size:11pt;margin:8pt 0 4pt;-webkit-text-stroke:.25pt #000}
.ins td{text-align:left;padding:4pt 7pt;line-height:1.5;font-size:8.4pt}
.card{border:1pt solid #bbb;border-radius:4pt;margin:0 0 9pt;break-inside:avoid;padding:6pt 8pt}
.card .hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:5pt}
.card .hd .t{font-size:11pt;-webkit-text-stroke:.25pt #000}
.pair{display:flex;gap:8pt}
.pair .c{flex:1;border:.6pt solid #ddd;padding:3pt}
.pair .c .l{font-size:8pt;color:#555;margin-bottom:2pt}
.pair img{width:100%}
.cmp{margin-top:5pt;font-size:8.8pt;line-height:1.6}
.cmp .k{color:#555}
.badge{color:#fff;border-radius:3pt;padding:1pt 6pt;font-size:8.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pb{break-before:page}
.miss img{width:48%;border:.6pt solid #ddd;margin:2pt}
"""

def row(n):
    s, d, src, h, hist, *_ = R[n]
    dl, dc = DIF[d]; hl, hc = HIT[h]
    kind = '객관식' if n <= 18 else '서답형'
    return (f'<tr><td>{n}</td><td class="nw">{kind}</td><td style="text-align:left">{s}</td><td class="nw">{PT[n]:.1f}</td>'
            f'<td class="nw" style="text-align:left;color:{dc}"><span class="dot" style="background:{dc}"></span>{dl}</td>'
            f'<td class="src">{src}</td><td class="hit nw" style="color:{hc}">{hl}</td><td class="src">{hist}</td></tr>')

def card(n):
    s, d, src, h, hist, img, lab, cmp = R[n]
    hl, hc = HIT[h]
    return (f'<div class="card"><div class="hd"><span class="t">실제 {n}번 · {s} <span style="color:#666;font-size:9pt">({PT[n]:.1f}점)</span></span>'
            f'<span class="badge" style="background:{hc}">{hl}</span></div>'
            f'<div class="pair"><div class="c"><div class="l">실제 시험 {n}번</div><img src="real_{n}.png"></div>'
            f'<div class="c"><div class="l">모의고사 {lab}</div><img src="{img}.png"></div></div>'
            f'<div class="cmp"><span class="k">출처</span> {src.replace("<br>", " ")} &nbsp;·&nbsp; <span class="k">모의고사 출제</span> {hist}<br>'
            f'<span class="k">비교</span> {cmp}</div></div>')

def build(out):
    rows = ''.join(row(n) for n in range(1, 21))
    head = f"""<div style="text-align:right"><span class="tag">FINAL PAGE · 적중 분석</span></div>
<h1>양정고등학교 2학년 2026학년도 2학기 중간고사 FINAL PAGE</h1>
<div class="sub">미적분Ⅰ · 2026년 10월 13일(화) 1교시 · 모의고사 1–20회 대조</div>
<table class="main"><colgroup><col style="width:4%"><col style="width:6%"><col style="width:19%"><col style="width:5%"><col style="width:13%"><col style="width:27%"><col style="width:8%"><col style="width:18%"></colgroup><tr><th>번호</th><th>구조</th><th>문항 유형</th><th>배점</th><th>난이도</th><th>출처</th><th>적중</th><th>모의고사 출제 회차</th></tr>{rows}</table>
<div class="sum"><div>원본 적중 (같은 원본·같은 풀이 구조)<b style="color:#0b7a35">{na}문항 · {tot('A'):.1f}점</b></div>
<div>유형 적중 (같은 문항 틀·같은 핵심 논리)<b style="color:#b36b00">{nb}문항 · {tot('B'):.1f}점</b></div>
<div>미적중<b style="color:#888">{nx}문항 · {tot('X'):.1f}점</b></div></div>
<h2>INSIGHT</h2>
<table class="ins"><tr><td style="width:24%;text-align:center">예상 등급컷</td><td>
<span class="dot" style="background:#e01b24"></span>1등급(상위 10%) <b>87점</b> (86–88) &nbsp;&nbsp;
<span class="dot" style="background:#1f3fd6"></span>2등급(34%) <b>73점</b> (72–74) &nbsp;&nbsp; 3등급(66%) <b>52점</b> &nbsp;&nbsp; 4등급(90%) <b>27점</b><br>
<span style="color:#666">참고: 1학기 기말 실제 컷 90.1 / 76.1 / 55.8 / 27.7 (상위권은 예상보다 높고 중위권은 낮게 형성)</span></td></tr>
<tr><td style="text-align:center">출제 분석</td><td>
· 20문항 중 <b>{na + nb}문항({tot('A') + tot('B'):.1f}점)</b>이 모의고사에서 원본 또는 같은 유형으로 출제됐어요.<br>
· 1–16번은 부교재 평가원·수능특강 문항을 숫자·조건만 바꿔 냈어요. 1학기와 같은 출제 습관이에요.<br>
· 킬러 20번은 2025학년도 수능 21번(부교재 68번) 변형으로, 모의고사 8·17·20회에서 세 번 연습했어요.<br>
· 미적중: 3·4번 평균값 정리(모의고사 범위에서 제외했던 단원), 17번 합성함수 극한(그래프 활용).</td></tr>
<tr><td style="text-align:center">본인 점수</td><td><b>88.8점</b> → 예상 1등급 컷보다 위. 실제 컷이 1학기 기말처럼 높게 형성되면 경계 근처.</td></tr></table>"""
    hits = [n for n in range(1, 21) if R[n][3] in 'AB']
    hits.sort(key=lambda n: (R[n][3] != 'A', n))
    cards = '<div class="pb"></div><h2>원본 적중 문항 비교 (실제 시험 ↔ 모의고사)</h2>' + ''.join(card(n) for n in hits if R[n][3] == 'A')
    cards += '<div class="pb"></div><h2>유형 적중 문항 비교</h2>' + ''.join(card(n) for n in hits if R[n][3] == 'B')
    miss = ('<div class="pb"></div><h2>미적중 문항과 기말 대비</h2><div class="miss">'
            + ''.join(f'<img src="real_{n}.png">' for n in (3, 4, 17)) + '</div>'
            + r"""<table class="ins" style="margin-top:6pt"><tr><td style="width:24%;text-align:center">3·4번 평균값 정리</td><td>모의고사에서는 범위 밖으로 빼 두었던 단원이에요. 실제로는 기본 문항 2개(8점)로 출제됐어요. 기말 범위를 정할 때 교과서 단원을 다시 확인해서 넣을게요.</td></tr>
<tr><td style="text-align:center">17번 합성함수 극한</td><td>그래프가 주어진 \(f\)와 이차함수 \(g\)의 합성 \(\displaystyle\lim_{x\to t}(f\circ g)(x)\). 속함수 \(g(x)\)가 다가가는 방향(위·아래·양쪽)을 먼저 보는 유형으로, 모의고사에서 다루지 않았어요. 기말 대비 유형으로 추가할게요.</td></tr>
<tr><td style="text-align:center">기말 대비 시사점</td><td>· 부교재 평가원 문항 반영률이 매우 높아요. 부교재 평가원·수능특강 문항의 풀이 구조를 그대로 익히는 전략이 유효해요.<br>· 킬러는 최신 수능·평가원 21번급에서 출제돼요. 다음에도 부교재 최신 평가원 고난도 문항을 우선 대비해요.<br>· 서답형은 기본 논증(연속·미분가능성) 1문항과 킬러 분할형 1문항 구성이었어요.</td></tr></table>""")
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{cards}{miss}</body></html>')
    open(os.path.join(HERE, 'rep_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'rep_src.html', 'rep_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'rep_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
