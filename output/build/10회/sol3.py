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
    ans=['(1) 1/3', '(2) 1', '(3) 31'],
    sol=[r"(1) \(f=g\)인 점 \(\alpha\)에서 좌우 극한값은 \(2g(\alpha)\)와 \(0\)이므로 \(g(\alpha)\ne0\)인 교점에서 좌우극한이 다르다. (나)에서 \(|h-1|\)의 극한이 존재하려면 그 점에서 \(|2g(\alpha)-1|=|0-1|\), \(g(\alpha)=1\). \(\alpha=2\)이므로 \(\tfrac23+a=1\), \(a=\tfrac13\). 정답 \(\tfrac13\) ------ [3점]",
         r"(2) 다른 교점에서는 좌우극한이 같아야 하므로 \(g=0\): \(x=-1\). 두 근의 합 \(2+(-1)=1\). 정답 \(1\) ------ [3점]",
         r"(3) \(f-g=c(x-2)(x+1)\), \(h(0)=g(0)-f(0)=2c=3\), \(c=\tfrac32\). \(h(5)=2g(5)+(f-g)(5)=4+27=31\). 정답 \(31\) ------ [4점]"],
    src='외부 문항: 261003_수능&모의 공통_원본 (1).pdf — 2025학년도 9월 고2 학력평가 30번 [4점]',
    var="h(0)=7/3 → 3, 단답형 3단계(a, 두 근의 합, h(5))")
S2 = dict(
    ans=['(1) f(1)=3, f(4)=9', '(2) 0 < p < (4+2√3)/3', '(3) 10'],
    sol=[r"(1) \(x=1\), \(x=4\)에서 연속이므로 \(\dfrac1{f(1)}=\dfrac13\), \(\dfrac1{f(4)}=\dfrac19\): \(f(1)=3\), \(f(4)=9\) ------ [1점]. \(f(x)-(2x+1)\)은 \(x=1,4\)를 근으로 갖는 이차식이므로 \(f=p(x-1)(x-4)+2x+1\), \(p>0\) ------ [1점]",
         r"(2) \([1,4]\)에서 \(\dfrac1f\)가 연속이려면 \(f>0\) ------ [1점]. \(f=px^2+(2-5p)x+4p+1\)의 판별식 \(9p^2-24p+4<0\)이면 항상 양수: \(\tfrac{4-2\sqrt3}3<p<\tfrac{4+2\sqrt3}3\) ------ [1점]. \(p\le\tfrac{4-2\sqrt3}3\)이면 축 \(x=\tfrac52-\tfrac1p<1\)이고 \(f(1)>0\)이라 \([1,4]\)에서 양수 ------ [1점]. \(p\ge\tfrac{4+2\sqrt3}3\)이면 축이 \([1,4]\) 안에 있고 최솟값 \(\le0\)이라 불가. 따라서 \(0<p<\tfrac{4+2\sqrt3}3\) ------ [1점]",
         r"(3) \(k=f(0)=4p+1<\dfrac{19+8\sqrt3}3=10.9\cdots\) ------ [2점]. 자연수 \(k\)의 최댓값 \(10\) (\(p=\tfrac94\)) ------ [2점]"],
    src=s2('02 함수의 연속', 8),
    var='1/2, 1/6 → 1/3, 1/9, 구간 [1,3] → [1,4], 단계형 서술')

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
    for lab, d, nn in [('단답형 1 (19번)', S1, '중상 → 중상'), ('서술형 1 (20번)', S2, '중상 → 중상')]:
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
