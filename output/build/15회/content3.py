# -*- coding: utf-8 -*-
# 학생용 문항 (본문 HTML, 수식은 \( \) / \[ \] LaTeX)
def COND(items):
    return '<div class="cond">' + ''.join(
        (f'<div class="ci"><span class="ck">({k})</span>{v}</div>' if k else f'<div>{v}</div>') for k, v in items) + '</div>'
def BOGI(items):
    return '<fieldset class="bogi"><legend>&lt;보 기&gt;</legend>' + ''.join(
        f'<div class="bi"><span class="bk">{k}.</span><span>{v}</span></div>' for k, v in items) + '</fieldset>'
def FIG(name, w):
    return f'<div class="fig"><img src="{name}.svg" style="width:{w}pt"></div>'

Q = {}
PTS = [4.0] * 4 + [4.2] * 4 + [4.4] * 2 + [4.5] * 2 + [4.7] * 3 + [4.9] + [5.2] * 2
Q[1] = r"""함수 \(f(x)=\dfrac{|x-1||x+1|(x+a)}{(x-1)(x+1)}\)에 대하여 \(\displaystyle\lim_{x\to1+}f(x)+\lim_{x\to-1-}f(x)=8\)일 때, 상수 \(a\)의 값은?{PT}""", ["1", "2", "3", "4", "5"]
Q[2] = r"""다항함수 \(f(x)\)가
\[\lim_{x\to\infty}\frac{f(x)}{x^3}=0,\quad \lim_{x\to0}\frac{f(x)}{x}=3\]
을 만족시킨다. 방정식 \(f(x)=x\)의 한 근이 \(-1\)일 때, \(f(1)\)의 값은?{PT}""", ["3", "4", "5", "6", "7"]
Q[3] = r"""실수 전체의 집합에서 연속인 함수 \(f(x)\)가 모든 실수 \(x\)에 대하여
\[(x-1)f(x)=\frac{\sqrt{x^2+a}-3}{x^2+1}\]
을 만족시킨다. \(\dfrac{a}{f(1)}\)의 값은? (단, \(a\)는 양수이다.){PT}""", ["24", "30", "36", "42", "48"]
Q[4] = r"""두 함수 \(f(x)\), \(g(x)\)가
\[\lim_{x\to2}\{f(x)-g(x)\}=1,\quad \lim_{x\to2}f(x)g(x)=6\]
을 만족시킬 때, \(\displaystyle\lim_{x\to2}\left\{\frac{1}{f(x)+g(x)}\right\}^2\)의 값은?{PT}""", [r"\dfrac1{25}", r"\dfrac1{16}", r"\dfrac19", r"\dfrac14", "1"]
Q[5] = r"""다항함수 \(y=f(x)\)의 그래프 위의 점 \((x,\,f(x))\)에서의 접선의 기울기가 \(2x^2-x+3\)일 때, \(\displaystyle\lim_{h\to0}\frac{f(2+h)-f(2-3h)}{h}\)의 값은?{PT}""", ["27", "36", "45", "54", "63"]
Q[6] = r"""다항함수 \(f(x)\)에 대하여 \(f(1)=3\)이고
\[\lim_{h\to0}\frac{\{f(1+h)\}^2-\{f(1)\}^2}{3h}=4\]
일 때, \(f'(1)\)의 값은?{PT}""", ["-1", "0", "1", "2", "3"]
Q[7] = r"""곡선 \(y=x^3-x\) 위의 점 \((-1,\,0)\)에서의 접선이 이 곡선과 만나는 점 중 \((-1,\,0)\)이 아닌 점의 \(y\)좌표는?{PT}""", ["2", "4", "6", "8", "10"]
Q[8] = r"""두 양수 \(a\), \(b\)에 대하여 함수 \(f(x)\)가
\[f(x)=\begin{cases}x+a & (x<-2)\\ x & (-2\le x<2)\\ bx+1 & (x\ge2)\end{cases}\]
이다. 함수 \(|f(x)|\)가 실수 전체의 집합에서 연속일 때, \(a+b\)의 값은?{PT}""", [r"\dfrac92", "5", r"\dfrac{11}2", "6", r"\dfrac{13}2"]
Q[9] = r"""함수
\[f(x)=\begin{cases}(x-a)(x-b) & (x<2)\\ ax-b & (x\ge2)\end{cases}\]
가 실수 전체의 집합에서 미분가능하도록 하는 두 상수 \(a\), \(b\)의 모든 순서쌍 \((a,\,b)\)에 대하여 \(a+b\)의 값의 합은?{PT}""", ["3", "4", "5", "6", "7"]
Q[10] = r"""두 함수 \(f(x)\), \(g(x)\)가 모든 실수 \(x\)에 대하여
\[-x^2+4x-1\le\frac{f(x)}{g(x)}\le x^2-4x+7\]
을 만족시킬 때, \(\displaystyle\lim_{x\to2}\frac{\{f(x)\}^2-\{g(x)\}^2}{f(x)g(x)+\{g(x)\}^2}\)의 값은?{PT}""", ["1", "2", "3", "4", "5"]
Q[11] = r"""두 함수 \(f(x)=\dfrac{1}{x+a}\), \(g(x)=\sqrt{x+b}-c\)에 대하여
\[\lim_{x\to3-}f(x)=-\infty,\quad \lim_{x\to1}f(x)g(x)=\frac12\]
이고 \(\displaystyle\lim_{x\to3}f(x)g(x)\)의 값이 존재한다. \(\displaystyle\lim_{x\to3}f(x)g(x)\)의 값은? (단, \(a\), \(b\), \(c\)는 상수이다.){PT}""", [r"\dfrac16", r"\dfrac15", r"\dfrac14", r"\dfrac13", r"\dfrac12"]
Q[12] = r"""함수 \(f(x)=x^2-3x+a\)에 대하여 함수 \(g(x)\)를
\[g(x)=\begin{cases}f(x+2) & (x<0)\\ f(x-1) & (x\ge0)\end{cases}\]
이라 하자. 함수 \(\{g(x)\}^2\)이 \(x=0\)에서 연속일 때, \(g(-1)+g(1)\)의 값은? (단, \(a\)는 상수이다.){PT}""", ["-6", "-5", "-4", "-3", "-2"]
Q[13] = r"""두 함수
\[f(x)=\begin{cases}-2 & (|x|\ge1)\\ 1 & (|x|<1)\end{cases},\quad g(x)=\begin{cases}1 & (|x|\ge1)\\ -2x & (|x|<1)\end{cases}\]
에 대하여 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?{PT}""" + BOGI([
            ('ㄱ', r"\(\displaystyle\lim_{x\to1}f(x)g(x)=-2\)"),
            ('ㄴ', r"함수 \(f(x)g(x)\)는 \(x=-1\)에서 연속이다."),
            ('ㄷ', r"함수 \(f(x)g(x+1)\)은 \(x=-1\)에서 연속이다.")]), ['T:ㄱ', 'T:ㄴ', 'T:ㄱ, ㄴ', 'T:ㄱ, ㄷ', 'T:ㄱ, ㄴ, ㄷ']
Q[14] = r"""좌표평면 위의 두 점 \(\mathrm A(a,\ 2a+1)\), \(\mathrm B(a+1,\ 2a+4)\)에 대하여 선분 \(\mathrm{OA}\)의 길이를 \(f(a)\), 선분 \(\mathrm{AB}\)의 길이를 \(g(a)\)라 하자. \(\displaystyle\lim_{a\to1}\frac{f(a)-g(a)}{a-1}\)의 값은? (단, \(\mathrm O\)는 원점이다.){PT}""", [r"\dfrac{7\sqrt{10}}{10}", r"\dfrac{4\sqrt{10}}5", r"\dfrac{9\sqrt{10}}{10}", r"\sqrt{10}", r"\dfrac{11\sqrt{10}}{10}"]
Q[15] = r"""다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여
\[\lim_{h\to0}\frac{f(2h)f(x+h)-f(2h)f(x)}{h^2}=6x^2-4x+8\]
을 만족시킨다. \(f(0)=0\), \(f'(0)=1\)일 때, \(f'(2)\)의 값은?{PT}""", ["8", "9", "10", "11", "12"]
Q[16] = r"""함수
\[f(x)=\begin{cases}\dfrac{x-3}{(x+1)(x-3)} & (x\ne-1,\ x\ne3)\\[6pt] 1 & (x=-1\ \text{또는}\ x=3)\end{cases}\]
가 닫힌구간 \([a-1,\ a+1]\)에서 최댓값과 최솟값을 모두 갖도록 하는 정수 \(a\ (-10<a<10)\)의 개수는?{PT}""", ["13", "15", "16", "17", "19"]
Q[17] = r"""실수 \(t\ (0<t<\sqrt2)\)에 대하여 곡선 \(y=x^2\) 위의 점 중에서 직선 \(y=2tx-2\)와의 거리가 최소인 점을 \(\mathrm P\)라 하고, 직선 \(\mathrm{OP}\)가 직선 \(y=2tx-2\)와 만나는 점을 \(\mathrm Q\)라 할 때, \(\displaystyle\lim_{t\to\sqrt2-}\frac{\overline{\mathrm{PQ}}}{\sqrt2-t}\)의 값은? (단, \(\mathrm O\)는 원점이다.){PT}""", [r"2\sqrt2", r"\sqrt{10}", r"2\sqrt3", r"\sqrt{14}", "4"]
Q[18] = r"""두 자연수 \(a\), \(b\ (a<b<8)\)에 대하여 함수 \(f(x)\)가
\[f(x)=\begin{cases}|x+2|-1 & (x<a)\\ x-11 & (a\le x<b)\\ |x-10|-1 & (x\ge b)\end{cases}\]
이다. 함수 \(f(x)\)와 양수 \(k\)가 다음 조건을 만족시킨다.""" + COND([
            ('가', r"함수 \(f(x)f(x+k)\)는 실수 전체의 집합에서 연속이다."),
            ('나', r"\(f(k)<0\)")]) + \
       r"""\(f(a)\times f(b)\times f(k)\)의 값은?{PT}""", ["96", "112", "128", "144", "160"]
ANS = {1: 4, 2: 3, 3: 5, 4: 1, 5: 2, 6: 4, 7: 3, 8: 1, 9: 5, 10: 2, 11: 4, 12: 3, 13: 4, 14: 1, 15: 5, 16: 2, 17: 3, 18: 2}
Q = {n: (PTS[n - 1],) + tuple(Q[n]) for n in Q}

S1 = r"""상수항과 계수가 모두 음이 아닌 정수인 두 다항함수 \(f(x)\), \(g(x)\)가 다음 조건을 만족시킨다.""" + COND([
            ('가', r"\(\displaystyle\lim_{x\to\infty}\frac{\{f(x)\}^2g(x)}{x^5}=9\)"),
            ('나', r"\(\displaystyle\lim_{x\to0}\frac{f(x)\{g(x)\}^2}{x^5}=3\)")]) + \
     r"""다음 물음에 답하시오."""
S1S = [(r"\(f(x)\)의 차수와 \(g(x)\)의 차수의 합을 구하시오.", "3점"),
       (r"\(f(1)\)의 값을 구하시오.", "3점"),
       (r"\(f(2)+g(2)\)의 값을 구하시오.", "4점")]
S2 = r"""양수 \(a\)에 대하여 함수 \(f(x)=|x(x-a)|\)가
\[\lim_{x\to0}\frac{f(x)f(-x)}{x^2}=4\]
를 만족시킨다. 다음 물음에 답하시오."""
S2S = [(r"\(a\)의 값을 구하시오.", "2점"),
       (r"\(\displaystyle\lim_{x\to a+}\frac{f(x)f(-x)}{x-a}\)의 값을 구하는 과정을 서술하시오.", "4점"),
       (r"\(\displaystyle\lim_{x\to a}\frac{f(x)f(-x)}{x-a}\)의 값이 존재하는지 판정하는 과정을 서술하시오.", "4점")]
S1 = S1.replace('<div class="ci">', '<div class="ci" style="margin:4pt 0">')
