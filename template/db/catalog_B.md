# Catalog B — PDF pages 14–26 (미적분Ⅰ 미분 단원)

Notes
- Printed page = 52 + (pdf page − 1) for pdf pages 14–24 (printed 65–75). **PDF page 25 is printed 78 and page 26 is printed 79**: printed pages 76–77 are not in the PDF (probably answer/separator pages).
- Problems 43–44 sit under the **Level Up** banner that starts on PDF p13 (printed 64, problem 41). PDF p15 starts a new **Level Up** banner (45–48). 49–68 are **평가원 기출**. PDF p25 starts a new chapter part: **유형 1 접선의 방정식**, with numbering restarting at 1 (problem 1 under the **대표기출** banner; 2–8 follow with no further sub-banner on these pages).
- Source tags cut at the image edge (closing bracket or "번") were completed in brackets [ ].
- EXCLUDE flags: **59** (distance between (1,f(1)) and (a,f(a)) equals \(a^2-1\); printed as a², not a³, but it is the "distance = a^n−1" problem). No inverse-function / 3-intersection problem occurs on these pages.
- All answers were worked by hand and checked with python/sympy where they were non-trivial (43, 44, 57, 63, 65, 67).

---

## 43 — PDF p14 (printed 65), Level Up (continued)
- Source: 2022년 수능특강 [22009-0074]   - Points: not printed   - Format: short answer   - Figure: none
- Statement:
  함수 \(f(x)\)와 최고차항의 계수가 1인 삼차함수 \(g(x)\)가 다음 조건을 만족시킨다.
  > (가) 임의의 두 실수 \(x_1, x_2\ (x_1<x_2)\)에 대하여 \(x\)의 값이 \(x_1\)에서 \(x_2\)까지 변할 때의 함수 \(y=f(x)\)의 평균변화율은 2로 일정하다.
  > (나) 두 함수 \(y=f(x),\ y=g(x)\)의 그래프는 점 \((1, 3)\)에서 만난다.
  > (다) 함수 \(|f(x)-g(x)|\)가 실수 전체의 집합에서 미분가능하다.

  \(f(3)+g(3)\)의 값을 구하시오.
- **Answer: 22**
- Solution: (가) ⇒ f is linear with slope 2, and (나) gives f(x)=2x+1. h=g−f is a monic cubic with h(1)=0. |h| is differentiable only if every real root has multiplicity ≥2 or is a triple root, so h=(x−1)³. Then f(3)=7 and g(3)=7+8=15, so the sum is 22.
- Difficulty: 6 — needs the fact that |h| is differentiable at a root exactly when the root is not simple, and it combines three conditions.

## 44 — PDF p14 (printed 65), Level Up (continued)
- Source: 2024년 수능특강 [24009-0075]   - Points: not printed   - Format: short answer   - Figure: none
- Statement:
  다항함수 \(f(x)\)가 다음 조건을 만족시킨다.
  > (가) \(\displaystyle\lim_{x\to\infty}\frac{f(x)}{x^3}=2\)
  > (나) \(\displaystyle\lim_{x\to 0}\frac{f(x)-2}{x}=24\)

  함수 \(y=f(x)\)의 그래프와 직선 \(y=2\)는 서로 다른 세 점 A, B, C에서 만나고 점 B는 선분 AC를 \(1:2\)로 내분하는 점일 때, \(f(1)\)의 최댓값을 구하시오. (단, 원점 O에 대하여 \(\overline{\mathrm{OA}}<\overline{\mathrm{OB}}<\overline{\mathrm{OC}}\)이다.)
- **Answer: 44**
- Solution: f(x)=2x³+ax²+24x+2, and f(x)=2 ⇔ x(2x²+ax+24)=0. The distance to O grows with |x|, so A has x=0. B divides AC 1:2, so x_C=3x_B, and x_B·x_C=12 gives x_B=±2, x_C=±6. Then −a/2=±8, a=∓16, and f(1)=28+a has maximum 44 (at a=16).
- Difficulty: 6 — limit conditions plus root/ratio reasoning and a case split.

## 45 — PDF p15 (printed 66), Level Up
- Source: 2025년 수능특강 [25009-0073]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement:
  다항함수 \(f(x)\)와 연속함수 \(g(x)\)가 다음 조건을 만족시킬 때, \(f'(0)\)의 값은?
  > (가) \(f(0)=0,\ g(0)=5\)
  > (나) 모든 양수 \(x\)에 대하여 \(f(x)>0\)이다.
  > (다) 모든 양수 \(t\)에 대하여 점 \((t, f(t))\)와 원점 사이의 거리는 \(tg(t)\)이다.

  ① \(2\sqrt6\)  ② \(5\)  ③ \(\sqrt{26}\)  ④ \(3\sqrt3\)  ⑤ \(2\sqrt7\)
- **Answer: ① \(2\sqrt6\)**
- Solution: For t>0, g(t)=√(1+(f(t)/t)²). Continuity at 0 gives 5=√(1+f'(0)²), so f'(0)²=24. Since f>0 for x>0 and f(0)=0, f'(0)≥0, so f'(0)=2√6.
- Difficulty: 5 — a definition-of-derivative limit hidden inside a distance condition. (It is a distance problem, but not the a^n−1 type; not flagged.)

## 46 — PDF p15 (printed 66), Level Up
- Source: 2025년 수능특강 [25009-0074]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement:
  함수
  \[f(x)=\begin{cases}|x+1| & (x\le 0)\\ 3x+1 & (x>0)\end{cases}\]
  이 있다. 최고차항의 계수가 1인 이차함수 \(g(x)\)에 대하여 함수 \(f(x)g(x)\)가 실수 전체의 집합에서 미분가능할 때, \(g(4)\)의 값은?
  ① 12  ② 14  ③ 16  ④ 18  ⑤ 20
- **Answer: ⑤ 20**
- Solution: f has corners at x=−1 (f=0 there) and at x=0 (slopes 1 and 3, f(0)=1). At −1, g(−1)=0 is needed. At 0, matching g(0)+g'(0)=3g(0)+g'(0) gives g(0)=0. So g=x(x+1) and g(4)=20.
- Difficulty: 5 — standard differentiability of a product with a piecewise function.

## 47 — PDF p16 (printed 67), Level Up
- Source: 2025년 수능특강 [25009-0076]   - Points: not printed   - Format: short answer   - Figure: none
- Statement:
  최고차항의 계수가 1인 이차함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(1)\)의 값을 구하시오.
  > (가) 모든 실수 \(x\)에 대하여 \(f'(x)+f'(8-x)=0\)이다.
  > (나) \(\displaystyle\sum_{k=1}^{10}\lim_{h\to0}\frac{f(k-3+h)-f(k-3-h)}{h}=-f(0)\)
- **Answer: 53**
- Solution: f'(x)=2x+b, and (가) gives 2b+16=0, so b=−8 and f=x²−8x+c. Each limit equals 2f'(k−3)=2(2k−14), and the sum over k=1..10 is −60. So −c=−60, c=60, and f(1)=53.
- Difficulty: 5 — derivative-definition limit combined with Σ.

## 48 — PDF p16 (printed 67), Level Up
- Source: 2025년 수능특강 [25009-0077]   - Points: not printed   - Format: short answer   - Figure: none
- Statement:
  최고차항의 계수가 1인 삼차함수 \(f(x)\)에 대하여 함수
  \[g(x)=\begin{cases} f(x)+2x & (x<-1)\\ -f(x)-x^2+a & (-1\le x<2)\\ f(x)+2x+b & (x\ge 2)\end{cases}\]
  는 실수 전체의 집합에서 미분가능하다. \(f(2)=6\)일 때, \(g(1)+g(3)\)의 값을 구하시오. (단, \(a, b\)는 상수이다.)
- **Answer: 75**
- Solution: The derivative conditions give f'(−1)=0 and f'(2)=−3, so f=x³−2x²−7x+r, and f(2)=6 gives r=20. Continuity: 2f(−1)=1+a gives a=47, and −f(2)−4+a=f(2)+4+b gives b=27. g(1)=−12−1+47=34 and g(3)=8+6+27=41, so the sum is 75.
- Difficulty: 5 — routine continuity/differentiability matching with a lot of algebra.

## 49 — PDF p17 (printed 68), 평가원 기출
- Source: 2009학년도 수능 가형 18번   - Points: [3점]   - Format: short answer   - Figure: none
- Statement: 다항함수 \(f(x)\)에 대하여 \(\displaystyle\lim_{x\to2}\frac{f(x+1)-8}{x^2-4}=5\)일 때, \(f(3)+f'(3)\)의 값을 구하시오. [3점]
- **Answer: 28**
- Solution: f(3)=8, and f'(3)/(2+2)=5 gives f'(3)=20. The sum is 28.
- Difficulty: 3 — basic limit to derivative.

## 50 — PDF p17 (printed 68), 평가원 기출
- Source: 2024학년도 수능 9월 모의평가 18번   - Points: [3점]   - Format: short answer   - Figure: none
- Statement: 함수 \(f(x)=(x^2+1)(x^2+ax+3)\)에 대하여 \(f'(1)=32\)일 때, 상수 \(a\)의 값을 구하시오. [3점]
- **Answer: 5**
- Solution: f'(1)=2(4+a)+2(2+a)=12+4a=32, so a=5.
- Difficulty: 2 — product rule plug-in.

## 51 — PDF p17 (printed 68), 평가원 기출
- Source: 2010학년도 수능 6월 모의평가 가형 6번   - Points: [3점]   - Format: 5-choice   - Figure: none
- Statement: 함수 \(y=f(x)\)의 그래프는 \(y\)축에 대하여 대칭이고, \(f'(2)=-3,\ f'(4)=6\)일 때, \(\displaystyle\lim_{x\to-2}\frac{f(x^2)-f(4)}{f(x)-f(-2)}\)의 값은? [3점]
  ① −8  ② −4  ③ 4  ④ 8  ⑤ 12
- **Answer: ① −8**
- Solution: f is even, so f' is odd and f'(−2)=3. The limit is f'(4)·2(−2)/f'(−2)=6·(−4)/3=−8.
- Difficulty: 4 — symmetry of f' plus a ratio of difference quotients.

## 52 — PDF p17 (printed 68), 평가원 기출
- Source: 2008학년도 수능 6월 모의평가 가형 18번   - Points: [3점]   - Format: short answer   - Figure: none
- Statement: 함수 \(f(x)\)가 \(f(x+2)-f(2)=x^3+6x^2+14x\)를 만족시킬 때, \(f'(2)\)의 값을 구하시오. [3점]
- **Answer: 14**
- Solution: f'(2)=lim_{x→0}(f(2+x)−f(2))/x=lim(x²+6x+14)=14.
- Difficulty: 3 — definition of the derivative.

## 53 — PDF p18 (printed 69), 평가원 기출
- Source: 2021학년도 수능 6월 모의평가 나형 26번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 함수 \(f(x)=x^3-3x^2+5x\)에서 \(x\)의 값이 0에서 \(a\)까지 변할 때의 평균변화율이 \(f'(2)\)의 값과 같게 되도록 하는 양수 \(a\)의 값을 구하시오. [4점]
- **Answer: 3**
- Solution: The average rate is a²−3a+5 and f'(2)=5, so a²−3a=0 and a=3.
- Difficulty: 2 — direct computation (despite the 4점 label).

## 54 — PDF p18 (printed 69), 평가원 기출
- Source: 2026학년도 수능 6월 모의평가 7번   - Points: [3점]   - Format: 5-choice   - Figure: none
- Statement: 다항함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \[g(x)=5x^2+xf(x)\] 라 하자. \(f(3)=2,\ f'(3)=1\)일 때, \(g'(3)\)의 값은? [3점]
  ① 31  ② 32  ③ 33  ④ 34  ⑤ 35
- **Answer: ⑤ 35**
- Solution: g'(x)=10x+f(x)+xf'(x), so g'(3)=30+2+3=35.
- Difficulty: 2 — product rule.

## 55 — PDF p18 (printed 69), 평가원 기출
- Source: 2021학년도 수능 9월 모의평가 나형 10번   - Points: [3점]   - Format: 5-choice   - Figure: none
- Statement: 함수 \[f(x)=\begin{cases}x^3+ax+b & (x<1)\\ bx+4 & (x\ge1)\end{cases}\] 이 실수 전체의 집합에서 미분가능할 때, \(a+b\)의 값은? (단, \(a, b\)는 상수이다.) [3점]
  ① 6  ② 7  ③ 8  ④ 9  ⑤ 10
- **Answer: ④ 9**
- Solution: Continuity: 1+a+b=b+4, so a=3. Derivatives: 3+a=b, so b=6. a+b=9.
- Difficulty: 3 — standard piecewise differentiability.

## 56 — PDF p18 (printed 69), 평가원 기출
- Source: 2013학년도 수능 6월 모의평가 나형 27번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 다항함수 \(f(x)\)가 \(\displaystyle\lim_{x\to1}\frac{f(x)-5}{x-1}=9\)를 만족시킨다. \(g(x)=xf(x)\)라 할 때, \(g'(1)\)의 값을 구하시오. [4점]
- **Answer: 14**
- Solution: f(1)=5 and f'(1)=9, so g'(1)=f(1)+f'(1)=14.
- Difficulty: 3.

## 57 — PDF p19 (printed 70), 평가원 기출
- Source: 2014학년도 수능 예시문항 A형 21번   - Points: [4점]   - Format: 5-choice   - **Figure: yes**
- Statement: 좌표평면 위에 그림과 같이 어두운 부분을 내부로 하는 도형이 있다. 이 도형과 네 점 \((0,0), (t,0), (t,t), (0,t)\)를 꼭짓점으로 하는 정사각형이 겹치는 부분의 넓이를 \(f(t)\)라 하자.
  [그림]
  열린구간 \((0,4)\)에서 함수 \(f(t)\)가 미분가능하지 <u>않은</u> 모든 \(t\)의 값의 합은? [4점]
  ① 2  ② 3  ③ 4  ④ 5  ⑤ 6
- Figure: Axes with ticks 1, 2, 3, 4 on x and 1, 2, 3 on y; O at the origin. The shaded region lies between the x-axis and an upper boundary that runs: horizontal segment y=1 from (0,1) to (1,1); slanted segment from (1,1) to (2,2) (on the line y=x); horizontal y=2 from (2,2) to (3,2); a vertical jump at x=3 from (3,2) up to (3,3); horizontal y=3 from (3,3) to (4,3); then vertical down from (4,3) to (4,0). The left edge is the y-axis from (0,0) to (0,1). Dashed vertical lines at x=1, 2, 3 down to the axis. Dashed horizontals from the y-axis at y=2 to (2,2) and at y=3 to (3,3). Polygon vertices: (0,0),(0,1),(1,1),(2,2),(3,2),(3,3),(4,3),(4,0).
- **Answer: ③ 4**
- Solution: f(t)=∫₀ᵗ min(h(x),t)dx, so f'(t)=min(h(t),t)+|{x<t : h(x)>t}|. That gives f'=2t on (0,1), t on (1,2), 2 on (2,3), and 3 on (3,4). f' jumps at t=1 (2→1) and at t=3 (2→3), and is continuous at t=2 (2=2). The sum is 1+3=4.
- Difficulty: 6 — needs a careful piecewise area function; the t=2 trap.

## 58 — PDF p19 (printed 70), 평가원 기출
- Source: 2022학년도 수능 예시문항 11번   - Points: [4점]   - Format: 5-choice   - Figure: none
- Statement: 최고차항의 계수가 1인 삼차함수 \(f(x)\)가 다음 조건을 만족시킨다.
  > 방정식 \(f(x)=9\)는 서로 다른 세 실근을 갖고, 이 세 실근은 크기 순서대로 등비수열을 이룬다.

  \(f(0)=1,\ f'(2)=-2\)일 때, \(f(3)\)의 값은? [4점]
  ① 6  ② 7  ③ 8  ④ 9  ⑤ 10
- **Answer: ② 7**
- Solution: Take the roots as r/q, r, rq. Their product is r³=9−f(0)=8, so r=2, and the pairwise sum is r·(sum)=2p. So f=x³−px²+2px+1. f'(2)=12−2p=−2 gives p=7, and f(3)=27−63+42+1=7. Check: f−9=(x−1)(x−2)(x−4).
- Difficulty: 6 — Vieta's formulas with a geometric sequence.

## 59 — PDF p20 (printed 71), 평가원 기출  — **EXCLUDE (distance = a²−1 type)**
- Source: 2013학년도 수능 6월 모의평가 가형 16번   - Points: [4점]   - Format: 5-choice   - **Figure: yes**
- Statement: 양의 실수 전체의 집합에서 증가하는 함수 \(f(x)\)가 \(x=1\)에서 미분가능하다. 1보다 큰 모든 실수 \(a\)에 대하여 점 \((1, f(1))\)과 점 \((a, f(a))\) 사이의 거리가 \(a^2-1\)일 때, \(f'(1)\)의 값은? [4점]
  [그림]
  ① 1  ② \(\frac{\sqrt5}{2}\)  ③ \(\frac{\sqrt6}{2}\)  ④ \(\sqrt2\)  ⑤ \(\sqrt3\)
- Figure: An increasing, convex curve labeled y=f(x). It starts slightly left of the y-axis just above the x-axis (minimum near the y-axis), rises through the dot (1, f(1)), and goes steeply up through the dot (a, f(a)). The chord joins the two dots. A dotted horizontal segment runs from (1,f(1)) to x=a, with a right-angle mark at (a, f(1)). Dotted verticals drop to x=1 and x=a on the x-axis. The label "(1, f(1))" has a curved arrow pointing to the lower dot. O at the origin.
- **Answer: ⑤ \(\sqrt3\)**
- Solution: (a−1)²+(f(a)−f(1))²=(a²−1)², and dividing by (a−1)² gives 1+((f(a)−f(1))/(a−1))²=(a+1)². Letting a→1⁺ gives 1+f'(1)²=4, so f'(1)=√3 (f is increasing).
- Difficulty: 6 — turning the distance into a difference quotient.
- **FLAG: distance expression a²−1 (the requested a³−1-style distance problem). EXCLUDE.**

## 60 — PDF p20 (printed 71), 평가원 기출
- Source: 2018학년도 수능 나형 18번   - Points: [4점]   - Format: 5-choice   - Figure: none
- Statement: 최고차항의 계수가 1이고 \(f(1)=0\)인 삼차함수 \(f(x)\)가 \[\lim_{x\to2}\frac{f(x)}{(x-2)\{f'(x)\}^2}=\frac14\] 을 만족시킬 때, \(f(3)\)의 값은? [4점]
  ① 4  ② 6  ③ 8  ④ 10  ⑤ 12
- **Answer: ④ 10**
- Solution: The limit requires f(2)=0, so f=(x−1)(x−2)(x−b). The limit is (2−b)/(2−b)²=1/(2−b)=1/4, so b=−2. (The case b=2 makes the limit diverge.) f(3)=2·1·5=10.
- Difficulty: 5.

## 61 — PDF p21 (printed 72), 평가원 기출
- Source: 2008학년도 수능 9월 모의평가 가형 22번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 두 다항함수 \(f(x), g(x)\)가 다음 조건을 만족시킬 때, \(g'(0)\)의 값을 구하시오. [4점]
  > (가) \(f(0)=1,\ f'(0)=-6,\ g(0)=4\)
  > (나) \(\displaystyle\lim_{x\to0}\frac{f(x)g(x)-4}{x}=0\)
- **Answer: 24**
- Solution: (fg)'(0)=f'(0)g(0)+f(0)g'(0)=−24+g'(0)=0, so g'(0)=24.
- Difficulty: 3.

## 62 — PDF p21 (printed 72), 평가원 기출
- Source: 2021학년도 수능 9월 모의평가 나형 18번   - Points: [4점]   - Format: 5-choice   - Figure: none
- Statement: 최고차항의 계수가 \(a\)인 이차함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \[|f'(x)|\le 4x^2+5\] 를 만족시킨다. 함수 \(y=f(x)\)의 그래프의 대칭축이 직선 \(x=1\)일 때, 실수 \(a\)의 최댓값은? [4점]
  ① \(\frac32\)  ② 2  ③ \(\frac52\)  ④ 3  ⑤ \(\frac72\)
- **Answer: ② 2**
- Solution: f'(x)=2a(x−1). We need 4x²−2ax+5+2a≥0 and 4x²+2ax+5−2a≥0 for all x. The discriminants give −2≤a≤10 and −10≤a≤2, so the maximum is 2.
- Difficulty: 6 — inequality between graphs and a discriminant (tangency) idea.

## 63 — PDF p22 (printed 73), 평가원 기출
- Source: 2025학년도 수능 9월 모의평가 21번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 최고차항의 계수가 1인 삼차함수 \(f(x)\)가 모든 정수 \(k\)에 대하여 \[2k-8\le\frac{f(k+2)-f(k)}{2}\le4k^2+14k\] 를 만족시킬 때, \(f'(3)\)의 값을 구하시오. [4점]
- **Answer: 31**
- Solution: With f=x³+ax²+bx+c, the middle term is 3k²+(6+2a)k+4+2a+b. At k=−1 it is squeezed between −10 and −10, so b=−11. Then k=0 gives −1/2≤a≤7/2, and k=1 and k=2 pin a=5/2 (checked numerically for all integers). f'(3)=27+6a+b=27+15−11=31.
- Difficulty: 8 — a squeeze at an integer point is the key insight; this is a 21번 killer.

## 64 — PDF p22 (printed 73), 평가원 기출
- Source: 2018학년도 수능 6월 모의평가 나형 30번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 최고차항의 계수가 1인 삼차함수 \(f(x)\)와 최고차항의 계수가 2인 이차함수 \(g(x)\)가 다음 조건을 만족시킨다.
  > (가) \(f(\alpha)=g(\alpha)\)이고 \(f'(\alpha)=g'(\alpha)=-16\)인 실수 \(\alpha\)가 존재한다.
  > (나) \(f'(\beta)=g'(\beta)=16\)인 실수 \(\beta\)가 존재한다.

  \(g(\beta+1)-f(\beta+1)\)의 값을 구하시오. [4점]
- **Answer: 243**
- Solution: With g'=4x+c, g'(β)−g'(α)=32 gives β−α=8. h=f−g=(x−α)²(x−γ) has h'=(x−α)(3x−α−2γ)=0 at β, so β−α=2(γ−α)/3 and γ−α=12. g(β+1)−f(β+1)=−h(β+1)=−9²·(−3)=243.
- Difficulty: 7 — a 30번 in its year; needs the factored form of f−g.

## 65 — PDF p23 (printed 74), 평가원 기출
- Source: 2017학년도 수능 6월 모의평가 나형 29번   - Points: [4점]   - Format: short answer   - **Figure: yes**
- Statement: 함수 \(f(x)\)는 \[f(x)=\begin{cases}x+1 & (x<1)\\ -2x+4 & (x\ge1)\end{cases}\] 이고, 좌표평면 위에 두 점 A\((-1,-1)\), B\((1,2)\)가 있다. 실수 \(x\)에 대하여 점 \((x, f(x))\)에서 점 A까지의 거리의 제곱과 점 B까지의 거리의 제곱 중 크지 않은 값을 \(g(x)\)라 하자. 함수 \(g(x)\)가 \(x=a\)에서 미분가능하지 않은 모든 \(a\)의 값의 합이 \(p\)일 때, \(80p\)의 값을 구하시오. [4점]
- Figure: Graph of y=f(x): a line rising through (−1,0) to the peak B(1,2) (dot labeled B), then a line falling through (2,0) and continuing down-right, labeled y=f(x). Point A(−1,−1) is a dot below the x-axis. Dotted lines: a vertical from (−1,0) down to A, and a horizontal from A to the y-axis tick −1. For B: a dotted horizontal to the y-axis tick 2 and a dotted vertical to x=1. Ticks: x-axis −1, 1, 2; y-axis 2, −1; O at the origin.
- **Answer: 186**
- Solution: For x<1, dA²=2x²+6x+5 and dB²=2x²−4x+2, equal at x=−3/10. For x≥1, dA²=5x²−18x+26 and dB²=5x²−10x+5, equal at x=21/8. The slopes differ at both crossings, so g is not differentiable there. At x=1, g=dB² has derivative 0 on both sides, so it is differentiable. p=−3/10+21/8=93/40, and 80p=186.
- Difficulty: 7 — the min-function setup and the x=1 trap.

## 66 — PDF p23 (printed 74), 평가원 기출
- Source: 2020학년도 수능 나형 20번   - Points: [4점]   - Format: 5-choice (보기)   - Figure: none
- Statement: 함수 \[f(x)=\begin{cases}-x & (x\le0)\\ x-1 & (0<x\le2)\\ 2x-3 & (x>2)\end{cases}\] 와 상수가 아닌 다항식 \(p(x)\)에 대하여 <보기>에서 옳은 것만을 있는 대로 고른 것은? [4점]
  > ㄱ. 함수 \(p(x)f(x)\)가 실수 전체의 집합에서 연속이면 \(p(0)=0\)이다.
  > ㄴ. 함수 \(p(x)f(x)\)가 실수 전체의 집합에서 미분가능하면 \(p(2)=0\)이다.
  > ㄷ. 함수 \(p(x)\{f(x)\}^2\)이 실수 전체의 집합에서 미분가능하면 \(p(x)\)는 \(x^2(x-2)^2\)으로 나누어떨어진다.

  ① ㄱ  ② ㄱ, ㄴ  ③ ㄱ, ㄷ  ④ ㄴ, ㄷ  ⑤ ㄱ, ㄴ, ㄷ
- **Answer: ② ㄱ, ㄴ**
- Solution: ㄱ: f jumps 0→−1 at x=0, so p(0)=0. True. ㄴ: at x=2, f is continuous with slopes 1 and 2, so p'(2)+p(2)=p'(2)+2p(2) and p(2)=0. True. ㄷ: this forces x²∣p and p(2)=0 only. p=x²(x−2) works, so ㄷ is false.
- Difficulty: 7.

## 67 — PDF p24 (printed 75), 평가원 기출
- Source: 2019학년도 수능 6월 모의평가 나형 30번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 사차함수 \(f(x)\)가 다음 조건을 만족시킨다.
  > (가) 5 이하의 모든 자연수 \(n\)에 대하여 \(\displaystyle\sum_{k=1}^{n}f(k)=f(n)f(n+1)\)이다.
  > (나) \(n=3, 4\)일 때, \(f(x)\)에서 \(x\)의 값이 \(n\)에서 \(n+2\)까지 변할 때의 평균변화율은 양수가 아니다.

  \(128\times f\!\left(\frac52\right)\)의 값을 구하시오. [4점]
- **Answer: 65**
- Solution: Subtracting consecutive sums gives, for each n=2..5, f(n)=0 or f(n+1)−f(n−1)=1, and for n=1, f(1)=0 or f(2)=1. Of the 2⁵ cases (enumerated with sympy), the only quartic satisfying (나) [f(5)−f(3)≤0, f(6)−f(4)≤0] has f(1)=−1, f(2)=1, f(3)=f(4)=f(5)=0, f(6)=−6. That is f(x)=−(5/24)x⁴+(11/4)x³−(307/24)x²+(97/4)x−15 = −(x−3)(x−4)(x−5)(5x−6)/24, and 128f(5/2)=65.
- Difficulty: 9 — heavy casework; a 30번 killer.

## 68 — PDF p24 (printed 75), 평가원 기출
- Source: 2028학년도 수능 예시문항 28번   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: 두 상수 \(a, k\ (k>0)\)과 함수 \(f(x)=x(x-1)^2(x-2)\)에 대하여 함수 \(g(x)\)는 \[g(x)=f(x-a)\] 이고 다음 조건을 만족시키는 함수 \(h(x)\)가 존재할 때, \(a+20k^2\)의 값을 구하시오. [4점]
  > (가) 함수 \(h(x)\)는 실수 전체의 집합에서 연속이다.
  > (나) 모든 실수 \(x\)에 대하여 \((|x|-k)h(x)=|g(x)-g(k)|\)이다.
- **Answer: 9**
- Solution: At x=−k, 0=|g(−k)−g(k)|, so g(−k)=g(k). For h=|g(x)−g(k)|/(|x|−k) to be continuous at x=±k, we need g'(k)=g'(−k)=0. f=u²−u with u=(x−1)² has critical points x=1 (value 0) and x=1±1/√2 (value −1/4). The equal-valued symmetric pair forces a+1=0, so a=−1 and k=1/√2. a+20k²=−1+10=9.
- Difficulty: 8 — differentiability-to-continuity translation plus symmetry of the quartic.

---

## 유형 1 접선의 방정식 — 1 — PDF p25 (printed 78), 대표기출
- Source: 2024학년도 대수능 20번 [24107-0113]   - Points: [4점]   - Format: short answer   - Figure: none
- Statement: \(a>\sqrt2\)인 실수 \(a\)에 대하여 함수 \(f(x)\)를 \[f(x)=-x^3+ax^2+2x\] 라 하자. 곡선 \(y=f(x)\) 위의 점 \(\mathrm O(0,0)\)에서의 접선이 곡선 \(y=f(x)\)와 만나는 점 중 O가 아닌 점을 A라 하고, 곡선 \(y=f(x)\) 위의 점 A에서의 접선이 \(x\)축과 만나는 점을 B라 하자. 점 A가 선분 OB를 지름으로 하는 원 위의 점일 때, \(\overline{\mathrm{OA}}\times\overline{\mathrm{AB}}\)의 값을 구하시오. [4점]
- **Answer: 25**
- Solution: The tangent at O is y=2x, which meets the curve again at A=(a,2a). The tangent slope at A is 2−a². OA⊥AB gives 2(2−a²)=−1, so a²=5/2. Then B=(5a,0), OA=√5a, AB=2√5a, and the product is 10a²=25.
- Difficulty: 6 — a 수능 20번 with several steps, but each is standard.

## 유형 1 — 2 — PDF p25 (printed 78)
- Source: 2023년 수능특강 [23009-0074]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement: 다항함수 \(f(x)\)에 대하여 곡선 \(y=x^2f(x)\) 위의 점 \((1, 2)\)에서의 접선의 기울기가 3일 때, 곡선 \(y=f(x)\) 위의 점 \((1, f(1))\)에서의 접선의 \(y\)절편은?
  ① 1  ② 2  ③ 3  ④ 4  ⑤ 5
- **Answer: ③ 3**
- Solution: f(1)=2, and 2f(1)+f'(1)=3 gives f'(1)=−1. The tangent is y=−x+3, so the y-intercept is 3.
- Difficulty: 3.

## 유형 1 — 3 — PDF p25 (printed 78)
- Source: 2025년 수능특강 [25009-0081]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement: 함수 \(f(x)=x^3+ax^2+bx\)가 다음 조건을 만족시킬 때, \(f(1)\)의 값은? (단, \(a, b\)는 상수이다.)
  > (가) 닫힌구간 \([0, 2]\)에서 평균값 정리를 만족시키는 상수 \(c\)의 값은 \(\frac23\)이다.
  > (나) \(f'(3)=0\)

  ① −8  ② −7  ③ −6  ④ −5  ⑤ −4
- **Answer: ③ −6**
- Solution: (f(2)−f(0))/2=4+2a+b=f'(2/3)=4/3+4a/3+b gives a=−4. f'(3)=27−24+b=0 gives b=−3. f(1)=1−4−3=−6. Check: f'(x)=−7 gives 3x²−8x+4=0, so x=2/3 or 2; the only c in (0,2) is 2/3.
- Difficulty: 4 — the mean value theorem in equation form.

## 유형 1 — 4 — PDF p25 (printed 78)
- Source: 2024년 수능특강 [24009-0076]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement: 함수 \(f(x)=x^4+ax+4\)에 대하여 곡선 \(y=f(x)\) 위의 점 \((1, f(1))\)에서의 접선의 방정식이 \(y=-2x+b\)일 때, \(a+b\)의 값은? (단, \(a, b\)는 상수이다.)
  ① −5  ② −4  ③ −3  ④ −2  ⑤ −1
- **Answer: ① −5**
- Solution: f'(1)=4+a=−2, so a=−6. f(1)=−1=−2+b, so b=1. a+b=−5.
- Difficulty: 2.

## 유형 1 — 5 — PDF p26 (printed 79)
- Source: 2022년 수능완성 [22054-0132]   - Points: not printed   - Format: 5-choice   - **Figure: yes**
- Statement: 함수 \(f(x)=x^3-2x\)에 대하여 곡선 \(y=f(x)\) 위의 점 A\((-1, 1)\)에서의 접선이 이 곡선과 만나는 점 중 A가 아닌 점을 B\((b, f(b))\)라 하자. 직선 \(x=k\ (-1<k<b)\)가 곡선 \(y=f(x)\)와 만나는 점을 \(\mathrm P_k\)라 할 때, 삼각형 \(\mathrm{AP}_k\mathrm B\)의 넓이의 최댓값은?
  ① 5  ② \(\frac{21}{4}\)  ③ \(\frac{11}{2}\)  ④ \(\frac{23}{4}\)  ⑤ 6
- Figure: The cubic y=f(x)=x³−2x (labeled), with a local max near A and a local min below the x-axis right of O. The tangent line at A(−1,1) (y=x+2) crosses the curve again at B(2,4) in the upper right. P_k is a point on the curve slightly right of the y-axis, below the x-axis. Triangle A–P_k–B is shaded. Labels A, B, P_k, O; axes x, y.
- **Answer: ⑤ 6**
- Solution: The tangent is y=x+2, and x³−3x−2=(x+1)²(x−2) gives b=2. The area is ½·3·(k+2−k³+2k)=(3/2)(−k³+3k+2), maximized at k=1 where it equals (3/2)·4=6.
- Difficulty: 5.

## 유형 1 — 6 — PDF p26 (printed 79)
- Source: 2023년 수능완성 [23054-0130]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement: 다음 조건을 만족시키는 모든 다항함수 \(f(x)\)에 대하여 \(f(2)\)의 최댓값을 \(M\), 최솟값을 \(m\)이라 할 때, \(M-m\)의 값은?
  > (가) \(f(4)=10\)
  > (나) \(2<x<4\)인 모든 실수 \(x\)에 대하여 \(|f'(x)|\le6\)이다.

  ① 18  ② 20  ③ 22  ④ 24  ⑤ 26
- **Answer: ④ 24**
- Solution: By the mean value theorem, |f(4)−f(2)|=2|f'(c)|≤12, so −2≤f(2)≤22. Both ends are attained by f=6x−14 and f=−6x+34. M−m=24.
- Difficulty: 5 — mean value theorem as a bound.

## 유형 1 — 7 — PDF p26 (printed 79)
- Source: 2025년 수능완성 [25054-0143]   - Points: not printed   - Format: short answer   - **Figure: yes**
- Statement: 최고차항의 계수가 양수인 삼차함수 \(f(x)\)에 대하여 그림과 같이 곡선 \(y=f(x)\)와 직선 \(y=\frac12x\)가 서로 다른 세 점 O, A, B에서 만난다. 곡선 \(y=f(x)\) 위의 점 A에서의 접선이 \(x\)축과 만나는 점을 C라 하자. \(\overline{\mathrm{OA}}=\overline{\mathrm{AB}}\)이고 \(\overline{\mathrm{OC}}=\overline{\mathrm{BC}}=\frac52\)일 때, \(f(6)\)의 값을 구하시오. (단, 점 A의 \(x\)좌표는 양수이고, O는 원점이다.)
- Figure: A cubic with positive leading coefficient through the origin O. It rises steeply to a local max in the first quadrant, comes down through A, dips to a local min just below the x-axis, then rises steeply through B. The line y=½x (labeled) passes through O, A, B. A steep negative-slope line (the tangent at A) comes from the upper left, passes through A, and crosses the x-axis at C (C labeled with an arrow; C is between A's and B's x-coordinates, very close to where the curve crosses the x-axis). A segment joins C to B. Labels O, A, B, C, y=f(x), y=½x.
- **Answer: 33**
- Solution: OA=AB means A=(t,t/2) and B=(2t,t). OC=5/2 gives C=(5/2,0), and BC=5/2 gives 5t²=10t, so t=2. The tangent slope at A is (0−1)/(5/2−2)=−2. With f(x)−x/2=px(x−2)(x−4), f'(2)=1/2−4p=−2 gives p=5/8. f(6)=3+(5/8)·48=33.
- Difficulty: 7 — combining geometry with the factor form.

## 유형 1 — 8 — PDF p26 (printed 79)
- Source: 2024년 수능완성 [24054-0116]   - Points: not printed   - Format: 5-choice   - Figure: none
- Statement: 두 함수 \(f(x)=x^3-3x^2+2x+a,\ g(x)=x^2+bx+c\)가 다음 조건을 만족시킬 때, \(|abc|\)의 값은? (단, \(a, b, c\)는 상수이다.)
  > (가) 두 곡선 \(y=f(x), y=g(x)\)가 점 A\((1, 2)\)에서 만난다.
  > (나) 곡선 \(y=f(x)\) 위의 점 A에서의 접선과 곡선 \(y=g(x)\) 위의 점 A에서의 접선이 서로 수직이다.

  ① \(\frac52\)  ② 3  ③ \(\frac72\)  ④ 4  ⑤ \(\frac92\)
- **Answer: ④ 4**
- Solution: f(1)=a=2. f'(1)=−1, so g'(1)=2+b=1 and b=−1. g(1)=1−1+c=2, so c=2. |abc|=4.
- Difficulty: 3.
