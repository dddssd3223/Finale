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
<h1>절댓값 위치에 따른 극한 존재 조건</h1>
<div style="font-size:9.5pt">분자 절댓값도 상관있다. 위치마다 조건이 달라진다.</div>

<h2>1. 공통 도구: 좌우 미분계수</h2>
구간별 다항함수 \(f\)에 대해 \(x=k\) 근처에서
\[f(x)-f(k)\approx\begin{cases}f'_-(k)\,(x-k) & (x\to k-)\\[4pt] f'_+(k)\,(x-k) & (x\to k+)\end{cases}\]
여기에 절댓값이 어디 붙는지에 따라 좌극한, 우극한이 달라진다.

<h2>2. 네 가지 경우</h2>
<table>
<tr><th>극한식</th><th>좌극한 \((x\to k-)\)</th><th>우극한 \((x\to k+)\)</th><th>존재 조건</th></tr>
<tr><td>(A) \(\displaystyle\frac{f(x)-f(k)}{x-k}\)</td><td>\(f'_-(k)\)</td><td>\(f'_+(k)\)</td><td>\(f'_-=f'_+\) (미분가능)</td></tr>
<tr><td>(B) \(\displaystyle\frac{f(x)-f(k)}{|x-k|}\)</td><td>\(-f'_-(k)\)</td><td>\(f'_+(k)\)</td><td>\(f'_-+f'_+=0\)</td></tr>
<tr><td>(C) \(\displaystyle\frac{|f(x)-f(k)|}{x-k}\)</td><td>\(-|f'_-(k)|\)</td><td>\(|f'_+(k)|\)</td><td class="r">\(f'_-=f'_+=0\)</td></tr>
<tr><td>(D) \(\displaystyle\frac{|f(x)-f(k)|}{|x-k|}\)</td><td>\(|f'_-(k)|\)</td><td>\(|f'_+(k)|\)</td><td>\(|f'_-|=|f'_+|\)</td></tr>
</table>
<div class="box">
(C)가 앞 질문의 <b>분자 절댓값</b> 경우다. 좌극한 \(\le0\le\) 우극한이므로 둘 다 \(0\)이어야 한다.
<ul style="margin:1mm 0">
<li>다항식이면 \(f'(k)=0\iff f(x)-f(k)=(x-k)^2Q(x)\), 즉 "근이 하나 더(중근)".</li>
<li>꺾인 점이면 좌우 기울기가 <b>모두</b> \(0\)이어야 하므로, 대칭인 V자라도 안 된다.</li>
</ul>
</div>

<h2>3. 4-4의 함수에 네 경우를 모두 적용</h2>
\[f(x)=\begin{cases}x^2-2|x|+2 & (x\ge-2)\\ x^2+6x+10 & (x<-2)\end{cases}\]
\(f'(x)=0\)인 점은 \(x=-3,\,-1,\,1\)이고, 꺾인 점 \(x=-2,\ 0\)에서는 \((f'_-,\,f'_+)=(2,\,-2)\)이다.
<table>
<tr><th>극한식</th><th>극한이 존재하는 \(k\)</th><th>개수</th></tr>
<tr><td>(A) 절댓값 없음</td><td>\(-2,\ 0\)을 뺀 모든 실수</td><td>무수히 많음</td></tr>
<tr><td>(B) 분모 절댓값 (4-4 원문)</td><td>\(-3,\ -2,\ -1,\ 0,\ 1\)</td><td><b>5</b></td></tr>
<tr><td>(C) 분자 절댓값</td><td>\(-3,\ -1,\ 1\) (꺾인 점은 \(|{\pm2}|\ne0\)이라 제외)</td><td class="r"><b>3</b></td></tr>
<tr><td>(D) 분자·분모 모두 절댓값</td><td>모든 실수 (\(|2|=|-2|\))</td><td>무수히 많음</td></tr>
</table>
<div class="key">
노트의 답 ① 3은 정확히 <b>(C) 분자 절댓값</b>의 답이다. 4-4는 분모 절댓값 (B)이므로,
분자 \(f(x)-f(k)\)의 <b>부호가 살아 있어서</b> 꺾인 점에서 좌극한 \(-f'_-=-2\), 우극한 \(f'_+=-2\)로 같아져 극한이 존재한다.
</div>

<h2>4. 정리</h2>
<div class="box">
<ul style="margin:0">
<li>절댓값은 <b>위치에 따라 조건을 바꾼다.</b> 분자든 분모든 상관있다.</li>
<li>판정은 항상 "좌극한, 우극한을 따로 계산"으로 하면 네 경우 모두 한 방법으로 풀린다.</li>
<li>"근의 개수(중근)"는 (C)에서 \(f\)가 \(x=k\) 근처에서 하나의 다항식일 때만 쓰는 지름길이다.</li>
</ul>
</div>
"""
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{B}</body></html>'
open(os.path.join(HERE, 'note_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'note_src.html', 'note_tmp.pdf', 'bg'], cwd=HERE, check=True)
os.replace(os.path.join(HERE, 'note_tmp.pdf'), os.path.join(HERE, 'note44b.pdf'))
