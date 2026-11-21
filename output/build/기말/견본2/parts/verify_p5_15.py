# 15번 수정본(60∫_1^3 f) 검증: 정답·오답 선지·미분가능성
import sympy as sp, os
x = sp.symbols('x')
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns); it = ns['ITEMS'][15]
f0 = x**2 + x + 2
def run(A, B):
    f1 = ((x - 2) * f0.subs(x, x - 1) + A * (x - 1) + B).expand(); f2 = ((x - 2) * f1.subs(x, x - 1) + A * (x - 1) + B).expand()
    return f1, f2, 60 * (sp.integrate(f1, (x, 1, 2)) + sp.integrate(f2, (x, 2, 3)))
a = sp.diff(f0, x).subs(x, 1) - f0.subs(x, 0) + sp.diff(f0, x).subs(x, 0); b = f0.subs(x, 1) + f0.subs(x, 0)
f1, f2, ans = run(a, b)
for X, g, h in ((1, f0, f1), (2, f1, f2)):
    assert g.subs(x, X) == h.subs(x, X) and sp.diff(g, x).subs(x, X) == sp.diff(h, x).subs(x, X)
assert ans == 1077 and it['choices'][it['ans'] - 1] == '1077'
wrong = {run(3, 4)[2], run(1, 6)[2], run(2, 4)[2], 60 * sp.integrate(f1, (x, 1, 2))}
assert wrong == {917, 937, 777, 345} and '917' in it['choices']   # 선지 등차 배열 917~1077: 원본 공식 함정 917
assert [int(c) for c in it['choices']] == sorted(int(c) for c in it['choices'])
print('15번 수정본 ALL OK')
