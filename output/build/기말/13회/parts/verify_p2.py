# -*- coding: utf-8 -*-
# p2.py (13회 5·6·7·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor
x, t, a, b, p, q, c, k = symbols('x t a b p q c k', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 1, 6: 2, 7: 4, 8: 5}                                      # 6·7은 분담표(④·②)와 자리를 맞바꿈(note·보고)
REF = {5: 'I19 후보_순위 2', 6: 'I15 결합 1', 7: 'J36 분석집_변형 1', 8: 'M8 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['I19', 'I15', 'J36', 'M8']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n               # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'
    if n == 7: assert 'STUDY-J36' in it['precedent']
    if n == 8: assert 'STUDY-M8' in it['precedent']
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body', 'precedent'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'bogi' not in it
    if n != 7: assert 'cond' not in it                                 # 상자는 7번(원문 상자)만
    for w in it['wrongs']:
        assert f'{CIRC[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)
    txt = it['body'] + ''.join(v for _, v in it.get('cond', []))
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
    body = it['body'] + ''.join(v for _, v in it.get('cond', []))
    nums = {nsimplify(v) for v in re.findall(r'(?<![\w^{])\d+', body)}  # 정답이 본문에 나온 수와 같지 않음
    assert nsimplify(val) not in nums, (no, val)

# ===== 원문 풀이 =====
# I19: b=-a, 1/2 + a/2 > 5 → a>=10 → |ab|=100
best = min(abs(A*(-A)) for A in range(-60, 61) if integrate(-x + 1, (x, 0, 1)) + integrate(A*x - A, (x, 1, 2)) > 5)
assert best == 100
# I15: g=(x+2)f-f(0)+1, g(0)=3, g'(0)=0, g(1)=8 → f(-1)=3
fI = x**3 + p*x**2 + q*x + c
gI = integrate(diff(fI, x).subs(x, t), (t, 0, x)) + (x + 1)*fI + 1
sI = solve([gI.subs(x, 0) - 3, diff(gI, x).subs(x, 0), gI.subs(x, 1) - 8], [p, q, c], dict=True)
assert len(sI) == 1 and fI.subs(sI[0]).subs(x, -1) == 3
# J36: f=x²+3x-3, f-f'=(x+3)(x-2) → 125/6
fJ = x**2 + 3*x - 3; assert factor(fJ - diff(fJ, x)) == (x - 2)*(x + 3)
assert integrate(diff(fJ, x) - fJ, (x, -3, 2)) == R(125, 6)
# M8: f=(x+2)(x-1)², AC-BD=9a³-9a, a1=-1/√3
fM = (x + 2)*(x - 1)**2; GM = expand(fM.subs(x, a) - fM.subs(x, -2*a)); assert GM == 9*a**3 - 9*a
assert -1/sp.sqrt(3) in solve(diff(GM, a), a)

# ===== 5번 =====
def int5(A, B):
    return integrate(-x + 1, (x, 0, 1)) + integrate(2*A*x + B, (x, 1, 2))
sols = [(A, -2*A) for A in range(-100, 101) if int5(A, -2*A) > 5]       # 연속: 2a+b=0
assert all(-1 + 1 == 2*A + B for A, B in sols)
mn = min(abs(A*B) for A, B in sols); arg = [(A, B) for A, B in sols if abs(A*B) == mn]
assert arg == [(5, -10)] and mn == 50                                  # 최소인 순서쌍 하나
ans5 = arg[0][0] - arg[0][1]
w5 = [(A, -2*A) for A in range(-100, 101) if integrate(2*A*x - 2*A, (x, 1, 2)) > 5]   # 왼쪽 조각 적분 누락
w5 = min(w5, key=lambda s_: abs(s_[0]*s_[1])); w5 = w5[0] - w5[1]
chk(5, ans5, [w5])
s_nc = [(A, B) for A in range(-30, 31) for B in range(-30, 31) if int5(A, B) > 5]
print('ABLATION 5 연속: 필요(빼면 |ab|의 최솟값', min(abs(A*B) for A, B in s_nc), ', 순서쌍 여럿)')
print('ABLATION 5 부등식 ∫>5: 필요(빼면 a=b=0에서 최소 0)')
s_o = min([(A, -A) for A in range(-100, 101) if integrate(-x + 1, (x, 0, 1)) + integrate(A*x - A, (x, 1, 2)) > 5], key=lambda s_: abs(s_[0]*s_[1]))
assert s_o[0] - s_o[1] != ans5
print('ABLATION 5 계수 2a: 일함(원문 ax+b이면 a-b =', s_o[0] - s_o[1], ')')

# ===== 6번 =====
for deg in (1, 2, 3, 4):                                               # 다항함수 f: 차수별 일반형으로 전수
    cs = symbols(f'c0:{deg + 1}', real=True)
    f6 = sum(cs[i]*x**i for i in range(deg + 1))
    g6 = integrate(diff(f6, x).subs(x, t), (t, 0, x)) + (2*x + 1)*f6 + 1
    assert expand(g6 - ((2*x + 2)*f6 - f6.subs(x, 0) + 1)) == 0
    s6 = solve([diff(g6, x).subs(x, 0), diff(f6, x).subs(x, 0) - 4], [cs[0], cs[1]], dict=True)
    assert len(s6) == 1
    assert expand(g6.subs(s6[0]).subs(x, -1)) == 5                      # 나머지 계수와 무관
ans6 = 5
f6e = 4*x - 4; g6e = expand(integrate(diff(f6e, x).subs(x, t), (t, 0, x)) + (2*x + 1)*f6e + 1)
assert g6e == 8*x**2 - 3                                              # 조건을 만족시키는 f가 실제로 있음(x=0에서 극소)
f6c = x**3 + p*x**2 + 4*x - 4; g6c = integrate(diff(f6c, x).subs(x, t), (t, 0, x)) + (2*x + 1)*f6c + 1
assert diff(g6c, x).subs(x, 0) == 0 and diff(g6c, x, 2).subs(x, 0) == 16 + 4*p   # p≠-4이면 극값
w6 = ans6 - 1                                                         # +1 누락
w6b = 1 + 2                                                           # ∫의 도함수 f′ 누락: 2f(0)+f′(0)=0 → f(0)=-2 → 3 (선지 밖)
assert w6b not in [int(c_) for c_ in IT[6]['choices']]
chk(6, ans6, [w6])
print('ABLATION 6 f\'(0)=4: 필요(빼면 g(-1)=1+f\'(0)로 정해지지 않음)')
print('ABLATION 6 x=0에서 극값: 필요(빼면 f(0)이 정해지지 않음)')
g6o = integrate(diff(f6c, x).subs(x, t), (t, 0, x)) + (x + 1)*f6c + 1     # 원문 (x+1): g'(0)=f(0)+2f'(0) → f(0)=-8, 묻는 점은 x=-2
assert sp.simplify(g6o - ((x + 2)*f6c - f6c.subs(x, 0) + 1)) == 0
print('ABLATION 6 계수 2x+1: 일함(원문 (x+1)이면 사라지는 점이 x=-2, g(-1)은 f(-1)에 따라 변함)')

# ===== 7번 =====
f7 = R(1, 2)*x**2 + p*x + q                                           # (가): f′은 최고차항 1인 일차 → f = x²/2 + …
assert sp.limit(diff(f7, x)/x, x, sp.oo) == 1
r1 = solve(f7, x); assert sp.simplify((r1[1] - r1[0])**2 - (4*p**2 - 8*q)) == 0
h7 = f7 - 2*diff(f7, x); r2 = solve(h7, x)
D2 = sp.simplify((r2[1] - r2[0])**2); assert sp.simplify(D2 - (4*p**2 - 8*q + 16)) == 0
area = []
for pv in [0, 1, -2, R(3, 2), 5]:                                     # (나): 4p²-8q=20 인 여러 f에서 넓이가 같음
    qv = solve(4*p**2 - 8*q - 20, q)[0].subs(p, pv)
    hh = h7.subs({p: pv, q: qv}); rr = sorted(solve(hh, x))
    area.append(sp.simplify(integrate(-hh, (x, rr[0], rr[1]))))
assert len(set(area)) == 1
ans7 = area[0]; assert ans7 == 18
w7 = R(1, 2)*6**3/12                                                  # 1/12 공식
w7b = 1*R(6**3, 6); assert w7b == 36 and str(w7b) not in IT[7]['choices']   # 최고차항 계수 1로(선지 밖)
chk(7, ans7, [w7])
print('ABLATION 7 (가): 필요(빼면 최고차항 계수 a가 정해지지 않아 넓이 36|a|)')
print('ABLATION 7 (나): 필요(빼면 넓이가 p, q에 따라 변함)')
hk = f7 - diff(f7, x); rk = solve(hk, x)
print('ABLATION 7 계수 2f′: 일함(y=f′(x)이면 두 근의 차의 제곱', sp.simplify(((rk[1] - rk[0])**2).subs(q, (4*p**2 - 20)/8)), ', 넓이 무리수)')

# ===== 8번 =====
f8 = x**3 - 9*x
tan = diff(f8, x).subs(x, a)*(x - a) + f8.subs(x, a)
assert factor(f8 - tan) == (x - a)**2*(x + 2*a)
bx = -2*a
for av in [R(j, 100) for j in range(1, 150)]:                          # 0<a<3/2: A는 x축 아래, B는 위
    assert f8.subs(x, av) < 0 and f8.subs(x, bx.subs(a, av)) > 0
K = expand(sp.Abs(f8.subs(x, a)).subs(sp.Abs(f8.subs(x, a)), -f8.subs(x, a)) + f8.subs(x, bx))
assert K == -9*a**3 + 27*a
crit = [r for r in solve(diff(K, a), a) if 0 < r < R(3, 2)]; assert crit == [1]
assert diff(K, a, 2).subs(a, 1) < 0
vals = [K.subs(a, R(j, 1000)) for j in range(1, 1500)]; assert max(vals) <= K.subs(a, 1)
ans8 = K.subs(a, 1)
w8 = f8.subs(x, -2)                                                   # BD만
chk(8, ans8, [w8])
print('ABLATION 8 0<a<3/2: 필요(a>3/2이면 B도 x축 아래로 가 합의 식이 바뀌고, 원문 쪽 -3/2<a<0이면 A가 위·B가 아래)')
print('ABLATION 8 최댓값 판정: 필요(구간 끝 a→3/2에서', K.subs(a, R(3, 2)), '< 18, 극대가 최대)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [1, 2, 4, 5]
print('ALL OK')
