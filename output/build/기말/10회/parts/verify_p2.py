# -*- coding: utf-8 -*-
# p2.py (10회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor, oo, limit
x, t, a, b, c, k, C, g = symbols('x t a b c k C g', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 4, 6: 2, 7: 3, 8: 1}                                       # 분담표 목표 정답
REF = {5: 'J7 분석집_변형 1', 6: 'I8 후보_순위 1', 7: 'I38 후보_순위 2', 8: 'I13 후보_순위 2'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['J7', 'I8', 'I38', 'I13']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'       # 분담표 목표 수준
    if n == 5: assert 'STUDY-J7' in it['precedent']                    # 분석집 변형 id
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
    nums = {nsimplify(v) for v in re.findall(r'(?<![\w^{])\d+', it['body'])}   # 정답이 본문에 나온 수와 같지 않음
    assert nsimplify(val) not in nums, (no, val)

# ===== 원문·분석집 변형 풀이 =====
# J7: f'=3x^2-2x+a, f(0)=1, f'(0)=-1 → f=(x-1)^2(x+1), 30S=40
fJ = integrate(3*x**2 - 2*x - 1, x) + 1
assert factor(fJ) == (x - 1)**2*(x + 1) and 30*integrate(fJ, (x, -1, 1)) == 40
# STUDY-J7-변형①: f'=3x^2-6x+a, f(2)=3, f'(2)=-2 → 접선 y=-2x+7, 4S=27
aV = solve(3*4 - 12 + a + 2, a)[0]; fV = x**3 - 3*x**2 + aV*x; fV = fV + 3 - fV.subs(x, 2)
assert factor(fV - (-2*x + 7)) == (x - 2)**2*(x + 1) and 4*integrate(fV - (-2*x + 7), (x, -1, 2)) == 27
# I8: 극솟값 f(2)=3, f(-2)=-1 → 합 2
def build8(outer, inner, y0, e=1):
    Fi = integrate(inner, x) + y0
    Fr = integrate(outer, x); Fr = Fr - Fr.subs(x, e) + Fi.subs(x, e)
    Fl = integrate(outer, x); Fl = Fl - Fl.subs(x, -e) + Fi.subs(x, -e)
    return Fl, Fi, Fr
Fl, Fi, Fr = build8(x**3 - 4*x, 2*x + 2, R(9, 4))
assert Fr.subs(x, 2) + Fl.subs(x, -2) == 2
# I38: c=-1, b∈[-2/3,10/3], ∫_{-1}^2 f=3b/2 → 합 4
assert R(3, 2)*(-R(2, 3)) + R(3, 2)*R(10, 3) == 4
# I13: a=1, b=-2, f=4x(x+1) → 최솟값 -1
sI = solve([a + b + 1, 4*a + 2*b], [a, b]); assert sI == {a: 1, b: -2}
assert sp.cancel((4*x**3 - 4*x)/(x - 1)) == 4*x**2 + 4*x and sp.minimum(4*x**2 + 4*x, x) == -1
print('원문·분석집 변형 풀이 OK')

# ===== 5번 =====
f5g = x**3 - 4*x**2 + a*x + C                                           # f'=3x^2-8x+a
assert diff(f5g, x) == 3*x**2 - 8*x + a
# 극한 조건: 분자→0, 극한값 = 2f'(2)
s5 = solve([f5g.subs(x, 2) - 1, 2*diff(f5g, x).subs(x, 2) + 2], [a, C], dict=True); assert s5 == [{a: 3, C: 3}]
f5 = f5g.subs(s5[0])
assert limit((f5.subs(x, 2*x) - 1)/(x - 1), x, 1) == -2                # 조건 재확인
L5 = -x + 3
assert factor(f5 - L5) == x*(x - 2)**2
assert sp.real_roots(sp.Poly(f5 - L5, x)) == [0, 2, 2]
S5 = integrate(sp.Abs(f5 - L5), (x, 0, 2)); assert S5 == R(4, 3)
ans5 = 3*S5
chk(5, ans5, [3*R(2**4, 6)])                                           # 1/12 → 1/6
def area(F):
    rs = sorted(set(v for v in sp.Poly(F, x).nroots(n=30) if abs(sp.im(v)) < 1e-20))
    rs = [sp.re(v) for v in rs]
    return sum(abs(integrate(F, (x, rs[i], rs[i + 1]))) for i in range(len(rs) - 1))
print('ABLATION 5 극한 조건: 필요(빼면 a, C가 정해지지 않음; 예 a=3, C=2이면 넓이', sp.N(area(f5g.subs({a: 3, C: 2}) - L5), 6), ')')
fw = f5g.subs({a: 2}).subs(C, solve(f5g.subs({a: 2}).subs(x, 2) - 1, C)[0])  # 인자 2를 놓쳐 f'(2)=-2
print('ABLATION 5 인자 2x → x(극한 lim(f(x)-1)/(x-1)=-2 꼴): 필요(f\'(2)=-2가 되어 직선이 접선이 아님, f-(−x+3) =', factor(fw - L5), ')')
f5b = x**3 + g*x**2 + a*x + C                                           # 이차항 계수 미정
print('ABLATION 5 도함수 식 f\'(x)=3x^2-8x+a: 필요(이차항 계수가 없으면 다른 교점 γ가 정해지지 않음:',
      [factor((f5b - L5).subs(sp.solve([f5b.subs(x, 2) - 1, diff(f5b, x).subs(x, 2) + 1], [a, C], dict=True)[0]).subs(g, gv)) for gv in (-4, -3)], ')')

# ===== 6번 =====
Fl, Fi, Fr = build8(x**3 - 9*x, 2*x + 2, k)
# 연속 확인
assert Fl.subs(x, -1) == Fi.subs(x, -1) and Fr.subs(x, 1) == Fi.subs(x, 1)
# 부호 변화로 극값 판정(전수: 정류점 + 경계)
fp = lambda v: (v**3 - 9*v) if abs(v) > 1 else (2*v + 2)
cands = [-3, -1, 0, 1, 3]
kinds = {}
for v in cands:
    e = R(1, 100); l, r_ = fp(v - e), fp(v + e)
    kinds[v] = 'min' if (l < 0 < r_) else ('max' if (l > 0 > r_) else 'none')
assert kinds == {-3: 'min', -1: 'none', 0: 'none', 1: 'max', 3: 'min'}
fpw = sp.Piecewise((Fl, x <= -1), (Fi, x <= 1), (Fr, True))
mins = [Fl.subs(x, -3), Fr.subs(x, 3)]
assert sp.simplify(mins[0] - (k - 17)) == 0 and sp.simplify(mins[1] - (k - 13)) == 0
# 최솟값 = 두 극솟값 중 작은 값(양끝 → ∞), 격자 확인
grid = [R(i, 10) for i in range(-80, 81)]
assert min(fpw.subs(k, 0).subs(x, v) for v in grid) == -17
ks = solve(mins[0] + 2, k); assert ks == [15]
ans6 = ks[0]
chk(6, ans6, [solve(mins[1] + 2, k)[0]])
print('ABLATION 6 최솟값 -2: 필요(빼면 k가 정해지지 않음)')
print('ABLATION 6 연속 조건: 필요(바깥 적분상수도 k로 두면 f(-3)=', sp.simplify(integrate(x**3 - 9*x, x).subs(x, -3) + k), '라 k =', solve(integrate(x**3 - 9*x, x).subs(x, -3) + k + 2, k)[0], ')')
Fl2, Fi2, Fr2 = build8(x**3 - 9*x, 2*x - 2, k)
print('ABLATION 6 가운데 조각 2x+2 → 2x-2: 필요(극솟값 f(-3)=', sp.simplify(Fl2.subs(x, -3)), ', f(3)=', sp.simplify(Fr2.subs(x, 3)), '로 최소 위치가 바뀜)')

# ===== 7번 =====
f7 = x**2 + b*x + c
cs = solve(f7.subs(x, 1) + f7.subs(x, -1) - R(4, 3), c); assert cs == [-R(1, 3)]
S7 = integrate(f7, (x, 0, 1)).subs(c, cs[0]); assert sp.simplify(S7 - b/2) == 0
T7 = integrate(f7.subs(x, 2*x), (x, 0, 1)).subs(c, cs[0]); assert sp.simplify(T7 - (b + 1)) == 0
brange = sp.Interval(0, 4)
assert all((0 <= S7.subs(b, v) <= 2) == (v in brange) for v in [R(i, 4) for i in range(-16, 33)])
mx7, mn7 = T7.subs(b, 4), T7.subs(b, 0); assert (mx7, mn7) == (5, 1)
ans7 = mx7 + mn7
w7a = 0 + 2                                                           # ∫f(2x)=∫f로 봄
I_orig = integrate(f7, (x, -1, 2)).subs(c, cs[0]); w7b = I_orig.subs(b, 4) + I_orig.subs(b, 0)
chk(7, ans7, [w7a, w7b])
# 일반 c에서 T = 2S - c + 2/3 → (가) 필요
assert sp.simplify(integrate(f7.subs(x, 2*x), (x, 0, 1)) - (2*integrate(f7, (x, 0, 1)) - c + R(2, 3))) == 0
print('ABLATION 7 f(1)+f(-1)=4/3: 필요(c가 정해지지 않아 합 = 16/3 - 2c 로 변함)')
print('ABLATION 7 0≤∫f≤2: 필요(빼면 b 범위가 없어 최댓값·최솟값 없음)')
print('ABLATION 7 f(2x) → f(x): 필요(합', 2, '로 바뀜, 이때 (가)는 군더더기)')

# ===== 8번 =====
f8 = sp.Function('f')
# x=1 대입, 미분 후 x=2 대입
s8 = solve([a + b + 7, 32*a + 4*b], [a, b]); assert s8 == {a: 1, b: -8}
q8, r8 = sp.div(sp.Poly(4*x**3 - 16*x, x), sp.Poly(x - 2, x)); assert r8.is_zero
F8 = q8.as_expr(); assert expand(F8) == 4*x**2 + 8*x
# 항등식 검산
assert expand(integrate((t - 2)*F8.subs(x, t), (t, 1, x)) - (x**4 - 8*x**2 + 7)) == 0
# 유일성: f가 다항함수이려면 (x-2) | 4ax^3+2bx ⇔ 32a+4b=0, 아래끝 조건과 연립하면 해 하나
assert len(solve([a + b + 7, 32*a + 4*b], [a, b], dict=True)) == 1
ans8 = sp.minimum(F8, x); assert ans8 == -4
w8a = sp.minimum(sp.cancel((x*(2*x**2 - 8))/(x - 2)), x)              # 앞의 2 누락
w8b = solve(diff(F8, x), x)[0]                                          # 최소점
chk(8, ans8, [w8a, w8b])
print('ABLATION 8 상수항 7: 필요(7 → 1이면 a = 1/7, 최솟값', sp.minimum(sp.cancel(R(4, 7)*x*(x**2 - 4)/(x - 2)), x), ')')
print('ABLATION 8 인수 (t-2): 필요((t-1)이면 아래끝과 같은 점이라 a+b+7=0, 4a+2b=0 → a=7, 최솟값', sp.minimum(sp.cancel((28*x**3 - 28*x)/(x - 1)), x), ')')
print('ABLATION 8 아래끝 1: 필요(빼면 a+b+7=0이 없어 a가 정해지지 않음)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [4, 2, 3, 1]
print('ALL OK')
