"""17번(L42 변형) sympy 검증."""
import importlib.util, os, re, sys
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('p17', os.path.join(HERE, 'p17.py'))
p17 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p17)
item = p17.ITEMS[17]

x, k, t = sp.symbols('x k t', real=True)
FAIL = []
def check(ok, msg):
    print(('OK   ' if ok else 'FAIL ') + msg)
    if not ok: FAIL.append(msg)

# ---------------------------------------------------------------- f (그림)
# 그림: x<0 에서 (x+3)(x-3)/9, 0<=x<1 에서 삼차 조각(값 양수, f(0)=1, x->1- 에서 0), x>=1 에서 -x+3.
# 삼차 조각의 정확한 식은 답에 쓰이지 않는다. 수치 확인용으로 그림 조건을 만족하는 하나를 쓴다.
ALPHA, BETA = sp.Rational(-1, 2), sp.Integer(2)          # alpha*beta = -1, gamma = 1
cubic = (t - ALPHA) * (t - BETA) * (t - 1)
assert cubic.subs(t, 0) == 1 and cubic.subs(t, 1) == 0
assert all(cubic.subs(t, sp.Rational(i, 100)) > 0 for i in range(100))
def f_num(v):
    v = mp.mpf(v)
    if v < 0: return (v + 3) * (v - 3) / 9
    if v < 1: return (v - mp.mpf(-0.5)) * (v - 2) * (v - 1)
    return -v + 3
# f 의 불연속점과 좌우 극한 (그림에서 읽는 값)
LEFT = {0: -1, 1: 0}; VAL = {0: 1, 1: 2}; RIGHT = {0: 1, 1: 2}

# ---------------------------------------------------------------- 원문 정답 12
a_, b_, c_ = sp.symbols('a b c')
al, be = sp.symbols('alpha beta')
G = x**3 + a_*x**2 + b_*x + c_
# a=0: 좌극한 g(0)/(-1), 우극한 g(0)/1 -> 같아야 함
e1 = sp.Eq(G.subs(x, 0) / -1, G.subs(x, 0) / 1)
# a=1: 우극한 g(1)/2, 좌극한은 분모 -> 0 이므로 g(1)=0 이어야 유한, 그때 좌극한 = g'(1)/((1-al)(1-be)) = 우극한 0
e2 = sp.Eq(G.subs(x, 1), 0)
e3 = sp.Eq(sp.diff(G, x).subs(x, 1) / ((1 - al) * (1 - be)), 0)
sol0 = sp.solve([e1, e2, e3], [a_, b_, c_], dict=True)
g0 = G.subs(sol0[0])
check(len(sol0) == 1 and sp.expand(g0 - x*(x-1)**2) == 0, f'원문: g(x)=x(x-1)^2 유일 ({sp.factor(g0)})')
# 구체적인 삼차 조각으로 극한 직접 확인
fpiece = (x - ALPHA) * (x - BETA) * (x - 1)
lim1m = sp.limit(g0 / fpiece, x, 1, '-'); lim1p = sp.limit(g0 / (-x + 3), x, 1, '+')
lim0m = sp.limit(g0 / ((x+3)*(x-3)/9), x, 0, '-'); lim0p = sp.limit(g0 / fpiece, x, 0, '+')
check(lim1m == lim1p == 0 and lim0m == lim0p == 0, '원문: x=0, x=1 에서 좌우 극한 일치')
check(g0.subs(x, 3) == 12, f'원문 정답 g(3) = {g0.subs(x, 3)} (=12)')

# ---------------------------------------------------------------- 변형: 불연속점 판정
def disc_points(kv, rule='correct'):
    """f(g(x)) 의 불연속점 (정확한 대수적 수) 목록.
    rule='correct': g(x)=c 의 근에서 좌우 모두 g>=c 이면 연속(극소 접촉), 아니면 불연속.
    rule='touch'  : 오답 규칙 - g(x)=c 의 모든 근을 불연속으로 센다."""
    g = x**3 - 3*x**2 + kv
    out = []
    for c in (0, 1):
        _, facs = sp.sqf_list(sp.Poly(g - c, x))
        for fac, m in facs:
            for r in sp.real_roots(fac):
                d = sp.diff(g, x, m).subs(x, r)
                dval = sp.N(d, 50)
                right = sp.sign(dval); left = sp.sign(dval) * (-1)**m
                cont = (left >= 0 and right >= 0)
                if rule == 'touch' or not cont:
                    out.append((r, c, m))
    return out

def numeric_disc(kv, r):
    """구체적인 f 로 x=r 좌우 값을 수치로 비교 (불연속이면 True)."""
    mp.mp.dps = 50
    gf = lambda xx: xx**3 - 3*xx**2 + mp.mpf(sp.N(kv, 60))
    rr = mp.mpf(sp.N(r, 60)); eps = mp.mpf('1e-20')
    v0 = f_num(gf(rr)) if abs(gf(rr) - round(float(gf(rr)))) > mp.mpf('1e-30') else f_num(round(float(gf(rr))))
    vl, vr = f_num(gf(rr - eps)), f_num(gf(rr + eps))
    return abs(vl - v0) > mp.mpf('1e-6') or abs(vr - v0) > mp.mpf('1e-6')

def h(kv, rule='correct'):
    return len(disc_points(kv, rule))

def answer(kv):
    return sp.nsimplify(sp.N(sum(r for r, _, _ in disc_points(kv)), 60), rational=False, tolerance=1e-40)

# 전체 k 에 대한 개수 표 (경계 k = 0, 1, 4, 5: 극댓값 k, 극솟값 k-4 가 0 또는 1)
reps = [-1, 0, sp.Rational(1, 2), 1, 2, 4, sp.Rational(9, 2), 5, 6]
table = {kv: h(kv) for kv in reps}
print('h(k) 표:', {str(kk): vv for kk, vv in table.items()})
check(table == {-1: 2, 0: 3, sp.Rational(1, 2): 4, 1: 5, 2: 6, 4: 4, sp.Rational(9, 2): 4, 5: 2, 6: 2},
      'h(k): k<0:2, 0:3, (0,1):4, 1:5, (1,4):6, 4:4, (4,5):4, 5:2, k>5:2')
# 수치 교차 확인 (구체적 f 로 좌우 극한 비교)
numok = True
for kv in [4, 5, sp.Rational(1, 2), sp.Rational(9, 2), 0, 1]:
    g = x**3 - 3*x**2 + kv
    for c in (0, 1):
        for r in set(sp.real_roots(sp.Poly(g - c, x))):
            inlist = any(sp.simplify(r - q) == 0 for q, _, _ in disc_points(kv))
            if numeric_disc(kv, r) != inlist:
                numok = False; print('  수치 불일치', kv, c, r)
check(numok, '판정 규칙과 구체적 f 의 수치 좌우 극한 비교 일치 (k=0,1/2,1,4,9/2,5)')

# (나): x=-1 에서 불연속 <=> g(-1) in {0,1} 이고 그 점이 불연속 (그 밖의 값이면 f 가 연속이라 f(g(x)) 연속)
cand_na = []
for c in (0, 1):
    for kv in sp.solve(sp.Eq((x**3 - 3*x**2 + k).subs(x, -1), c), k):
        if any(sp.simplify(r + 1) == 0 for r, _, _ in disc_points(kv)):
            cand_na.append(kv)
check(sorted(cand_na) == [4, 5], f'(나) 만족 k = {cand_na} (경우 전수: g(-1)=0 또는 1)')

# (가)∧(나): 전수
sols = [kv for kv in cand_na if h(kv) == 4]
check(sols == [4], f'(가)∧(나) 만족 k = {sols} (유일)')
K = sols[0]
dp = disc_points(K)
print('k=4 불연속점:', [(sp.N(r, 8), c) for r, c, _ in dp])
ans_val = answer(K)
vieta = -1 + 3   # x=-1 과 x^3-3x^2+3=0 의 세 근의 합
check(ans_val == 2 and vieta == 2, f'정답(불연속점의 합) = {ans_val}')
check(any(sp.simplify(r - 2) == 0 for r in sp.real_roots(sp.Poly(x**3 - 3*x**2 + 4, x))) and
      not any(sp.simplify(r - 2) == 0 for r, _, _ in dp), '경계 함정: k=4 에서 x=2 (극솟값 0 접점) 는 연속')

# ---------------------------------------------------------------- 선지
def num(s): return sp.sympify(re.sub(r'\\\(|\\\)', '', s))
ch = [num(s) for s in item['choices']]
diffs = {ch[i+1] - ch[i] for i in range(4)}
check(len(diffs) == 1, f'선지 등차 {ch} 공차 {diffs}')
check(ch.count(ans_val) == 1 and ch[item['ans'] - 1] == ans_val, f'정답 {ans_val} 이 선지에 정확히 한 번, ans={item["ans"]}')

# 오답 근거
w_touch = sp.nsimplify(sp.N(sum(r for r, _, _ in disc_points(K, 'touch')), 60), tolerance=1e-40)  # x=2 포함
w_g0only = sum(sp.roots(sp.Poly(x**3 - 3*x**2 + 4, x)).get(r, 0) * r for r in sp.roots(sp.Poly(x**3 - 3*x**2 + 4, x)))  # 중복도 포함 -1+2+2
w_vieta2 = 3 + 3   # 두 방정식 근의 합 그대로
print(f'오답 근거: 접점 포함 {w_touch}, g=0만(중근 중복) {w_g0only}, 두 방정식 근과 계수 그대로 {w_vieta2}')
wrongs = {'경계 함정(x=2 포함)': w_touch, '경우 누락(g=1 누락)': w_g0only, '중근·연속점 포함': w_vieta2}
check(all(v in ch and v != ans_val for v in wrongs.values()) and len(set(wrongs.values())) == 3,
      f'오답 근거 3개가 서로 다른 선지에 있음 {wrongs}')
# 오답 규칙(접점도 불연속)으로는 (가)∧(나) 만족 k 가 없다
check([kv for kv in cand_na if h(kv, 'touch') == 4] == [], '접점 오판 규칙이면 k=4 의 개수 5, k=5 의 개수 3 -> 해 없음 (함정 작동)')

# ---------------------------------------------------------------- 조건 빼 보기
# (가) 제거: (나)만
ans_wo_ga = {kv: sp.N(sum(r for r, _, _ in disc_points(kv)), 12) for kv in cand_na}
ok = len(set(ans_wo_ga.values())) > 1
check(ok, 'ablation (가)')
print(f"ABLATION (가) 불연속인 x의 개수 4: 필요(빼면 k=4,5 -> 합 {[str(v) for v in ans_wo_ga.values()]}, 답이 정해지지 않음)")
# (나) 제거: (가)만 -> k in (0,1) ∪ [4,5)
samp = [sp.Rational(1, 2), sp.Rational(1, 4), 4, sp.Rational(9, 2)]
assert all(h(kv) == 4 for kv in samp)
ans_wo_na = {str(kv): sp.N(sum(r for r, _, _ in disc_points(kv)), 12) for kv in samp}
ok = len(set(ans_wo_na.values())) > 1
check(ok, 'ablation (나)')
print(f"ABLATION (나) x=-1에서 불연속: 필요(빼면 k는 (0,1)∪[4,5)의 모든 값, 예 {ans_wo_na} -> 답이 정해지지 않음)")
# 본문 조건: g(x)=x^3-3x^2+k 의 k 는 미지수 정의이고, 그래프는 설정이다. 그래프의 채운 점 위치(f(0)=1, f(1)=2) 가 바뀌면?
#   f 가 왼쪽 연속(f(0)=-1, f(1)=0) 이라면 '아래에서 닿는 점'이 연속이 되어 판정이 뒤집힌다.
def disc_left(kv):
    g = x**3 - 3*x**2 + kv; out = []
    for c in (0, 1):
        _, facs = sp.sqf_list(sp.Poly(g - c, x))
        for fac, m in facs:
            for r in sp.real_roots(fac):
                dval = sp.N(sp.diff(g, x, m).subs(x, r), 50)
                right = sp.sign(dval); left = sp.sign(dval) * (-1)**m
                if not (left <= 0 and right <= 0): out.append(r)
    return out
alt = [kv for kv in (4, 5) if len(disc_left(kv)) == 4]
print(f"ABLATION 그림의 채운 점(f 오른쪽 연속): 필요(왼쪽 연속으로 바꾸면 (가)∧(나) 만족 k = {alt}, 답이 바뀜/정해지지 않음)")
check(alt != [4], 'ablation 채운 점')

print()
print('ALL OK' if not FAIL else f'FAILED: {FAIL}')
sys.exit(1 if FAIL else 0)
