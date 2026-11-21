# -*- coding: utf-8 -*-
# p3.py (4회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, nsimplify, integrate, Abs, sqrt, factor

x, k, t, u = symbols('x k t u', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 2, 10: 3, 11: 5, 12: 1}
DBREF = {9: 'J51 결합 1', 10: 'J17 후보_순위 2', 11: 'I34 v3_추가 1', 12: 'I64 v3_추가 1'}
KEYS = {9: 'J51', 10: 'J17', 11: 'I34', 12: 'I64'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n], f'{n}번 정답 번호 {it["ans"]}·db_ref·key 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'level'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (10, 12)), '10·12번 ops에 계수·매개변수 자리 조작(OP11·12·28·38·51) 있음')
ok('cond' not in IT[9] and 'cond' not in IT[10] and len(IT[11]['cond']) == 2 and len(IT[12]['cond']) == 2, '조건 상자: 9·10번 없음, 11·12번 (가)(나)')
ok('fig_10.svg' in IT[10]['body'] and os.path.exists(os.path.join(HERE, 'fig_10.svg')), '10번 그림 fig_10.svg 있음')

def cv(c):
    return nsimplify(str(c))

def arith(n):
    v = [cv(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    return v

def chk(n, val):
    v = arith(n)
    ok(v[IT[n]['ans'] - 1] == val, f'{n}번 계산 정답 {val} = 선지 {IT[n]["ans"]}번')

def area_between(e, lo, hi):
    """∫_lo^hi |e| dx (e: x의 조각 없는 다항식) — 구간 안의 실근에서 나눠 적분"""
    rs = sorted({r for r in real_roots(Poly(e, x)) if lo < r < hi})
    pts = [lo] + rs + [hi]
    return sum(abs(integrate(e, (x, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))

# ---------- 9번 (J51) ----------
# 원문: f=x(4-x)/3, g=|x-1|-1 → 4S=14
f0 = x * (4 - x) / 3
L0, R0 = f0 - (-x), f0 - (x - 2)                     # x≤1: g=-x, x≥1: g=x-2
rl = [r for r in solve(L0, x) if r <= 1]; rr = [r for r in solve(R0, x) if r >= 1]
ok(rl == [0] and rr == [3], '9번 원문 J51 교점 x=0, 3 (조각 범위 안의 근만)')
S0 = integrate(L0, (x, 0, 1)) + integrate(R0, (x, 1, 3))
ok(4 * S0 == 14, f'9번 원문 J51 정답 4S=14 (S={S0})')
# 변형: f=|x(4-x)|, g=5
out9 = x**2 - 4 * x          # x<0 또는 x>4에서 f
in9 = -x**2 + 4 * x          # 0≤x≤4에서 f
r_out = sorted(r for r in solve(out9 - 5, x) if r < 0 or r > 4)
r_in = [r for r in solve(in9 - 5, x) if r.is_real and 0 <= r <= 4]
ok(r_out == [-1, 5] and r_in == [] and in9.subs(x, 2) == 4, '9번 교점 x=-1, 5뿐 (0≤x≤4에서 f의 최댓값 4<5)')
S9 = integrate(5 - out9, (x, -1, 0)) + integrate(5 - in9, (x, 0, 4)) + integrate(5 - out9, (x, 4, 5))
ok(S9 == Rational(44, 3) and S9 == Rational(6**3, 6) - 2 * Rational(4**3, 6), f'9번 S={S9} = 36 - 2×32/3')
B9 = integrate(out9 - 5, (x, 5, k))                                  # k>5
ok(expand(3 * (B9 - S9)) == expand(k**3 - 6 * k**2 - 15 * k + 56) and factor(k**3 - 6 * k**2 - 15 * k + 56) == (k - 7) * (k**2 + k - 8), '9번 k³-6k²-15k+56=(k-7)(k²+k-8)')
sol9 = [r for r in real_roots(Poly(B9 - S9, k)) if r > 5]
ok(sol9 == [7] and diff(B9, k).subs(k, 6) > 0, f'9번 k>5인 해는 k=7 하나 (k>5에서 넓이는 증가)')
chk(9, sol9[0])
# 오답: 절댓값(뒤집힌 조각)을 놓침 → S=36 → k=8
S9w = integrate(5 - out9, (x, -1, 5))
w9 = [r for r in real_roots(Poly(B9 - S9w, k)) if r > 5]
ok(S9w == 36 and w9 == [8] and '8' in IT[9]['wrongs'], f'9번 오답 8 = 절댓값을 놓친 S=36일 때의 k {w9}')
# 빼 보기
Bl = integrate(out9 - 5, (x, k, -1))                                  # k<-1 쪽
left = [r for r in real_roots(Poly(Bl - S9, k)) if r < -1]
print('ABLATION 9 단서 k>5: ' + (f'필요(없으면 k={left}도 넓이가 S)' if left else '군더더기(답 그대로)')); assert left == [-3]
print(f'ABLATION 9 절댓값: 필요(절댓값이 없으면 S=36, k={w9[0]})'); assert w9[0] != 7
# g=5의 높이: 4 이하이면 0≤x≤4 조각과 만나 영역이 달라짐
ok(all(not [r for r in solve(in9 - c, x) if r.is_real] for c in (5,)) and [r for r in solve(in9 - 4, x)] == [2], '9번 직선 y=5는 뒤집힌 조각 위(높이 4이면 접함)')

# ---------- 10번 (J17) ----------
# 원문: y=x³+x², y=-x²+k, y축, x=2, A=B → k=14/3 (4<k<5)
h0 = (x**3 + x**2) - (-x**2 + k)
k0 = solve(integrate(h0, (x, 0, 2)), k)
ok(k0 == [Rational(14, 3)] and 4 < k0[0] < 5, f'10번 원문 J17 정답 k=14/3 (선지 ④)')
# 변형
C10, V10 = 45, 18
cub = x**3 + x**2
par = -2 * (x + k)**2 + C10
h = expand(cub - par)                                  # 삼차 곡선 − 포물선
I10 = expand(integrate(-h, (x, 0, 2)))                 # 포물선이 y축 쪽에서 위일 때 A−B
ok(I10 == -4 * k**2 - 8 * k + 78, f'10번 ∫₀²(포물선−삼차)dx = {I10}')
def config(kv):
    """0≤x≤2에서 두 곡선의 배치와 실제 넓이 A(y축 쪽), B(직선 x=2 쪽). 교점이 구간 안에 정확히 하나일 때만 (A, B, 꼴)"""
    e = h.subs(k, kv)
    rs = sorted({r for r in real_roots(Poly(e, x)) if 0 < r < 2})
    if len(rs) != 1: return None
    r = rs[0]
    s0, s2 = e.subs(x, 0), e.subs(x, 2)
    if s0 == 0 or s2 == 0: return None
    A = abs(integrate(e, (x, 0, r))); B = abs(integrate(e, (x, r, 2)))
    return sp.nsimplify(A), sp.nsimplify(B), ('포물선이 y축 쪽에서 위' if s0 < 0 else '삼차 곡선이 y축 쪽에서 위')
# k>0: h'(x)=3x²+2x+4(x+k)>0 (0≤x≤2) → 교점은 많아야 하나, 배치는 '포물선이 y축 쪽에서 위'뿐
hp = diff(h, x)
ok(expand(hp - (3 * x**2 + 6 * x + 4 * k)) == 0, "10번 h'(x)=3x²+6x+4k: k>0, x≥0에서 양수 → 교점은 많아야 하나")
cand = [r for r in solve(sp.Eq(I10, V10), k)]
ok(sorted(cand) == [-5, 3], f'10번 -4k²-8k+78=18의 근 {sorted(cand)}')
A3, B3, shape3 = config(3)
ok(sp.simplify(A3 - B3 - V10) == 0 and shape3 == '포물선이 y축 쪽에서 위', f'10번 k=3: 실제 넓이 A−B=18 (교점 하나, {shape3})')
# k>0 전수: 두 부분이 모두 생기는 범위(h(0)<0<h(2))에서 A−B=I10(k)는 감소 → 18이 되는 k는 하나
lo_, hi_ = solve(sp.Eq(h.subs(x, 2), 0), k), solve(sp.Eq(h.subs(x, 0), 0), k)
rng = (max(r for r in lo_), max(r for r in hi_))        # (2 쪽 경계, y축 쪽 경계) 양수 근
ok(rng[0] < 3 < rng[1] and diff(I10, k).subs(k, 1) < 0, f'10번 두 부분이 모두 생기는 k>0의 범위 ({sp.N(rng[0], 4)}, {sp.N(rng[1], 4)}) 안에 k=3, A−B는 k>0에서 감소 → 유일')
grid = [Rational(j, 20) for j in range(1, 200)]
hits = [kv for kv in grid if (c := config(kv)) and sp.simplify(c[0] - c[1] - V10) == 0]
ok(hits == [3], f'10번 k=0.05~9.95(간격 0.05) 전수: 실제 넓이로 A−B=18인 k는 {hits}')
chk(10, Rational(3))
# 오답: 빼는 순서 거꾸로 → k=4
w10 = [r for r in solve(sp.Eq(-I10, V10), k) if r > 0]
ok(w10 == [4] and '4' in IT[10]['wrongs'], f'10번 오답 4 = B−A=18로 둔 값 {w10}')
# 빼 보기
cm6 = config(-6); cm5 = config(-5)
ok(cm6 is not None and sp.simplify(cm6[0] - cm6[1] - V10) == 0 and cm6[2] == '삼차 곡선이 y축 쪽에서 위', 'k=-6: 교점 하나, 삼차 곡선이 y축 쪽에서 위, A−B=18')
ok(cm5 is not None and sp.simplify(cm5[0] - cm5[1] + V10) == 0, 'k=-5(이차방정식의 다른 근): 배치가 뒤집혀 A−B=-18')
print('ABLATION 10 단서 k>0: 필요(없으면 k=-6도 A−B=18)')
kAB = [r for r in solve(sp.Eq(I10, 0), k) if r > 0]
print(f'ABLATION 10 A−B=18: 필요(A=B이면 k={kAB[0]} ≈ {sp.N(kAB[0], 4)})'); assert kAB[0] != 3
kC = [r for r in solve(sp.Eq(expand(integrate(-(cub - (-2 * (x + k)**2 + 44)), (x, 0, 2))), V10), k) if r > 0]
print(f'ABLATION 10 상수 45: 필요(44이면 k={kC[0]})'); assert kC[0] != 3

# ---------- 11번 (I34) ----------
a, C, c = symbols('a C c', real=True)
# 원문: f'=2x-1, ∫₁²f=0 → f(2)=7/6
fo = x**2 - x + C
Co = solve(integrate(fo, (x, 0, 1)) - integrate(fo, (x, 0, 2)), C)[0]
ok(fo.subs(C, Co).subs(x, 2) == Rational(7, 6), '11번 원문 I34 정답 7/6 (선지 ④)')
# 변형: (가) f'{f'-(2x+a)}=0 → f'=0 또는 f'=2x+a (다항식의 곱이 0), 상수함수가 아니므로 f=x²+ax+C
f11 = x**2 + a * x + C
F11 = integrate(f11, x)
ok(expand(diff(f11, x) * (diff(f11, x) - (2 * x + a))) == 0, "11번 f=x²+ax+C는 (가)를 만족시킴: f'{f'-(2x+a)}=0")
s11 = solve([F11.subs(x, -3) - F11.subs(x, 3), F11.subs(x, 3) - F11.subs(x, 6)], [a, C], dict=True)
ok(len(s11) == 1 and s11[0] == {a: -4, C: -3}, f'11번 (나)에서 (a, C) 유일: {s11}')
g11 = f11.subs(s11[0])
ok(expand(g11 - (x**2 - 4 * x - 3)) == 0 and expand(diff((x + 3) * (x - 3) * (x - 6) / 3, x) - g11) == 0, '11번 f=x²-4x-3 = {(x+3)(x-3)(x-6)/3}′')
ok(integrate(g11, (x, -3, 3)) == 0 and integrate(g11, (x, 3, 6)) == 0, '11번 ∫₋₃³f=0, ∫₃⁶f=0')
chk(11, g11.subs(x, 5))
# 오답: 대칭 구간에서 일차항을 지우지 않고 2∫₀³f로 계산
w11 = solve([2 * integrate(f11, (x, 0, 3)), integrate(f11, (x, 3, 6))], [a, C], dict=True)[0]
ok(w11 == {a: -6, C: 6} and f11.subs(w11).subs(x, 5) == 1 and '1' in IT[11]['wrongs'], f'11번 오답 1 = 2∫₀³f=0으로 둔 값 (a, C)={w11}')
# 빼 보기
fc = c + 0 * x; Fc = integrate(fc, x)
zc = solve([Fc.subs(x, -3) - Fc.subs(x, 3), Fc.subs(x, 3) - Fc.subs(x, 6)], c)
print("ABLATION 11 '상수함수가 아닌': " + (f'필요(상수함수 f(x)={zc[c]}도 (가), (나)를 만족시켜 f(5)={zc[c]}도 답)' if zc[c] == 0 else '확인')); assert zc[c] == 0
ok('0' in IT[11]['wrongs'] and zc[c] == 0, '11번 오답 0 = 상수함수 f(x)=0을 버리지 않은 값')
s_a = solve(F11.subs(x, 3) - F11.subs(x, 6), C)[0]       # F(-3)=F(3)을 뺌 → a가 남음
v_a = sp.simplify(f11.subs(C, s_a).subs(x, 5))
print(f'ABLATION 11 F(-3)=F(3): 필요(빼면 f(5)={v_a}, a에 따라 달라짐)'); assert v_a.free_symbols
s_b = solve(F11.subs(x, -3) - F11.subs(x, 3), C)[0]      # F(3)=F(6)을 뺌
v_b = sp.simplify(f11.subs(C, s_b).subs(x, 5))
print(f'ABLATION 11 F(3)=F(6): 필요(빼면 f(5)={v_b}, a에 따라 달라짐)'); assert v_b.free_symbols
fg = diff(c * (x + 3) * (x - 3) * (x - 6), x)            # (가)를 뺌: F(-3)=F(3)=F(6)인 삼차 F 아무거나
print(f'ABLATION 11 (가): 필요(빼면 예: F(x)=c(x+3)(x-3)(x-6)에서 f(5)={expand(fg.subs(x, 5))}, c에 따라 달라짐)'); assert expand(fg.subs(x, 5)).free_symbols

# ---------- 12번 (I64) ----------
aa, bb = symbols('aa bb', real=True)
def chain(init, m, aval=None, lin_shift=True):
    """[0,1]에서 f=init(u). f(x+1)=m·x·f(x)+a·x+b. u=x-(구간 왼쪽 끝).
    반환: (a, b, [1,2]의 식 f1(u), [2,3]의 식 f2(u)). aval을 주면 미분가능 조건 대신 그 값을 씀. lin_shift=False면 [2,3]에서 a(u+1)+b를 au+b로 잘못 둠"""
    b_ = init.subs(u, 1)                                 # x=0 대입: f(1)=b
    f1 = expand(m * u * init + aa * u + b_)
    if aval is None:
        sa = solve(diff(f1, u).subs(u, 0) - diff(init, u).subs(u, 1), aa)   # x=1에서 좌우 미분계수
        assert len(sa) == 1; aval = sa[0]
    f1 = f1.subs(aa, aval)
    f2 = expand(m * (u + 1) * f1 + (aval * (u + 1) if lin_shift else aval * u) + b_)
    return aval, b_, f1, f2
I01 = lambda e: integrate(e, (u, 0, 1))
# 원문: f=x, 계수 1 → 60∫₁²f=110
a0, b0, f1o, f2o = chain(u, 1)
ok((a0, b0) == (1, 1) and 60 * I01(f1o) == 110, '12번 원문 I64 정답 110 (a=b=1)')
ok(12 * (I01(f1o) + I01(f2o)) == 87, '12번 DB v3_추가 1 스케치(원문 조건, 12{g(1)+g(2)}=87) 확인')
# 변형: f=x+1, 계수 2
a12, b12, f1, f2 = chain(u + 1, 2)
ok((a12, b12) == (-1, 2), f'12번 a={a12}, b={b12} 유일(x=0 대입, x=1에서 미분가능)')
ok(expand(f1 - (2 * u**2 + u + 2)) == 0 and expand(f2 - (4 * u**3 + 6 * u**2 + 5 * u + 5)) == 0, f'12번 [1,2]: {f1}, [2,3]: {f2} (u=x-왼쪽 끝)')
ok(f1.subs(u, 0) == 2 and diff(f1, u).subs(u, 0) == 1, '12번 x=1에서 연속·미분가능(값 2, 기울기 1)')
ok(f2.subs(u, 0) == f1.subs(u, 1) and diff(f2, u).subs(u, 0) == diff(f1, u).subs(u, 1), '12번 x=2에서도 연속·미분가능(값 5, 기울기 5) → 조건을 만족시키는 함수가 있음')
ok(expand(f1.subs(u, x - 1) - (2 * x**2 - 3 * x + 3)) == 0 and expand(2 * x * (2 * x**2 - 3 * x + 3) - x + 2 - (4 * x**3 - 6 * x**2 + 5 * x + 2)) == 0, '12번 풀이의 식: [1,2]에서 f=2x²-3x+3, f(x+1)=4x³-6x²+5x+2')
g1, g2 = I01(f1), I01(f2)
ok(g1 == Rational(19, 6) and g2 == Rational(21, 2) and integrate(4 * x**3 - 6 * x**2 + 5 * x + 2, (x, 1, 2)) == g2, f'12번 g(1)={g1}, g(2)={g2}')
chk(12, 3 * (g1 + g2))
# 오답: [2,3]에서 일차식 a(u+1)+b를 au+b로 둠 → 44
_, _, f1w, f2w = chain(u + 1, 2, lin_shift=False)
ok(3 * (I01(f1w) + I01(f2w)) == 44 and '44' in IT[12]['wrongs'], '12번 오답 44 = [2,3]에서 ax+b의 x를 옮기지 않은 값')
_, _, f1a, f2a = chain(u + 1, 2, aval=1)
ok(3 * (I01(f1a) + I01(f2a)) == 63, '12번 참고: 원문 값 a=1로 두면 63(선지 밖)')
_, _, f1m, f2m = chain(u + 1, 1)
ok(3 * (I01(f1m) + I01(f2m)) == Rational(111, 4), '12번 참고: 계수 2를 빼면 111/4(선지 밖)')
# 빼 보기
_, _, f1s, f2s = chain(u + 1, 2, aval=aa)
va = sp.simplify(3 * (I01(f1s) + I01(f2s)))
print(f'ABLATION 12 미분가능: 필요(연속뿐이면 a가 정해지지 않아 값이 {va})'); assert va.free_symbols
a_x, _, f1x, f2x = chain(u, 2)
vx = 3 * (I01(f1x) + I01(f2x))
print(f'ABLATION 12 (가)의 상수항 1: 필요(f(x)=x이면 a={a_x}, 값 {vx})'); assert vx != 41
print('ABLATION 12 (나)의 계수 2: 필요(계수가 1이면 111/4)')

print(f'검사 {len(OK)}개')
print('ALL OK')
