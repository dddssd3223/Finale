# -*- coding: utf-8 -*-
"""인공지능 수학 모의고사 정답 및 해설"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
from content3 import ANS, SA_ANS
C = '①②③④⑤'
EX = {
 1: ("강화 학습 사례", r"강화 학습은 보상이 높은 방향으로 최적 행동을 찾는다. ㄱ(알파고), ㄹ(자율 주행 시뮬레이션)은 강화 학습, ㄴ은 정답이 있는 지도 학습, ㄷ은 정답 없이 패턴을 찾는 비지도 학습이다."),
 2: ("퍼셉트론 출력", r"\(x=2\times1+(-1)\times3+1\times2=1\). \(1<2\)이므로 \(y=f(1)=0\). 따라서 \(x+y=1\)."),
 3: ("AND 임곗값", r"입력 \((0,0),(0,1),(1,0),(1,1)\)에서 가중합은 \(0,\,3,\,2,\,5\). \((1,1)\)만 \(1\)이 출력되려면 \(3<c\le5\). 정수 \(c=4,\,5\)의 합은 \(9\)."),
 4: ("진릿값 계산", r"\(p\oplus r=1\oplus1=0\), \(q=0\)이므로 \((p\oplus r)\vee q=0\). 나머지는 모두 \(1\)이다."),
 5: ("활성화함수", r"ㄱ. 참(시그모이드 \(f(0)=0.5\)). ㄴ. 거짓: 렐루 함수는 \(x\ge0\)에서 \(f(x)=x\)이므로 \(1\)을 넘을 수 있다. ㄷ. 참."),
 6: ("인공지능의 역사", r"ㄴ 튜링 테스트(1950) → ㄹ 다트머스 회의(1956) → ㄱ 퍼셉트론(1957) → ㄷ 딥블루(1997)."),
 7: ("정형 데이터", r"정형 데이터는 정해진 형식이 있는 데이터: ㄱ(연속형), ㄷ(범주형). SNS 글, 상품평, 음성은 비정형 데이터이다."),
 8: ("옳지 않은 것", r"빅데이터의 5V는 규모(Volume), 속도(Velocity), 다양성(Variety), 정확성(Veracity), <b>가치(Value)</b>이다. 가시성은 포함되지 않는다."),
 9: ("다층 퍼셉트론", r"\(z_1=f(3x_1+3x_2)\)는 논리합, \(z_2=f(x_1+2x_2)\)는 논리곱. \(y=f(4z_1-z_2)\): \((z_1,z_2)=(1,1)\)이면 \(4-1=3\ge3\)이므로 \(y=1\). "
     r"따라서 \(y\)는 \((0,1),(1,0),(1,1)\)에서 \(1\) → 배타적 논리합이 아니라 논리합이다. (주의: \(w_{32}=-4\)인 교과서 예와 다름)"),
 10: ("순서도", r"\(n=1:\ a=4\), \(n=2:\ 7\), \(n=3:\ 14\), \(n=4:\ 17\), \(n=5:\ 34\), \(n=6:\ 37\), \(n=7:\ 74>40\) → \(74\) 인쇄."),
}
SX = [
 ("진리표", r"\(r=0\)일 때 \(p\wedge q=1\)인 \(1\)가지, \(r=1\)일 때 \(p\wedge q=0\)인 \(3\)가지 → 모두 \(4\)가지."),
 ("OR 임곗값", r"가중합 \(0,\,2,\,5,\,7\). \((0,0)\)만 \(0\)이 출력되려면 \(0<c\le2\)."),
 ("다층 퍼셉트론 표", r"\((2,-1)\): \(z_1=f(3)=1\), \(z_2=f(-1)=0\), \(y=f(3)=1\). "
  r"\((-1,3)\): \(z_1=f(1)=0\), \(z_2=f(8)=1\), \(y=f(-2)=0\). \((1,1)\): \(z_1=f(3)=1\), \(z_2=f(4)=1\), \(y=f(1)=0\)."),
 ("렐루 함수", r"출력이 양수이므로 \(w_1+2w_2=7\), \(2w_1+w_2=5\) → \(w_1=1\), \(w_2=3\). "
  r"\((3,-2)\): \(3-6=-3<0\)이므로 출력 \(0\). \((-1,4)\): \(-1+12=11\). 합 \(11\)."),
 ("용어", r"(가) 레이블링 (나) 오류 역전파 알고리즘"),
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
    head = ('<h1>2학년 인공지능 수학 모의고사 정답 및 해설</h1><div class="sub">교과서 10–45쪽 · 선택형 10문항(각 6점) · 서답형 5문항(각 8점)</div>'
            '<table><tr><th>번호</th>' + ''.join(f'<th>{n}</th>' for n in range(1, 11)) + '</tr><tr><th>정답</th>'
            + ''.join(f'<td>{C[ANS[n]-1]}</td>' for n in range(1, 11)) + '</tr></table>'
            '<table><tr><th style="width:14%">서답형</th><th>정답</th></tr>'
            + ''.join(f'<tr><td>{i+1}</td><td>{a}</td></tr>' for i, a in enumerate(SA_ANS)) + '</table>')
    body = '<h2>선택형 해설</h2>' + ''.join(f'<div class="it"><b class="n">{n}. {C[ANS[n]-1]}</b><span class="t">{EX[n][0]}</span><br>{EX[n][1]}</div>' for n in range(1, 11))
    body += '<h2>서답형 해설</h2>' + ''.join(f'<div class="it"><b class="n">서답형 {i+1}. {SA_ANS[i]}</b><span class="t">{t}</span><br>{x}</div>' for i, (t, x) in enumerate(SX))
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{body}</body></html>')
    open(os.path.join(HERE, 'sol_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'sol_src.html', 'sol_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'sol_tmp.pdf'), out)
if __name__ == '__main__':
    build(sys.argv[1])
