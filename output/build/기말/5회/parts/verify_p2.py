# -*- coding: utf-8 -*-
# p2.py (5회 5·6·7·8번) 검증: 원문·분석집 변형 풀이 · 계산 정답 = 지정 선지 · 유일성(전수) · 선지 등차·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re, itertools
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, oo, factor
x, a, b, p, q, r, s, al, be = symbols('x a b p q r s alpha beta', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p2.py')).read(), ns)
IT = ns['ITEMS']
WANT = {5: 4, 6: 1, 7: 5, 8: 3}                                       # 분담표 목표 정답
REF = {5: 'D10 분석집_변형 1', 6: 'J11 분석집_변형 1', 7: 'D35 분석집_변형 1', 8: 'D22 분석집_변형 1'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
assert sorted(IT) == [5, 6, 7, 8]
assert [IT[n]['key'] for n in (5, 6, 7, 8)] == ['D10', 'J11', 'D35', 'D22']
OPS = {f'OP{i:02d}' for i in range(1, 56)}
for n, it in IT.items():
    assert it['db_ref'] == REF[n] and it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐')
    assert it['ops'] and all(o in OPS for o in it['ops']) and it['precedent'] and 'STUDY-' in it['precedent']
    assert n == 5 or COEF & set(it['ops']), n                         # 계수·매개변수 자리 조작(6·7·8; 5번은 학교식으로 내려 뺌, 조정자 지시)
    assert '함정 추가' not in it['vtype'] and len(it['vtype']) <= 3 and it['level'] in ('하', '중')   # 목표 수준 중하–중
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src', 'body'):
        assert it[f]
    assert 'class="fig"' not in it['body'] and 'cond' not in it        # 그림 없음, 상자 × (문장 조건)
    for w in it['wrongs']:
        assert f'{"①②③④⑤"[it["choices"].index(w)]} \\({w}\\)' in it['wrong'], (n, w)

def cv(c_):
    c_ = str(c_)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', c_)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(c_)

def arith(no):
    v = [cv(c_) for c_ in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] != 0

def chk(no, val, wrongs):
    ch = [cv(c_) for c_ in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith(no)
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {ch[1] - ch[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

# ===== 공통: f=-x^3+ax^2+bx 조건을 (a,b)에 대한 식으로 =====
def fp_of(A, B): return -3*x**2 + 2*A*x + B
def inc_on(A, B, L, R):          # [L,R]에서 f' ≥ 0 (f'은 위로 볼록 → 양 끝만 보면 됨)
    g = fp_of(A, B); return g.subs(x, L) >= 0 and g.subs(x, R) >= 0
def dec_shift(A, B, k):          # x>0에서 f'(x)+k ≤ 0
    if A <= 0: return B + k <= 0
    return Rational(A)**2/3 + B + k <= 0
# 끝점 판정이 맞는지 표본으로 확인
for A, B in itertools.product(range(-8, 3), range(-12, 4)):
    g = fp_of(A, B)
    smp = [Rational(-2) + Rational(j, 20) for j in range(21)]
    assert inc_on(A, B, -2, -1) == all(g.subs(x, t_) >= 0 for t_ in smp)
    smp2 = [Rational(1, 10**6)] + [Rational(j, 10) for j in range(1, 200)]   # x→0+ 쪽도
    assert dec_shift(A, B, 7) == (max(g.subs(x, t_) for t_ in smp2) + 7 <= 0)

def lp_max(obj, L, R, k, use=('가', '나')):
    """조건을 만족시키는 (a,b) 영역에서 obj의 최댓값: 꼭짓점 후보 전수 + 격자 확인"""
    cons = []
    if '가' in use: cons += [fp_of(a, b).subs(x, L), fp_of(a, b).subs(x, R)]   # ≥ 0
    if '나' in use: cons += [-(b + k)]                                          # a≤0 가지에서 ≥ 0 (a>0 가지는 아래에서 불가능 확인)
    cands = []
    for c1, c2 in itertools.combinations(cons, 2):
        S = solve([c1, c2], [a, b], dict=True)
        for so in S:
            if all(c.subs(so) >= 0 for c in cons) and so[a] <= 0: cands.append(so)
    return cands

# ===== 원문 풀이 =====
# D10: (-3,0) 증가, (0,∞) 감소 → b=0, a≤-9/2, f(-2)=8+4a 최댓값 -10
assert solve(fp_of(a, 0).subs(x, -3), a) == [Rational(-9, 2)] and (8 + 4*a).subs(a, Rational(-9, 2)) == -10
# 분석집 D10 변형①: (-3,-1) 증가, (0,∞) 감소 → f(-2)=2-2f'(-1) ≤ 2
f10 = -x**3 + a*x**2 + b*x
assert expand(f10.subs(x, -2) - (2 - 2*fp_of(a, b).subs(x, -1))) == 0
assert inc_on(-6, -9, -3, -1) and dec_shift(-6, -9, 0) and f10.subs({a: -6, b: -9, x: -2}) == 2
# J11: y=-x^3+2x^2+3x, (1,4)에서의 접선 y=4x, 넓이 1/12
cJ = -x**3 + 2*x**2 + 3*x
tJ = cJ.subs(x, 1) + diff(cJ, x).subs(x, 1)*(x - 1)
assert expand(tJ - 4*x) == 0 and integrate(tJ - cJ, (x, 0, 1)) == Rational(1, 12)
# 분석집 J11 변형①: y=x^3-3x^2+2x+1, A(-1,-5) → 접점 2, 넓이 27/4
cS = x**3 - 3*x**2 + 2*x + 1
tS = cS.subs(x, 2) + diff(cS, x).subs(x, 2)*(x - 2)
assert tS.subs(x, -1) == -5 and abs(integrate(cS - tS, (x, -1, 2))) == Rational(27, 4)
# D35: 최고차항 1, 극솟값 -2, 감소 (-1,3) → 극댓값 30
fD = integrate(3*(x + 1)*(x - 3), x)
cD = solve(fD.subs(x, 3) + s + 2, s)[0]
assert (fD + cD).subs(x, -1) == 30
# 분석집 D35 변형①: 극댓 10, 극솟 -6, (-1,3) → f'(1)=-6
pS = solve(integrate(3*p*(x + 1)*(x - 3), (x, 3, -1)) - 16, p)
assert pS == [Rational(1, 2)] and (3*p*(x + 1)*(x - 3)).subs({p: pS[0], x: 1}) == -6
# D22: x=3 극댓값 0, 세 실근 등차, 극솟값 -16 → f(0)=9
d2 = symbols('d2', positive=True)
f22 = (x - 3)**2*((x - 3)**2 - d2)
mn = f22.subs(x, 3 + sp.sqrt(d2/2))
d2v = solve(sp.simplify(mn) + 16, d2)
assert d2v == [8] and f22.subs({d2: 8, x: 0}) == 9
# 분석집 D22 변형①: x=2 극댓값 5, 두 극솟값 같음, 극솟값 -11 → f(5)=14
fS22 = x**2*(x - 4)**2 - 11
assert fS22.subs(x, 2) == 5 and fS22.subs(x, 5) == 14
print('원문·분석집 풀이 OK (D10=-10/2, J11=1/12·27/4, D35=30/-6, D22=9/14)')

# ===== 5번 (D10 분석집_변형 1, 학교식: 최고차항 -2, 구간 (-2,-1), f(-2)의 최댓값) =====
f5 = -2*x**3 + a*x**2 + b*x
def fp5(A, B): return diff(f5, x).subs({a: A, b: B})
def ok5(A, B, use=('가', '나')):
    g = fp5(A, B)
    c1 = g.subs(x, -2) >= 0 and g.subs(x, -1) >= 0                    # (가): f'은 위로 볼록 → 양 끝만
    c2 = (B <= 0) if A <= 0 else (Rational(A)**2/6 + B <= 0)           # (나): x>0에서 f' ≤ 0
    return ('가' not in use or c1) and ('나' not in use or c2)
for A, B in itertools.product(range(-14, 3), range(-20, 4)):            # 끝점 판정 = 표본 판정
    g = fp5(A, B)
    assert (g.subs(x, -2) >= 0 and g.subs(x, -1) >= 0) == all(g.subs(x, Rational(-2) + Rational(j, 20)) >= 0 for j in range(21))
    assert ((B <= 0) if A <= 0 else (Rational(A)**2/6 + B <= 0)) == (max(g.subs(x, t_) for t_ in [Rational(1, 10**6)] + [Rational(j, 20) for j in range(1, 200)]) <= 0)
obj5 = f5.subs(x, -2)
assert expand(obj5 - (4 - 2*fp5(a, b).subs(x, -1))) == 0               # f(-2) = 4 - 2f'(-1): f'(-2)의 계수 0
grid = [Rational(j, 2) for j in range(-40, 7)]
mx = max(obj5.subs({a: A, b: B}) for A in grid for B in grid if ok5(A, B))
assert mx == 4
assert ok5(-9, -12) and obj5.subs({a: -9, b: -12}) == 4 and expand(fp5(-9, -12) + 6*(x + 1)*(x + 2)) == 0
v5 = 4
w5 = max(obj5.subs({a: A, b: 0}) for A in grid if ok5(A, 0))           # b=0 습관(원문처럼 f'(0)=0)
assert w5 == -8
chk(5, v5, [w5])

# ===== 6번 (J11 분석집_변형 1 + 학교식_예상 2: 계수 a, 넓이 → a) =====
def lines6(av, allowA=False):
    """곡선 y=x^3-av x^2+x 위의 A(1,·)를 지나고 곡선 위의 점 B에서 접하는 직선들 → (β, 넓이)"""
    c = x**3 - av*x**2 + x
    assert c.subs(x, 1) == 2 - av
    tb = symbols('tb', real=True)
    tan = c.subs(x, tb) + diff(c, x).subs(x, tb)*(x - tb)
    bs = solve(sp.Eq(tan.subs(x, 1), c.subs(x, 1)), tb)
    out = []
    for bb in bs:
        if bb == 1 and not allowA: continue
        tl = tan.subs(tb, bb)
        rts = sorted(set(real_roots(Poly(expand(c - tl), x))))
        if len(rts) < 2: out.append((bb, 0)); continue
        out.append((bb, abs(integrate(c - tl, (x, rts[0], rts[-1])))))
    return out
# β=(a-1)/2 (일반)
tb_ = symbols('tb', real=True); c6 = x**3 - a*x**2 + x
tan6 = c6.subs(x, tb_) + diff(c6, x).subs(x, tb_)*(x - tb_)
assert factor(expand(tan6.subs(x, 1) - c6.subs(x, 1))) in (factor((tb_ - 1)**2*(2*tb_ - a + 1)), factor(-(tb_ - 1)**2*(2*tb_ - a + 1)))
assert expand(c6 - tan6.subs(tb_, (a - 1)/2) - (x - (a - 1)/2)**2*(x - 1)) == 0
# 넓이 = ((a-3)/2)^4/12 = 1/12 를 만족시키는 a 전수 (정수 격자 + 방정식)
sol6 = sorted(solve(((a - 3)/2)**4/12 - Rational(1, 12), a))
assert sol6 == [1, 5]
for av in sol6:
    L = lines6(av); assert len(L) == 1 and L[0][1] == Rational(1, 12)
for av in range(-20, 21):                                           # 다른 정수 a는 넓이가 1/12가 아님
    L = lines6(av)
    assert (av in sol6) == any(ar == Rational(1, 12) for _, ar in L)
v6 = sol6[0]*sol6[1]
assert v6 == 5
w6 = sp.prod(solve(((a - 2) - 1)**4/12 - Rational(1, 12), a))        # A를 접점으로: 다른 교점 a-2
assert sorted(solve(((a - 2) - 1)**4/12 - Rational(1, 12), a)) == [2, 4] and w6 == 8
chk(6, v6, [w6])

# ===== 7번 (D35 분석집_변형 1 + 조작_보강 1: 기울기 2 기준) =====
c3, c2, c1, c0 = symbols('c3 c2 c1 c0', real=True)
f7 = c3*x**3 + c2*x**2 + c1*x + c0
g7 = f7 - 2*x
# g가 감소하는 최대 열린구간이 (-3,1) ⇔ g'(-3)=g'(1)=0 이고 c3>0 (c3<0이면 감소 구간이 한쪽으로 무한)
S7 = solve([diff(g7, x).subs(x, -3), diff(g7, x).subs(x, 1), g7.subs(x, -3) - 6, g7.subs(x, 1) + 10], [c3, c2, c1, c0], dict=True)
assert len(S7) == 1 and S7[0][c3] == Rational(1, 2)
F7 = f7.subs(S7[0])
assert expand(diff(F7, x) - (Rational(3, 2)*(x + 3)*(x - 1) + 2)) == 0
v7 = diff(F7, x).subs(x, -1)
assert v7 == -4
# 감소 조건 확인: (-3,1) 안에서 f(x2)-f(x1) < 2(x2-x1), 구간을 넓히면 깨짐
pts = [Rational(-3) + Rational(j, 10) for j in range(1, 40)]
assert all(F7.subs(x, u) - F7.subs(x, t_) < 2*(u - t_) for t_, u in itertools.combinations(pts, 2))
assert F7.subs(x, Rational(6, 5)) - F7.subs(x, 1) > 2*(Rational(6, 5) - 1)                    # b>1이면 (1, 6/5)에서 깨짐
assert F7.subs(x, -3) - F7.subs(x, Rational(-16, 5)) > 2*(-3 - Rational(-16, 5))              # a<-3이면 (-16/5, -3)에서 깨짐
# 극댓값 6, 극솟값 -10 확인
assert (F7 - 2*x).subs(x, -3) == 6 and (F7 - 2*x).subs(x, 1) == -10
w7a = diff(F7 - 2*x, x).subs(x, -1)                                   # g'(-1)
w7b = w7a - 2                                                         # 부호 반대로
assert (w7a, w7b) == (-6, -8)
chk(7, v7, [w7a, w7b])

# ===== 8번 (D22 분석집_변형 1 + 조작_보강 1: 직선 y=x-3에 두 점에서 접함, 한 접점 x=2) =====
g8 = (x - al)**2*(x - 2)**2 - 3                                       # f(x)-x
cand = solve(diff(g8, x).subs(x, 0), al)
assert sorted(cand) == [-2, 0]
good = [c_ for c_ in cand if c_ != 2 and diff(g8.subs(al, c_), x, 2).subs(x, 0) < 0]   # x=0에서 극대
assert good == [-2]                                                   # al=0이면 x=0은 극소(접점)
f8 = expand(g8.subs(al, -2) + x)
assert Poly(f8, x).LC() == 1 and expand(f8 - (x - 3) - (x + 2)**2*(x - 2)**2) == 0
v8 = f8.subs(x, 1); w8 = (f8 - x).subs(x, 1)
assert (v8, w8) == (7, 6)
chk(8, v8, [w8])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 5번
print("ABLATION 5 (가) (-2,-1)에서 증가: 필요(빼면 b→-∞에서 f(-2)가 한없이 커짐)"); assert ok5(-1, -100, use=('나',)) and obj5.subs({a: -1, b: -100}) > 100
print(f"ABLATION 5 (가)의 끝 -1: 필요(구간을 (-2,-1)에서 (-3,-2)로 옮기면 f(-2)=16+4a-2b의 최댓값이 바뀜)"); assert max(obj5.subs({a: A, b: B}) for A in grid for B in grid if ok5(A, B, use=('나',)) and fp5(A, B).subs(x, -3) >= 0 and fp5(A, B).subs(x, -2) >= 0) != v5
print("ABLATION 5 (나) (0,∞)에서 감소: 군더더기(답 그대로) — 분석집 문항과 같이 b=0 습관(오답 -8)을 부르는 원문 조건으로 둠"); assert max(obj5.subs({a: A, b: B}) for A in grid for B in grid if ok5(A, B, use=('가',))) == v5
# 6번
s6b = sorted(solve(((a - 3)/2)**4/12 - Rational(4, 3), a))
print(f'ABLATION 6 넓이 1/12: 필요(4/3이면 a={s6b}, 곱 {s6b[0]*s6b[1]})'); assert s6b[0]*s6b[1] != v6
allA = sorted(set(sol6) | {2, 4})
assert all(any(ar == Rational(1, 12) for _, ar in lines6(av, allowA=True)) for av in allA)
print(f'ABLATION 6 단서(B는 A가 아님): 필요(빼면 A에서의 접선도 들어가 a={allA}, 곱 {sp.prod(allA)})'); assert sp.prod(allA) != v6
print('ABLATION 6 A의 x좌표 1: 필요(x좌표가 0이면 β=a/2, |β|=1에서 a=±2, 곱 -4)'); assert sorted(solve((a/2)**4/12 - Rational(1, 12), a)) == [-2, 2]
# 7번
pS0 = solve(integrate(3*p*(x + 3)*(x - 1), (x, 1, -3)) - 16, p)[0]
alt7 = (3*pS0*(x + 3)*(x - 1)).subs(x, -1)
print(f'ABLATION 7 기울기 2(f(x)-2x와 2(x2-x1)): 필요(0이면 분석집처럼 f\'(-1)={alt7})'); assert alt7 != v7
pS1 = solve(integrate(3*p*(x + 3)*(x - 1), (x, 1, -3)) - 32, p)[0]
print(f'ABLATION 7 극댓값 6·극솟값 -10: 필요(차가 32이면 p={pS1}, 답 {(3*pS1*(x + 3)*(x - 1)).subs(x, -1) + 2})'); assert (3*pS1*(x + 3)*(x - 1)).subs(x, -1) + 2 != v7
pS2 = solve(integrate(3*p*(x + 3)*(x - 3), (x, 3, -3)) - 16, p)[0]
print(f'ABLATION 7 b의 최댓값 1: 필요(3이면 p={pS2}, 답 {(3*pS2*(x + 3)*(x - 3)).subs(x, -1) + 2})'); assert (3*pS2*(x + 3)*(x - 3)).subs(x, -1) + 2 != v7
# 8번
alt8 = expand((x - al)**2*(x - 2)**2 - 3 + x)
print("ABLATION 8 x=0에서 극대: 필요(극소로 읽으면 al=0, f(1)={})".format(alt8.subs({al: 0, x: 1}))); assert alt8.subs({al: 0, x: 1}) != v8
print("ABLATION 8 한 접점의 x좌표 2: 필요(3이면 다른 접점 -3, f(1)={})".format(((x + 3)**2*(x - 3)**2 - 3 + x).subs(x, 1))); assert ((x + 3)**2*(x - 3)**2 - 3 + x).subs(x, 1) != v8
print("ABLATION 8 직선 y=x-3(기울기 1): 필요(y=-3, f(x)로 두면 f(1)={})".format(w8)); assert w8 != v8

print('ALL OK')
