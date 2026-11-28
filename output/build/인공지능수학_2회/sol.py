# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS, SRC, SA_SRC
C = '①②③④⑤'
EX = {
 1: ("AI ⊃ ML ⊃ DL", "딥러닝은 인공신경망(퍼셉트론)을 이용하는 기계학습 방식이다. 기계학습의 일부이며 인공신경망과 직접 관련된다."),
 2: ("빅데이터 5V", "규모(Volume)·속도(Velocity)·다양성(Variety)·정확성(Veracity)·가치(Value). '확실성'은 없다."),
 3: ("데이터 편향성의 원인", "실제 원본 데이터의 편향(불균형·차별)이 그대로 학습되어 판단이 한쪽으로 치우친다."),
 4: ("학습 방법", "지도학습: 입력값+결괏값(정답), 비지도학습: 정답 없이 입력값만, 강화학습: 보상으로 행동 강화."),
 5: ("명제", "명제는 참·거짓을 명확히 판별할 수 있는 문장. '수학은 재미없다'는 판별 기준이 주관적이다."),
 6: ("논리 연산", r"(1) \(\sim p\) 참 (2) \(\vee\)는 하나라도 참이면 참 (3) \(\wedge\)는 하나라도 거짓이면 거짓 (4) \(\oplus\)는 같으면 거짓."),
 7: ("진리표", r"\(p\oplus q\) = 0, 1, 1, 0 → \(\vee q\) 하면 0, 1, 1, 1."),
 8: ("퍼셉트론", r"\(x=2\times0.5+0\times3+1\times1+1\times0.5=2.5<3\) → \(y=0\)."),
 9: ("퍼셉트론", r"가중합 \(-0.1,\ 0.2,\ -0.3,\ 0\) → 출력 \(0,\ 1,\ 0,\ 1\) (\(0\ge0\)이므로 \((0,0)\)은 1)."),
 10: ("순서도", r"\(n=1:\ a=1\), \(n=2:\ a=3\), \(n=3:\ a=6\) (\(3>2\)) → \(6\)."),
 11: ("순서도", r"\(a=1,2,3,\cdots\)에 따라 \(b=1,\,2,\,3,\,5,\,7,\,10,\,13,\cdots\) (\(b\)는 증가). \(4\)는 나오지 않으므로 \(m=4\)이면 종료되지 않는다."),
 12: ("집합과 벡터", r"\(A=\){축구, 세계, 인기, 종목} → \((1,1,0,1,0,1)\)."),
 13: ("벡터가 이루는 각", r"\(\cos\theta=\dfrac{12-2}{\sqrt{20}\sqrt{10}}=\dfrac{10}{10\sqrt2}=\dfrac{\sqrt2}{2}\)."),
 14: ("코사인 유사도", r"\(\dfrac{2+2+0}{\sqrt5\sqrt{10}}=\dfrac4{5\sqrt2}=\dfrac{2\sqrt2}5\)."),
 15: ("자카드 유사도", r"\(A\cap B=\){비, 우산}, \(n(A\cup B)=6\) → \(\dfrac26=\dfrac13\)."),
 16: ("유클리드 유사도", r"\((x-2)^2+(2-y)^2+z^2+1=7\). \(z=2\)이면 \((x-2)^2+(y-2)^2=2\) → \(x=y=1\)일 때 합 \(4\)가 최소(\(z=1\)이면 합 \(6\))."),
 17: ("유사도 비교", "유클리드 유사도는 작을수록, 코사인 유사도는 클수록(1에 가까울수록) 유사. 자카드는 공통 원소가 많을수록 1에 가깝다."),
 18: ("자카드 유사도", r"\(n(A\cap B)=k\): \(\dfrac{k}{13-k}=\dfrac2{11}\) → \(k=2\). \(\dfrac{t}{17-t}>\dfrac2{11}\) → \(t>\dfrac{34}{13}\) → \(t\ge3\)."),
 19: ("유클리드 유사도", r"\((a-4)^2+(a-2)^2+(2a-3)^2=6a^2-24a+29=6(a-2)^2+5\) → \(a=2\)."),
 20: ("코사인 유사도", r"\(\vec a=(1,2,1,0)\), \(\vec b=(0,1,1,1)\) → \(\dfrac{3}{\sqrt6\sqrt3}=\dfrac{\sqrt2}2\)."),
 21: ("유클리드 유사도", r"\(\vec a=(1,1,2,1,0,0)\), \(\vec b=(1,1,0,0,1,0)\), \(\vec c=(1,1,1,1,0,1)\). \(d(A,B)=\sqrt6\), \(d(A,C)=\sqrt2\), \(d(B,C)=2\)."),
}
SX = [
 ("TF-IDF", r"DF: 출산 3, 휴직 2, 용품 2, 보육 1 → IDF \(1,\ \tfrac32,\ \tfrac32,\ 3\). TF-IDF(A) \(=(11,\ 30,\ 0,\ 0)\), 합 \(41\)."),
 ("자카드 감성 분석", r"\(A=\){싱겁다, 맛없다, 비싸다, 별로, 친절, 깨끗하다}. \(J(P,A)=\dfrac2{10}\), \(J(N,A)=\dfrac48\). \(k=0.2-0.5=-0.3\le-0.25\) → 부정, \(10k=-3\)."),
 ("순서도", r"\(s\)는 \(m\)을 \(n\)으로 나눈 몫, \(t\)는 나머지. \(t=0\)이면 \(s=0\), 곧 \(m<n\)인데 나머지가 \(0\)일 수 없어 불가. \(t\ge1\)이면 \(m=5t\cdot n+t\), \(t<n\), \(m\le100\). "
  r"\(t=1\): \(5n+1\le100\), \(n\ge2\) → \(n=2,\cdots,19\) (18개). \(t=2\): \(10n+2\le100\), \(n\ge3\) → 7개. \(t=3\): \(15n+3\le100\), \(n\ge4\) → 3개. \(t\ge4\)는 없음. 합 \(28\)."),
 ("유클리드 유사도", r"\(\vec a=(2,1,1,0,0,2)\), \(\vec b=(1,0,2,1,0,2)\), \(\vec c=(0,1,0,2,1,2)\). \(d^2\): \(4+8+10=22\)."),
 ("다층 퍼셉트론과 XOR", r"\(s_1=2x_1+2x_2\) → \(f\)는 논리합, \(s_2=-x_1-3x_2\) → \(g\)는 \((1,1)\)에서만 0. \(s_3=0.5f+wg\). "
  r"\((0,0)\): \(w<2\), \((0,1),(1,0)\): \(0.5+w\ge2\) → \(w\ge1.5\), \((1,1)\): \(0.5<2\). \(1.5\le w<2\) → \(\tfrac72\)."),
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
    head = ('<h1>2학년 인공지능 수학 2회 정답 및 해설</h1><div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 선택형 21문항(80점) · 단답형 5문항(20점)</div>'
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
