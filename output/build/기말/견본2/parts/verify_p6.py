# -*- coding: utf-8 -*-
# p6 (17·18번) 검증: 전수 케이스 분석 (sympy 정확 계산 + 수치 스캔)
import sympy as sp
from fractions import Fraction as Fr
import itertools, math

x = sp.symbols('x', real=True)

# =====================================================================
# 17번 (M39 구조 변경)
#  f: 최고차항 1인 사차, f(0)=f'(0)=0, f(1)<1
#  h(t) = |f(x)-f(t)|가 미분가능하지 않은 x의 개수 = H(f(t)),  H(s) = f(x)=s의 단순근 개수
#  (가) h가 불연속인 t의 개수 3   (나) h는 t=6에서 불연속
#  답: 가능한 모든 f(1)의 합 = -12 (정답 ①)
# =====================================================================
print('=== 17번 ===')

def H(f, s):
    """f(x)=s 의 단순(중복도 1) 실근 개수 (s 유리수)"""
    P = sp.Poly(sp.expand(f - s), x)
    n = 0
    for fac, m in sp.sqf_list(P)[1]:
        if m == 1:
            n += len(sp.real_roots(fac))
    return n

def disc_points(f):
    """h(t)=H(f(t))가 불연속인 t 목록과 각 점의 (좌극한, 함숫값, 우극한)"""
    fp = sp.diff(f, x)
    crit = [c for c in sp.roots(sp.Poly(fp, x)) if c.is_real]
    assert all(c.is_Rational for c in crit), crit
    cvals = sorted(set(sp.expand(f.subs(x, c)) for c in crit), key=float)
    # 임계값 사이 구간의 대표값
    def Hside(c, side):
        i = cvals.index(c)
        if side > 0:
            s = c + 1 if i == len(cvals) - 1 else (c + cvals[i + 1]) / 2
        else:
            s = c - 1 if i == 0 else (c + cvals[i - 1]) / 2
        return H(f, sp.Rational(s))
    out = []
    for c in cvals:
        Hc = H(f, c)
        Hp, Hm = Hside(c, 1), Hside(c, -1)
        P = sp.Poly(sp.expand(f - c), x)
        for fac, mu in sp.sqf_list(P)[1]:
            for t0 in sp.real_roots(fac):
                # t0 근방에서 f(t)-c 의 부호 (오른쪽, 왼쪽)
                d = sp.diff(f, x, mu).subs(x, t0)
                sr = sp.sign(sp.N(d, 50))
                sl = sr * (-1) ** mu
                R = Hp if sr > 0 else Hm
                L = Hp if sl > 0 else Hm
                if not (L == Hc == R):
                    out.append((t0, (L, Hc, R)))
    return sorted(out, key=lambda z: float(z[0]))

def fam_pq(p, q):
    """f'(x)=4x(x-p)(x-q) 인 사차 (f(0)=0)"""
    return sp.expand(x**4 - sp.Rational(4, 3) * (p + q) * x**3 + 2 * p * q * x**2)

# (1) 전수 분류: 임계점이 실수인 경우 p,q 격자, 복소인 경우 (a,b) 격자
grid = [sp.Rational(n, 2) for n in range(-12, 13)]
cnt = {}
for p, q in itertools.combinations_with_replacement(grid, 2):
    f = fam_pq(p, q)
    n = len(disc_points(f))
    if p == 0 and q == 0: kind = 'B x^4'
    elif p == 0 or q == 0: kind = 'A 원점 정지변곡'
    elif p == q: kind = 'D 원점 밖 정지변곡'
    else:
        vals = sorted([0, f.subs(x, p), f.subs(x, q)])
        # 극소 두 개의 높이가 같은가
        mins = [v for v, c in [(f.subs(x, c), c) for c in (0, p, q)] if sp.diff(f, x, 2).subs(x, c) > 0]
        kind = 'C 극소 높이 같음' if len(set(mins)) == 1 else 'C 일반'
    cnt.setdefault(kind, set()).add(n)
for a_ in range(-6, 7):
    for b_ in range(1, 40):
        if 9 * a_**2 < 32 * b_:
            f = sp.expand(x**4 + a_ * x**3 + b_ * x**2)
            cnt.setdefault('E 임계점 0 하나', set()).add(len(disc_points(f)))
for k_, v in cnt.items():
    print('  ', k_, '→ 불연속점 개수', sorted(v))
assert cnt['A 원점 정지변곡'] == {3} and cnt['D 원점 밖 정지변곡'] == {3}
assert cnt['C 일반'] == {7} and cnt['C 극소 높이 같음'] == {5}
assert cnt['B x^4'] == {1} and cnt['E 임계점 0 하나'] == {1}
print('  (가) 불연속점 3개 ⇔ 정지 변곡점이 있음 (A: 원점, D: 원점 밖) 확인')

# (2) 두 가족을 기호로: A f=x^3(x+a) , D f'=4x(x-r)^2
a, r = sp.symbols('a r', real=True, nonzero=True)
fA = x**3 * (x + a)
fD = sp.expand(x**4 - sp.Rational(8, 3) * r * x**3 + 2 * r**2 * x**2)
# A: 불연속점 0(h=1), -a(h=1), -3a/4(h=0)  /  D: 0(h=0), r(h=1), -r/3(h=1)
for av in [-8, -6, -4, -1, 2, 5, sp.Rational(-7, 3)]:
    dp = disc_points(fA.subs(a, av))
    assert [t for t, _ in dp] == sorted([0, -av, sp.Rational(-3, 4) * av], key=float), (av, dp)
    for t, (L, v, R) in dp:
        assert (L, R) == (2, 2) and v == (0 if t == sp.Rational(-3, 4) * av else 1)
for rv in [6, -18, 1, -2, sp.Rational(5, 2)]:
    dp = disc_points(fD.subs(r, rv))
    assert [t for t, _ in dp] == sorted([0, rv, -sp.Rational(1, 3) * rv], key=float), (rv, dp)
    for t, (L, v, R) in dp:
        assert (L, R) == (2, 2) and v == (0 if t == 0 else 1)
print('  A: 불연속점 {0, -3a/4, -a} (h=1,0,1) / D: 불연속점 {r, 0, -r/3} (h=1,0,1) 확인')

# (3) (나) t=6 이 불연속점 + f(1)<1
cands = []
for av in sp.solve(sp.Eq(-sp.Rational(3, 4) * a, 6), a) + sp.solve(sp.Eq(-a, 6), a):
    cands.append(('A', av, sp.expand(fA.subs(a, av))))
for rv in sp.solve(sp.Eq(r, 6), r) + sp.solve(sp.Eq(-r / 3, 6), r):
    cands.append(('D', rv, sp.expand(fD.subs(r, rv))))
good = []
for kind, v, f in cands:
    f1 = f.subs(x, 1)
    dp = [t for t, _ in disc_points(f)]
    ok = (len(dp) == 3) and (6 in dp) and f1 < 1
    print('  ', kind, v, 'f =', sp.factor(f), ' 불연속점', dp, ' f(1) =', f1, '채택' if ok else '탈락')
    if ok: good.append(f1)
assert sorted(good) == [-7, -5]
ans17 = sum(good)
print('  가능한 모든 f(1)의 합 =', ans17)
assert ans17 == -12

# (4) 수치 직접 확인: h(t)를 촘촘히 계산해 불연속점 위치를 찾음
import numpy as np
def h_num(fc, t):
    c = np.polyval(fc, t)
    roots = np.roots(np.polysub(fc, [0, 0, 0, 0, c]))
    dfc = np.polyder(fc)
    n = 0
    for z in roots:
        if abs(z.imag) < 1e-7:
            # 단순근: 미분계수가 0이 아니고 같은 근이 둘이 아님
            same = sum(abs(z - w) < 1e-4 for w in roots)
            if same == 1: n += 1
    return n
for fexpr in [x**3 * (x - 8), x**3 * (x - 6)]:
    fc = [float(c) for c in sp.Poly(fexpr, x).all_coeffs()]
    ts = np.round(np.arange(-3, 11, 0.01), 6)
    hv = [h_num(fc, t) for t in ts]
    jumps = sorted(set(round(ts[i], 2) for i in range(1, len(ts) - 1) if hv[i] != hv[i - 1] or hv[i] != hv[i + 1]))
    print('   수치', sp.factor(fexpr), '값이 튀는 t:', jumps)

# 선지
ch17 = [-12, -7, -5, 50, 742]
assert ch17 == sorted(ch17) and ch17.index(ans17) == 0
# 오답 근거: -7 (꼭짓점이 아닌 원상 u 누락: m=6만), -5 (m=6 누락), 50 (정지점만 보고 f(1)<1 미확인: -7+57), 742 (f(1)<1 미확인: 네 함수 모두)
assert -7 + 57 == 50 and -7 - 5 + 57 + 697 == 742
print('17번 통과: 정답 ① -12')

# =====================================================================
# 18번 (D70 구조 변경)
#  f(x)=x^3-2ax^2 (정수 a≠0)
#  조건: 두 할선 기울기의 곱<0 인 세 실수 x1,x2,x3 이 존재하고, f(x1),f(x2),f(x3)이 모두 열린구간 (k, k+3/2)에 속함
#  ⇔ (k, k+3/2) 가 [극솟값, 극댓값] 과 만남 ⇔ m-3/2 < k < M
#  정수 k의 개수가 10 이하인 모든 정수 a: {1,-1,2} → f'(10)=300-40a 의 합 820 (정답 ③)
# =====================================================================
print('=== 18번 ===')
L = sp.Rational(3, 2)

def ext_vals(av):
    f = x**3 - 2 * av * x**2
    v = [f.subs(x, 0), f.subs(x, sp.Rational(4, 3) * av)]
    return min(v), max(v)

def ks_exact(av):
    m, M = ext_vals(av)
    lo = sp.floor(m - L) + 1          # k > m - 3/2
    hi = sp.ceiling(M) - 1            # k < M
    return list(range(int(lo), int(hi) + 1))

def ks_numeric(av, step=1e-3):
    """정의대로: f값이 띠 (k,k+3/2)에 드는 x 표본(정렬)에서 증가와 감소가 모두 나타나는가"""
    m, M = [float(v) for v in ext_vals(av)]
    R = 3 * abs(av) + 4
    xs = np.arange(-R, R, step)
    fs = xs**3 - 2 * av * xs**2
    out = []
    for k_ in range(int(math.floor(m)) - 4, int(math.ceil(M)) + 4):
        sel = (fs > k_) & (fs < k_ + 1.5)
        d = np.diff(fs[sel])
        if (d > 1e-12).any() and (d < -1e-12).any():
            out.append(k_)
    return out

counts = {}
for av in [v for v in range(-6, 7) if v != 0]:
    ke, kn = ks_exact(av), ks_numeric(av)
    assert ke == kn, (av, ke[:3], kn[:3], ke[-3:], kn[-3:])
    counts[av] = len(ke)
print('  정수 k의 개수 N(a):', counts)
# |a|>=3 이면 N(a)>=33 (M=32|a|^3/27 증가)
for av in range(3, 60):
    assert len(ks_exact(av)) >= 33 and len(ks_exact(-av)) >= 33
sel = sorted(av for av, n in counts.items() if n <= 10)
print('  N(a)<=10 인 a:', sel)
assert sel == [-1, 1, 2]
fp10 = lambda av: 300 - 40 * av
ans18 = sum(fp10(av) for av in sel)
print("  f'(10)의 합 =", ans18)
assert ans18 == 820
# 경계 확인: a=2 에서 k=-11 은 띠 (-11,-19/2)가 극솟값 -256/27 보다 아래 → 불가, a=-2 에서 k=-1,0 가능
assert -11 not in ks_exact(2) and sp.Rational(-19, 2) < sp.Rational(-256, 27)
assert ks_exact(-2)[:2] == [-1, 0] and len(ks_exact(-2)) == 11 and len(ks_exact(2)) == 10
# 선지와 오답 근거
ch18 = [480, 600, 820, 980, 1200]
assert ch18 == sorted(ch18) and ch18.index(ans18) == 2
assert sum(map(fp10, [1, 2])) == 480            # a<0 누락
assert sum(map(fp10, [1, -1])) == 600           # a=2 의 k=-11 포함(또는 k=0 포함)으로 N(2)=11 처리
assert sum(map(fp10, [1, -1, -2])) == 980       # a=2 탈락 + a=-2 에서 k=-1 누락
assert sum(map(fp10, [1, -1, 2, -2])) == 1200   # a=-2 도 10개로 셈(부호 대칭 가정)
# 원본 판정(극점이 x구간에 있음)으로 풀면 N(a)는 항상 2~3 → 모든 a가 조건을 만족해 답이 정해지지 않음
print('18번 통과: 정답 ③ 820')

# =====================================================================
# 부품 파일과 대조 (정답 번호·선지·수식 글꼴 제약)
# =====================================================================
import os, re
ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p6.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
for no, ans, ch in [(17, ans17, ch17), (18, ans18, ch18)]:
    it = IT[no]
    vals = [sp.sympify(c) for c in it['choices']]
    assert vals == ch and vals == sorted(vals), no
    assert vals[it['ans'] - 1] == ans, no
    assert it['ans'] == {17: 1, 18: 3}[no]
    text = it['body'] + ''.join(v for _, v in it.get('cond', [])) + it.get('after', '')
    for mth in re.findall(r'\\\((.*?)\\\)', text, flags=re.S):
        bare = re.sub(r'\\[A-Za-z]+|&[a-z]+;', '', mth)
        assert not re.search(r'[loWVYZ]', bare), (no, mth)
print('부품 대조 통과: 17번 ①, 18번 ③')
