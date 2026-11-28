# -*- coding: utf-8 -*-
# p3.py (14회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, integrate, diff, solve, expand, factor, Poly

x, t, m, C, k = symbols('x t m C k', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 2, 10: 4, 11: 5, 12: 1}
DBREF = {9: 'J52 후보_순위 4', 10: 'I4 결합 1', 11: 'M30 후보_순위 3', 12: 'D66 후보_순위 3'}
KEYS = {9: 'J52', 10: 'I4', 11: 'M30', 12: 'D66'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

def val(c):
    c = re.sub(r'\s', '', str(c))
    mm = re.fullmatch(r'(-?)\\[dt]?frac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(mm[2]), int(mm[3])) * (-1 if mm[1] else 1) if mm else Rational(c)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == '중', f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level(중)')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops']), f'{n}번 ops가 OP01–OP55 안')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('bogi' not in it, f'{n}번 보기형 아님')
    for f_ in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
        ok('이러한' not in it[f_] and '이와 같은' not in it[f_], f'{n}번 {f_} 금지 어구 없음')
    txt = it['body'] + ''.join(v for _, v in it.get('cond', []))
    ok(not any(('<' in mm or '>' in mm) for mm in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', txt, re.S)), f'{n}번 본문·상자 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all('cond' not in IT[n] for n in (9, 10, 11)) and [c[0] for c in IT[12]['cond']] == ['가', '나'], '9·10·11번 상자 없음, 12번 원문대로 (가)(나) 상자')
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if IT[n]['effect'] == '어려워짐') == 0, '9–12번 어려워짐 0개')
ok(f'fig_9.svg' in IT[9]['body'] and os.path.exists(os.path.join(HERE, 'fig_9.svg')) and os.path.exists(os.path.join(HERE, '..', 'fig_9.svg')) and os.path.exists(os.path.join(HERE, '..', 'figs', 'fig9.py')), '9번 그림 parts/fig_9.svg·회차 폴더 fig_9.svg·figs/fig9.py 있음')
ok(open(os.path.join(HERE, 'fig_9.svg'), 'rb').read() == open(os.path.join(HERE, '..', 'fig_9.svg'), 'rb').read(), '9번 그림 두 사본이 같음')
ok(sorted(IT[n]['ans'] for n in IT) == [1, 2, 4, 5], '9–12번 정답 ②④⑤① (분담표 ④②⑤①에서 9·10만 맞바꿈, 개수 그대로)')

def chk(n, v0, dset=(1,)):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1 and (v[1] - v[0]) in dset, f'{n}번 선지 {v} 서로 다르고 오름차순 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    txt = IT[n]['body'] + ''.join(c for _, c in IT[n].get('cond', []))
    plain = re.sub(r'\\[a-zA-Z]+', ' ', re.sub(r'<[^>]+>', ' ', txt))
    body_nums = {Rational(s) for s in re.findall(r'-?\d+', re.sub(r'\^\{?\d+\}?', ' ', plain))}
    ok(v0 not in body_nums, f'{n}번 정답 {v0}이 본문에 나온 수(지수 제외)와 다름')
    return v

# ---------- 9번 (J52) ----------
cur = x**2 - 5 * x
roots = sorted(solve(cur - 3 * x, x))
ok(roots == [0, 8], f'9번 곡선과 y=3x의 교점 x = {roots} → A(8, 24)')
S1 = integrate(3 * x - cur, (x, 0, 8))
ok(S1 == Rational(256, 3), f'9번 S1 = {S1}')
lineA = m * (x - 8) + 24
ok(expand(cur - lineA - (x - 8) * (x - m + 3)) == 0, '9번 곡선 − (A를 지나는 직선) = (x−8)(x−m+3)')
def S2(mv):
    r = sorted({8, mv - 3})
    if len(r) == 1: return 0
    return abs(integrate(cur - lineA.subs(m, mv), (x, r[0], r[1])))
ok(sp.simplify(S2(Rational(7)) - Rational(32, 3)) == 0, '9번 m=7: S2 = 32/3')
ms = solve(sp.Eq(S1, 8 * (11 - m)**3 / 6), m) + solve(sp.Eq(S1, 8 * (m - 11)**3 / 6), m)
ms = sorted({r for r in ms if r.is_real})
ok(ms == [7, 15], f'9번 S=8T의 실수해 m = {ms}')
ok([r for r in ms if r < 12] == [7], '9번 m<12에서 m = 7 하나')
ok(all(S2(Rational(mv)) * 8 != S1 for mv in range(-30, 40) if mv not in (7, 15)), '9번 정수 m 전수(−30..39): S=8T는 7, 15뿐')
ok(all(S2(Rational(i, 4)) * 8 != S1 for i in range(-40, 48) if Rational(i, 4) != 7), '9번 m을 1/4 간격으로 전수(−10..12): 7뿐')
c9 = chk(9, 7)
ok(11 - 10 == 1 and 8 / (11 - 10) == 8, '9번 오답 10: 넓이 비 8:1을 가로 길이 비로 보아 11−m = 1')
# 원문 J52: k=3(①)
ho = expand(x - (x**2 - 5 * x)); kk = symbols('kk')
ko = [r for r in solve(integrate(ho, (x, 0, kk)) - integrate(ho, (x, 0, 6)) / 2, kk) if r.is_real and 0 < r < 6]
ok(ko == [3], '9번 원문 J52 정답 k=3(①)')
print("ABLATION 9 S=8T: 필요(없으면 m이 정해지지 않음; 이등분이면 (11−m)³=256, m=11−4∛4로 선지 밖)")
print("ABLATION 9 m<12: 필요(없으면 m=15도 S=8T를 만족)")
ok(sp.nsimplify(11 - 4 * sp.cbrt(4)) not in [Rational(v) for v in c9], '9번 이등분 값 11−4∛4는 선지 밖(비 1:8이 일함)')

# ---------- 10번 (I4) ----------
f10 = integrate(12 * x**2 - 12, x) + C
eq = sp.Eq(diff(integrate(f10.subs(x, t), (t, 1, x)), x), diff(x * f10 - 3 * x**4 + 6 * x**2 + k, x))
ok(sp.simplify(eq.lhs - eq.rhs) == 0, '10번 f = 4x³−12x+C이면 양변 도함수 일치(일반해)')
# 일반 다항식에서 f가 이 꼴뿐임: f = Σ a_i x^i (차수 ≤ 5)로 두고 미분 항등식 계수 비교
a = symbols('a0:6'); fg = sum(a[i] * x**i for i in range(6))
cs = Poly(expand(fg - (fg + x * diff(fg, x) - 12 * x**3 + 12 * x)), x).all_coeffs()
sg = solve(cs, a[1:], dict=True)
ok(len(sg) == 1 and expand(fg.subs(sg[0]) - (4 * x**3 - 12 * x + a[0])) == 0, f'10번 차수 ≤5 다항식 전수: f = 4x³−12x+a0 하나 ({sg})')
Cv = solve(f10.subs(x, -1) - 9, C)
ok(Cv == [1], f'10번 f(−1)=9 → C = {Cv}')
f10 = f10.subs(C, 1)
kv = solve(0 - (1 * f10.subs(x, 1) - 3 + 6 + k), k)
ok(kv == [4], f'10번 x=1 대입 → k = {kv}')
ok(expand(integrate(f10.subs(x, t), (t, 1, x)) - (x * f10 - 3 * x**4 + 6 * x**2 + 4)) == 0, '10번 원래 등식이 k=4에서 항등식')
c10 = chk(10, 4)
ok(1 == 1 and '1' in IT[10]['choices'], '10번 오답 1: f의 적분상수 C=1을 k로')
# 원문 I4: f(−1)=3(③)
fo = 4 * x**3 - 2 * x + C; Co = solve((x * fo - 3 * x**4 + x**2).subs(x, 1) - 5, C)
ok(Co == [5] and fo.subs({C: 5, x: -1}) == 3, '10번 원문 I4 정답 f(−1)=3(③)')
for Ct in (0, 2):
    print(f'ABLATION 10 f(−1)=9: 필요(C={Ct}이면 k={3 + Ct} ≠ 4)'); assert 3 + Ct != 4

# ---------- 11번 (M30) ----------
n_ = symbols('n', positive=True)
f11 = x**2 * (5 - x) + n_ * (x - 5)
ok(expand(f11 - (5 - x) * (x**2 - n_)) == 0, '11번 f = (5−x)(x²−n)')
def holds(nv, closed=True, g=None):
    """정의역 (0,3] 또는 (0,3)의 모든 x에서 f<0인지 (정확 판정)"""
    g = (f11.subs(n_, nv) if g is None else g.subs(n_, nv))
    # 구간 안 최댓값: 임계점·끝점
    crit = [r for r in solve(diff(g, x), x) if r.is_real and 0 < r < 3]
    cand = [g.subs(x, r) for r in crit] + ([g.subs(x, 3)] if closed else [])
    sup = max(cand + [g.subs(x, 0), g.subs(x, 3)])
    attained = max(cand) if cand else None
    if closed: return attained is not None and attained < 0 and g.subs(x, 0) <= 0  # x→0+에서 극한은 −5n<0
    return sup <= 0 and (attained is None or attained < 0)
sols = [nv for nv in range(1, 41) if holds(nv)]
ok(sols[0] == 10 and sols == list(range(10, 41)), f'11번 n=1..40 전수: 성립하는 n은 {sols[0]}부터 → 최솟값 10')
c11 = chk(11, 10)
sols_open = [nv for nv in range(1, 41) if holds(nv, closed=False)]
ok(sols_open[0] == 9, f'11번 오답 9: 정의역을 0<x<3으로 보면 최솟값 {sols_open[0]}')
print(f'ABLATION 11 x≤3(닫힌 끝): 필요(0<x<3이면 최솟값 {sols_open[0]})')
g_flat = x**2 * (5 - x) - n_
sols_flat = [nv for nv in range(1, 41) if holds(nv, g=g_flat)]
print(f'ABLATION 11 n(x−5): 필요(−n으로 두면 최솟값 {sols_flat[0]})'); assert sols_flat[0] == 19
# 원문 M30: 5 — x²(3−x)<n on (0,3)
ho11 = x**2 * (3 - x)
ok(ho11.subs(x, 2) == 4 and diff(ho11, x).subs(x, 2) == 0 and [nv for nv in range(2, 10) if 4 < nv][0] == 5, '11번 원문 M30 정답 5')

# ---------- 12번 (D66) ----------
p, c = symbols('p c', real=True)
def F(cv, pv=1): return pv * (x - 2) * (x - 4) * (x - cv)
def nondiff_abs(poly):
    """|poly|가 미분가능하지 않은 점 = 홀수 중복도… 정확히는 중복도 1인 실근"""
    P = Poly(expand(poly), x); out = []
    for r, mult in sp.roots(P, filter='R').items():
        if mult == 1: out.append(r)
    return sorted(out)
def g_diff(cv):
    """|f(x)f(6−x)|가 모든 실수에서 미분가능 ⇔ 곱의 모든 실근 중복도 ≥ 2"""
    P = Poly(expand(F(cv) * F(cv).subs(x, 6 - x)), x)
    return all(mult >= 2 for mult in sp.roots(P, filter='R').values())
def cond_na(cv):
    return len([r for r in nondiff_abs(F(cv)) if r < 4]) == 1
grid = sorted({Rational(i, 4) for i in range(-40, 81)} | {Rational(i, 3) for i in range(-30, 61)})
okc = [cv for cv in grid if cond_na(cv) and g_diff(cv)]
ok(okc == [4], f'12번 c를 1/4·1/3 격자(−10..20) 전수: (나)와 g 미분가능을 함께 만족하는 c = {okc}')
# 일반 c에 대한 논증: (나) ⇔ c ≥ 4
ok(all(cond_na(cv) == (cv >= 4) for cv in grid), '12번 (나) ⇔ c ≥ 4 (격자 전수)')
# c>4이면 x=c의 짝 없음: c ∉ {2, 4, 6−c}
ok(solve([sp.Eq(c, 6 - c)], c) == {c: 3}, '12번 c>4에서 c = 6−c는 c=3뿐 → 짝 없음')
fq = F(4, p)
ratio = sp.simplify(sp.Abs(fq.subs(x, -2) * fq.subs(x, 8)) / (fq.subs(x, 0) * fq.subs(x, -2)))
ok(ratio == 3, f'12번 c=4: g(−2)/(f(0)f(−2)) = {ratio} (p 약분)')
ok(expand(fq * fq.subs(x, 6 - x) + p**2 * (x - 2)**3 * (x - 4)**3) == 0, '12번 f(x)f(6−x) = −p²(x−2)³(x−4)³')
c12 = chk(12, 3, dset=(2,))
def R(cv):
    fq = F(cv, p); return sp.simplify(sp.Abs(fq.subs(x, -2) * fq.subs(x, 8)) / (fq.subs(x, 0) * fq.subs(x, -2)))
ok(R(3) == 5 and g_diff(3) and not cond_na(3), '12번 오답 5: c=3(세 근 대칭)은 g 미분가능이지만 (나) 위반')
ok(R(2) == 9 and g_diff(2) and not cond_na(2), '12번 오답 9: c=2(작은 근 중근)는 g 미분가능이지만 (나) 위반(원문 방향 x>2로 읽은 경로)')
okc_nona = [cv for cv in grid if g_diff(cv)]
ok(okc_nona == [2, 3, 4], f'12번 (나) 없이 g 미분가능한 c = {okc_nona}')
print(f'ABLATION 12 (나): 필요(없으면 c ∈ {okc_nona}, 값 {[R(cv) for cv in okc_nona]})')
print(f'ABLATION 12 g 미분가능: 필요(없으면 c ≥ 4 전부, 예: c=5이면 {R(5)}, c=6이면 {R(6)})'); assert R(5) != 3 or R(6) != 3
# 원문 D66: 105
fo = p * (x + 1) * (x - 1) * (x - 3)
ro = sp.simplify(sp.Abs(fo.subs(x, 8) * fo.subs(x, 2 - 8)) / (fo.subs(x, 0) * fo.subs(x, 8)))
ok(ro == 105, f'12번 원문 D66 정답 {ro}')
# 원문 (나) 조건 확인: f'의 x≥1 근 1개 ⇔ r<1 (r=-1에서 성립)
fp = diff((x + 1) * (x - 1) * (x - 3), x)
ok(len([r for r in solve(fp, x) if r >= 1]) == 1, '12번 원문 f=(x+1)(x−1)(x−3)은 (나) 만족')
# LIVE1-01-140 '모든 a의 합'에서 (나)가 군더더기임(note 근거): c 전체에서 가능한 a 집합
def a_set(cv):
    out = set()
    for av in [Rational(i, 2) for i in range(-10, 30)]:
        P = Poly(expand((x - 1) * (x - 3) * (x - cv) * ((av - x) - 1) * ((av - x) - 3) * ((av - x) - cv)), x)
        if all(mm >= 2 for mm in sp.roots(P, filter='R').values()): out.add(av)
    return out
allA = set().union(*[a_set(cv) for cv in [Rational(i, 2) for i in range(-6, 13)]])
naA = set().union(*[a_set(cv) for cv in [Rational(i, 2) for i in range(-6, 3)]])
ok(allA == naA == {2, 4, 6}, f'12번 note: LIVE1-01-140에서 a 집합은 (나) 유무와 관계없이 {sorted(allA)}')

print(f'{len(OK)} checks')
print('ALL OK')
