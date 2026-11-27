# -*- coding: utf-8 -*-
# 17번 후보 A17 (J38: 이음점 a, 3a의 이차 조각, 닫힌구간 [0, a+2]에서 증가, 직선 x=2까지의 넓이) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a = sp.symbols('x a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def fexp(av, k=1, r=3):
    """연속(f(a)=a, f(ra)=ra)과 최고차항의 계수 -k에서 f(x)=x-k(x-a)(x-ra)"""
    return x - k*(x - av)*(x - r*av)


# 연속 조건에서 f가 하나로 정해짐
p_, q_ = sp.symbols('p q')
fg = -x**2 + p_*x + q_
s = sp.solve([fg.subs(x, a) - a, fg.subs(x, 3*a) - 3*a], [p_, q_], dict=True)[0]
assert sp.expand(fg.subs(s) - fexp(a)) == 0
print('연속 → f(x) = x-(x-a)(x-3a) = -x^2+(4a+1)x-3a^2')


def inc(av, end=lambda t: t + 2, k=1, r=3):
    """g가 [0,end(a)]에서 증가(정확 판정): 겹치는 부분 [a, min(ra,end)]에서 f'≥0 ⇔ 오른쪽 끝 ≤ 극점"""
    e = end(av)
    hi = min(r*av, e)
    if hi <= av:
        return True
    pole = sp.solve(sp.diff(fexp(av, k, r), x), x)[0]
    return hi <= pole


def inc_brute(av, end=lambda t: t + 2):
    f = fexp(av)
    g = lambda t: t if (t < av or t > 3*av) else f.subs(x, t)
    e = end(av); N = 240
    pts = [e*R(j, N) for j in range(N + 1)]
    v = [g(t) for t in pts]
    return all(v[i] < v[i + 1] for i in range(N))


def area(av, L=2, k=1, r=3):
    """그래프와 x축 및 직선 x=L로 둘러싸인 넓이: 조각에서 f≥x>0이므로 삼각형 + (f-x)의 [a, min(ra, L)] 적분"""
    hi = min(r*av, L)
    b = sp.integrate(fexp(av, k, r) - x, (x, av, hi)) if hi > av else 0
    return R(L*L, 2) + b


grid = [R(n, 48) for n in range(1, 48*5 + 1)]          # 0<a≤5, 눈금 1/48
ok = [av for av in grid if inc(av)]
assert ok == [av for av in grid if av <= R(1, 2) or av >= R(3, 2)]
smp = [R(n, 8) for n in range(1, 33)]
assert all(inc(av) == inc_brute(av) for av in smp)
print('증가 조건 ⇔ 0<a≤1/2 또는 a≥3/2 (직접 대입 표본과 일치)')

# 넓이 식
S1 = sp.expand(2 + sp.integrate((x - a)*(3*a - x), (x, a, 3*a)))
S3 = sp.expand(2 + sp.integrate(-x**2 + 4*a*x - 3*a**2, (x, a, 2)))
assert sp.expand(S1 - (2 + R(4, 3)*a**3)) == 0
assert sp.expand(S3 - (R(4, 3)*a**3 - 6*a**2 + 8*a - R(2, 3))) == 0
assert sp.expand(sp.diff(S3, a) - 4*(a - 1)*(a - 2)) == 0
for av in [R(1, 4), R(1, 2)]:
    assert area(av) == S1.subs(a, av)
for av in [R(3, 2), R(7, 4), R(1)]:
    assert area(av) == S3.subs(a, av)
assert all(area(av) == 2 for av in [R(2), R(3), R(5)])
# 조각에서 f≥x>0 (넓이 식의 전제)
assert all(sp.simplify(fexp(av).subs(x, av + (2*av)*R(j, 10)) - (av + 2*av*R(j, 10))) >= 0 for av in smp for j in range(11))
vals = {av: area(av) for av in ok}
mx = max(vals.values()); arg = [av for av in ok if vals[av] == mx]
assert arg == [R(3, 2)] and all(area(av) == 2 for av in ok if av >= 2)
ANS = 6*mx
b1 = 6*max(vals[av] for av in ok if av <= R(1, 2))
print('6S의 최댓값', ANS, '(a =', arg[0], ') · 따로 떨어진 범위 0<a≤1/2의 최댓값', b1)
assert ANS > b1 > 12

# 선지
ch = IT['choices']; vs = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ②, 선지 오름차순 등차', vs[1] - vs[0])

# 오답
w1 = b1                                   # 조각 전체가 증가해야 한다고만 봄
w2 = 6*area(R(1))                         # 조건을 범위로 옮기지 않고 넓이의 극대 a=1
assert w1 == 13 and w2 == 16 and not inc(R(1))
assert sp.diff(S3, a).subs(a, 1) == 0 and sp.diff(S3, a, 2).subs(a, 1) < 0
assert set(IT['wrongs']) == {'13', '16'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 13(a≤1/2만), 16(넓이의 극대 a=1, 조건 밖)')
assert ANS not in {1, 3, 2, 0, 6} and ANS != 28
print('정답은 본문의 수·원문 답 28과 다름')

# 원문 J38
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J38']; assert o[2] == '28'
c = sp.symbols('c')
fo = x + c*(x - 1)*(x - 3)
So = sp.integrate(x, (x, 0, 4)) + sp.integrate(fo - x, (x, 1, 3))
c0 = sp.solve(sp.Eq(So, R(34, 3)), c)[0]
xm = sp.solve(sp.diff(fo.subs(c, c0), x), x)[0]; M = fo.subs({c: c0, x: xm})
assert c0 == R(-5, 2) and xm == R(11, 5) and M == R(23, 5) and M.p + M.q == 28
print('원문 J38 OK: c=-5/2, 최댓값 23/5, 28')
# 원문 원리 줄 불통: 답이 나오는 a에서 '사다리꼴 + 조각 전체 넓이'가 맞지 않음
assert 6*S1.subs(a, arg[0]) != ANS
print('원문 줄 불통: 답이 나오는 a에서 조각 전체 넓이 식은', 6*S1.subs(a, arg[0]), '≠ 답')

# 문장 길이(원문의 90% 이상)
pl = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'])); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9*org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def best(**kw):
    end = kw.get('end', lambda t: t + 2); L = kw.get('L', 2); k = kw.get('k', 1)
    G = [av for av in grid if inc(av, end=end, k=k)]
    return 6*max(area(av, L=L, k=k) for av in G)


ablation('증가 조건 전체', 6*max(area(av) for av in grid))
ablation('구간 끝 a+2(→a+1)', best(end=lambda t: t + 1))
ablation('구간 끝 a+2(→a+3)', best(end=lambda t: t + 3))
ablation('구간 끝 a+2(→2, 고정)', best(end=lambda t: sp.Integer(2)))
ablation('직선 x=2(→x=3)', best(L=3))
ablation('최고차항의 계수 -1(→-2)', best(k=2))
# 연속을 빼면 f의 일차항·상수항이 자유: a=3/2에서 f=-x^2+8x+q (극점 4 ≥ 7/2라 증가)로 두면 넓이가 q에 따라 달라짐
qq = sp.symbols('qq')
A_q = sp.integrate(x, (x, 0, R(3, 2))) + sp.integrate(-x**2 + 8*x + qq, (x, R(3, 2), 2))
assert sp.diff(A_q, qq) != 0
ablation('연속', '정해지지 않음(a=3/2, f=-x^2+8x+q이면 넓이가 q에 따라 달라짐)')
print('ALL OK')
