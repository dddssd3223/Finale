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
f5k = x**3 + k
ks = solve(f5k.subs(x, 1) - (-5), k); assert ks == [-6]
f5 = f5k.subs(k, -6)
assert sp.real_roots(sp.Poly(f5 - x, x)) == [2]                            # y=x와 x=2에서만
assert sp.real_roots(sp.Poly(f5 + 5*x, x)) == [1]                          # y=-5x와 x=1에서만
assert all(-5*v <= f5.subs(x, v) <= v for v in [1 + R(i, 20) for i in range(21)])
assert all(f5.subs(x, v) < -5*v for v in [R(i, 20) for i in range(20)])  # [0,1)에서 곡선은 y=-5x 아래
A5 = integrate(x - (-5*x), (x, 0, 1)) + integrate(x - f5, (x, 1, 2))
A5b = integrate(x - sp.Max(-5*x, f5), (x, 0, 2))
assert A5 == R(27, 4) and sp.nsimplify(sp.N(A5b, 30)) == R(27, 4)
chk(5, A5, [integrate(5*x - x, (x, 0, 1)) + integrate(x - f5, (x, 1, 2))])
print('ABLATION 5 교점 조건(x=1에서 y=-5x와 만남): 필요(빼면 k가 정해지지 않아 넓이가 정해지지 않음)')
A_alt = integrate(2*x, (x, 0, sp.real_roots(sp.Poly(f5 + x, x))[0])) + integrate(x - f5, (x, sp.real_roots(sp.Poly(f5 + x, x))[0], 2))
print('ABLATION 5 직선 y=-5x → y=-x: 필요(넓이', sp.N(A_alt, 6), '로 바뀜)')
print('   (참고: 두 직선 사이 부분을 빠뜨리면', integrate(x - f5, (x, 1, 2)), ')')

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
P7, Q7 = -5, 4                                                          # P7 ≤ 2b ≤ Q7
# 극소 조건: f(2)=0, 부호 - → +. f=(x-2)(x-r), r<2 (r=2면 극값 아님, r>2면 극대)
def kind7(F):
    e = R(1, 1000); l, rr = F.subs(x, 2 - e) - F.subs(x, 2), F.subs(x, 2 + e) - F.subs(x, 2)
    return 'min' if (l > 0 and rr > 0) else ('max' if (l < 0 and rr < 0) else 'none')
for rv, kind in ((R(-1), 'min'), (R(2), 'none'), (R(3), 'max')):
    assert kind7(integrate((t - 2)*(t - rv), (t, 0, x))) == kind
# 전수: b를 [-5/2, 2] 밖·안의 촘촘한 격자에서 조건 판정 → f(6) 최대·최소
def ok7(bv):
    if not (P7 <= 2*bv <= Q7): return False
    fx = (x - 2)*(x - (-2 - bv))                                        # f(2)=0, 이차항 1
    return kind7(integrate(fx.subs(x, t), (t, 0, x))) == 'min'
grid = [R(i, 8) for i in range(-48, 49)]
vals = [((x - 2)*(x + 2 + bv)).subs(x, 6) for bv in grid if ok7(bv)]
mx7, mn7 = max(vals), min(vals); assert (mx7, mn7) == (40, 22)
assert sp.Interval(-R(5, 2), 2) == sp.Interval(R(P7, 2), R(Q7, 2)) and all(-2 - bv < 2 for bv in (-R(5, 2), 2))   # r<2 자동
ans7 = mx7 + mn7; assert ans7 == 62
w7 = (32 + 4*Q7) + (32 + 4*P7)                                          # 2로 나누지 않은 b 범위 [-5,4] → 48+12
chk(7, ans7, [w7])
print('ABLATION 7 위쪽 부등식 ≤8t+4: 필요(빼면 b 상한이 없어 f(6)의 최댓값이 없음)')
print('ABLATION 7 아래쪽 부등식 8t-5≤: 필요(빼면 b 하한이 없어 r<2 경계에서 최솟값이 없음)')
# [t,t+2]이면: f(t+2)-f(t)=4at+4a+2b → a=2, -5≤8+2b≤4 → -13/2≤b≤-2; f(2)=0 → f(6)=72+6b+c, c=-8-2b → 64+4b
fa = 2*x**2 + b*x; assert expand(fa.subs(x, t + 2) - fa.subs(x, t)) == 8*t + 8 + 2*b
alt7 = (64 + 4*(-2)) + (64 + 4*(-R(13, 2)))
print('ABLATION 7 구간 [2t-1,2t+1] → [t,t+2]: 필요(이차항 계수가 2가 되어 답', alt7, '로 바뀜)')
for cnt_name, fval in (('개수', lambda lo_, hi2: hi2 - lo_ + 1), ('차', lambda lo_, hi2: hi2 - lo_)):
    print(f'   (참고: 묻는 값을 {cnt_name}로 하면 [2t-1,2t+1]·[t,t+2] 모두', fval(22, 40), fval(64 + 4*(-R(13, 2)), 64 + 4*(-2)), '→ 계수 장치가 일하지 않아 합으로 둠)')
print('ABLATION 7 x=2에서 극소: 필요(빼면 f의 근이 정해지지 않음)')

# ===== 8번 =====
def disc_t(pv, a2=-14):
    """f(t)가 불연속인 t 목록(정확): 후보는 판별식이 0인 t(접선 기울기)뿐, 좌·중·우 근 개수 비교"""
    P = x**3 + a2*x**2 - t*x + pv
    cand = sorted(set(sp.real_roots(sp.Poly(sp.discriminant(P, x), t))))
    def cnt(tv): return len(set(sp.real_roots(sp.Poly(P.subs(t, tv), x))))
    out = []
    for i, t0 in enumerate(cand):
        lt = (cand[i - 1] + t0)/2 if i else t0 - 1
        rt = (t0 + cand[i + 1])/2 if i + 1 < len(cand) else t0 + 1
        if not (cnt(lt) == cnt(t0) == cnt(rt)): out.append(t0)
    return out
D8 = disc_t(-72); assert D8 == [-60, -57, 68]
assert expand(-2*s**3 + 14*s**2 - 72 + 2*(s - 6)*(s - 3)*(s + 2)) == 0
assert sorted(3*v**2 - 28*v for v in (-2, 3, 6)) == [-60, -57, 68]
ans8 = min(D8)
chk(8, ans8, [3*3**2 - 28*3])                                            # 오답 -57: s=3의 기울기
print('ABLATION 8 상수 -72: 필요(-72 → -36이면 접점 방정식 -2s^3+14s^2-36=0의 근', [sp.N(v, 4) for v in sp.Poly(-2*s**3 + 14*s**2 - 36, s).nroots() if abs(sp.im(v)) < 1e-12], '라 기울기 최솟값이', sp.N(min(3*v**2 - 28*v for v in sp.Poly(-2*s**3 + 14*s**2 - 36, s).nroots() if abs(sp.im(v)) < 1e-12), 5), '로 바뀜)')
print('ABLATION 8 실수 t(원문 양의 실수): 필요(양수만이면 불연속점이', [v for v in D8 if v > 0], '뿐이라 최솟값이 바뀜)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [3, 1, 4, 2]
print('ALL OK')
