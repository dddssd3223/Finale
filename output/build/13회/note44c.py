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
<h1>(B), (C) 원리와 암기 정리</h1>
<div style="font-size:9.5pt">\(f\)는 구간별 다항함수, \(x=k\)에서 연속. \(f'_-(k)\), \(f'_+(k)\)는 좌·우 미분계수.</div>

<h2>0. 출발점 (둘 다 공통)</h2>
\[x\to k-\ :\ \ f(x)-f(k)\approx f'_-(k)(x-k),\qquad x\to k+\ :\ \ f(x)-f(k)\approx f'_+(k)(x-k)\]
\[|x-k|=\begin{cases}-(x-k) & (x<k)\\ x-k & (x>k)\end{cases}\qquad\Longrightarrow\qquad \frac{x-k}{|x-k|}=\begin{cases}-1 & (x<k)\\ 1 & (x>k)\end{cases}\]

<h2>1. (B) 분모 절댓값 \(\displaystyle\lim_{x\to k}\frac{f(x)-f(k)}{|x-k|}\)</h2>
<div class="box">
<b>좌극한</b> \((x<k)\):
\[\frac{f(x)-f(k)}{|x-k|}=\frac{f(x)-f(k)}{x-k}\cdot\frac{x-k}{|x-k|}=\frac{f(x)-f(k)}{x-k}\cdot(-1)\ \longrightarrow\ -f'_-(k)\]
<b>우극한</b> \((x>k)\):
\[\frac{f(x)-f(k)}{|x-k|}=\frac{f(x)-f(k)}{x-k}\cdot1\ \longrightarrow\ f'_+(k)\]
<b>존재 조건</b>: \(\ -f'_-(k)=f'_+(k)\iff f'_-(k)+f'_+(k)=0\)
</div>
<b>의미</b>: 분모는 \(k\)에서 떨어진 <b>거리</b>(항상 양수)이므로 이 극한은 "거리 1당 높이가 얼마나 변하는가"이다. 왼쪽으로 가도, 오른쪽으로 가도 <b>높이 변화가 같아야</b> 한다.
<ul style="margin:1mm 0">
<li>미분가능한 점: 좌우 기울기가 같으므로 \(f'(k)=-f'(k)\), 즉 \(f'(k)=0\) (평평한 점)</li>
<li>꺾인 점: 기울기가 \((a,\,-a)\) 꼴, 즉 좌우 대칭인 V자, Λ자이면 존재</li>
</ul>
<table>
<tr><th>예</th><th>계산</th><th>결과</th></tr>
<tr><td>\(f(x)=|x|,\ k=0\)</td><td>\(\dfrac{|x|}{|x|}=1\)</td><td>존재 (V자, \((-1,\,1)\))</td></tr>
<tr><td>\(f(x)=x^2,\ k=0\)</td><td>\(\dfrac{x^2}{|x|}=|x|\to0\)</td><td>존재 (\(f'(0)=0\))</td></tr>
<tr><td>\(f(x)=x,\ k=0\)</td><td>\(\dfrac{x}{|x|}=\pm1\)</td><td>존재하지 않음</td></tr>
</table>

<h2>2. (C) 분자 절댓값 \(\displaystyle\lim_{x\to k}\frac{|f(x)-f(k)|}{x-k}\)</h2>
<div class="box">
<b>부호부터</b>: 분자 \(|f(x)-f(k)|\ge0\)이고, 분모 \(x-k\)는 \(x<k\)이면 음수, \(x>k\)이면 양수.
\[\text{좌극한}\le0,\qquad \text{우극한}\ge0\]
같아지려면 <b>둘 다 \(0\)</b>이어야 한다.<br>
<b>계산</b>:
\[\text{좌극한}=\lim_{x\to k-}\frac{|f'_-(k)|\,|x-k|}{x-k}=-|f'_-(k)|,\qquad \text{우극한}=|f'_+(k)|\]
<b>존재 조건</b>: \(\ -|f'_-(k)|=|f'_+(k)|\iff f'_-(k)=f'_+(k)=0\)
</div>
<b>의미</b>: 절댓값이 분자의 부호를 지워 버려서, 좌우의 차이를 분모의 부호가 그대로 만든다. 그 차이를 없애는 유일한 방법은 극한값이 \(0\)이 되는 것, 즉 <b>양쪽 모두 평평해야</b> 한다.
<ul style="margin:1mm 0">
<li>꺾인 점: 기울기가 \(0\)이 아니면 대칭인 V자여도 <b>불가능</b></li>
<li>다항식이면: \(f'(k)=0\iff f(x)-f(k)=(x-k)^2Q(x)\), 즉 중근 (근이 하나 더)</li>
</ul>
<table>
<tr><th>예</th><th>계산</th><th>결과</th></tr>
<tr><td>\(f(x)=|x|,\ k=0\)</td><td>\(\dfrac{|x|}{x}=\pm1\)</td><td>존재하지 않음 (V자도 안 됨)</td></tr>
<tr><td>\(f(x)=x^2,\ k=0\)</td><td>\(\dfrac{x^2}{x}=x\to0\)</td><td>존재</td></tr>
<tr><td>\(f(x)=x^3,\ k=0\)</td><td>\(\dfrac{|x^3|}{x}=x|x|\to0\)</td><td>존재 (근 3개, 하나 이상 더)</td></tr>
</table>

<h2>3. 암기 정리</h2>
<div class="key">
<table style="margin:0">
<tr><th></th><th>(B) \(\dfrac{f(x)-f(k)}{|x-k|}\) 분모 절댓값</th><th>(C) \(\dfrac{|f(x)-f(k)|}{x-k}\) 분자 절댓값</th></tr>
<tr><td>한 줄 요약</td><td><b>좌우 대칭이면 OK</b></td><td><b>극한값은 무조건 0</b></td></tr>
<tr><td>조건</td><td>\(f'_-(k)+f'_+(k)=0\)</td><td>\(f'_-(k)=f'_+(k)=0\)</td></tr>
<tr><td>미분가능한 점</td><td>\(f'(k)=0\)</td><td>\(f'(k)=0\) (다항식이면 중근)</td></tr>
<tr><td>꺾인 점</td><td class="r">대칭 V, Λ자면 존재</td><td class="r">불가능 (양쪽 기울기 0일 때만)</td></tr>
<tr><td>극한값</td><td>\(f'_+(k)\) (0이 아닐 수 있음)</td><td>항상 \(0\)</td></tr>
</table>
</div>
<div class="box">
<b>외우는 법</b>
<ol style="margin:1mm 0">
<li><b>절댓값이 있는 쪽은 부호가 고정된다.</b> 부호가 바뀌는 쪽이 어디인지 먼저 본다.</li>
<li>(C)처럼 <b>분모만 부호가 바뀌면</b>, 좌우 부호가 반대이므로 극한값 \(=0\). (\(\Rightarrow\) 양쪽 평평, 다항식이면 중근)</li>
<li>(B)처럼 <b>분자 부호가 살아 있으면</b>, 좌극한에 \(-1\)이 하나 붙는다. 좌극한 \(=-f'_-\), 우극한 \(=f'_+\). (\(\Rightarrow\) 기울기 합 0)</li>
<li>꺾인 점이 보이면 "미분불가능이니 제외"하지 말고 \(f'_-,\ f'_+\)를 직접 넣어 본다.</li>
</ol>
</div>
"""
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{B}</body></html>'
open(os.path.join(HERE, 'note_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'note_src.html', 'note_tmp.pdf', 'bg'], cwd=HERE, check=True)
os.replace(os.path.join(HERE, 'note_tmp.pdf'), os.path.join(HERE, 'note44c.pdf'))
