# -*- coding: utf-8 -*-
# p2.py (11회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational as R, diff, integrate, solve, expand, nsimplify, factor, Abs
x, t, a, b, c, k, C = symbols('x t a b c k C', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 2, 6: 5, 7: 3, 8: 1}                                       # 분담표 목표 정답
REF = {5: 'J4 분석집_변형 1', 6: 'I5 후보_순위 4', 7: 'I35 결합 1', 8: 'D23 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OPS = {f'OP{i:02d}' for i in range(1, 56)}
CIRC = '①②③④⑤'
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['J4', 'I5', 'I35', 'D23']
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐')
    assert it['ops'] and all(o in OPS for o in it['ops'])
    if n in (5, 6, 7): assert COEF & set(it['ops']), n                # 계수 ● 자리
    assert '함정 추가' not in it['vtype'] and it['level'] == '중'
    if n == 5: assert 'STUDY-J4' in it['precedent']
    if n == 8: assert 'STUDY-D23' in it['precedent']
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
# J4: 2∫_{-2}^0 x(x+2)(x-k) = 8(k+1)/3 = 6 → k = 5/4
assert solve(2*integrate(x*(x + 2)*(x - k), (x, -2, 0)) - 6, k) == [R(5, 4)]
# STUDY-J4-변형①: k>0 → 2, k<-2 → -4 (8이 되는 k), -2<k<0 → 넓이 < 8/3
A_pos = 2*integrate(x*(x + 2)*(x - k), (x, -2, 0)); A_neg = 2*integrate(x*(x + 2)*(x - k), (x, k, -2))
assert solve(A_pos - 8, k) == [2] and A_neg.subs(k, -4) == 8
# I5: f = 3x^4-5x^3+C, G(1)=C-1=4 → f(2)=13
fI = 3*x**4 - 5*x**3 + C; GI = x**2*fI - 2*x**6 + 3*x**5
assert expand(diff(GI, x) - 2*x*fI) == 0 and fI.subs(C, solve(GI.subs(x, 1) - 4, C)[0]).subs(x, 2) == 13
# I35: k = 4+8k-2k^2 → 4, -1/2; 증가 → k=4, f(2)=24
ks = solve(integrate(x**3 + 4*k*x - k**2, (x, 0, 2)) - k, k); assert set(ks) == {4, R(-1, 2)}
assert (x**3 + 16*x - 16).subs(x, 2) == 24
# D23: a=-15, b=24 → 29+2 = 31
fD = 2*x**3 - 15*x**2 + 24*x + 18
assert factor(fD - (2*x + 3)) == (x - 5)*(x - 3)*(2*x + 1) and fD.subs(x, 1) + fD.subs(x, 4) == 31
# STUDY-D23-변형①: f-g=(2x+7)(x+2)(x+1), 극소점 -7/2, -1 → -9/2
fS = expand((2*x + 7)*(x + 2)*(x + 1) + (-x + 4)); assert diff(fS, x).subs(x, -3) == 0

# ===== 5번 =====
f5 = -k*x*(x + 1)*(x - 2)
def area5(kv, n=4001):                                                  # 수치로 g=f+|f| 의 유계 영역 넓이: [-1, 2] 밖에서는 둘러싸인 부분 없음
    g = sp.lambdify(x, f5.subs(k, kv) + Abs(f5.subs(k, kv)))
    xs = [-1 + 3*i/(n - 1) for i in range(n)]; h = 3/(n - 1)
    return sum((g(xs[i]) + g(xs[i + 1]))/2*h for i in range(n - 1))
A5 = 2*integrate(f5, (x, 0, 2)); assert A5 == R(16, 3)*k
assert integrate(f5.subs(k, 1), (x, -1, 0)) < 0 and integrate(f5.subs(k, 1), (x, 0, 2)) > 0   # (-1,0)에서 f<0
s5 = solve(A5 - 16, k); assert s5 == [3] and abs(area5(3) - 16) < 1e-3
w5 = solve(A5/2 - 16, k)[0]                                            # 계수 2 누락
chk(5, s5[0], [w5])
print('ABLATION 5 부호 -k: 필요(+k이면 구간 [-1, 0], 넓이 5k/6=16 → k =', solve(R(5, 6)*k - 16, k)[0], ', 선지에 없음)')
print('ABLATION 5 양수 k: 필요(빼면 k<0일 때 구간이 [-1,0]으로 바뀌어 k = -96/5 도 됨)')
print('ABLATION 5 넓이 16: 필요(빼면 k가 정해지지 않음)')

# ===== 6번 =====
fx = sp.Function('f')
P6 = a*x**7 - 7*x**6
# x^3 f' = -P'  → f' = -P'/x^3
fp6 = sp.cancel(-diff(P6, x)/x**3); assert expand(fp6 - 7*x**2*(6 - a*x)) == 0
sa = solve(fp6.subs(x, 1), a); assert sa == [6]                         # 유일
fp6 = fp6.subs(a, 6); f6 = integrate(fp6, x) + C
G6 = x**3*f6 + 6*x**7 - 7*x**6
assert expand(diff(G6, x) - 3*x**2*f6) == 0
Cv = solve(G6.subs(x, 1) - 3, C)[0]; F6 = f6.subs(C, Cv)
crit = solve(diff(F6, x), x); assert set(crit) == {0, 1}
assert fp6.subs(x, R(-1, 2)) > 0 and fp6.subs(x, R(1, 2)) > 0 and fp6.subs(x, 2) < 0   # x=0 극값 아님, x=1 최대
assert sp.Poly(F6, x).LC() < 0
ans6 = F6.subs(x, 1)
w6a = 3                                                                 # G(1)=f(1)로
w6b = 3 - 1                                                             # a-7=-1 부호 반대
chk(6, ans6, [w6a, w6b])
fa = integrate(7*x**2*(6 - a*x), x); Ca = solve((x**3*(fa + C) + a*x**7 - 7*x**6).subs(x, 1) - 3, C)[0]
mx = [sp.simplify((fa + Ca).subs(x, 6/av).subs(a, av)) for av in (3, 6, 12)]
print('ABLATION 6 x=1에서 극값: 필요(빼면 a=3, 6, 12일 때 최댓값', mx, ')'); assert len(set(mx)) == 3
print('ABLATION 6 G(1)=3: 필요(빼면 적분상수가 정해지지 않음)')

# ===== 7번 =====
f7 = x**3 - 3*k*x + c + 5
s7 = solve([integrate(f7, (x, -1, 1)) - k, f7.subs(x, 1) - c], [k, c], dict=True)
assert len(s7) == 1 and s7[0] == {k: 2, c: -4}                         # 해 하나
F7 = f7.subs(s7[0]); assert expand(F7) == x**3 - 6*x + 1
assert expand(F7 - (x**3 - 3*x*integrate(F7, (x, -1, 1)) + F7.subs(x, 1) + 5)) == 0
ans7 = F7.subs(x, 3)
s7w = solve([(c + 5) - k, f7.subs(x, 1) - c], [k, c], dict=True)[0]   # ∫(c+5)에서 2 누락
w7 = f7.subs(s7w).subs(x, 3)
chk(7, ans7, [w7])
g7 = x**3 - 3*k*x + c; s7b = solve([integrate(g7, (x, -1, 1)) - k, g7.subs(x, 1) - c], [k, c], dict=True)[0]
print('ABLATION 7 상수 5: 필요(빼면', s7b, ', f(3) =', g7.subs(s7b).subs(x, 3), ')')
print('ABLATION 7 f(1) 항: 필요(빼면 k = 2*5 = 10, f(3) =', (x**3 - 30*x + 5).subs(x, 3), ')')
print('ABLATION 7 대칭 구간 [-1,1]: 필요([0,2]이면 k, c 연립이', solve([integrate(f7, (x, 0, 2)) - k, f7.subs(x, 1) - c], [k, c]), ')')

# ===== 8번 =====
F8 = 2*x**3 - 2*x**2 - 10*x + 11; g8 = -2*x + 3
assert expand(F8 - g8 - 2*(x - 2)*(x - 1)*(x + 2)) == 0
assert diff(F8, x).subs(x, -2) > 0 and diff(F8, x).subs(x, 2) > 0 and diff(F8, x).subs(x, 1) < -2   # 바깥 교점 극소, 가운데 아님
assert set(solve(diff(F8, x), x)) == {-1, R(5, 3)} and F8.subs(x, R(5, 3)) < g8.subs(x, R(5, 3))   # f의 극소점은 g 아래
hfun = sp.lambdify(x, sp.Max(F8, g8)); N = 60001; xs = [-6 + 12*i/(N - 1) for i in range(N)]; hv = [hfun(v) for v in xs]
mins = [(round(xs[i], 3), round(hv[i], 4)) for i in range(1, N - 1) if hv[i] < hv[i - 1] and hv[i] < hv[i + 1]]
maxs = [(round(xs[i], 3), round(hv[i], 4)) for i in range(1, N - 1) if hv[i] > hv[i - 1] and hv[i] > hv[i + 1]]
print('8번 h 극소', mins, '극대', maxs)
assert [m[0] for m in mins] == [-2.0, 2.0] and [m[0] for m in maxs] == [-1.0] and abs(maxs[0][1] - 17) < 1e-6
ans8 = g8.subs(x, -2) + g8.subs(x, 2)
w8 = g8.subs(x, -2) + g8.subs(x, 1) + g8.subs(x, 2)                    # 가운데 교점도 극소로
assert w8 == g8.subs(x, -2)                                              # 왼쪽 교점만 본 값과 같음
chk(8, ans8, [w8])
print('ABLATION 8 g 기울기 -2: 필요(원문처럼 +2이면 f-g 의 근이 바뀌고 가운데 교점이 극소 후보, 답 달라짐)')

assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [2, 5, 3, 1]
print('ALL OK')
