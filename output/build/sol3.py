# -*- coding: utf-8 -*-
import os, subprocess, sys
from content3 import Q, ANS
from build3 import font_css, KATEX_CSS, HERE

MAIN = '미적분1 (2).pdf'
def src(page, num, sec, tag):
    pdfp = page - 51 if page < 76 else page - 53
    return f'{MAIN} {sec} — 교재 {page}쪽(PDF {pdfp}쪽) {num}번 {tag}'

CIRC = '①②③④⑤'
# n: (풀이, 출처, 원본 난도, 변형 포인트, 변형 후 난도, 오답 근거)
D = {
1: (r"평균변화율 \(=\dfrac{f(3)-f(0)}{3}=8\), \(f'(x)=3x^2-1\)이므로 \(3c^2-1=8\), \(c^2=3\). \(0<c<3\)이므로 \(c=\sqrt3\).",
    src(53, 5, '유형1 미분계수', '[22009-0051] 2022 수능특강'), '하',
    '이차함수→삼차함수, 구간 [1,4]→[0,3], 답이 무리수가 되도록 재설계', '하',
    '① 범위 조건 무시 ② 상수항 미분 누락(3c²=8) ④ 구간 길이로 나누지 않음 ⑤ 제곱근 누락'),
2: (r"\(f'(x)=6x^2-2x+1\). 주어진 극한 \(=3f'(1)+f'(1)=4f'(1)=4\times5=20\).",
    src(57, 21, '유형3 도함수', '[24009-0054] 2024 수능특강'), '하',
    '접선의 기울기 식 변경, 증분 2h → 3h와 −h의 결합', '하',
    "① f'(1)만 ② 3f'(1)−f'(1)로 부호 오류 ③ 3f'(1)만 ⑤ 5f'(1)로 계산"),
3: (r"\(g'(x)=2xf(x)+x^2f'(x)-3\)이므로 \(g'(2)=4\times1+4\times3-3=13\).",
    src(69, 54, '평가원 기출', '2026학년도 6월 모의평가 7번 [3점]'), '하',
    '5x²+xf(x) → x²f(x)−3x, 기준점 3 → 2', '하',
    "① x²f'(x) 항 누락 ② 2xf(x) 항 누락 ④ −3 누락 ⑤ −3을 +3으로"),
4: (r"연속: \(1+a+b=b+2\)에서 \(a=1\). 미분계수: \(3+2a=b\)에서 \(b=5\). \(f(-1)=-1+1+5=5\), \(f(2)=12\)이므로 합은 \(17\).",
    src(69, 55, '평가원 기출', '2021학년도 9월 모의평가 나형 10번 [3점]'), '하',
    '왼쪽 식 x³+ax+b → x³+ax²+b, 오른쪽 상수 변경, 구하는 대상 a+b → f(−1)+f(2)', '하',
    '① f(−1)만 ② f(2)만 ③ 계수 계산 오류 ⑤ f(2)를 x<1의 식에 대입'),
5: (r"첫째 극한에서 \(f(0)+g(0)=0\), \(f'(0)+g'(0)=3\). 둘째 극한에서 \(f(0)=g(0)=0\)이어야 하고 극한값 \(\dfrac{2f'(0)+1}{g'(0)-1}=3\). 연립하면 \(f'(0)=1\), \(g'(0)=2\), 곱은 \(2\).",
    src(53, 6, '유형1 미분계수', '[25054-0130] 2025 수능완성'), '중하',
    '두 극한식의 형태 변경(합의 극한, f(2x)+x), 구하는 대상 합 → 곱', '중하',
    "① f'(0)만 ③ f'(0)+g'(0) ④ 2g'(0) ⑤ (f'(0)+g'(0))×g'(0)로 대상 혼동"),
6: (r"\(f'(-1)=3-2a=5\)에서 \(a=-1\). \(f(-1)=-1-1+2=0\)이므로 \(0=-5+b\), \(b=5\). \(a+b=4\).",
    src(78, 4, '접선의 방정식 유형1', '[24009-0076] 2024 수능특강'), '하',
    '사차함수 → 삼차함수, 접점 x=1 → x=−1', '하',
    '① a−b ② a만 ③ f(−1)=0을 답으로 ④ f(1)=2로 혼동'),
7: (r"ㄱ. 좌극한 \(\dfrac{x^2+2x}{x}\to2\), 우극한 \(\dfrac{-x^3+2x}{x}\to2\) (참). ㄴ. 좌미분계수 \(-1\), 우미분계수 \(0\) (거짓). ㄷ. \(f(1)=0\)이므로 \(\dfrac{\{f(x)\}^2}{x-1}=f(x)\cdot\dfrac{f(x)}{x-1}\to0\) (양쪽 모두) (참).",
    src(54, 11, '유형2 미분가능성과 연속', '[23054-0125] 2023 수능완성'), '중',
    '세 구간 식 재설계, ㄷ을 |f(x)| → {f(x)}²로 변경', '중',
    'ㄷ: 미분불가능한 함수의 제곱은 미분불가능하다고 착각 / ㄴ: 연속이면 미분가능하다고 착각'),
8: (r"\(f'(t)=\min(\text{높이},t)+(\text{높이}>t\text{인 구간의 길이})\). \(t=1\)(좌 \(2\), 우 \(1\)), \(t=2\)(좌 \(3\), 우 \(2\)), \(t=3\)(좌 \(3\), 우 \(2\))에서 미분가능하지 않으므로 합은 \(6\).",
    src(70, 57, '평가원 기출', '2014학년도 수능 예시문항 A형 21번 [4점]'), '중',
    '도형(계단·경사 위치) 새로 작도, 미분불가능점 2개 → 3개', '중',
    '① t=2만 ② t=1, 2만 ③ t=1, 3만(t=2 누락) ④ t=2, 3만(t=1 누락)'),
9: (r"\(4a^2x^2+4abx+b^2=(4a+8)x^2+(4b+4)x+4c-7\). \(a>0\)이므로 \(a=2\), \(b=1\), \(c=2\). \(f(2)=12\).",
    src(56, 17, '유형3 도함수(평가원)', '2019학년도 6월 모의평가 나형 17번 [4점]'), '중',
    '함수 형태 ax²+b → ax²+bx+c, 항등식 재구성, 조건 a>0 추가', '중',
    "① b 부호 오류 ② f'(2) ③ 상수항 누락 ⑤ 상수항 비교 오류"),
10: (r"\(x=y=0\)에서 \(f(0)=1\). \(f'(x)=\lim\dfrac{f(h)-1+3xh}{h}=f'(0)+3x\). \(f'(1)=5\)에서 \(f'(0)=2\), \(f'(-2)=-4\).",
    src(56, 19, '유형3 도함수', '[23009-0052] 2023 수능특강'), '중',
    '함수방정식 형태 변경, 주어진 값 f\'(1)', '중',
    "① f'(0) 누락 ③ 부호 오류 ④ f'(0)=5로 착각 ⑤ f'(0)만"),
11: (r"\(a>1\)이므로 \(x<1\)에서 \(f(x)>0\)이고 \(f(1)\ne0\) → \(f\)는 \(x=1\)에서 미분가능: \(b=2\), \(c=a-2\). \(x\ge1\)에서 \(f(x)=-(x-1)^2+a-1\)이 \(x=4\)에서 \(0\): \(a=10\), \(c=8\). \(f(-1)+f(3)=13+5=18\).",
    src(55, 14, '유형2 미분가능성과 연속', '[25054-0134] 2025 수능완성'), '중',
    '함수식·미분불가능점 재설계(조건 a>0 → a>1 유지), 구하는 대상 변경', '중',
    '② a+b+c ③ f(3)을 x<1의 식으로 ④ b 부호 오류 ⑤ 근 계산 오류'),
12: (r"극한이 존재하려면 \(f(1)=0\), \(f(x)=x(x-1)(x-k)\). \(\dfrac{f(x)}{x-1}\to1-k\), \(f'(1)=1-k\)이므로 극한값 \(\dfrac1{1-k}=-\dfrac12\), \(k=3\). \(f(4)=4\cdot3\cdot1=12\).",
    src(71, 60, '평가원 기출', '2018학년도 수능 나형 18번 [4점]'), '중',
    'f(1)=0 → f(0)=0, 극한 위치 2 → 1, 극한값 1/4 → −1/2', '중',
    '① f(3)(대상 혼동) ③ 극한을 1−k로 잘못 정리(k=3/2) ④ 극한값 부호 오류(k=−1) ⑤ k=−3'),
13: (r"\(x=2\)에서 미분가능 → \(f(2)=0\). 극한 존재 → \(f(0)=0\). \(f(x)=px(x-2)\), \(x\to0\)에서 \(\dfrac{g(x)}{x}=(2-x)p(x-2)\to-4p=8\), \(p=-2\). \(g(3)=1\cdot(-2)\cdot3\cdot1=-6\).",
    src(61, 35, 'Level Up', '[22009-0068] 2022 수능특강'), '중상',
    '|x+1| → |x−2|, 극한값 2 → 8, 구하는 대상 g(1) → g(3)', '중상',
    '① x=0에서 |x−2|=2를 빠뜨림(p=−4) ③ g(1) ④ |x−2|를 x−2로 처리(p=2) ⑤ ④의 결과를 2배'),
14: (r"\(f(x)=x^2+px+q\). 연속: \(f(1)=f(2)+f(1)\)이므로 \(f(2)=0\). 미분: \(f'(1)=f'(2)+f'(1)\)이므로 \(f'(2)=0\). 따라서 \(f(x)=(x-2)^2\), \(g(3)=f(4)+f(3)=4+1=5\).",
    src(61, 36, 'Level Up', '[24009-0071] 2024 수능특강'), '중상',
    'f(x+1)−f(x) → f(x+1)+f(x), 구하는 대상 f(2) → g(3)', '중상',
    '① f(3) ② g의 식 혼동 ④ f(4) ③ 계산 오류'),
15: (r"\(f(0)=3\), \(f'(0)=-12\). \(f'(x)=k(x-2)^2\)에서 \(4k=-12\), \(k=-3\). \(f(x)=-(x-2)^3+C\), \(f(0)=8+C=3\)에서 \(C=-5\). \(f(3)=-1-5=-6\).",
    src(63, 40, 'Level Up', '[21009-0068] 2021 수능특강'), '중상',
    '극한 조건에 상수항 추가(f(0)=3), 접점 (1,0) → (2,0), 구하는 대상 f(1) → f(3)', '중상',
    '② 상수 C 누락 ③ f(0)=3을 답으로 ④ k 부호 오류 시 구한 C ⑤ k 부호 오류(k=3)'),
16: (r"\(f\)는 \(x=-2\)(\(f=0\)), \(x=0\)(\(f(0)=2\))에서 미분불가능. \(x=-2\): \(g(-2)=0\). \(x=0\): 좌 \(g(0)+2g'(0)\), 우 \(-3g(0)+2g'(0)\)이므로 \(g(0)=0\). \(g(x)=x(x+2)\), \(g(4)=24\).",
    src(66, 46, 'Level Up', '[25009-0074] 2025 수능특강'), '상',
    '|x+1|, 3x+1 → |x+2|, 2−3x', '상',
    '① g(2) ② g(3) ③ 원본 결과식 x(x+1) 사용 ④ g(0)=0 누락'),
17: (r"\(x<0\): \(\mathrm{PA}^2=2x^2+8x+10\), \(\mathrm{PB}^2=2x^2-4x+4\) → \(x=-\tfrac12\)에서 교차. \(0\le x<2\): \(\mathrm{PB}^2\) 선택, \(x=0\) 양쪽 식이 같아 미분가능. \(x\ge2\): \(\mathrm{PB}^2\), \(x=2\)에서 좌 \(4\), 우 \(-4\). \(p=\tfrac32\), \(10p=15\).",
    src(74, 65, '평가원 기출', '2017학년도 6월 모의평가 나형 29번 [4점]'), '상',
    '두 구간 → 세 구간 함수, 점 A, B 변경, 80p → 10p', '상',
    '② 교차점 x=−1/2 누락 ③ 교차점 부호 오류 ④ 정의역 밖 x=3/2 포함 ⑤ ③과 ④의 오류를 함께 범함'),
18: (r"\(f'(x)=4\Leftrightarrow 4(x+1)(x-1)(x-3)=0\). 미분가능 조건 \(f'(p)=f'(p-a)\), \(a<0\)이므로 \((p,\,p-a)\)는 \((-1,1),(-1,3),(1,3)\). \(b=f(p)-f(p-a)\): \(a-b=22,\ 12,\ -10\). 최댓값과 최솟값의 합 \(12\).",
    f'외부 문항: 2026_대비_EBS_봉투_모의고사_수학_3회.pdf 15번 [25393-0107] (4점)', '상',
    '사차함수 재설계(f\'(x)=4의 해 −1, 1, 3), 원본의 구조(a<0, a−b의 최댓값·최솟값의 합) 유지', '상',
    '① b 부호 반대(b=f(p−a)−f(p)) ② (−1,1) 경우 누락 ④ 최댓값만 ⑤ (1,3) 경우 누락'),
}
S1 = dict(
    ans=['(1) a = −3', '(2) l₁: 7, l₂: −25', '(3) −18'],
    sol=[r"(1) 거리가 일정 → \(l_1\parallel l_2\). \(f'(-1)=f'(3)\): \(3-2a+b=27+6a+b\), \(a=-3\). ------ [3점]",
         r"(2) \(m=f'(-1)=9+b\), \(f(-1)=-2-b\), \(f(3)=3b+2\). \(l_1: y=m(x+1)-2-b\)의 \(y\)절편 \(7\), \(l_2: y=m(x-3)+3b+2\)의 \(y\)절편 \(-25\). ------ [각 1.5점]",
         r"(3) \(\mathrm T\left(-\tfrac7m,0\right)\), \(\mathrm S\left(\tfrac{25}m,0\right)\), \(\overline{\mathrm{TS}}=\tfrac{32}{|m|}=8\) ------ [2점]  \(|m|=4\), \(b=-5\) 또는 \(-13\), 합 \(-18\) ------ [2점]"],
    src='외부 문항: 2026학년 EBS 만점 마무리 시즌2 1~3회.pdf 제3회 13번 [25412-0105] (4점)',
    var='원본(접점 0, 2, 거리 → TS)을 접점 −1, 3으로 바꾸고 (1) 평행 조건 → (2) y절편 → (3) TS 조건으로 b 결정의 단계형으로 재구성')
S2 = dict(
    ans=['(1) 4', '(2) h(x) = (x−α)²(x−α−6)', '(3) 72'],
    sol=[r"(1) \(g'(x)=-2x+p\)이므로 \(g'(\alpha)-g'(\beta)=-2(\alpha-\beta)=8\), \(\beta-\alpha=4\). ------ [2점]",
         r"(2) \(h(\alpha)=0\), \(h'(\alpha)=0\)이므로 \(h(x)=(x-\alpha)^2(x-\gamma)\) ------ [1점]. \(h'(x)=(x-\alpha)(3x-\alpha-2\gamma)\) ------ [1점], \(h'(\beta)=0\), \(\beta\ne\alpha\)이므로 \(\gamma=\tfrac{3\beta-\alpha}2=\alpha+6\) ------ [1점]. \(h(x)=(x-\alpha)^2(x-\alpha-6)\) ------ [1점]",
         r"(3) 교점의 \(x\)좌표 \(\alpha,\ \alpha+6\) ------ [1점]. \(g\)의 축이 \(x=\alpha+3\)이므로 \(g(\alpha)=g(\alpha+6)\), \(\overline{\mathrm{PQ}}=6\) ------ [1점]. \(h(\beta)=16\cdot(-2)=-32\), \(g(\beta)-g(\alpha)=8\)이므로 높이 \(24\) ------ [1점]. 넓이 \(\tfrac12\cdot6\cdot24=72\) ------ [1점]"],
    src=src(73, 64, '평가원 기출', '2018학년도 6월 모의평가 나형 30번 [4점]'),
    var='계수 2 → −1, 미분계수 ∓16 → 6, −2, 결론 g(β+1)−f(β+1) → 단계형 서술(관계식 도출, 대칭성을 이용한 넓이)')

PTS = {n: Q[n][0] for n in Q}
CSS = r"""
@page{size:A4;margin:16mm 14mm 16mm 14mm}
body{font-family:'HB','MJ','GL',serif;font-size:9.3pt;line-height:1.6;margin:0}
.katex{font-size:1.02em;font-family:'TN','KaTeX_Main'}
.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
.katex .text,.katex .text *{font-family:'HB','MJ','TN'!important;font-style:normal}
.katex .mord,.katex .mbin,.katex .mrel,.katex .mpunct,.katex .mopen,.katex .mclose,.katex .mop{font-family:'TN','KaTeX_Main'}
h1{font-family:'HB','GL';font-weight:700;font-size:15pt;margin:0 0 2mm;letter-spacing:1pt}
.dot{border-bottom:1.2pt dotted #000;width:60%;margin-bottom:3mm}
.meta{font-size:9pt;margin-bottom:5mm}
table{border-collapse:collapse;width:100%}
td,th{border:.6pt solid #000;padding:1.5pt 2pt;text-align:center;font-weight:400}
.big td,.big th{font-size:8.6pt}
.big{border:1.6pt solid #000}
.rub td{text-align:left;padding:4pt 6pt;vertical-align:top}
.rub td.lab{text-align:center;width:16mm;vertical-align:middle}
h2{font-family:'GL';font-size:11pt;margin:7mm 0 2mm;border-bottom:1.2pt solid #000;padding-bottom:1mm}
.p{border:.6pt solid #000;margin:0 0 3mm;break-inside:avoid}
.p .hd{background:#eee;border-bottom:.6pt solid #000;padding:1.5pt 5pt;font-weight:700}
.p .r{display:flex;border-top:.4pt solid #aaa}.p .r:first-of-type{border-top:0}
.p .k{flex:none;width:19mm;padding:2pt 4pt;font-family:'GL';font-size:8.3pt;border-right:.4pt solid #aaa;background:#fafafa}
.p .v{flex:1;padding:2pt 5pt}
"""

def build(out):
    head = ''.join(f'<th>{n}</th>' for n in range(1, 19))
    pts = ''.join(f'<td>{PTS[n]:.1f}</td>' for n in range(1, 19))
    ans = ''.join(f'<td>{CIRC[ANS[n]-1]}</td>' for n in range(1, 19))
    h = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>']
    h.append('<h1>2학년 (미적분Ⅰ) 과 문제 정답 및 채점기준</h1><div class="dot"></div>'
             '<div class="meta">시험일자 2026 년 &nbsp;&nbsp;7 월 &nbsp;11 일 &nbsp;&nbsp;&nbsp; 1 교시</div>')
    h.append('<table class="big"><tr><th rowspan="2">학년</th><th rowspan="2">과정</th><th rowspan="2">과목<br>코드</th><th rowspan="2">과목명</th>'
             '<th rowspan="2">이수<br>학점</th><th rowspan="2">문항<br>수</th><th rowspan="2">선택<br>형<br>점수</th><th rowspan="2">서답<br>형<br>점수</th>'
             f'<th>번호</th>{head}</tr><tr><th>배점</th>{pts}</tr>'
             '<tr><td rowspan="2">2</td><td rowspan="2">2022<br>개정</td><td rowspan="2">09</td><td rowspan="2">미적분Ⅰ</td><td rowspan="2">4</td>'
             '<td>18</td><td rowspan="2">80</td><td rowspan="2">20</td>'
             f'<th>정답</th>{ans}</tr><tr><td>2</td><td colspan="19"></td></tr></table>')
    def rub(lab, d):
        return (f'<tr><td class="lab">서답형<br>{lab}<br>[10점]</td><td>' + '<br>'.join(d['sol']) +
                '<br><b>정답</b> ' + ' / '.join(d['ans']) + '</td></tr>')
    h.append('<table class="rub" style="margin-top:4mm">' + rub('1', S1) + rub('2', S2) + '</table>')
    h.append('<div style="font-size:8.3pt;margin-top:2mm">※ 서답형은 결과만 쓰고 근거가 없으면 해당 단계 점수를 주지 않는다. 계산 실수로 최종값만 틀린 경우 마지막 단계 점수만 감점한다.</div>')
    h.append('<h2>문항별 상세 해설 · 출처 · 난도</h2>')
    for n in range(1, 19):
        sol, so, d0, var, d1, wr = D[n]
        c = Q[n][2][ANS[n]-1]
        ct = c[2:] if c.startswith('T:') else f'\\({c}\\)'
        h.append(f'<div class="p"><div class="hd">{n}번 &nbsp; 정답 {CIRC[ANS[n]-1]} {ct} &nbsp; [{PTS[n]:.1f}점]</div>'
                 f'<div class="r"><div class="k">풀이</div><div class="v">{sol}</div></div>'
                 f'<div class="r"><div class="k">원본 출처</div><div class="v">{so}</div></div>'
                 f'<div class="r"><div class="k">난도</div><div class="v">원본 {d0} → 변형 후 {d1}</div></div>'
                 f'<div class="r"><div class="k">변형 포인트</div><div class="v">{var}</div></div>'
                 f'<div class="r"><div class="k">오답 설계</div><div class="v">{wr}</div></div></div>')
    for lab, d, nn in [('서답형 1 (19번)', S1, '중상 → 중상'), ('서답형 2 (20번)', S2, '상 → 상')]:
        h.append(f'<div class="p"><div class="hd">{lab}</div>'
                 f'<div class="r"><div class="k">원본 출처</div><div class="v">{d["src"]}</div></div>'
                 f'<div class="r"><div class="k">난도</div><div class="v">원본 {nn}</div></div>'
                 f'<div class="r"><div class="k">변형 포인트</div><div class="v">{d["var"]}</div></div></div>')
    h.append('</body></html>')
    src_html = os.path.join(HERE, 'sol_src.html')
    open(src_html, 'w').write(''.join(h))
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'sol_src.html', 'sol_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'sol_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
