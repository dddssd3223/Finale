# -*- coding: utf-8 -*-
# 17번 후보 A17 (J39 킬러 설계A: 누적 최댓값 M(T), 시각 T의 거리 < M(T) 인 T의 범위 길이) 검증 · author='claude'
import sympy as sp, os, sys
t, a, T = sp.symbols('t a T', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def pos_diff(av, c1=1, c2=-8, k=R(3, 4)):
    """x1-x2 (동시에 원점 출발), v1 = k t^2 + c1, v2 = av t + c2"""
    return sp.integrate(k * t**2 + c1 - (av * t + c2), (t, 0, t)).subs(t, t)


def meetings(D):
    """출발한 후(t>0) 만나는 시각들"""
    return sorted({r for r in sp.real_roots(sp.Poly(sp.expand(D), t)) if r > 0})


def region_len(D, Tmax=40, n=8000):
    """dist(T)=|D(T)| < M(T) 인 T 들(격자). (길이, 왼끝, 오른끝, 연결 여부)"""
    f = sp.lambdify(t, sp.Abs(D))
    run, pts = 0.0, []
    h = Tmax / n
    for i in range(n + 1):
        x = i * h; v = f(x); run = max(run, v)
        if v < run - 1e-9: pts.append(x)
    if not pts: return None
    gaps = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
    conn = all(g < 1.5 * h for g in gaps)
    return round(pts[-1] - pts[0] + h, 2), round(pts[0] - h, 2), round(pts[-1] + h, 2), conn


# ---------- 1) 위치 차와 '출발한 후 한 번만 만난다' → a = 6 (전수)
Da = sp.expand(pos_diff(a))
assert sp.expand(Da - t / 4 * (t**2 - 2 * a * t + 36)) == 0
good = []
for av in [R(k, 4) for k in range(-80, 81)] + [6, -6, 6 + R(1, 100), 6 - R(1, 100), -6 - R(1, 100)]:
    if len(meetings(Da.subs(a, av))) == 1: good.append(av)
assert sorted(set(good)) == [6], good
assert meetings(Da.subs(a, -6)) == [] and len(meetings(Da.subs(a, 7))) == 2 and meetings(Da.subs(a, 5)) == []
D = sp.factor(Da.subs(a, 6)); assert sp.expand(D - t * (t - 6)**2 / 4) == 0
print('한 번만 만남: a ∈ [-20,20](1/4 간격)+경계 근방 전수 → a=6 뿐 (a=-6 은 근 -6, a>6 은 두 번, |a|<6 은 안 만남); D = t(t-6)^2/4 ≥ 0')

# ---------- 2) M(T) 조각과 범위 (정확)
assert sp.factor(sp.diff(D, t)) == sp.factor(R(3, 4) * (t - 2) * (t - 6))
assert D.subs(t, 2) == 8 and D.subs(t, 6) == 0
assert sp.expand(D - 8 - (t - 2)**2 * (t - 8) / 4) == 0
# (i) T≤2: D 증가 → M=D (거리 = M)
# (ii) 2≤T≤8: D≤8 → M=8, D(T)<8 ⇔ T≠2,8  (iii) T≥8: D 증가, D≥8 → M=D
assert sp.solve(sp.Eq(D, 8), t) == [2, 8]
sol_lt = sp.solve_univariate_inequality(D < 8, t, relational=False).intersect(sp.Interval(2, 8))
assert sol_lt == sp.Interval.open(2, 8), sol_lt
alpha, beta = 2, 8
ANS = beta - alpha
num = region_len(D, Tmax=20, n=20000)
assert num[3] and abs(num[1] - 2) < 0.01 and abs(num[2] - 8) < 0.01, num
print(f'M(T): T≤2 끝값, 2≤T≤8 극댓값 8, T≥8 끝값; 거리<M(T) ⇔ 2<T<8 (격자 확인 {num}); β-α = {ANS}')

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {2}
print('정답 6 = 선지 ②, 선지 4..12 공차 2 오름차순')

# ---------- 3) 오답 근거
w4 = 6 - 2          # 만난 뒤(t=6) 다시 커지는 거리를 최댓값으로 봄: 2<T<6
w8 = 8 - 0          # M(T)=8 로 보고 0<T<8
# 확인: 만난 뒤 6<T<8 에서 실제로 D(T) < 8 (그래서 4 는 틀림), 0<T<2 에서 D 증가라 거리 = M(T) (그래서 8 은 틀림)
assert all(D.subs(t, x) < 8 for x in (R(13, 2), 7, R(15, 2))) and all(sp.diff(D, t).subs(t, x) > 0 for x in (R(1, 2), 1, R(3, 2)))
assert {str(w4), str(w8)} == set(IT['wrongs']) and all(w in ch for w in IT['wrongs'])
print('오답 근거 OK: 4(만남 뒤 갱신으로 봄, 2<T<6) · 8(끝값 구간 누락, 0<T<8)')

# ---------- 4) 원문 J39 직접 풀기: 20/3
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J39']
assert o[2] == '③' and o[1][2] == r'\dfrac{20}3'
d0 = sp.integrate(2 * t**3 - 2 * t - (t**2 + 4 * t), (t, 0, t))
assert sp.expand(d0 - (t**4 / 2 - t**3 / 3 - 3 * t**2)) == 0
cands = [0, 3] + [r for r in sp.solve(sp.diff(d0, t), t) if 0 <= r <= 3]
omax = max(abs(d0.subs(t, c)) for c in cands)
assert omax == R(20, 3) and abs(d0.subs(t, 3)) == R(9, 2)
assert str(ANS) != '20/3'
print('원문 J39 OK: |d| 최댓값 = |d(2)| = 20/3 (원문 ③), 변형 답 6 과 다름')

# ---------- 5) 핵심 한 줄 (②형: 원문 설정 줄 불통)
body = IT['body']
assert '2t^3' not in body and '0\\le t\\le3' not in body.replace(' ', '') and 'M(T)' in body
# 원문 원리(고정 구간 극값·끝값 비교)를 T 마다 다시 써야 함: 갈래 셋
assert [sp.Max(*[D.subs(t, c) for c in [0, Tv] + [r for r in (2, 6) if r <= Tv]]) for Tv in (1, 5, 7, 10)] == [D.subs(t, 1), 8, 8, D.subs(t, 10)]
print('핵심: 원문 설정 줄(사차 위치 차·[0,3]) 불통, 원리 줄(극값·끝값 비교)은 T 마다 세 갈래로 다시 씀')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    msg = (f'군더더기(답 그대로{"; " + why if why else ""})' if res == ANS else f'필요({res}{"; " + why if why else ""})')
    print(f'ABLATION 17 {cname}: {msg}')
    assert res != ANS

# (1) '출발한 후 한 번만 만난다' 빼기: a 가 정해지지 않음 → 범위 길이가 a 에 따라 다름
lens = {}
for av in (R(11, 2), 7, 8):
    r = region_len(Da.subs(a, av), Tmax=40, n=8000); lens[str(av)] = r[0] if r else None
assert len(set(lens.values())) == 3 and all(v is not None for v in lens.values()), lens
ablation("'출발한 후 한 번만 만난다'", f'정해지지 않음({lens})', 'a 가 남음')
# (2) '출발한 후' 빼기: t=0 도 만남으로 세면 '한 번만' = 출발 뒤 안 만남 → |a|<6 또는 a≤-6, 하나로 안 정해짐
r55 = region_len(Da.subs(a, R(11, 2)), Tmax=40, n=8000); r0 = region_len(Da.subs(a, 0), Tmax=40, n=8000)
assert r55 is not None and r0 is None
ablation("'출발한 후'", f'정해지지 않음(a=11/2 길이 {r55[0]}, a=0 범위 없음)', 't=0 을 만남으로 세면 a 가 남음')
# (3) v2 의 상수 -8 을 0 으로 (계수 자리 확인): 한 번만 만나는 a 가 a^2=4 → a=2, 범위 길이 2
D3 = sp.expand(sp.integrate(R(3, 4) * t**2 + 1 - a * t, (t, 0, t)))
g3 = [av for av in [R(k, 4) for k in range(-40, 41)] if len(meetings(D3.subs(a, av))) == 1]
assert g3 == [2]
r3 = region_len(D3.subs(a, 2), Tmax=20, n=20000)
assert abs(r3[0] - 2) < 0.01
ablation('v2 의 상수 -8 (→0)', 2, '중근 위치가 바뀜')
# (4) '동시에 원점을 출발' 빼기: Q 가 c 에서 출발하면 D 에 -c 가 붙어 만남 조건·범위가 바뀜 (c=2 예)
D4 = Da - 2
g4 = sorted({av for av in [R(k, 4) for k in range(-80, 81)] if len(meetings(D4.subs(a, av))) == 1})
assert len(g4) > 1
ablation("'동시에 원점을 출발'", f'정해지지 않음(Q 가 2 에서 출발하면 한 번만 만나는 a 가 {len(g4)}개 이상)', '')
# (5) 비교 대상 'M(T)' 를 '극댓값 8' 같은 고정값으로 두면 0<T<8 → 8 (오답 ③) : 묻는 식이 일함
ablation("'M(T)보다 작도록' (→ 전체 최댓값과 비교)", 8, '끝값 구간이 빠짐')
print('ALL OK')
