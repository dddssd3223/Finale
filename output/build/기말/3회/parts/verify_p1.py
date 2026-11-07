# -*- coding: utf-8 -*-
# p1.py (3회 1–4번) 검증: 원문 풀이 · 계산 정답 = 지정 선지(분담표 정답 번호) · 유일성(전수) · 선지 5개 서로 다름·등차 · wrongs가 선지에 있고 실제 경로로 나옴 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, factor, nsimplify, Poly, real_roots, oo, limit
x, t, a, C = symbols('x t a C', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {1: 3, 2: 1, 3: 4, 4: 2}                                   # 분담표 정답 ③ ① ④ ②
KEY = {1: ('M41', 'M41 후보_순위 1'), 2: ('I53', 'I53 후보_순위 1'), 3: ('M52', 'M52 후보_순위 1'), 4: ('I49', '자체 (가장 가까운 I49)')}
assert sorted(IT) == [1, 2, 3, 4]
for n, it in IT.items():
    assert (it['key'], it['db_ref']) == KEY[n], n
    assert it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐') and it['precedent']
    assert it['ops'] and all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops'])
    assert '함정 추가' not in it['vtype'] and it['level'] in ('하', '중', '중상', '상', '최상')
    assert 'cond' not in it and 'class="fig"' not in it['body']      # 1–4번: 상자·그림 없음
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])

def cv(c):
    return nsimplify(str(c))

def arith(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0, list(d)[0]

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    ok_ar, dd = arith(no)
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and ok_ar and dd > 0
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {dd}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def maxmin(f, lo, hi):
    """닫힌구간 [lo, hi]에서 다항식 f의 최댓값·최솟값 (끝값과 구간 안 임계점 비교)"""
    cand = [lo, hi] + [r for r in real_roots(Poly(diff(f, x), x)) if lo < r < hi]
    vals = [f.subs(x, c) for c in cand]
    return max(vals), min(vals)

def turn_times(pos, lo=0):
    """위치 pos(t)에서 t>lo인 운동 방향 전환 시각 = 속도의 부호가 바뀌는 근"""
    v = diff(pos, t)
    rs = sorted({r for r in real_roots(Poly(v, t)) if r > lo})
    eps = Rational(1, 1000)
    return [r for r in rs if sp.sign(v.subs(t, r - eps)) * sp.sign(v.subs(t, r + eps)) < 0]

# ===== 원문 풀이 =====
# M41: [1,4]에서 x^3-3x^2+a, M+m=20 → a=4 (④)
sols = [A for A in range(-50, 51) if sum(maxmin(x**3 - 3*x**2 + A, 1, 4)) == 20]
assert sols == [4]
# I53: ∫_0^x f=3x^3+2x → f(1)=11 (③)
assert diff(3*x**3 + 2*x, x).subs(x, 1) == 11
# M52: x=t^3-(3/2)t^2-6t → 방향 전환 t=2, 가속도 9 (②)
p52 = t**3 - Rational(3, 2)*t**2 - 6*t
assert turn_times(p52) == [2] and diff(p52, t, 2).subs(t, 2) == 9
# I49: f'=6x^2+5, f(0)=3 → f(1)=10 (단답)
assert 3 + integrate(6*x**2 + 5, (x, 0, 1)) == 10
print('원문 풀이 OK (M41=4, I53=11, M52=9, I49=10)')

# ===== 1번 =====
f1 = x**3 - 6*x**2 + 9*x + a
assert expand(diff(f1, x) - 3*(x - 1)*(x - 3)) == 0
assert expand(f1 - a - x*(x - 3)**2) == 0
# 극대점 x=1은 구간 밖, 극소점 x=3은 구간 안
assert not (2 <= 1 <= 5) and 2 < 3 < 5
assert [f1.subs(x, c) - a for c in (2, 3, 5)] == [2, 0, 20]
# 전수: 정수 a를 넓게 훑어 M+m=30인 a (a는 모든 후보에 공통이라 M+m=2a+20, 선형 → 해 하나)
sols1 = [A for A in range(-200, 201) if sum(maxmin(f1.subs(a, A), 2, 5)) == 30]
assert sols1 == [5]
M_, m_ = maxmin(f1.subs(a, 0), 2, 5)
assert (M_, m_) == (20, 0)
assert solve(2*a + (M_ + m_) - 30, a) == [5]
v1 = sols1[0]
# 오답: 양 끝값만 비교 (a+20)+(a+2)=30
w1_end = solve((f1.subs(x, 5)) + (f1.subs(x, 2)) - 30, a)[0]
assert w1_end == 4
# 원문 구조 보존: 왼쪽 끝값-최솟값 = 2, M-m = 20 (원문과 같음)
assert f1.subs(x, 2) - f1.subs(x, 3) == 2 == (x**3 - 3*x**2).subs(x, 1) - (x**3 - 3*x**2).subs(x, 2)
assert M_ - m_ == 20 == (x**3 - 3*x**2).subs(x, 4) - (x**3 - 3*x**2).subs(x, 2)
chk(1, v1, [w1_end])

# ===== 2번 =====
F2 = x**3 + 5*x
assert F2.subs(x, 0) == 0                                       # 아래끝 0과 우변 상수항 0이 맞음(조건이 모순 없음)
f2 = diff(F2, x)
assert expand(f2 - (3*x**2 + 5)) == 0
# 유일성: f를 일반 다항식(차수 ≤6)으로 두고 항등식 ∫_0^x f = x^3+5x 를 풀면 하나
cs = symbols('c0:7')
fg = sum(cs[i]*t**i for i in range(7))
eqs = Poly(expand(integrate(fg, (t, 0, x)) - F2), x).all_coeffs()
sol2 = solve(eqs, cs, dict=True)
assert len(sol2) == 1 and expand(fg.subs(sol2[0]).subs(t, x) - f2) == 0
v2 = f2.subs(x, 2)
assert v2 == 17
w2_int = F2.subs(x, 2)                                          # ∫_0^2 f = 우변에 x=2 대입
assert w2_int == integrate(f2, (x, 0, 2)) == 18
chk(2, v2, [w2_int])

# ===== 3번 =====
p3 = t**3 - Rational(3, 2)*t**2 - 18*t
v3t = diff(p3, t)
assert expand(v3t - 3*(t - 3)*(t + 2)) == 0
tt = turn_times(p3)                                             # t>0에서 방향 전환 시각 전수
assert tt == [3]
assert v3t.subs(t, 0) != 0                                      # t=0은 정지 상태 아님
acc = diff(p3, t, 2)
assert expand(acc - (6*t - 3)) == 0
v3 = acc.subs(t, tt[0])
assert v3 == 15
# 원문 구조 보존: 두 근의 합 1 → t^2 계수 -3/2, 가속도 6t-3 원문과 같음
assert solve(v3t, t) == [-2, 3] and sum(solve(v3t, t)) == 1 and expand(acc - diff(p52, t, 2)) == 0
# 오답: 3t^2-3t-18을 3(t+3)(t-2)로 잘못 인수분해 → t=2에서 가속도
wrong_v = 3*(t + 3)*(t - 2)
assert expand(wrong_v) == 3*t**2 + 3*t - 18 and expand(wrong_v) != expand(v3t)  # 일차항 부호만 다름
w3_fac = acc.subs(t, [r for r in solve(wrong_v, t) if r > 0][0])
assert w3_fac == 9
chk(3, v3, [w3_fac])

# ===== 4번 (자체 기본형) =====
C1, C2 = symbols('C1 C2', real=True)
L4, R4 = x**2 + C1, 3*x + C2                                    # x<1, x>1에서의 부정적분
assert expand(diff(L4, x) - 2*x) == 0 and diff(R4, x) == 3
sol4 = solve([L4.subs(x, 0) - 1, L4.subs(x, 1) - R4.subs(x, 1)], [C1, C2], dict=True)   # f(0)=1, x=1에서 연속
assert len(sol4) == 1 and sol4[0] == {C1: 1, C2: -1}            # 적분상수 둘이 하나로 정해짐
fL, fR = L4.subs(sol4[0]), R4.subs(sol4[0])
v4 = fR.subs(x, 3)
assert v4 == 8 == 1 + integrate(2*x, (x, 0, 1)) + integrate(3, (x, 1, 3))
f4pw = sp.Piecewise((fL, x <= 1), (fR, True))
assert limit(fL, x, 1, '-') == limit(fR, x, 1, '+') == f4pw.subs(x, 1) == 2          # 연속
dl = limit((fL - 2)/(x - 1), x, 1, '-'); dr = limit((fR - 2)/(x - 1), x, 1, '+')
assert (dl, dr) == (2, 3)                                       # x=1에서 미분가능하지 않음 → f'(1)을 두지 않은 것이 맞음
w4_noinit = integrate(2*x, (x, 0, 1)) + integrate(3, (x, 1, 3))  # 초기값 빠뜨림
w4_sameC = (3*x + 1).subs(x, 3)                                 # 두 구간 적분상수를 모두 f(0)=1로
assert w4_sameC == (x**2 + 1).subs(x, 3) == 10 and w4_noinit == 7
chk(4, v4, [w4_noinit, w4_sameC])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 1번
assert limit(f1, x, oo) == oo and limit(f1, x, -oo) == -oo
print('ABLATION 1 닫힌구간 [2, 5]: 필요(빼면 실수 전체에서 최댓값·최솟값이 존재하지 않음)')
s1c = [A for A in range(-200, 201) if sum(maxmin(f1.subs(a, A), 2, 4)) == 30]
print(f'ABLATION 1 오른쪽 끝 5: 필요(4이면 M=f(4)=a+4, m=a라 답 {s1c} ≠ [5])')
assert s1c == [13]
print('ABLATION 1 M+m=30: 필요(빼면 a가 정해지지 않음)')
# 2번
print('ABLATION 2 모든 실수 x에 대하여: 필요(한 x에서만 성립하면 f가 정해지지 않음, 예: f=3x^2+5와 f=3x^2+5+k(3x^2-2x) 모두 x=1에서 성립)')
gk = 3*x**2 + 5 + 7*(3*x**2 - 2*x)
assert integrate(gk, (x, 0, 1)) == F2.subs(x, 1) and gk.subs(x, 2) != v2
print('ABLATION 2 우변 x^3+5x: 필요(우변이 없으면 f가 정해지지 않음)')
# 3번
tt_all = sorted({r for r in real_roots(Poly(v3t, t))})
acc_all = sorted({acc.subs(t, r) for r in tt_all})
print(f'ABLATION 3 t≥0: 필요(빼면 방향 전환 시각 {tt_all}, 가속도 {acc_all}로 정해지지 않음)')
assert len(acc_all) == 2
p3b = t**3 - Rational(3, 2)*t**2 - 6*t
print(f'ABLATION 3 -18t: 필요(원문 -6t이면 답 {diff(p3b, t, 2).subs(t, turn_times(p3b)[0])} ≠ {v3})')
# 4번
vals = sorted({(3*x + c).subs(x, 3) for c in (-1, 0, 1, 5)})
print(f'ABLATION 4 연속: 필요(빼면 x>1에서 f=3x+C2의 C2가 정해지지 않음, 예 f(3)={vals})'); assert len(vals) > 1
vals0 = sorted({(3*x + c - 2).subs(x, 3) for c in (0, 1, 2)})   # f(0)=c이면 C2=c-2
print(f'ABLATION 4 f(0)=1: 필요(빼면 C1이 정해지지 않음, 예 f(3)={vals0})'); assert len(vals0) > 1
v4b = (5*x + (1 + 1 - 5)).subs(x, 3)
print(f"ABLATION 4 x>1에서 f'(x)=3: 필요(5이면 답 {v4b} ≠ {v4})"); assert v4b != v4

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
