# -*- coding: utf-8 -*-
# 17번 후보 A17 (J42: 삼차 조각과 직선 조각 k(x-3)을 이은 함수, 부등식 조건의 구간 끝 3a) 검증 · author='claude'
import sympy as sp, os, sys, re
x, a = sp.symbols('x a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
p = x**3 - 2*x**2


def kval(av, d=3):
    """연속 조건 k(a-d)=p(a). a=d이면 p(d)≠0이라 연속일 수 없다(None)."""
    if av == d:
        return None
    return p.subs(x, av) / (av - d)


def cond(av, end=lambda t: 3*t, d=3):
    """x≤end(a)인 모든 실수 x에서 f(x)≤0 (정확 판정). 삼차 조각: x<min(a,end)에서 x^2(x-2)≤0 ⇔ 그 끝 ≤2. 직선 조각: [a,end]의 두 끝값."""
    k = kval(av, d)
    if k is None:
        return False
    e = end(av)
    if min(av, e) > 2:
        return False
    if e < av:
        return True
    return p.subs(x, av) <= 0 and k*(e - d) <= 0


def area(av, d=3):
    """그래프와 x축으로 둘러싸인 부분의 넓이(없으면 None). 영점: 삼차 조각 0·2(x<a), 직선 조각 d(x≥a, k≠0)."""
    k = kval(av, d)
    if k is None:
        return None
    Z = [t for t in (0, 2) if t < av]
    if k == 0:
        Z.append(av)                      # x≥a에서 f=0: 영역은 a에서 닫힘
    elif d >= av:
        Z.append(d)
    Z = sorted(set(Z))
    if len(Z) < 2:
        return None
    lo, hi = Z[0], Z[-1]
    s = 0
    for u, v in zip(Z[:-1], Z[1:]):
        if v <= av:
            s += sp.Abs(sp.integrate(p, (x, u, v)))
        else:
            s += sp.Abs(sp.integrate(p, (x, u, av))) if u < av else 0
            s += sp.Abs(sp.integrate(k*(x - d), (x, max(u, av), v)))
    return sp.nsimplify(s)


# ---------- 1) 조건을 만족시키는 a (정확 전수: 눈금 1/32, 0<a≤8)
grid = [R(n, 32) for n in range(1, 257)]
ok = [av for av in grid if cond(av)]
assert ok == [av for av in grid if av <= 1 or av == 2], ok[-5:]
# 표본으로 다시 확인(직접 대입)
def brute(av, d=3):
    k = kval(av, d)
    if k is None: return False
    f = lambda t: p.subs(x, t) if t < av else k*(t - d)
    return all(f(3*av - R(j, 64)) <= 0 for j in range(0, 64*12))
assert all(brute(av) == cond(av) for av in [R(n, 8) for n in range(1, 41)])
print('조건 ⇔ 0<a≤1 또는 a=2 (a>2: 삼차 조각이 양수, 1<a<2: 직선 조각이 3a 전에 양수, a=2: k=0)')
assert all(kval(av) > 0 for av in ok if av < 2) and kval(R(2)) == 0 and kval(R(1)) == R(1, 2)

# ---------- 2) 넓이 식과 최댓값
Sa = sp.expand(sp.integrate(-p, (x, 0, a)) + R(1, 2)*(3 - a)*a**2*(2 - a))
assert sp.expand(Sa - (a**4/4 - R(11, 6)*a**3 + 3*a**2)) == 0
for av in [R(1, 4), R(1, 2), R(3, 4), R(1), R(3, 2), R(7, 4)]:
    assert area(av) == Sa.subs(a, av), av
dS = sp.expand(sp.diff(Sa, a))
assert sp.factor(dS) == sp.factor(a*(2*a - 3)*(a - 4)/2)
assert all(dS.subs(a, t) > 0 for t in [R(n, 64) for n in range(1, 96)])       # 0<a<3/2에서 증가
assert area(R(2)) == R(4, 3)
vals = {av: area(av) for av in ok}
mx = max(vals.values()); arg = [av for av in ok if vals[av] == mx]
assert mx == R(17, 12) and arg == [1]
ANS = 12*mx
assert ANS == 17 and R(17, 12) > R(4, 3)
print('S = a^4/4 - 11a^3/6 + 3a^2 (0<a<2), 0<a≤1에서 증가 → a=1에서 17/12, a=2에서 4/3 → 12S의 최댓값', ANS)

# ---------- 3) 선지
ch = IT['choices']; vs = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 3
assert len(set(vs)) == 5 and len({vs[i + 1] - vs[i] for i in range(4)}) == 1 and vs == sorted(vs)
print('정답 = 선지 ③, 선지 오름차순 등차', vs[1] - vs[0])

# ---------- 4) 오답
w1 = 12*area(R(2))                                                            # a=2만(또는 원문처럼 4/3 고정)
w2 = 12*(sp.integrate(-p, (x, 0, 2)) + sp.integrate(-R(1, 2)*(x - 3), (x, 2, 3)))   # 조각 경계 무시: 삼차식을 2까지 + 직선은 [2,3]만
assert w1 == 16 and w2 == 19
assert set(IT['wrongs']) == {'16', '19'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 16(a=2만·넓이 4/3 고정), 19(조각 경계 무시 4/3+1/4)')
assert ANS not in {2, 3, 12} and R(ANS) != R(15, 2)
print('정답은 본문의 수·원문 답 15/2와 다름')

# ---------- 5) 원문 J42: 15/2
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J42']; assert o[2] == '⑤' and o[1][4] == r'\dfrac{15}2'
k0 = a**3 - R(5, 2)*a**2
S2o = sp.integrate(-p, (x, 0, 2)); S1o = sp.integrate(x**2/2 + k0, (x, a, a + 1))
sol = [t for t in sp.solve(sp.Eq(S1o, 8*S2o), a) if t.is_real and k0.subs(a, t) > 0]
assert S2o == R(4, 3) and sol == [3] and sol[0] + k0.subs(a, 3) == R(15, 2)
print('원문 J42 OK: a=3, k=9/2, a+k=15/2')
# 원문 원리 줄 불통: 답이 나오는 a=1에서 k>0인데 접합점이 영점 2의 왼쪽이고 넓이가 4/3이 아님. a>2는 조건에서 빠짐
assert kval(R(1)) > 0 and area(R(1)) != R(4, 3) and not any(cond(av) for av in grid if av > 2)
print('원문 줄 불통: a=1에서 k=1/2>0, 넓이 17/12 ≠ 4/3 · a>2는 모두 조건 밖')

# ---------- 6) 문장 길이(원문의 90% 이상)
pl = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s.replace('&lt;', '<').replace('&gt;', '>')))
new_len = len(pl(IT['body'])); org_len = len(pl(o[0]))
print('문장 길이', new_len, '/ 원문', org_len)
assert new_len >= 0.9 * org_len

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def best(G, **kw):
    V = {av: area(av, kw.get('d', 3)) for av in G if cond(av, **kw)}
    V = {t: v for t, v in V.items() if v is not None}
    return 12*max(V.values())


# 부등식 조건 전체를 빼면: 2<a<3에서 넓이가 계속 커지며 a=3은 연속일 수 없어 최댓값이 없다
B = [area(R(3) - R(1, 2**j)) for j in range(1, 9)]
assert all(B[i] < B[i + 1] for i in range(7)) and B[-1] > R(17, 12) and kval(R(3)) is None
ablation('부등식 조건 전체', f'최댓값 없음(a→3-에서 {sp.N(B[-1], 5)}로 커지기만 함)')
ablation('구간 끝 3a(→a)', best(grid, end=lambda t: t))
ablation('구간 끝 3a(→2a)', best(grid, end=lambda t: 2*t))
ablation('구간 끝 3a(→4a)', best(grid, end=lambda t: 4*t))
# 연속을 빼면 k가 a와 무관: a=1에서 조건은 k≥0이면 되고 넓이 5/12+2k는 한없이 커짐
ablation('x=a에서 연속', '최댓값 없음(a=1, k≥0이면 조건을 만족시키고 넓이 5/12+2k)')
assert all(sp.integrate(-p, (x, 0, 1)) + sp.integrate(-kk*(x - 3), (x, 1, 3)) == R(5, 12) + 2*kk for kk in [1, 5, 50])
ablation('직선 조각의 영점 3(→4)', best(grid, d=4))
# 양수 a: a≤0이면 조건은 성립하지만 둘러싸인 부분이 없다(원문 단서, S가 정의되도록 하는 조건)
assert all(cond(av) and area(av) is None for av in [R(-n, 4) for n in range(1, 13)])
ablation('양수 a(→실수 a)', '원문 단서: a<0이면 조건은 성립하나 둘러싸인 부분이 없어 S가 정의되지 않음')
print('ALL OK')
