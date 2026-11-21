# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS, SRC, SA_SRC
C = '①②③④⑤'
EX = {
 1: ("인공지능의 구성 요소", "ㄷ: 반대로 설명했다. 데이터는 집합·벡터·행렬로, 학습은 미분·확률로 다룬다."),
 2: ("인공지능의 역사", "딥블루가 카스파로프를 이긴 것은 1997년이다. 2016년에는 알파고가 이세돌에게 승리했다."),
 3: ("학습 방법 사례", "정답이 있는 스팸 분류는 지도학습, 정답 없이 묶는 회원 그룹은 비지도학습, 보상을 받는 자율 주행은 강화학습이다."),
 4: ("활성화함수", r"시그모이드 함수는 \(f(0)=0.5\)이다. 렐루 함수는 \(x\ge0\)에서 \(f(x)=x\)이므로 1을 넘을 수 있다."),
 5: ("딥러닝 구조", "단층 퍼셉트론은 입력층과 출력층만 있다. 은닉층이 있으면 다층 퍼셉트론이다."),
 6: ("진릿값 계산식", r"\((p,q)\)에 \((0,0),(0,1),(1,0),(1,1)\)을 넣으면 ㄱ·ㄴ·ㄷ 모두 성립한다. 특히 \(p\oplus q\)는 \((1,1)\)일 때 \(1+1-2=0\)이다."),
 7: ("진릿값", r"\((1\wedge0)\vee1=1\), \((1\vee0)\wedge1=1\), \((1\oplus0)\oplus1=1\oplus1=0\)."),
 8: ("AND/OR 퍼셉트론", r"가중합은 \(0,1,1,2\)이다. \(c=2\)이면 \((1,1)\)만 1이므로 AND, \(c=1\)이면 OR이다. \(c=3\)이면 항상 0이다."),
 9: ("배타적 논리합", "XOR은 퍼셉트론 하나(직선 하나)로는 구분할 수 없어 다층 퍼셉트론이 필요하다."),
 10: ("전문가 시스템", "0과 1 사이의 값을 다루는 퍼지 이론과 확률적 방법이 활용되었다."),
 11: ("순서도 기호", "물결 모양 사각형은 문서 출력(인쇄)을 뜻한다. 반복은 판단(마름모)과 화살표로 나타낸다."),
 12: ("연속형·범주형", "키·몸무게는 연속형 데이터이다. 혈액형·거주 지역·설문 응답 단계는 구분 지어 표현하는 범주형 데이터이다."),
 13: ("빅데이터", r"\(1\,\mathrm{TB}=10^{12}\)바이트이다 (KB \(10^3\), MB \(10^6\), GB \(10^9\), TB \(10^{12}\), PB \(10^{15}\))."),
 14: ("활용 사례", "장애인 콜택시는 합성곱 신경망(CNN), 맞춤형 복지는 GBM 알고리즘, 해양 안전 세이프존은 다중회귀분석을 사용했다."),
 15: ("데이터 편향성", "양이 많아도 원본 데이터 자체에 편향이 있으면 편향성이 생긴다. 양과 질이 모두 중요하다."),
 16: ("텍스트 데이터 표현", "단어집합은 중복을 허용하지 않고 순서도 고려하지 않는다. 이 한계 때문에 빈도수 벡터를 사용한다."),
 17: ("벡터의 연산", r"\(3(\vec a+\vec b)-5\vec b=3\vec a-2\vec b=(6-6,\ 12+2)=(0,\ 14)\)."),
 18: ("TF-IDF", r"DF는 앞의 세 단어가 3, 화창·날씨·예상이 2, 햇볕·따뜻하다가 1이다. 문서 C의 TF-IDF는 \((1,1,1,0,0,0,3,3)\)이므로 햇볕과 따뜻하다가 가장 크다."),
 19: ("감성 점수", r"A: \(2+0-1+1+2+2=6\) 긍정. B: \(-1+0+1=0\) 중립. C: \(0+1-2-1-2-2=-6\) 부정."),
 20: ("유클리드 유사도로 감성 분석", r"\(\vec a-\vec p=(1,-1,1,1,0,1,1,0)\) → \(\sqrt6\). \(\vec a-\vec n=(2,0,2,2,-1,0,0,-1)\) → \(\sqrt{14}\). 긍정 쪽이 더 가까우므로 긍정."),
 21: ("유사도 비교", "코사인 유사도는 방향만 비교하므로, 벡터의 크기 정보가 중요할 때는 유용하지 않을 수 있다(교과서 77쪽 단점)."),
}
SX = [
 ("진릿값", r"\((0\wedge1)\vee0=0\), \((0\vee1)\wedge0=0\), \((0\oplus1)\oplus0=1\)."),
 ("빈도수 벡터", "책장 2, 책 2, 가득차다·많다·그·지적이다·분위기·나타내다 각 1."),
 ("자카드 유사도", r"\(J(A,B)=\dfrac27\), \(J(A,C)=\dfrac36=\dfrac12\), \(J(B,C)=\dfrac28=\dfrac14\) → A와 C."),
 ("코사인 유사도", r"\(C(\vec a,\vec b)=\dfrac2{\sqrt{13}}\), \(C(\vec a,\vec c)=0\), \(C(\vec b,\vec c)=\dfrac{12}{\sqrt{13}\times4}=\dfrac{3\sqrt{13}}{13}\) → B와 C."),
 ("TF-IDF", r"DF는 기상 이변·폭우·증가가 3이고 나머지는 1이다. IDF는 각각 1, 3이다. TF-IDF(A)\(=(1,1,1,3,3,0,0,0)\) → 합 9. (기사 A의 핵심 단어: 취약 지역, 침수 사고)"),
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
    head = ('<h1>2학년 인공지능 수학 3회(최종) 정답 및 해설</h1><div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 선택형 21문항(80점) · 단답형 5문항(20점)</div>'
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
