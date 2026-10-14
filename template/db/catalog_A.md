# Catalog A — 미적분Ⅰ 미분 workbook, PDF pages 01–13 (printed pp. 52–64), problems 1–42

Notes
- Section headings: each 유형 opens with a single dark "대표기출" bar under the 유형 title. No separate "유형 연습" bar appears anywhere on these pages, so every problem until the next 유형 title or Level Up banner is listed under that 유형's 대표기출 heading. Level Up pages (pp. 60–64) have a "Level Up" banner.
- Point values are printed only on the 평가원/수능 기출 items (1, 9, 17, 25).
- None of the problems 1–42 has a figure or graph.
- None of the problems 1–42 has an a^3−1 distance expression or an inverse-function three-intersection setup, so nothing is marked EXCLUDE.
- Answers were checked by hand, and the harder ones also with sympy.

---

## Problem 1
- PDF page 01 (L), printed p.52 | 유형1 미분계수 — 대표기출
- Source: 2022학년도 대수능 9월 모의평가 19번 [22107-0075] | [3점]
- Statement: 함수 \(f(x)=x^3-6x^2+5x\)에서 \(x\)의 값이 0에서 4까지 변할 때의 평균변화율과 \(f'(a)\)의 값이 같게 되도록 하는 \(0<a<4\)인 모든 실수 \(a\)의 값의 곱은 \(\dfrac{q}{p}\)이다. \(p+q\)의 값을 구하시오. (단, \(p\)와 \(q\)는 서로소인 자연수이다.)
- Short answer. Figure: none.
- **Answer: 11**
- Solution: average rate \(=\frac{f(4)-f(0)}{4}=\frac{-12}{4}=-3\). \(3a^2-12a+5=-3\Rightarrow 3a^2-12a+8=0\), roots \(2\pm\frac{2\sqrt3}{3}\), both in (0,4). The product is \(8/3\), so \(p+q=11\).
- Difficulty: 3. Direct mean-value setup plus Vieta's formulas, with a check that both roots lie in (0,4).

## Problem 2
- PDF page 01 (L), printed p.52 | 유형1 미분계수 — 대표기출
- Source: 2025년 수능특강 [25009-0053] | no points printed
- Statement: 함수 \(f(x)=x^2+ax+b\)가 다음 조건을 만족시킨다.
  (가) \(x\)의 값이 0에서 2까지 변할 때의 함수 \(y=f(x)\)의 평균변화율은 4이다.
  (나) \(\displaystyle\lim_{x\to-1}\frac{f(x)-f(-1)}{x^2-1}=f(1)\)
  \(ab\)의 값은? (단, \(a,\ b\)는 상수이다.)
- Choices: ① −2 ② −4 ③ −6 ④ −8 ⑤ −10. Figure: none.
- **Answer: ③ −6**
- Solution: (가) \(\frac{4+2a}{2}=4\Rightarrow a=2\). (나) the limit is \(\frac{f'(-1)}{-2}=\frac{-2+a}{-2}=0\), so \(f(1)=1+a+b=0\Rightarrow b=-3\). Then \(ab=-6\).
- Difficulty: 3. Two routine conditions; you need to see that (나) is a derivative divided by \(x-1\).

## Problem 3
- PDF page 01 (R), printed p.52 | 유형1 미분계수 — 대표기출
- Source: 2023년 수능완성 [23054-0122]
- Statement: 다항함수 \(f(x)\)에 대하여 \(f(3)=2\)이고 \(\displaystyle\lim_{h\to0}\frac{\{f(3+h)\}^2-\{f(3)\}^2}{2h}=16\)일 때, \(f'(3)\)의 값은?
- Choices: ① 6 ② 7 ③ 8 ④ 9 ⑤ 10. Figure: none.
- **Answer: ③ 8**
- Solution: factor the difference of squares. The limit is \(\frac12\cdot 2f(3)\cdot f'(3)=2f'(3)=16\), so \(f'(3)=8\).
- Difficulty: 2. A single step of difference-of-squares factoring.

## Problem 4
- PDF page 01 (R), printed p.52 | 유형1 미분계수 — 대표기출
- Source: 2023년 수능완성 [23054-0123]
- Statement: 두 다항함수 \(f(x),\ g(x)\)가 \[\lim_{x\to1}\frac{f(x)+3}{x-1}=4,\quad \lim_{x\to1}\frac{f(x)+g(x)}{x-1}=10\] 을 만족시킨다. \(g(1)+g'(1)\)의 값은?
- Choices: ① 6 ② 7 ③ 8 ④ 9 ⑤ 10. Figure: none.
- **Answer: ④ 9**
- Solution: \(f(1)=-3,\ f'(1)=4\). Next, \(f(1)+g(1)=0\Rightarrow g(1)=3\) and \(f'(1)+g'(1)=10\Rightarrow g'(1)=6\). Sum \(=9\).
- Difficulty: 3. Standard "0/0 means the numerator vanishes" reasoning.

## Problem 5
- PDF page 02 (L), printed p.53 | 유형1 미분계수 — 대표기출
- Source: 2022년 수능특강 [22009-0051]
- Statement: 함수 \(f(x)=x^2+1\)에 대하여 \(x\)의 값이 1에서 4까지 변할 때의 함수 \(y=f(x)\)의 평균변화율이 \(x=c\)에서의 미분계수와 같도록 하는 상수 \(c\)의 값은?
- Choices: ① \(\frac32\) ② 2 ③ \(\frac52\) ④ 3 ⑤ \(\frac72\). Figure: none.
- **Answer: ③ 5/2**
- Solution: average rate \(=\frac{17-2}{3}=5=2c\), so \(c=\frac52\).
- Difficulty: 1. Definition plug-in.

## Problem 6
- PDF page 02 (L), printed p.53 | 유형1 미분계수 — 대표기출
- Source: 2025년 수능완성 [25054-0130]
- Statement: 두 다항함수 \(f(x),\ g(x)\)가 \[\lim_{x\to0}\frac{f(x)-g(x)}{x}=2,\quad \lim_{x\to0}\frac{g(2x)-x}{f(x)-2x}=4\] 를 만족시킬 때, \(f'(0)+g'(0)\)의 값은?
- Choices: ① 1 ② 2 ③ 3 ④ 4 ⑤ 5. Figure: none.
- **Answer: ① 1**
- Solution: \(f(0)=g(0)\). If this common value were nonzero, the second limit would equal 1, so \(f(0)=g(0)=0\). Then \(\frac{2g'(0)-1}{f'(0)-2}=4\) and \(f'(0)-g'(0)=2\) give \(g'(0)=-\frac12,\ f'(0)=\frac32\). Sum \(=1\).
- Difficulty: 5. Requires the case argument that rules out \(f(0)\neq0\).

## Problem 7
- PDF page 02 (R), printed p.53 | 유형1 미분계수 — 대표기출
- Source: 2024년 수능완성 [24054-0107]
- Statement: 다항함수 \(f(x)\)에 대하여 \(\displaystyle\lim_{h\to0}\frac{f(1+2h)-f(1)}{h}=4\)일 때, \(\displaystyle\lim_{h\to0}\frac{f\!\left(1+\frac h2\right)-f\!\left(1-\frac h3\right)}{h}\)의 값은?
- Choices: ① 1 ② \(\frac76\) ③ \(\frac43\) ④ \(\frac32\) ⑤ \(\frac53\). Figure: none.
- **Answer: ⑤ 5/3**
- Solution: \(2f'(1)=4\Rightarrow f'(1)=2\). The second limit is \(\left(\frac12+\frac13\right)f'(1)=\frac56\cdot2=\frac53\).
- Difficulty: 2. Coefficient bookkeeping in the limit definition.

## Problem 8
- PDF page 02 (R), printed p.53 | 유형1 미분계수 — 대표기출
- Source: 2024년 수능특강 [24009-0052]
- Statement: 다항함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(\displaystyle\lim_{x\to-2}\frac{f(x)-f(-2)}{x^2+5x+6}\)의 값을 구하시오.
  (가) \(x\)의 값이 \(-2\)에서 1까지 변할 때의 함수 \(y=f(x)\)의 평균변화율과 \(x=-2\)에서의 미분계수가 서로 같다.
  (나) \(\displaystyle\lim_{h\to0}\frac{f(-2-h)-(1-h)f(-2)}{h}=f(1)-60\)
- Short answer. Figure: none.
- **Answer: 15**
- Solution: (나) \(=\lim\frac{f(-2-h)-f(-2)}{h}+f(-2)=-f'(-2)+f(-2)=f(1)-60\). (가) gives \(f(1)-f(-2)=3f'(-2)\). Combining, \(4f'(-2)=60\Rightarrow f'(-2)=15\). The requested limit is \(\frac{f'(-2)}{x+3}\big|_{x=-2}=15\).
- Difficulty: 5. You have to split the \((1-h)f(-2)\) term and combine the two conditions.

## Problem 9
- PDF page 03 (L), printed p.54 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2018학년도 대수능 6월 모의평가 나형 16번 [9107-0161] | [4점]
- Statement: 함수 \[f(x)=\begin{cases}x^2+ax+b & (x\le-2)\\ 2x & (x>-2)\end{cases}\] 가 실수 전체의 집합에서 미분가능할 때, \(a+b\)의 값은? (단, \(a\)와 \(b\)는 상수이다.)
- Choices: ① 6 ② 7 ③ 8 ④ 9 ⑤ 10. Figure: none.
- **Answer: ⑤ 10**
- Solution: slopes \(-4+a=2\Rightarrow a=6\). Continuity \(4-12+b=-4\Rightarrow b=4\). Sum \(=10\).
- Difficulty: 2. A textbook piecewise-differentiability exercise.

## Problem 10
- PDF page 03 (L), printed p.54 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2025년 수능특강 [25009-0054]
- Statement: 함수 \[f(x)=\begin{cases}(x+a)(x+b) & (x<1)\\ ax+b & (x\ge1)\end{cases}\] 이 \(x=1\)에서 미분가능할 때, \(a+b\)의 값은? (단, \(a,\ b\)는 상수이다.)
- Choices: ① \(-\frac12\) ② −1 ③ \(-\frac32\) ④ −2 ⑤ \(-\frac52\). Figure: none.
- **Answer: ③ −3/2**
- Solution: continuity \((1+a)(1+b)=a+b\Rightarrow ab=-1\). Slopes \(2+a+b=a\Rightarrow b=-2\), then \(a=\frac12\). Sum \(=-\frac32\).
- Difficulty: 3. Routine, though the algebra is slightly nonlinear.

## Problem 11
- PDF page 03 (R), printed p.54 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2023년 수능완성 [23054-0125]
- Statement: 함수 \(f(x)\)가 \[f(x)=\begin{cases}x^2-1 & (x<0)\\ 1-x^3 & (0\le x<1)\\ 3-3x & (x\ge1)\end{cases}\] 일 때, <보기>에서 옳은 것만을 있는 대로 고른 것은?
  ㄱ. \(\displaystyle\lim_{x\to0-}\frac{f(x)+1}{x}=0\)
  ㄴ. 함수 \(f(x)\)는 \(x=0\)에서 미분가능하다.
  ㄷ. 함수 \(|f(x)|\)는 \(x=1\)에서 미분가능하다.
- Choices: ① ㄱ ② ㄴ ③ ㄱ, ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ. Figure: none.
- **Answer: ① ㄱ**
- Solution: ㄱ: for \(x<0\), \(\frac{x^2}{x}=x\to0\), true. ㄴ: \(f(0)=1\) but the left limit is \(-1\), so f is discontinuous and ㄴ is false. ㄷ: \(f(1)=0\) and both one-sided slopes are \(-3\neq0\), so \(|f|\) has slopes \(-3\) and \(+3\) at 1. Not differentiable, false.
- Difficulty: 4. A three-statement 보기 check on continuity, differentiability and |f|.

## Problem 12
- PDF page 03 (R), printed p.54 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2023년 수능완성 [23054-0126]
- Statement: 함수 \(f(x)\)가 다음 조건을 만족시킨다.
  (가) \(0\le x\le k\)일 때, \(f(x)=x^3-6x^2+10x\)
  (나) 모든 실수 \(x\)에 대하여 \(f(x+k)=f(x)+f(k)\)이다.
  함수 \(f(x)\)가 실수 전체의 집합에서 미분가능하도록 하는 양수 \(k\)의 값은?
- Choices: ① 1 ② 2 ③ 3 ④ 4 ⑤ 5. Figure: none.
- **Answer: ④ 4**
- Solution: by (나), f near \(x=k^+\) is a shift of f near \(0^+\), so the right derivative at \(k\) is \(f'(0)=10\). The left derivative is \(3k^2-12k+10\). Setting them equal gives \(k=4\). Continuity holds automatically because \(f(0)=0\).
- Difficulty: 5. The functional equation must be read as matching slopes at the junction.

## Problem 13
- PDF page 04 (L), printed p.55 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2022년 수능특강 [22009-0052]
- Statement: 함수 \[f(x)=\begin{cases}3x^2-x+2 & (x\le0)\\ ax+b & (x>0)\end{cases}\] 이 \(x=0\)에서 미분가능할 때, \(f(b)\)의 값은? (단, \(a,\ b\)는 상수이다.)
- Choices: ① 0 ② 1 ③ 2 ④ 3 ⑤ 4. Figure: none.
- **Answer: ① 0**
- Solution: \(b=2\) and \(a=-1\). Then \(f(b)=f(2)=-2+2=0\).
- Difficulty: 2. Direct application.

## Problem 14
- PDF page 04 (L), printed p.55 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2025년 수능완성 [25054-0134]
- Statement: 실수 전체의 집합에서 연속인 함수 \[f(x)=\begin{cases}x^2+a & (x<1)\\ -3x^2+bx+c & (x\ge1)\end{cases}\] 에 대하여 함수 \(|f(x)|\)가 \(x=3\)에서만 미분가능하지 않을 때, \(a+b+c\)의 값은? (단, \(a,\ b,\ c\)는 상수이고, \(a>0\)이다.)
- Choices: ① 12 ② 14 ③ 16 ④ 18 ⑤ 20. Figure: none.
- **Answer: ④ 18**
- Solution: \(f(1)=1+a>0\), so \(|f|\) differentiable at 1 means f is differentiable at 1: \(2=-6+b\Rightarrow b=8\). The only kink must be at a sign change at \(x=3\): \(-27+24+c=0\Rightarrow c=3\). Then \(-3x^2+8x+3=-(3x+1)(x-3)\), whose only root with \(x\ge1\) is 3. Continuity gives \(1+a=8\Rightarrow a=7\). Sum \(=18\).
- Difficulty: 6. Combines continuity, differentiability and absolute-value kinks.

## Problem 15
- PDF page 04 (R), printed p.55 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2024년 수능특강 [24009-0053]
- Statement: 함수 \[f(x)=\begin{cases}(ax-3)(x+a) & (x<1)\\ 4ax+4 & (x\ge1)\end{cases}\] 이 실수 전체의 집합에서 미분가능할 때, 상수 \(a\)의 값은?
- Choices: ① −1 ② 1 ③ 3 ④ 5 ⑤ 7. Figure: none.
- **Answer: ① −1**
- Solution: continuity \((a-3)(1+a)=4(a+1)\Rightarrow a=-1\) or \(7\). Slopes \(a^2+2a-3=4a\Rightarrow a=3\) or \(-1\). The common value is \(a=-1\).
- Difficulty: 3. Intersecting two quadratic conditions, with distractors 7 and 3 among the choices.

## Problem 16
- PDF page 04 (R), printed p.55 | 유형2 미분가능성과 연속 — 대표기출
- Source: 2024년 수능완성 [24054-0111]
- Statement: 함수 \(f(x)=(x-2)\left|(x-a)(x-b)^2\right|\)이 실수 전체의 집합에서 미분가능하도록 하는 한 자리의 자연수 \(a,\ b\)의 모든 순서쌍 \((a,\ b)\)의 개수는?
- Choices: ① 11 ② 13 ③ 15 ④ 17 ⑤ 19. Figure: none.
- **Answer: ④ 17**
- Solution: \(f=(x-2)(x-b)^2|x-a|\) is differentiable everywhere if and only if \((x-2)(x-b)^2\) vanishes at \(x=a\), that is, \(a=2\) or \(a=b\). Count: 9 (a=2) + 9 (a=b) − 1 (overlap (2,2)) = 17.
- Difficulty: 6. Needs the "|x−a|·g(x) is differentiable ⇔ g(a)=0" criterion plus careful counting.

## Problem 17
- PDF page 05 (L), printed p.56 | 유형3 도함수 — 대표기출
- Source: 2019학년도 대수능 6월 모의평가 나형 17번 [9107-0175] | [4점]
- Statement: 함수 \(f(x)=ax^2+b\)가 모든 실수 \(x\)에 대하여 \[4f(x)=\{f'(x)\}^2+x^2+4\] 를 만족시킨다. \(f(2)\)의 값은? (단, \(a,\ b\)는 상수이다.)
- Choices: ① 3 ② 4 ③ 5 ④ 6 ⑤ 7. Figure: none.
- **Answer: ① 3**
- Solution: \(4ax^2+4b=(4a^2+1)x^2+4\Rightarrow (2a-1)^2=0\), so \(a=\frac12\) and \(b=1\). Then \(f(2)=3\).
- Difficulty: 3. Comparing coefficients in an identity.

## Problem 18
- PDF page 05 (L), printed p.56 | 유형3 도함수 — 대표기출
- Source: 2023년 수능특강 [23009-0051]
- Statement: 다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \[\lim_{h\to0}\frac{f(x)-f(x-h)}{h}=3x^2+ax\] 이고 \(f'(1)=2\)일 때, 상수 \(a\)의 값은?
- Choices: ① −2 ② −1 ③ 0 ④ 1 ⑤ 2. Figure: none.
- **Answer: ② −1**
- Solution: the limit is \(f'(x)=3x^2+ax\), so \(3+a=2\Rightarrow a=-1\).
- Difficulty: 1. Definition of the derivative.

## Problem 19
- PDF page 05 (R), printed p.56 | 유형3 도함수 — 대표기출
- Source: 2023년 수능특강 [23009-0052]
- Statement: 실수 전체의 집합에서 미분가능한 함수 \(f(x)\)가 모든 실수 \(x,\ y\)에 대하여 \[f(x+y)=f(x)+f(y)-xy-f(0)\] 일 때, \(f'(0)-f'(-2)\)의 값은?
- Choices: ① −2 ② −1 ③ 0 ④ 1 ⑤ 2. Figure: none.
- **Answer: ① −2**
- Solution: \(f'(x)=\lim\frac{f(h)-xh-f(0)}{h}=f'(0)-x\). Hence \(f'(0)-f'(-2)=-2\).
- Difficulty: 4. Standard functional-equation-to-derivative technique.

## Problem 20
- PDF page 05 (R), printed p.56 | 유형3 도함수 — 대표기출
- Source: 2025년 수능특강 [25009-0056]
- Statement: 다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \[\lim_{h\to0}\frac{f(x+h)-f(x-h)}{h}=-8x^3+4x^2+2\] 를 만족시킨다. 함수 \(g(x)\)를 \[g(x)=\lim_{h\to0}\frac{f(x+4h)-f(x-2h)}{2h}\] 라 할 때, \(g(0)\times g(1)\)의 값은?
- Choices: ① −12 ② −9 ③ −6 ④ −3 ⑤ −1. Figure: none.
- **Answer: ② −9**
- Solution: \(2f'(x)=-8x^3+4x^2+2\Rightarrow f'(x)=-4x^3+2x^2+1\). \(g(x)=\frac{4+2}{2}f'(x)=3f'(x)\), so \(g(0)=3\), \(g(1)=-3\), and the product is \(-9\).
- Difficulty: 3. Coefficient bookkeeping.

## Problem 21
- PDF page 06 (L), printed p.57 | 유형3 도함수 — 대표기출
- Source: 2024년 수능특강 [24009-0054]
- Statement: 다항함수 \(y=f(x)\)의 그래프 위의 점 \((x,\ f(x))\)에서의 접선의 기울기가 \(3x^2+4x-1\)일 때, \(\displaystyle\lim_{h\to0}\frac{f(-1+2h)-f(-1)}{h}\)의 값은?
- Choices: ① −2 ② −4 ③ −6 ④ −8 ⑤ −10. Figure: none.
- **Answer: ② −4**
- Solution: \(f'(-1)=3-4-1=-2\), and the limit is \(2f'(-1)=-4\).
- Difficulty: 1. Plug-in.

## Problem 22
- PDF page 06 (L), printed p.57 | 유형3 도함수 — 대표기출
- Source: 2024년 수능특강 [24009-0055]
- Statement: 다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \[\lim_{h\to0}\frac{f(h)f(x+h)-f(h)f(x)}{h^2}=2x^3+4\] 를 만족시킨다. \(f(0)=0,\ f'(0)=2\)일 때, \(f'(3)\)의 값을 구하시오.
- Short answer. Figure: none.
- **Answer: 29**
- Solution: split as \(\frac{f(h)}{h}\cdot\frac{f(x+h)-f(x)}{h}\to f'(0)f'(x)=2f'(x)\). Then \(f'(x)=x^3+2\) and \(f'(3)=29\).
- Difficulty: 3. Factor the limit into two derivative definitions.

## Problem 23
- PDF page 06 (R), printed p.57 | 유형3 도함수 — 대표기출
- Source: 2020년 수능특강 37쪽 예제 3번 (no bracket code)
- Statement: 다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \[f'(2)+\lim_{h\to0}\frac{f(x-h)-f(x)}{h}=2x^3+ax\] 를 만족시킨다. \(f'(-2)=-f'(2)\)일 때, \(f'(1)\)의 값은? (단, \(a\)는 상수이다.)
- Choices: ① 4 ② 5 ③ 6 ④ 7 ⑤ 8. Figure: none.
- **Answer: ③ 6**
- Solution: \(f'(2)-f'(x)=2x^3+ax\). At \(x=2\): \(0=16+2a\Rightarrow a=-8\). So \(f'(x)=f'(2)-2x^3+8x\) and \(f'(-2)=f'(2)\). With \(f'(-2)=-f'(2)\) this forces \(f'(2)=0\), so \(f'(1)=-2+8=6\).
- Difficulty: 4. Substitute a special x into a derivative identity.

## Problem 24
- PDF page 06 (R), printed p.57 | 유형3 도함수 — 대표기출
- Source: 2025년 수능완성 [25054-0138]
- Statement: 최고차항의 계수가 1인 이차함수 \(f(x)\)가 \[\lim_{x\to\infty}\frac{f(x)-x^2}{x}=\lim_{x\to\infty}x\left\{f\!\left(1+\frac2x\right)-f(1)\right\}\] 을 만족시킨다. \(f(2)=-1\)일 때, \(f(5)\)의 값은?
- Choices: ① 6 ② 8 ③ 10 ④ 12 ⑤ 14. Figure: none.
- **Answer: ② 8**
- Solution: let \(f=x^2+bx+c\). The left side is \(b\). The right side is \(2f'(1)=2(2+b)\), so \(b=-4\). \(f(2)=-1\Rightarrow c=3\), and \(f(5)=8\).
- Difficulty: 4. Substitution \(t=1/x\) turns the right side into a derivative.

## Problem 25
- PDF page 07 (L), printed p.58 | 유형4 미분법 — 대표기출
- Source: 2021학년도 대수능 나형 17번 [21106-0069] | [4점]
- Statement: 두 다항함수 \(f(x),\ g(x)\)가 \[\lim_{x\to0}\frac{f(x)+g(x)}{x}=3,\quad \lim_{x\to0}\frac{f(x)+3}{xg(x)}=2\] 를 만족시킨다. 함수 \(h(x)=f(x)g(x)\)에 대하여 \(h'(0)\)의 값은?
- Choices: ① 27 ② 30 ③ 33 ④ 36 ⑤ 39. Figure: none.
- **Answer: ① 27**
- Solution: \(f(0)=-3\) and \(g(0)=3\). \(\frac{f'(0)}{g(0)}=2\Rightarrow f'(0)=6\), and \(f'(0)+g'(0)=3\Rightarrow g'(0)=-3\). \(h'(0)=6\cdot3+(-3)(-3)=27\).
- Difficulty: 5. A typical 4점 limits-plus-product-rule question.

## Problem 26
- PDF page 07 (L), printed p.58 | 유형4 미분법 — 대표기출
- Source: 2025년 수능특강 [25009-0058]
- Statement: 다항함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \[g(x)=5x^2-2xf(x)\] 라 하자. \(f(2)=3,\ f'(2)=1\)일 때, \(g'(2)\)의 값은?
- Choices: ① 6 ② 7 ③ 8 ④ 9 ⑤ 10. Figure: none.
- **Answer: ⑤ 10**
- Solution: \(g'=10x-2f-2xf'\), so \(g'(2)=20-6-4=10\).
- Difficulty: 1. Product rule plug-in.

## Problem 27
- PDF page 07 (R), printed p.58 | 유형4 미분법 — 대표기출
- Source: 2023년 수능완성 [23054-0129]
- Statement: 함수 \(f(x)=2x^3+ax^2-5x+b\)가 \[\lim_{x\to\infty}x\left\{f\!\left(2+\frac3x\right)-21\right\}=f(2)\] 를 만족시킬 때, \(a+b\)의 값은? (단, \(a,\ b\)는 상수이다.)
- Choices: ① 22 ② 24 ③ 26 ④ 28 ⑤ 30. Figure: none.
- **Answer: ② 24**
- Solution: a finite limit needs \(f(2)=21\), and then the limit is \(3f'(2)=21\Rightarrow f'(2)=7\). \(24+4a-5=7\Rightarrow a=-3\), and \(16+4a-10+b=21\Rightarrow b=27\). Sum \(=24\).
- Difficulty: 4. You must infer \(f(2)=21\) from finiteness.

## Problem 28
- PDF page 07 (R), printed p.58 | 유형4 미분법 — 대표기출
- Source: 2025년 수능완성 [25054-0139]
- Statement: 최고차항의 계수가 1인 다항함수 \(f(x)\)가 \[\lim_{x\to\infty}\frac{f(x)}{xf'(x)}=\lim_{x\to0}\frac{f(x)}{xf'(x)}=\frac13\] 을 만족시킬 때, \(f(2)\)의 값을 구하시오.
- Short answer. Figure: none.
- **Answer: 8**
- Solution: as \(x\to\infty\) the ratio tends to \(1/\deg f\), so f is cubic. As \(x\to0\), writing \(f=x^m u(x)\) with \(u(0)\neq0\) gives \(1/m\), so \(m=3\). A monic cubic with \(m=3\) is \(f=x^3\), and \(f(2)=8\).
- Difficulty: 5. Leading-order versus lowest-order term analysis is an unusual idea.

## Problem 29
- PDF page 08 (L), printed p.59 | 유형4 미분법 — 대표기출
- Source: 2022년 수능완성 [22054-0129]
- Statement: 다항함수 \(f(x)\)와 실수 전체의 집합에서 미분가능한 함수 \(g(x)\)는 모든 실수 \(x\)에 대하여 \[(x^2-1)g(x)=f(x)-2\] 를 만족시킨다. 함수 \(h(x)=f(x)g(x)\)에 대하여 \(f'(1)=-2,\ h'(1)=6\)일 때, \(g'(1)\)의 값을 구하시오.
- Short answer. Figure: none.
- **Answer: 2**
- Solution: at \(x=1\), \(f(1)=2\). Differentiating gives \(2xg+(x^2-1)g'=f'\), so at 1, \(2g(1)=-2\Rightarrow g(1)=-1\). \(h'(1)=f'(1)g(1)+f(1)g'(1)=2+2g'(1)=6\Rightarrow g'(1)=2\).
- Difficulty: 4. Differentiate an identity and substitute.

## Problem 30
- PDF page 08 (L), printed p.59 | 유형4 미분법 — 대표기출
- Source: 2024년 수능특강 [24009-0057]
- Statement: 일차함수 \(f(x)\)와 다항함수 \(g(x)\)가 다음 조건을 만족시킨다.
  (가) \(\displaystyle\lim_{x\to0}\frac{f(x)-g(x)}{x}=0\)
  (나) \(f(x)+g(x)=x^2-6x+12\)
  \(f(5)\times f'(5)\)의 값을 구하시오.
- Short answer. Figure: none.
- **Answer: 27**
- Solution: \(f(0)=g(0)\) and \(f'(0)=g'(0)\). From (나), \(2f(0)=12\) and \(2f'(0)=-6\), so \(f=-3x+6\). Then \(f(5)f'(5)=(-9)(-3)=27\).
- Difficulty: 3.

## Problem 31
- PDF page 08 (R), printed p.59 | 유형4 미분법 — 대표기출
- Source: 2021년 수능완성 [21054-0143]
- Statement: 삼차항의 계수가 1인 삼차함수 \(f(x)\)와 이차함수 \(g(x)\)가 다음 조건을 만족시킨다.
  (가) \(f(1)=g(1),\ f'(1)=g'(1)\)
  (나) \(f'(-1)=8,\ g'(1)=-g'(3)=4\)
  \(f(2)-g(2)\)의 값은?
- Choices: ① 3 ② 4 ③ 5 ④ 6 ⑤ 7. Figure: none.
- **Answer: ③ 5**
- Solution: \(g'\) is linear with \(g'(1)=4,\ g'(3)=-4\), so \(g'=-4x+8\). With \(f'=3x^2+px+q\), \(f'(1)=4\) and \(f'(-1)=8\) give \(p=-2,\ q=3\). \(f-g=(x-1)^2(x-k)\), and comparing \((f-g)'=3x^2+2x-5=(x-1)(3x+5)\) gives \(k=-3\). \((f-g)(2)=1\cdot5=5\). Sympy check: 5.
- Difficulty: 5. Several conditions to combine, plus the double-root structure.

## Problem 32
- PDF page 08 (R), printed p.59 | 유형4 미분법 — 대표기출
- Source: 2024년 수능완성 [24054-0114]
- Statement: 최고차항의 계수가 1인 이차함수 \(f(x)\)에 대하여 함수 \(y=f(x)\)의 그래프와 직선 \(y=f(2)\)가 서로 다른 두 점 A, B에서 만난다. 두 점 A, B의 \(x\)좌표의 합이 6일 때, \(\displaystyle\sum_{n=1}^{10}f'(n)\)의 값은?
- Choices: ① 50 ② 60 ③ 70 ④ 80 ⑤ 90. Figure: none.
- **Answer: ① 50**
- Solution: \(f(x)=f(2)\) has roots 2 and \(-b-2\), whose sum is \(-b=6\), so \(b=-6\). Then \(f'(n)=2n-6\) and \(\sum_{n=1}^{10}=110-60=50\).
- Difficulty: 3.

## Problem 33
- PDF page 09 (L), printed p.60 | Level Up
- Source: 2023년 수능특강 [23009-0065]
- Statement: 이차함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f'(1)\)의 값은?
  (가) \(\displaystyle\lim_{x\to\infty}\frac{\{f(x)\}^2}{3x^2f(x)+f(x^2)}=3\)
  (나) \(\displaystyle\lim_{x\to0}\frac{f(x)}{x}=2\)
- Choices: ① 24 ② 26 ③ 28 ④ 30 ⑤ 32. Figure: none.
- **Answer: ② 26**
- Solution: let \(f=ax^2+bx+c\). (나) gives \(c=0,\ b=2\). (가) gives \(\frac{a^2}{3a+a}=\frac a4=3\Rightarrow a=12\). Then \(f'(1)=24+2=26\).
- Difficulty: 4. Note that \(f(x^2)\) also contributes an \(ax^4\) term.

## Problem 34
- PDF page 09 (R), printed p.60 | Level Up
- Source: 2024년 수능특강 [24009-0067]
- Statement: 함수 \(f(x)\)는 최고차항의 계수가 1인 삼차함수이고, 실수 \(t\)에 대하여 곡선 \(y=f(x)\) 위의 점 \((t,\ f(t))\)에서의 접선의 기울기를 함수 \(g(t)\)라 하자. \[\left\{x\,\middle|\,\lim_{h\to0}\frac{f(x+h)-f(x)}{h}=2\right\}=\{-3,\ 4\}\] 일 때, \(g(-2)\)의 값은?
- Choices: ① −20 ② −19 ③ −18 ④ −17 ⑤ −16. Figure: none.
- **Answer: ⑤ −16**
- Solution: \(f'(x)-2=3(x+3)(x-4)\), so \(f'(x)=3x^2-3x-34\). Then \(g(-2)=f'(-2)=12+6-34=-16\).
- Difficulty: 3. Despite the Level Up label, it is a direct reading of set notation.

## Problem 35
- PDF page 10 (L), printed p.61 | Level Up
- Source: 2022년 수능특강 [22009-0068]
- Statement: 이차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \[g(x)=|x+1|f(x)\] 라 하자. 함수 \(g(x)\)가 실수 전체의 집합에서 미분가능하고 \(\displaystyle\lim_{x\to0}\frac{g(x)}{x}=2\)일 때, \(g(1)\)의 값은?
- Choices: ① 2 ② 4 ③ 6 ④ 8 ⑤ 10. Figure: none.
- **Answer: ④ 8**
- Solution: differentiability at \(-1\) needs \(f(-1)=0\), and the limit needs \(f(0)=0\), so \(f=kx(x+1)\). \(g(x)/x\to k\cdot1\cdot1=2\Rightarrow k=2\). Then \(g(1)=2\cdot(2\cdot1\cdot2)=8\).
- Difficulty: 4.

## Problem 36
- PDF page 10 (R), printed p.61 | Level Up
- Source: 2024년 수능특강 [24009-0071]
- Statement: 최고차항의 계수가 1인 이차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \[g(x)=\begin{cases}f(x) & (x<1)\\ f(x+1)-f(x) & (x\ge1)\end{cases}\] 이라 하자. 함수 \(g(x)\)가 \(x=1\)에서 미분가능할 때, \(f(2)\)의 값은?
- Choices: ① 6 ② 7 ③ 8 ④ 9 ⑤ 10. Figure: none.
- **Answer: ① 6**
- Solution: let \(f=x^2+bx+c\). Continuity gives \(f(2)=2f(1)\), and slopes give \(f'(2)=2f'(1)\Rightarrow 4+b=4+2b\Rightarrow b=0\). Then \(4+c=2+2c\Rightarrow c=2\), so \(f(2)=6\).
- Difficulty: 4.

## Problem 37
- PDF page 11 (L), printed p.62 | Level Up
- Source: 2024년 수능특강 [24009-0069]
- Statement: 최고차항의 계수가 1인 삼차함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(3)\)의 값은? (단, \(a\)는 0이 아닌 실수이다.)
  (가) \(\{x\mid f(x)=3\}=\{-a,\ a,\ 2a\}\)
  (나) \(f(0)>0,\ f'(1)=-2\)
- Choices: ① 7 ② 8 ③ 9 ④ 10 ⑤ 11. Figure: none.
- **Answer: ⑤ 11**
- Solution: \(f(x)=(x+a)(x-a)(x-2a)+3\). \(f'(1)=2(1-2a)+(1-a^2)=-2\Rightarrow a^2+4a-5=0\Rightarrow a=1\) or \(-5\). \(f(0)=2a^3+3>0\) rules out \(-5\), so \(a=1\) and \(f(3)=8\cdot1+3=11\).
- Difficulty: 5. Factored form plus a case elimination.

## Problem 38
- PDF page 11 (R), printed p.62 | Level Up
- Source: 2024년 수능특강 [24009-0074]
- Statement: 두 함수 \[f(x)=\begin{cases}-4x-2 & (x\le-1)\\ ax^2+bx-1 & (-1<x<2)\\ 2x+c & (x\ge2)\end{cases},\qquad g(x)=-x^2+4ax+b-c\] 에 대하여 함수 \(f(x)\)가 실수 전체의 집합에서 미분가능할 때, \(\displaystyle\lim_{x\to1}\frac{f(x)g(x)+12}{x-1}\)의 값은? (단, \(a,\ b,\ c\)는 상수이다.)
- Choices: ① −10 ② −8 ③ −6 ④ −4 ⑤ −2. Figure: none.
- **Answer: ④ −4**
- Solution: at \(-1\), \(a-b-1=2\) and \(-2a+b=-4\), so \(a=1,\ b=-2\). The slope at 2 checks: \(4-2=2\). Continuity at 2: \(-1=4+c\Rightarrow c=-5\). Then \(g=-x^2+4x+3\), \(f(1)=-2\), \(g(1)=6\), so \(fg+12=0\) at 1. The limit is \((fg)'(1)=f'(1)g(1)+f(1)g'(1)=0\cdot6+(-2)(2)=-4\). Sympy check: −4.
- Difficulty: 5. Several steps, but each one is routine.

## Problem 39
- PDF page 12 (L), printed p.63 | Level Up
- Source: 2021년 수능특강 [21009-0065]
- Statement: 함수 \(f(x)=|x-2|\)에 대하여 <보기>에서 \(x=2\)에서 미분가능한 함수만을 있는 대로 고른 것은?
  ㄱ. \(xf(x)\)
  ㄴ. \(f(4-x)f(x)\)
  ㄷ. \(f(x)f(-x)\)
- Choices: ① ㄱ ② ㄴ ③ ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ. Figure: none.
- **Answer: ② ㄴ**
- Solution: ㄱ: \(x|x-2|\) with \(2\neq0\) has a kink, so it is not differentiable. ㄴ: \(|2-x||x-2|=(x-2)^2\) is differentiable. ㄷ: \(|x-2||x+2|=|x^2-4|\) has a kink at 2, so it is not differentiable.
- Difficulty: 3.

## Problem 40
- PDF page 12 (R), printed p.63 | Level Up
- Source: 2021년 수능특강 [21009-0068]
- Statement: 삼차함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(1)\)의 값은?
  (가) \(\displaystyle\lim_{x\to0}\frac{f(x)}{x}=6\)
  (나) 함수 \(y=f'(x)\)의 그래프는 점 \((1,\ 0)\)에서 \(x\)축에 접한다.
- Choices: ① −2 ② −1 ③ 0 ④ 1 ⑤ 2. Figure: none (the graph is described only in words).
- **Answer: ⑤ 2**
- Solution: \(f'(x)=k(x-1)^2\) and \(f'(0)=6\Rightarrow k=6\). Then \(f=2(x-1)^3+C\), and \(f(0)=0\Rightarrow C=2\). So \(f(1)=2\).
- Difficulty: 4. Writing f from f′ without integration takes a little care for 미분 단원; it can also be done by matching coefficients of \(f=px^3+qx^2+6x\).

## Problem 41
- PDF page 13 (L), printed p.64 | Level Up
- Source: 2022년 수능특강 [22009-0072]
- Statement: 삼차함수 \(f(x)\)와 이차함수 \(g(x)\)가 다음 조건을 만족시킨다.
  (가) 두 함수 \(f(x),\ g(x)\)는 모두 최고차항의 계수가 정수이다.
  (나) 모든 실수 \(x\)에 대하여 \[\lim_{h\to0}\frac{f\!\left(x+\frac h2\right)-f(x)}{h}\times\lim_{h\to0}\frac{g\!\left(x-\frac h3\right)-g(x)}{h}=-x^3-x^2+2\] 이다.
  함수 \(f'(x)\)가 최솟값 \(m\)을 가질 때, \(g'(m)\)의 값을 구하시오.
- Short answer. Figure: none.
- **Answer: 4**
- Solution: \(\frac12f'(x)\cdot(-\frac13)g'(x)=-x^3-x^2+2\Rightarrow f'g'=6(x-1)(x^2+2x+2)\). Since \(x^2+2x+2\) is irreducible, \(f'=3p(x^2+2x+2)\) and \(g'=2q(x-1)\) with \(pq=1\). f′ having a minimum means \(p=1\), so \(f'=3(x+1)^2+3\), \(m=3\), \(g'=2(x-1)\), and \(g'(3)=4\).
- Difficulty: 7. Factorization, the integer-coefficient condition and the minimum-sign condition all interact.

## Problem 42
- PDF page 13 (R), printed p.64 | Level Up
- Source: 2022년 수능특강 [22009-0073]
- Statement: 사차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \[g(x)=\begin{cases}\dfrac{f(x)}{x^2-4} & (|x|\ne2)\\ -x+a & (|x|=2)\end{cases}\] 라 하자. 함수 \(g(x)\)가 실수 전체의 집합에서 미분가능하고 \(\displaystyle\lim_{x\to2}\frac{g(x)-3}{f(x)}=\frac14\)일 때, \(g(a)\)의 값은? (단, \(a\)는 상수이다.)
- Choices: ① 21 ② 23 ③ 25 ④ 27 ⑤ 29. Figure: none.
- **Answer: ① 21**
- Solution: continuity forces \(f=(x^2-4)h(x)\) with h quadratic, \(h(2)=a-2\) and \(h(-2)=a+2\). In the limit the denominator tends to 0, so \(h(2)=3\), giving \(a=5\) and \(h(-2)=7\). The limit equals \(\frac{h'(2)}{4h(2)}=\frac14\Rightarrow h'(2)=3\). Solving gives \(h=x^2-x+1\), and \(g(5)=h(5)=21\). Sympy check: 21.
- Difficulty: 7. A multi-condition reconstruction where the piecewise definition hides that g is the polynomial h.
