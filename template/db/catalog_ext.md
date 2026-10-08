# 외부 자료 후보 문항 카탈로그 (고2 미적분Ⅰ 중간: 극한·연속 / 미분계수 / 미분가능성 / 도함수 / 곱의 미분 / 접선 / 평균값 정리 / 증감·극값)

Renders: `ext/f{0..4}_p{n}.png` (f0 = EBS 봉투 3회, f1 = EBS 만점마무리 시즌2, f2 = `261003_수능&모의 공통_원본 (1).pdf`, f3 = `261003_수능&모의 공통_원본.pdf`, f4 = ebs_클리어_모의고사_미적분).
Every answer below was solved independently. Checks are in `ext/verify.py`, `chk1.py`, `chk2.py` and `chk3.py` (sympy/numeric). For f2 and f3 the answers also match the printed 빠른정답.

## 0. File notes / dedup
- **f2 and f3 are NOT duplicates.** f2 (`... (1).pdf`) is "수학Ⅱ 수능/모의 공통 **고2** 21년 9월~25년 10월" (30 problems). f3 (`..._원본.pdf`) is the **고3** 21년 3월~26년 7월 version (31 problems). In both, pages 1–8 hold the problems, p9 is the 빠른정답, pp10–26 are the solutions and p27 is an OMR sheet.
- ALREADY USED and skipped: f0 #15 [25393-0107] and f1 제3회 #13 [25412-0105].
- No problem about a function and its inverse meeting at 3 points was found, and no problem with a distance equal to a³−1 or a²−1.
- **Out of scope (excluded):** f0 #16 (log), f0 #17 (needs antiderivative/적분), f1 제1회 #11 (circle geometry only), f1 제2회 #12 (sin), f1 제3회 #14 (2^x), f1 제3회 #22 (수열), f2 #08 (trig), f2 #12 (2^{x+a}), f2 #30 (log in condition).

Difficulty scale: 1–10 (5 = typical 4점, 8+ = killer).

---------------------------------------------------------------------------------------------------

## A. f1 — 2026학년 EBS 만점 마무리 시즌2 (1~3회)

### A1. 제1회 12번 [25412-0012] (4점) p1 — 함수의 극한 / 다항함수 결정 — 난이도 5
다항함수 \(f(x)\)가 다음 조건을 만족시킨다.
(가) 모든 실수 \(x\)에 대하여 \((x+1)f(x)=(x-2)f(x+1)\)이다.
(나) 어떤 실수 \(a\)에 대하여 \(\lim_{x\to a}\frac{1}{f(x)}\)의 값은 존재하지 않고, \(\lim_{x\to a}\frac{f(x)}{f(x+a)}=0\)이다.
\(\lim_{x\to f(3)}\frac{f(x)}{x}=220\)일 때, \(f(a^2)\)의 값은?
① 48 ② 50 ③ 52 ④ 54 ⑤ 56
**Answer ① 48.**
Sol: Put x = −1, 2, 0 to get f(0)=f(1)=f(2)=0. Comparing coefficients forces deg f = 3, so f = c x(x−1)(x−2). (나) needs f(a)=0, and only a=2 gives a limit of 0 (a=0 gives 1, a=1 gives −1/2). Then c(6c−1)(6c−2)=220, whose only real root is c=2, and f(4)=24c=48.

### A2. 제2회 11번 [25412-0057] (4점) p2 — 연속 (절댓값 함수의 연속) — 난이도 5
다음 조건을 만족시키는 최고차항의 계수가 1이고 \(f(2)=8\)인 이차함수 \(f(x)\)와 실수 \(a\)의 순서쌍 \((f(x),a)\)에 대하여 \(f(5)+a\)의 최댓값은?
(가) \(g(x)=\begin{cases} f(x)-a & (x\le 0)\\ a-f(2a-x) & (x>0)\end{cases}\)라 할 때, 함수 \(|g(x)|\)는 실수 전체의 집합에서 연속이다.
(나) \(f(a)=a\)
① 31 ② 33 ③ 35 ④ 37 ⑤ 39
**Answer ③ 35.**
Sol: Continuity at 0 means |f(0)−a| = |a−f(2a)|. That gives either f(0)=f(2a), or f(0)+f(2a)=2a (which forces a=0). With f = x²+px+4−2p and f(a)=a, the candidates are (a, f) = (0, x²+2x), (4, x²−8x+20) and (−1, x²+2x). So f(5)+a ∈ {35, 9, 34}, and the maximum is 35.

### A3. 제3회 21번 [25412-0113] (4점, 단답) p4 — 극한 + 도함수 — 난이도 7
최고차항의 계수가 1이고 \(f(0)=0\)인 다항함수 \(f(x)\)가 다음 조건을 만족시킨다.
(가) \(\lim_{x\to\infty}\frac{f(x)+1}{f(-x)}=1,\ \lim_{x\to\infty}\frac{x^3f(x)}{\{f'(x)\}^2}=\infty\)
(나) 모든 실수 \(\alpha\)에 대하여 \(\lim_{x\to\alpha}\frac{f(x)}{f'(x)}\)의 값이 존재하고 \(\lim_{x\to 1}\frac{f(x)}{f'(x)}=\frac12\)이다.
\(f(-2)>f(2)\)일 때, \(\lim_{x\to3}\{f(-x)-f(x)\}\)의 값을 구하시오.
**Answer 108.**
Sol: (가) makes the degree even and less than 5, so deg f is 2 or 4. Degree 2 gives f = x², which violates f(−2)>f(2). For degree 4, every real critical point must be a multiple root. So f = x²(x²+ux+v) with no other real critical points, and f(1)/f'(1)=1/2 gives u=−2. Then f(−3)−f(3) = −2·(−2)·27 = 108, independent of v.

## B. f4 — EBS 클리어 모의고사 (p1)

### B1. 13번 [25742-0013] (4점) — 곱의 미분가능성 + 극대 — 난이도 6
함수 \(f(x)=|x^2-3x-4|\)와 최고차항의 계수가 1인 삼차함수 \(g(x)\)에 대하여 함수 \(f(x)g(x)\)는 실수 전체의 집합에서 미분가능하다. 자연수 \(k\)에 대하여 함수 \(g(x)\)가 \(x=k\)에서 극대일 때, \(g(k)\)의 값은?
① 35 ② 36 ③ 37 ④ 38 ⑤ 39
**Answer ② 36.**
Sol: |(x−4)(x+1)|·g is differentiable at x = 4 and x = −1 only if g(4) = g(−1) = 0, so g = (x−4)(x+1)(x−c). g'(k)=0 gives c = (3k²−6k−4)/(2k−3). For k to be the local max we need g''(k)<0, i.e. c > 3k−3, and only k=1 works (c=7). Then g(1) = (−3)(2)(−6) = 36.

### B2. 14번 [25742-0014] (4점) — 미분계수 정의형 극한 — 난이도 5
최고차항의 계수가 \(p\)인 이차함수 \(f(x)\)가 다음 조건을 만족시키도록 하는 실수 \(p\)의 개수는? (단, \(a\)는 실수이다.)
(가) \(\lim_{x\to a}\frac{f(x)}{x-a}=2\)
(나) 모든 실수 \(t\)에 대하여 \(\lim_{x\to t}\frac{f(x^2)}{f(x)}\)의 값이 존재한다.
① 1 ② 2 ③ 3 ④ 4 ⑤ 5
**Answer ④ 4.**
Sol: Write f = p(x−a)(x−b) with p(a−b)=2. (나) requires a², b² ∈ {a, b}. The admissible (a, b) are (0,1), (1,0), (1,−1) and (−1,1), giving p = −2, 2, 1, −1. That is 4 values.

---------------------------------------------------------------------------------------------------

## C. f2 — 수학Ⅱ 수능/모의 공통 (고2 21.9~25.10), file `261003_수능&모의 공통_원본 (1).pdf`

### C01. p1 #01 [2025.10 고2 16번] (4점) — 극한·다항함수 결정 — 난이도 4
최고차항의 계수가 1인 두 이차함수 \(f(x), g(x)\)가 \(f(1)=0,\ \lim_{x\to1}\frac{f(x+3)\cdot g(x)}{\{f(x)\}^2}=0\)을 만족시킬 때, \(f(5)+g(5)\)의 값은?
① 14 ② 16 ③ 18 ④ 20 ⑤ 22
**④ 20.** Write f = (x−1)(x−a). If a=1 the denominator has order 4, which is impossible. If a≠1 the numerator needs order at least 3 at x=1, so f(4)=0 (a=4) and g=(x−1)². Then 4+16=20.

### C02. p1 #02 [2025.10 고2 26번] (4점, 단답) — 미분가능성(좌·우 미분계수) — 난이도 3
두 상수 \(a, k\)에 대하여 함수 \(f(x)=a|x-2|\)가 \(\lim_{x\to k+}\frac{f(x)-f(k)}{x-k}-\lim_{x\to k-}\frac{f(x)-f(k)}{x-k}=6\)을 만족시킬 때, \(f(a+k)\)의 값을 구하시오.
**9.** The left and right derivatives differ only at k=2, where the difference is 2a=6, so a=3. f(5)=9.

### C03. p1 #03 [2025.10 고2 28번] (4점, 단답) — 연속·사잇값 정리 — 난이도 4
닫힌구간 \([0,2]\)에서 정의된 함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(\frac{f(0)}{f(2)}\)의 값을 구하시오.
(가) 함수 \(f(x)\)는 \(x=1\)에서만 불연속이고, \(\lim_{x\to1}f(x)=3f(2)\)이다.
(나) \(0\le x\le2\)인 모든 실수 \(x\)에 대하여 \(f(x)\ne2\)이고, \(f(0)+f(2)=4\)이다.
**5.** By the IVT each of [0,1) and (1,2] lies entirely on one side of 2. Because f(0)+f(2)=4 they lie on opposite sides, so the common limit must be 2. Then f(2)=2/3, f(0)=10/3, and the ratio is 5.

### C04. p1 #04 [2025.10 고2 30번] (4점, 단답) — 평균변화율 + 연속 — 난이도 7
세 양수 \(a,b,c\)에 대하여 함수 \(f(x)=\begin{cases}(x+4)(x+a) & (x<-4,\ -4<x<0)\\ b & (x=-4)\\ -x^2+6x+c & (x\ge0)\end{cases}\)이 있다. 상수 \(k\ (k>4)\)와 실수 \(t\)에 대하여 함수 \(f(x)\)에서 \(x\)의 값이 \(t\)에서 \(t+k\)까지 변할 때의 평균변화율을 \(g(t)\)라 하고, \(f(t)g(t)\)의 값을 \(h(t)\)라 하자. 두 함수 \(f(x), h(t)\)가 다음 조건을 만족시킨다.
(가) 함수 \(h(t)\)가 실수 전체의 집합에서 연속이다. (나) \(f(k)=b\)
\(f(c-a-b)\)의 값을 구하시오.
**50.** h(t) = f(t)(f(t+k)−f(t))/k. At t=−4 the limit is 0, so f(k−4)=b=f(k). The parabola's symmetry about x=3 then gives k=5 and b=c+5. At t=−9 we need f(−9)=0, so a=9. Continuity at t=0 forces c=36=4a. Hence b=41 and f(−14) = (−10)(−5) = 50.

### C05. p2 #05 [2025.9 고2 17번] (4점) — 극한 활용(도형) — 난이도 3
실수 \(t\ (t>1)\)에 대하여 직선 \(x=t\)가 두 곡선 \(y=x^2,\ y=\sqrt{x}\)와 만나는 점을 각각 P, Q라 하자. 점 A(1, 1)에 대하여 삼각형 APQ의 넓이를 \(S(t)\)라 할 때, \(\lim_{t\to1+}\frac{S(t)}{(t-1)^2}\)의 값은? [그림: \(y=x^2, y=\sqrt x\), 두 곡선은 O와 A에서 만나고, 직선 \(x=t\) 위에 P(위)와 Q(아래)]
① 1/4 ② 1/2 ③ 3/4 ④ 1 ⑤ 5/4
**③ 3/4.** S = ½(t²−√t)(t−1), and the limit is ½(2−½) = 3/4.

### C06. p2 #06 [2025.9 고2 30번] (4점, 단답) — 좌·우극한, 연속 — 난이도 6
최고차항의 계수가 양수인 이차함수 \(f(x)\)와 함수 \(g(x)=\frac13x+a\)에 대하여 함수 \(h(x)=\begin{cases}g(x)+f(x) & (f(x)\ge g(x))\\ g(x)-f(x) & (f(x)<g(x))\end{cases}\)가 다음 조건을 만족시킨다.
(가) \(\lim_{x\to\alpha-}h(x)\ne\lim_{x\to\alpha+}h(x)\)를 만족시키는 실수 \(\alpha\)의 값은 2뿐이다.
(나) 모든 실수 \(k\)에 대하여 \(\lim_{x\to k}|h(x)-1|\)의 값이 존재한다.
\(h(0)=\frac73\)일 때, \(h(5)\)의 값을 구하시오. (단, \(a\)는 상수이다.)
**25.** At a crossing α the one-sided values are 2g(α) and 0. (나) forces g(2)=1, so a=1/3. The other crossing must have g=0, which is x=−1. Hence f−g = c(x−2)(x+1). h(0) = 2c = 7/3 gives c=7/6, and h(5) = 2g(5)+18c = 4+21 = 25.

### C07. p2 #07 [2024.10 고2 14번] (4점) — 연속(무리식) — 난이도 3
실수 전체의 집합에서 연속인 함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(0)\)의 값은?
(가) \(x\ge-\frac12\)인 모든 실수 \(x\)에 대하여 \((\sqrt{2x+1}-1)\cdot f(x)=x^2+ax+b\) (단, \(a\)와 \(b\)는 상수이다.) (나) \(f(4)=2\)
① −7 ② −3 ③ 1 ④ 5 ⑤ 9
**② −3.** b=0 and f = (x+a)(√(2x+1)+1)/2. f(4)=2 gives a=−3, so f(0)=−3.

### C09. p3 #09 [2024.10 고2 20번] (4점) — 평균변화율 — 난이도 6
실수 \(a\)에 대하여 함수 \(f(x)=\begin{cases}(x-1)(x-a) & (x<1)\\ 0 & (1\le x<2)\\ 1 & (x\ge2)\end{cases}\)라 하자. 양의 실수 \(t\)에 대하여 함수 \(f(x)\)에서 \(x\)의 값이 0에서 \(t\)까지 변할 때의 평균변화율을 \(g(t)\)라 할 때, 〈보기〉에서 옳은 것만을 있는 대로 고른 것은?
ㄱ. \(a=1\)일 때, \(g(1)=-1\)이다. ㄴ. 함수 \(g(t)\)의 최댓값이 1일 때, \(g(2)=\frac12\)이다. ㄷ. \(g(k)=g(k+1)=g(k+2)\)를 만족시키는 \(0<k<2\)인 실수 \(k\)가 존재할 때, 함수 \(y=f(x)\)의 그래프와 직선 \(y=-\frac32\)은 서로 다른 두 점에서 만난다.
① ㄱ ② ㄴ ③ ㄱ,ㄴ ④ ㄱ,ㄷ ⑤ ㄴ,ㄷ
**④.** Here g = t−1−a on (0,1), −a/t on [1,2) and (1−a)/t on [2,∞). ㄱ is true. ㄴ: a maximum of 1 forces a=−1 and then g(2)=1, so it is false. ㄷ: this forces k=−a−1 and a=−3/2 (k=1/2). Then (x−1)(x+3/2) = −3/2 gives x = 0 and −1/2, two points, so it is true.

### C10. p3 #10 [2024.10 고2 27번] (4점, 단답) — 극한 활용 — 난이도 4
실수 \(t\ (t>1)\)에 대하여 곡선 \(y=\frac{2t}{x}\)와 직선 \(y=-\frac1tx+3\)이 만나는 두 점을 A, B라 하자. \(\lim_{t\to1+}\frac{\overline{OB}-\overline{OA}}{t-1}=k\)라 할 때, \(30k^2\)의 값을 구하시오. (단, O는 원점이고, 점 B의 \(x\)좌표는 점 A의 \(x\)좌표보다 크다.) [그림 有]
**54.** A=(t,2) and B=(2t,1). Rationalising gives k = 3/√5, so 30k² = 54.

### C11. p3 #11 [2024.10 고2 30번] (4점, 단답) — 연속, 교점 개수 함수 — 난이도 8
두 양수 \(a,b\)와 최고차항의 계수가 1인 이차함수 \(f(x)\)에 대하여 집합 \(\{x\mid x\ne-a,\ x는 실수\}\)에서 정의된 함수 \(g(x)=\begin{cases}\frac{bx}{x+a} & (x<-a,\ -a<x<1)\\ f(x) & (x\ge1)\end{cases}\)이라 할 때, 함수 \(g(x)\)는 \(x=1\)에서 연속이다. 실수 \(t\)에 대하여 함수 \(y=|g(x)|\)의 그래프와 직선 \(y=t\)가 만나는 점의 개수를 \(h(t)\)라 할 때, 함수 \(h(t)\)가 다음 조건을 만족시킨다.
(가) 임의의 두 양수 \(t_1,t_2\)에 대하여 \(t_1<t_2\)이면 \(h(t_1)\ge h(t_2)\)이다.
(나) 함수 \(h(t)\)는 \(t=0,\ t=\alpha,\ t=\beta\ (0<\alpha<\beta)\)에서만 불연속이며 \(h(0)=\alpha,\ h(\alpha)=\beta-1\)이다.
\(f(a-b)\)의 값을 구하시오.
**75.** Monotonicity forces f to dip below 0 on (1,∞). Counting gives α = f(1) = b/(1+a) = 3, β = b = |min f| = 6 and h(0)=3. So a=1, b=6 and f = (x−4)²−6, giving f(−5)=75.

### C13. p4 #13 [2024.9 고2 28번] (4점, 단답) — 극한값 존재 조건 — 난이도 6
최고차항의 계수가 양수인 이차함수 \(f(x)\)가 다음 조건을 만족시킨다.
(가) \(\lim_{x\to0-}\frac{\sqrt{x^2}-f(x)}{x+f(x)}\cdot\lim_{x\to0+}\frac{\sqrt{x^2}-f(x)}{x+f(x)}=-2\)
(나) \(\lim_{x\to a}\frac{f(x-4)f(x+1)}{\sqrt{x^2}-3}\)의 값이 존재하지 않는 실수 \(a\)의 개수는 1이다.
\(f(24)\)의 값을 구하시오.
**40.** f(0)=0 (otherwise the product is 1). With f = cx²+dx, (가) gives d=−1/3. Then exactly one of a = ±3 must fail, which requires f(4)=0, so c=1/12. f(24) = 48−8 = 40.

### C14. p4 #14 [2023.11 고2 16번] (4점) — 극한 활용 — 난이도 3
\(0<t<3\)인 실수 \(t\)에 대하여 함수 \(y=\left|\frac2x-3\right|\)의 그래프와 직선 \(y=t\)가 만나는 두 점 사이의 거리를 \(f(t)\)라 할 때, \(\lim_{t\to0+}\frac{f(t)}{t}\)의 값은? [그림 有]
① 2/9 ② 1/3 ③ 4/9 ④ 5/9 ⑤ 2/3
**③ 4/9.** f = 2/(3−t) − 2/(3+t) = 4t/(9−t²).

### C15. p4 #15 [2023.11 고2 28번] (4점, 단답) — 극한·다항함수 결정 — 난이도 5
상수항과 계수가 모두 음이 아닌 정수인 두 다항함수 \(f(x),g(x)\)가 다음 조건을 만족시킬 때, \(f(2)+g(2)\)의 값을 구하시오.
(가) \(\lim_{x\to\infty}\frac{\{f(x)\}^2g(x)}{x^5}=4\) (나) \(\lim_{x\to0}\frac{f(x)\{g(x)\}^2}{x^5}=2\)
**16.** Matching degrees and lowest orders leaves f = 2x and g = x³+x², so 4+12 = 16.

### C16. p4 #16 [2023.9 고2 20번] (4점) — 연속(구간별 함수) — 난이도 5
이차함수 \(f(x)=(x-k)^2\ (k>0)\)이 있다. 양수 \(a\)에 대하여 함수 \(g(x)=\begin{cases}f(x) & (x\le3)\\ kf(x-a) & (x>3)\end{cases}\)이 다음 조건을 만족시킬 때, 〈보기〉에서 옳은 것만을 있는 대로 고른 것은?
(가) \(\lim_{x\to3}g(x)\)가 존재한다. (나) 함수 \(y=g(x)\)의 그래프는 \(x\)축과 오직 한 점에서만 만난다.
ㄱ. \(f(1)=1\)이면 \(g(2)=0\)이다. ㄴ. \(g(k+a)<g(3)\) ㄷ. \((k-1)(k-2)\ge0\)
① ㄱ ② ㄱ,ㄴ ③ ㄱ,ㄷ ④ ㄴ,ㄷ ⑤ ㄱ,ㄴ,ㄷ
**② ㄱ,ㄴ.** We need (3−k)² = k(3−a−k)², and either k>3 or k+a ≤ 3. ㄱ: k=2 and a = 1−1/√2, so it is true. ㄴ: g(k+a) is a² < (3−k)² or 0 < (3−k)², so it is true. ㄷ: k=1.5, a≈0.275 is a counterexample, so it is false.

### C17. p5 #17 [2023.9 고2 26번] (4점, 단답) — 극한·다항함수 결정 — 난이도 4
두 이차함수 \(f(x),g(x)\)가 \(\lim_{x\to\infty}\frac{f(x)}{g(x)-x^2}=1,\ \lim_{x\to3}\frac{g(x)-f(x)}{x-3}=8\)을 만족시킬 때, \(g(5)-f(5)\)의 값을 구하시오.
**20.** g−f is monic with (g−f)(3)=0 and (g−f)'(3)=8, so g−f = x²+2x−15, and its value at 5 is 20.

### C18. p5 #18 [2023.9 고2 30번] (4점, 단답) — 좌·우극한(교점 개수 함수) — 난이도 8
두 양수 \(a,b\ (a<b)\)에 대하여 함수 \(f(x)=\begin{cases}|-ax^2+b| & (x\le0)\\ x^2-2ax+b^2 & (x>0)\end{cases}\)이다. 양의 실수 \(t\)에 대하여 직선 \(y=t\)가 함수 \(y=f(x)\)의 그래프와 만나는 서로 다른 점의 개수를 \(g(t)\)라 하자. 함수 \(g(t)\)는 최솟값 2를 갖고, 두 상수 \(\alpha,\beta\)에 대하여 다음 조건을 만족시킨다.
(가) \(\left|\lim_{t\to\alpha-}g(t)-\lim_{t\to\alpha+}g(t)\right|=2\) (나) \(\lim_{t\to\beta-}g(t)-\lim_{t\to\beta+}g(t)+1=g(\beta)\) (다) \(g(\alpha)\ne g(\beta)\)
\(f\left(\frac12\right)=\alpha,\ \alpha+24\beta=30\)일 때, \(f(-2)+f(1)=\frac qp\)이다. \(p+q\)의 값을 구하시오. (단, \(p\)와 \(q\)는 서로소인 자연수이다.)
**311.** α = b²−a² (vertex value) and β = b². Then f(1/2) = α gives a = 1/2, and 25b² = 30.25 gives b = 1.1. f(−2)+f(1) = 0.9+1.21 = 211/100, so p+q = 311.

### C19. p5 #19 [2022.11 고2 17번] (4점) — 곱의 미분법 — 난이도 4
다항함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \(g(x)=(x^2-2x+2)f(x)\)라 하자. \(\lim_{x\to2}\frac{g(x)-1}{2f(x)-1}=-2\)일 때, \(g'(2)\)의 값은?
① 1/3 ② 2/3 ③ 1 ④ 4/3 ⑤ 5/3
**② 2/3.** f(2) = 1/2 and g(2) = 1. The limit equals g'(2)/(2f'(2)) = −2, and g'(2) = 1+2f'(2). So f'(2) = −1/6 and g'(2) = 2/3.

### C20. p5 #20 [2022.11 고2 19번] (4점) — 불연속점(교점 개수) — 난이도 5
두 집합 \(A=\{(x,y)\mid x^2+y^2=5,\ y\ge0\},\ B=\{(x,y)\mid y=2|x|\}\)에 대하여 좌표평면에서 집합 \(A\cup B\)가 나타내는 도형을 \(S\)라 하자. 양의 실수 \(m\)에 대하여 직선 \(y=m(x+5)\)가 도형 \(S\)와 만나는 점의 개수를 \(f(m)\)이라 할 때, 열린구간 \((0,\infty)\)에서 함수 \(f(m)\)은 \(m=\alpha_1,\ m=\alpha_2,\ m=\alpha_3\)에서만 불연속이다. \(\alpha_1+\alpha_2+\alpha_3\)의 값은? [그림: 반원과 V자 \(y=2|x|\)]
① 17/6 ② 3 ③ 19/6 ④ 10/3 ⑤ 7/2
**① 17/6.** The critical slopes are 1/3 (through (1,2)), 1/2 (tangent to the circle, which also passes through (−1,2)) and 2 (parallel to y=2x).

### C21. p6 #21 [2022.11 고2 27번] (4점, 단답) — 극한·다항함수 결정 — 난이도 4
일차함수 \(f(x)\)와 최고차항의 계수가 1인 이차함수 \(g(x)\)에 대하여 \(\lim_{x\to-3}\frac{f(x)g(x)}{(x+3)^2}=4,\ \lim_{x\to-3}\frac{f(x)+g(x)}{x+3}=-4\)일 때, \(g(2)-f(2)\)의 값을 구하시오.
**25.** f = −2(x+3) and g = (x+3)(x+1), so 15+10 = 25.

### C22. p6 #22 [2022.11 고2 29번] (4점, 단답) — 곱함수의 미분가능성 — 난이도 6
두 자연수 \(a,b\)에 대하여 두 함수 \(f(x),g(x)\)를 \(f(x)=\begin{cases}x+5 & (x<5)\\ |2x-a| & (x\ge5)\end{cases},\ g(x)=(x-5)(x-b)\)라 하자. 함수 \(f(x)g(x)\)가 실수 전체의 집합에서 미분가능하도록 하는 \(a,b\)의 모든 순서쌍 \((a,b)\)의 개수를 구하시오.
**11.** At x=5: 10(5−b) = |10−a|(5−b), so b=5 or a=20. The corner at a/2 ≥ 5 needs g(a/2)=0. That leaves (a,5) for a = 1,…,10 plus (20,10), 11 pairs in all (brute-force checked).

### C23. p6 #23 [2022.9 고2 26번] (4점, 단답) — 극한의 성질 — 난이도 2
두 함수 \(f(x),g(x)\)가 \(\lim_{x\to1}\frac{f(x)}{x-1}=8,\ \lim_{x\to1}\frac{g(x)}{x^2-1}=\frac12\)을 만족시킬 때, \(\lim_{x\to1}\frac{(x+1)f(x)}{g(x)}\)의 값을 구하시오.
**16.**

### C24. p6 #24 [2022.9 고2 29번] (4점, 단답) — 불연속·극한 존재 — 난이도 7
양수 \(m\)과 0이 아닌 실수 \(a\)에 대하여 두 함수 \(f(x)=\begin{cases}x^2+(a-1)x-a^2+2 & (x\le2m)\\ -3x+4a & (x>2m)\end{cases},\ g(x)=\begin{cases}ax-a & (x\le m+1)\\ x-a+1 & (x>m+1)\end{cases}\)이 다음 조건을 만족시킨다.
(가) \(\lim_{x\to\alpha-}f(x)\ne\lim_{x\to\alpha+}f(x),\ \lim_{x\to\beta-}g(x)\ne\lim_{x\to\beta+}g(x)\)인 실수 \(\alpha,\beta\)가 존재한다.
(나) 모든 실수 \(k\)에 대하여 \(\lim_{x\to k}\frac{f(x)}{g(x)}\)의 값이 존재한다.
\(m+g(a^2)\)의 값을 구하시오.
**4.** The jump of f at 2m must coincide with the jump of g at m+1, so m=1. Then g(1)=0 forces f(1)=0, so a ∈ {2, −1}, and matching the ratios at x=2 gives a=2. m+g(4) = 1+3 = 4.

### C25. p7 #25 [2021.11 고2 15번] (4점) — 곱의 미분 — 난이도 3
두 다항함수 \(f(x),g(x)\)가 \(\lim_{x\to1}\frac{f(x)-a+2}{x-1}=4,\ \lim_{x\to1}\frac{g(x)+a-2}{x-1}=a\)를 만족한다. 함수 \(f(x)g(x)\)의 \(x=1\)에서의 미분계수가 −1일 때, 상수 \(a\)의 값은?
① 1 ② 2 ③ 3 ④ 4 ⑤ 5
**③ 3.** (fg)'(1) = 4(2−a) + (a−2)a = (2−a)(4−a) = −1, so (a−3)² = 0.

### C26. p7 #26 [2021.11 고2 18번] (4점) — 극한 활용(도형) — 난이도 5
그림과 같이 실수 \(t\ (0<t<1)\)에 대하여 직선 \(y=2t\)가 두 곡선 \(y=x^2,\ y=tx^2\)과 제1사분면에서 만나는 점을 각각 A, B라 하고, 직선 \(y=t+1\)이 두 곡선 \(y=x^2,\ y=tx^2\)과 제1사분면에서 만나는 점을 각각 C, D라 하자. 사각형 ABDC의 넓이를 \(S(t)\)라 할 때, \(\lim_{t\to1-}\frac{S(t)}{(1-t)^2}\)의 값은? [그림 有]
① 1/4 ② √2/4 ③ 1/2 ④ √2/2 ⑤ 1
**④ √2/2.** Trapezoid area ½(AB+CD)(1−t). Each bracket over (1−t) tends to √2/2, so the limit is ½·√2 = √2/2.

### C27. p7 #27 [2021.11 고2 28번] (4점, 단답) — 미분계수·도함수 이용 미정계수 — 난이도 5
삼차함수 \(f(x)\)가 다음 조건을 만족시킨다.
(가) \(\lim_{x\to1}\frac{f(x)}{x-1}=3\) (나) 1이 아닌 상수 \(\alpha\)에 대하여 \(\lim_{x\to2}\frac{f(x)}{(x-2)f'(x)}=\alpha\)이다.
\(\alpha\cdot f(4)\)의 값을 구하시오.
**18.** A simple root at 2 would give α=1, so 2 is a double root. Then f = 3(x−1)(x−2)², α = 1/2, f(4) = 36, and α·f(4) = 18.

### C28. p7 #28 [2021.11 고2 30번] (4점, 단답) — 연속(교점 개수 함수 곱) — 난이도 8
두 자연수 \(a,b\)에 대하여 함수 \(f(x)=x^2-2ax+b\)라 할 때, 함수 \(g(x)\)를 \(g(x)=\begin{cases}f(x+a) & (x\le a)\\ |f(x)| & (x>a)\end{cases}\)라 하자. 실수 \(t\)에 대하여 직선 \(y=t\)와 함수 \(y=g(x)\)의 그래프가 만나는 서로 다른 점의 개수를 \(h(t)\)라 할 때, 함수 \(h(t)\)는 다음 조건을 만족시킨다.
\(k\ge24\)인 임의의 실수 \(k\)에 대해서만 함수 \(\{h(t)-2\}h(t-k)\)가 실수 전체의 집합에서 연속이다.
\(10a+b\)의 값을 구하시오.
**44** (a=4, b=4; unique by brute force over a ≤ 14 and b < 80).

### C29. p8 #29 [2021.9 고2 26번] (4점, 단답) — 극한·다항함수 결정 — 난이도 3
다항함수 \(f(x)\)가 \(\lim_{x\to\infty}\frac{f(x)}{2x^2}=1,\ \lim_{x\to1}\frac{f(x)-3}{(x-1)(x-2)}=4\)를 만족시킬 때, \(f(4)\)의 값을 구하시오.
**9.** f = 2x²−8x+9.

---------------------------------------------------------------------------------------------------

## D. f3 — 수학Ⅱ 수능/모의 공통 (고3 21.3~26.7), file `261003_수능&모의 공통_원본.pdf`

### D01. p1 #01 [2026.7 고3 9번] (4점) — 접선의 방정식 — 난이도 3
양수 \(t\)에 대하여 함수 \(f(x)=2x^3-7x^2+1\)의 그래프 위의 점 \((t,f(t))\)에서의 접선이 점 \((0,1)\)을 지나도록 하는 \(t\)의 값은?
① 3/4 ② 1 ③ 5/4 ④ 3/2 ⑤ 7/4
**⑤ 7/4.** f(t) − t f'(t) = 1 gives −4t³+7t² = 0.

### D02. p1 #02 [2026.7 고3 21번] (4점, 단답) — 불연속(교점 개수) — 난이도 8
두 양수 \(a,b\)에 대하여 함수 \(f(x)\)는 \(f(x)=\begin{cases}(x-a)(x-4) & \left(a\le x\le\frac32a\right)\\ (x-a)(x-b) & \left(x<a\ 또는\ x>\frac32a\right)\end{cases}\)이다. 양의 실수 \(t\)에 대하여 \(x\)에 대한 방정식 \(|f(x)|=t\)의 서로 다른 실근의 개수를 \(g(t)\)라 하자. 함수 \(g(t)\)가 다음 조건을 만족시킨다.
(가) \(\lim_{t\to0+}g(t)=6\) (나) 함수 \(g(t)\)는 \(t=\alpha,\ t=\beta\ (\alpha\ne\beta)\)에서만 불연속이고, \(\lim_{t\to\alpha+}g(t)=\lim_{t\to\beta-}g(t)=1\)이다.
\(f(0)=p+q\sqrt2\)일 때, \(p^2+q^2\)의 값을 구하시오. (단, \(p\)와 \(q\)는 유리수이다.)
**320.** The zeros are b < a < 4 < 3a/2. The two hump heights and the endpoint value must all be equal: ((a−b)/2)² = ((4−a)/2)² = (a/2)(3a/2−4). So a = 2√2, b = 4√2−4, and f(0) = ab = 16−8√2.

### D03. p1 #03 [2026.5 고3 9번] (4점) — 곱의 미분법 — 난이도 3
다항함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \(g(x)=(x^2+x)f(x)\)라 하자. \(\lim_{h\to0}\frac{g(1+h)-4}{h}=9\)일 때, \(f(1)\cdot f'(1)\)의 값은?
① 3 ② 9/2 ③ 6 ④ 15/2 ⑤ 9
**① 3.** f(1) = 2, and 6+2f'(1) = 9 gives f'(1) = 3/2.

### D04. p1 #04 [2026.5 고3 13번] (4점) — 평균변화율·연속 — 난이도 4
실수 전체의 집합에서 연속인 함수 \(f(x)\)가 다음 조건을 만족시킬 때, \(f(28)\)의 값은?
(가) \(0\le x\le12\)인 모든 실수 \(x\)에 대하여 \((\sqrt{2x+1}-1)f(x)=ax\)이다. (단, \(a\)는 상수이다.)
(나) 모든 실수 \(k\)에 대하여 함수 \(f(x)\)에서 \(x\)의 값이 \(k\)에서 \(k+12\)까지 변할 때의 평균변화율은 \(\frac12\)이다.
① 16 ② 18 ③ 20 ④ 22 ⑤ 24
**② 18.** f = a(√(2x+1)+1)/2 and f(12)−f(0) = 2a = 6, so a = 3. f(28) = f(4)+12 = 18.

### D05. p2 #05 [2026.3 고3 13번] (4점) — 접선, 접선과 축 — 난이도 3
함수 \(f(x)=x^3-4x^2+6x-8\)에 대하여 곡선 \(y=f(x)\) 위의 점 P(1, −5)에서의 접선이 곡선 \(y=f(x)\)와 만나는 점 중 P가 아닌 점을 Q라 하자. 곡선 \(y=f(x)\) 위의 점 Q에서의 접선과 \(x\)축, \(y\)축으로 둘러싸인 도형의 넓이는?
① 8 ② 10 ③ 12 ④ 14 ⑤ 16
**⑤ 16.** The tangent at P is y = x−6, which meets the curve again at Q(2,−4). The tangent at Q is y = 2x−8, and the triangle with the axes has area ½·4·8 = 16. (No integration is needed.)

### D06. p2 #06 [2025.10 고3 21번] (4점, 단답) — 미분계수 정의·곱의 미분·최솟값 — 난이도 7 ★
최고차항의 계수가 1인 사차함수 \(f(x)\)가 다음 조건을 만족시킨다.
\(\lim_{x\to k}\frac{2x^2f(x)-\{f(k)\}^2}{x-k}=\lim_{x\to k}\frac{\{f(x)\}^2-\{f(k)\}^2}{x-k}\)을 만족시키는 실수 \(k\)는 \(t,\ -t\ (t>1)\)뿐이다.
함수 \(f(x)\)의 최솟값이 17일 때, \(f(4)\)의 값을 구하시오.
**81.** The left limit exists only if 2k²f(k) = f(k)². Since f > 0, f(k) = 2k². Then equating the derivatives 4kf + 2k²f' = 2ff' gives f'(k) = 4k. So h = f−2x² has double roots exactly at ±t, i.e. h = (x²−t²)². The minimum of f is 2t²−1 = 17, so t² = 9 and f(4) = 49+32 = 81.

### D07. p2 #07 [2025.7 고3 13번] (4점) — 연속·교점 개수 — 난이도 5
함수 \(f(x)=x^2-4x+5\)와 두 상수 \(a,b\)에 대하여 함수 \(g(x)=\begin{cases}f(x+a)+b & (x<0)\\ f(x) & (x\ge0)\end{cases}\)이 실수 전체의 집합에서 연속이다. 실수 \(t\)에 대하여 함수 \(y=g(x)\)의 그래프와 직선 \(y=t\)가 만나는 점의 개수를 \(h(t)\)라 하자. \(\left|\lim_{t\to k+}h(t)-\lim_{t\to k-}h(t)\right|=2\)를 만족시키는 서로 다른 모든 실수 \(k\)의 값이 1, 4, 5일 때, \(g(-4)\)의 값은?
① 9 ② 10 ③ 11 ④ 12 ⑤ 13
**⑤ 13.** We need a > 2 with left vertex value 1+b = 4, so b = 3. Then f(a) = 2 gives a = 3, and g(−4) = f(−1)+3 = 13. (This glues f(x+a)+b, similar to the excluded idea.)

### D08. p2 #08 [2025.7 고3 15번] (4점) — 구간별 함수의 미분가능성 — 난이도 7 ★
함수 \(f(x)=x^2+ax+b\)에 대하여 함수 \(g(x)=\begin{cases}|f(x)|-x^2 & (x\le0)\\ \{f(x)\}^2+x^3 & (x>0)\end{cases}\)이 다음 조건을 만족시킨다.
(가) 함수 \(g(x)\)는 \(x=b\)에서만 미분가능하지 않다. (나) 방정식 \(g(x)=0\)은 음의 실근을 갖는다.
\(g\left(-\frac12\right)+g(3)\)의 값은? (단, \(a,b\)는 상수이다.)
① 183/2 ② 187/2 ③ 191/2 ④ 195/2 ⑤ 199/2
**① 183/2.** Continuity at 0 gives |b| = b², so b ∈ {0, ±1}. If b=0, (나) fails or a second corner appears. If b=1 the non-differentiable point would lie in the smooth x>0 part. So b=−1, and differentiability at 0 (−a = −2a) gives a=0. Then f = x²−1, the corner is at x = −1, and the negative root is x = −1/√2. g(−1/2)+g(3) = 1/2+91 = 183/2.

### D09. p3 #09 [2025.5 고3 15번] (4점) — 미분가능성·함수 선택 — 난이도 8
최고차항의 계수가 1이고 \(\lim_{x\to0}\frac{f(x)}{x}=1\)인 사차함수 \(f(x)\)와 실수 전체의 집합에서 연속인 함수 \(g(x)\)가 모든 실수 \(x\)에 대하여 \(\{g(x)-x\}\{g(x)-f(x)\}=0\)을 만족시킨다. 함수 \(g(x)\)가 다음 조건을 만족시킬 때, 모든 \(\frac{g(-2)}{g(3)}\)의 값의 합은?
(가) \(\lim_{x\to2}\frac{g(x)-g(2)}{x-2}\)의 값은 존재하지 않는다.
(나) \(x\ge a\)인 모든 실수 \(x\)에 대하여 \(g(-x)=-g(x)\)를 만족시키는 실수 \(a\)의 최솟값은 4이다.
① −41/3 ② −13 ③ −37/3 ④ −35/3 ⑤ −11
**⑤ −11.** f − x = x²(x−2)(x∓4). For (x−2)(x−4), g = f on [2,4] and x elsewhere, so g(−2)/g(3) = (−2)/(−6) = 1/3. For (x−2)(x+4), g = f on [−4,2] and x elsewhere, giving −34/3. The sum is −11.

### D10. p3 #10 [2025.5 고3 21번] (4점, 단답) — 극값·교점 개수 함수의 연속 — 난이도 7
최고차항의 계수가 1이고 \(f(0)=0\)인 삼차함수 \(f(x)\)와 실수 \(t\)에 대하여 곡선 \(y=f(x)\)와 직선 \(y=t\)가 만나는 점의 개수를 \(g(t)\)라 하자. 양수 \(a\)와 함수 \(g(t)\)가 다음 조건을 만족시킨다.
함수 \(g(t)+g(t-4)\)는 \(t=0\)과 \(t=a\)에서만 불연속이다.
\(f(a)\)의 최솟값을 구하시오.
**200.** The jumps cancel only if local max − local min = 4. Then the discontinuities are at m and M+4, so m = 0, M = 4 and a = 8. f = (x−p)²(x−q) with p−q = 3 and f(0) = 0 gives f = x(x−3)² (f(8) = 200) or x²(x+3) (f(8) = 704). The minimum is 200.

### D11. p3 #11 [2025.3 고3 22번] (4점, 단답) — 미분가능성(절댓값) — 난이도 6 ★
삼차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \(g(x)=\begin{cases}-f(x) & (x<0)\\ |f(x)|-|2x^2-8| & (x\ge0)\end{cases}\)이라 하자. 함수 \(g(x)\)가 실수 전체의 집합에서 미분가능할 때, \(f(-5)\)의 값을 구하시오.
**154.** Continuity at 0 gives f(0) = 4, and differentiability there gives f'(0) = 0. The corner of |2x²−8| at x=2 forces f(2) = 0 and |f'(2)| = 8. No other positive simple root is allowed. The case f'(2) = −8 gives f = −x³+x²+4 = −(x−2)(x²+x+2). The case f'(2) = 8 gives (x−2)(3x+2)(x−1), which has a corner at x=1 and is rejected. f(−5) = 154.

### D12. p3 #12 [2024.10 고3 10번] (4점) — 연속 — 난이도 4
최고차항의 계수가 1인 삼차함수 \(f(x)\)와 실수 전체의 집합에서 정의된 함수 \(g(x)\)가 모든 실수 \(x\)에 대하여 \((x-1)g(x)=|f(x)|\)를 만족시킨다. 함수 \(g(x)\)가 \(x=1\)에서 연속이고 \(g(3)=0\)일 때, \(f(4)\)의 값은?
① 9 ② 12 ③ 15 ④ 18 ⑤ 21
**① 9.** f = (x−1)²(x−3).

### D13. p4 #13 [2024.10 고3 14번] (4점) — 미분가능성·접선 (⚠ f(x−1)+2 gluing — overlaps excluded idea) — 난이도 5
최고차항의 계수가 1인 사차함수 \(f(x)\)에 대하여 함수 \(g(x)=\begin{cases}f(x) & (x\le1)\\ f(x-1)+2 & (x>1)\end{cases}\)은 실수 전체의 집합에서 미분가능하고, 곡선 \(y=g(x)\) 위의 점 \((0,g(0))\)에서의 접선의 방정식이 \(y=2x+1\)이다. \(g'(t)=2\)인 서로 다른 모든 \(t\)의 값의 합은?
① 4 ② 9/2 ③ 5 ④ 11/2 ⑤ 6
**③ 5.** f = x⁴−2x³+x²+2x+1. f'(t) = 2 at t = 0, 1/2, 1, and the shifted piece adds t = 3/2, 2. The sum is 5.

### D14. p4 #14 [2024.10 고3 22번] (4점, 단답) — 연속·미분가능성 — 난이도 7 ★
최고차항의 계수가 1인 삼차함수 \(f(x)\)에 대하여 함수 \(g(x)=\begin{cases}f(x)+x & (f(x)\ge0)\\ 2f(x) & (f(x)<0)\end{cases}\)이라 할 때, 함수 \(g(x)\)는 다음 조건을 만족시킨다.
(가) 함수 \(g(x)\)가 \(x=t\)에서 불연속인 실수 \(t\)의 개수는 1이다. (나) 함수 \(g(x)\)가 \(x=t\)에서 미분가능하지 않은 실수 \(t\)의 개수는 2이다.
\(f(-2)=-2\)일 때, \(f(6)\)의 값을 구하시오.
**486.** At a root r the jump is r vs 0, so g is continuous only at r = 0, and differentiability there needs f'(0) = 1. Case analysis leaves f = x(x−r)² with r < 0 and r² ≠ 1. f(−2) = −2 gives r = −3, so f(6) = 6·81 = 486.

### D15. p4 #15 [2024.7 고3 22번] (4점, 단답) — 곱함수의 연속 — 난이도 7
두 자연수 \(a,b\ (a<b<8)\)에 대하여 함수 \(f(x)=\begin{cases}|x+3|-1 & (x<a)\\ x-10 & (a\le x<b)\\ |x-9|-1 & (x\ge b)\end{cases}\)이다. 함수 \(f(x)\)와 양수 \(k\)는 다음 조건을 만족시킨다.
(가) 함수 \(f(x)f(x+k)\)는 실수 전체의 집합에서 연속이다. (나) \(f(k)<0\)
\(f(a)\cdot f(b)\cdot f(k)\)의 값을 구하시오.
**96.** The unique solution (brute force) is a=2, b=6, k=4: (−8)(2)(−6) = 96.

### D16. p4 #16 [2024.5 고3 14번] (4점) — 접선의 y절편 — 난이도 5
최고차항의 계수가 1인 삼차함수 \(f(x)\)와 실수 \(t\)에 대하여 곡선 \(y=f(x)\) 위의 점 \((t,f(t))\)에서의 접선의 \(y\)절편을 \(g(t)\)라 하자. 두 함수 \(f(x),g(t)\)가 다음 조건을 만족시킨다.
\(|f(k)|+|g(k)|=0\)을 만족시키는 실수 \(k\)의 개수는 2이다.
\(4f(1)+2g(1)=-1\)일 때, \(f(4)\)의 값은?
① 46 ② 49 ③ 52 ④ 55 ⑤ 58
**② 49.** g(t) = f(t) − t f'(t). Both terms vanish only at k=0 (if f(0)=0) or at a multiple root, so f = x(x−r)². The condition gives 4u²−4u+1 = 0 with u = 1−r, so r = 1/2 and f(4) = 4·(7/2)² = 49.

### D17. p5 #17 [2024.5 고3 20번] (4점, 단답) — 다항식 항등식·극한 — 난이도 6
두 다항함수 \(f(x),g(x)\)가 모든 실수 \(x\)에 대하여 \(xf(x)=\left(-\frac12x+3\right)g(x)-x^3+2x^2\)을 만족시킨다. 상수 \(k\ (k\ne0)\)에 대하여 \(\lim_{x\to2}\frac{g(x-1)}{f(x)-g(x)}\cdot\lim_{x\to\infty}\frac{\{f(x)\}^2}{g(x)}=k\)일 때, \(k\)의 값을 구하시오.
**25.** The x³ term must cancel, so g = −2x²+px. The limit at 2 needs g(1) = 0, so p = 2. Then f = −5x+6, and the product is (−2)·(−25/2) = 25.

### D18. p5 #18 [2023.10 고3 10번] (4점) — 극한 활용 — 난이도 3
실수 \(t\ (t>0)\)에 대하여 직선 \(y=tx+t+1\)과 곡선 \(y=x^2-tx-1\)이 만나는 두 점을 A, B라 할 때, \(\lim_{t\to\infty}\frac{\overline{AB}}{t^2}\)의 값은? [그림 有]
① √2/2 ② 1 ③ √2 ④ 2 ⑤ 2√2
**④ 2.**

### D19. p5 #19 [2023.10 고3 22번] (4점, 단답) — 미분가능성 + 곡선 밖의 점에서 그은 접선 — 난이도 8
삼차함수 \(f(x)\)에 대하여 구간 \((0,\infty)\)에서 정의된 함수 \(g(x)\)를 \(g(x)=\begin{cases}x^3-8x^2+16x & (0<x\le4)\\ f(x) & (x>4)\end{cases}\)라 하자. 함수 \(g(x)\)가 구간 \((0,\infty)\)에서 미분가능하고 다음 조건을 만족시킬 때, \(g(10)=\frac qp\)이다. \(p+q\)의 값을 구하시오. (단, \(p\)와 \(q\)는 서로소인 자연수이다.)
(가) \(g\left(\frac{21}{2}\right)=0\) (나) 점 \((-2,0)\)에서 곡선 \(y=g(x)\)에 그은, 기울기가 0이 아닌 접선이 오직 하나 존재한다.
**29.** f = c(x−4)²(x−21/2). The cubic piece already gives the tangent y = 3x+6 (touching at x=1). The f-piece has a tangent from (−2,0) at s=8, so it must be the same line, which forces f'(8) = −4c = 3, i.e. c = −3/4. g(10) = 27/2.

### D20. p5 #20 [2023.7 고3 14번] (4점) — 곱함수의 연속(보기) — 난이도 7
최고차항의 계수가 1이고 \(f(-3)=f(0)\)인 삼차함수 \(f(x)\)에 대하여 함수 \(g(x)\)를 \(g(x)=\begin{cases}f(x) & (x<-3\ 또는\ x\ge0)\\ -f(x) & (-3\le x<0)\end{cases}\)이라 하자. 함수 \(g(x)g(x-3)\)이 \(x=k\)에서 불연속인 실수 \(k\)의 값이 한 개일 때, 〈보기〉에서 옳은 것만을 있는 대로 고른 것은?
ㄱ. 함수 \(g(x)g(x-3)\)은 \(x=0\)에서 연속이다. ㄴ. \(f(-6)\cdot f(3)=0\) ㄷ. 함수 \(g(x)g(x-3)\)이 \(x=k\)에서 불연속인 실수 \(k\)가 음수일 때, 집합 \(\{x\mid f(x)=0,\ x는 실수\}\)의 모든 원소의 합이 −1이면 \(g(-1)=-48\)이다.
① ㄱ ② ㄱ,ㄴ ③ ㄱ,ㄷ ④ ㄴ,ㄷ ⑤ ㄱ,ㄴ,ㄷ
**⑤.** With d = f(0) ≠ 0, the jumps cancel at x=0. The candidates k = −3 and k = 3 need f(−6) = 0 and f(3) = 0 respectively, and exactly one holds. In ㄷ, f(3) = 0 and the root-set sum −1 force f = (x−3)²(x+4), so g(−1) = −f(−1) = −48.

### D21. p6 #21 [2023.3 고3 12번] (4점) — 극한 활용 — 난이도 3
곡선 \(y=x^2\)과 기울기가 1인 직선 \(l\)이 서로 다른 두 점 A, B에서 만난다. 양의 실수 \(t\)에 대하여 선분 AB의 길이가 \(2t\)가 되도록 하는 직선 \(l\)의 \(y\)절편을 \(g(t)\)라 할 때, \(\lim_{t\to\infty}\frac{g(t)}{t^2}\)의 값은? [그림 有]
① 1/16 ② 1/8 ③ 1/4 ④ 1/2 ⑤ 1
**④ 1/2.** g = (2t²−1)/4.

### D22. p6 #22 [2022.10 고3 9번] (4점) — 도함수 항등식 — 난이도 3
최고차항의 계수가 1인 다항함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \(xf'(x)-3f(x)=2x^2-8x\)를 만족시킬 때, \(f(1)\)의 값은?
① 1 ② 2 ③ 3 ④ 4 ⑤ 5
**③ 3.** f = x³−2x²+4x.

### D23. p6 #23 [2022.10 고3 11번] (4점) — 연속·주기·근의 개수 — 난이도 5
두 정수 \(a,b\)에 대하여 실수 전체의 집합에서 연속인 함수 \(f(x)\)가 다음 조건을 만족시킨다.
(가) \(0\le x<4\)에서 \(f(x)=ax^2+bx-24\)이다. (나) 모든 실수 \(x\)에 대하여 \(f(x+4)=f(x)\)이다.
\(1<x<10\)일 때, 방정식 \(f(x)=0\)의 서로 다른 실근의 개수가 5이다. \(a+b\)의 값은?
① 18 ② 19 ③ 20 ④ 21 ⑤ 22
**④ 21.** Continuity gives b = −4a. The count is 5 exactly when the smaller root lies in (1,2), i.e. −8 < a < −6, so a = −7, b = 28 and a+b = 21.

### D24. p6 #24 [2022.10 고3 20번] (4점, 단답) — 극한 존재·부등식 — 난이도 5
최고차항의 계수가 1이고 다음 조건을 만족시키는 모든 삼차함수 \(f(x)\)에 대하여 \(f(5)\)의 최댓값을 구하시오.
(가) \(\lim_{x\to0}\frac{|f(x)-1|}{x}\)의 값이 존재한다. (나) 모든 실수 \(x\)에 대하여 \(xf(x)\ge-4x^2+x\)이다.
**226.** f = x³+ax²+1 with a² ≤ 16, so the maximum of 126+25a is at a = 4, giving 226.

### D25. p7 #25 [2022.4 고3 14번] (4점) — 연속·미분가능성(보기, 그래프) — 난이도 5
정수 \(k\)와 함수 \(f(x)=\begin{cases}x+1 & (x<0)\\ x-1 & (0\le x<1)\\ 0 & (1\le x\le3)\\ -x+4 & (x>3)\end{cases}\)에 대하여 함수 \(g(x)\)를 \(g(x)=|f(x-k)|\)라 할 때, 〈보기〉에서 옳은 것만을 있는 대로 고른 것은? [그림: y=f(x), (0,1)·(3,1) 빈 점, (0,−1)·(3,0) 채운 점]
ㄱ. \(k=-3\)일 때, \(\lim_{x\to0-}g(x)=g(0)\)이다. ㄴ. 함수 \(f(x)+g(x)\)가 \(x=0\)에서 연속이 되도록 하는 정수 \(k\)가 존재한다. ㄷ. 함수 \(f(x)g(x)\)가 \(x=0\)에서 미분가능하도록 하는 모든 정수 \(k\)의 값의 합은 −5이다.
① ㄱ ② ㄷ ③ ㄱ,ㄴ ④ ㄱ,ㄷ ⑤ ㄱ,ㄴ,ㄷ
**④.** ㄴ is false because |f| never jumps by 2. ㄷ: the admissible k are −4, −2, 1 (numeric check), with sum −5.

### D26. p7 #26 [2022.3 고3 12번] (4점) — 연속(유리식형) — 난이도 5
\(a>2\)인 상수 \(a\)에 대하여 함수 \(f(x)\)를 \(f(x)=\begin{cases}x^2-4x+3 & (x\le2)\\ -x^2+ax & (x>2)\end{cases}\)라 하자. 최고차항의 계수가 1인 삼차함수 \(g(x)\)에 대하여 실수 전체의 집합에서 연속인 함수 \(h(x)\)가 다음 조건을 만족시킬 때, \(h(1)+h(3)\)의 값은?
(가) \(x\ne1,\ x\ne a\)일 때, \(h(x)=\frac{g(x)}{f(x)}\)이다. (나) \(h(1)=h(a)\)
① −15/6 ② −7/3 ③ −13/6 ④ −2 ⑤ −11/6
**③ −13/6.** g = (x−1)(x−2)(x−a), and h(1) = h(a) gives a = 4. h(1)+h(3) = −3/2 − 2/3.

### D27. p7 #27 [2021.10 고3 12번] (4점) — 극한 활용(원의 접선) — 난이도 5
곡선 \(y=x^2-4\) 위의 점 \(P(t,t^2-4)\)에서 원 \(x^2+y^2=4\)에 그은 두 접선의 접점을 각각 A, B라 하자. 삼각형 OAB의 넓이를 \(S(t)\), 삼각형 PBA의 넓이를 \(T(t)\)라 할 때, \(\lim_{t\to2+}\frac{T(t)}{(t-2)S(t)}+\lim_{t\to\infty}\frac{T(t)}{(t^4-2)S(t)}\)의 값은? (단, O는 원점이고, \(t>2\)이다.) [그림 有]
① 1 ② 5/4 ③ 3/2 ④ 7/4 ⑤ 2
**② 5/4.** T/S = (OP²−4)/4 = (t²−3)(t²−4)/4, so the sum is 1 + 1/4.

### D28. p7 #28 [2021.7 고3 12번] (4점) — 곱함수 연속 — 난이도 3
다항함수 \(f(x)\)는 \(\lim_{x\to\infty}\frac{f(x)}{x^2-3x-5}=2\)를 만족시키고, 함수 \(g(x)\)는 \(g(x)=\begin{cases}\frac{1}{x-3} & (x\ne3)\\ 1 & (x=3)\end{cases}\)이다. 두 함수 \(f(x),g(x)\)에 대하여 함수 \(f(x)g(x)\)가 실수 전체의 집합에서 연속일 때, \(f(1)\)의 값은?
① 8 ② 9 ③ 10 ④ 11 ⑤ 12
**① 8.** f = 2(x−3)².

### D29. p8 #29 [2021.4 고3 9번] (4점) — 극한의 성질 — 난이도 2
두 함수 \(f(x),g(x)\)가 \(\lim_{x\to\infty}\{2f(x)-3g(x)\}=1,\ \lim_{x\to\infty}g(x)=\infty\)를 만족시킬 때, \(\lim_{x\to\infty}\frac{4f(x)+g(x)}{3f(x)-g(x)}\)의 값은?
① 1 ② 2 ③ 3 ④ 4 ⑤ 5
**② 2.**

### D30. p8 #30 [2021.3 고3 12번] (4점) — 미분계수 정의형 극한 — 난이도 3
두 다항함수 \(f(x),g(x)\)가 다음 조건을 만족시킨다.
(가) \(\lim_{x\to1}\frac{f(x)-g(x)}{x-1}=5\) (나) \(\lim_{x\to1}\frac{f(x)+g(x)-2f(1)}{x-1}=7\)
두 실수 \(a,b\)에 대하여 \(\lim_{x\to1}\frac{f(x)-a}{x-1}=b\cdot g(1)\)일 때, \(ab\)의 값은?
① 4 ② 5 ③ 6 ④ 7 ⑤ 8
**③ 6.** f'(1) = 6, a = f(1) = g(1), and b = 6/g(1).

### D31. p8 #31 [2021.3 고3 20번] (4점, 단답) — 곱함수 연속 — 난이도 4
실수 \(m\)에 대하여 직선 \(y=mx\)와 함수 \(f(x)=2x+3+|x-1|\)의 그래프의 교점의 개수를 \(g(m)\)이라 하자. 최고차항의 계수가 1인 이차함수 \(h(x)\)에 대하여 함수 \(g(x)h(x)\)가 실수 전체의 집합에서 연속일 때, \(h(5)\)의 값을 구하시오.
**8.** g jumps at m = 1 and m = 3, so h = (x−1)(x−3) and h(5) = 8.

---------------------------------------------------------------------------------------------------

## E. RECOMMENDATIONS

**(a) #18 (hardest 5-choice, target ≈7): D08 — f3 p2 #08 [2025.7 고3 15번], answer ① 183/2.**
- It is purely about differentiability of a piecewise function built from |f| and f² + x³. Students use continuity at 0 (|b| = b²), compare left and right derivatives (−a vs −2a), find the corner of |f| at a root, and use the negative-root condition to eliminate cases.
- There are no tangent-distance or translation-gluing ideas in it. The answer comes in a clean 5-choice form and needs a 3-way case split (b = 0, 1, −1), which suits a #18.
- Backup: D09 [2025.5 고3 15번, answer −11]. It is harder (8) but also differentiability-based.

**(b) 3-step written-response item (target 6–7): D06 — f3 p2 #06 [2025.10 고3 21번], answer 81.**
It splits naturally into three steps:
 (1) Explain why the left limit exists only if 2k²f(k) = {f(k)}², and conclude f(k) = 2k², using f > 0.
 (2) Use the definition of the derivative and the product rule to show 4k f(k) + 2k² f'(k) = 2 f(k) f'(k), so f'(k) = 4k. Deduce that f(x) − 2x² = (x² − t²)².
 (3) Use the minimum value 17 (via the derivative or u = x²) to get t² = 9 and f(4) = 81.
It covers the 미분계수 definition, 곱의 미분 and 극값 with no overlap with the excluded ideas.
- Backup: D11 [2025.3 고3 22번, answer 154]. Its three steps are (1) f(0) = 4, (2) f'(0) = 0, f(2) = 0, |f'(2)| = 8, (3) rejecting the case with a positive simple root, giving f(−5) = 154.

---------------------------------------------------------------------------------------------------

## F. f5 — 2026 EBS FINAL 실전모의고사 수학영역 (1~7회, 공통+확통) [추가 2026-10-07]

Source: `EBS_2026_FINAL ... compressed.pdf` (55쪽 스캔). Page renders are `ext/f5/pNN.png` (150dpi); 1회 starts at #11.
Answers below were solved independently and checked in `ext/verify_f5.py` (sympy). No answer key was in the file.
Scope used: 극한·연속, 미분계수, 미분가능성, 도함수(곱의 미분), 접선. 증감·수직선 운동 items are tagged [경계]. 극대/극소, 평균값 정리 and 적분 items are excluded.

### F-1. 1회 14번 [25363-0014] (4점) p2 — 유리식 함수의 연속 — 난이도 6
최고차항의 계수가 1이고 \(f'(1)=-6\)인 삼차함수 \(f(x)\)와 상수 \(k\)에 대하여 함수 \(g(x)=\begin{cases}k & (f'(x)=0)\\ \dfrac{f(x)}{\{f'(x)\}^2} & (f'(x)\ne0)\end{cases}\)가 다음 조건을 만족시킨다.
[조건] 함수 \(g(x)\)는 \(x=3\)에서 불연속이고, \(x\ne3\)인 모든 실수 \(x\)에서 연속이다.
\(k+g(5)\)의 값은? ① \(-\frac1{24}\) ② \(-\frac1{12}\) ③ \(-\frac18\) ④ \(-\frac16\) ⑤ \(-\frac5{24}\)
**Answer ① −1/24.**
Sol: Continuity at the other root r of f′ forces a double root of f at r, so f=(x−r)²(x−s). Then f′'s other root is (r+2s)/3=3. With f′(1)=−6 this gives r=0, s=9/2. k=lim_{x→0} f/f′²=−1/18 and g(5)=1/72.

### F-2. 1회 20번 [25363-0020] (단답 4점) p4 — 도함수의 부호 — 난이도 4
최고차항의 계수가 1인 삼차함수 \(f(x)\)가 모든 실수 \(x\)에 대하여 \(xf(x)\ge0\)을 만족시키고, \(\{x\mid f(x)=f(0)\}=\{0,6\}\)일 때, 부등식 \(f'(m)\times f'(m+2)<0\)을 만족시키는 모든 정수 \(m\)의 값의 합을 구하시오.
**Answer 6.**
Sol: f=x(x−6)², so f′=3(x−2)(x−6). The valid values are m=1 and m=5.

### F-3. 2회 02번 [25363-0048] (2점) p6 — 미분계수 — 난이도 1
함수 \(f(x)=2x^2-3x+4\)에 대하여 \(\lim_{h\to0}\frac{f(a+h)-f(a)}{h}=5\)일 때, 상수 \(a\)의 값은? ①1 ②2 ③3 ④4 ⑤5
**Answer ② 2.**

### F-4. 2회 04번 [25363-0050] (3점) p6 — 그래프와 좌·우극한 (그림) — 난이도 2
Graph (p06 render): constant 2 on x<−1, open at (−1,2); segment from the closed point (−1,1) to the open point (0,0); segment from the closed point (0,−1) to the open point (1,2); closed point (1,4); constant 3 on x>1, open at (1,3).
\(\lim_{x\to-1-}f(x)+\lim_{x\to0+}f(x)+\lim_{x\to1+}f(x)\)의 값은? ①1 ②2 ③3 ④4 ⑤5
**Answer ④ 4** (2 + (−1) + 3).

### F-5. 2회 05번 [25363-0051] (3점) p7 — 곱의 미분 — 난이도 1
\(f(1)=3,\ f'(1)=-1\)인 다항함수 \(f(x)\)에 대하여 \(g(x)=(2x^2-1)f(x)\)일 때, \(g'(1)\)의 값은? ①7 ②8 ③9 ④10 ⑤11
**Answer ⑤ 11.**

### F-6. 2회 11번 [25363-0057] (4점) p9 — [경계: 수직선 운동] 속도 — 난이도 2
수직선 위를 움직이는 두 점 P, Q의 시각 \(t\,(t\ge0)\)에서의 위치가 각각 \(x_1(t)=t^3-2t^2+4t,\ x_2(t)=t^2+t\)이다. 두 점 P, Q의 속도가 같아지는 시각에서의 두 점 P, Q 사이의 거리는? ①1 ②2 ③3 ④4 ⑤5
**Answer ① 1** (t=1).

### F-7. 2회 21번 [25363-0067] (단답 4점) p13 — [경계: 증감] 곱의 미분·삼차함수 결정 — 난이도 6
최고차항의 계수가 1인 삼차함수 \(f(x)\)와 \(f(x)\)의 도함수 \(f'(x)\)에 대하여 함수 \(g(x)=f(x)f'(x)\)는 다음 조건을 만족시킨다.
(가) \(g'(1)=g(1)=0,\ g(0)=-3\)
(나) 함수 \(y=g(x)\)의 그래프와 직선 \(y=t\)의 교점의 개수를 \(h(t)\)라 하면 \(h(t)\ge2\)인 실수 \(t\)가 존재한다.
\(g(2)\)의 값을 구하시오.
**Answer 28.**
Sol: (가) leaves f=(x−1)²(x−c) with c=1 or −3/2. For c=1, g=3(x−1)⁵ is increasing, so (나) fails. Hence f=(x−1)²(x+3/2), f(2)=7/2, f′(2)=8.

### F-8. 3회 02번 [25363-0094] (2점) p17 — 미분계수 — 난이도 1
함수 \(f(x)=x^3-x+1\)에 대하여 \(\lim_{x\to2}\frac{f(x)-f(2)}{x-2}\)의 값은? ①5 ②7 ③9 ④11 ⑤13
**Answer ④ 11.**

### F-9. 3회 04번 [25363-0096] (3점) p17 — 연속(주기형 확장) — 난이도 3
실수 전체의 집합에서 정의된 함수 \(f(x)\)가 \(1\le x<3\)일 때 \(f(x)=x^2-2x+3\)이고 모든 실수 \(x\)에 대하여 \(f(x+2)=f(x)+k\)를 만족시킨다. \(f(x)\)가 실수 전체의 집합에서 연속일 때, 상수 \(k\)의 값은? ①−4 ②−2 ③0 ④2 ⑤4
**Answer ⑤ 4** (lim_{x→3−}f = 6 = f(1)+k).

### F-10. 3회 05번 [25363-0097] (3점) p18 — 극한→미분계수·곱의 미분 — 난이도 2
다항함수 \(f(x)\)가 \(\lim_{x\to2}\frac{f(x)-3}{x-2}=-2\)를 만족시킨다. \(g(x)=(3x^2+1)f(x)\)일 때, \(g'(2)\)의 값은? ①6 ②7 ③8 ④9 ⑤10
**Answer ⑤ 10.**

### F-11. 3회 07번 [25363-0099] (3점) p18 — [경계: 수직선 운동] 속도·가속도 — 난이도 2
P, Q의 위치 \(f(t)=t^3-3t^2,\ g(t)=-t^2+15t\). 출발한 후 두 점의 속도가 같아지는 시각에서의 가속도를 각각 \(p,q\)라 할 때 \(p+q\)는? ①−2 ②4 ③10 ④16 ⑤22
**Answer ③ 10** (t=3, so p=12 and q=−2).

### F-12. 3회 15번 [25363-0107] (4점, 보기) p22 — 사잇값 정리 — 난이도 5
0이 아닌 실수 \(k\)에 대하여 \(f(x)=x^3-2x+2k,\ g(x)=x^2+kx-2\).
ㄱ. 함수 \(g(x)\)는 음수인 극솟값을 갖는다. ㄴ. \(g(x)=0\)의 서로 다른 두 실근을 \(\alpha,\beta\,(\alpha<\beta)\)라 하면 \(f(\alpha)f(\beta)>0\)이다. ㄷ. 모든 실수 \(k\)에 대하여 \(f(x)=0\)은 \(g(x)=0\)의 두 실근 사이에서 적어도 하나의 실근을 갖는다.
①ㄱ ②ㄱ,ㄴ ③ㄴ,ㄷ ④ㄱ,ㄷ ⑤ㄱ,ㄴ,ㄷ
**Answer ④ ㄱ, ㄷ.**
Sol: f ≡ k²x (mod g), so f(α)f(β)=k⁴αβ=−2k⁴<0. ㄴ is false and ㄷ is true by the 사잇값 정리.
⚠ ㄱ uses the word 극솟값. Rephrase it as "최솟값" (it is a quadratic) before use.

### F-13. 3회 19번 [25363-0111] (단답 3점) p23 — [경계: 증가함수] — 난이도 3
이차 이상의 다항함수 \(f(x)\)의 도함수가 모든 실수 \(x\)에 대하여 \(f'(x)\ge5\)이고 \(f(2)=7\)이다. 부등식 \(f(x)\le5x-3\)을 만족시키는 실수 \(x\)의 최댓값을 구하시오.
**Answer 2.**

### F-14. 4회 02번 [25363-0140] (2점) p25 — 미분계수 — 난이도 1
\(f(x)=2x^3-x^2+9\), \(\lim_{h\to0}\frac{f(2+h)-f(2)}{h}\)는? ①18 ②19 ③20 ④21 ⑤22
**Answer ③ 20.**

### F-15. 4회 03번 [25363-0141] (3점) p25 — 연속 — 난이도 1
\(f(x)=\begin{cases}-2x+1&(x<a)\\x^2-6x+5&(x\ge a)\end{cases}\)가 실수 전체에서 연속일 때 \(a\)는? ①1 ②2 ③3 ④4 ⑤5
**Answer ② 2.**

### F-16. 4회 09번 [25363-0147] (4점) p27 — 극한·이차함수 결정 — 난이도 4
이차함수 \(f(x)\)와 상수 \(a\)가 \(\lim_{x\to3}\frac{f(x)-f(-1)}{x-3}=4a,\ \lim_{x\to2}\frac{f(x+2)}{f(x-4)}=3a\)를 만족시킨다. \(f(x)\)의 최솟값이 2일 때, \(f(4)\)의 값은? ①9/2 ②5 ③11/2 ④6 ⑤13/2
**Answer ② 5.**
Sol: f(3)=f(−1) puts the axis at x=1, so f(4)=f(−2) and 3a=1. Then f′(3)=4/3, which gives f=(x−1)²/3+2. The case f(−2)=0 contradicts min=2.

### F-17. 4회 13번 [25363-0151] (4점) p29 — [경계: 수직선 운동] 운동 방향 — 난이도 4
\(x(t)=t^3+at^2+bt\). P changes direction at \(t=t_1, t_2\) with \(t_2-t_1=4\), \(x(1)=25\) and \(0<t_1<t_2\). P가 \(t_1\)에서 \(t_2\)까지 움직인 거리는? ①28 ②29 ③30 ④31 ⑤32
**Answer ⑤ 32** (a=−12, b=36, t=2 and 6).

### F-18. 4회 16번 [25363-0154] (단답 3점) p30 — 곱의 미분 — 난이도 1
\(f(x)=(x^3-x)(x^2+2x)\)에 대하여 \(f'(1)\)의 값을 구하시오. **Answer 6.**

### F-19. 4회 22번 [25363-0160] (단답 4점) p32 — 미분가능성(절댓값) — 난이도 8 ★
최고차항의 계수가 1인 삼차함수 \(f(x)\)가 \(f'(0)+f'(1)=1,\ f(0)=0\)을 만족시킨다. 실수 \(k\)에 대하여 함수 \(g(x)=\begin{cases}f(x)&(x<k)\\f(x)+|f(x)|&(x\ge k)\end{cases}\)가 실수 전체의 집합에서 미분가능할 때, \(g(4k)\)의 값을 구하시오.
**Answer 72.**
Sol: Continuity and differentiability at k require f(k)=f′(k)=0. A simple root of f beyond k would create a corner. So f=x(x−k)² with k>0, and p+q=−1 gives k=1. Then g(4)=2f(4)=72.

### F-20. 5회 02번 [25363-0186] (2점) p33 — 미분계수 — 난이도 1
\(f(x)=5x^2-6x\), \(\lim_{x\to1}\frac{f(x)-f(1)}{x-1}\)은? ①1 ②2 ③3 ④4 ⑤5 **Answer ④ 4.**

### F-21. 5회 04번 [25363-0188] (3점) p33 — 그래프와 극한 (그림) — 난이도 2
Graph (p33 render): line falling to the closed point (1,−1); segment from the open point (1,1) to the open point (2,3); closed point (2,2) and a line from it down to (4,0).
\(\lim_{x\to1-}f(x)+\lim_{x\to2+}f(x)\)? ①1 ②2 ③3 ④4 ⑤5 **Answer ① 1.**

### F-22. 5회 08번 [25363-0192] (3점) p34 — 연속·다항식 결정 — 난이도 3
연속함수 \(f(x)\)가 (가) \(\lim_{x\to-1}f(x)=\lim_{x\to3}f(x)\), (나) 모든 실수 \(x\)에 대하여 \((x-1)f(x)=x^3+ax^2+b\)를 만족시킬 때, \(f(1)\)은? ①−9 ②−7 ③−5 ④−3 ⑤−1
**Answer ④ −3** (f=x²−2x−2).

### F-23. 5회 11번 [25363-0195] (4점) p35 — 접선·원 — 난이도 5
곡선 \(y=ax^4+x^2-ax-1\) 위의 두 점 A(1,0), B(0,−1)에서의 접선이 제4사분면의 점 C에서 만난다. 네 점 O, A, B, C가 한 원 위에 있을 때 \(a\)는? ①1/9 ②2/9 ③1/3 ④4/9 ⑤5/9
**Answer ③ 1/3.**
Sol: AB is a diameter (∠AOB=90°), so the tangents are perpendicular: (3a+2)(−a)=−1. a=−1 gives C=A, so it is rejected.

### F-24. 5회 20번 [25363-0204] (단답 4점) p38 — 극한·다항함수 결정 — 난이도 3
다항함수 \(f(x)\): (가) \(\lim_{x\to\infty}\frac{f(x)-x^4}{1-x^2}=3\), (나) \(\lim_{x\to0}\frac{f(x)}{x}=4\). \(f(2)\)의 값을 구하시오. **Answer 12.**

### F-25. 6회 02번 [25363-0232] (2점) p40 — 무리식 극한 — 난이도 1
\(\lim_{x\to-1}\frac{x+1}{\sqrt{x+5}-2}\)? ①1 ②2 ③3 ④4 ⑤5 **Answer ④ 4.**

### F-26. 6회 04번 [25363-0234] (3점) p40 — 연속 — 난이도 1
\(f(x)=\begin{cases}3x+7&(x<1)\\x^2+ax+2&(x\ge1)\end{cases}\) 연속일 때 \(a\)? ①6 ②7 ③8 ④9 ⑤10 **Answer ② 7.**

### F-27. 6회 05번 [25363-0235] (3점) p41 — 곱의 미분 — 난이도 1
\(f(x)=(3x-1)(x^2+x+2)\), \(f'(1)\)? ①16 ②17 ③18 ④19 ⑤20 **Answer ③ 18.**

### F-28. 6회 21번 [25363-0251] (단답 4점) p47 — 극한의 존재(유리함수) — 난이도 7 ★
두 삼차함수 \(f(x)=x^3+ax^2+bx+c,\ g(x)=cx^3+bx^2+ax+1\)이 다음 조건을 만족시킨다.
(가) \(\lim_{x\to3}\frac{f(x)}{x-3}\)의 값이 존재한다. (나) 4가 아닌 모든 실수 \(t\)에 대하여 \(\lim_{x\to t}\frac{g(x)}{f(x)}\)의 값이 존재한다. (다) \(\lim_{x\to4}\frac{g(x)}{f(x)}\)의 값은 존재하지 않는다.
\(\lim_{x\to3}\frac{g(x)}{f(x)}\)의 값을 구하시오.
**Answer 11.**
Sol: f=(x−3)(x−4)(x−r). g(3)=0 forces r=1/3. Then g=−(x−3)(3x−1)(4x−1)/3 and the limit is 11. The r=3 case fails (lim at 3 diverges).

### F-29. 7회 02번 [25363-0278] (2점) p48 — 미분계수 — 난이도 1
\(f(x)=x^3+2x-3\), \(\lim_{h\to0}\frac{f(2+h)-f(2)}{h}\)? ①10 ②12 ③14 ④16 ⑤18 **Answer ③ 14.**

### F-30. 7회 04번 [25363-0280] (3점) p48 — 그래프와 극한 (그림) — 난이도 2
Graph (p48 render): parabola-like curve into the open point (0,−1); closed point (0,1); segment from (0,−1) to the open point (1,0); curve from the closed point (1,2) to the open point (2,1); closed point (2,−2) with an increasing line after it.
\(\lim_{x\to1+}f(x)+\lim_{x\to2-}f(x)\)? ①−1 ②0 ③1 ④2 ⑤3 **Answer ⑤ 3.**

### F-31. 7회 05번 [25363-0281] (3점) p49 — 미분가능성 — 난이도 2
\(f(x)=\begin{cases}ax+1&(x\le2)\\x^2+2a-3&(x>2)\end{cases}\)가 실수 전체에서 미분가능하도록 하는 \(a\)? ①2 ②4 ③6 ④8 ⑤10 **Answer ② 4.**

### F-32. 7회 08번 [25363-0284] (3점) p50 — 극한·다항함수 결정 — 난이도 3
최고차항의 계수가 1인 다항함수 \(f(x)\)가 \(\lim_{x\to\infty}\frac{f(x)}{x^4}=\lim_{x\to0}\frac{f(x)-xf(2)}{x^2}=0\)을 만족시킬 때 \(f(3)\)? ①1 ②3 ③5 ④7 ⑤9
**Answer ② 3** (f=x³−8x).

### F-33. 7회 13번 [25363-0289] (4점) p52 — 원점을 지나는 접선·함수의 불연속 — 난이도 6
함수 \(f(x)=x^3-2x^2+8\)과 실수 \(t\)에 대하여 \(x\)에 대한 방정식 \(f(x)-xf'(t)=0\)의 서로 다른 실근의 개수를 \(g(t)\)라 하자. 함수 \(g(t)\)가 \(t=k\)에서 불연속인 모든 실수 \(k\)의 값의 합은? ①1/3 ②2/3 ③1 ④4/3 ⑤5/3
**Answer ④ 4/3.**
Sol: The only tangent through O touches at x=2 with slope 4. g=1, 2, 3 according as f′(t) <, =, > 4. f′(t)=4 gives t=2 and t=−2/3.

### F-34. 7회 15번 [25363-0291] (4점) p53 — 곡선 밖의 점에서 그은 접선의 개수 — 난이도 8 ★
최고차항의 계수가 1인 삼차함수 \(f(x)\)가 다음 조건을 만족시킨다.
[조건] 어떤 양수 \(a\)에 대하여 점 \((a,0)\)에서 곡선 \(y=f(x)\)에 그은 접선의 개수는 방정식 \(\{f(x)-x\}^2+\{f'(x)-3\}^2=0\)의 서로 다른 실근의 개수보다 작다.
\(f'(0)=3\)일 때, \(f(2)\)의 값은? ①1 ②2 ③3 ④4 ⑤5
**Answer ② 2.**
Sol: The root count must be 2 and the tangent count 1. Both roots 0 and s of f′=3 satisfy f(x)=x, so s=±2. For s=2, f=(x−1)³+1 and points (a,0) with 0<a<1 give 1 tangent. For s=−2, every a>0 gives 3 tangents.

### F-X. 범위 밖으로 제외한 수학Ⅱ 문항 (참고)
- 극대/극소: 1회 19, 2회 19, 4회 07, 4회 19 (사차함수 극값 구조), 5회 06, 5회 19, 6회 06, 7회 19, 3회 12.
- 적분/부정적분: 1회 12, 1회 17, 2회 07, 2회 09, 2회 13, 2회 15, 2회 17, 3회 09, 3회 13, 3회 16, 3회 21, 4회 05, 4회 08, 5회 09, 5회 13, 5회 17, 5회 22, 6회 14, 6회 17, 6회 19, 7회 07, 7회 11, 7회 17, 7회 21.
- 최솟값 함수의 미분가능성(극값 의존): 1회 22.
