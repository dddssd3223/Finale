# -*- coding: utf-8 -*-
# p3.py (8회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, Poly, real_roots, diff, expand, solve, integrate, sqrt, oo

x, t = symbols('x t', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 4, 10: 1, 11: 5, 12: 2}
DBREF = {9: 'M59 후보_순위 3', 10: 'M7 예상밖 1', 11: 'M35 예상밖 1', 12: 'M63 결합 1'}
KEYS = {9: 'M59', 10: 'M7', 11: 'M35', 12: 'M63'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

def val(c):
    c = re.sub(r'\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1) if m else Rational(c)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == '중', f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level 분담표와 같음')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    ok('이러한' not in it['body'] and '이와 같은' not in it['body'], f'{n}번 금지 어구 없음')
    ok(not re.search(r'\\[\(\[][^)\]]*[<>]', it['body']), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok('fig_10.svg' in IT[10]['body'] and os.path.exists(os.path.join(HERE, 'fig_10.svg')) and os.path.exists(os.path.join(HERE, '..', 'fig_10.svg')), '10번 그림 parts/fig_10.svg·회차 폴더 fig_10.svg 있음')

def chk(n, v0):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    return v

def pmin(P, lo=-oo, hi=oo):
    """다항식 P의 [lo, hi]에서의 최솟값(정확)"""
    cand = [r for r in real_roots(Poly(diff(P, x), x)) if lo <= r <= hi]
    cand += [c for c in (lo, hi) if c not in (-oo, oo)]
    return min(P.subs(x, c) for c in cand)

# ---------- 9번 (M59) ----------
a, b, c = symbols('a b c', real=True)
# 원문: f'(10)=296
fo = x**3 + a * x**2 + b * x + c
mid_o = expand(sp.cancel((fo.subs(x, 2 * x) - fo.subs(x, 0)) / (2 * x)))
ok(expand(mid_o - (4 * x**2 + 2 * a * x + b)) == 0, '9번 원문 가운데 = 4x²+2ax+b')
def orig_ok(av, bv):
    L = expand(mid_o - (diff(fo, x) / 2 + x**2 - 2)).subs({a: av, b: bv})
    R = expand(x**4 - mid_o).subs({a: av, b: bv})
    return pmin(L) >= 0 and pmin(R) >= 0
G = [(av, bv) for av in [Rational(i, 4) for i in range(-16, 17)] for bv in [Rational(j, 4) for j in range(-40, 17)] if orig_ok(av, bv)]
ok(G == [(0, -4)] and 3 * 100 - 4 == 296, f'9번 원문 M59 격자 전수 (a,b)={G} → f′(10)=296')
# 변형
f9 = x**3 + a * x**2 + b * x + c
mid = expand((f9.subs(x, 2 * x + 1) - f9.subs(x, 2 * x - 1)) / 2)
ok(expand(mid - (12 * x**2 + 4 * a * x + b + 1)) == 0, '9번 가운데 = 12x²+4ax+b+1 (= f′(2x)+1)')
ok(expand(mid - (diff(f9, x).subs(x, 2 * x) + 1)) == 0, '9번 가운데 = f′(2x)+1')
def ok9(av, bv, L=12 * x**2 - 1, R=x**4 + 8 * x**2 + 3, M=mid):
    m = M.subs({a: av, b: bv})
    d1 = expand(m - L); d2 = expand(R - m)
    if Poly(d1, x).degree() == 1 and Poly(d1, x).coeffs()[0] != 0: return False
    if Poly(d2, x).degree() == 1 and Poly(d2, x).coeffs()[0] != 0: return False
    return (d1.is_number and d1 >= 0 or not d1.is_number and pmin(d1) >= 0) and (d2.is_number and d2 >= 0 or not d2.is_number and pmin(d2) >= 0)
G9 = [(av, bv) for av in [Rational(i, 4) for i in range(-20, 21)] for bv in [Rational(j, 4) for j in range(-40, 21)] if ok9(av, bv)]
ok(G9 == [(0, -2)], f'9번 (a,b) 격자 전수(1/4 간격) → {G9}')
# 식으로도: 왼쪽 차 4ax+b+2 ≥ 0 ∀x ⇔ a=0, b≥−2 / a=0일 때 오른쪽 최솟값
ok(pmin(x**4 - 4 * x**2 + 2) == -2, '9번 오른쪽 x⁴−4x²+2의 최솟값 −2 (x²=2)')
f9s = x**3 - 2 * x
ok(expand(mid.subs({a: 0, b: -2}) - (12 * x**2 - 1)) == 0, '9번 a=0, b=−2에서 왼쪽은 등호(가운데 = 12x²−1)')
ok(diff(f9s, x).subs(x, 3) == 25, "9번 f′(x)=3x²−2, f′(3)=25")
v9 = chk(9, 25)
# 오답 26: +1을 빠뜨림
G9w = [(av, bv) for av in [Rational(i, 4) for i in range(-8, 9)] for bv in [Rational(j, 4) for j in range(-24, 9)] if ok9(av, bv, M=12 * x**2 + 4 * a * x + b)]
ok(G9w == [(0, -1)] and 27 - 1 == val(IT[9]['wrongs'][0]), f'9번 오답 26: +1 빠뜨리면 (a,b)={G9w}, f′(3)=26')
# 빼 보기
L1 = [(av, bv) for av in [Rational(i, 2) for i in range(-4, 5)] for bv in [Rational(j, 2) for j in range(-12, 5)] if ok9(av, bv, L=sp.Integer(-10**6))]
print(f'ABLATION 9 왼쪽 부등식: 필요(없으면 (a,b) 후보 {len(L1)}개 — a가 정해지지 않음)'); assert len(L1) > 1
R1 = [(av, bv) for av in [0] for bv in range(-2, 6) if ok9(av, bv, R=10**6 + x**4)]
print(f'ABLATION 9 오른쪽 부등식: 필요(없으면 b≥−2 전부, 예 b={R1[:3]}…)'); assert len(R1) > 1
G9c = [(av, bv) for av in [Rational(i, 4) for i in range(-8, 9)] for bv in [Rational(j, 4) for j in range(-24, 9)] if ok9(av, bv, M=expand((f9.subs(x, x + 1) - f9.subs(x, x - 1)) / 2))]
print(f'ABLATION 9 인자 2x±1: 필요(x±1이면 조건을 만족시키는 (a,b)가 격자에서 {len(G9c)}개 — 하나로 정해지지 않음)'); assert G9c != [(0, -2)]

# ---------- 10번 (M7) ----------
# 원문: P(t,t), Q(2−t², t), 사다리꼴 POHQ
So = t * ((2 - t**2) + (2 - t**2 - t)) / 2
cr = [r for r in solve(diff(So, t), t) if r.is_real and 0 < r < 1]
ok(cr == [Rational(2, 3)] and So.subs(t, Rational(2, 3)) == Rational(22, 27), '10번 원문 M7 정답 22/27(②)')
# DB 예상밖 1·조작_보강 1 스케치 확인
fd = -x**2 + 4 * x
Sd = integrate(fd, (x, t, 2 * t))
ok(solve(diff(Sd, t), t) == [0, Rational(12, 7)] and Sd.subs(t, Rational(12, 7)) == Rational(288, 49), 'DB 조작_보강 1 스케치(∫_t^{2t}(−x²+4x)) t=12/7, 288/49 확인')
f10 = -x**2 + 6 * x + 40
ok(expand(f10 + (x + 4) * (x - 10)) == 0, '10번 f=−(x+4)(x−10), 0≤x≤10에서 f≥0')
S10 = integrate(f10, (x, t, 2 * t))
dS = expand(diff(S10, t))
ok(expand(dS - (2 * f10.subs(x, 2 * t) - f10.subs(x, t))) == 0 and expand(dS + (t - 4) * (7 * t + 10)) == 0, "10번 S′(t)=2f(2t)−f(t)=−(7t+10)(t−4)")
# 넓이 = ∫|f| 로 전수 (0<t<5)
def area(tv):
    return integrate(sp.Abs(f10), (x, tv, 2 * tv))
grid = [Rational(j, 20) for j in range(1, 100)]
vals = {tv: S10.subs(t, tv) for tv in grid}
ok(all(f10.subs(x, xv) >= 0 for xv in [Rational(j, 10) for j in range(0, 101)]), '10번 0<t<5에서 [t,2t]⊂[0,10], 넓이 = 정적분')
best = max(vals, key=vals.get)
ok(best == 4 and all(vals[tv] < S10.subs(t, 4) for tv in grid if tv != 4), f'10번 t 전수(1/20 간격): 최대는 t={best}뿐')
ok(S10.subs(t, 4) == Rational(464, 3), '10번 최댓값 464/3(묻지 않음, 분수라 t를 물음)')
v10 = chk(10, 4)
tw = [r for r in solve(f10.subs(x, 2 * t) - f10.subs(x, t), t) if r > 0]
ok(tw == [2] and val(IT[10]['wrongs'][0]) == 2, '10번 오답 2: S′=f(2t)−f(t)로 계수 2를 빠뜨린 값(구간 가운데가 꼭짓점 3)')
ok(S10.subs(t, 2) < S10.subs(t, 4), '10번 t=2는 최대가 아님')
# 빼 보기: 범위 (0<t<5) 없으면 넓이 ∫|f|가 t→∞에서 한없이 커짐
ok(area(Rational(20)) > S10.subs(t, 4), '범위 없으면 t=20에서 넓이가 더 큼')
print(f'ABLATION 10 닫힌구간 [0, 10]·0<t<5: 필요(정의역이 없으면 넓이 ∫|f|가 한없이 커져 최대가 없음, t=20에서 {area(20)}). 0<t<5는 원문 (0<t<1)처럼 정의역에서 따라 나오는 범위를 원문 꼴대로 적은 것')
S1 = integrate(f10, (x, t, t + 1)); r1 = solve(diff(S1, t), t)
print(f'ABLATION 10 구간 끝 2t: 필요(t+1이면 t={r1})'); assert r1 != [4]

# ---------- 11번 (M35) ----------
def gmax(F, lo, hi):
    cand = [lo, hi] + [r for r in real_roots(Poly(diff(F, x), x)) if lo < r < hi]
    return max(F.subs(x, cc) for cc in cand)
fo11 = x**3 / 7 - x**2
go = {tv: gmax(fo11, tv, tv + 3) for tv in [Rational(j, 10) for j in range(0, 51)]}
ok(max(go.values()) + min(go.values()) == 4 and min(go, key=go.get) == 3, '11번 원문 M35 정답 4(④), 최소 t=3')
f11 = x**3 / 13 - x**2
ok(expand(13 * (f11 - f11.subs(x, 4)) - (x - 4) * (x - 12) * (x + 3)) == 0 and expand(13 * f11 - x**2 * (x - 13)) == 0, '11번 13(f−f(4))=(x−4)(x−12)(x+3), 13f=x²(x−13)')
def argmin_g(w, T=[Rational(j, 8) for j in range(0, 49)]):
    gv = {tv: gmax(f11, tv, tv + w) for tv in T}
    m = min(gv.values())
    return [tv for tv in T if gv[tv] == m], gv
W = [Rational(j, 4) for j in range(1, 81)]          # w = 1/4 .. 20
good = [w for w in W if argmin_g(w)[0] == [4]]
ok(good == [8], f'11번 w 전수(1/4 간격, 0<w≤20): 0≤t≤6(1/8 간격)에서 g의 최솟점이 t=4뿐인 w = {good}')
# 실수 w로도: 최솟점 4 ⇔ f(4)=f(4+w)
ws = [r for r in solve(f11.subs(x, 4 + t) - f11.subs(x, 4), t) if r > 0]
ok(ws == [8], '11번 f(4+w)=f(4)의 양수 해 w=8 하나')
_, g8 = argmin_g(8, [Rational(j, 8) for j in range(0, 49)])
zeros = [tv for tv in g8 if tv > 0 and g8[tv] == 0]
ok(zeros == [5], f'11번 w=8에서 g(t)=0인 양수 t(1/8 간격, 0..6) = {zeros}')
ok(all(g8[tv] < 0 for tv in g8 if 0 < tv < 5) and all(g8[tv] > 0 for tv in g8 if tv > 5), '11번 0<t<5에서 g<0, t>5에서 g>0 (유일)')
v11 = chk(11, 5)
ok(13 - 12 == val(IT[11]['wrongs'][0]), '11번 오답 1: 다른 근 12를 폭으로 보아 t+12=13')
print("ABLATION 11 t=4에서 최소: 필요(없으면 w가 정해지지 않음)")
print(f"ABLATION 11 양수 t: 필요(g(0)=f(0)={g8[0]}이라 0도 g(t)=0을 만족시킴)")
assert g8[0] == 0
_, gall = argmin_g(8, [Rational(j, 2) for j in range(-40, 41)])
print(f"ABLATION 11 0≤t의 아래 끝 0: 필요(t가 음수까지면 t→−∞에서 g→−∞라 t=4에서 최소가 아님, g(−20)={gall[-20]})")
assert gall[-20] < g8[4]
g_long = argmin_g(8, [Rational(j, 4) for j in range(0, 81)])
assert g_long[0] == [4] and [tv for tv in g_long[1] if tv > 0 and g_long[1][tv] == 0] == [5]
print("ABLATION 11 위 끝 6: 원문 범위 꼴(0≤t≤5)을 따른 표현, 답에는 영향 없음(t≥0 전체여도 w=8, t=5) — 원문 문장 그대로 두는 학교식")
good4 = [w for w in [Rational(j, 4) for j in range(1, 81)] if argmin_g(w, [Rational(j, 8) for j in range(0, 33)])[0] == [4]]
assert len(good4) > 1
print(f'  (위 끝이 4이면 t=4가 끝점이라 w가 {len(good4)}개로 정해지지 않음 — 위 끝은 4보다 커야 함)')

# ---------- 12번 (M63) ----------
# 원문: (g∘g)(−1)=19
fo12 = (x - 2)**2 * (x - 5) + 3
ok(fo12.subs(x, 2) == 3 and fo12.subs(x, 6) == 19 and Rational(3 * (-1) - 9, -1 - 1) == 6, '12번 원문 M63 정답 19 (a=3, g(−1)=6, f(6)=19)')
f12 = -2 * x**3 + 15 * x**2 - 36 * x + 27
ok(expand(f12 + (x - 3)**2 * (2 * x - 3)) == 0 and expand(f12 + 1 + (x - 2)**2 * (2 * x - 7)) == 0, '12번 f=−(x−3)²(2x−3), f+1=−(x−2)²(2x−7)')
A = solve(1 + symbols('A') - f12.subs(x, 1), symbols('A'))
ok(A == [3], '12번 연속 조건 a=3 하나')
av = 3
def N(tv):
    n = 1 if (tv - av) < 1 else 0                    # x + 3 = t, x < 1
    n += len({r for r in real_roots(Poly(f12 - tv, x)) if r >= 1})
    return n
e = Rational(1, 1000)
crit = sorted({f12.subs(x, 1), f12.subs(x, 2), f12.subs(x, 3)})
ok(crit == [-1, 0, 4], '12번 N의 후보 경계 −1, 0, 4')
pat = [(N(cc - e), N(cc), N(cc + e)) for cc in crit]
ok(pat == [(2, 3, 4), (4, 3, 2), (2, 1, 0)], f'12번 N(t) 경계 좌·값·우 {pat}')
T = [Rational(j, 4) for j in range(-40, 61)]
jumpsN = [tv for tv in T if not (N(tv - e) == N(tv) == N(tv + e))]
ok(jumpsN == [-1, 0, 4], f'12번 N 불연속점(1/4 간격 전수 −10..15) {jumpsN}')
def h(tv): return N(tv) - N(tv - 4)
disc = [tv for tv in T if not (h(tv - e) == h(tv) == h(tv + e))]
ok(disc == [-1, 0, 3, 8], f'12번 h 불연속점(1/4 간격 전수) {disc}')
ok((h(4 - e), h(4), h(4 + e)) == (-2, -2, -2), '12번 t=4에서 h는 −2로 연속(상쇄)')
v12 = chk(12, sum(disc))
naive = sorted(set(jumpsN + [j + 4 for j in jumpsN]))
ok(sum(naive) == 14 and val(IT[12]['wrongs'][0]) == 14, '12번 오답 14: 상쇄를 보지 않고 −1, 0, 3, 4, 8을 더한 값')
# 빼 보기
for p in (3, 5):
    dp = [tv for tv in T if not (N(tv - e) - N(tv - p - e) == N(tv) - N(tv - p) == N(tv + e) - N(tv - p + e))]
    print(f'ABLATION 12 이동량 4: 필요(이동량 {p}이면 불연속점 {dp}, 합 {sum(dp)})'); assert sum(dp) != 10
def N2(tv, aa):
    n = 1 if (tv - aa) < 1 else 0
    return n + len({r for r in real_roots(Poly(f12 - tv, x)) if r >= 1})
alt = []
for aa in (2, 5):
    dd = [tv for tv in T if not (N2(tv - e, aa) - N2(tv - 4 - e, aa) == N2(tv, aa) - N2(tv - 4, aa) == N2(tv + e, aa) - N2(tv - 4 + e, aa))]
    alt.append((aa, sum(dd)))
print(f'ABLATION 12 연속 조건: 필요(a가 정해지지 않음. a=2이면 합 {alt[0][1]}, a=5이면 합 {alt[1][1]})')
assert all(s != 10 for _, s in alt)

print(f'{len(OK)} checks')
print('ALL OK')
