# -*- coding: utf-8 -*-
# p2.py (9회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor, oo, Interval
x, t, s, a, b, c, k, p, r = symbols('x t s a b c k p r', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 3, 6: 1, 7: 4, 8: 2}                                       # 분담표 목표 정답
REF = {5: 'J23 분석집_변형 1', 6: 'I30 분석집_변형 1', 7: 'I48 분석집_변형 1', 8: 'M14 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['J23', 'I30', 'I48', 'M14']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'       # 분담표 목표 수준
    assert 'STUDY-' + it['key'] in it['precedent']                     # 분석집 변형 id
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 ×
    for w in it['wrongs']:
        assert f'{CIRC[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)
    txt = it['body']
    assert 'log' not in txt and '이러한' not in txt and '이와 같은' not in txt and '역함수' not in txt
    for mm in re.findall(r'\\\((.*?)\\\)|\\\[(.*?)\\\]', txt, re.S):
        assert '<' not in ''.join(mm) and '>' not in ''.join(mm), (n, mm)

def num(s_):
    s_ = re.sub(r'\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', r'(\1)/(\2)', s_)
    return nsimplify(sp.sympify(s_))

def chk(no, val, wrongs):
    it = IT[no]; chv = [num(c_) for c_ in it['choices']]; ws = [num(w) for w in it['wrongs']]
    dd = {chv[i + 1] - chv[i] for i in range(4)}
    good = (it['ans'] == WANT[no] and nsimplify(val) == chv[it['ans'] - 1] and len(set(chv)) == 5 and len(dd) == 1 and 0 not in dd
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {chv[it["ans"] - 1]} (위치 {it["ans"]}), 공차 {chv[1] - chv[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good
    # 정답이 본문에 나온 수와 같지 않음(8회 18번 지적)
    nums = {nsimplify(v) for v in re.findall(r'(?<![\w^{])\d+', it['body'])}
    assert nsimplify(val) not in nums, (no, val)

# ===== 원문·분석집 변형 풀이 =====
# J23: f=(2/7)x^3+x-16/7, 대칭이동하면 f와 y=x, y=-x → 1 + ∫_1^2 (x-f) = 31/14
fJ = R(2, 7)*x**3 + x - R(16, 7)
assert sp.real_roots(sp.Poly(fJ - x, x)) == [2] and sp.real_roots(sp.Poly(fJ + x, x)) == [1]
assert integrate(2*x, (x, 0, 1)) + integrate(x - fJ, (x, 1, 2)) == R(31, 14)
# STUDY-J23-변형①: f=x^3-5/2x^2+3x-2, 대칭이동 뒤 y=x, y=-x/2 → 11/6
fV = x**3 - R(5, 2)*x**2 + 3*x - 2
assert sp.real_roots(sp.Poly(fV - x, x)) == [2] and sp.real_roots(sp.Poly(fV + x/2, x)) == [1]
assert integrate(R(3, 2)*x, (x, 0, 1)) + integrate(x - fV, (x, 1, 2)) == R(11, 6)
# I30: f=x^3+qx, ∫(x+5)^2 f = 64 → q=9, 34/3 ; 변형①: ∫(x-1)^3 f = 44/7 → q=2, 13/3
q = symbols('q', real=True)
qa = solve(integrate((x + 5)**2*(x**3 + q*x), (x, -1, 1)) - 64, q); assert qa == [9]
assert integrate(x**2 + 9, (x, 1, 2)) == R(34, 3)
qb = solve(integrate((x - 1)**3*(x**3 + q*x), (x, -1, 1)) - R(44, 7), q); assert qb == [2]
assert integrate(x**2 + 2, (x, 1, 2)) == R(13, 3)
# I48: f=m(x-3), 2≤m≤5 → f(6)∈[6,15], 합 21 ; 변형①: f=(x-3)(x-r), -4≤r≤0 → 18+30=48
assert 3*2 + 3*5 == 21 and 3*(6 - 0) + 3*(6 - (-4)) == 48
# M14: t=x^2+3x-27/x, x<0에서 최솟값 9 → a=9 ; 변형①: p=2s^3+6s^2 극값 0, 8 → 8
hM = x**2 + 3*x - 27/x
assert sp.minimum(hM, x, Interval.open(-oo, 0)) == 9
gV = 2*s**3 + 6*s**2; assert sorted(gV.subs(s, v) for v in solve(diff(gV, s), s)) == [0, 8]
print('원문·분석집 변형 풀이 OK')

# ===== 5번 =====
f5k = x**3 - 3*x**2 + 7*x + k
ks = solve(f5k.subs(x, 1) - (-3), k); assert ks == [-8]
f5 = f5k.subs(k, -8)
assert sp.discriminant(diff(f5, x), x) < 0                               # f 증가
assert sp.real_roots(sp.Poly(f5 - x, x)) == [2]                            # y=x와 x=2에서만
assert sp.real_roots(sp.Poly(f5 + 3*x, x)) == [1]                          # y=-3x와 x=1에서만
# [1,2]에서 -3x ≤ f ≤ x (곡선이 두 직선 사이), [0,1]은 두 직선 사이 부분
assert all(-3*v <= f5.subs(x, v) <= v for v in [1 + R(i, 20) for i in range(21)])
assert all(f5.subs(x, v) < -3*v for v in [R(i, 20) for i in range(20)])  # [0,1)에서 곡선은 y=-3x 아래 → 경계 아님
# 넓이: 직접 영역 적분(위 경계 y=x, 아래 경계 max(-3x, f))
A5 = integrate(x - (-3*x), (x, 0, 1)) + integrate(x - f5, (x, 1, 2))
A5b = integrate(x - sp.Max(-3*x, f5), (x, 0, 2))
assert A5 == R(17, 4) and sp.nsimplify(sp.N(A5b, 30)) == R(17, 4)
chk(5, A5, [integrate(x - f5, (x, 1, 2)), integrate(3*x - x, (x, 0, 1)) + integrate(x - f5, (x, 1, 2))])
print('ABLATION 5 교점 조건(x=1에서 y=-3x와 만남): 필요(빼면 k가 정해지지 않아 넓이가 정해지지 않음)')
for kv in (-7, -9):
    fk = f5k.subs(k, kv); print('   (k =', kv, '이면 교점', [sp.N(v, 4) for v in sp.real_roots(sp.Poly(fk + 3*x, x))], [sp.N(v, 4) for v in sp.real_roots(sp.Poly(fk - x, x))], ')')
A_alt = integrate(x - (-x), (x, 0, sp.real_roots(sp.Poly(f5 + x, x))[0])) + integrate(x - f5, (x, sp.real_roots(sp.Poly(f5 + x, x))[0], 2))
print('ABLATION 5 직선 y=-3x → y=-x: 필요(넓이', sp.N(A_alt, 6), '로 바뀜)')

# ===== 6번 =====
f6 = x**3 + c*x
# 기함수·최고차항 1인 삼차의 일반형 확인
g6 = x**3 + a*x**2 + b*x + k
assert solve(sp.Poly(expand(g6.subs(x, -x) + g6), x).all_coeffs(), [a, k], dict=True) == [{a: 0, k: 0}]
I6 = integrate((x + 1)**3*f6.subs(x, 2*x), (x, -1, 1))
cs = solve(I6 - R(184, 7), c); assert cs == [3]                           # c 유일
assert expand(f6.subs(x, 2*x).subs(c, 3)) == 8*x**3 + 6*x
ans6 = integrate(sp.cancel(f6.subs(c, 3)/x), (x, 1, 2)); assert ans6 == R(16, 3)
# 오답 25/3: f(2x)를 8x^3+cx로
cw = solve(integrate((x + 1)**3*(8*x**3 + c*x), (x, -1, 1)) - R(184, 7), c); assert cw == [6]
chk(6, ans6, [integrate(x**2 + cw[0], (x, 1, 2))])
cn = solve(integrate((x + 1)**3*f6, (x, -1, 1)) - R(184, 7), c)[0]
print('ABLATION 6 인자 2x → x: 필요(c =', cn, ', 답', integrate(x**2 + cn, (x, 1, 2)), '로 바뀜)')
fg = x**3 + a*x**2 + c*x + k
print('ABLATION 6 기함수 조건: 필요(빼면 f=x^3+ax^2+cx+k의 미지수 3개를 식 하나로 정할 수 없음; 예',
      [integrate(sp.cancel((fg.subs({a: av, k: 0}).subs(c, solve(integrate((x + 1)**3*fg.subs({a: av, k: 0}).subs(x, 2*x), (x, -1, 1)) - R(184, 7), c)[0]))/x), (x, 1, 2)) for av in (0, 1)], ')')
print('ABLATION 6 정적분 값 184/7: 필요(빼면 c가 정해지지 않음)')

# ===== 7번 =====
# 차수: f(2t+1)-f(2t-1)-8t가 유계 ⇔ 상수. 일반 n차(n≤4)에서 확인
cf = symbols('e0:5', real=True)
for deg in range(0, 5):
    fn = sum(cf[i]*x**i for i in range(deg + 1))
    D = sp.Poly(expand(fn.subs(x, 2*t + 1) - fn.subs(x, 2*t - 1) - 8*t), t)
    # t의 1차 이상 계수가 모두 0이어야 함
    hi = [co for (e,), co in D.terms() if e >= 1]
    sol_ = solve(hi, cf[1:deg + 1], dict=True) if hi else [{}]
    ok = [sd for sd in sol_ if all(sp.simplify(h.subs(sd)) == 0 for h in hi)]
    if deg == 2: assert ok and ok[0][cf[2]] == 1
    elif deg > 2: assert all(sd.get(cf[deg], cf[deg]) == 0 for sd in ok)      # 최고차 계수 0 강제 → 실제 차수 ≤2
    else: assert not ok                                                        # 일차 이하는 -8t 항이 남음
f7 = x**2 + b*x + c
assert expand(f7.subs(x, 2*t + 1) - f7.subs(x, 2*t - 1)) == 8*t + 2*b
brng = Interval(-2, 2)
# 극소 조건: f(2)=0, 부호 - → +. f=(x-2)(x-r), r<2 (r=2면 극값 아님, r>2면 극대)
for rv, kind in ((R(-1), 'min'), (R(2), 'none'), (R(3), 'max')):
    F = integrate((t - 2)*(t - rv), (t, 0, x)); e = R(1, 1000)
    l, rr = F.subs(x, 2 - e) - F.subs(x, 2), F.subs(x, 2 + e) - F.subs(x, 2)
    assert (kind == 'min') == (l > 0 and rr > 0)
# b=-(2+r) ∈ [-2,2] → r∈[-4,0], r<2 자동
assert all(-2 <= -(2 + v) <= 2 for v in (-4, 0)) and -(2 + R(-41, 10)) > 2 and -(2 + R(1, 10)) < -2
f6v = lambda rv: (6 - 2)*(6 - rv)
lo, hi_ = f6v(0), f6v(-4); assert (lo, hi_) == (24, 40)
ints = [n_ for n_ in range(0, 100) if lo <= n_ <= hi_]                   # r 연속 → [24,40] 전체
ans7 = len(ints); assert ans7 == 17
chk(7, ans7, [hi_ - lo])
print('ABLATION 7 위쪽 부등식 ≤8t+4: 필요(빼면 b 상한이 없어 r의 하한이 없고 f(6)의 정수가 무수히 많음)')
# [t,t+2]이면: 4a=8 → a=2, -4 ≤ 4a+2b ≤ 4 → -6 ≤ b ≤ -2; f=2(x-2)(x-r), b=-2(2+r) → -1 ≤ r ≤ 1; f(6)=8(6-r)∈[40,56] → 17개? 확인
fa = 2*x**2 + b*x; assert expand(fa.subs(x, t + 2) - fa.subs(x, t)) == 8*t + 8 + 2*b     # -4≤8+2b≤4 → -6≤b≤-2
alt = sorted({2*(6 - 2)*(6 - v) for v in (-1, 1)})                   # f=2(x-2)(x-r), b=-2(2+r) → r∈[-1,1]
print('ABLATION 7 구간 [2t-1,2t+1] → [t,t+2]: 필요(이차항 계수가 2가 되어 f(6)∈', alt, ', 정수', alt[1] - alt[0] + 1, '개 — 개수는 같지만 범위가 바뀜)')
print('ABLATION 7 x=2에서 극소: 필요(빼면 f의 근이 정해지지 않음)')

# ===== 8번 =====
def disc_t(pv):
    """f(t)가 불연속인 t의 목록(정확): 후보는 판별식이 0인 t(접선 기울기)뿐, 좌·중·우 근 개수 비교"""
    P = x**3 - 9*x**2 - t*x + pv
    Dt = sp.Poly(sp.discriminant(P, x), t)
    cand = sorted(set(sp.real_roots(Dt)), key=lambda v: sp.N(v))
    def cnt(tv): return len(set(sp.real_roots(sp.Poly(P.subs(t, tv), x))))
    out = []
    for i, t0 in enumerate(cand):
        lo_ = cand[i - 1] if i else t0 - 10; hi2 = cand[i + 1] if i + 1 < len(cand) else t0 + 10
        lt = (lo_ + t0)/2 if i else t0 - 1; rt = (t0 + hi2)/2 if i + 1 < len(cand) else t0 + 1
        lt = sp.nsimplify(sp.N(lt, 40), rational=True); rt = sp.nsimplify(sp.N(rt, 40), rational=True)
        mid = sp.factor(P.subs(t, t0)) if t0.is_rational else None
        c0 = cnt(t0) if t0.is_rational else 2                            # 무리 기울기: 접점 중근 + 단순근(변곡점 아님 확인은 아래)
        if not (cnt(lt) == c0 == cnt(rt)): out.append(t0)
    return out
good8 = [pv for pv in range(-60, 30) if len(disc_t(pv)) == 3]
assert good8 == list(range(-26, 0)), good8
# 무리 기울기 경우 c0=2 가정 검증: 접점 s가 변곡점(s=3)이 아니면 중근+단순근 → 2개
gs = 2*s**3 - 9*s**2
assert solve(diff(x**3 - 9*x**2, x, 2), x) == [3] and gs.subs(s, 3) == -27
assert len(disc_t(0)) == 2 and len(disc_t(-27)) == 1 and expand((x - 3)**3) == x**3 - 9*x**2 + 27*x - 27
ans8 = len(good8)
chk(8, ans8, [0 - (-27), len(range(-27, 1))])
print('ABLATION 8 정수 p: 필요(실수 p면 무수히 많음)')
print('ABLATION 8 불연속인 t의 개수 3 → 2: 필요(p∈', [pv for pv in range(-60, 30) if len(disc_t(pv)) == 2], ')')
print('ABLATION 8 -9x^2 → -6x^2: 필요(개수', len([pv for pv in range(-40, 10) if pv > -8 and pv < 0]), '로 바뀜)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [3, 1, 4, 2]
print('ALL OK')
