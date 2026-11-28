# -*- coding: utf-8 -*-
import json, re, os, sys, glob, importlib, subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); SCR=os.path.join(HERE,'..')
sys.path.insert(0,HERE)
from build3 import font_css, KATEX_CSS
sys.path.insert(0,os.path.join(SCR,'wb2/parts')); sys.path.insert(0,os.path.join(SCR,'wbfull'))
I={};DD={}
for f in sorted(glob.glob(os.path.join(SCR,'wb2/parts/items_p*.py'))):
    m=importlib.import_module(os.path.basename(f)[:-3]); I.update(m.I); DD.update(m.D)
W=importlib.import_module('items'); I.update(W.I)
USE=json.load(open(os.path.join(HERE,'use.json')))
LOSTK={'B51':'1회 10번 오답','B65':'2회 17번 오답','A42':'3회 16번 오답','L64':'9회 11번 오답','B50':'12회 3번 오답','B66':'12회 15번 오답','C7':'13회 16번 오답','C18':'15회 16번 오답',
 'B44':'1회 서술 −1','B64':'2회 서술 −1','B43':'3회 서술 −5','B63':'4회 서술 −4','A41':'5회 서술 −1','C24':'7회 서술 −2','C30':'9·12회 서술 감점','L24':'15회 서술 −8'}
# (key, 단원, 예상 위치, 선정 이유, 예상 변형, 핵심(A/B/T만))
T=[
('L65', 'S', '함수의 극한', '17–18번', '2026학년도 6월 모의평가 21번. 가장 최근 평가원 킬러로 학교 시험 최고난도 후보 1순위', 'f를 다른 두 근으로, |g−f| → |g−kf|, 묻는 값 변경', None),
('C55', 'S', '함수의 연속', '17–18번', '2026학년도 수능 21번. 부교재에 실린 최신 수능 킬러', '분모 x(x−2)의 근 변경, 집합 조건의 식 변경', None),
('B54', 'S', '미분법', '5–8번', '2026학년도 6월 모의평가 7번. 최신 평가원 쉬운 문항', '곱하는 식·기준점 변경', 'g′(x)=10x+f(x)+xf′(x), g′(3)=30+2+3=35'),
('L49', 'S', '함수의 극한', '1–3번', '2027학년도 6월 모의평가 4번. 최신 그래프 극한 기본', '그래프 재설계, 좌·우극한 위치 변경', None),
('L63', 'S', '함수의 극한', '10–13번', '2027학년도 6월 모의평가 11번. 부교재 수록 최신 문항', '이동량·상수 변경, 존재/비존재 조건 위치 변경', None),
('L67', 'S', '함수의 극한', '13–15번', '2026학년도 9월 모의평가 13번. 최근 평가원, 판별식 활용 중상급', '기울기 k 범위·개수 묻기 변경', None),
('B63', 'S', '미분법', '15–17번 / 서술', '2025학년도 9월 모의평가 21번. 정수 조건+부등식, 단계형 서술로 바꾸기 좋음', '부등식 경계 식 변경, f′(3) → 다른 점의 값, 단계형', '두 경계가 같아지는 정수 k=−1, −2에서 등호 → f(1)−f(−1), f(0)−f(−2)가 정해져 삼차함수 결정, f′(3)=31'),
('L68', 'S', '함수의 극한', '16–17번', '2025학년도 수능 21번. 최근 수능 극한 킬러', '고정점·실근 조건의 수 변경', None),
('B68', 'S', '미분법(극한·연속)', '17번 / 서술', '2028학년도 수능 예시문항 28번. 새 교육과정 예시라 학교에서 선호', 'f 변경, |x| → |x−c| (대칭축 이동)', 'h가 연속 → g(x)−g(k)가 x=±k에서 중근 → g(x)−g(k)=(x²−k²)², f=(x−1)⁴−(x−1)²에서 a=−1, k²=1/2 → 9'),
('C56', 'S', '함수의 연속', '17–18번', '2023학년도 6월 모의평가 22번. 연속+극한 킬러', '근 위치·조건 값 변경', None),
('C41', 'S', '함수의 연속', '3–6번', '2025학년도 6월 모의평가 9번. 최신 평가원 {f+a}² 연속', '식·상수 변경', None),
('C54', 'S', '함수의 연속', '13–16번', '2024학년도 9월 모의평가 15번. 함숫값 따로 정의한 함수의 극한', '이동량 x+3 → x+2, 함숫값·극한값 변경', None),
('B50', 'S', '미분법', '2–5번', '2024학년도 9월 모의평가 18번. 곱의 미분 기본(12회에서 계수 실수)', '인수·값 변경', 'f′(1)=2(4+a)+2(2+a)… 정리하면 a=5'),
('L62', 'S', '함수의 극한', '14–16번', '2024학년도 6월 모의평가 11번. 접선 개념+도형 극한', '직선의 y절편·극한점 변경', None),
('T1', 'S', '접선', '12–16번 / 단답', '2024학년도 수능 20번(대표기출). 1학기 16번처럼 대표기출 4점을 고난도 자리에 낸 사례 있음', '계수 a 조건·접점 변경', '두 접선 조건으로 a 결정 → 25'),
('C1', 'S', '함수의 연속', '1–4번', '2023학년도 6월 모의평가 6번(대표기출, 3점). 1학기 앞 번호에 평가원 3점 문항이 매번 출제', '경계·값 변경', None),
('C17', 'S', '함수의 연속', '13–16번', '2022학년도 수능 12번(대표기출). 1학기 16번이 유형 대표기출 4점이었음', '식의 인수·최댓값 조건 변경', None),
('A25', 'S', '미분법', '9–12번', '2021학년도 수능 17번(대표기출). 평가원 4점 중급', '극한값 변경', 'f(0)+g(0)=0, f(0)=−3, g(0)=3 → f′(0)=6, g′(0)=−3, h′(0)=f′(0)g(0)+f(0)g′(0)=18+9=27'),
('B48', 'A', '미분가능성', '14–16번 / 서술', '2025 수능특강 Level Up. 구간별 함수 미분가능, 미지수 다수', '구간·덧붙는 식 변경', 'x=−1, 2에서 연속·미분가능 조건 4개로 f와 a, b 결정 → 75'),
('B47', 'A', '도함수', '11–13번', '2025 수능특강 Level Up. 대칭축+극한의 합', '대칭축·합의 범위 변경', '(가) 축 x=4, f=(x−4)²+c, 극한=2f′(k−3), 합=−f(0)에서 c 결정 → 53'),
('B46', 'A', '미분가능성', '11–14번', '2025 수능특강 Level Up. |x+1|과 곱의 미분가능성', '꺾인 점·기울기 변경', 'x=−1에서 g(−1)=0, x=0에서 좌우 미분계수 비교로 g(0)=0 → g=x(x+1), g(4)=20'),
('C33', 'A', '함수의 연속', '10–12번', '2025 수능특강 Level Up. 연속 조건 미정계수 결정', '근 개수·식 변경', None),
('C35', 'A', '함수의 연속', '12–15번', '2025 수능특강. 실근 개수 함수의 불연속', 'f·불연속점 변경', None),
('C36', 'A', '함수의 연속', '10–12번', '2025 수능특강. f(x−1)f(x−a) 연속(14회 변형)', '점프 상쇄 경우가 되도록/안 되도록', None),
('L45', 'A', '함수의 극한', '9–12번', '2025 수능특강. ∞ 꼴 극한과 다항식 결정', '계수·극한값 변경', None),
('L47', 'A', '함수의 극한', '11–13번', '2025 수능특강. 0/0 꼴 미정계수 + 극한값 연립', '극한점·값 변경', None),
('C24', 'B', '함수의 연속', '15–16번 / 서술', '2025 수능완성. 사잇값 정리+실근 개수(7회 서술 감점)', 'g(0)값·구간 변경(경계 근이 답이 되게)', None),
('C7', 'B', '함수의 연속', '14–16번', '2025 수능완성. 구간 최댓값 함수의 연속(13회 오답)', '점프 방향, 묻는 값(최대·최소 합)', None),
('L24', 'B', '함수의 극한', '서술 / 14–16번', '2025 수능완성. |x(x−a)|와 좌·우극한(15회 서술 감점)', '극한값·좌우 판정 추가', None),
('L30', 'B', '함수의 극한', '13–15번', '2025 수능완성. f(x−a) 근 조건 미정계수', '이동량·극한값 변경', None),
('A24', 'B', '미분계수', '9–11번', '2025 수능완성. ∞ 꼴 극한=미분계수', '기준점·계수 변경', 'f=x²+px+q, p=2f′(1)=2(2+p) → p=−4, f(2)=−1 → f(5)=8'),
('A28', 'B', '미분법', '9–12번', '2025 수능완성. 차수·최저차항 판별', '극한값 1/3 → 다른 값', '∞에서 1/차수, 0에서 1/최저차수 → f=x³, f(2)=8'),
('L14', 'B', '함수의 극한', '12–14번', '2025 수능완성. |f−k| 극한 존재 + f/|f−k|', '구간·직선 변경(구간 밖 근 함정)', None),
('A14', 'B', '미분가능성', '9–12번', '2025 수능완성. |f| 미분불가능 점 조건', '미분불가능 점 위치 변경', '연속 1+a=−3+b+c, |f|가 x=3에서만 꺾임 → f(3)=0, x=1에서 미분가능 → a+b+c=18'),
('C14', 'B', '함수의 연속', '6–9번', '2025 수능완성. 곱의 연속, 두 경우', '식·경계 변경', None),
('A10', 'B', '미분가능성', '5–8번', '2025 수능특강. 미분가능 조건 연립(15회 변형: 해가 둘)', '경계·식 변경', '연속 (1+a)(1+b)=a+b, 미분 2+a+b=a → b=−2, a=1/2 → a+b=−3/2'),
('A20', 'B', '도함수', '6–9번', '2025 수능특강. 대칭차분 극한 → 도함수', '계수 변경', '2f′(x)=−8x³+4x²+2, g(x)=3f′(x) → g(0)g(1)=3·3·(−1)… = −9'),
('L5', 'B', '함수의 극한', '1–2번', '2025 수능완성. 좌·우극한 곱', '경계·식 변경', None),
('L18', 'B', '함수의 극한', '3–5번', '2025 수능특강. 선분 길이 극한(무리식)', '점 좌표 변경', None),
('A26', 'B', '미분법', '4–6번', '2025 수능특강. 곱의 미분 기본', '계수 변경', 'g′(2)=20−2f(2)−4f′(2)=20−6−4=10'),
]
assert len(T)==40, len(T)
CSS=r"""
@page{size:A4;margin:14mm 14mm 14mm 14mm}
body{font-family:'HB','MJ','GL',serif;font-size:9.6pt;line-height:1.65;margin:0;color:#000;background:#fff}
.katex{font-size:1.02em;font-family:'TN','KaTeX_Main'}
.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
.katex .text,.katex .text *{font-family:'HB','MJ','TN'!important;font-style:normal}
h1{font-family:'GL';font-size:17pt;font-weight:400;margin:0 0 1mm;-webkit-text-stroke:.3pt #000}
h2{font-family:'GL';font-size:12.5pt;font-weight:400;margin:5mm 0 2mm;border-bottom:1.3pt solid #000;padding-bottom:1mm;-webkit-text-stroke:.2pt #000}
table{border-collapse:collapse;width:100%;margin:1.5mm 0}
td,th{border:.6pt solid #000;padding:1.6pt 3pt;text-align:center;font-weight:400;font-size:8.6pt}
th{background:#eee;-webkit-print-color-adjust:exact;print-color-adjust:exact}
td.l{text-align:left}
.r{color:#c8141a}
.note{border:.7pt solid #000;padding:2.5mm 3.5mm;margin:2mm 0}
.item{break-inside:avoid;margin:0 0 4mm;border:.7pt solid #000}
.ihd{background:#222;color:#fff;padding:2pt 6pt;font-family:'GL';font-size:10pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.ihd .tag{float:right;font-size:8.5pt}
.qb{padding:2mm 3.5mm}
.ch{display:flex;flex-wrap:wrap;gap:1mm 5mm;margin-top:1mm}
.kv{display:flex;border-top:.5pt solid #999}
.kv .k{flex:none;width:22mm;padding:1.5pt 4pt;font-family:'GL';font-size:8.5pt;background:#f2f2f2;border-right:.5pt solid #999;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.kv .v{flex:1;padding:1.5pt 5pt;font-size:9pt}
.cond{border:.6pt solid #000;padding:2pt 6pt;margin:2pt 0}
.ci{padding-left:2.2em;text-indent:-2.2em}.ck{display:inline-block;width:2.2em;text-indent:0}
.bogi{border:.6pt solid #000;padding:2pt 6pt;margin:3pt 0}.bogi legend{font-size:8.5pt}
.bi{display:flex;gap:4pt}
.fig{text-align:center;margin:3pt 0}
.nw{white-space:nowrap}
.cols{columns:2;column-gap:5mm}
"""
CIRC='①②③④⑤'
h=['<h1>화요일 예상 문항 Top 40 (부교재) · 개정판</h1>',
'<div style="font-size:9.5pt">같은 선생님들이 출제한 1학기 중간·기말 출처표와 부교재 원문을 대조해 출제 습관을 분석하고, 그 습관을 2학기 부교재에 적용해 다시 고른 예측입니다. 실제 출제 정보는 아닙니다.</div>']
from part1 import PART1
h+=PART1
rows=[]
for i,(k,tier,u,pos,why,var,key) in enumerate(T,1):
    hist=', '.join(USE.get(k,[])) or '—'
    lost=LOSTK.get(k,'')
    rows.append(f'<tr><td>{i}</td><td>{tier}</td><td>{k}</td><td>{u}</td><td>{pos}</td><td class="l">{I[k][3]}</td><td class="l">{hist}{(" <span class=r>("+lost+")</span>") if lost else ""}</td></tr>')
h.append('<h2 style="break-before:page">3. 개정 Top 40 요약표</h2><div>등급 S: 1학기 패턴상 출제 가능성 최상(최신 평가원·킬러·대표기출) / A: 2025 Level Up / B: 2025 유형 EBS</div><table><tr><th>순위</th><th>등급</th><th>문항</th><th>단원</th><th>예상 위치</th><th>출처</th><th>모의고사 출제(변형) 이력</th></tr>'+''.join(rows)+'</table>')
h.append('<h2 style="break-before:page">4. 문항</h2>')
for i,(k,tier,u,pos,why,var,key) in enumerate(T,1):
    q,ch,ans,srcs=I[k]
    chs=''
    if ch:
        chs='<div class="ch">'+''.join(f'<span>{CIRC[j]} '+(c[2:] if c.startswith('T:') else f'\\({c}\\)')+'</span>' for j,c in enumerate(ch))+'</div>'
    hist=', '.join(USE.get(k,[])) or '없음'
    lost=LOSTK.get(k,'')
    h.append(f'<div class="item"><div class="ihd">{i}. [{tier}] 부교재 {k} · {u}<span class="tag">예상 {pos}</span></div><div class="qb">{q}{chs}</div>'
             f'<div class="kv"><div class="k">출처</div><div class="v">{srcs}</div></div>'
             f'<div class="kv"><div class="k">선정 이유</div><div class="v">{why}</div></div>'
             f'<div class="kv"><div class="k">예상 변형</div><div class="v">{var}</div></div>'
             f'<div class="kv"><div class="k">내 이력</div><div class="v">{hist}{(" · <span class=r>"+lost+"</span>") if lost else ""}</div></div></div>')
h.append('<h2 style="break-before:page">5. 정답과 핵심</h2><table><tr><th style="width:7%">순위</th><th style="width:8%">문항</th><th style="width:9%">정답</th><th>핵심</th></tr>')
for i,(k,tier,u,pos,why,var,key) in enumerate(T,1):
    ans=I[k][2]
    core=key if key else (DD[k][2] if k in DD else '')
    h.append(f'<tr><td>{i}</td><td>{k}</td><td>{ans}</td><td class="l">{core}</td></tr>')
h.append('</table>')
html0=f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{"".join(h)}</body></html>'
html=re.sub(r'\\\\\[\d+pt\]', r'\\\\ ', html0)
_f=lambda m:m.group(0).replace('&lt;','<').replace('&gt;','>')
html=re.sub(r'\\\(.*?\\\)',_f,html,flags=re.S)
html=re.sub(r'\\\[.*?\\\]',_f,html,flags=re.S)
open(os.path.join(HERE,'top2_src.html'),'w').write(html)
subprocess.run(['node',os.path.join(HERE,'render3.js'),'top2_src.html','top2_tmp.pdf','bg'],cwd=HERE,check=True)
os.replace(os.path.join(HERE,'top2_tmp.pdf'),os.path.join(HERE,'top40_v2.pdf'))
