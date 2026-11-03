# -*- coding: utf-8 -*-
import os, subprocess, sys
from content3 import Q, ANS
from build3 import font_css, KATEX_CSS, HERE

sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F
from content3 import RAW, SA_ANS, SRC_S
CIRC = '①②③④⑤'
LV = {1: '하', 2: '하', 3: '하', 4: '중하', 5: '중', 6: '중상', 7: '상', 8: '최상', 9: '최상'}
SOL = {
1: (r"접점 \(t\): \(6=-t(3t^2-2)+t^3-2t+4\), \(t^3=-1\), \(t=-1\). 접선 \(y=x+6\) → \(x\)절편 \(-6\).", "접점의 \(x\)좌표 \(-1\)을 답으로"),
2: (r"\(f'=3x(x-2)\): \(m=f(2)=a-4\), \(M=f(5)=a+50\) (\(f(1)=a-2\)). \(2a+46=50\), \(a=2\).", "\(M=f(1)\)로 착각"),
3: (r"\(a^3-a^2-6a=a(a-3)(a+2)=0\), 양수 \(a=3\).", "음수 해 \(-2\)의 절댓값"),
4: (r"\(x^2(x-3)=0\)에서 \(0\), \(3\). \(\displaystyle\int_0^3(3x^2-x^3)\,dx=27-\tfrac{81}4=\tfrac{27}4\).", "부호 처리 실수"),
5: (r"(가)(나)에서 \(f'(0)=b=0\). \(f'=-x(3x-2a)\ge0\) \((-2&lt;x&lt;0)\) → \(\tfrac{2a}3\le-2\), \(a\le-3\). \(f(-2)=8+4a\le-4\).", "증가 구간 끝점 미반영"),
6: (r"\(x^3+3x^2-9x-8=a\). 극댓값 \(19\)(\(x=-3\)), 극솟값 \(-13\)(\(x=1\)) → \(-13&lt;a&lt;19\). 근의 곱 \(8+a&gt;0\) → \(a&gt;-8\). \(-7+18=11\).", "곱 조건 누락 시 \(-12+18=6\)"),
7: (r"\(x=1\): \(a+b+2=0\). 미분 \((x-1)f(x)=4ax^3+2bx\), \(x=1\): \(4a+2b=0\) → \(a=2\), \(b=-4\). \(f=8x^2+8x\), 최솟값 \(f(-\tfrac12)=-2\).", "\(a\), \(b\) 부호 착오"),
8: (r"\(a=f'(0)=4\). \(g-f=-x^3+4x^2=x^2(4-x)\) → \(\displaystyle\int_0^4(4x^2-x^3)\,dx=\tfrac{64}3\).", "접점(중근) 처리 누락"),
9: (r"\(f'=3(x-3a)(x+a)\), 극댓값 \(f(-a)=5a^3+2=7\) → \(a=1\). \(f(2)=8-12-18+2=-20\).", "극솟값으로 접선 처리"),
10: (r"\(-a=3x^3-9x=k(x)\): \(k(-2)=-6\), \(k(-1)=6\), \(k(1)=-6\). 서로 다른 두 실근 ⇔ \(-6\le-a&lt;6\) → \(a=-5,\,\cdots,\,6\) (12개).", "끝점 포함 여부 착오"),
11: (r"\(x=0\): \(\int_0^1f=2a\). \(x=1\): \(f(1)=2+3a\). 조건에서 \(a=-2\). 미분: \(xf'=6x^2+2ax\) → \(f=3x^2-4x+C\), \(f(1)=-4\)에서 \(C=-3\). \(f(3)=12\), 합 \(10\).", "\(f(3)\)만 답으로"),
12: (r"두 곡선은 \(x=0,\,1\)에서 만남(\(0\le x\le1\)). 넓이 \(\int_0^1(-2x^3+x^2+x)\,dx=\tfrac13\). \(\int_0^1\{ax(1-x)-(x^3-x^2)\}dx=\tfrac a6+\tfrac1{12}=\tfrac16\) → \(a=\tfrac12\).", "위 곡선 기준으로 계산"),
13: (r"(가) \(b=0\). \(f'=x(x^2-9x+2a)\ge0\) \((x&gt;0)\) → \(\tfrac{81}4-\tfrac{81}2+2a\ge0\), \(a\ge\tfrac{81}8\). \(f'(1)=2a-8\ge\tfrac{49}4\).", "판별식 \(&lt;0\)으로 범위 설정"),
14: (r"\(v=2t^3-8t+10-m\). \(h(t)=2t^3-8t+10\)의 \(t&gt;0\) 극솟값 \(10-\tfrac{32}{3\sqrt3}\approx3.84\), \(h(0)=10\). 부호 두 번 변화 ⇔ \(3.84&lt;m&lt;10\) → \(m=4,\cdots,9\), 합 \(39\).", "\(m=10\) 포함"),
15: (r"(가) \(f'(f'-2x-1)=0\), 상수함수 아님 → \(f'=2x+1\), \(f=x^2+x+C\). (나) \(\int_2^3f=\tfrac{19}3+\tfrac52+C=0\) → \(C=-\tfrac{53}6\). \(f(2)=6-\tfrac{53}6=-\tfrac{17}6\).", "적분 구간을 \([0,1]\)로"),
16: (r"\(v=3(t-1)(t-3)\): ㄱ 참. \(x(t)=t^3-6t^2+9t\), \(x(1)=4\): ㄴ 참. 거리 \(4+|0-4|+|4-0|=12\): ㄷ 거짓.", "ㄷ을 변위로 계산"),
17: (r"\(x\le3\): \(x(x-3)^2=tx\) ⇔ \(x=0\) 또는 \((x-3)^2=t\) → \(t&lt;0\)이면 \(1\)개, \(t&gt;0\)이면 \(2\)개(\(t=9\)이면 \(1\)개지만 좌·우극한은 같음). \(x&gt;3\): \(t&gt;0\)이면 항상 \(1\)개. \(t&lt;0\)이면 원점에서 그은 접선의 기울기 \(t_0=-a(\sqrt b-\sqrt3)^2\) (접점 \(x=\sqrt{3b}&gt;3\), \(b&gt;3\))보다 크면 \(2\)개 → \(g\)는 \(t_0\)에서 \(1\to3\). \(b\le3\)이면 \(t=0\)에서만 \(1\to3\). 따라서 \(a(\sqrt b-\sqrt3)^2=12\): \(3b\)가 제곱수, \(b=3m^2\), \(3a(m-1)^2=12\) → \((4,12)\), \((1,27)\). 합 \(16+28=44\).", r"\(b\le3\)인 경우(점프가 \(t=0\))를 넣거나 \(t=9\)를 불연속으로 셈"),
18: (r"\(h'=g-f\): \(x\ge0\)에서 \(x(1-x)\), \([-1,0)\)에서 \(x^2\), \(x&lt;-1\)에서 \(x^2+ax+a\). \(a\le4\)이면 \(h\)는 \(x=1\)에서만 극대 → 실근 \(0,\ \tfrac32\) 두 개. \(a&gt;4\)이면 \(x&lt;-1\)에 극대 \(r\), 극소 \(s\) (\(h(s)&lt;h(0)=0\)) → 실근 3개 ⇔ \(h(r)=0\). \(\int_r^{-1}(x^2+ax+a)\,dx+\tfrac13=0\) ⇔ \(2r^3+3a(r+1)^2=0\), \(a=-\tfrac{r^2}{r+1}\) → \(r^2(r+3)=0\), \(r=-3\), \(a=\tfrac92\). 실근 \(-3,\ 0,\ \tfrac32\), 합 \(-\tfrac32\).", r"\(x&gt;1\)의 실근 \(\tfrac32\)를 빠뜨리거나 극소점이 접한다고 봄"),
}
import re as _re
_fx=lambda s: _re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;','<').replace('&gt;','>'), s)
D = {n: (_fx(SOL[n][0]), f"부교재 {F.I[r[3]][3]} — {r[3]} ({F.D[r[3]][1]})", LV[F.D[r[3]][0]], r[5], r[6], SOL[n][1]) for n, r in RAW.items()}
from content3 import S1S, S2S
S1 = dict(ans=['(1) 6', '(2) 21'],
    sol=[r"(1) 주기가 \(3\)이므로 \(\int_{-3}^6f=3\int_0^3f=18\) ------ [3점], \(\int_0^3f=6\) ------ [1점]",
         r"(2) 우함수·주기 3: \(\int_0^3f=\int_{-3/2}^{3/2}f=2\int_0^{3/2}f\) → \(\int_0^{3/2}f=3\) ------ [3점]. \(\tfrac{21}2=3\times3+\tfrac32\) → \(3\times6+3=21\) ------ [3점]"],
    src=f"부교재 {SRC_S['S1'][1]} — I20", var=SRC_S['S1'][2])
from content3 import _S2
S2 = dict(ans=_S2['ans'], sol=_S2['rubric'] + ([r"빠른 풀이: " + _S2['fast']] if _S2.get('fast') else []) + ([r"원본 대비: " + _S2['note']] if _S2.get('note') else []),
    src=f"부교재 {SRC_S['S2'][1]} — {SRC_S['S2'][0]}", var=SRC_S['S2'][2])

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
             '<div class="meta">기말고사 1회 · 시험일자 2026 년 &nbsp;&nbsp;12 월 &nbsp;○○ 일 &nbsp;&nbsp;&nbsp; 1 교시</div>')
    h.append('<table class="big"><tr><th rowspan="2">학년</th><th rowspan="2">과정</th><th rowspan="2">과목<br>코드</th><th rowspan="2">과목명</th>'
             '<th rowspan="2">이수<br>학점</th><th rowspan="2">문항<br>수</th><th rowspan="2">선택<br>형<br>점수</th><th rowspan="2">서답<br>형<br>점수</th>'
             f'<th>번호</th>{head}</tr><tr><th>배점</th>{pts}</tr>'
             '<tr><td rowspan="2">2</td><td rowspan="2">2022<br>개정</td><td rowspan="2">09</td><td rowspan="2">미적분Ⅰ</td><td rowspan="2">4</td>'
             '<td>18</td><td rowspan="2">80</td><td rowspan="2">20</td>'
             f'<th>정답</th>{ans}</tr><tr><td>2</td><td colspan="19"></td></tr></table>')
    def rub(lab, d):
        return (f'<tr><td class="lab">{lab.replace(" ", "<br>")}<br>[10점]</td><td>' + '<br>'.join(d['sol']) +
                '<br><b>정답</b> ' + ' / '.join(d['ans']) + '</td></tr>')
    h.append('<table class="rub" style="margin-top:4mm">' + rub('서답형 1', S1) + rub('서답형 2', S2) + '</table>')
    h.append('<div style="font-size:8.3pt;margin-top:2mm">※ 서답형 1은 풀이 과정을 채점한다(근거 없이 결과만 쓰면 해당 단계 점수 없음). 서답형 2는 답만 채점한다(소문항별 점수).</div>')
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
    for lab, d, nn in [('서답형 1 (19번)', S1, '하 → '+SRC_S['S1'][3]), ('서답형 2 (20번)', S2, '최상 → '+SRC_S['S2'][3])]:
        h.append(f'<div class="p"><div class="hd">{lab}</div>'
                 f'<div class="r"><div class="k">원본 출처</div><div class="v">{d["src"]}</div></div>'
                 f'<div class="r"><div class="k">난도</div><div class="v">원본 {nn}</div></div>'
                 f'<div class="r"><div class="k">변형 포인트</div><div class="v">{d["var"]}</div></div></div>')
    h.append('</body></html>')
    src_html = os.path.join(HERE, 'sol_src.html')
    open(src_html, 'w').write(_fx(''.join(h)))
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'sol_src.html', 'sol_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'sol_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
