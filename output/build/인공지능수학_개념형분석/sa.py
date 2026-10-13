# -*- coding: utf-8 -*-
"""단답형 예상 문항 — 세화·명지·대일 2026-1 중간 서답형(이미지·행렬 제외 16문항) 유형 빈도순"""
import os
from extra import TB, BX
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = lambda n, w: f'<div class="fig"><img src="file://{HERE}/{n}.svg" style="width:{w}pt"></div>'
STEP = r"\(f(x)=\begin{cases}0 & (x<1)\\ 1 & (x\ge 1)\end{cases}\)"

# 유형, 세화, 명지, 대일
TALLY = [
 ('유클리드·코사인 유사도 계산', '서답 6', '14, 17', '서답 2, 4'),
 ('TF-IDF 표 계산', '서답 2', '13', '서답 4'),
 ('빈도수 벡터 만들기', '', '14(1), 17(1)', '서답 2(1)(2)'),
 ('다층 퍼셉트론 출력', '', '18', '서답 1'),
 ('자카드 유사도 감성 분석', '서답 4', '16', ''),
 ('단층 퍼셉트론 가중치·임곗값', '서답 7, 8', '18(3)', ''),
 ('순서도 출력값', '서답 5', '20', ''),
 ('감성 사전 점수 합', '서답 3', '', ''),
 ('명제와 진릿값', '', '20', ''),
 ('개념 빈칸', '', '', ''),
]

SA = [
 dict(t='유클리드·코사인 유사도',
  q=r"세 리뷰 A, B, C를 빈도수 벡터로 나타내면 \(\vec a=(1,\,1,\,0,\,2)\), \(\vec b=(2,\,1,\,1,\,0)\), \(\vec c=(1,\,2,\,0,\,2)\)이다. "
    r"유클리드 유사도로 판단할 때 가장 유사한 두 리뷰와 그 유클리드 유사도, 그리고 코사인 유사도 \(C(\vec a,\,\vec c)\)를 구하시오.",
  a=r"A와 C, \(1\) / \(C(\vec a,\vec c)=\dfrac{7\sqrt6}{18}\ (\approx0.953)\)",
  s=r"\(d(\vec a,\vec b)=\sqrt6\), \(d(\vec a,\vec c)=1\), \(d(\vec b,\vec c)=\sqrt7\). \(C(\vec a,\vec c)=\dfrac{1+2+0+4}{\sqrt6\times3}\)."),
 dict(t='TF-IDF',
  q="세 문서 A, B, C의 단어 빈도(TF)가 다음과 같다." + TB(['', '축제', '공연', '음식', '불꽃'], [['TF(A)', 2, 1, 0, 3], ['TF(B)', 1, 0, 2, 0], ['TF(C)', 3, 2, 1, 0]])
    + r"\(\mathrm{IDF}=\dfrac{n}{\mathrm{DF}}\)일 때, 문서 A의 TF-IDF를 벡터로 나타내고, A에서 가장 중요한 단어를 쓰시오.",
  a=r"\(\left(2,\,\dfrac32,\,0,\,9\right)\), 불꽃",
  s=r"DF \(=(3,2,2,1)\), IDF \(=\left(1,\dfrac32,\dfrac32,3\right)\). TF와 성분끼리 곱한다."),
 dict(t='빈도수 벡터',
  q=r"두 문장에서 불용어를 제거하고 기본형으로 나타낸 단어의 전체집합이 \(U=\){사과, 바나나, 포도, 좋아하다, 싫어하다}이다."
    + BX("문장 A: 나는 사과를 좋아하고 바나나도 좋아한다.<br>문장 B: 너는 사과를 싫어하지만 포도는 좋아한다.")
    + r"\(U\)의 원소 순서대로 두 문장의 빈도수 벡터 \(\vec a\), \(\vec b\)를 구하시오.",
  a=r"\(\vec a=(1,\,1,\,0,\,2,\,0)\), \(\vec b=(1,\,0,\,1,\,1,\,1)\)",
  s="‘좋아하고’, ‘좋아한다’는 기본형 ‘좋아하다’로 2번 센다."),
 dict(t='다층 퍼셉트론',
  q=r"그림과 같은 다층 퍼셉트론의 모든 활성화함수가 " + STEP + r"일 때, 입력 \((x_1,x_2)\)가 \((0,0)\), \((0,1)\), \((1,0)\), \((1,1)\)인 경우의 출력값 \(y\)를 순서대로 쓰고, 이 퍼셉트론이 나타내는 논리 연산을 쓰시오."
    + IMG('fig_sa_mlp', 150),
  a=r"\(0,\,1,\,1,\,0\), 배타적 논리합(XOR)",
  s=r"\(z_1=f(x_1+x_2)\)는 논리합, \(z_2=f(0.5x_1+0.5x_2)\)는 논리곱, \(y=f(z_1-z_2)\)."),
 dict(t='자카드 유사도 감성 분석',
  q=r"긍정 단어 집합 \(P=\){좋다, 친절, 깨끗하다, 맛있다, 빠르다, 저렴하다}, 부정 단어 집합 \(N=\){나쁘다, 불친절, 더럽다, 맛없다, 느리다, 비싸다}이다."
    + BX("리뷰 X: 음식이 <u>맛있고</u> 직원도 <u>친절</u>했지만 가격이 <u>비싸요</u>.")
    + r"리뷰 X에 쓰인 \(P\cup N\)의 단어 집합을 \(X\)라 할 때, \(J(P,X)\), \(J(N,X)\)를 구하고 감성을 분류하시오. (단, 차가 \(0.25\) 이상이면 긍정, \(-0.25\) 초과 \(0.25\) 미만이면 중립, \(-0.25\) 이하이면 부정)",
  a=r"\(J(P,X)=\dfrac27\), \(J(N,X)=\dfrac18\), 중립",
  s=r"\(X=\){맛있다, 친절, 비싸다}. \(\dfrac2{6+3-2}\), \(\dfrac1{6+3-1}\), 차 \(\approx0.16<0.25\)."),
 dict(t='단층 퍼셉트론 임곗값',
  q=r"두 입력값 \(x_1\), \(x_2\)(\(0\) 또는 \(1\))의 가중치가 \(w_1=2\), \(w_2=3\)이고 활성화함수가 \(f(x)=\begin{cases}0 & (x<c)\\ 1 & (x\ge c)\end{cases}\)인 퍼셉트론이 "
    r"논리곱(AND)이 되는 \(c\)의 범위와 논리합(OR)이 되는 \(c\)의 범위를 각각 구하시오.",
  a=r"AND: \(3<c\le5\), OR: \(0<c\le2\)",
  s=r"가중합은 \((0,0)\) 0, \((0,1)\) 3, \((1,0)\) 2, \((1,1)\) 5. AND는 5만 1, OR는 2·3·5가 1."),
 dict(t='순서도',
  q=r"다음 순서도에서 인쇄되는 \(a\)의 값을 구하시오." + IMG('fig_sa_flow', 140),
  a=r"\(30\)",
  s=r"\(n=1,2,3,4\)일 때 \(a\)에 \(1,4,9,16\)을 더하고 \(n=5\)에서 인쇄. \(1+4+9+16\)."),
 dict(t='감성 사전 점수',
  q="다음 감성 사전으로 리뷰의 감성 점수 합을 구하고, 합이 0보다 크면 긍정, 0이면 중립, 0보다 작으면 부정으로 분류하시오. (사전에 없는 단어는 0점)"
    + TB(['단어', '최고', '친절', '좋다', '불편하다', '별로', '최악'], [['점수', 2, 1, 1, -1, -1, -2]], first=True)
    + BX("리뷰: 위치는 <u>최고</u>인데 방이 <u>좁고</u> 침대가 <u>불편해요</u>. 직원은 <u>친절</u>했지만 조식은 <u>별로</u>였어요."),
  a=r"\(1\), 긍정",
  s=r"\(2+0-1+1-1=1\). ‘좁다’는 사전에 없어 0점."),
 dict(t='명제와 진릿값',
  q=r"세 명제 \(p\) : 1은 소수이다, \(q\) : \(\sqrt4\)는 유리수이다, \(r\) : 12의 약수는 6개이다에 대하여 \((p\oplus q)\wedge r\)와 \({\sim}(q\wedge r)\)의 진릿값을 각각 구하시오.",
  a=r"\(1\), \(0\)",
  s=r"\(p=0\) (1은 소수가 아님), \(q=1\), \(r=1\). \((0\oplus1)\wedge1=1\), \({\sim}(1\wedge1)=0\)."),
 dict(t='개념 빈칸',
  q="다음 (가), (나)에 알맞은 말을 쓰시오."
    + BX("TF-IDF는 단어 빈도(TF)와 <b>(가)</b>을/를 곱하여 구한다. 이때 (가)는 문서 빈도(DF)를 전체 문서의 개수 n으로 나눈 <b>(나)</b>의 역수로 계산한다."),
  a="(가) 역문서 빈도(IDF), (나) 상대도수",
  s="교과서 64쪽 중단원 마무리 ‘배운 내용 정리하기’와 같은 빈칸 형식."),
]

def sa_section(CIRC):
    rows = ''.join(f'<tr><td>{i+1}</td><td class="l">{t}</td><td>{a or "–"}</td><td>{b or "–"}</td><td>{c or "–"}</td>'
                   f'<td>{sum(1 for x in (a, b, c) if x)}</td></tr>' for i, (t, a, b, c) in enumerate(TALLY))
    out = ('<div class="sec sa-sec"><div class="sech"><span class="sn">단답형 예상 문항</span><span class="pg">출제 가능성 높은 순</span><span class="cnt">10문항</span></div>'
           '<div class="why">근거: 세화고·명지고·대일고 2026-1 중간고사 서답형 중 범위 안 16문항(이미지·행렬 제외)을 유형별로 세어, '
           '<b>출제 학교 수 → 문항 수</b> 순으로 정렬했다.</div>'
           f'<table class="tp tal"><tr><th style="width:6%">순위</th><th>유형</th><th>세화</th><th>명지</th><th>대일</th><th style="width:9%">출제 학교</th></tr>{rows}</table>'
           '<div class="sagrid">')
    for i, e in enumerate(SA):
        out += (f'<div class="sac"><div class="sah"><span class="rk">{i+1}위</span><span class="tt">{e["t"]}</span></div>'
                f'<div class="saq">{e["q"]}</div><div class="saa"><span class="lb">답</span>{e["a"]}</div>'
                f'<div class="sas">{e["s"]}</div></div>')
    return out + '</div></div>'

SA_CSS = r"""
.sa-sec{break-before:page;margin-top:0}
.why{font-size:8.6pt;color:#333;margin:0 0 4pt}
.tal td,.tal th{font-size:8.2pt;padding:1.6pt 4pt}
.sagrid{columns:2;column-gap:9pt;margin-top:7pt}
.sac{break-inside:avoid;border:.6pt solid #aaa;border-radius:2pt;margin:0 0 6pt;font-size:8.7pt;line-height:1.5}
.sah{display:flex;gap:6pt;align-items:center;background:#f2f2f2;border-bottom:.6pt solid #ccc;padding:2pt 6pt;font-family:'GY','GL';font-size:8.6pt}
.rk{background:#b42318;color:#fff;border-radius:7pt;padding:0 6pt;font-size:7.8pt}
.saq{padding:3pt 7pt}
.saq .bx{padding:2pt 5pt;margin:3pt 0}.saq .gt{font-size:7.8pt;margin:3pt auto}
.saa{padding:2pt 7pt;border-top:.6pt dashed #bbb;color:#b42318}
.saa .lb{font-family:'GY','GL';background:#b42318;color:#fff;border-radius:2pt;padding:0 4pt;margin-right:5pt;font-size:7.8pt}
.sas{padding:1pt 7pt 3pt;color:#555;font-size:8.1pt;background:#fffaf2}
"""
