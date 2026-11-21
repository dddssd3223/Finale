# -*- coding: utf-8 -*-
"""p2.py (견본2 5–8번) 정답 검증: 정답·선지 정렬·유일성·함정 값"""
import os, re, sympy as sp, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p2.py'), encoding='utf-8').read(), ns); IT = ns['ITEMS']
x, t = sp.symbols('x t', real=True)

def parse(c):
    m = re.fullmatch(r'\\dfrac(\d+)(\d+)', c)
    if m: return sp.Rational(int(m.group(1)), int(m.group(2)))
    return sp.Integer(int(c))

def chk(no, v):
    it = IT[no]
    ch = [parse(c) for c in it['choices']]
    assert ch == sorted(ch), (no, '선지 정렬', ch)
    assert len(set(ch)) == 5, (no, '선지 중복')
    assert ch[it['ans'] - 1] == v, (no, ch, v)
    assert list(ch).count(v) == 1
    print(f'{no}번 OK: 정답 {v} = 선지 {it["ans"]}  선지 {ch}')
    return ch

def sign_changes(expr, var, lo, hi_extra=50):
    """var>lo 에서 expr의 실근 중 부호가 실제로 바뀌는 점"""
    out = []
    for r, m in sp.roots(sp.Poly(expr, var)).items():
        if r.is_real and r > lo:
            eps = sp.Rational(1, 1000)
            if sp.sign(expr.subs(var, r - eps)) != sp.sign(expr.subs(var, r + eps)):
                out.append(r)
    return sorted(out)

# ---------- 5번 ----------
k = sp.Symbol('k', real=True)
X = t**4 - 8*t**3 + k*t**2
V = sp.diff(X, t); A = sp.diff(V, t)
tv = sp.solve(sp.diff(A, t), t); assert tv == [2] and sp.diff(A, t, 2) > 0      # 가속도 최솟값은 꼭짓점 t=2 (t>=0 안)
ks = sp.solve(sp.Eq(A.subs(t, 2), -28), k); assert ks == [10]
V5 = V.subs(k, 10); A5 = A.subs(k, 10)
assert sp.factor(V5) == 4*t*(t - 1)*(t - 5)
sc = sign_changes(V5, t, 0); assert sc == [1, 5], sc                            # t=0은 출발 시각(제외)
assert V5.subs(t, 0) == 0                                                        # 함정: 출발 시각 속도 0
ch = chk(5, A5.subs(t, sc[1]))
assert A5.subs(t, 1) + A5.subs(t, 5) in ch   # 함정 값 64 (선지 등차 배열 64~80)

# ---------- 6번 ----------
v1 = (t - 1)**2
assert sp.diff(v1, t).subs(t, 2) == (-6*t + 14).subs(t, 2)                        # 연결점 가속도 일치(조건 모순 없음)
C = sp.Symbol('C')
v2 = sp.integrate(-6*t + 14, t) + C
Cv = sp.solve(sp.Eq(v2.subs(t, 2), v1.subs(t, 2)), C); assert Cv == [-15]
v2 = v2.subs(C, -15); assert sp.factor(v2 + (3*t - 5)*(t - 3)) == 0
# 방향 전환: [0,2]에서는 v1, [2,∞)에서는 v2
sc1 = [r for r in sign_changes(v1, t, 0) if r < 2]; assert sc1 == []            # t=1 중근: 방향 불변
assert v1.subs(t, 1) == 0
sc2 = [r for r in sign_changes(v2, t, 0) if r > 2]; assert sc2 == [3]
assert v1.subs(t, 2) > 0 and v2.subs(t, 2) > 0                                    # t=2는 전환 아님
pos = lambda T: sp.integrate(v1, (t, 0, min(T, 2))) + (sp.integrate(v2, (t, 2, T)) if T > 2 else 0)
ans6 = sum(pos(T) for T in sc1 + sc2)
# 수치 확인: 구간별 속도로 부호 전환 탐색
f1 = sp.lambdify(t, v1); f2 = sp.lambdify(t, v2)
g = np.linspace(0, 20, 2000001); vv = np.where(g <= 2, f1(g), f2(g))
s = np.sign(np.round(vv, 12)); nz = s != 0
idx = np.where(np.diff(s[nz]) != 0)[0]
assert len(idx) == 1 and abs(g[nz][idx[0]] - 3) < 1e-4
ch = chk(6, ans6)
assert pos(1) + pos(3) in ch and pos(2) + pos(3) in ch  # 함정 값 2, 7/3 (선지 등차 배열 1~7/3)

# ---------- 7번 ----------
b, c, d = sp.symbols('b c d')
f = x**3 + b*x**2 + c*x + d
tan = lambda p, X0: f.subs(x, p) + sp.diff(f, x).subs(x, p)*(X0 - p)
eqs = [sp.Eq(f.subs(x, -1), 8), sp.Eq(tan(-1, 0), 8), sp.Eq(tan(2, 0), 8)]
sol = sp.solve(eqs, [b, c, d], dict=True); assert len(sol) == 1                 # 유일
f7 = sp.expand(f.subs(sol[0])); assert sp.expand(f7 - ((x + 1)**2*(x - 8) + 8)) == 0
crit = sp.solve(sp.diff(f7, x), x); assert sorted(crit) == [-1, 5]
assert sp.diff(f7, x, 2).subs(x, -1) < 0 and sp.diff(f7, x, 2).subs(x, 5) > 0   # -1 극대, 5 극소 (함정)
ch = chk(7, f7.subs(x, 5))
assert f7.subs(x, 4) in ch   # 함정 값 -92 (선지 등차 배열 -100~-68)

# ---------- 8번 ----------
cs = sp.symbols('c0:7'); K = sp.Symbol('K')
fg = sum(cs[i]*x**i for i in range(7))
G = sp.integrate(2*x*fg, x) + K
eqs = sp.Poly(sp.expand(G - (x**2*fg - 3*x**5 + 4*x**4)), x).coeffs()
sl = sp.solve(eqs, list(cs[1:]) + [K], dict=True); assert len(sl) == 1
f8 = fg.subs(sl[0]); G8 = G.subs(sl[0]); C0 = cs[0]
assert sp.expand(f8 - (5*x**3 - 8*x**2 + C0)) == 0
assert sp.expand(sp.diff(G8, x) - 2*x*f8) == 0
# 접선이 원점을 지남: 0 = G(1) + G'(1)(0-1)
Cs = sp.solve(sp.Eq(G8.subs(x, 1) - sp.diff(G8, x).subs(x, 1), 0), C0); assert Cs == [4]
ans8 = f8.subs({C0: 4, x: 2})
ch = chk(8, ans8)
# 함정: G(1)=f(1) (P(1) 누락) → 11, G(1)=0 → 10
trapA = f8.subs({C0: sp.solve(sp.Eq(f8.subs(x, 1), 2*f8.subs(x, 1)), C0)[0], x: 2})
trapB = f8.subs({C0: sp.solve(sp.Eq(G8.subs(x, 1), 0), C0)[0], x: 2})
assert trapA == 11 and trapB == 10 and trapA in ch and trapB in ch

# 정답 번호 지정 위치
assert [IT[n]['ans'] for n in (5, 6, 7, 8)] == [5, 3, 1, 4]
# 글꼴 금지 문자(기울임 l, o, 대문자 W V Y Z) 검사: 수식 안 단독 변수
for n, it in IT.items():
    txt = ' '.join(str(v) for kk, v in it.items() if isinstance(v, str)) + ' '.join(v for _, v in it.get('cond', []))
    for m in re.findall(r'\\\((.*?)\\\)', txt, flags=re.S):
        s2 = re.sub(r'\\[A-Za-z]+', '', m)
        bad = re.findall(r'(?<![A-Za-z])[loWVYZ](?![A-Za-z])', s2)
        assert not bad, (n, m, bad)
print('ALL OK')
