# -*- coding: utf-8 -*-
# p3.py (12회 9·10·11·12번) 검증: 계산 정답 = 지정 선지 · 전수 유일성 · 선지 등차·서로 다름 · wrongs 실재 · 원문 정답 · 조건 빼 보기
import os, re
import sympy as sp
from sympy import symbols, Rational, integrate, diff, solve, expand, factor

x, t = symbols('x t', real=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}; exec(open(os.path.join(HERE, 'p3.py')).read(), ns)
IT = ns['ITEMS']
WANT = {9: 5, 10: 4, 11: 2, 12: 1}
DBREF = {9: 'J71 후보_순위 4', 10: 'J10 후보_순위 3', 11: 'M37 v3_추가 1', 12: 'J72 후보_순위 2'}
KEYS = {9: 'J71', 10: 'J10', 11: 'M37', 12: 'J72'}
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
    ok('cond' not in it, f'{n}번 상자 없음(분담표 ×)')
    for f_ in ('body', 'sol', 'fast', 'wrong', 'note', 'var'):
        ok('이러한' not in it[f_] and '이와 같은' not in it[f_], f'{n}번 {f_} 금지 어구 없음')
    txt = it['body'] + ''.join(b for _, b in it.get('bogi', []))
    ok(not any(('<' in m or '>' in m) for m in re.findall(r'\\\(.*?\\\)|\\\[.*?\\\]', txt, re.S)), f'{n}번 본문 수식에 맨 부등호 없음')
    for f_ in ('var', 'sol', 'fast', 'wrong', 'note', 'src'):
        assert it[f_], (n, f_)
ok(all(COEF & set(IT[n]['ops']) for n in (9, 10, 12)), '9·10·12번(계수 ●) ops에 계수·매개변수 자리 조작 있음')
ok(sum(1 for n in IT if IT[n]['effect'] == '어려워짐') == 0, '9–12번 어려워짐 0개')
ok(sum(1 for n in IT if IT[n].get('bogi')) == 1, '9–12번 보기형 1개(12번)')
ok('fig_10.svg' in IT[10]['body'] and os.path.exists(os.path.join(HERE, 'fig_10.svg')) and os.path.exists(os.path.join(HERE, '..', 'fig_10.svg')), '10번 그림 파일 parts/fig_10.svg·회차 폴더 fig_10.svg 있음')

def chk(n, v0, dset=(1,)):
    v = [val(c) for c in IT[n]['choices']]
    d = {v[i + 1] - v[i] for i in range(4)}
    ok(len(set(v)) == 5 and len(d) == 1 and (v[1] - v[0]) in dset, f'{n}번 선지 {v} 서로 다르고 오름차순 등차(공차 {v[1] - v[0]})')
    ok(v[IT[n]['ans'] - 1] == v0, f'{n}번 계산 정답 {v0} = 선지 {IT[n]["ans"]}번')
    plain = re.sub(r'\\[a-zA-Z]+', ' ', re.sub(r'<[^>]+>', ' ', IT[n]['body']))
    body_nums = {Rational(s) for s in re.findall(r'-?\d+', re.sub(r'\^\{?\d+\}?', ' ', plain))}
    ok(v0 not in body_nums, f'{n}번 정답 {v0}이 본문에 나온 수(지수 제외)와 다름')
    return v

def dist(v, a, b):
    """[a, b]에서 움직인 거리(정확값): 속도 부호가 바뀌는 점에서 나눠 적분"""
    cuts = sorted({r for r in solve(v, t) if r.is_real and a < r < b})
    pts = [a] + cuts + [b]
    return sum(abs(integrate(v, (t, pts[i], pts[i + 1]))) for i in range(len(pts) - 1))

# ---------- 9번 (J71) ----------
v9 = 3 * t**2 - 24 * t + 45
ok(expand(v9 - 3 * (t - 3) * (t - 5)) == 0, '9번 v = 3(t−3)(t−5)')
tm = solve(diff(v9, t), t)
ok(tm == [4] and all(v9.subs(t, s) > v9.subs(t, 4) for s in [Rational(i, 4) for i in range(0, 60)] if s != 4), '9번 t≥0에서 속도가 최소인 순간은 t=4뿐(가속도 0)')
x9 = integrate(v9, (t, 0, t))
ok(x9.subs(t, 3) == 54 and x9.subs(t, 4) == 52, '9번 x(3)=54, x(4)=52')
D9 = dist(v9, 0, 4)
ok(D9 == 56, f'9번 t=0부터 t=4까지 움직인 거리 {D9}')
# 수치 적분으로 한 번 더
D9n = sp.Integral(sp.Abs(v9), (t, 0, 4)).evalf()
ok(abs(D9n - 56) < 1e-9, f'9번 수치 적분 ∫|v| = {D9n}')
c9 = chk(9, D9)
ok(x9.subs(t, 4) == 52, '9번 오답 52: 위치의 변화량 x(4)−x(0)')
ok(dist(v9, 0, 3) == 54, '9번 오답 54: 속력 0인 t=3을 최소로 보아 t=3까지의 거리')
# 원문 J71: 보기 ㄱ·ㄴ·ㄷ 모두 참
vo = 3 * t**2 - 10 * t + 7
ok(expand(vo - (t - 1) * (3 * t - 7)) == 0 and integrate(vo, (t, 0, 1)) == 3 and dist(vo, 0, 2) == 4, '9번 원문 J71: t=1 전환, x(1)=3, [0,2] 거리 4 → ⑤')
# 빼 보기
print('ABLATION 9 속도식: 필요(없으면 값이 정해지지 않음)')
print(f'ABLATION 9 "속도가 최소": 필요(속력 0인 순간으로 읽으면 {dist(v9, 0, 3)}, t=5로 읽으면 {dist(v9, 0, 5)})')
ok(dist(v9, 0, 5) not in c9, '9번 t=5까지의 거리는 선지 밖(구간이 다르면 다른 값)')

# ---------- 10번 (J10) ----------
a = symbols('a')
f10 = 2 * x**3 + a * x**2 - 9 * x - 5
g10 = x**2 + 5 * x + 7
sa = solve(f10.subs(x, -1) - g10.subs(x, -1), a)
ok(sa == [1], f'10번 x=−1에서 만남 → a = {sa}')
h = expand((f10 - g10).subs(a, 1))
ok(expand(h - 2 * (x - 3) * (x + 1) * (x + 2)) == 0, '10번 차 = 2(x+2)(x+1)(x−3)')
roots = sorted(solve(h, x))
ok(roots == [-2, -1, 3], f'10번 교점 x = {roots} (간격 1, 4로 등간격 아님)')
L = abs(integrate(h, (x, -2, -1))); R = abs(integrate(h, (x, -1, 3)))
ok(L == Rational(3, 2) and R == 64, f'10번 두 부분 넓이 {L}, {R}')
ok(all(h.subs(x, -2 + Rational(i, 10)) > 0 for i in range(1, 10)) and all(h.subs(x, -1 + Rational(i, 10)) < 0 for i in range(1, 40)), '10번 [−2,−1]에서 삼차곡선이 위, [−1,3]에서 포물선이 위')
S10 = L + R
import mpmath
S10n = mpmath.quad(sp.lambdify(x, sp.Abs(h), 'mpmath'), mpmath.linspace(-2, 3, 51))
ok(abs(S10n - float(S10)) < 1e-6, f'10번 수치 적분 넓이 {S10n}')
c10 = chk(10, S10, dset=(Rational(1, 2),))
ok(R == 64, '10번 오답 64: 좁은 부분(−2≤x≤−1)을 놓치고 큰 부분만')
ok(2 * L != S10 and 2 * R != S10 and abs(integrate(h, (x, -2, 3))) not in c10, '10번 대칭 2배·부호 있는 적분 값은 답이 아님(등간격 깨짐 확인)')
# 원문 J10: 8
ho = expand(x**3 + 4 * x**2 - 3 - (x**2 + x))
ok(integrate(sp.Abs(ho), (x, -3, 1)) == 8, '10번 원문 J10 정답 8(④)')
# 빼 보기: x=−1에서 만난다는 조건이 없으면 a에 따라 넓이가 바뀜(예: a=0이면 교점이 무리수)
ha0 = expand((f10 - g10).subs(a, 0))
print(f'ABLATION 10 x=−1에서 만남: 필요(없으면 a가 정해지지 않음; a=0이면 차 {ha0}, 근 {[sp.nsimplify(r) for r in solve(ha0, x)]})')
ok(-1 not in solve(ha0, x), '10번 (빼 보기) a=0이면 x=−1은 교점이 아님')

# ---------- 11번 (M37) ----------
A = symbols('A')
J = 1                                   # 이음점
left = (x - 1) * (x - 5)
right = x**3 - 9 * x**2 + 24 * x + A
sA = solve(left.subs(x, J) - right.subs(x, J), A)
ok(sA == [-16], f'11번 x=1에서 연속 → a = {sA}')
def Ffun(Av):
    fl = sp.lambdify(x, left); fr = sp.lambdify(x, right.subs(A, Av))
    return lambda u: fl(u) if u < J else fr(u)
def extrema(Av, lo=-6, hi=10, step=0.001):
    """격자 전수: 이웃 두 점보다 엄격히 크거나 작은 점(조각함수 그대로)"""
    F = Ffun(Av); n = int(round((hi - lo) / step))
    g = [lo + i * step for i in range(n + 1)]; Fv = [F(u) for u in g]
    return sorted({round(g[i], 2) for i in range(1, n) if (Fv[i] > Fv[i - 1] and Fv[i] > Fv[i + 1]) or (Fv[i] < Fv[i - 1] and Fv[i] < Fv[i + 1])})
ex = extrema(-16)
ok(ex == [1.0, 2.0, 4.0], f'11번 격자 전수(0.001 간격) 극값을 갖는 x = {ex} (이음점 1 극소, 꼭짓점 3은 구간 밖)')
ok(diff(left, x).subs(x, J) < 0 and diff(right, x).subs(x, J) > 0, '11번 이음점: 왼쪽 미분계수 −4 <0, 오른쪽 9 >0')
ok(all(diff(left, x).subs(x, J - Rational(i, 4)) < 0 for i in range(1, 40)), '11번 x<1에서 f′=2x−6<0 (왼쪽 조각에 극점 없음)')
ok(expand(diff(right, x) - 3 * (x - 2) * (x - 4)) == 0, "11번 x>1에서 f′=3(x−2)(x−4)")
ok(len(ex) == 3, '11번 극점이 정확히 셋(본문 서로 다른 세 실수와 맞음)')
s11 = sum(Rational(round(e)) for e in ex)
c11 = chk(11, s11)
ok(3 + 2 + 4 == 9, '11번 오답 9: 이음점 대신 꼭짓점 3을 세 번째 극점으로 셈(원문 습관)')
# 원문 M37: a=12, b=5 → 17
ao = solve((-x**3 - x**2 + 8 * x + A).subs(x, 3), A)[0]
b = symbols('b')
bo = solve(-2 + Rational(4, 3) + (3 + b) / 2 - Rational(10, 3), b)[0]
ok(ao == 12 and bo == 5 and ao + bo == 17, '11번 원문 M37 정답 17')
# 빼 보기: 연속 조건이 없으면 a가 자유 → a=−10이면 f(1)=6 > 왼쪽 극한 0, 오른쪽은 증가 → x=1은 극값 아님
fl_, fr_ = left, right.subs(A, -10)
e_ = Rational(1, 10**4)
v0, vl, vr = fr_.subs(x, J), fl_.subs(x, J - e_), fr_.subs(x, J + e_)
is_ext = (v0 > vl and v0 > vr) or (v0 < vl and v0 < vr)
print(f'ABLATION 11 연속: 필요(a=−10이면 f(1)={v0}, 왼쪽 {vl}, 오른쪽 {vr} → x=1 극값 {is_ext}, 극점 2, 4 둘뿐)'); assert not is_ext
# 분석집 M37 변형①의 삼차 조각과 다름
ok(expand(right.subs(A, 0) - (x**3 - 3 * x**2 - 9 * x)) != 0, '11번 삼차 조각이 분석집 변형①(x³−3x²−9x+a)과 다름')

# ---------- 12번 (J72) ----------
k = symbols('k')
v12 = (t - k)**2 - 4
def turns(kv):
    """출발한 후(t>0) 속도 부호가 바뀌는 시각"""
    vv = v12.subs(k, kv)
    return sorted(r for r in solve(vv, t) if r.is_real and r > 0 and sp.sign(vv.subs(t, r - Rational(1, 1000))) != sp.sign(vv.subs(t, r + Rational(1, 1000))))
g_ = integrate(v12.subs(k, 0), (t, 0, 1))
T1 = (g_ == Rational(-11, 3))
T2 = (len(turns(2)) == 2)
d3 = dist(v12.subs(k, 3), 0, 2)
T3 = (d3 == Rational(2, 3))
ok(T1 and not T2 and not T3, f'12번 ㄱ x(1)={g_} 참, ㄴ k=2 전환 {turns(2)} (한 번) 거짓, ㄷ 거리 {d3} 거짓')
truth = ''.join(c for c, b_ in zip('ㄱㄴㄷ', (T1, T2, T3)) if b_)
ok(IT[12]['choices'][IT[12]['ans'] - 1] == 'T:' + ', '.join(truth), f'12번 정답 {truth} = 선지 {IT[12]["ans"]}번')
ok(expand(v12.subs(k, 2) - t * (t - 4)) == 0, '12번 k=2: v = t(t−4), t=0은 출발 시각')
ok(integrate(v12.subs(k, 3), (t, 0, 2)) == Rational(2, 3), '12번 오답 ㄱ, ㄷ: k=3에서 위치의 변화량 2/3을 거리로')
ok(len(solve(v12.subs(k, 2), t)) == 2, '12번 오답 ㄱ, ㄴ: v=0인 두 시각 0, 4를 모두 전환으로 셈')
# 원문 J72: ㄱ 참, ㄴ 거짓, ㄷ 참 → ③
vo2 = t**2 - k * t + 4
ok(integrate(vo2.subs(k, 0), (t, 0, 1)) == Rational(13, 3) and sp.discriminant(vo2.subs(k, 3), t) < 0 and dist(vo2.subs(k, 5), 0, 2) == 3, '12번 원문 J72 ㄱ 참·ㄴ 거짓·ㄷ 참 → ③')
print(f'{len(OK)} checks')
print('ALL OK')
