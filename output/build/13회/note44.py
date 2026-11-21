# -*- coding: utf-8 -*-
import os, subprocess
from build3 import font_css, KATEX_CSS, HERE
CSS = r"""
@page{size:A4;margin:16mm 16mm 16mm 16mm}
body{font-family:'HB','MJ','GL',serif;font-size:10.5pt;line-height:1.75;margin:0;color:#000;background:#fff}
.katex{font-size:1.05em}
h1{font-family:'GL';font-size:15pt;font-weight:400;margin:0 0 2mm;-webkit-text-stroke:.3pt #000}
h2{font-family:'GL';font-size:11.5pt;font-weight:400;margin:6mm 0 2mm;border-bottom:1pt solid #000;padding-bottom:1mm;-webkit-text-stroke:.2pt #000}
.box{border:.7pt solid #000;padding:3mm 4mm;margin:2mm 0}
.key{border:1.3pt solid #c8141a;padding:2.5mm 4mm;margin:3mm 0}
table{border-collapse:collapse;width:100%;margin:2mm 0}
td,th{border:.6pt solid #000;padding:2.5pt 5pt;text-align:center;font-weight:400}
th{background:#eee;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.r{color:#c8141a}
"""
B = r"""
<h1>극한 존재 조건: 절댓값과 꺾인 점</h1>
<div style="font-size:9.5pt">문항 4-4 해설 및 앞 질문(분자·분모 절댓값)과의 비교</div>

<h2>1. 문항</h2>
<div class="box">
\[f(x)=\begin{cases}x^2-2|x|+2 & (x\ge-2)\\ x^2+6x+10 & (x<-2)\end{cases}\]
에 대하여 \(\displaystyle\lim_{x\to k}\frac{f(x)-f(k)}{|x-k|}\)의 값이 존재하도록 하는 모든 실수 \(k\)의 개수는?
</div>

<h2>2. 핵심: 좌우 극한을 따로 계산한다</h2>
\(x\to k\)일 때 분자는 좌우에서 각각
\[f(x)-f(k)\approx\begin{cases}f'_-(k)\,(x-k) & (x\to k-)\\[4pt] f'_+(k)\,(x-k) & (x\to k+)\end{cases}\]
이고, 분모는 \(|x-k|=\begin{cases}-(x-k) & (x<k)\\ x-k & (x>k)\end{cases}\) 이므로
\[\lim_{x\to k-}\frac{f(x)-f(k)}{|x-k|}=-f'_-(k),\qquad \lim_{x\to k+}\frac{f(x)-f(k)}{|x-k|}=f'_+(k)\]
<div class="key">
극한이 존재할 조건 : \(\quad -f'_-(k)=f'_+(k)\iff \boxed{\,f'_-(k)+f'_+(k)=0\,}\)
</div>
<table>
<tr><th>\(x=k\)에서의 상태</th><th>조건</th><th>뜻</th></tr>
<tr><td>미분가능 \((f'_-=f'_+)\)</td><td>\(f'(k)=0\)</td><td>노트의 \(f(x)-f(k)=(x-k)^2Q(x)\)와 같음</td></tr>
<tr><td>꺾인 점 \((f'_-\ne f'_+)\)</td><td>\(f'_-(k)=-f'_+(k)\)</td><td class="r">미분불가능이어도 극한 존재 가능 (대칭인 V자, Λ자)</td></tr>
</table>

<h2>3. 적용</h2>
<b>(1) 미분가능한 구간</b>
<table>
<tr><th>구간</th><th>식</th><th>\(f'(x)\)</th><th>\(f'(k)=0\)</th></tr>
<tr><td>\(x<-2\)</td><td>\(x^2+6x+10\)</td><td>\(2x+6\)</td><td>\(k=-3\)</td></tr>
<tr><td>\(-2<x<0\)</td><td>\(x^2+2x+2\)</td><td>\(2x+2\)</td><td>\(k=-1\)</td></tr>
<tr><td>\(x>0\)</td><td>\(x^2-2x+2\)</td><td>\(2x-2\)</td><td>\(k=1\)</td></tr>
</table>
<b>(2) 꺾인 점</b>
<div class="box">
\(x=-2\) : 좌극한·함숫값 모두 \(2\) (연속).
\[f'_-(-2)=2(-2)+6=2,\qquad f'_+(-2)=2(-2)+2=-2\quad\Rightarrow\quad f'_-+f'_+=0\ \ \text{(극한 존재)}\]
\(x=0\) :
\[f'_-(0)=2\cdot0+2=2,\qquad f'_+(0)=2\cdot0-2=-2\quad\Rightarrow\quad f'_-+f'_+=0\ \ \text{(극한 존재)}\]
</div>
<div class="key">
\(k=-3,\ -2,\ -1,\ 0,\ 1\) \(\Rightarrow\) <b>5개 (정답 ③)</b>. &nbsp; ① 3은 꺾인 점 \(-2,\ 0\)을 빠뜨린 값.
</div>

<h2>4. 앞 질문과의 비교</h2>
<table>
<tr><th></th><th>\(\displaystyle\lim\frac{|N(x)|}{D(x)}\) (분자 절댓값)</th><th>\(\displaystyle\lim\frac{N(x)}{|D(x)|}\) (이 문항)</th></tr>
<tr><td>부호가 바뀌는 쪽</td><td>분모 \(D\) (홀수 중근)</td><td>분자 \(N=f(x)-f(k)\)</td></tr>
<tr><td>\(N\)의 형태</td><td>다항식: 좌우가 같은 식</td><td>구간별 함수: 좌우 기울기가 다를 수 있음</td></tr>
<tr><td>판정 도구</td><td>근의 개수 (중근)</td><td>좌우 미분계수 \(f'_-+f'_+=0\)</td></tr>
<tr><td>결론</td><td>극한값 \(=0\) \(\Rightarrow\) \(N\)이 근을 하나 이상 더</td><td>미분가능이면 \(f'(k)=0\), 꺾이면 기울기 크기 같고 부호 반대</td></tr>
</table>
<div class="key">
<b>정리.</b> "근의 개수(중근)"는 \(x=k\) 좌우에서 같은 다항식일 때만 쓸 수 있다.
구간별 함수의 꺾인 점에서는 반드시 \(f'_-(k)\), \(f'_+(k)\)를 따로 구해 판정한다.
"미분불가능 \(\Rightarrow\) 제외"로 끝내면 경우 누락이 생긴다.
</div>
"""
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{B}</body></html>'
open(os.path.join(HERE, 'note_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'note_src.html', 'note_tmp.pdf', 'bg'], cwd=HERE, check=True)
os.replace(os.path.join(HERE, 'note_tmp.pdf'), os.path.join(HERE, 'note44.pdf'))
