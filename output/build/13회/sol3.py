# -*- coding: utf-8 -*-
import os, subprocess, sys
from content3 import Q, ANS
from sold import make, s2
from build3 import font_css, KATEX_CSS, HERE

MAIN = '미적분1 (2).pdf'
def src(page, num, sec, tag):
    pdfp = page - 51 if page < 76 else page - 53
    return f'{MAIN} {sec} — 교재 {page}쪽(PDF {pdfp}쪽) {num}번 {tag}'

CIRC = '①②③④⑤'
# n: (풀이, 출처, 원본 난도, 변형 포인트, 변형 후 난도, 오답 근거)
D = make(src)

S1 = dict(
    ans=['(1) 2', '(2) −4', '(3) 77'],
    sol=[r"(1) \(x=0\)에서 연속: \(-f(0)=|f(0)|-4\). \(f(0)<0\)이면 불가능하므로 \(f(0)=2\). 정답 \(2\) ------ [3점]",
         r"(2) \(x=0\)에서 미분가능하므로 \(-f'(0)=f'(0)\), \(f'(0)=0\). \(|x^2-4|\)는 \(x=2\)에서 꺾이므로 \(|f|\)도 꺾여 상쇄: \(f(2)=0\), \(|f'(2)|=4\). \(f=Ax^3+Bx^2+2\)에서 \(f'(2)=4\)이면 \(f=\tfrac12(x-2)(x-1)(3x+2)\)로 \(x=1\)에서 \(|f|\)가 꺾여 불가. \(f'(2)=-4\). 정답 \(-4\) ------ [3점]",
         r"(3) \(f=-\tfrac12(x-2)(x^2+x+2)\), \(f(-5)=-\tfrac12\cdot(-7)\cdot22=77\). 정답 \(77\) ------ [4점]"],
    src='외부 문항: 261003_수능&모의 공통_원본.pdf — 2025학년도 3월 고3 학력평가 22번 [4점]',
    var="|2x²−8| → |x²−4|, 단답형 3단계(f(0), f′(2), f(−5))")
S2 = dict(
    ans=['(1) 4', '(2) 증명', '(3) 117'],
    sol=[r"(1) \(x=2\)에서 좌극한 \((a_1+1)\cdot2+4\), 함숫값 \((2a_2+1)\cdot2+12\). 같다고 두면 \(a_1-2a_2=4\) ------ [2점]",
         r"(2) \(x=k+1\)에서 좌극한 \((ka_k+1)(k+1)+2k(k+1)\) ------ [1점], 함숫값 \(\{(k+1)a_{k+1}+1\}(k+1)+2(k+1)(k+2)\) ------ [1점]. 같다고 두고 \(k+1\)로 나누면 \(ka_k+2k=(k+1)a_{k+1}+2k+4\), \(ka_k-(k+1)a_{k+1}=4\) ------ [2점]",
         r"(3) \(b_k=ka_k\)라 하면 \(b_k=b_{k+1}+4\), \(b_6=36\) ------ [1점]. \(b_5=40\), \(b_4=44\), \(b_3=48\), \(b_2=52\), \(b_1=56\) ------ [1점]. \(a_n=\dfrac{b_n}n\): \(56+26+16+11+8=117\) ------ [2점]"],
    src=s2('02 함수의 연속', 26),
    var='상수항 k(k+1) → 2k(k+1), a₆=8 → 6, 단계형 서술(관계식 → 일반화 → 합)')

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
             '<div class="meta">시험일자 2026 년 &nbsp;&nbsp;10 월 &nbsp;13 일 &nbsp;&nbsp;&nbsp; 1 교시</div>')
    h.append('<table class="big"><tr><th rowspan="2">학년</th><th rowspan="2">과정</th><th rowspan="2">과목<br>코드</th><th rowspan="2">과목명</th>'
             '<th rowspan="2">이수<br>학점</th><th rowspan="2">문항<br>수</th><th rowspan="2">선택<br>형<br>점수</th><th rowspan="2">서답<br>형<br>점수</th>'
             f'<th>번호</th>{head}</tr><tr><th>배점</th>{pts}</tr>'
             '<tr><td rowspan="2">2</td><td rowspan="2">2022<br>개정</td><td rowspan="2">09</td><td rowspan="2">미적분Ⅰ</td><td rowspan="2">4</td>'
             '<td>18</td><td rowspan="2">80</td><td rowspan="2">20</td>'
             f'<th>정답</th>{ans}</tr><tr><td>2</td><td colspan="19"></td></tr></table>')
    def rub(lab, d):
        return (f'<tr><td class="lab">{lab.replace(" ", "<br>")}<br>[10점]</td><td>' + '<br>'.join(d['sol']) +
                '<br><b>정답</b> ' + ' / '.join(d['ans']) + '</td></tr>')
    h.append('<table class="rub" style="margin-top:4mm">' + rub('단답형 1', S1) + rub('서술형 1', S2) + '</table>')
    h.append('<div style="font-size:8.3pt;margin-top:2mm">※ 단답형은 정답만 채점한다(소문항별 부분 점수). 서술형은 결과만 쓰고 근거가 없으면 해당 단계 점수를 주지 않으며, 계산 실수로 최종값만 틀린 경우 마지막 단계 점수만 감점한다.</div>')
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
    for lab, d, nn in [('단답형 1 (19번)', S1, '중상 → 중'), ('서술형 1 (20번)', S2, '중상 → 중상')]:
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
