# -*- coding: utf-8 -*-
# p1.py (2회 Claude 2·4·6·8번) 검증: 원문 풀이 · 계산 정답 = 지정 선지 · 유일성 · 선지 등차·오름차순·서로 다름 · wrongs가 선지에 있음 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, diff, integrate, solve, expand, nsimplify, Poly, real_roots, Abs, oo, limit
x, t, k, s = symbols('x t k s', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p1.py')).read(), ns)
IT = ns['ITEMS']
WANT = {2: 4, 4: 3, 6: 1, 8: 2}
assert sorted(IT) == [2, 4, 6, 8] and all(IT[n]['author'] == 'claude' for n in IT)
assert [IT[n]['key'] for n in (2, 4, 6, 8)] == ['M11', 'D54', 'D30', 'J25']
BUN = {2: False, 4: False, 6: True, 8: True}
for n in IT:
    it = IT[n]
    assert it['bunseok'] is BUN[n] and it['effect'] in ('같음', '쉬워짐') and it['precedent']
    assert 2 <= len(it['vtype']) <= 3 and it['level'] in ('하', '중', '중상', '상', '최상')
    assert '함정 추가' not in it['vtype'] or it['bunseok']
    assert len(it['wrongs']) >= 1 and all(w in it['choices'] for w in it['wrongs'])
    for f in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f]

def cv(c):
    c = str(c)
    m = re.fullmatch(r'\\dfrac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[1]), int(m[2])) if m else nsimplify(c)

def arith_up(no):
    v = [cv(c) for c in IT[no]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    return len(set(v)) == 5 and len(d) == 1 and list(d)[0] > 0

def chk(no, val, wrongs):
    ch = [cv(c) for c in IT[no]['choices']]
    ws = [cv(w) for w in IT[no]['wrongs']]
    good = (IT[no]['ans'] == WANT[no] and nsimplify(val) == ch[IT[no]['ans'] - 1] and arith_up(no)
            and sorted(ws) == sorted(nsimplify(w) for w in wrongs) and all(w in ch and w != nsimplify(val) for w in ws))
    print(f'{no}번: 계산 {val}, 선지 {ch[IT[no]["ans"] - 1]} (위치 {IT[no]["ans"]}), 공차 {ch[1] - ch[0]}, 오답 {ws} {"OK" if good else "FAIL"}')
    assert good

def min_on_ray(f, lo):
    """구간 [lo, ∞)에서 다항식 f의 최솟값 (최고차항 양수 가정, 끝점과 극점 비교)"""
    assert Poly(f, x).LC() > 0
    cand = [lo] + [r for r in real_roots(Poly(diff(f, x), x)) if r > lo]
    return min(f.subs(x, c) for c in cand)

def invertible(f):
    """다항함수 f가 실수 전체에서 일대일(역함수 존재) ⇔ f'이 부호를 바꾸지 않음 (f'=0은 고립점)"""
    fp = Poly(diff(f, x), x)
    rr = sorted(set(real_roots(fp)))
    pts = [rr[0] - 1] + [(rr[i] + rr[i + 1]) / 2 for i in range(len(rr) - 1)] + [rr[-1] + 1] if rr else [0]
    signs = {sp.sign(fp.eval(p)) for p in pts}
    return len(signs) == 1

def nondiff_pts(g):
    """|g(x)|가 미분가능하지 않은 점 = g의 실근 가운데 g'≠0인 점 (한쪽 미분계수로도 확인)"""
    out = []
    for r in set(real_roots(Poly(g, x))):
        dl = limit((Abs(g) - Abs(g.subs(x, r))) / (x - r), x, r, '-')
        dr = limit((Abs(g) - Abs(g.subs(x, r))) / (x - r), x, r, '+')
        assert (dl != dr) == (diff(g, x).subs(x, r) != 0)
        if dl != dr: out.append(r)
    return sorted(out)

def motion(v1, v2):
    """f(t)=|x1-x2| (t≥0)의 t>0에서 극대·극소 시각 (증감을 구간별로 조사)"""
    g = integrate(v1 - v2, (t, 0, t))
    f2 = expand(g**2)                       # f=|g|, f의 증감은 f^2의 증감과 같음
    crit = sorted({r for r in real_roots(Poly(diff(f2, t), t)) if r > 0})
    pts = [Rational(0)] + crit
    sgn = []
    for i in range(len(pts)):
        m = (pts[i] + pts[i + 1]) / 2 if i + 1 < len(pts) else pts[i] + 1
        sgn.append(sp.sign(diff(f2, t).subs(t, m)))
    mx = [crit[i] for i in range(len(crit)) if sgn[i] > 0 and sgn[i + 1] < 0]
    mn = [crit[i] for i in range(len(crit)) if sgn[i] < 0 and sgn[i + 1] > 0]
    return g, mx, mn

# ===== 원문 풀이 =====
# M11: x≥0에서 2x^3-6x^2+14 > a 인 정수 a의 최댓값 5 (②)
m11 = min_on_ray(2*x**3 - 6*x**2 + 14, 0)
assert m11 == 6 and max(a for a in range(-50, 50) if m11 > a) == 5
# D54: f=x^3/3-ax^2+3ax 역함수 존재 a의 최댓값 3 (①)
assert max(a for a in [Rational(j, 4) for j in range(-40, 60)] if invertible(x**3/3 - a*x**2 + 3*a*x)) == 3
# D30: f+kx=(x-1)^3, f(2)+f'(2)=0 → k=4/3 (②)
f30 = (x - 1)**3 - k*x
assert solve(f30.subs(x, 2) + diff(f30, x).subs(x, 2), k) == [Rational(4, 3)]
assert nondiff_pts((x - 1)**3) == []
# J25: v1=t^2-6t+5, v2=2t-7 → a=2, b=6, Q 거리 17/2 (②)
g25, mx25, mn25 = motion(t**2 - 6*t + 5, 2*t - 7)
assert mx25 == [2] and mn25 == [6]
assert integrate(Abs(2*t - 7), (t, 2, 6)) == Rational(17, 2)
print('원문 풀이 OK (M11=5, D54=3, D30=4/3, J25=17/2)')

# ===== 2번 =====
f2 = 2*x**3 - 3*x**2 - 12*x + 24
assert expand(diff(f2, x) - 6*(x + 1)*(x - 2)) == 0
m2 = min_on_ray(f2, 0)
assert m2 == 4 and f2.subs(x, 2) == 4 and f2.subs(x, 0) == 24
# 전수: 자연수 a = 1..200 중 x≥0에서 f(x)≥a가 항상 성립하는 것
ok2 = [a for a in range(1, 201) if m2 >= a]
v2 = len(ok2)
assert ok2 == [1, 2, 3, 4]
w2_strict = len([a for a in range(1, 201) if m2 > a])          # 부등호를 > 로 본 값
chk(2, v2, [w2_strict])

# ===== 4번 =====
F4 = lambda a: x**3/3 - a*x**2 + 4*a*x
non = [a for a in range(1, 41) if not invertible(F4(a))]
assert [a for a in range(1, 41) if invertible(F4(a))] == [1, 2, 3, 4]
v4 = min(non)
assert v4 == 5
# 판별식 확인: D/4 = a^2-4a, a=4이면 f'=(x-4)^2 ≥ 0 (증가, 역함수 존재)
assert expand(diff(F4(4), x) - (x - 4)**2) == 0 and invertible(F4(4))
w4_eq = min(a for a in range(1, 41) if a*a - 4*a >= 0)         # D=0도 역함수 없다고 본 값
chk(4, v4, [w4_eq])

# ===== 6번 =====
# g=f+kx (최고차항 계수 1 삼차). (나) ⇒ g(2)=0 (분모→0이면 분자→0). (가) ⇒ |g|의 미분불가능점 = {4} ⇒ g(4)=0
# 따라서 g=(x-2)(x-4)(x-s) (s 실수). 전수: s 후보를 유리수 격자 + 특수값으로 조사
def ok6(g):
    lim_ok = g.subs(x, 2) == 0                                   # (나) 극한 존재 ⇔ g(2)=0
    return lim_ok and nondiff_pts(g) == [4]
cand_s = sorted({Rational(j, 2) for j in range(-12, 21)} | {Rational(1, 3), Rational(7, 3)})
good_s = [c for c in cand_s if ok6(expand((x - 2)*(x - 4)*(x - c)))]
assert good_s == [2]
# 기호로도: |g|가 x=2에서 미분가능 ⇔ g'(2)=0 ⇔ s=2, x=4에서 미분불가능 ⇔ g'(4)≠0 ⇔ s≠4
gs = (x - 2)*(x - 4)*(x - s)
assert solve(diff(gs, x).subs(x, 2), s) == [2] and solve(diff(gs, x).subs(x, 4), s) == [4]
# 근이 2, 4뿐이 아닌 꼴(허근을 갖는 경우)은 g(4)=0을 함께 만족할 수 없음: g(2)=g(4)=0이면 위 꼴로 인수분해됨
g6 = (x - 2)**2*(x - 4)
assert ok6(expand(g6))
f6 = g6 - k*x
k6 = solve(f6.subs(x, 1) + diff(f6, x).subs(x, 1), k)
assert k6 == [2]
v6 = k6[0]
h6 = (x - 2)*(x - 4)**2 - k*x                                    # 중근·단순근을 바꾼 꼴
w6_swap = solve(h6.subs(x, 1) + diff(h6, x).subs(x, 1), k)[0]
assert not ok6(expand((x - 2)*(x - 4)**2))
c6 = (x - 2)**3 - k*x                                            # TIP1을 그대로 쓴 꼴 (선지 밖)
assert solve(c6.subs(x, 1) + diff(c6, x).subs(x, 1), k) == [1]
chk(6, v6, [w6_swap])

# ===== 8번 =====
v1, v2_ = (t - 3)**2, 9 - 2*t
g8, mx8, mn8 = motion(v1, v2_)
assert expand(g8 - t**2*(t - 6)/3) == 0
assert mx8 == [4] and mn8 == [6]                                 # t>0에서 극대 하나, 극소 하나 ⇒ a=4, b=6 유일
a8, b8 = mx8[0], mn8[0]
assert g8.subs(t, a8) < 0 and diff(g8, t).subs(t, a8) == 0      # 거리의 극대 = 위치의 차의 극소
assert g8.subs(t, b8) == 0 and diff(g8, t).subs(t, b8) != 0     # 거리의 극소 = 두 점이 만나는 시각 (g'≠0, 뾰족점)
v8 = integrate(Abs(v2_), (t, a8, b8))
assert v8 == Rational(5, 2)
w8_disp = Abs(integrate(v2_, (t, a8, b8)))                       # 위치의 변화량의 크기
assert integrate(v2_, (t, a8, b8)) == -2
chk(8, v8, [w8_disp])

# ===== 조건 빼 보기 =====
print('--- 조건 빼 보기 ---')
# 2번
print('ABLATION 2 x≥0: 필요(빼면 실수 전체에서 삼차함수는 아래로 끝없이 작아져 자연수 a가 없음, 4 → 0)')
assert limit(f2, x, -oo) == -oo
w = len([a for a in range(1, 201) if m2 > a])
print(f'ABLATION 2 부등호의 등호(≥): 필요(>이면 답 바뀜 {v2} → {w})'); assert w != v2
m2b = min_on_ray(2*x**3 - 3*x**2 - 12*x + 25, 0)
print(f'ABLATION 2 상수항 24: 필요(25이면 답 바뀜 {v2} → {len([a for a in range(1, 201) if m2b >= a])})')
print('ABLATION 2 자연수: 필요(정수이면 a≤4인 정수가 끝없이 많아 개수가 정해지지 않음)')
# 4번
neg = [a for a in (-1, -2, -10) if not invertible(F4(a))]
print(f'ABLATION 4 자연수: 필요(정수이면 a={neg}도 역함수가 없어 최솟값이 정해지지 않음)'); assert neg == [-1, -2, -10]
F4b = lambda a: x**3/3 - a*x**2 + 3*a*x
v4b = min(a for a in range(1, 41) if not invertible(F4b(a)))
print(f'ABLATION 4 계수 4a: 필요(3a이면 답 바뀜 {v4} → {v4b})'); assert v4b != v4
# 6번
fa = [(x - 2)**3, (x - 2)*(x**2 + 1), (x - 2)*(x - 5)**2]       # (가)를 빼면 g(2)=0만 남음
ka = {solve((g - k*x).subs(x, 1) + diff(g - k*x, x).subs(x, 1), k)[0] for g in fa}
print(f'ABLATION 6 (가): 필요(정해지지 않음: g=(x-2)^3, (x-2)(x^2+1), (x-2)(x-5)^2 → k={sorted(ka)})'); assert len(ka) > 1
fb = [(x - 4)*(x - c)**2 for c in (0, 1, 2, 3)]                   # (나)를 빼면 |g|가 x=4에서만 꺾이는 g는 여럿
assert all(nondiff_pts(expand(g)) == [4] for g in fb)
kb = {solve((g - k*x).subs(x, 1) + diff(g - k*x, x).subs(x, 1), k)[0] for g in fb}
print(f'ABLATION 6 (나): 필요(정해지지 않음: g=(x-4)(x-c)^2, c=0,1,2,3 → k={sorted(kb)})'); assert len(kb) > 1
print('ABLATION 6 f(1)+f\'(1)=0: 필요(없으면 f(x)=(x-2)^2(x-4)-kx가 모든 k에서 (가)(나)를 만족)')
assert all(ok6(expand((x - 2)**2*(x - 4))) for _ in (0,))
g6c = (x - 2)*(x - 4)*(x - 1)                                    # '에서만'을 빼고 'x=4에서 미분가능하지 않다'만 두면
assert 4 in nondiff_pts(expand(g6c)) and g6c.subs(x, 2) == 0
k6c = solve((g6c - k*x).subs(x, 1) + diff(g6c - k*x, x).subs(x, 1), k)[0]
print(f'ABLATION 6 (가)의 \'에서만\': 필요(빼면 g=(x-1)(x-2)(x-4)도 가능, k={k6c} ≠ {v6})'); assert k6c != v6
# 8번
print('ABLATION 8 t=a에서 극대: 필요(없으면 a가 정해지지 않음)')
print('ABLATION 8 t=b에서 극소: 필요(없으면 b가 정해지지 않음)')
# 단서 0<a<b: t=0에서 f(0)=0이 f의 최솟값이라 t=0을 극소로 읽으면 b=0도 후보
assert g8.subs(t, 0) == 0 and all(Abs(g8).subs(t, Rational(j, 10)) > 0 for j in range(1, 60))
print('ABLATION 8 (단, 0<a<b): 필요(빼면 f(0)=0인 t=0도 극소로 읽혀 b=0 또는 6, 원문 단서 그대로)')
g8b, mx8b, mn8b = motion((t - 3)**2, 2*t - 7)
print(f'ABLATION 8 v2=9-2t: 필요(원문 2t-7이면 극대 {mx8b}, 극소 {mn8b}: 도함수 (t-4)^2≥0이라 극값이 없음)'); assert (mx8b, mn8b) != ([4], [6])
g8c, mx8c, mn8c = motion(t**2 - 6*t + 5, 9 - 2*t)
v8c = integrate(Abs(9 - 2*t), (t, mx8c[0], mn8c[0])) if mx8c and mn8c else None
print(f'ABLATION 8 v1=(t-3)^2: 필요(원문 t^2-6t+5이면 극대 {mx8c}, 극소 {mn8c}, 답 {sp.N(v8c, 6)}: 무리수)'); assert v8c != v8

print('정답 위치:', [IT[n]['ans'] for n in sorted(IT)])
print('ALL OK')
