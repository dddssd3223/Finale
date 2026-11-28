# -*- coding: utf-8 -*-
# 17번 후보 A17 (M31 킬러 설계A 변형 2판: 곱 g(t)·g(c-t), p(c)=불연속점 개수, p(c)=4 인 정수 c 의 개수) 검증 · author='claude'
import sympy as sp, os, sys
from fractions import Fraction as Fr
x = sp.symbols('x', real=True)
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]
e = Fr(1, 10**6)


def g_exact(F, tv):
    tv = sp.nsimplify(tv)
    if tv < 0: return 0
    return len(set(sp.real_roots(sp.Poly(F - tv, x))) | set(sp.real_roots(sp.Poly(F + tv, x))))


def g_tab(P, Q):
    def g(t):
        if t < 0: return 0
        if t == 0: return 3
        if t < P: return 6
        if t == P: return 5
        if t < Q: return 4
        if t == Q: return 3
        return 2
    return g


def p_of(c, g, P, Q, op=lambda u, v: u * v, refl=True):
    h = (lambda t: op(g(t), g(c - t))) if refl else (lambda t: op(g(t), g(t - c)))
    cands = {Fr(0), Fr(P), Fr(Q)} | ({c - Fr(v) for v in (0, P, Q)} if refl else {c + Fr(v) for v in (0, P, Q)})
    return len([t for t in cands if not (h(t - e) == h(t) == h(t + e))])


def scan(g, P, Q, **kw):
    """c 전수: 개수가 바뀌는 c 는 0 과 겹침 값(u+v, u,v∈{0,P,Q})·그 사이뿐 → 1/4 간격 + 특수값"""
    sp_ = sorted({Fr(u) + Fr(v) for u in (0, P, Q) for v in (0, P, Q)} | {Fr(u) - Fr(v) for u in (0, P, Q) for v in (0, P, Q)})
    cs = set(sp_) | {Fr(n, 4) for n in range(-200, 260)}
    return {c: p_of(c, g, P, Q, **kw) for c in cs}


# ---------- 1) f, g
f = x**3 - 3 * x**2 - 9 * x + 8
assert sp.solve(sp.diff(f, x), x) == [-1, 3] and f.subs(x, -1) == 13 and f.subs(x, 3) == -19
g = g_tab(13, 19)
for tv in (-1, 0, 1, 12, 13, 14, 18, 19, 20, 50):
    assert g_exact(f, tv) == g(Fr(tv)), tv
print('f 극댓값 13, 극솟값 -19; g: 0,3,6,5,4,3,2 (불연속 0, 13, 19) — 근 개수 직접 확인')

# ---------- 2) p(c) 전수
Pc = scan(g, 13, 19)
four = sorted(c for c, v in Pc.items() if v == 4)
assert [c for c in four if c.denominator == 1] == [14, 15, 16, 17, 18, 19, 32]
assert all((13 < c <= 19) or c == 32 for c in four)
assert Pc[Fr(13)] == 2 and Pc[Fr(0)] == 1 and Pc[Fr(-1)] == 0 and Pc[Fr(26)] == 5 and Pc[Fr(38)] == 5 and Pc[Fr(20)] == 6
assert Pc[Fr(27, 2)] == 4 and Pc[Fr(37, 2)] == 4      # 실수 c 는 13<c≤19 전체
ANS = len([c for c in four if c.denominator == 1])
assert ANS == 7
# 겹친 점은 합쳐질 뿐 지워지지 않음 (c=26, t=13: 24, 25, 24)
h26 = lambda t: g(t) * g(26 - t)
assert (h26(13 - e), h26(Fr(13)), h26(13 + e)) == (24, 25, 24)
h32 = lambda t: g(t) * g(32 - t)
assert len({h32(13 - e), h32(Fr(13)), h32(13 + e)}) > 1
print(f'p(c)=4 ⇔ 13<c≤19 또는 c=32 → 정수 c: 14..19, 32 → {ANS}개; c=26,38 은 5개, c=13 은 2개')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {1}
print('정답 7 = 선지 ②, 선지 6..10 공차 1')

# ---------- 3) 오답
w6 = ANS - 1        # c=32 놓침
w8 = ANS + 1        # c=13 을 4개로 셈(합쳐짐 놓침): 0, 0, 13, 13
assert Pc[Fr(13)] != 4
assert {str(w6), str(w8)} == set(IT['wrongs']) and all(w in ch for w in IT['wrongs'])
assert ANS not in (3, 9, 8, 13, 19, 4, 36)
print('오답 근거 OK: 6(c=32 놓침) · 8(c=13 합쳐짐 놓침); 정답 7 은 문항 속 수·원문 답과 다름')

# ---------- 4) 원문 M31: 36
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['M31']; assert o[2] == '⑤' and o[1][4] == '36'
f0 = x**3 - 3 * x**2 - 9 * x + 10
g0 = g_tab(15, 17)
for tv in (0, 1, 15, 16, 17, 18): assert g_exact(f0, tv) == g0(Fr(tv))
ho = lambda t: g0(t) - g0(t - 2)
dpo = sorted(t for t in {Fr(v) for v in (0, 2, 15, 17, 19)} if not (ho(t - e) == ho(t) == ho(t + e)))
assert sum(dpo) == 36
print('원문 M31 OK: 불연속 0, 2, 15, 19 (17 상쇄) → 36')

# ---------- 5) 핵심 한 줄: 원문 원리(겹친 같은 크기 점프 상쇄) 불통
# 곱에서 두 불연속점이 겹치는 모든 경우(0≤t≤c 안)에서 불연속이 남는다
for c in sorted({Fr(u) + Fr(v) for u in (13, 19) for v in (13, 19)}):
    h = lambda t, c=c: g(t) * g(c - t)
    for t0 in {Fr(13), Fr(19)} & {c - 13, c - 19}:
        assert not (h(t0 - e) == h(t0) == h(t0 + e)), (c, t0)
print('핵심: 곱에서는 겹친 점의 점프가 지워지지 않음(원문 원리 불통), 0 인 인수가 다른 쪽 점프를 지움(새 판단)')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})'); assert res != ANS
def int_count(Pd, v=4): return len([c for c, k in Pd.items() if k == v and c.denominator == 1])
S = scan(g, 13, 19, op=lambda u, v: u + v)
ablation('곱 × (→ 합 +)', int_count(S), f'정수 c = {sorted(int(c) for c, k in S.items() if k == 4 and c.denominator == 1)}')
T_ = scan(g, 13, 19, refl=False)
ablation('반사 g(c-t) (→ g(t-c))', int_count(T_), '')
g0c = scan(g0, 15, 17)
ablation('f 의 상수항 8 (→ 원문 10)', int_count(g0c), '높이 15, 17')
ablation("'정수' c (→ 실수 c)", '무수히 많음(13<c≤19)', '')
print('ALL OK')
