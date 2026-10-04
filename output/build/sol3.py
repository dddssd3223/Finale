# -*- coding: utf-8 -*-
import os, subprocess, sys
from content3 import Q, ANS
from sold import make
from build3 import font_css, KATEX_CSS, HERE

MAIN = '미적분1 (2).pdf'
def src(page, num, sec, tag):
    pdfp = page - 51 if page < 76 else page - 53
    return f'{MAIN} {sec} — 교재 {page}쪽(PDF {pdfp}쪽) {num}번 {tag}'

CIRC = '①②③④⑤'
# n: (풀이, 출처, 원본 난도, 변형 포인트, 변형 후 난도, 오답 근거)
D = make(src)
D[18] = (r"\(x=0\)에서 연속: \(|b|=b^2\)이므로 \(b\in\{0,\,1,\,-1\}\). \(b=1\)이면 \(x=0\)에서 미분가능 조건(좌 \(a\), 우 \(2a\))으로 \(a=0\), \(g\)가 모든 점에서 미분가능하여 (가)에 모순. \(b=0\)이면 \(a\ne0\)이어야 하는데 \(a>0\)이면 \(x=-a\)에서도 미분불가능, \(a<0\)이면 \(x\le0\)에서 \(g(x)=ax\)로 (나)에 모순. \(b=-1\): 좌미분계수 \(-a\), 우미분계수 \(2f(0)f'(0)=-2a\)이므로 \(a=0\). \(f(x)=x^2-1\), \(x=-1\)에서만 미분불가능, \(1-2x^2=0\)에서 음의 실근 존재. \(g(-\tfrac12)+g(2)=\tfrac12+25=\tfrac{51}2\).",
    '외부 문항: 261003_수능&모의 공통_원본.pdf — 2025학년도 7월 고3 학력평가 15번 [4점]', '상',
    'x>0의 식 {f(x)}²+x³ → {f(x)}²+2x³, 구하는 대상 g(−1/2)+g(3) → g(−1/2)+g(2)', '상',
    "① 2x³을 x³으로 계산(17) ② x≤0에서 절댓값 누락(g(−1/2)=−1) ④ −x²을 +x²으로 처리(g(−1/2)=1) ⑤ (가)를 무시하고 b=1로 처리")

S1 = dict(
    ans=['(1) f(k) = 4k²', "(2) f'(k) = 8k, f(x) = (x²−t²)² + 4x²", '(3) 113'],
    sol=[r"(1) 좌변의 극한이 존재하므로 \(4k^2f(k)-\{f(k)\}^2=0\) ------ [1점]. \(f(x)\)의 최솟값이 \(32\)이므로 \(f(k)>0\) ------ [1점], \(f(k)=4k^2\) ------ [1점]",
         r"(2) 양변은 각각 \(\{4x^2f(x)\}'\), \(\{f(x)^2\}'\)의 \(x=k\)에서의 값: \(8kf(k)+4k^2f'(k)=2f(k)f'(k)\) ------ [1점]. \(f(k)=4k^2\) 대입, \(k\ne0\)이므로 \(f'(k)=8k\) ------ [1점]. \(h(x)=f(x)-4x^2\)은 최고차항의 계수가 \(1\)인 사차함수이고 \(h(\pm t)=h'(\pm t)=0\) ------ [1점], \(f(x)=(x^2-t^2)^2+4x^2\) ------ [1점]",
         r"(3) \(f'(x)=4x(x^2-t^2+2)\), \(x^2=t^2-2\)에서 최솟값 \(4t^2-4=32\) ------ [1점], \(t=3\) ------ [1점], \(f(4)=49+64=113\) ------ [1점]"],
    src='외부 문항: 261003_수능&모의 공통_원본.pdf — 2025학년도 10월 고3 학력평가 21번 [4점]',
    var='2x²f(x) → 4x²f(x), 조건 t>1 → t>2, 최솟값 17 → 32, 단답형 → (1) f(k) (2) f\'(k)와 f(x) (3) f(4)의 단계형 서술')
S2 = dict(
    ans=['(1) f(x) = x³ + bx² + 16x + 3', '(2) A(0, 3), B와 C의 x좌표: 2, 8 또는 −2, −8', '(3) 30'],
    sol=[r"(1) (가)에서 \(f(x)\)는 최고차항의 계수가 \(1\)인 삼차함수 ------ [1점]. (나)에서 \(f(0)=3\), \(f'(0)=16\)이므로 \(f(x)=x^3+bx^2+16x+3\) ------ [1점]",
         r"(2) \(f(x)=3\iff x(x^2+bx+16)=0\) ------ [1점]. \(x=0\)인 점이 원점에 가장 가까우므로 \(\mathrm A(0,\,3)\) ------ [1점]. \(\mathrm B\), \(\mathrm C\)의 \(x\)좌표 \(\beta\), \(\gamma\)는 \(\beta\gamma=16\), \(\beta=\tfrac{\gamma}4\) ------ [1점]. \((\beta,\,\gamma)=(2,\,8)\) 또는 \((-2,\,-8)\) ------ [1점]",
         r"(3) \(b=-(\beta+\gamma)=-10\) 또는 \(10\) ------ [2점]. \(f(1)=20+b\)이므로 최댓값 \(30\) ------ [2점]"],
    src=src(65, 44, 'Level Up', '[24009-0075] 2024 수능특강'),
    var='최고차항 계수 2 → 1, f\'(0)=24 → 16, 직선 y=2 → y=3, 내분비 1:2 → 1:3, 단답형 → 단계형 서술')

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
    for lab, d, nn in [('서답형 1 (19번)', S1, '상 → 상'), ('서답형 2 (20번)', S2, '중상 → 중상')]:
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
