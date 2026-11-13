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
Q[1] = r"""함수
\[f(x)=\begin{cases}x+a & (x<2)\\ -x^2+x+3a & (x\ge2)\end{cases}\]
에 대하여 \(\displaystyle\lim_{x\to2-}f(x)\times\lim_{x\to2+}f(x)=16\)이 되도록 하는 양수 \(a\)의 값은?{PT}""", ["1", "2", "3", "4", "5"]
Q[2] = r"""다항함수 \(f(x)\)가 \(\displaystyle\lim_{x\to2}\frac{f(x)}{x^2-4}=3\)을 만족시킬 때, \(\displaystyle\lim_{x\to2}\frac{x^3-8}{xf(x)}\)의 값은?{PT}""", [r"\dfrac16", r"\dfrac15", r"\dfrac14", r"\dfrac13", r"\dfrac12"]
Q[3] = r"""함수
\[f(x)=\begin{cases}\dfrac{x-a}{\sqrt{x+3}-\sqrt{a+3}} & (x\ne a)\\ 8 & (x=a)\end{cases}\]
가 구간 \([-3,\,\infty)\)에서 연속일 때, 상수 \(a\)의 값은? (단, \(a>-3\)){PT}""", ["11", "12", "13", "14", "15"]
Q[4] = r"""다항함수 \(f(x)\)가
\[\lim_{x\to\infty}\frac{f(x)-x^3}{2x}=3,\quad \lim_{x\to0}f(x)=-5\]
를 만족시킬 때, \(f(2)\)의 값은?{PT}""", ["15", "17", "19", "21", "23"]
Q[5] = r"""두 함수 \(f(x)\), \(g(x)\)가
\[\lim_{x\to1}(x+1)f(x)=6,\quad \lim_{x\to1}\frac{f(x)g(x)}{x+2}=4\]
를 만족시킬 때, \(\displaystyle\lim_{x\to1}\frac{g(x)}{2x+6}\)의 값은?{PT}""", [r"\dfrac18", r"\dfrac14", r"\dfrac38", r"\dfrac12", r"\dfrac58"]
Q[6] = r"""다항함수 \(f(x)\)에 대하여 함수 \(g(x)=3x^2-xf(x)\)라 하자. \(f(2)=1\), \(f'(2)=4\)일 때, \(g'(2)\)의 값은?{PT}""", ["1", "3", "5", "7", "9"]
Q[7] = r"""함수 \(f(x)=x^4+ax+2\)에 대하여 곡선 \(y=f(x)\) 위의 점 \((1,\,f(1))\)에서의 접선의 방정식이 \(y=-3x+b\)일 때, \(a+b\)의 값은? (단, \(a\), \(b\)는 상수이다.){PT}""", ["-10", "-9", "-8", "-7", "-6"]
Q[8] = r"""두 함수
\[f(x)=\begin{cases}x^2-2x+3 & (x<1)\\ 4 & (x\ge1)\end{cases},\quad g(x)=ax-3\]
에 대하여 함수 \(\dfrac{g(x)}{f(x)}\)가 실수 전체의 집합에서 연속일 때, 상수 \(a\)의 값은?{PT}""", ["-1", "0", "1", "2", "3"]
Q[9] = r"""최고차항의 계수가 \(1\)인 이차함수 \(f(x)\)가
\[\lim_{x\to a}\frac{f(x)+2(x-a)}{f(x)-(x-a)}=4\]
를 만족시킨다. 방정식 \(f(x)=0\)의 두 근을 \(\alpha\), \(\beta\)라 할 때, \(|\alpha-\beta|\)의 값은? (단, \(a\)는 상수이다.){PT}""", ["2", "3", "4", "5", "6"]
Q[10] = r"""두 함수 \(f(x)\), \(g(x)\)가
\[\lim_{x\to0}\{xf(x)-(x+3)\}=2,\quad \lim_{x\to0}\left\{\frac{g(x)}{x}-\frac{2}{x+1}\right\}=1\]
을 만족시킬 때, \(\displaystyle\lim_{x\to0}\{f(x)g(x)+xf(x)\}\)의 값은?{PT}""", ["14", "16", "18", "20", "22"]
Q[11] = r"""두 다항함수 \(f(x)\), \(g(x)\)가 모든 실수 \(x\)에 대하여
\[-x^2+7\le f(x)+g(x)\le-2x+8\]
을 만족시키고, \(\displaystyle\lim_{x\to1}\frac{2f(x)+g(x)}{f(x)+2g(x)}=\frac45\)일 때, \(\displaystyle\lim_{x\to1}f(x)g(x)\)의 값은?{PT}""", ["6", "7", "8", "9", "10"]
Q[12] = r"""함수
\[f(x)=\begin{cases}-2x(x-1) & (x<2)\\ (x-4)(x-6) & (x\ge2)\end{cases}\]
일 때, 함수 \(f(x-1)f(x-a)\)가 \(x=3\)에서 연속이 되도록 하는 모든 실수 \(a\)의 값의 합은?{PT}""", ["0", "1", "2", "3", "4"]
Q[13] = r"""일차함수 \(f(x)\)에 대하여
\[\lim_{x\to a}\frac{f(x+1)}{(x-1)\{f(x)-4\}}\]
의 값이 \(a=1\)일 때 존재하고 \(a=4\)일 때 존재하지 않는다. \(f(7)\)의 값은?{PT}""", ["6", "7", "8", "9", "10"]
Q[14] = r"""일차함수 \(f(x)\)와 이차함수 \(g(x)\)가 다음 조건을 만족시킬 때, \(\dfrac{f(1)}{g(0)}\)의 값은?{PT}""" + COND([
            ('가', r"\(\displaystyle\lim_{x\to a}g(x)=0\)인 실수 \(a\)의 집합은 \(\{2\}\)이다."),
            ('나', r"\(\displaystyle\lim_{x\to b}\frac{1}{g(x)-f(x)}\)의 값이 존재하지 않는 실수 \(b\)의 집합은 \(\{-1,\ 3\}\)이다.")]), [r"\dfrac54", r"\dfrac32", r"\dfrac74", "2", r"\dfrac94"]
Q[15] = r"""함수
\[f(x)=\begin{cases}x+1 & (x<1)\\ -2x+6 & (x\ge1)\end{cases}\]
이다. \(\displaystyle\lim_{x\to1}|f(x)-k|\)의 값이 존재하도록 하는 상수 \(k\)에 대하여 \(\displaystyle\lim_{x\to a}\frac{f(x)}{|f(x)-k|}\)의 값이 존재하지 않도록 하는 모든 실수 \(a\)의 값의 합은?{PT}""", ["1", r"\dfrac32", "2", r"\dfrac52", r"\dfrac92"]
Q[16] = r"""다항식 \(f(x)\)를 \((x-3)^2\)으로 나누었을 때의 몫을 \(Q(x)\), 나머지를 \(R(x)\)라 하자. \(Q(3)=R(3)\)일 때,
\[\lim_{x\to3}\frac{f(x)+x^2}{f(x)-R(x)}=k\]
이다. 상수 \(k\)의 값은?{PT}""", [r"\dfrac23", r"\dfrac34", r"\dfrac89", "1", r"\dfrac98"]
Q[17] = r"""사차함수 \(f(x)\)가 다음 조건을 만족시킨다.""" + COND([
            ('가', r"\(5\) 이하의 모든 자연수 \(n\)에 대하여<div style='margin:2pt 0 2pt 1.2em'>\(\displaystyle\sum_{k=1}^{n}f(k)=f(n)f(n+1)\)이다.</div>"),
            ('나', r"\(n=1\), \(4\)일 때, 함수 \(f(x)\)에서 \(x\)의 값이 \(n\)에서 \(n+2\)까지 변할 때의 평균변화율은 양수가 아니다.")]) + \
       r"""\(f(0)\)의 값은?{PT}""", ["-20", "-15", "-10", "-5", "0"]
Q[18] = r"""최고차항의 계수가 \(1\)인 삼차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를
\[g(x)=\begin{cases}f(x)+2x & (f(x)\ge0)\\ 3f(x) & (f(x)<0)\end{cases}\]
이라 할 때, 함수 \(g(x)\)는 다음 조건을 만족시킨다.""" + COND([
            ('가', r"함수 \(g(x)\)가 \(x=t\)에서 불연속인 실수 \(t\)의 개수는 \(1\)이다."),
            ('나', r"함수 \(g(x)\)가 \(x=t\)에서 미분가능하지 않은 실수 \(t\)의 개수는 \(2\)이다.")]) + \
       r"""\(f(-3)=-12\)일 때, \(f(2)\)의 값은?{PT}""", ["18", "50", "72", "98", "128"]
ANS = {1: 2, 2: 5, 3: 3, 4: 1, 5: 4, 6: 2, 7: 3, 8: 5, 9: 1, 10: 4, 11: 3, 12: 2, 13: 5, 14: 1, 15: 4, 16: 3, 17: 2, 18: 4}
Q = {n: (PTS[n - 1],) + tuple(Q[n]) for n in Q}

S1 = r"""최고차항의 계수가 \(1\)인 삼차함수 \(f(x)\)가 다음 조건을 만족시킨다.""" + COND([
            ('가', r"\(\displaystyle\lim_{x\to0}\frac{|f(x)-2|}{x}\)의 값이 존재한다."),
            ('나', r"모든 실수 \(x\)에 대하여 \(xf(x)\ge-9x^2+2x\)이다.")]) + \
     r"""다음 물음에 답하시오."""
S1S = [(r"\(f(0)+f'(0)\)의 값을 구하시오.", "3점"),
       (r"\(f(1)\)의 최댓값을 구하시오.", "3점"),
       (r"\(f(3)\)의 최댓값과 최솟값의 합을 구하시오.", "4점")]
S2 = r"""함수
\[f(x)=\begin{cases}x^2-2x & (x<3,\ x\ne2)\\ 5 & (x=2)\\ x^2-x & (x\ge3)\end{cases}\]
와 이차함수 \(g(x)\)가 다음 조건을 만족시킨다.""" + COND([
            ('가', r"\(\displaystyle\lim_{x\to0}\frac{g(x)}{f(x+2)}=3\)"),
            ('나', r"\(\displaystyle\lim_{x\to-1+}f(2-x)g(x)=\lim_{x\to1+}f(x+2)g(x)\)")]) + \
     r"""다음 물음에 답하시오."""
S2S = [(r"\(g(0)=0\)임을 보이고 \(g'(0)\)의 값을 구하시오.", "2점"),
       (r"(나)의 두 극한을 각각 \(g(-1)\), \(g(1)\)을 이용하여 나타내는 과정을 서술하시오.", "4점"),
       (r"\(g(1)\)의 값을 구하는 과정을 서술하시오.", "4점")]
S1 = S1.replace('<div class="ci">', '<div class="ci" style="margin:4pt 0">')
S2 = S2.replace('<div class="ci">', '<div class="ci" style="margin:4pt 0">')
