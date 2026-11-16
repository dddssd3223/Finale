# -*- coding: utf-8 -*-
# 17번 후보 A17 수정본 (J39 킬러 설계A: 누적 최댓값 M(T), 위치 차가 두 번 부호를 바꿈, 거리 < M(T) 인 T 의 범위 α<T<β, α+β) 검증 · author='claude'
import sympy as sp, os, sys
t, a = sp.symbols('t a', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5.py')).read(), ns)
IT = ns['ITEMS'][17]


def pos_diff(av, c1=4, c2=-36, k=3, x20=0):
    """x1-x2, v1 = k t^2 + c1, v2 = av t + c2, P 는 원점·Q 는 x20 에서 출발"""
    s = sp.Symbol('s')
    return sp.expand(sp.integrate(k * s**2 + c1 - (av * s + c2), (s, 0, t)) - x20)


def region(D, Tmax=30.0, n=30000):
    """|D(T)| < M(T) 인 T 들(격자) → 연결 구간 목록 [(왼끝, 오른끝)]"""
    f = sp.lambdify(t, sp.Abs(D))
    run, segs, cur = -1.0, [], None
    h = Tmax / n
    for i in range(n + 1):
        x = i * h; v = float(f(x)); run = max(run, v)
        inside = v < run - 1e-9
        if inside and cur is None: cur = [x - h, x]
        elif inside: cur[1] = x
        elif cur is not None: cur[1] = x; segs.append(tuple(round(c, 2) for c in cur)); cur = None
    if cur is not None: segs.append((round(cur[0], 2), None))
    return segs


# ---------- 1) '시각 5에서 만남' → a = 26 (일차식, 유일)
Da = pos_diff(a)
assert sp.expand(Da - t * (t**2 - a / 2 * t + 40)) == 0
asol = sp.solve(Da.subs(t, 5), a); assert asol == [26]
D = sp.expand(Da.subs(a, 26)); assert sp.expand(D - t * (t - 5) * (t - 8)) == 0
assert sorted({r for r in sp.real_roots(sp.Poly(D, t)) if r > 0}) == [5, 8]
print('t=5 에서 만남 → a=26 (유일), D = t(t-5)(t-8): 두 점은 t=5, 8 에서 만나고 5<t<8 에서 Q 가 앞섬')

# ---------- 2) 극값·접힌 봉우리·경계 9 (정확)
assert sp.factor(sp.diff(D, t)) == sp.factor((t - 2) * (3 * t - 20))
h1, h2 = D.subs(t, 2), D.subs(t, R(20, 3))
assert h1 == 36 and h2 == R(-400, 27) and abs(h2) < h1
assert sp.expand(D - 36 - (t - 2)**2 * (t - 9)) == 0
# 0≤t≤9 에서 |D|≤36, 등호는 t=2, 9 뿐
assert sp.solve_univariate_inequality(D <= 36, t, relational=False).contains(R(85, 10))
assert sp.solve(sp.Eq(D, 36), t) == [2, 9]
eq_neg = [r for r in sp.real_roots(sp.Poly(D + 36, t)) if 0 <= r <= 9]
assert eq_neg == [], eq_neg                                   # 접힌 쪽(-D=36)은 [0,9] 안에서 안 생김
segs = region(D)
assert len(segs) == 1 and abs(segs[0][0] - 2) < 0.01 and abs(segs[0][1] - 9) < 0.01, segs
alpha, beta = 2, 9
ANS = alpha + beta
print(f'극댓값 D(2)=36, 접힌 봉우리 |D(20/3)|=400/27<36, D-36=(t-2)^2(t-9); 격자 {segs} → α=2, β=9, α+β={ANS}')
# M(T) 세 갈래 (정확값 표본)
def M_exact(Tv):
    cands = [0, Tv] + [c for c in (2, R(20, 3)) if c <= Tv]
    return max(abs(D.subs(t, c)) for c in cands)
assert [M_exact(Tv) for Tv in (1, 3, 6, 7, 9, 10)] == [D.subs(t, 1), 36, 36, 36, 36, D.subs(t, 10)]
assert M_exact(10) == 100 and abs(D.subs(t, 7)) == 14

ch = IT['choices']
assert ch[IT['ans'] - 1] == str(ANS) and IT['ans'] == 2
assert len(set(ch)) == 5 and {int(ch[i + 1]) - int(ch[i]) for i in range(4)} == {-1}
print('정답 11 = 선지 ②, 선지 12..8 공차 1 내림차순')

# ---------- 3) 오답 근거
w10 = 2 + 8      # 두 번째 만남(8) 뒤 거리 증가를 최댓값 갱신으로 봄: 2<T<8
w9 = 0 + 9       # M(T)=36 을 처음부터: 0<T<9
w8 = 0 + 8       # 둘 다
assert all(abs(D.subs(t, x)) < 36 for x in (R(17, 2), R(9, 1) - R(1, 10)))        # 8<T<9 에서 실제로 거리 < 36 → 10 은 틀림
assert all(sp.diff(D, t).subs(t, x) > 0 for x in (R(1, 2), 1, R(3, 2)))            # T<2 에서 거리 증가 → 거리 = M(T) → 9 는 틀림
assert {str(w10), str(w9), str(w8)} == set(IT['wrongs']) and all(w in ch for w in IT['wrongs'])
for v in (2 + 5, 9 - 2, 6):   # 다른 흔한 값(첫 만남 5까지·β-α·a/만남 관련)이 정답과 겹치지 않음
    assert v != ANS
assert ANS not in (5, 8, 26, 2, 9)
print('오답 근거 OK: 10(8 뒤 갱신으로 봄) · 9(T≤2 끝값 누락) · 8(둘 다); 정답 11 은 만남 시각·극점·a 와 다름')

# ---------- 4) 원문 J39 직접 풀기: 20/3
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as Fm
o = Fm.I['J39']
assert o[2] == '③' and o[1][2] == r'\dfrac{20}3'
d0 = sp.integrate(2 * t**3 - 2 * t - (t**2 + 4 * t), (t, 0, t))
cands = [0, 3] + [r for r in sp.solve(sp.diff(d0, t), t) if 0 <= r <= 3]
assert max(abs(d0.subs(t, c)) for c in cands) == R(20, 3)
print('원문 J39 OK: |d(2)|=20/3 > |d(3)|=9/2 → 20/3 (원문 ③), 변형 답 11 과 다름')

# ---------- 5) 핵심 한 줄 (②형: 원문 설정 줄 불통, 원리 줄은 T 마다·절댓값 비교로 다시 씀)
body = IT['body']
assert '2t^3' not in body and 'M(T)' in body and 't=5' in body
print('핵심: 원문 설정 줄(사차 위치 차·[0,3]) 불통, 원리 줄(극값·끝값 절댓값 비교)은 T 마다 세 갈래 + 접힌 봉우리 비교')

# ===== 조건 빼 보기 (ABLATION) =====
print('--- 조건 빼 보기 ---')
def ablation(cname, res, why=''):
    print(f'ABLATION 17 {cname}: 필요({res}{"; " + why if why else ""})')
    assert res != ANS

# (1) 't=5 에서 만남' 빼기: a 가 남음
outs = {}
for av in (24, 26, 28):
    sg = region(pos_diff(av)); outs[av] = sg
assert len({str(v) for v in outs.values()}) == 3
ablation("'시각 t=5에서 만남'", f'정해지지 않음({outs})', 'a 가 남음')
# (2) '동시에 원점에서 출발' 빼기: Q 가 원점이 아닌 곳(예: 10)에서 출발하면 a 와 범위가 바뀜
D2a = pos_diff(a, x20=10); a2 = sp.solve(D2a.subs(t, 5), a)[0]
sg2 = region(D2a.subs(a, a2))
assert a2 != 26 and sg2 != segs
ablation("'원점에서 동시에 출발'(Q 가 10 에서 출발)", f'a={a2}, 범위 {sg2}', '')
# (3) v2 의 상수 -36 → 0: a 와 범위가 바뀜(계수 자리 확인)
D3a = pos_diff(a, c2=0); a3 = sp.solve(D3a.subs(t, 5), a)[0]; sg3 = region(D3a.subs(a, a3))
assert sg3 != segs
ablation('v2 의 상수 -36 (→0)', f'a={a3}, 범위 {sg3}', '')
# (4) 거리(|x1-x2|) 대신 위치 차 x1-x2 로 보면? 여기서는 접힌 봉우리가 36 보다 작아 범위는 같음 → 절댓값 비교가 답을 바꾸지 않는지 확인
#     (절댓값 판단은 'M(T) 를 바꾸지 않는다'는 확인 단계: 접힌 봉우리 400/27 < 36 이 성립해야 β=9)
Dbig = t * (t - 3) * (t - 8)      # 접힌 봉우리가 극댓값보다 큰 경우(대조): 범위가 둘로 갈라짐
sgb = region(Dbig)
assert len(sgb) == 2
print(f'대조(접힌 봉우리 36 > 극댓값 400/27 인 t(t-3)(t-8)): 범위 {sgb} 둘로 갈라짐 → 절댓값 비교가 β 를 정하는 판단임')
# (5) 'M(T)보다 작은' 을 '전체 극댓값과 비교'로 바꾸면 0<T<9 → 9 (오답 ④)
ablation("'M(T)보다 작은' (→ 극댓값 36 과 비교)", 9, '끝값 구간이 빠짐')
print('ALL OK')
