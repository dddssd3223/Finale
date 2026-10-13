# -*- coding: utf-8 -*-
"""마지막 쪽: 주제별 계산 문항 2개씩 (단답, 정답은 쪽 아래)"""
from extra import TB, BX
STEP = lambda c: rf"\(f(x)=\begin{{cases}}0 & (x<{c})\\ 1 & (x\ge {c})\end{{cases}}\)"

CALC = [
 ('명제와 진릿값', [
  (r"세 명제 \(p\) : 2는 소수이다, \(q\) : 9는 짝수이다, \(r\) : \(\sqrt9=3\)이다에 대하여 \((p\wedge q)\vee r\)와 \({\sim}(p\vee q)\wedge r\)의 진릿값을 각각 구하시오.", r"\(1,\ 0\)"),
  (r"두 명제 \(p\wedge{\sim}q\)와 \(q\vee r\)의 진릿값이 모두 \(1\)일 때, \(p\oplus r\)의 진릿값을 구하시오.", r"\(0\)"),
 ]),
 ('퍼셉트론', [
  (r"입력값 \((x_1,x_2,x_3)=(1,\,0,\,1)\), 가중치 \((w_1,w_2,w_3)=(0.4,\,-0.3,\,0.5)\), 활성화함수 " + STEP('0.8') + r"일 때, 가중합 \(s\)와 출력값 \(y\)를 구하시오.", r"\(s=0.9,\ y=1\)"),
  (r"두 입력값 \(x_1\), \(x_2\)(\(0\) 또는 \(1\))의 가중치가 \(w_1=1\), \(w_2=2\)이고 활성화함수가 " + STEP('c') + r"인 퍼셉트론이 논리곱(AND)이 되는 \(c\)의 범위를 구하시오.", r"\(2<c\le3\)"),
 ]),
 ('순서도', [
  (r"다음 순서도의 과정에서 인쇄되는 \(a\)의 값을 구하시오." + BX(r"① \(a\leftarrow1\), \(n\leftarrow1\) &nbsp;② \(a\leftarrow2a+1\) &nbsp;③ \(n\leftarrow n+1\) &nbsp;④ \(n\le4\)이면 ②로, 아니면 ⑤로 &nbsp;⑤ \(a\) 인쇄"), r"\(31\)"),
  (r"다음 순서도의 과정에서 인쇄되는 \(s\)의 값을 구하시오." + BX(r"① \(s\leftarrow0\), \(k\leftarrow1\) &nbsp;② \(s\leftarrow s+k\) &nbsp;③ \(k\leftarrow k+2\) &nbsp;④ \(k<10\)이면 ②로, 아니면 ⑤로 &nbsp;⑤ \(s\) 인쇄"), r"\(25\)"),
 ]),
 ('데이터 단위와 통계', [
  (r"\(5\times10^{8}\,\mathrm{KB}\)는 몇 \(\mathrm{TB}\)인지 구하시오.", r"\(0.5\,\mathrm{TB}\)"),
  (r"세 사람의 키가 \(162\,\mathrm{cm}\), \(168\,\mathrm{cm}\), \(171\,\mathrm{cm}\)일 때, 평균과 표준편차를 구하시오.", r"\(167\,\mathrm{cm},\ \sqrt{14}\,\mathrm{cm}\)"),
 ]),
 ('벡터', [
  (r"\(\vec a=(3,\,-1)\), \(\vec b=(1,\,2)\)일 때, 벡터 \(2\vec a-3\vec b\)와 그 크기를 구하시오.", r"\((3,\,-8),\ \sqrt{73}\)"),
  (r"두 벡터 \(\vec a=(x+y,\,4)\), \(\vec b=(5,\,x-y)\)가 서로 같을 때, \(xy\)의 값을 구하시오.", r"\(\dfrac94\)"),
 ]),
 ('TF-IDF', [
  (r"전체 문서 4개 중 2개의 문서에 등장하는 단어가 어떤 문서에 3번 나왔다. \(\mathrm{IDF}=\dfrac{n}{\mathrm{DF}}\)일 때, 그 문서에서 이 단어의 TF-IDF를 구하시오.", r"\(6\)"),
  ("세 문서의 단어 빈도가 다음과 같을 때, 문서 B의 TF-IDF 성분의 합을 구하시오. (단, IDF = n/DF)"
   + TB(['', '여행', '바다', '산'], [['TF(A)', 2, 3, 0], ['TF(B)', 1, 0, 2], ['TF(C)', 2, 1, 0]]), r"\(7\)"),
 ]),
 ('자카드 유사도', [
  (r"\(A=\){여름, 바다, 휴가, 수영}, \(B=\){바다, 수영, 모래}일 때, \(J(A,\,B)\)를 구하시오.", r"\(\dfrac25\)"),
  (r"\(n(A)=n(B)=6\)이고 \(J(A,\,B)=\dfrac12\)일 때, \(n(A\cap B)\)와 \(n(A\cup B)\)를 구하시오.", r"\(4,\ 8\)"),
 ]),
 ('유클리드·코사인 유사도', [
  (r"\(\vec a=(1,\,0,\,2,\,1)\), \(\vec b=(0,\,1,\,1,\,1)\)의 유클리드 유사도 \(d(\vec a,\,\vec b)\)를 구하시오.", r"\(\sqrt3\)"),
  (r"\(\vec a=(1,\,2,\,2)\), \(\vec b=(2,\,1,\,2)\)의 코사인 유사도 \(C(\vec a,\,\vec b)\)를 구하시오.", r"\(\dfrac89\)"),
 ]),
 ('감성 분석', [
  ("감성 사전(최고 2, 좋다 1, 아쉽다 −1, 비싸다 −1)으로 다음 리뷰의 감성 점수 합을 구하고 감성을 분류하시오."
   + BX("맛은 <u>최고</u>인데 가격이 <u>비싸고</u> 양이 <u>아쉬워요</u>."), "0, 중립"),
  (r"\(n(P)=n(N)=5\)이고, 리뷰 X의 단어 집합 \(X\)는 \(P\)의 원소 3개와 \(N\)의 원소 1개로 이루어져 있다. \(J(P,X)\), \(J(N,X)\)를 구하고 감성을 분류하시오. (기준 \(\pm0.25\))", r"\(\dfrac12,\ \dfrac18\), 긍정"),
 ]),
]

def calc_section():
    out = ('<div class="sec cl-sec"><div class="sech"><span class="sn">주제별 계산 연습</span><span class="pg">주제마다 2문항 · 답만 쓰기</span>'
           f'<span class="cnt">{sum(len(v) for _, v in CALC)}문항</span></div><div class="clgrid">')
    n = 0; ans = []
    for t, items in CALC:
        out += f'<div class="clt"><div class="clh">{t}</div>'
        for q, a in items:
            n += 1; ans.append((n, a))
            out += f'<div class="clq"><span class="cn2">{n}</span><div>{q}</div></div>'
        out += '</div>'
    out += '</div><div class="clans"><b>정답</b> ' + ' &nbsp;·&nbsp; '.join(f'{k}) {a}' for k, a in ans) + '</div></div>'
    return out

CALC_CSS = r"""
.cl-sec{break-before:page;margin-top:0}
.clgrid{columns:2;column-gap:10pt}
.clt{break-inside:avoid;border:.6pt solid #bbb;border-radius:2pt;margin:0 0 5pt}
.clh{font-family:'GY','GL';background:#eef0f3;padding:1.5pt 6pt;font-size:8.6pt;border-bottom:.6pt solid #ccc;color:#1f4e9a}
.clq{display:flex;gap:4pt;padding:2.5pt 6pt;font-size:8.5pt;line-height:1.5}
.clq+.clq{border-top:.6pt dashed #ddd}
.cn2{flex:none;font-family:'GY','GL';color:#fff;background:#555;border-radius:6pt;width:12pt;height:12pt;text-align:center;line-height:12pt;font-size:7.6pt;margin-top:1pt}
.clq .bx{padding:1.5pt 5pt;margin:2pt 0;font-size:8.2pt}.clq .gt{font-size:7.8pt;margin:2pt auto}
.clans{margin-top:4pt;border-top:1pt solid #333;padding-top:4pt;font-size:8.4pt;line-height:1.75;color:#b42318}
.clans b{font-family:'GY','GL';color:#111;margin-right:4pt}
"""
