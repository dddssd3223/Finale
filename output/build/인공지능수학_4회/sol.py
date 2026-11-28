# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS, SRC, SA_SRC
C = '①②③④⑤'
EX = {
 1: ("데이터와 수학", "이미지 인식·분류에는 인공신경망(행렬, 합성함수, 확률, 미적분, 통계, 벡터)이 활용된다."),
 2: ("기계학습", "레이블링된(정답이 있는) 데이터로 학습하는 것은 지도학습이다. 비지도학습은 정답이 없는 데이터로 숨겨진 패턴을 찾는다."),
 3: ("튜링 테스트", "'튜링 기계'는 1936년에 제시되었다. 다트머스 회의(1956)는 '인공지능' 용어가 처음 쓰인 회의이다."),
 4: ("뉴런과 퍼셉트론", "퍼셉트론은 여러 값을 입력받아 하나의 값을 출력하는, 가장 작은 인공신경망 단위이다."),
 5: ("퍼셉트론", r"\(x=0.6-0.2+0+0.5=0.9<1\) → \(y=0\)."),
 6: ("명제와 참", "ㄱ: 4와 6의 최대공약수가 2이므로 거짓. ㄴ·ㄷ: 참. ㄹ: 참·거짓을 판별할 수 없으므로 명제가 아니다."),
 7: ("논리 연산", r"\(p\) 거짓(오리너구리는 포유류), \(q\) 참. \(p\vee q\) 참, \(p\wedge q\) 거짓, \(p\oplus q\) 참(하나만 참)."),
 8: ("진리표", r"\(\sim q\) = 0, 1, 0, 1 → \(p\vee\sim q\) = 1, 1, 0, 1."),
 9: ("단층 퍼셉트론의 한계", "배타적 논리합은 직선 하나로 나눌 수 없다. 이 한계를 다층 퍼셉트론과 오류 역전파 알고리즘으로 해결했다."),
 10: ("다층 퍼셉트론", r"\(z_1=f(3x_1+x_2)\), \(z_2=f(2x_1+x_2)\)는 둘 다 논리합이라 항상 같은 값을 가진다. \(y=f(3z_1-3z_2)=f(0)=0\)이므로 개수는 0이다."),
 11: ("순서도", r"\(a=1\) → \(n=1\): \(a=3\), \(n=2\): \(a=7\), \(n=3\): \(a=13\), \(n=4>3\) → \(13\)."),
 12: ("정형·비정형", "이미지·의견·SNS 글은 비정형, 체력 검사 결과·혈액형은 정형 데이터이다."),
 13: ("빅데이터", "고정된 형식이 없는 것은 비정형 데이터이고, 비정형 데이터를 정형 데이터로 가공해야 컴퓨터가 처리하기 쉽다(반대로 설명함)."),
 14: ("데이터 편향 사례", "문제를 고치려 했지만 같은 문제가 반복되지 않으리라는 확신을 주지 못해 결국 폐기되었다."),
 15: ("벡터의 성분", "첫째 성분 2, 넷째 성분 0, 성분이 5개이므로 5차원 벡터이다."),
 16: ("벡터의 상등", r"\(2x+y=0\), \(x-3y=7\) → \(x=1\), \(y=-2\) → \(x-y=3\)."),
 17: ("단어 포함 벡터", "문장 B에는 '향하다'가 없고 나머지 7개 단어가 모두 있다. 참고로 '꽃'의 원-핫 벡터는 ②이다."),
 18: ("빈도수와 주제어", "조리법 A는 김치(4), 조리법 B는 된장(4)이 가장 자주 언급되었다."),
 19: ("로그를 이용한 IDF", r"\(\mathrm{IDF}=\log\dfrac{1000}{10}=\log100=2\), \(\mathrm{TF\text{-}IDF}=3\times2=6\)."),
 20: ("자카드 유사도 감성 분석", r"\(X=\){많다, 빠르다, 맛없다}. \(J(P,X)=\dfrac2{11}\), \(J(N,X)=\dfrac1{12}\). 차는 \(0.098\cdots\)로 \(0.25\)보다 작으므로 중립이다."),
 21: ("유클리드와 코사인 비교", r"\(d(\vec b,\vec c)=\sqrt2\)가 최소(\(d(\vec a,\vec b)=\sqrt3\), \(d(\vec a,\vec c)=\sqrt7\)), \(C(\vec a,\vec b)\approx0.956\)이 최대. 방향만 비교하는 것은 코사인 유사도이다."),
}
SX = [
 ("감성 분석", "감성 분석은 극성(긍정·중립·부정)이나 감정(기쁨·슬픔 등)으로 분류하는 방법이다. 분류한 감성을 점수로 나타내는 방식이 감성 점수 회귀 분석이다."),
 ("TF-IDF", r"DF: 언어 생성·신경망·문맥 이해 3, 인간 같은 반응·데이터 학습·창의적 결과물 2 → IDF \(1,1,1,\tfrac32,\tfrac32,\tfrac32\). TF-IDF(A)\(=(3,1,2,3,0,3)\) → 12."),
 ("유클리드 유사도", r"\(d(A,B)=\sqrt{12}\), \(d(A,C)=\sqrt4=2\), \(d(B,C)=\sqrt8\) → A와 C, 2. (코사인 유사도로도 A와 C가 가장 유사)"),
 ("유클리드 감성 분석", r"\(\vec x-\vec p=(0,0,-1,-1,1,1,1,0)\) → \(\sqrt5\), \(\vec x-\vec n=(1,1,0,0,0,0,0,-1)\) → \(\sqrt3\). 부정 쪽이 더 가까우므로 부정."),
 ("코사인 유사도", r"배¹–부르다 \(\approx0.999\), 배²–타다 \(\approx0.992\), 배³–달콤하다 \(\approx0.990\)이 각각 가장 크다."),
]
CSS = r"""@page{size:A4;margin:14mm 13mm}
body{font-family:'HB','GL';font-size:9.6pt;color:#111;line-height:1.6}
h1{font-family:'GL';font-size:15pt;text-align:center;margin:0 0 3pt;-webkit-text-stroke:.3pt #000}
.sub{text-align:center;color:#555;font-family:'GL';font-size:9pt;margin-bottom:10pt}
table{border-collapse:collapse;width:100%;margin-bottom:10pt}
th,td{border:.6pt solid #888;padding:3pt 4pt;text-align:center;font-size:9.4pt}
th{background:#eee;font-family:'GL';font-weight:400;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.it{margin:0 0 7pt;break-inside:avoid}.it b.n{font-family:'GL'}
.it .t{color:#555;font-family:'GL';font-size:8.8pt;margin-left:4pt}
h2{font-family:'GL';font-size:11pt;margin:10pt 0 5pt;border-bottom:1pt solid #333;padding-bottom:2pt}"""
def build(out):
    head = ('<h1>2학년 인공지능 수학 4회 정답 및 해설</h1><div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 선택형 21문항(80점) · 단답형 5문항(20점)</div>'
            '<table><tr><th>번호</th>' + ''.join(f'<th>{n}</th>' for n in range(1, 22)) + '</tr><tr><th>정답</th>'
            + ''.join(f'<td>{C[ANS[n]-1]}</td>' for n in range(1, 22)) + '</tr></table>'
            '<table><tr><th style="width:14%">단답형</th><th>정답</th></tr>'
            + ''.join(f'<tr><td>{i+1}</td><td>{a}</td></tr>' for i, a in enumerate(SA_ANS)) + '</table>')
    body = '<h2>선택형 해설</h2>' + ''.join(f'<div class="it"><b class="n">{n}. {C[ANS[n]-1]}</b><span class="t">{EX[n][0]} · 출처 {SRC[n]}</span><br>{EX[n][1]}</div>' for n in range(1, 22))
    body += '<h2>단답형 해설</h2>' + ''.join(f'<div class="it"><b class="n">단답형 {i+1}. {SA_ANS[i]}</b><span class="t">{t} · 출처 {SA_SRC[i]}</span><br>{x}</div>' for i, (t, x) in enumerate(SX))
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{body}</body></html>')
    open(os.path.join(HERE, 'sol_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'sol_src.html', 'sol_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'sol_tmp.pdf'), out)
if __name__ == '__main__':
    build(sys.argv[1])
