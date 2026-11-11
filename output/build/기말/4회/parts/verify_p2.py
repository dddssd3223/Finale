# -*- coding: utf-8 -*-
# p2.py (4회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, limit, oo, cos, sin, pi, simplify, Piecewise, Abs, factor
x, t, a, b, c, d1, d2, k = symbols('x t a b c d1 d2 k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 3, 6: 5, 7: 1, 8: 4}                                       # 분담표 목표 정답
REF = {5: 'I20 후보_순위 2', 6: 'I12 후보_순위 2', 7: 'M38 예상밖 1', 8: 'J24 후보_순위 2'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['I20', 'I12', 'M38', 'J24']
OPS = {f'OP{i:02d}' for i in range(1, 56)}
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐')
    assert it['ops'] and all(o in OPS for o in it['ops']) and it['precedent']
    assert COEF & set(it['ops']), n                                   # 계수·매개변수 자리 조작(6·7번 필수, 5·8번도 넣음)
    assert '함정 추가' not in it['vtype'] and len(it['vtype']) <= 3 and it['level'] in ('하', '중', '중상', '상', '최상')
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body'):
        assert it[f]
    assert 'class="fig"' not in it['body']                           # 1–8번 그림 없음
    assert ('cond' in it) == (n == 5)                                 # 상자: 5번만(원문대로), 6·7·8번은 문장 조건
    for w in it['wrongs']:                                            # wrong 설명에 선지 번호와 값이 함께 있음
        assert f'{"①②③④⑤"[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)

def cv(c_):
    c_ = str(c_)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', c_)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(c_)

def arith(no):
    v = [cv(c_) for c_ in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs):
    ch = [cv(c_) for c_ in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {ch[1] - ch[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

# ===== 원문 풀이 =====
# I20: f 우함수·주기 2, ∫_{-1}^{3} f = 12 → ∫_0^{15} f = 45.  우함수·주기 2인 연속함수족 f = c + d1 cos(πx) + d2 cos(2πx)로 확인
fam = c + d1*cos(pi*x) + d2*cos(2*pi*x)
assert simplify(fam.subs(x, -x) - fam) == 0 and simplify(fam.subs(x, x + 2) - fam) == 0
c20 = solve(integrate(fam, (x, -1, 3)) - 12, c)
assert c20 == [3] and simplify(integrate(fam.subs(c, 3), (x, 0, 15))) == 45
# I12: f = ∫_0^x (3t^2+a) dt, lim_{x→1} (f-3)/(x^2-1) = b → a+10b = 27
f12 = integrate(3*t**2 + a, (t, 0, x))
a12 = solve(f12.subs(x, 1) - 3, a)
assert a12 == [2]
b12 = limit((f12.subs(a, 2) - 3)/(x**2 - 1), x, 1)
assert b12 == Rational(5, 2) and 2 + 10*b12 == 27
# M38: x1 = t^3+2t^2-3t, x2 = t^2+5t, 거리 12 → p+q = 47
D38 = expand((t**3 + 2*t**2 - 3*t) - (t**2 + 5*t))
ts38 = sorted({r for s_ in (12, -12) for r in real_roots(Poly(D38 - s_, t)) if r >= 0})
assert ts38 == [3] and (diff(t**3 + 2*t**2 - 3*t, t) + diff(t**2 + 5*t, t)).subs(t, 3) == 47
# J24: f = x^3-4x^2+5x, S1 = 2∫_0^2 (f-x), S2 = 2{∫_2^3 (f-x) + ∫_3^{9/2} (9-2x)} → 9.  뼈대(학교식_예상 2) 스케치 19/6
f24 = x**3 - 4*x**2 + 5*x
assert expand(f24 - x - x*(x - 2)**2) == 0 and real_roots(Poly(f24 + x - 9, x)) == [3]
S1o = 2*integrate(f24 - x, (x, 0, 2)); S2o = 2*(integrate(f24 - x, (x, 2, 3)) + integrate(9 - 2*x, (x, 3, Rational(9, 2))))
assert (S1o, S2o, S1o + S2o) == (Rational(8, 3), Rational(19, 3), 9) and S2o/2 == Rational(19, 6)
print('원문 풀이 OK (I20=45, I12=27, M38=47, J24=9)')

# ===== 5번 (I20 후보_순위 2 = LIVE2-03-088 + 조작_보강 1: F로 올림, 이동량 a) =====
# (1) 조건만으로 유도: 정수점의 F값과 a를 미지수로 두고 (가)·(나)·F(0)=0·F(1)=5를 연립 → F(7)-F(-3)이 하나로 정해짐
Fv = {n: symbols(f'F_{"m" if n < 0 else ""}{abs(n)}') for n in range(-9, 10)}
def sys5(use=('가', '나', 'F1')):
    eqs = [Fv[0]]                                                     # F(0) = ∫_0^0 f = 0
    if '가' in use: eqs += [Fv[-n] + Fv[n] for n in range(1, 10)]
    if '나' in use: eqs += [Fv[n + 2] - Fv[n] - a for n in range(-9, 8)]
    if 'F1' in use: eqs += [Fv[1] - 5]
    return eqs
sol5 = solve(sys5(), list(Fv.values()) + [a], dict=True)
assert len(sol5) == 1 and sol5[0][a] == 10
v5 = sol5[0][Fv[7]] - sol5[0][Fv[-3]]
assert v5 == 50 and not v5.free_symbols
# (2) 실제 함수족으로 확인: F 기함수 ⇔ f 우함수, F(x+2)=F(x)+a ⇔ f 주기 2이고 한 주기 적분 a. f = c + d1 cos πx + d2 cos 2πx
Ffam = integrate(fam.subs(x, t), (t, 0, x))
assert simplify(Ffam.subs(x, -x) + Ffam) == 0                          # (가)
sh = simplify(Ffam.subs(x, x + 2) - Ffam)
assert sh == 2*c                                                      # (나): a = 2c
c5 = solve(Ffam.subs(x, 1) - 5, c)
assert c5 == [5] and sh.subs(c, 5) == 10
I5 = simplify(integrate(fam.subs(c, 5), (x, -3, 7)))
assert I5 == 50 and not I5.free_symbols                               # d1, d2와 무관하게 50
# 뼈대·스케치와 다른 수치인지: LIVE2-03-088(∫_0^1 f=4, [-3,9] → 48), 조작_보강 스케치(+6, [0,15] → 45)
assert simplify(integrate(fam.subs(c, 4), (x, -3, 9))) == 48 and simplify(integrate(fam.subs(c, 3), (x, 0, 15))) == 45
w5_4, w5_6 = 4*10, 6*10                                               # (나)를 네 번/여섯 번 적용
assert (w5_4, w5_6) == (40, 60)
chk(5, v5, [w5_4, w5_6])

# ===== 6번 (I12 후보_순위 2 = LIVE2-03-041 + 조작_보강 1: 극한점 k를 미지수로) =====
f6 = integrate(3*t**2 + 1, (t, 1, x))
assert expand(f6 - (x**3 + x - 2)) == 0
ks = real_roots(Poly(f6 - 8, x))                                      # (분자)→0: f(k)=8
assert ks == [2] and expand(f6 - 8 - (x - 2)*(x**2 + 2*x + 5)) == 0 and sp.discriminant(x**2 + 2*x + 5, x) < 0
assert all(diff(f6, x).subs(x, r) > 0 for r in (-3, 0, 3)) and sp.discriminant(diff(f6, x), x) < 0   # f'=3x^2+1>0: 증가 → k 유일
b6 = limit((f6 - 8)/(x - 2), x, 2)
assert b6 == 13 == diff(f6, x).subs(x, 2)
for kk in (Rational(-3), Rational(0), Rational(1), Rational(3, 2), Rational(3)):   # k≠2이면 분자가 0이 아니어서 극한값이 없음
    assert f6.subs(x, kk) != 8 and limit((f6 - 8)/(x - kk), x, kk, '+') in (oo, -oo)
v6 = 2 + b6
assert v6 == 15
w6_b = b6                                                             # b만 답함
# 뼈대 LIVE2-03-041(∫_1^x(3t^2+a), x→2, f-10 → a+b=18)과 다른 문항인지
fL = integrate(3*t**2 + a, (t, 1, x)); aL = solve(fL.subs(x, 2) - 10, a)
assert aL == [3] and aL[0] + diff(fL.subs(a, 3), x).subs(x, 2) == 18 and v6 != 18
chk(6, v6, [w6_b])

# ===== 7번 (M38 예상밖 1 + 조작_보강 1: 거리(차) → 중점(합의 절반)) =====
x1 = t**3 - 3*t**2 - t; x2 = 3*t**2 - 11*t
M7 = expand((x1 + x2)/2)
assert expand(2*M7 - (t**3 - 12*t)) == 0
D7 = expand(x1 - x2)
assert expand(D7 - t*(t**2 - 6*t + 10)) == 0 and sp.discriminant(t**2 - 6*t + 10, t) < 0   # t>0에서 P≠Q (선분 PQ가 항상 있음)
def moments(dist, lo=0):
    """|M(t)| = dist 인 t ≥ lo 전수"""
    return sorted({r for s_ in (dist, -dist) for r in real_roots(Poly(M7 - s_, t)) if lo is None or r >= lo})
ts7 = moments(8)
assert ts7 == [2, 4]
assert expand(2*(M7 + 8) - (t - 2)**2*(t + 4)) == 0 and expand(2*(M7 - 8) - (t - 4)*(t + 2)**2) == 0
g7 = 2*M7                                                             # t≥0에서 g의 최솟값이 정확히 -16 (t=2)
assert [r for r in solve(diff(g7, t), t) if r >= 0] == [2] and g7.subs(t, 2) == -16
vP = diff(x1, t)
assert expand(vP - (3*t**2 - 6*t - 1)) == 0 and [vP.subs(t, r) for r in ts7] == [-1, 23]
v7 = sum(vP.subs(t, r) for r in ts7)
assert v7 == 22
w7_pos = vP.subs(t, 4)                                                # 양의 경우(t=4)만
w7_spd = sum(abs(vP.subs(t, r)) for r in ts7)                         # 속력의 합
assert (w7_pos, w7_spd) == (23, 24)
# 뼈대 스케치(x1=t^3+t^2, x2=t^2+12t, 거리 16, P의 속도 합 72)와 다른 수치인지
Dsk = (t**3 + t**2) - (t**2 + 12*t)
tsk = sorted({r for s_ in (16, -16) for r in real_roots(Poly(Dsk - s_, t)) if r >= 0})
assert tsk == [2, 4] and sum(diff(t**3 + t**2, t).subs(t, r) for r in tsk) == 72 and v7 != 72
chk(7, v7, [w7_pos, w7_spd])

# ===== 8번 (J24 후보_순위 2 = 학교식_예상 2 + 예상밖 2 장치: 접선이 y=x, 계수 a) =====
f8a = x**3 + 3*x**2 + a*x
assert f8a.subs(x, 0) == 0                                            # 점 (0,0)은 a와 무관하게 곡선 위
a8 = solve(diff(f8a, x).subs(x, 0) - 1, a)                            # 접선 y=x ⇔ f(0)=0, f'(0)=1
assert a8 == [1]
f8 = f8a.subs(a, 1)
assert expand(f8 - x - x**2*(x + 3)) == 0
assert real_roots(Poly(f8 - x, x), multiple=True) == [-3, 0, 0]       # 곡선과 y=x: x=-3, x=0(접함)
r8 = real_roots(Poly(f8 - (-x + 6), x))
assert r8 == [1] and f8.subs(x, 1) == 5 and expand(f8 + x - 6 - (x - 1)*(x**2 + 4*x + 6)) == 0   # 곡선과 y=-x+6: (1,5) 하나
assert solve(x - (-x + 6), x) == [3]                                  # 두 직선: (3,3)
# 세 경계로 둘러싸인 부분은 꼭짓점 (0,0), (1,5), (3,3)인 부분 하나: 0≤x≤1에서 x ≤ f ≤ -x+6, 1≤x≤3에서 x ≤ -x+6 ≤ f
for q in [Rational(j, 20) for j in range(0, 61)]:
    fx, ln = f8.subs(x, q), -q + 6
    assert (q <= fx <= ln) if q <= 1 else (q <= ln <= fx)
top = Piecewise((f8, x <= 1), (-x + 6, True))
v8 = integrate(f8 - x, (x, 0, 1)) + integrate((-x + 6) - x, (x, 1, 3))
assert v8 == Rational(21, 4) == integrate(top - x, (x, 0, 3))
assert integrate(f8 - x, (x, 0, 1)) == Rational(5, 4) and Rational(1, 2)*4*2 == 4   # 곡선 부분 5/4 + 삼각형 (1,1),(1,5),(3,3) 넓이 4
# 다른 방법(신발끈 + 곡선 조각): 다각형 (0,0),(1,1),(3,3),(1,5)는 일직선 부분 때문에 삼각형 (1,1),(3,3),(1,5)와 같음
tri = Rational(abs((3 - 1)*(5 - 1) - (1 - 1)*(3 - 1)), 2)
assert tri == 4 and tri + Rational(5, 4) == v8
# 곡선과 y=x만으로 둘러싸인 부분(-3≤x≤0)은 직선 y=-x+6과 닿지 않음: 그 구간에서 f(x) < -x+6
assert all(f8.subs(x, q) < -q + 6 for q in [Rational(j, 10) for j in range(-30, 1)])
w8_nosub = integrate(f8, (x, 0, 1)) + 4                               # 곡선 부분에서 y=x를 빼지 않음
assert w8_nosub == Rational(23, 4)
chk(8, v8, [w8_nosub])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 5번
s_ = solve(sys5(use=('나', 'F1')), list(Fv.values()) + [a], dict=True)[0]
e5 = s_[Fv[7]] - s_[Fv[-3]]
g5 = c + d1*sin(pi*x)                                                  # 주기 2이지만 우함수가 아닌 예: F(1)=c+2d1/π
G5 = integrate(g5.subs(x, t), (t, 0, x))
cc = solve(G5.subs({x: 1, d1: pi}) - 5, c)[0]
alt5 = simplify(integrate(g5.subs({c: cc, d1: pi}), (x, -3, 7)))
print(f'ABLATION 5 (가): 필요(빼면 a가 정해지지 않아 답이 {e5}로 남음, 예: f=3+π sin πx이면 {alt5})'); assert e5.free_symbols and alt5 != v5 and simplify(G5.subs({c: cc, d1: pi}).subs(x, x + 2) - G5.subs({c: cc, d1: pi})) == 6
h5 = c + 3*d1*x**2                                                    # 우함수이지만 주기가 없는 예
H5 = integrate(h5.subs(x, t), (t, 0, x))
vals5 = {integrate(h5.subs({c: 5 - dd, d1: dd}), (x, -3, 7)) for dd in (0, 1, 2)}
print(f'ABLATION 5 (나): 필요(빼면 f=c+3dx^2, c+d=5에서 답이 {sorted(vals5)} 등으로 달라짐)'); assert len(vals5) == 3 and simplify(H5.subs(x, -x) + H5) == 0
s_ = solve(sys5(use=('가', '나')), list(Fv.values()) + [a], dict=True)[0]
e5b = s_[Fv[7]] - s_[Fv[-3]]
print(f'ABLATION 5 ∫_0^1 f=5: 필요(빼면 답이 {e5b}로 남아 정해지지 않음)'); assert e5b.free_symbols
print(f'ABLATION 5 (나)의 이동량 a(문자): (가)와 ∫_0^1 f=5로 a=10이 정해짐 — (가)가 실제로 쓰임'); assert sol5[0][a] == 10
# 6번
f6b = integrate(3*t**2 + 1, (t, 0, x)); k6b = real_roots(Poly(f6b - 8, x))
print(f'ABLATION 6 아래끝 1: 필요(0이면 k^3+k=8의 실근이 {sp.N(k6b[0], 4)}로 바뀌어 답이 달라짐)'); assert len(k6b) == 1 and k6b[0] != 2
k6c = real_roots(Poly(f6 - 28, x)); v6c = k6c[0] + diff(f6, x).subs(x, k6c[0])
print(f'ABLATION 6 분자의 상수 8: 필요(28이면 k={k6c[0]}, 답 {v6} → {v6c})'); assert k6c == [3] and v6c != v6
b6d = limit((f6 - 8)/(x**2 - 4), x, 2)
print(f'ABLATION 6 분모 x-k(원문 꼴 x^2-k^2이면): 답 바뀜 {v6} → {2 + b6d}'); assert 2 + b6d != v6
print('ABLATION 6 극한값이 존재(=b): 필요(k≠2이면 극한값이 없음 — 위에서 확인)')
# 7번
cnt = {dd: len(moments(dd)) for dd in (Rational(4), Rational(6), Rational(8), Rational(10), Rational(20))}
print(f'ABLATION 7 거리 8: 필요(거리별 순간의 수 {dict((str(k_), v_) for k_, v_ in cnt.items())} — 8보다 작으면 세 번, 크면 한 번이라 답이 달라짐)'); assert cnt[Rational(8)] == 2 and cnt[Rational(4)] == 3 and cnt[Rational(10)] == 1
pos_only = [r for r in real_roots(Poly(M7 - 8, t)) if r >= 0]
print(f'ABLATION 7 원점 사이의 거리(절댓값): 필요(중점의 위치가 8인 순간만이면 t={pos_only}, 답 {v7} → {sum(vP.subs(t, r) for r in pos_only)})'); assert pos_only == [4]
allt = moments(8, lo=None)
print(f'ABLATION 7 t≥0: 필요(빼면 순간이 {allt}로 늘어 답 {v7} → {sum(vP.subs(t, r) for r in allt)})'); assert allt == [-4, -2, 2, 4] and sum(vP.subs(t, r) for r in allt) != v7
ts_diff = sorted({r for s_ in (8, -8) for r in real_roots(Poly(D7 - s_, t)) if r >= 0})
print(f'ABLATION 7 중점(합의 절반): 필요(두 점 P, Q 사이의 거리가 8인 순간으로 읽으면 t={ts_diff}, 답 {v7} → {sum(vP.subs(t, r) for r in ts_diff)})'); assert ts_diff == [4] and sum(vP.subs(t, r) for r in ts_diff) == w7_pos
# 8번
def area8(av, kv=6):
    """f=x^3+3x^2+av·x (av≥1), y=x, y=-x+kv: 곡선이 x≥0에서 y=x 위에 있을 때 세 경계 부분의 넓이"""
    fa = x**3 + 3*x**2 + av*x
    rr = [r for r in real_roots(Poly(fa + x - kv, x)) if r > 0]
    assert len(rr) == 1
    assert all(fa.subs(x, q) >= q for q in [Rational(j, 10) for j in range(0, 61)])
    return integrate(fa - x, (x, 0, rr[0])) + integrate(kv - 2*x, (x, rr[0], Rational(kv, 2)))
assert area8(1) == v8
alt8 = sp.N(area8(2), 6)
print(f'ABLATION 8 접선이 y=x(a=1): 필요(a=2이면 넓이 {alt8}로 달라짐, a가 정해지지 않음)'); assert abs(alt8 - sp.N(v8)) > 1e-3
alt8k = area8(1, 24)                                                  # y=-x+24는 곡선과 (2, 22)에서 만남
print(f'ABLATION 8 직선 y=-x+6: 필요(y=-x+24이면 답 {v8} → {alt8k}; 빼면 둘러싸인 부분이 -3≤x≤0의 다른 부분이 됨)'); assert alt8k == 112 and alt8k != v8
loop8 = integrate(f8 - x, (x, -3, 0))
print(f'ABLATION 8 직선 y=x: 필요(빼면 세 경계가 되지 않음; 참고로 곡선과 y=x만으로 둘러싸인 부분은 {loop8})'); assert loop8 == Rational(27, 4)

print('ALL OK')
