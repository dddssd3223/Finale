# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS, SRC, SA_SRC
C = '①②③④⑤'
EX = {
 1: ("인공지능의 개념", "'인공지능'이라는 용어는 1956년 미국 다트머스 회의에서 처음 사용되었다. 1950년 튜링의 논문은 튜링 테스트를 제시했다."),
 2: ("딥러닝", "포함 관계는 (인공지능) ⊃ (기계학습) ⊃ (딥러닝)이다. ㄹ은 방향이 반대이다."),
 3: ("알고리즘과 순서도", "계산 방법 또는 처리 과정의 순서 = 알고리즘, 알고리즘을 기호와 그림으로 나타낸 것 = 순서도."),
 4: ("순서도 (확인하기 6)", r"\(a=0\)이면 \(bx+c=0\)이 된다. (가) \(b=0\)? 아니요 → \(x=-\dfrac cb\). (나) \(c=0\)? 예 → (라) 해가 무수히 많다, 아니요 → (마) 해가 없다. \(a\ne0\)이면 (다) 근의 공식을 이용한다."),
 5: ("명제", r"ㄱ: 참인 명제. ㄴ: \(2x+1=5\)이므로 거짓인 명제. ㄷ: \(x\)의 값에 따라 참·거짓이 달라지므로 명제가 아니다. ㄹ: '가까운'은 기준이 모호하므로 명제가 아니다."),
 6: ("진릿값", r"(1) 거짓 (2) \(25-30+5=0\) 참 (3) \(4-1=3<3\) 거짓 (4) 8의 약수는 \(\{1,2,4,8\}\)이므로 거짓."),
 7: ("전문가 시스템의 구성", "증상은 사실, 규칙은 지식 베이스, 사실과 규칙으로 결론을 내리는 것은 추론 엔진이다."),
 8: ("XOR 다층 퍼셉트론", r"\(z_1=f(5\cdot1+4\cdot0)=f(5)=1\), \(z_2=f(1\cdot1+2\cdot0)=f(1)=0\), \(y=f(4\cdot1-4\cdot0)=f(4)=1\)."),
 9: ("평균과 표준편차", r"평균 \(\dfrac{170+173+185}{3}=176\), 분산 \(\dfrac{36+9+81}{3}=42\) → 표준편차 \(\sqrt{42}\)."),
 10: ("빅데이터와 인공지능", "빅데이터와 인공지능은 상호 보완 관계이다."),
 11: ("다중회귀분석", "합성곱 신경망은 이미지 패턴 분석(콜택시 배차), GBM은 수열의 점화식과 미분의 성질을 활용한 분류(맞춤형 복지)에 쓰였다."),
 12: ("집합으로 표현", "단어집합은 중복을 허용하지 않는다. 그래서 중복된 단어를 한 번만 나타내는 한계가 있다."),
 13: ("빈도수 벡터의 합", r"\(\vec u=(4,3,2,1,1,1,1,1,1,1,1,1)\) → 합 18 (\(\vec a\)의 합 8 + \(\vec b\)의 합 10)."),
 14: ("단어 임베딩", "가장 많이 사용되는 단어 임베딩 방법은 워드투벡(Word2vec)이다."),
 15: ("형태소와 단어 구름", "TF 기반은 많이 나온 단어가, TF-IDF 기반은 문맥상 중요한 단어가 크게 나타나므로 서로 다를 수 있다."),
 16: ("TF-IDF", "TF-IDF에는 절대적인 기준값이 없고, 분석 목적에 따라 상대적인 기준값을 설정한다."),
 17: ("TF-IDF", r"DF: 프라이드치킨·추천 3, 나머지 2 → IDF 1, 1, \(\tfrac32\), … 후기 B의 TF-IDF \(=(1,1,\tfrac32,\tfrac32,0,0,\tfrac32)\) → 배달, 빠르다, 맛있다."),
 18: ("감성 분석", "'잘(능력 긍정)'은 긍정(1)이지만, '잘(단순 긍정, 의지 긍정)'은 중립(0)이다. 같은 단어라도 의미에 따라 감성 점수가 다르다."),
 19: ("감성 분석의 한계", r"\(2-2-2-2+0-2=-6\) → 규칙상 부정이지만 실제로는 긍정. 그래서 기계학습을 도입한다."),
 20: ("벡터의 성질", r"\(k\vec a=(ka_1,\,ka_2)\)이다. 모든 성분에 \(k\)를 곱한다."),
 21: ("코사인 유사도와 각", r"\(\vec a\)와 \(\vec b\)는 0° → 1, \(\vec a\)와 \(\vec d\)는 90° → 0, \(\vec a\)와 \(\vec c\)는 약 33.7° → \(\dfrac{3}{\sqrt{13}}=\dfrac{3\sqrt{13}}{13}\). 각이 작을수록 코사인 유사도가 크다."),
}
SX = [
 ("활성화함수", "(가) 임곗값 (나) 활성화함수."),
 ("벡터의 크기", r"\(\vec b-\vec a=\overrightarrow{\mathrm{AB}}=(2,\,-3)\) → \(\sqrt{4+9}=\sqrt{13}\) (두 점 사이의 거리)."),
 ("빈도수 벡터", "수학, 인공지능, 원리, 이해, 필요가 각 1회씩, 관련·기반·발전은 0회."),
 ("유클리드 유사도", r"\(d(A,B)=\sqrt4=2\), \(d(A,C)=\sqrt9=3\), \(d(B,C)=\sqrt3\) → B와 C."),
 ("코사인 유사도", r"\(C(A,B)\approx0.667\), \(C(A,C)=\dfrac{12+4+2+15+12}{\sqrt{32}\sqrt{65}}\approx0.987\), \(C(B,C)\approx0.672\) → A와 C."),
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
    head = ('<h1>2학년 인공지능 수학 5회 정답 및 해설</h1><div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 선택형 21문항(80점) · 단답형 5문항(20점)</div>'
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
