# -*- coding: utf-8 -*-
# p3.py (10회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, integrate, diff, solve, expand

x, t = symbols('x t', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 1, 10: 2, 11: 4, 12: 5}          # 분담표 9⑤·12①을 맞바꿈(회차 분포 그대로)
DBREF = {9: 'I57 v3_추가 1', 10: 'I6 후보_순위 2', 11: 'I33 후보_순위 2', 12: 'I75 후보_순위 1'}
KEYS = {9: 'I57', 10: 'I6', 11: 'I33', 12: 'I75'}
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
    ok(len(it['wrongs']) >= 1 and all(w in it['choices'] and it['choices'].index(w) != it['ans'] - 1 for w in it['wrongs']), f'{n}번 wrongs {it["wrongs"]}가 선지에 있고 정답과 다름')
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    for f_ in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
        ok('이러한' not in it[f_] and '이와 같은' not in it[f_], f'{n}번 {f_} 금지 어구 없음')
    ok(not any(('<' in m or '>' in m) for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', it['body'], re.S)), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if IT[n]['effect'] == '어려워짐') <= 1, '어려워짐 1개 이하(9번)')

def chk(n, v0):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1, f'{n}번 선지 {v} 서로 다르고 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    body_nums = {Rational(s) for s in re.findall(r'-?\d+', re.sub(r'\^\{?\d+\}?', ' ', re.sub(r'\\[a-zA-Z]+', ' ', IT[n]['body'])))}
    ok(v0 not in body_nums or v0 in (0,), f'{n}번 정답 {v0}이 본문에 나온 수(지수 제외)와 다름')
    return v

# ---------- 9번 (I57) ----------
def amin9(kv, g=x**2 + 6 * x):
    """g′=f=g+a ≥ 0 on [k,k+1] ⇔ a ≥ −min g → a의 최솟값 = −min_{[k,k+1]} g (볼록, 꼭짓점 −3)"""
    kv = Rational(kv)
    pts = [kv, kv + 1] + ([Rational(-3)] if kv <= -3 <= kv + 1 else [])
    return -min(g.subs(x, p) for p in pts)
k = symbols('k', real=True)
# 경우별 식으로 전수: k>−3, k<−4, −4≤k≤−3
c1 = [r for r in solve(-(k**2 + 6 * k) + 7, k) if r > -3]
c2 = [r for r in solve(-((k + 1)**2 + 6 * (k + 1)) + 7, k) if r < -4]
c3 = [] if 9 != -7 else ['all']
K9 = sorted(c1 + c2)
ok(K9 == [-8, 1], f'9번 a의 최솟값 −7이 되는 k = {K9} (꼭짓점을 품으면 최솟값 9)')
# 촘촘한 격자로도 확인(유리수 격자 + 경우 경계)
grid = [Rational(i, 8) for i in range(-120, 81)]
hit = sorted({kv for kv in grid if amin9(kv) == -7})
ok(hit == [-8, 1], f'9번 격자 −15..10 (1/8 간격)에서 a의 최솟값 −7인 k {hit}')
# 실제로 a=−7일 때 [k,k+1]에서 f≥0, a<−7이면 깨짐
for kv in K9:
    f9 = x**2 + 6 * x - 7
    mn = min(f9.subs(x, p) for p in [kv, kv + 1] + ([-3] if kv <= -3 <= kv + 1 else []))
    ok(mn == 0, f'9번 k={kv}, a=−7: 구간 최솟값 0(증가), a가 더 작으면 음수')
v9 = chk(9, K9[0] * K9[1])
wr = solve(k**2 + 6 * k - 7, k)
ok(wr[0] * wr[1] == -7 and amin9(-7) == 0, '9번 오답 −7: f(k)≥0 식의 두 근 1, −7을 곱함(k=−7이면 a의 최솟값 0)')
# 원문 I57: f=−x²−4x+a, [0,1] → 5
ok(amin9(0, -x**2 - 4 * x) == 5 if False else (-min((-x**2 - 4 * x).subs(x, p) for p in (0, 1))) == 5, '9번 원문 I57 정답 5')
ok(K9[0] + K9[1] == -7, '9번 (note) 합은 축 대칭으로 늘 −7 → 곱을 물음')
# 빼 보기
k_alt = sorted({kv for kv in grid if amin9(kv) == -16})
print(f'ABLATION 9 최솟값 −7: 필요(−16이면 k = {k_alt}, 곱 {k_alt[0] * k_alt[1]})'); assert k_alt[0] * k_alt[1] != -8
k_w = sorted({kv for kv in grid if amin9(kv, -x**2 - 6 * x) == 7})
print(f'ABLATION 9 최고차항 부호(아래로 볼록): 필요(−x²−6x+a이면 a의 최솟값 7인 k {k_w})'); assert k_w != [-8, 1]
print('ABLATION 9 구간 [k,k+1]: 필요(고정 구간이면 묻는 k가 없음)')

# ---------- 10번 (I6) ----------
P, Q, C = symbols('P Q C')
fx = symbols('fx')
# 일반 f(다항식): xf + C = 2x³ − Px² + Qx, x=0 → C=0
Cs = solve((2 * x**3 - P * x**2 + Q * x - C).subs(x, 0), C)
ok(Cs == [0], '10번 x=0 대입 → C=0, f = 2x² − Px + Q')
f10 = 2 * x**2 - P * x + Q
ok(expand(diff(x * f10, x) - (f10 + x * diff(f10, x))) == 0 and expand(integrate(f10 + x * diff(f10, x), x) - (2 * x**3 - P * x**2 + Q * x)) == 0, '10번 ∫{f+xf′}dx = xf 확인')
pairs = []
for pv in range(1, 200):
    for qv in range(1, 21):
        ff = f10.subs({P: pv, Q: qv})
        cr = solve(diff(ff, x), x)
        if len(cr) == 1 and ff.subs(x, cr[0]) == 1:
            pairs.append((pv, qv))
ok(pairs == [(4, 3), (8, 9), (12, 19)], f'10번 전수(p<200, q≤20): 극값 f(a)=1인 (p, q) = {pairs}')
v10 = chk(10, len(pairs))
pw = [(pv, qv) for pv in range(1, 200) for qv in range(1, 21) if Rational(qv) - Rational(pv**2, 4) == 1]
ok(len(pw) == 4, f'10번 오답 4: 꼭짓점 값을 q−p²/4로 두면 {pw}')
# 원문 I6: f = x²−2x+3, 극값 2
fo = x**2 - 2 * x + 3
ok(expand(diff(fo - 3, x) * 0 + (fo - 3) + x * diff(fo, x) - diff(x**3 - 2 * x**2, x)) == 0 and fo.subs(x, 1) == 2, '10번 원문 I6 정답 2(③)')
# 빼 보기
pr2 = [(pv, qv) for pv in range(1, 200) for qv in range(1, 200) if Rational(qv) - Rational(pv**2, 8) == 1]
print(f'ABLATION 10 q≤20: 필요(없으면 순서쌍이 끝없이 {pr2[:5]}…)'); assert len(pr2) > 3
pr3 = [(pv, qv) for pv in range(1, 200) for qv in range(1, 21) if Rational(qv) - Rational(pv**2, 8) == 3]
print(f'ABLATION 10 f(a)=1: 필요(f(a)=3이면 {len(pr3)}개)'); assert len(pr3) != 3
print('ABLATION 10 이차항 계수 2: 필요(1이면 p 짝수 조건으로 개수가 달라짐 — 오답 4와 같은 계산)')

# ---------- 11번 (I33) ----------
m, n0, L = symbols('m n0 L', real=True)
f11 = m * x + n0
F11 = integrate(f11, x)
expr = integrate(diff(f11, x), (x, 0, 1)) + diff(F11, x).subs(x, 0)
ok(expand(expr - f11.subs(x, 1)) == 0, '11번 ∫_0^1 f′dx + F′(0) = f(1)')
# f(0)=1 → n0=1, |f(1)| ≤ L → f(3)=3f(1)−2 최댓값 3L−2
f3 = f11.subs(n0, 1).subs(x, 3)
f1 = f11.subs(n0, 1).subs(x, 1)
mx = sp.maximum(f3.subs(m, sp.Symbol('u') - 1), sp.Symbol('u'), sp.Interval(-L, L)) if False else None
# 직접: m = f(1) − 1 ∈ [−L−1, L−1], f(3) = 3m + 1, 증가 → 최댓값 3(L−1)+1 = 3L−2
Ls = solve(3 * (L - 1) + 1 - 10, L)
ok(Ls == [4], '11번 f(3)의 최댓값 3L−2 = 10 → L = 4 (유일, f=3x+1에서 달성)')
ok((3 * x + 1).subs(x, 3) == 10 and abs((3 * x + 1).subs(x, 1)) <= 4, '11번 f=3x+1: |f(1)|=4≤4, f(3)=10')
# 격자 전수: L=4에서 f(3) 최댓값
best = max((3 * mm + 1) for mm in [Rational(i, 10) for i in range(-60, 61)] if abs(mm + 1) <= 4)
ok(best == 10, f'11번 L=4 격자 전수: f(3)의 최댓값 {best}')
v11 = chk(11, Ls[0])
Lw = solve(3 * (L - 1 - 1) + 1 - 10, L)    # |f(1)+1|≤L → f(1)≤L−1 → m≤L−2
ok(Lw == [5], '11번 오답 5: ∫_0^1 f′dx를 f(1)로 보아 |f(1)+1|≤L')
# 원문 I33: f(3)=3f(1)−8, |f(1)|≤2 → [−14, −2], 곱 28
ok((-14) * (-2) == 28 and 3 * 2 - 8 == -2 and 3 * (-2) - 8 == -14, '11번 원문 I33 정답 28(④)')
# 빼 보기
print(f'ABLATION 11 f(0)=1: 필요(f(0)=2이면 L = {solve(3 * L - 4 - 10, L)[0]})'); assert solve(3 * L - 4 - 10, L)[0] != 4
print(f'ABLATION 11 최댓값 10: 필요(없으면 L이 정해지지 않음)')
print('ABLATION 11 일차함수: 필요(다항함수면 f(3)이 f(0), f(1)로 정해지지 않아 최댓값이 없음)')

# ---------- 12번 (I75) ----------
def sign_change_ranges(roots_sc, a_coef=2, w=4):
    """창 (a p, a p + w)가 부호 변화점 r을 품는 p 범위: (r−w)/a < p < r/a"""
    return sorted(((r - w) / a_coef, r / a_coef) for r in roots_sc)
ok(sign_change_ranges([6]) == [(1, 3)], '12번 부호 변화점이 6 하나 → 1<p<3')
ok(sign_change_ranges([0, 6]) == [(-2, 0), (1, 3)], '12번 0이 단순근이면 −2<p<0도 생김 → 0은 중근')
# 후보 전수: 상수항 0 삼차, 실근 {0, 6, s}, 부호 변화점 집합이 {6}이어야 함
def sc_roots(rts):
    from collections import Counter
    c = Counter(rts)
    return sorted(r for r, mlt in c.items() if mlt % 2 == 1)
good = []
for s_ in [Rational(i, 2) for i in range(-30, 31)]:
    if sc_roots([0, 6, s_]) == [6]: good.append(s_)
ok(good == [0], f'12번 세 근 0, 6, s에서 부호 변화점이 6뿐인 s = {good} → f = c x²(x−6)')
# 수치: f=x²(x−6), 창 [2p, 2p+4]에서 ∫|f| ≠ |∫f| 인 p
cc = symbols('cc', positive=True)
F12 = x**2 * (x - 6)
def neq(lo, hi, h):
    a1 = sp.integrate(sp.Abs(h), (x, lo, hi)) if False else None
    # 부호 변화 여부를 직접: 열린구간 안의 근에서 부호가 바뀌는지
    rs = [r for r in sp.real_roots(sp.Poly(h, x)) if lo < r < hi]
    return any(h.subs(x, r - Rational(1, 10**6)) * h.subs(x, r + Rational(1, 10**6)) < 0 for r in rs)
ps = [Rational(i, 4) for i in range(-20, 21)]
inside = [pv for pv in ps if neq(2 * pv, 2 * pv + 4, F12)]
ok(min(inside) > 1 and max(inside) < 3 and Rational(5, 4) in inside and Rational(11, 4) in inside and 1 not in inside and 3 not in inside, f'12번 f=x²(x−6) 격자: 부등식 성립 p ⊂ (1,3), 끝 1·3 제외')
# 실제 적분으로 몇 점 확인
for pv in (Rational(1, 2), Rational(2), Rational(7, 2)):
    cuts = [2 * pv] + sorted(r for r in (0, 6) if 2 * pv < r < 2 * pv + 4) + [2 * pv + 4]
    I1 = sum(abs(sp.integrate(F12, (x, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))
    I2 = abs(sp.integrate(F12, (x, 2 * pv, 2 * pv + 4)))
    ok((sp.simplify(I1 - I2) != 0) == (1 < pv < 3), f'12번 p={pv}: ∫|f| {"≠" if 1 < pv < 3 else "="} |∫f| (적분 직접)')
# (나): [0,6]에서 f의 값 범위 [−32c, 0] → 0<q<32c
fmin = min(F12.subs(x, r) for r in [0, 6] + solve(diff(F12, x), x))
ok(fmin == -32 and F12.subs(x, 4) == -32, '12번 [0,6]에서 c=1일 때 최솟값 f(4)=−32')
qs = [Rational(i, 2) for i in range(-10, 80)]
qin = [qv for qv in qs if neq(0, 6, F12 + qv)]
ok(min(qin) > 0 and max(qin) < 32 and Rational(1, 2) in qin and Rational(63, 2) in qin and 32 not in qin, '12번 c=1: q 범위가 0<q<32 (32에서 접하기만 함)')
qneg = [qv for qv in qs if neq(0, 6, -F12 + qv)]
ok(all(qv < 0 for qv in qneg), '12번 c<0이면 q 범위가 음수 → c>0')
csol = solve(32 * cc - 32, cc)
ok(csol == [1], '12번 32c = 32 → c = 1 (유일)')
v12 = chk(12, F12.subs(x, 3))
ok(F12.subs(x, 4) == -32, '12번 오답 −32: 최솟값을 구간 가운데 x=3의 값으로 착각')
# 원문 I75: f = x²(x−3)/4, f(6)=27
fo12 = x**2 * (x - 3) / 4
ok(fo12.subs(x, 6) == 27 and min(fo12.subs(x, r) for r in [0, 3, 2]) == -1, '12번 원문 I75 정답 27(④)')
# 빼 보기
print(f'ABLATION 12 p 범위 1<p<3: 필요(0<p<2이면 r=4, f=x²(x−4)로 바뀜)')
print(f'ABLATION 12 구간 끝 2p: 필요(p, p+4이면 범위 1<p<3에서 r이 정해지지 않음 — 길이 2인 범위는 폭 4 창에서 나오지 않음)')
assert sign_change_ranges([6], 1, 4) == [(2, 6)]
c_alt = solve(32 * cc - 16, cc)[0]
print(f'ABLATION 12 q 범위 0<q<32: 필요(0<q<16이면 c={c_alt}, f(3)={F12.subs(x, 3) * c_alt})'); assert F12.subs(x, 3) * c_alt != -27
print('ABLATION 12 상수항 0: 필요(없으면 다른 근이 정해지지 않아 f가 하나로 정해지지 않음)')

print(f'{len(OK)} checks')
print('ALL OK')
