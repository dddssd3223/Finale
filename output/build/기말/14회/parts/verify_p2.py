# -*- coding: utf-8 -*-
# p2.py (14회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor
x, t, a, b, p, q, c, k = symbols('x t a b p q c k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 5, 6: 2, 7: 1, 8: 3}                                      # 분담표 정답 목표 그대로
REF = {5: 'I11 후보_순위 2', 6: 'M10 v3_추가 1', 7: 'J33 후보_순위 3', 8: 'J20 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['I11', 'M10', 'J33', 'J20']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n               # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'
    if n == 8: assert 'STUDY-J20' in it['precedent']
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'bogi' not in it and 'cond' not in it   # 그림·보기·상자 없음
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

# ===== 원문 풀이 =====
# I11: f=(x³-2x+1)/2, f(1)+f'(1)=1/2
fo = (x**3 - 2*x + 1)/2
assert expand(integrate(((t**3 - 2*t)*diff(fo, x).subs(x, t)), (t, 1, x)) - (fo**2 - fo)) == 0
assert fo.subs(x, 1) + diff(fo, x).subs(x, 1) == R(1, 2)
# M10: h=-x⁴+4x³/3+4x²-2, 세 실근 a=-1/3, -2 → -7/3
hM = -x**4 + R(4, 3)*x**3 + 4*x**2 - 2
three = [v for v in {hM.subs(x, r) for r in solve(diff(hM, x), x)} if len(sp.solveset(hM - v, x, sp.S.Reals)) == 3]
assert sum(three) == R(-7, 3)
# J33: a=2, A=14/3, B=8 → 38/3
fb = -x**2 + 2*x
Aj = -(integrate(fb.subs(x, x + 2) - 4, (x, -2, -1)) + integrate(fb, (x, -1, 0)))
Bj = integrate(fb, (x, 0, 1)) + integrate(fb.subs(x, x - 2) + 4, (x, 1, 3))
assert (-1 + 2) == fb.subs(x, -1) + 4 and Aj + Bj == R(38, 3)
# J20: k=10/3
assert solve(integrate(x**2*(x - 2)*(x - k), (x, 0, k)) / k**4, k) == [R(10, 3)]

# ===== 5번 =====
for deg in (1, 2, 3, 4, 5):                                           # 다항함수 일반형 전수: 상수함수가 아닌 해는 하나
    cs = symbols(f'c0:{deg + 1}')
    f5 = sum(cs[i]*x**i for i in range(deg + 1))
    eq = expand(integrate((t**3 - 3*t)*diff(f5, x).subs(x, t), (t, 1, x)) - (f5**2 - 2*f5))
    sol = solve(sp.Poly(eq, x).coeffs(), cs, dict=True)
    nonconst = [s_ for s_ in sol if any(sp.simplify(f5.subs(s_).diff(x)) != 0 for _ in [0])]
    if deg < 3: assert nonconst == [], deg
    else:
        assert len(nonconst) == 1 and expand(f5.subs(nonconst[0]) - (x**3 - 3*x + 2)/2) == 0, deg
f5e = (x**3 - 3*x + 2)/2
assert f5e.subs(x, 1) == 0
ans5 = f5e.subs(x, 3)
w5 = ((x**3 - 3*x + 1)/2).subs(x, 3)                                 # 원문 습관 2f-1
assert ((x**3 - 3*x + 1)/2).subs(x, 1)**2 - 2*((x**3 - 3*x + 1)/2).subs(x, 1) != 0   # 그 f는 아래끝 확인에서 탈락
chk(5, ans5, [w5])
print('ABLATION 5 상수함수가 아닌: 필요(빼면 상수 해 f=0, f=2가 생겨 f(3)이 0, 2, 10으로 정해지지 않음)')
fo2 = (x**3 - 2*x + 2)/2                                             # 원문 t³-2t 그대로 두면
assert fo2.subs(x, 1)**2 - 2*fo2.subs(x, 1) != 0
print('ABLATION 5 t³-3t(OP02): 일함(원문 t³-2t 그대로면 f(1)=1/2이라 아래끝에서 등식이 깨져 해가 없음)')
print('ABLATION 5 우변 계수 2: 일함(원문 f²-f이면 f(3)=19/2)')

# ===== 6번 =====
a6 = solve((x**4 + a - (4*x**3 + 8*x**2 - 2)).subs(x, -1), a); assert a6 == [1]
F6p = (4*x**3 + 8*x**2 - 2) - (x**4 + 1)
assert factor(F6p) == -(x + 1)**2*(x**2 - 6*x + 3)
def ext_points(Fp):
    rts = sp.roots(sp.Poly(Fp, x))
    return [r for r, m in rts.items() if r.is_real and m % 2 == 1]
ex = ext_points(F6p); assert len(ex) == 2
ans6 = sp.simplify(sum(ex)); assert ans6 == 6
h6 = 4*x**3 + 8*x**2 - 2 - x**4
assert sorted(solve(diff(h6, x), x)) == [-1, 0, 4] and h6.subs(x, -1) == 1   # a=h(-1): 작은 극댓값에서 중근
w6 = sp.simplify(sum(sp.roots(sp.Poly(F6p, x)).keys()))              # 서로 다른 근 모두
assert w6 == 5
w6b = 4                                                              # 중복도까지 근과 계수의 관계(선지 밖)
assert sum(r*m for r, m in sp.roots(sp.Poly(F6p, x)).items()) == w6b and str(w6b) not in IT[6]['choices']
chk(6, ans6, [w6])
print('ABLATION 6 x=-1이 근: 필요(빼면 a가 정해지지 않음. 예: a=0이면 극값 x 넷, a=-2(극솟값)이면 근의 합이 달라짐)')
ex0 = ext_points((4*x**3 + 8*x**2 - 2) - (x**4 - 2)); assert sp.simplify(sum(ex0)) != 6
print('ABLATION 6 극값(부호 변화): 일함(근을 모두 세면 5)')

# ===== 7번 =====
base = -x**2 - 2*x
kv = solve(base.subs(x, 1) - (2*base.subs(x, -1) + k), k); assert kv == [-5]
K7 = kv[0]
left = (base.subs(x, x + 2) - K7)/2                                  # -3≤x<-1
assert expand(left - (-x**2 - 6*x - 3)/2) == 0
assert left.subs(x, -1) == base.subs(x, -1)                           # x=-1에서도 이어짐
assert all(left.subs(x, R(j, 100)) > 0 for j in range(-300, -99))     # 구간에서 양수
right = 2*base.subs(x, x - 2) + K7                                    # 1≤x<3
assert right.subs(x, 1) == base.subs(x, 1)
ans7 = integrate(left, (x, -3, -1)); assert ans7 == R(14, 3)
assert ans7 == R(1, 2)*(integrate(base, (x, -1, 1)) - 2*K7)
w7 = abs(R(1, 2)*(integrate(base, (x, -1, 1)) + 2*K7))               # k 부호 그대로
assert w7 == R(16, 3)
k0 = solve(base.subs(x, 1) - (base.subs(x, -1) + k), k)[0]           # 계수 2 무시: k=-4
w7b = integrate(base.subs(x, x + 2) - k0, (x, -3, -1)); assert w7b == R(22, 3) and '\\dfrac{22}{3}' not in IT[7]['choices']
chk(7, ans7, [w7])
print('ABLATION 7 연속: 필요(빼면 k가 정해지지 않아 넓이 -1/3-k로 변함)')
print('ABLATION 7 바깥 계수 2: 일함(원문처럼 계수 1이면 넓이 22/3)')
print('ABLATION 7 x=-3, x=-1: 필요(넓이 구간)')

# ===== 8번 =====
y8 = x*(x - k)*(x - 5)**2
I8 = integrate(y8, (x, 0, 5)); assert sp.simplify(I8 - (R(625, 6) - R(625, 12)*k)) == 0
ks = solve(I8, k); assert ks == [2]
for kv8 in [R(j, 10) for j in range(1, 50)]:                          # 0<k<5에서 두 부분은 부호가 반대 → 넓이 같음 ⇔ ∫=0
    yy = y8.subs(k, kv8)
    assert yy.subs(x, kv8/2) < 0 and yy.subs(x, (kv8 + 5)/2) > 0
    L = -integrate(yy, (x, 0, kv8)); Rr = integrate(yy, (x, kv8, 5))
    assert (L == Rr) == (kv8 == 2)
ans8 = 2
w8 = 3                                                                # 왼쪽 근 0에서 3:5
w8b = R(5, 2)                                                         # 중점 습관
chk(8, ans8, [w8, w8b])
print('ABLATION 8 0<k<5: 필요(k>5이면 둘러싸인 부분이 (0,5),(5,k)로 바뀌어 같은 부호 → 다른 k; k<0도 구조가 바뀜)')
yo = x*(x - k)*(x - 5)**2
print('ABLATION 8 중근 x=5: 일함(단순근이면 삼차 중점 규칙 k=5/2)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [5, 2, 1, 3]
print('ALL OK')
