# -*- coding: utf-8 -*-
# p3.py (견본4 17번, M27 구조 변경) sympy 전수 검증 + 조건 빼 보기
import os
from fractions import Fraction
import numpy as np
from sympy import (symbols, Rational, sqrt, factor, expand, simplify, sympify, nsimplify, diff, Poly,
                   real_roots, solve, discriminant, S as SS)
x, t, p, k, c = symbols('x t p k c', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'draft17.py')).read(), ns)
it = ns['ITEMS'][17]
ok = True
def chk(cond, msg):
    global ok
    ok &= bool(cond); print(('OK  ' if cond else 'FAIL') + ' ' + msg)

# ---------- 공통: 교점 개수 (정확 계산) ----------
def count_abs(F, h):
    """|F(x)| = h 를 만족시키는 서로 다른 실수 x 의 개수 (F 유리계수 다항식, h 유리수)"""
    h = sympify(h)
    if h < 0: return 0
    if h == 0: return len(set(real_roots(Poly(F, x))))
    r = set(real_roots(Poly(expand(F - h), x))) | set(real_roots(Poly(expand(F + h), x)))
    return len(r)
def g_of(F, T):
    return count_abs(F, -F.subs(x, T))

# ---------- 0. 원문 M27 직접 풀이 ----------
# f=2x^3+cx, y=|f| 와 y=-f(1) 이 네 점. c 전수(정수 -40..40 + 유리 격자)로 네 점이 되는 c 는 -6 하나
cands = [Rational(n, 4) for n in range(-160, 161)]
four = [C for C in cands if count_abs(2*x**3 + C*x, -(2 + C)) == 4]
chk(four == [-6], f'원문: 네 점이 되는 c = {four}')
chk(factor(4*p**3 - 6*p**2 + 2) == 2*(p - 1)**2*(2*p + 1), '원문 기호: -f(1)=4p^3 ⇔ 2(p-1)^2(2p+1)=0 ⇔ p=1')
orig_ans = (2*x**3 - 6*x).subs(x, 3)
chk(orig_ans == 36, f'원문 정답 f(3)={orig_ans} = 원문 선지 ② 36')

# ---------- 1. 새 문항: 기호 풀이 ----------
f = 2*x**3 - 6*p**2*x                  # c=-6p^2 (p>0)
M = 4*p**3
chk(expand(f + M - 2*(x - p)**2*(x + 2*p)) == 0, 'f+4p^3 = 2(x-p)^2(x+2p)  (극솟값 -4p^3, x=p, -2p)')
chk(expand(f - M - 2*(x + p)**2*(x - 2*p)) == 0, 'f-4p^3 = 2(x+p)^2(x-2p)  (극댓값 4p^3, x=-p, 2p)')
chk(expand(f - 2*x*(x - sqrt(3)*p)*(x + sqrt(3)*p)) == 0, 'f=0 ⇔ x=0, ±√3p')
# f(x)=k 가 서로 다른 세 실근 ⇔ k^2 < 16p^6 (판별식)
dsc = factor(discriminant(f - k, x))
chk(simplify(dsc - 108*(16*p**6 - k**2)) == 0, f'판별식 {dsc} = 108(16p^6-k^2)')
# 높이 k 에 대한 교점 개수 N(k): 수치 표본으로 0,3,6,4,2 확인 (p=1, 3/2, 2, 5/2)
def N_tab(P):
    F = f.subs(p, P); m = M.subs(p, P)
    return [count_abs(F, h) for h in (-1, 0, m/3, m/2, m, m + 1, 2*m)]
chk(all(N_tab(P) == [0, 3, 6, 6, 4, 2, 2] for P in (1, Rational(3, 2), 2, Rational(5, 2), 3)),
    'N(k): k<0 → 0, k=0 → 3, 0<k<M → 6, k=M → 4, k>M → 2')
# t>0 에서 g(t): 높이 h(t)=-f(t)
h = -f.subs(x, t)
chk(expand(M - h - 2*(t - p)**2*(t + 2*p)) == 0, 'M - (-f(t)) = 2(t-p)^2(t+2p) ≥ 0 (t>0): 높이는 M 을 넘지 않고 t=p 에서만 닿음')
# g 표: 0<t<p:6, t=p:4, p<t<√3p:6, t=√3p:3, t>√3p:0  (p 유리 표본으로 정확 계산)
def g_table(P):
    F = f.subs(p, P); r3 = sqrt(3)*P
    pts = [P/2, P, (P + r3)/2, r3, r3 + 1]
    out = []
    for T in pts:
        HT = -F.subs(x, T)
        if T == r3: out.append(count_abs(F, 0))          # 높이 0 (정확)
        else: out.append(count_abs(F, nsimplify(HT)) if HT.is_rational else None)
    return out
for P in (Rational(1, 2), 1, 2, Rational(5, 2), 3):
    F = f.subs(p, P)
    gp = [g_of(F, P / 2), g_of(F, P), g_of(F, Rational(int(P * 1300), 1000)), count_abs(F, 0), g_of(F, 2 * P)]
    chk(gp == [6, 4, 6, 3, 0], f'p={P}: g(p/2), g(p), g(1.3p), g(√3p), g(2p) = {gp}')
# t=p 는 제거 가능한 불연속(좌·우 6, 값 4), t=√3p 는 6 → 3 → 0
for P in (2, Rational(5, 2)):
    F = f.subs(p, P); e = Rational(1, 10**6)
    chk([g_of(F, P - e), g_of(F, P), g_of(F, P + e)] == [6, 4, 6], f'p={P}: t=p 근방 g = 6, 4, 6')
# c >= 0: f 증가, t>0 에서 g(t)=0, g(3)=0
for C in (0, 1, 5, 30):
    F = 2*x**3 + C*x
    chk(all(g_of(F, Rational(T, 10)) == 0 for T in range(1, 40)) and g_of(F, 3) == 0, f'c={C}: t>0 에서 g(t)=0 → (가) 실패, (나)는 성립')

# ---------- 2. 조건을 c 의 범위로 (기호 + 전수) ----------
# (가) g(3)=6 ⇔ 0 < -f(3) < M ⇔ p>√3, p≠3   (c<-18, c≠-54)
f3 = f.subs(x, 3)
chk(expand(M - (-f3) - 2*(p - 3)**2*(2*p + 3)) == 0, 'M-(-f(3)) = 2(p-3)^2(2p+3): (가)에서 위쪽 부등식은 p≠3 만 남김')
chk(solve(f3, p) and set(s for s in solve(f3, p) if s > 0) == {sqrt(3)}, '-f(3)>0 ⇔ p>√3')
def cond_A(C):
    return g_of(2*x**3 + C*x, 3) == 6
def disc_pts(C):
    """g 의 t>0 불연속점 (c<0): p, √3p.  c>=0: 없음"""
    if C >= 0: return []
    P = sqrt(Rational(-C, 6)); return [P, sqrt(3)*P]
def cond_B(C, ignore_removable=False):
    pts = disc_pts(C)
    if ignore_removable and pts: pts = pts[1:]
    return all(not (0 < q < 2) for q in pts)
grid = sorted(set([Rational(n, 2) for n in range(-160, 41)] + [Rational(v) for v in (-54, -24, -18, -8, -6, -2, 0)]
                  + [Rational(-24) + Rational(1, 100), Rational(-24) - Rational(1, 100), Rational(-18) - Rational(1, 100)]))
A_set = [C for C in grid if cond_A(C)]
chk(all((C < -18 and C != -54) == cond_A(C) for C in grid), f'(가) ⇔ c<-18, c≠-54  (격자 {len(grid)}개 전수, 정확 계산)')
chk(all(cond_B(C) == (C >= 0 or C <= -24) for C in grid), '(나) ⇔ c≥0 또는 c≤-24')
# (나) 를 불연속점 공식 대신 g 값 직접 비교로 확인 (p 유리인 c 에서): (0,2) 위 촘촘한 t 와 t=p 에서 g 가 일정한가
def cond_B_direct(P):
    F = f.subs(p, P)
    ts = [Rational(j, 50) for j in range(1, 100)] + ([P] if 0 < P < 2 else [])
    vals = set(g_of(F, T) for T in ts)
    if 0 < sqrt(3)*P < 2: vals.add(count_abs(F, 0))
    return len(vals) == 1
for P in (Rational(1, 2), 1, Rational(6, 5), Rational(3, 2), Rational(19, 10), 2, Rational(9, 4), 3):
    chk(cond_B_direct(P) == (P >= 2), f'p={P}: (0,2)에서 g 일정 = {cond_B_direct(P)} (기대 {P >= 2})')
feas = [C for C in grid if cond_A(C) and cond_B(C)]
chk(feas and max(feas) == -24 and all(C <= -24 and C != -54 for C in feas), f'(가)·(나) ⇒ c≤-24, c≠-54 (격자 최대 c={max(feas)})')
# 연속 자유도: c ≤ -24 전체가 가능 (c=-24-1/100, -30, -80 등)
chk(all(cond_A(C) and cond_B(C) for C in (Rational(-2401, 100), -25, -30, -53, -55, -80)), '연속 자유도: c<-24 의 여러 값도 조건 만족')
chk(not cond_A(-54), 'c=-54(p=3): g(3)=4 → 제외(최댓값과 무관)')
F_ans = 2*x**3 - 24*x
ans = F_ans.subs(x, 3)
# 최댓값: f(3)=54+3c 는 c 증가함수, 최대 c=-24
chk(ans == 54 + 3*max(feas) == -18, f'최댓값 f(3) = {ans} (f(x)=2x^3-24x, p=2: t=p=2 는 열린구간 끝점 밖)')
chk(g_of(F_ans, 3) == 6 and cond_B_direct(2), 'f(x)=2x^3-24x: g(3)=6, (0,2)에서 g≡6')

# ---------- 3. 선지·정답 ----------
ch = [sympify(v) for v in it['choices']]
chk(nsimplify(it['choices'][it['ans'] - 1]) == ans and it['ans'] == 2, f'정답 {ans} = 선지 {it["ans"]}번 (지정 ②)')
chk(len(set(ch)) == 5 and len({ch[i + 1] - ch[i] for i in range(4)}) == 1, f'선지 {ch} 서로 다름·등차')
chk(it.get('author') == 'claude', "author='claude'")

# ---------- 4. 오답 근거 ----------
# (1) t=p 의 제거 가능 불연속 무시 → (가) 아래서 (나) 자동 성립 → c<-18 만 남음, 경계 c=-18 → f(3)=0
feas_w1 = [C for C in grid if cond_A(C) and cond_B(C, ignore_removable=True)]
chk(set(feas_w1) == set(A_set) and 54 + 3*Rational(-18) == 0 and count_abs(2*x**3 - 18*x, 0) == 3,
    't=p 무시: 조건이 c<-18 로 줄고 경계 c=-18(f(3)=0, 이때 g(3)=3)')
w_rem = 0
# (2) 원문 풀이 그대로: f=2x^3-6x → 36
w_orig = orig_ans
# (3) p≥2 를 -c/6≥2 로 처리 → c≤-12 → 18
w_sq = 54 + 3*(-12)
chk({w_rem, w_orig, w_sq} <= set(ch), f'오답 {w_rem}, {w_orig}, {w_sq} 모두 선지에 있음')
chk(all(s in it['wrong'] for s in (r'\(0\)', r'\(36\)', r'\(18\)')), 'wrong 필드에 0, 36, 18 근거')

# ---------- 5. 조건 빼 보기 ----------
def report(name, need, why):
    print(f'ABLATION 17 {name}: ' + (f'필요({why})' if need else '군더더기(답 그대로)'))
    return need
abl = []
# (가) 제거: (나)만 → c≥0 도 가능, f(3)=54+3c 상한 없음
onlyB = [C for C in grid if cond_B(C)]
abl.append(report('(가) g(3)=6', max(54 + 3*C for C in onlyB) > ans and cond_B(100),
                  'c≥0이면 (나) 성립, c=0 → f(3)=54, c=100 → 354: 최댓값 없음'))
# (나) 제거: (가)만 → c<-18 (c≠-54), f(3)<0 이고 0 에 한없이 가까워짐 → 최댓값 없음
cA = Rational(-1801, 100)
abl.append(report('(나) (0,2)에서 연속', cond_A(cA) and 54 + 3*cA > ans and not cond_A(-18),
                  f'c={cA} 도 (가) 만족, f(3)={54 + 3*cA}; c=-18 은 제외 → 상한 0 에 닿지 않아 최댓값 없음'))
# 본문 '원점에 대하여 대칭' 제거: f=2x^3-8x^2+17 이 (가)(나) 만족, f(3)=-1 > -18
Fn = 2*x**3 - 8*x**2 + 17
crit = solve(diff(Fn, x), x)
levels = sorted(set([SS(0)] + [abs(Fn.subs(x, r)) for r in crit]))
# (0,2) 에서 f 감소(f'<0), f(2)=1>0 → 높이 -f(t)<0 → g(t)=0
chk(set(crit) == {0, Rational(8, 3)} and Fn.subs(x, 2) == 1, '반례 f=2x^3-8x^2+17: (0,8/3)에서 감소, f(2)=1>0')
nB = all(g_of(Fn, Rational(j, 50)) == 0 for j in range(1, 100))
abl.append(report('본문 원점 대칭', g_of(Fn, 3) == 6 and nB and Fn.subs(x, 3) > ans,
                  f'f=2x^3-8x^2+17: g(3)={g_of(Fn, 3)}, (0,2)에서 g≡0, f(3)={Fn.subs(x, 3)} > -18 → 답 바뀜'))
# 본문 '최고차항의 계수 2' 제거: f=x^3-12x (p=2) → f(3)=-9
Fl = x**3 - 12*x
dB = all(g_of(Fl, Rational(j, 50)) == 6 for j in range(1, 100)) and g_of(Fl, 2) == 4  # t=2 는 구간 밖
abl.append(report('본문 최고차항 계수 2', g_of(Fl, 3) == 6 and dB and Fl.subs(x, 3) != ans,
                  f'f=x^3-12x: g(3)={g_of(Fl, 3)}, (0,2)에서 g≡6, f(3)={Fl.subs(x, 3)} → 답 바뀜'))
chk(all(abl), '조건 빼 보기: 모두 필요')

print('ALL OK' if ok else 'SOME FAIL')
