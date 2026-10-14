# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS, SRC, SA_SRC
C = '①②③④⑤'
EX = {
 1: ("AI ⊃ ML ⊃ DL", "포함 관계는 딥러닝 ⊂ 기계학습 ⊂ 인공지능. 레이블링한 데이터로 훈련하면 지도학습, 보상으로 최적 행동을 강화하면 강화학습."),
 2: ("빅데이터 5V", "여러 형태(사진·동영상·음악)의 데이터 → 다양성(Variety)."),
 3: ("정형 데이터", "글·사진은 비정형 데이터. 게시판별 글의 '개수'는 정해진 형식의 수치이므로 정형 데이터."),
 4: ("데이터 편향성", "특정 집단의 데이터로 치우쳐 학습해 판단 결과가 한쪽으로 치우침 → 데이터 편향성."),
 5: ("데이터 단위", r"\(10^{11}\,\mathrm{MB}=10^{11}\times10^{6}=10^{17}\,\)바이트 \(=10^{2}\times10^{15}\) → \(10^{2}\,\mathrm{PB}\)."),
 6: ("전문가 시스템", "사용자 ↔ 사용자 인터페이스 ↔ 추론 엔진 ↔ 지식 베이스 ↔ 전문가. 사용자와 전문가는 직접 소통하지 않으며, 추론 엔진이 입력된 질의에 대해 추론하여 답한다."),
 7: ("진릿값", r"\(p\), \(q\) 모두 참(1). ㄱ \(1\vee1=1\), ㄴ \(\sim(1\wedge1)=0\), ㄷ \(1\oplus1=0\)."),
 8: ("집합과 벡터", r"\(A=\){인공지능, 수학, 원리, 작동} → \(U\)의 순서대로 \((1,0,1,1,1,0)\)."),
 9: ("벡터의 상등", r"\(x+2y=-2\), \(2x-3y=10\) → \(x=2\), \(y=-2\)."),
 10: ("TF와 주제어", "단어별 빈도 합: 카페 3, 분위기 3, 커피 5, 정원 2, 맛있다 2 → 커피."),
 11: ("진릿값", r"\(p=1\), \(p\wedge\sim q=1\)이므로 \(q=0\). ㄱ \(1\wedge(0\vee0)=0\), ㄴ \(0\oplus1=1\), ㄷ \((0\oplus0)\vee0=0\)."),
 12: ("퍼셉트론", r"\(s=3\times1+(-1)\times1+2\times0.5=3\ge1\)이므로 \(y=1\). \(s+y=4\)."),
 13: ("자카드 유사도", r"교집합 {반려동물, 행복, 교감} 3개, 합집합 9개 → \(\dfrac39=\dfrac13\)."),
 14: ("유클리드 유사도", r"\(\sqrt{2^2+(-1)^2+2^2+2^2}=\sqrt{13}\)."),
 15: ("AND 임곗값", r"가중합 \(0,\,1,\,3,\,4\)에서 \((1,1)\)만 1 → \(3<c\le4\). \(a+b=7\)."),
 16: ("감성 분석", r"A: 편리하다 \(2\) + 불편하다 \(-2=0\) → 중립. B: 유용하다 \(2\) + 느리다 \(-1=1\) → 긍정."),
 17: ("TF-IDF", "일부 문서에만 등장하는 단어는 DF가 작아 IDF가 커진다(중요도가 높다고 판단). ③이 거꾸로 설명."),
 18: ("TF-IDF 합", r"DF: ㄱ~ㄹ 3, ㅁ 2 → IDF 1, 1, 1, 1, \(\dfrac32\). 합: ㄱ \(9\), ㄴ \(6\), ㄷ \(6\), ㄹ \(9\), ㅁ \(7\times\dfrac32=10.5\) → ㅁ."),
 19: ("자카드 유사도", r"\(J(C,D)=\dfrac{4}{8}=\dfrac12\)로 최대 (\(J(B,D)=\dfrac13\), \(J(B,C)=\dfrac14\), …)."),
 20: ("코사인 유사도", r"\(C(\vec a,\vec b)=\dfrac{2+2+2+1+1}{\sqrt{14}\sqrt5}\approx0.956\)으로 최대 (\(B\)와 \(C\)는 \(0.8\))."),
 21: ("다층 퍼셉트론", r"\(z_1=f(3x_1+4x_2)\), \(z_2=f(x_1+2x_2)\), \(y=f(4z_1-2z_2)\). \((-1,1)\): \(z_1=f(1)=0\), \(z_2=f(1)=0\), \(y=0\). "
     r"\((-1,3)\): \(z_1=f(9)=1\), \(z_2=f(5)=1\), \(y=f(2)=0\). 합 \(2\)."),
}
SX = [
 ("순서도", r"\(n=2,3,4,5\)일 때 \(a=3,\,9,\,27,\,81\). \(n=5\)에서 인쇄 → \(81\)."),
 ("TF와 TF-IDF", r"문맥 이해: TF(A)=1, TF-IDF(A)=\(\dfrac32\) → IDF \(\dfrac32\), DF=2 → \(e=0\), \(f=2\times\dfrac32=3\). "
  r"언어 생성: TF-IDF(C)=2이고 A, B에 등장 → \(a\ge1\)이면 DF=3, IDF=1 → \(a=2\), \(b=3\), \(c=1\). 신경망: C에만 등장 → IDF 3, \(d=6\). 합 \(15\)."),
 ("두 유사도 비교", r"유클리드: \(|(7,x)-(3,4)|^2<|(7,x)-(10,24)|^2 \iff 16+(x-4)^2<9+(x-24)^2 \iff x<13.825\)이므로 \(x\le13\)이면 \(\vec a\)와 유사. "
  r"코사인: \((7,x)\)가 \(\vec a\), \(\vec b\)가 이루는 각의 이등분선보다 위(\(x>12.2\cdots\), 곧 \(x\ge13\))이면 \(\vec b\)와 유사. 둘이 다른 자연수는 \(x=13\)."),
 ("퍼셉트론 부등식", r"\(11w_1+12w_2<c\le\min(11w_1+13w_2,\,12w_1+12w_2)\)에서 \(w_1,w_2>0\). \(13w_1+xw_2<c\le12w_1+12w_2\)이므로 \(x<12-\tfrac{w_1}{w_2}<12\). "
  r"\(\tfrac{w_1}{w_2}\)를 작게 하면 \(x=11\)이 가능 → 최댓값 \(11\)."),
 ("자카드 감성 분석", r"\(X=\){넓다, 편하다, 많다, 맛있다, 불친절}. \(J(P,X)=\dfrac4{11}\), \(J(N,X)=\dfrac1{14}\), 차 \(\approx0.29\ge0.25\) → 긍정, \(c=1\). "
  r"\(a+b+c=\dfrac4{11}+\dfrac1{14}+1=\dfrac{221}{154}\) → \(p+q=375\)."),
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
    head = ('<h1>2학년 인공지능 수학 1회 정답 및 해설</h1><div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 선택형 21문항(80점) · 단답형 5문항(20점)</div>'
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
