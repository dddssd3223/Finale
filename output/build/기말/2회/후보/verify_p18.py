# -*- coding: utf-8 -*-
# p18.py (2회 18번 Claude 후보, 원본 D45) 검증 — 2차(검토 반영)
# 원문 풀이(102) · 원리(극한 존재 ⇔ f'(a)=0) · 설정 줄 불통 · 경우 분기 기호·격자 전수 조사(유일성) · 정답 = ②
# · 선지 등차 · 오답 값(선지 안) · 조건 빼 보기(빼면 선지만으로 답이 하나로 남지 않음) · 문장 길이 · 원문 골격
import os, re, sys, itertools
import sympy as sp
from sympy import Rational as R
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
sys.path.insert(0, os.path.join(HERE, '..', '..', '지침'))
from items_common import COND
import items_final as F
x, t, a = sp.symbols('x t a', real=True)
ns = {}; exec(open(os.path.join(HERE, 'p18.py')).read(), ns)
it = ns['ITEMS'][18]
assert it['author'] == 'claude' and it['cand'] == 'claude18' and it['key'] == 'D45' and it['ans'] == 2
assert it['core']['axis'] == '②' and [k for k, _ in it['cond']] == ['가', '나']
assert it['effect'] == '어려워짐' and it['bunseok'] is False and '함정 추가' not in it['vtype']
CH = [sp.nsimplify(v) for v in it['choices']]

# ---------- 원문 D45 ----------
b2, b1, b0 = sp.symbols('b2 b1 b0')
fo = x**3 + b2*x**2 + b1*x + b0
so = sp.solve([fo.subs(x, -2) - 2, sp.diff(fo, x).subs(x, -2), sp.diff(fo, x).subs(x, 4)], [b2, b1, b0], dict=True)
assert len(so) == 1
fo = fo.subs(so[0])
assert sp.expand(fo - (x**3 - 3*x**2 - 24*x - 26)) == 0
assert sp.limit((fo - 2) / (x + 2)**2, x, -2).is_finite
assert all(fo.subs(x, R(v, 10)) >= fo.subs(x, 4) for v in range(31, 50))
assert fo.subs(x, 8) == 102 and F.I['D45'][2] == '102'
print('원문 D45: f=x^3-3x^2-24x-26, f(8)=102 OK')

# ---------- 원리: lim (f(x)-f(a))/(x-a)^2 존재 ⇔ f'(a)=0 ----------
c = sp.symbols('c0:5')
g = sum(c[k] * x**k for k in range(5))
ratio = sp.cancel((g - g.subs(x, a)) / (x - a))
assert sp.expand(ratio.subs(x, a) - sp.diff(g, x).subs(x, a)) == 0
print("원리: (f(x)-f(a))/(x-a) → f'(a) 이므로 극한 존재 ⇔ f'(a)=0")

# ---------- 도구 ----------
def fP(fp):
    """f'(최고차항 4)로부터 f(0)=0인 f"""
    return sp.expand(sp.integrate(fp.subs(x, t), (t, 0, x)))

def crit(f):
    return sorted(set(sp.real_roots(sp.Poly(sp.diff(f, x), x))))

def ok_ga(f, need=('개수', '정수', '합')):
    S = crit(f); r = True
    if '개수' in need: r &= (len(S) == 2)
    if '정수' in need: r &= all(s.is_integer for s in S)
    if '합' in need: r &= (sum(S) == 5)
    return bool(r)

def ok_na(f):
    """열린구간 (3,9/2)에서 최솟값 존재 ⇔ 구간 안 임계점 중 최소 f(c)가 f(3), f(9/2) 이하"""
    cs = [s for s in crit(f) if 3 < s < R(9, 2)]
    if not cs: return False
    m = min(f.subs(x, s) for s in cs)
    return bool(m <= f.subs(x, 3) and m <= f.subs(x, R(9, 2)))

def minval(f):
    fp = sp.diff(f, x)
    return [f.subs(x, s_) for s_ in crit(f) if fp.subs(x, s_ - R(1, 1000)) < 0 < fp.subs(x, s_ + R(1, 1000))]

def ok(f, need=('개수', '정수', '합', '나')):
    r = ok_ga(f, tuple(k for k in need if k != '나'))
    if '나' in need: r &= ok_na(f)
    return bool(r)

# ---------- 설정 줄 불통 ----------
# 원문 설정 줄: '두 극점이 정해지면 f'가 정해진다'. 사차에서는 두 근 1, 4를 알아도 어느 쪽이 중근인지(또는 셋째 근) 남는다.
fam = {sv: fP(4*(x - 1)*(x - 4)*(x - sv)).subs(x, 4) for sv in (1, 4, 0)}
assert len(set(fam.values())) == 3
print("설정 줄 불통: f'(1)=f'(4)=0, f(0)=0, 최고차항 1이어도 f'=4(x-1)(x-4)(x-s)로 s가 남음, f(4) =", fam)

# ---------- 기호: 근 구조와 (나) ----------
for fp, n in ((4*(x+1)*(x-1)*(x-3), 3), (4*(x-1)**2*(x-4), 2), (4*(x-2)**3, 1), (4*(x-1)*(x**2+1), 1)):
    assert len(crit(fP(fp))) == n
p, q, e = sp.symbols('p q e', real=True)
fpq = 4*(x - p)**2*(x - q)
assert sp.factor(fpq.subs(x, p - e) * fpq.subs(x, p + e)) == sp.factor(16*e**4*(p - e - q)*(p + e - q))      # 중근: 부호 그대로
assert sp.factor(fpq.subs(x, q - e) * fpq.subs(x, q + e)) == sp.factor(-16*e**2*(q - e - p)**2*(q + e - p)**2)  # 단순근: 부호 바뀜
# (나): 극소점이 q 하나뿐 → (3,9/2)에서 최솟값 존재 ⇔ 3<q<9/2  (q<=3: 증가, q>=9/2: 감소)
for pv, qv, exp in ((1, 4, True), (7, R(7, 2), True), (4, 1, False), (0, 3, False), (0, 5, False), (4, R(9, 2), False), (2, R(17, 4), True)):
    assert ok_na(fP(4*(x - pv)**2*(x - qv))) == exp, (pv, qv)
sols_int = [(pv, 5 - pv) for pv in range(-30, 31) if pv != 5 - pv and 3 < 5 - pv < R(9, 2)]
assert sols_int == [(1, 4)]
fA = fP(4*(x - 1)**2*(x - 4))
assert sp.expand(fA - (x**4 - 8*x**3 + 18*x**2 - 16*x)) == 0
assert sp.expand(fA - ((x - 1)**3*(x - 5) - 5)) == 0
r_ = sp.symbols('r')
assert sp.solve(sp.Poly(sp.expand(sp.diff((x - 1)**3*(x - r_), x) - 4*(x - 1)**2*(x - 4)), x).coeffs(), r_, dict=True) == [{r_: 5}]
assert ok(fA) and crit(fA) == [1, 4]
ans = fA.subs(x, 4)
assert minval(fA) == [ans] and ans == -32 and fA.subs(x, 1) == -5 and CH[it['ans'] - 1] == ans
print(f'유일한 f(x) = {fA} = (x-1)^3(x-5)-5, 극솟값 f(4) = {ans} = ②')

# ---------- 격자 전수 조사: f'의 근 구조 전부 ----------
Gr = [R(k, 2) for k in range(-6, 17)]           # -3 ~ 8, 0.5 간격
sols = set(); cnt = 0
for r1, r2, r3 in itertools.combinations_with_replacement(Gr, 3):
    f_ = fP(4*(x - r1)*(x - r2)*(x - r3)); cnt += 1
    if ok(f_): sols.add((r1, r2, r3))
for r1 in Gr:                                    # 실근 하나 + 허근 둘
    for al in (0, 2, 4):
        for be in (1, 2):
            f_ = fP(4*(x - r1)*((x - al)**2 + be**2)); cnt += 1
            assert not ok_ga(f_, ('개수',))
assert sols == {(1, 1, 4)}, sols
print(f"격자 {cnt}개 f' 중 (가)(나)를 모두 만족시키는 것은 f'=4(x-1)^2(x-4) 하나")

# ---------- 선지 ----------
dif = {CH[i + 1] - CH[i] for i in range(4)}
assert len(set(CH)) == 5 and dif == {5}
print('선지', [str(v) for v in CH], '공차 5 (오름차순), 정답 ②')

# ---------- 오답 (선지 안) ----------
W1 = fP(4*(x - 1)*(x - 4)**2)                    # 구간 안 정수 4를 f'의 중근으로 (최솟값 판별 생략)
assert ok_ga(W1) and not ok_na(W1)               # (가) 만족, (나)만 위반
assert sp.diff(W1, x).subs(x, R(7, 2)) > 0 and sp.diff(W1, x).subs(x, R(17, 4)) > 0   # 구간에서 증가
assert sp.expand(W1 - (x**4 - 12*x**3 + 48*x**2 - 64*x)) == 0
W2 = sp.expand((x - 1)**3*(x - 5))               # f(0)=0을 빠뜨림 (f(1)=0으로 둠)
W3 = sp.expand((x - 1)**3*(x - 5) + 5)           # f(0)-f(1)=(-1)^3(-5)의 부호를 틀려 f(1)=5
assert ok(W2) and W2.subs(x, 0) != 0 and W3.subs(x, 0) == 10
w1, w2, w3 = minval(W1), minval(W2), minval(W3)
assert (w1, w2, w3) == ([-27], [-27], [-22])
assert it['wrongs'] == ['-27', '-22'] and all(sp.nsimplify(w) in CH for w in it['wrongs'])
for s_ in ('-27', '-22', '4(x-1)(x-4)^2', 'x^4-12x^3+48x^2-64x', 'f(1)=5'):
    assert s_ in it['wrong'], s_
print("오답 (선지 안): -27 (4를 f'의 중근으로 둔 함수의 극솟값, (나) 위반 / f(0)=0 빠뜨림), -22 (f(1)의 부호 실수)")

# ---------- 조건 빼 보기 ----------
print('--- 조건 빼 보기 ---')
three, dbl_ok = [], []
for u, v in itertools.combinations(range(-20, 26), 2):
    w = 5 - u - v
    if w > v:
        f_ = fP(4*(x - u)*(x - v)*(x - w))
        if ok_na(f_): three.append(((u, v, w), minval(f_)))
    for d_, s_ in ((u, v), (v, u)):
        if d_ + s_ == 5 and ok_na(fP(4*(x - d_)**2*(x - s_))): dbl_ok.append((d_, s_))
assert dbl_ok == [(1, 4)] and not ok_na(fP(4*(x - 5)**3)) and not ok_na(fP(4*(x - 5)*(x**2 + 1)))
assert three and all(len(v_) == 2 for _, v_ in three)
print('경우 분기: 실근 하나(5)·삼중근은 (나) 불만족, 중근+단순근은 (중근 1, 단순근 4)만, 세 정수 근은 개수 조건으로 제외')
print(f"ABLATION 18 (가) 개수: 필요(정해지지 않음: 세 정수 근(합 5)도 (나) 만족 {len(three)}개, 예 {three[0][0]} 극솟값 {three[0][1]})")
altv = {}
for pv in (R(3, 2), R(3, 4), R(5, 4)):
    f_ = fP(4*(x - pv)**2*(x - (5 - pv)))
    assert ok(f_, ('개수', '합', '나')) and not ok(f_)
    altv[pv] = minval(f_)[0]
assert len(set(altv.values()) | {ans}) == 4
print(f'ABLATION 18 (가) 정수: 필요(정해지지 않음: p=3/2→{altv[R(3,2)]}, p=3/4→{altv[R(3,4)]}, p=5/4→{altv[R(5,4)]})')
altw = {}
for pv in (0, 2, -1, 3):
    f_ = fP(4*(x - pv)**2*(x - 4))
    assert ok(f_, ('개수', '정수', '나')) and not ok(f_)
    altw[pv] = minval(f_)[0]
assert len(set(altw.values()) | {ans}) == 5
print(f"ABLATION 18 (가) 합 5: 필요(정해지지 않음: f'=4(x-p)^2(x-4), p=0→{altw[0]}, p=2→{altw[2]}, p=-1→{altw[-1]}, p=3→{altw[3]})")
altn = {}
for pv in range(-6, 12):
    qv = 5 - pv
    if pv == qv: continue
    f_ = fP(4*(x - pv)**2*(x - qv))
    assert ok(f_, ('개수', '정수', '합'))
    altn[(pv, qv)] = minval(f_)[0]
listed = {k: v for k, v in altn.items() if v in CH}
assert listed == {(1, 4): -32, (4, 1): -27, (2, 3): -27}, listed   # (2,3): 단순근 3이 열린구간 끝점 → (나) 불만족
print(f'ABLATION 18 (나): 필요(정해지지 않음: (가)만이면 (중근,단순근)=(1,4)→-32, (4,1)→-27, (2,3)→-27(끝점 3) 모두 선지에 있음, 그 밖 (0,5)→{altn[(0, 5)]} 등)')
assert minval(fA + 7) != [ans] and ok(fA + 7)
print('ABLATION 18 f(0)=0: 필요(정해지지 않음: 상수항 자유, f(1)=0으로 두면 -27이 선지에 있음)')
print('조건 하나만 어긴 값: (나) 최솟값 판별 생략 → -27(③), f(0)=0 빠뜨림 → -27, f(1) 부호 실수 → -22(④) — 선지만 보고 조건을 건너뛸 수 없음')

# ---------- 문장 길이 ----------
L = lambda html: len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', html)))
Lo = L(F.I['D45'][0]); Lm = L(it['body'] + COND(it['cond']))
assert Lo == 184 and Lm >= Lo, (Lo, Lm)
print(f'문장 길이: 원문 {Lo}자, 변형 {Lm}자 (조건 {len(it["cond"])}개, 원문 2개)')

# ---------- 원문 골격 ----------
import dupcheck as DC
A_ = set(DC.shingles(DC.skel(DC.norm(it['body'] + COND(it['cond']))))); B_ = set(DC.shingles(DC.skel(DC.norm(F.I['D45'][0]))))
jd = len(A_ & B_) / len(A_ | B_)
assert jd <= 0.25, jd
print(f'원문 골격 유사도 {jd:.2f} (17·18 목표 0.25 이하)')
assert '\\[' not in it['body'] + COND(it['cond'])
print('ALL OK')
