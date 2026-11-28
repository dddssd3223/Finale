# -*- coding: utf-8 -*-
# 17번 후보 A17 (M32: (x-9)f>=0, f(0)=0, 방정식 f(x)-(x-k+2)f'(k)=0의 실근 3개인 정수 k의 개수) 검증 · author='claude'
import sympy as sp, os, sys
x, k, r = sp.symbols('x k r', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def nroots(poly):
    """다항식(x)의 서로 다른 실근의 개수(정확)"""
    P = sp.Poly(sp.expand(poly), x)
    return len(set(sp.real_roots(P)))


def count_int(f, shift, want=3, lo=-60, hi=60):
    """방정식 f(x)-(x-k+shift)f'(k)=0 의 서로 다른 실근이 want개인 정수 k 목록(범위 끝에서도 성립하면 무한으로 봄)"""
    fp = sp.diff(f, x)
    out = [kv for kv in range(lo, hi + 1) if nroots(f - (x - kv + shift) * fp.subs(x, kv)) == want]
    if out and (out[0] == lo or out[-1] == hi):
        return None
    return out


# ---------- 1) (가)(나) → f = x^2(x-9) 유일
# (가)에서 f(9)=0(부호가 바뀜), (나) f(0)=0 → f = x(x-9)(x-r). (x-9)f = x(x-r)(x-9)^2 >= 0 ⇔ x(x-r) >= 0 ⇔ r=0
for rv in [R(n, 4) for n in range(-40, 41)]:
    g = x * (x - rv)
    ok = all(g.subs(x, t) >= 0 for t in [R(n, 8) for n in range(-80, 81)])
    assert ok == (rv == 0), rv
f = x**2 * (x - 9); fp = sp.diff(f, x)
print('f = x^2(x-9) 유일 (r 눈금 전수)')

# ---------- 2) 풀이 줄 검산
h = f - (x - k + 2) * fp.subs(x, k)
assert sp.factor(sp.diff(h, x)) == sp.factor(3 * (x - k) * (x + k - 6))
hk = sp.factor(h.subs(x, k)); hs = sp.factor(sp.expand(h.subs(x, 6 - k)))
assert sp.expand(hk - k * (k - 3) * (k - 12)) == 0
assert sp.expand(hs - (k - 6) * (k - 3) * (5 * k - 6)) == 0
assert sp.expand(fp.subs(x, 6 - k) - fp.subs(x, k)) == 0
S3 = sp.solve_univariate_inequality(sp.expand(hk * hs) < 0, k, relational=False)
assert S3 == sp.Union(sp.Interval.open(0, R(6, 5)), sp.Interval.open(6, 12)), S3
# k=3: h' = 3(x-3)^2 → 실근 1개 (변곡점에서의 접선)
assert nroots(h.subs(k, 3)) == 1 and sp.factor(h.subs(k, 3)) == sp.factor((x - 3)**3)
# 끝점: 실근 2개
for kv in (0, R(6, 5), 6, 12):
    assert nroots(h.subs(k, kv)) == 2, kv
# 실수 k 눈금 전수: 실근 3개 ⇔ 0<k<6/5 또는 6<k<12
for kv in [R(n, 10) for n in range(-50, 160)]:
    assert (nroots(h.subs(k, kv)) == 3) == bool(S3.contains(kv)), kv
print('h(k)=k(k-3)(k-12), h(6-k)=(k-6)(k-3)(5k-6), 실근 3개 ⇔', S3, '(k=3은 실근 1개)')

# ---------- 3) 답
ints = count_int(f, 2)
assert ints == [1, 7, 8, 9, 10, 11], ints
ANS = len(ints)
print('정수 k =', ints, '→ 개수', ANS)

# ---------- 4) 선지
ch = IT['choices']; vals = [int(c) for c in ch]
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 1
assert len(set(vals)) == 5 and len({vals[i + 1] - vals[i] for i in range(4)}) == 1 and vals == sorted(vals) and vals[1] - vals[0] == 1
print('정답 = 선지 ①, 선지', vals, '공차 1 오름차순')

# ---------- 5) 오답
w_ge2 = [kv for kv in range(-60, 61) if nroots(h.subs(k, kv)) >= 2]        # 끝점(실근 2개)까지 셈
assert w_ge2 == [0, 1, 6, 7, 8, 9, 10, 11, 12] and len(w_ge2) == 9
S_le = sp.solve_univariate_inequality(sp.expand(hk * hs) <= 0, k, relational=False)
w_le = [kv for kv in range(-60, 61) if S_le.contains(kv)]                     # 곱 <= 0 (k=3 포함)
assert 3 in w_le and len(w_le) == 10
assert set(IT['wrongs']) == {'9', '10'} and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 9(끝점 0, 6, 12 포함), 10(곱 <= 0, k=3까지)')
assert ANS not in {1, 9, 0, 2, 3} and ANS != 19
print('정답은 본문의 수(1, 9, 0, 2, 3)·원문 답 19와 다름')

# ---------- 6) 원문 M32: 19
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['M32']; assert o[2] == '19'
f0 = x**2 * (x - 4); f0p = sp.diff(f0, x)
ks = set()
for kv in [R(n, 6) for n in range(-30, 40)]:
    if nroots(f0 - x * f0p.subs(x, kv)) == 2:
        ks.add(kv)
cs = set()
for c in (0, -4):
    cs |= set(sp.solve(3 * k**2 - 8 * k - c, k))
assert ks <= cs and all(nroots(f0 - x * f0p.subs(x, c)) == 2 for c in cs)
s = sum(cs); assert s == R(16, 3) and s.p + s.q == 19
print('원문 M32 OK: k = 0, 8/3, 2/3, 2, 합 16/3, p+q=19')
# 원문 원리 줄 불통: 직선이 원점을 지나지 않아 x로 묶이지 않음(k≠2이고 f'(k)≠0이면 h(0)≠0)
assert sp.factor(h.subs(x, 0)) == sp.factor((k - 2) * fp.subs(x, k))
assert h.subs({x: 0, k: 7}) != 0
print('원문 줄 불통: h(0)=(k-2)f\'(k)≠0 (정답 구간 안의 k)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res):
    print(f'ABLATION 17 {cname}: 필요({res})'); assert res != ANS


def ans_of(f_, shift=2, want=3):
    L = count_int(f_, shift, want)
    return '무한' if L is None else len(L)


# (가) 삭제: f(0)=0인 최고차 1 삼차함수 여럿 → 답이 갈림
alts = {str(g): ans_of(g) for g in (x**3, x**2 * (x - 4), x * (x - 3) * (x - 9), x**2 * (x - 9))}
assert len(set(alts.values())) > 1
ablation('(가) 부등식', f'정해지지 않음 {alts}')
# (나) 삭제: (x-9)f>=0 → f=(x-9)(x-c)^2 또는 (x-9)^3
alts = {str(g): ans_of(g) for g in ((x - 9)**3, (x - 9) * (x - 3)**2, (x - 9) * x**2)}
assert len(set(alts.values())) > 1
ablation('(나) f(0)=0', f'정해지지 않음 {alts}')
ablation('(가)의 9(→4)', ans_of(x**2 * (x - 4)))
ablation('직선의 +2(→0, 원점 대신 (k,0))', ans_of(f, 0))
ablation('직선의 +2(→1)', ans_of(f, 1))
ablation('직선의 +2(→3)', ans_of(f, 3))
ablation('개수 3(→2)', ans_of(f, 2, 2))
print('ALL OK')
