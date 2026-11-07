# -*- coding: utf-8 -*-
"""q5.py (4·12번) 정답 검증"""
import os, re, sympy as sp, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'q5.py'), encoding='utf-8').read(), ns); IT = ns['ITEMS']
x, r, b, c, d = sp.symbols('x r b c d', real=True)
EXPECT_POS = {4: 1, 12: 5}

def chk(no, val):
    it = IT[no]
    def tex(s):
        s = re.sub(r'\\dfrac\{(-?\d+)\}\{?(\d+)\}?', r'(\1)/(\2)', s)
        return sp.nsimplify(s)
    ch = [tex(s) for s in it['choices']]
    assert ch == sorted(ch), (no, '선지 정렬', ch)
    assert len(set(ch)) == 5, (no, '선지 중복')
    assert it['ans'] == EXPECT_POS[no], (no, '지정 정답 위치')
    assert sp.simplify(ch[it['ans'] - 1] - val) == 0, (no, ch, val)
    print(f'{no}번 OK: 정답 {val} = 선지 {it["ans"]}  선지 {ch}')
    return ch

# ---------- 4번 ----------
f1 = x**2 - 2*x + 4; f2 = -x**2 + 2*x + 2
diff = sp.factor(f1 - f2)
assert sp.expand(diff - 2*(x - 1)**2) == 0
assert sp.solve(sp.Eq(f1, f2), x) == [1]          # 접점 하나뿐 → 둘러싸인 부분은 [1,4] 하나
A = sp.integrate(f1 - f2, (x, 1, 4))
# 수치 확인: 격자 면적
xs = np.linspace(1, 4, 300001); A_num = np.trapezoid(2*(xs - 1)**2, xs)
assert abs(A_num - 18) < 1e-6
ch = chk(4, A)
# 오답 설계 값 포함 확인
assert sp.integrate(f1 - f2, (x, 0, 4)) == sp.Rational(56, 3) and sp.Rational(56, 3) in ch
assert sp.integrate(2*x**2 - 4*x + 6, (x, 1, 4)) == 30 and 30 in ch

# ---------- 12번 ----------
# 일반 삼차 f = x^3 + b x^2 + c x + d 에 대해 (가): f(-1)=3, f'(-1)=0 (극한 존재 필요충분)
F = x**3 + b*x**2 + c*x + d
eqs = [F.subs(x, -1) - 3, sp.diff(F, x).subs(x, -1)]
# (가) 필요충분 확인: 분자 = (x+1)^2(x-r) 꼴일 때 극한값 -1-r 존재
fr = (x + 1)**2*(x - r) + 3
assert sp.limit((fr - 3)/(x + 1)**2, x, -1) == -1 - r
# (나): 열린구간 (4,6)의 모든 x에서 f(x) >= f(5) → r 전수 탐색(수치) + 기호
g_num = sp.lambdify((x, r), fr, 'numpy')
XS = np.linspace(4, 6, 4001)[1:-1]
RV = np.linspace(-20, 40, 60001)
G = g_num(XS[None, :], RV[:, None]) - g_num(5.0, RV)[:, None]
ok = RV[np.all(G >= -1e-9, axis=1)]
assert ok and abs(min(ok) - 8) < 2e-3 and abs(max(ok) - 8) < 2e-3, (min(ok), max(ok))
rs = sp.solve(sp.diff(fr, x).subs(x, 5), r); assert rs == [8]
f = sp.expand(fr.subs(r, 8))
assert f == x**3 - 6*x**2 - 15*x - 5
fp = sp.factor(sp.diff(f, x)); assert sp.expand(fp - 3*(x + 1)*(x - 5)) == 0
# 극대 x=-1, 극소 x=5 (부호 + - +)
assert sp.diff(f, x, 2).subs(x, -1) < 0 and sp.diff(f, x, 2).subs(x, 5) > 0
M = f.subs(x, -1); m = f.subs(x, 5)
assert (M, m) == (3, -105)
assert sp.expand(f - M - (x + 1)**2*(x - 8)) == 0
assert sp.expand(f - m - (x - 5)**2*(x + 4)) == 0
sol = sp.solve_univariate_inequality(f >= m, x, relational=False).intersect(
      sp.solve_univariate_inequality(f <= M, x, relational=False))
assert sol == sp.Interval(-4, 8), sol
ints = [k for k in range(-200, 201) if m <= f.subs(x, k) <= M]
assert ints == list(range(-4, 9)), ints
ch = chk(12, len(ints))
# 오답 설계 값
assert len(range(-1, 6)) == 7 and 7 in ch            # 극점 사이만
assert len(ints) - 2 == 11 and 11 in ch              # 양 끝 등호 제외
assert len(ints) - 1 == 12 and 12 in ch              # 한쪽 끝 제외
assert len(range(-1, 9)) == 10 and len(range(-4, 6)) == 10 and 10 in ch   # 한쪽 바깥만
# 다른 확정 문항과 정답값 겹침 확인(참고)
print('모든 검증 통과')
