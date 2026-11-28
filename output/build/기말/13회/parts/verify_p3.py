# -*- coding: utf-8 -*-
# p3.py (13회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, integrate, diff, solve, expand, factor, sqrt

x, t = symbols('x t', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 3, 10: 5, 11: 1, 12: 3}
DBREF = {9: 'J50 후보_순위 3', 10: 'J21 v3_추가 1', 11: 'M39 예상밖 2', 12: 'D64 후보_순위 3'}
KEYS = {9: 'J50', 10: 'J21', 11: 'M39', 12: 'D64'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
OK = []

def ok(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    assert cond, msg
    OK.append(msg)

def val(c):
    c = re.sub(r'\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{(\d+)\}\{(\d+)\}', c)
    return Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1) if m else Rational(c)

# ---------- 공통 필드 ----------
assert sorted(IT) == [9, 10, 11, 12]
for n, it in IT.items():
    ok(it['ans'] == WANT[n] and it['db_ref'] == DBREF[n] and it['key'] == KEYS[n] and it['level'] == '중', f'{n}번 정답 번호 {it["ans"]}·db_ref·key·level(중)')
    ok(it['bunseok'] is False and it['effect'] in ('같음', '쉬워짐', '어려워짐') and it['precedent'] and it['ops'] and it['vtype'], f'{n}번 vtype·effect·bunseok·precedent·ops 있음')
    ok(all(re.fullmatch(r'OP(0[1-9]|[1-4]\d|5[0-5])', o) for o in it['ops']), f'{n}번 ops가 OP01–OP55 안')
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it and 'bogi' not in it, f'{n}번 상자 없음·보기형 아님')
    for f_ in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
        ok('이러한' not in it[f_] and '이와 같은' not in it[f_], f'{n}번 {f_} 금지 어구 없음')
    ok(not any(('<' in m or '>' in m) for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'], re.S)), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if IT[n]['effect'] == '어려워짐') == 0, '9–12번 어려워짐 0개')
for n in (9, 10):
    ok(f'fig_{n}.svg' in IT[n]['body'] and os.path.exists(os.path.join(HERE, f'fig_{n}.svg')) and os.path.exists(os.path.join(HERE, '..', f'fig_{n}.svg')) and os.path.exists(os.path.join(HERE, '..', 'figs', f'fig{n}.py')), f'{n}번 그림 parts/fig_{n}.svg·회차 폴더 fig_{n}.svg·figs/fig{n}.py 있음')
ok(sorted(IT[n]['ans'] for n in IT) == [1, 3, 3, 5], '9–12번 정답 ③⑤①③ (분담표 ③①⑤③에서 10·11만 맞바꿈, 개수 그대로)')

def chk(n, v0, dset=(1,)):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1 and (v[1] - v[0]) in dset, f'{n}번 선지 {v} 서로 다르고 오름차순 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    plain = re.sub(r'\\[a-zA-Z]+', ' ', re.sub(r'<[^>]+>', ' ', IT[n]['body']))
    body_nums = {Rational(s) for s in re.findall(r'-?\d+', re.sub(r'\^\{?\d+\}?', ' ', plain))}
    ok(v0 not in body_nums, f'{n}번 정답 {v0}이 본문에 나온 수(지수 제외)와 다름')
    return v

# ---------- 9번 (J50) ----------
a = symbols('a')
F9 = x**2 + 3; G9 = -Rational(1, 2) * x**2 + a * x + 3
sa = solve((F9 - G9).subs(x, 2), a)
ok(sa == [3], f'9번 x=2에서 만남 → a = {sa}')
d9 = expand((F9 - G9).subs(a, 3))
ok(expand(d9 - Rational(3, 2) * x * (x - 2)) == 0, '9번 차 = (3/2)x(x−2): x=0, 2에서 교차')
ok(sorted(solve(d9, x)) == [0, 2], '9번 [0,4] 안의 교점은 x=0, 2뿐 → 둘러싸인 부분 두 개')
L9 = abs(integrate(d9, (x, 0, 2))); R9 = abs(integrate(d9, (x, 2, 4)))
ok(all(d9.subs(x, Rational(i, 10)) < 0 for i in range(1, 20)) and all(d9.subs(x, 2 + Rational(i, 10)) > 0 for i in range(1, 21)), '9번 0<x<2에서 아래로 볼록 곡선이 아래, 2<x≤4에서 위')
S9 = L9 + R9
ok(L9 == 2 and R9 == 10 and S9 == 12, f'9번 두 부분 넓이 {L9}, {R9}, 합 {S9}')
import mpmath
S9n = mpmath.quad(sp.lambdify(x, sp.Abs(d9), 'mpmath'), [0, 2, 4])
ok(abs(S9n - 12) < 1e-9, f'9번 수치 적분 ∫|차| = {S9n}')
c9 = chk(9, S9, dset=(2,))
ok(integrate(d9, (x, 0, 4)) == 8, '9번 오답 8: 부호 있는 정적분 ∫₀⁴(3/2 x²−3x)dx')
ok(R9 == 10, '9번 오답 10: 큰 부분(2≤x≤4)만')
# 원문 J50: 16/5 (⑤)
ok(integrate((x**2 + 3) - (-Rational(1, 5) * x**2 + 3), (x, 0, 2)) == Rational(16, 5), '9번 원문 J50 정답 16/5(⑤)')
# 빼 보기
for av in (2, 4):
    dd = expand((F9 - G9).subs(a, av)); rr = sorted(solve(dd, x))
    Sv = sum(abs(integrate(dd, (x, rr_[0], rr_[1]))) for rr_ in zip([0] + [r for r in rr if 0 < r < 4], [r for r in rr if 0 < r < 4] + [4]))
    print(f'ABLATION 9 x=2에서 만남: 필요(a={av}이면 넓이 {Sv} ≠ 12)'); assert Sv != 12
# 'y축'은 두 곡선이 (0,3)에서 만나므로 넣어도 영역이 같음(군더더기) → 본문에서 뺌
ok('y\\)축' not in IT[9]['body'], '9번 본문에 군더더기 y축 없음(두 곡선이 y축 위에서 만남)')

# ---------- 10번 (J21) ----------
C1 = x**3 - 4 * x**2 - 5 * x - 8; C2 = x**3 - 7 * x**2 + 7 * x + 7
h10 = expand(C2 - C1)
ok(expand(h10 - (-3) * (x + 1) * (x - 5)) == 0, '10번 차 = −3(x+1)(x−5) (삼차항 소거)')
ok(sorted(solve(expand(C1 - C2), x)) == [-1, 5], '10번 두 곡선의 교점은 x=−1, 5 두 개 → 둘러싸인 부분 하나')
Tot = integrate(h10, (x, -1, 5))
k = symbols('k', real=True)
ks = [r for r in solve(integrate(h10, (x, -1, k)) - Tot / 2, k) if r.is_real and -1 < r < 5]
ok(ks == [2], f'10번 이등분하는 k (−1<k<5) = {ks} (유일)')
D10 = abs(C2.subs(x, 2) - C1.subs(x, 2))
ok(D10 == h10.subs(x, 2) == 27, f'10번 x=2 위 두 점 사이 거리 {D10} (C2(2)={C2.subs(x,2)}, C1(2)={C1.subs(x,2)})')
c10 = chk(10, D10)
ok(h10.subs(x, 1) == 24, '10번 오답 24: 원문 습관 k=1로 h(1)')
ok(Tot == 108, '10번 전체 넓이 108(참고)')
# 원문 J21: k=1 (②)
ho = expand((-x**2 + 6 * x + 1) - (2 * x**2 - 8))
ko = [r for r in solve(integrate(ho, (x, -1, k)) - integrate(ho, (x, -1, 3)) / 2, k) if r.is_real and -1 < r < 3]
ok(ko == [1], '10번 원문 J21 정답 k=1(②)')
print('ABLATION 10 이등분: 필요(없으면 k가 정해지지 않아 거리가 정해지지 않음; 예: k=1이면 24, k=0이면 %s)' % h10.subs(x, 0))

# ---------- 11번 (M39) ----------
C = symbols('C')
f11 = integrate(4 * x**3 - 4 * x, x) + C
def H(fx, tv, eps=Rational(1, 10**6)):
    """|t−f(x)|가 미분가능하지 않은 x의 개수 = f(x)=t의 실근 중 부호가 바뀌는 근(f−t가 홀수 중복이고 f'≠0이면 꺾임)
    정확 판정: 실근 r마다 좌우 미분계수 |…|' 비교(차분)"""
    P = sp.Poly(fx - tv, x)
    roots = sorted(set(r for r in sp.real_roots(P)))
    cnt = 0
    for r in roots:
        g = sp.lambdify(x, sp.Abs(tv - fx), 'mpmath')
        rr = mpmath.mpf(sp.N(r, 50)); e = mpmath.mpf('1e-12')
        dl = (g(rr) - g(rr - e)) / e; dr = (g(rr + e) - g(rr)) / e
        if abs(dl - dr) > 1e-6: cnt += 1
    return cnt
mpmath.mp.dps = 50
f0 = f11.subs(C, 0)
ok(expand(f0 - (x**4 - 2 * x**2)) == 0, '11번 상수항 0 → f = x⁴−2x²')
hp, hm, h0 = H(f0, Rational(1, 10**4)), H(f0, -Rational(1, 10**4)), H(f0, 0)
ok((hp, hm, h0) == (2, 4, 2), f'11번 h(0+)={hp}, h(0−)={hm}, h(0)={h0}')
# 극한이 실제로 그 값인지: 0 근처 여러 t에서 같은 값
ok(all(H(f0, Rational(s, 1000)) == 2 for s in (1, 5, 50, 300)) and all(H(f0, -Rational(s, 1000)) == 4 for s in (1, 5, 50, 300)), '11번 0<t<1, −1<t<0에서 h가 각각 2, 4로 일정(극한 확인)')
S11 = hp + hm + h0
c11 = chk(11, S11)
ok(2 + 4 + 3 == 9 and 2 + 4 + 4 == 10 and 4 + 4 + 4 == 12, '11번 오답 9(접점 x=0을 셈), 10(x=0을 두 번), 12(t>0에서도 4)')
ok(len([r for r in sp.real_roots(sp.Poly(f0, x))]) == 4, '11번 f(x)=0은 중복도 포함 근 4개(x=0 중근) — 오답 10의 경로')
# 원문 M39: f=x³(x−4)에서 (나) 합 5, f(1)=−3
fo = x**3 * (x - 4)
ok(H(fo, Rational(1, 10**4)) + H(fo, -Rational(1, 10**4)) + H(fo, 0) == 5 and fo.subs(x, 1) == -3, '11번 원문 M39: 합 5, f(1)=−3(③)')
# 빼 보기: 상수항 조건
for Cv in (1, -1):
    fc = f11.subs(C, Cv); Sv = H(fc, Rational(1, 10**4)) + H(fc, -Rational(1, 10**4)) + H(fc, 0)
    print(f'ABLATION 11 상수항 0: 필요(C={Cv}이면 합 {Sv})'); assert Sv != 8
print(f'ABLATION 11 h(0): 필요(h(0)을 빼면 {hp + hm}, 접점 판단이 답에 일함)')

# ---------- 12번 (D64) ----------
A, B, Cc = symbols('A B Cc', real=True)
fG = x**3 + A * x**2 + B * x + Cc
s = expand(diff(fG, x).subs(x, t) - 4 * (t - 2)**2)
ok(sp.Poly(s, t).LC() == -1, '12번 우변 s(t)의 t² 계수 −1 (위로 볼록, 원문과 같은 방향)')
sol = solve([diff(s, t).subs(t, 5), diff(fG, x).subs(x, 2), s.subs(t, 5) - fG.subs(x, 2)], [A, B, Cc], dict=True)
ok(sol == [{A: -3, B: 0, Cc: 13}], f'12번 a, b, c = {sol}')
f12 = fG.subs(sol[0]); s12 = s.subs(sol[0])
ok(expand(f12 - 9 - (x - 2)**2 * (x + 1)) == 0, '12번 f−9 = (x−2)²(x+1), 극솟값 9(x=2)')
ok(sorted(solve(diff(f12, x), x)) == [0, 2] and diff(f12, x, 2).subs(x, 2) > 0, '12번 극대 x=0, 극소 x=2')
ok(expand(s12 - (9 - (t - 5)**2)) == 0, '12번 s(t) = 9 − (t−5)², 최댓값 9 = 극솟값')
import numpy as np
CO = [float(c) for c in sp.Poly(f12, x).all_coeffs()]
def gmax(kv):
    rs = np.roots(CO[:-1] + [CO[-1] - kv])
    return max(r.real for r in rs if abs(r.imag) < 1e-5)
ok(max(sp.real_roots(sp.Poly(f12 - 9, x))) == 2, '12번 g(5) = 2 (높이 9의 최대 실근 = 극솟점, 정확값)')
ts = np.linspace(-6, 16, 22001)
gs = [gmax(9 - (tv - 5)**2) for tv in ts]
jumps = [ts[i] for i in range(len(ts) - 1) if abs(gs[i + 1] - gs[i]) > 0.3]
ok(len(jumps) == 2 and all(abs(j - 5) < 0.002 for j in jumps), f'12번 [−6,16] 격자(0.001)에서 점프는 t=5 근처뿐 {[round(j, 4) for j in jumps]}')
near = [gmax(9 - e**2) for e in (1e-2, 1e-3, 1e-4)]
ok(all(abs(v + 1) < 1e-2 for v in near), f'12번 t→5에서 g(t) → −1 ({[round(v, 4) for v in near]})')
c12 = chk(12, -1)
ok(0 in c12 and 0 in solve(diff(f12, x), x), '12번 오답 0: 극댓점을 극한값으로')
fo = x**3 + 3 * x**2 - 9 * x + 9
so = expand(diff(fo, x).subs(x, t) - 4 * t**2 + 4)
ok(expand(so - (-(t - 3)**2 + 4)) == 0 and fo.subs(x, 1) == 4 and fo.subs(x, 2) == 11, '12번 원문 D64 정답 11')
sol2 = solve([diff(s, t).subs(t, 6), diff(fG, x).subs(x, 2), s.subs(t, 6) - fG.subs(x, 2)], [A, B, Cc], dict=True)[0]
f2 = fG.subs(sol2); gam = sp.solve(sp.cancel((f2 - f2.subs(x, 2)) / (x - 2)**2), x)
print(f"ABLATION 12 't=5에서만 불연속': 필요(꼭짓점이 t=6이면 a={sol2[A]}, 극한값 {gam})"); assert gam != [-1]
sol3 = solve([diff(s, t).subs(t, 5), diff(fG, x).subs(x, 3), s.subs(t, 5) - fG.subs(x, 3)], [A, B, Cc], dict=True)[0]
f3 = fG.subs(sol3); gam3 = sp.solve(sp.cancel((f3 - f3.subs(x, 3)) / (x - 3)**2), x)
print(f"ABLATION 12 'g(5)=2': 필요(극솟점이 3이면 극한값 {gam3})"); assert gam3 != [-1]

print(f'{len(OK)} checks')
print('ALL OK')
