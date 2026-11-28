# -*- coding: utf-8 -*-
# 13회 서답형2 (D62 후보_순위 3 학교식, 답만 3단계) 검증 · author='claude'
import sympy as sp, os, sys, re
x, d, r = sp.symbols('x d r', real=True)
a, b, c, m, n = sp.symbols('a b c m n', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p7b.py')).read(), ns)
S2 = ns['SITEMS']['S2']
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F


def abs_diffable(q, lo=None, hi=None):
    """|q|가 열린구간 (lo, hi)에서 미분가능한가: 구간 안 실근마다 q'=0 (다항식 q의 근에서 |q| 미분가능 ⇔ 중복도 2 이상)"""
    for rt in sp.Poly(q, x).real_roots():
        if (lo is None or rt > lo) and (hi is None or rt < hi) and sp.diff(q, x).subs(x, rt) != 0: return False
    return True


def solve_all(lead, p, side, zero, pt, val, gdeg=1):
    """일반형 h: side='R'이면 f+g (x≤p), |f-g| (x>p) / 'L'이면 |f-g| (x<p), f+g (x≥p).
    f=lead·x^3+ax^2+bx+c, g=mx+n(m≠0). h가 실수 전체에서 미분가능, h(zero)=0, h(pt)=val(절댓값 쪽 점)인 (f, g) 전부.
    q=f-g의 영점 zero에서 제곱 인수 → q=lead(x-zero)^2(x-d), |q(pt)|=val에서 d 후보 → 구간 미분가능성 → 이음점 부호별 연립"""
    out = []
    q0 = lead * (x - zero)**2 * (x - d)
    for sg in (1, -1):
        for dv in sp.solve(sp.Eq(q0.subs(x, pt), sg * val), d):
            q = q0.subs(d, dv)
            if not (abs_diffable(q, lo=p) if side == 'R' else abs_diffable(q, hi=p)): continue
            eps = R(1, 10**6) * (1 if side == 'R' else -1)
            s = sp.sign(q.subs(x, p + eps))
            if s == 0: continue
            f = lead * x**3 + a * x**2 + b * x + c; g = m * x + n
            eqs = sp.Poly(sp.expand(f - g - q), x).all_coeffs()
            eqs += [(f + g - s * q).subs(x, p), sp.diff(f + g - s * q, x).subs(x, p)]
            for so in sp.solve(eqs, [a, b, c, m, n], dict=True):
                if so[m] == 0: continue                      # g는 일차함수
                out.append((sp.expand(f.subs(so)), sp.expand(g.subs(so)), sp.factor(q)))
    return out


def hval(f, g, p, side, t):
    poly = (t <= p) if side == 'R' else (t >= p)
    return (f + g).subs(x, t) if poly else abs((f - g).subs(x, t))


# --- 원문 D62: 최고차항 1, |f-g| (x<1), f+g (x≥1), h(0)=0, h(2)=5 → h(4)=39
# (원문은 f+g 쪽 값이 주어지므로 q=x^2(x-c), f=(x-1)^2(x-s), c=s+2, h(2)=2s+4=5로 따로 푼다)
s_ = sp.symbols('s_')
fo = (x - 1)**2 * (x - s_); qo = x**2 * (x - s_ - 2); go = sp.expand(fo - qo)
assert sp.degree(go, x) == 1
sv = sp.solve(sp.Eq((fo + go).subs(x, 2), 5), s_); assert sv == [R(1, 2)]
assert (fo + go).subs(x, 4).subs(s_, sv[0]) == 39 and F.I['D62'][2] == '39'
print('D62 원문 OK: s=1/2, h(4)=39')

# --- S2 본문 수치 확인
B = S2['body']
for w in (r"최고차항의 계수가 \(-1\)인 삼차함수", r"일차함수 \(g(x)\)", r"f(x)+g(x) & (x\le2)", r"|f(x)-g(x)| & (x&gt;2)",
          r"실수 전체의 집합에서 미분가능", r"\(h(5)=0\)", r"\(h(4)=3\)"): assert w in B, w
assert 'cond' not in S2

# --- 전수: 조건을 만족시키는 (f, g)는 하나뿐
sols = solve_all(-1, 2, 'R', 5, 4, 3)
assert len(sols) == 1, sols
f, g, q = sols[0]
assert sp.expand(f - (-(x - 2)**2 * (x - 7))) == 0 and g == 3 * x + 3 and sp.expand(q + (x - 5)**2 * (x - 1)) == 0
# 제곱 인수 가정 없이도: q는 최고차항 -1인 삼차, q(5)=0. x=5에서 |q| 미분가능 ⇔ q'(5)=0 (좌우 미분계수 ±q'(5))
# 후보 d: |4-d|=3 → 1, 7. d=7은 x=7(>2)에서 단순근, 삼중근 d=5는 h(4)=1≠3
assert sorted(sp.solve(sp.Eq(sp.Abs(4 - d), 3), d)) == [1, 7]
assert not abs_diffable(-(x - 5)**2 * (x - 7), lo=2) and abs((-(x - 5)**3).subs(x, 4)) == 1
assert sp.diff(-(x - 5)**2 * (x - 7), x).subs(x, 7) == -4
# 실제 h의 미분가능성 직접 확인 (x=2 좌우 값·미분계수, x>2에서 q≤0)
assert (f + g).subs(x, 2) == abs(q.subs(x, 2)) == 9
assert sp.diff(f + g, x).subs(x, 2) == sp.diff(-q, x).subs(x, 2) == 3
assert all(q.subs(x, 2 + R(k, 7)) <= 0 for k in range(1, 80)) and sp.diff(q, x).subs(x, 5) == 0
assert hval(f, g, 2, 'R', 5) == 0 and hval(f, g, 2, 'R', 4) == 3
A1, A2, A3 = hval(f, g, 2, 'R', 3), f.subs(x, 1), hval(f, g, 2, 'R', 0)
assert (A1, A2, A3) == (8, 6, 31)
assert S2['ans'] == [r'(1) \(8\)', r'(2) \(6\)', r'(3) \(31\)']
assert f.subs(x, 0) == 28 and g.subs(x, 0) == 3 and sp.expand((x - 2)**2 * (x - 7)) == x**3 - 11 * x**2 + 32 * x - 28 \
    and sp.expand((x - 5)**2 * (x - 1)) == x**3 - 11 * x**2 + 35 * x - 25
print('S2 OK: (f, g) 하나뿐 — f=-(x-2)^2(x-7), g=3x+3, f-g=-(x-5)^2(x-1) → (1) 8 (2) 6 (3) 31')

# --- 정답이 본문 수와 같지 않음
txt = S2['body'] + ''.join(s[0] for s in S2['subs'])
nums = set(re.findall(r'\d+', txt))
for v in ('8', '6', '31'): assert v not in nums, (v, nums)

# --- 오답 값
qw = -(x - 5)**2 * (x - 7)
assert abs(qw.subs(x, 3)) == 16 and (f + g).subs(x, 3) == 16                       # (1) d=7 / 왼쪽 식을 씀
assert ((x - 2)**2 * (x - 7)).subs(x, 1) == -6                                     # (2) 최고차항 1
assert (-(x - 2)**2 * (x - 3)).subs(x, 1) == 2 and (-(x - 2)**2 * (x + 5)).subs(x, 1) == -6   # (2) r=3 / r=-5
assert abs((f - g).subs(x, 0)) == 25 and f.subs(x, 0) == 28 and 28 + (28 + 25) == 81          # (3)
for w in (r'골라 \(16\)', r'f(3)+g(3)=16\)', r'\(-6\)', r'f(1)=2\)', r'f(1)=-6\)', r'|f(0)-g(0)|=25\)', r'f(0)=28\)', r'\(81\)'):
    assert w in S2['wrong'], w

# --- 배점·형식
assert len(S2['subs']) == 3 and len(S2['ans']) == 3 and len(S2['sol']) == 3
assert [s[1] for s in S2['subs']] == ['3점, 답만 적으시오.', '4점, 답만 적으시오.', '3점, 답만 적으시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', l)] for l in S2['rubric'][:3]]
assert pts == [[3], [4], [3]] and sum(map(sum, pts)) == 10
assert not re.findall(r'\[(\d)점\]', ''.join(S2['rubric'][3:])) and all('채점자 참고용' in l for l in S2['rubric'][:3])
assert S2['db_ref'] == 'D62 후보_순위 3' and S2['cand'] == 'S2' and set(S2['core']) == {'axis', 'setting', 'principle', 'new'} and S2['level'] == '중상'
assert '이러한' not in txt and '이와 같은' not in txt and txt.count('다음') == 0
allt = ' '.join([S2['body'], S2['fast'], S2['wrong'], S2['note'], S2['var']] + S2['rubric'] + S2['sol'] + [s[0] for s in S2['subs']] + list(S2['core'].values()))
assert not re.search(r'<(?!br>)', allt), '맨 < 있음'

# --- 인쇄 N제 D62(396–403, 분석집 변형 41·42)와 다름: 경계·영점·주는 값이 겹치지 않음
for fn in ('미적분1_기말_N제_04_도함수의활용(1).md', '미적분1_기말_N제_분석집변형.md'):
    nz = open('/home/user/Finale/output/N제/' + fn).read()
    i = nz.index('## D62'); sec = nz[i:nz.index('\n## ', i + 5)]
    for w in ('h(5)=0', 'h(4)=3', r'(x\le2)', '(x>2)', r'(x\gt 2)'): assert w not in sec, (fn, w)
# 거울·평행이동으로도 같지 않음: (영점-경계, 값을 준 점-경계, 값)이 N제 396(2, 1, 3)·분석집 42(1, 2, 4)와 다름
assert (5 - 2, 4 - 2, 3) not in {(2, 1, 3), (1, 2, 4)}
# N제 401(경계 1, h(2)=0, h(0)=5 → h(-2)=39)은 f+g 쪽 값을 주는 문항이라 주는 조건의 자리부터 다름

# --- 조건 빼 보기
def abl(cn, msg): print(f'ABLATION S2 {cn}: {msg}')
# 최고차항의 계수 -1: 1이면 조건을 만족시키는 함수가 없음
assert solve_all(1, 2, 'R', 5, 4, 3) == []
abl('최고차항의 계수 -1', '필요(1로 바꾸면 이음점 오른쪽에서 f-g>0이 되어 g가 일차함수일 수 없으므로 조건을 만족시키는 함수가 없음)')
# g는 일차함수: 이차 이하로 풀면 r이 정해지지 않음 ((1)은 그대로, (2)·(3)이 정해지지 않음)
fr = -(x - 2)**2 * (x - r); gr = sp.expand(fr - q)
assert sp.Poly(gr, x).coeff_monomial(x**2) == r - 7 and sp.simplify(fr.subs(x, 1) - (r - 1)) == 0
for rv in (0, 3, 9):   # g가 이차함수여도 h는 실수 전체에서 미분가능
    f2, g2 = fr.subs(r, rv), gr.subs(r, rv)
    assert (f2 + g2).subs(x, 2) == 9 and sp.diff(f2 + g2, x).subs(x, 2) == sp.diff(-q, x).subs(x, 2)
abl('g(x)는 일차함수', '필요(이차함수까지 허용하면 f=-(x-2)^2(x-r)의 r가 정해지지 않아 f(1)=r-1, (2)·(3)이 정해지지 않음; (1)에는 쓰이지 않음)')
# 경계 2: 1로 옮기면 값이 달라짐
s1 = solve_all(-1, 1, 'R', 5, 4, 3); assert len(s1) == 1 and s1[0][0].subs(x, 1) == 0 != 6
abl('조각의 경계 x=2', '필요(경계를 1로 옮기면 f(1)=0, h(0)도 달라짐)')
# 미분가능: 연속만이면 d=7도 가능 (g=m(x-2), f=q+g)
qc = -(x - 5)**2 * (x - 7)
assert qc.subs(x, 2) > 0 and abs(qc.subs(x, 4)) == 3 and abs(qc.subs(x, 3)) == 16 != 8
abl('실수 전체의 집합에서 미분가능', '필요(연속으로 바꾸면 f-g=-(x-5)^2(x-7), g=m(x-2)도 조건에 맞아 h(3)=16 등 값이 정해지지 않음)')
# h(5)=0: 없으면 다른 함수도 가능 — 예: f-g=-(x-1)((x-4)^2+1) (x>2에서 음수, h(4)=3)
q5 = -(x - 1) * ((x - 4)**2 + 1)
assert abs(q5.subs(x, 4)) == 3 and all(q5.subs(x, 2 + R(k, 7)) < 0 for k in range(0, 80))
r5 = sp.solve(sp.Poly(sp.expand(-(x - 2)**2 * (x - r) - q5), x).coeff_monomial(x**2), r)[0]
f5 = -(x - 2)**2 * (x - r5); g5 = sp.expand(f5 - q5)
assert sp.degree(g5, x) == 1 and (f5 + g5).subs(x, 2) == -q5.subs(x, 2) and sp.diff(f5 + g5 + q5, x).subs(x, 2) == 0
assert abs(q5.subs(x, 3)) == 4 != 8
abl('h(5)=0', '필요(없으면 f-g=-(x-1)((x-4)^2+1), f=-(x-2)^2(x-5)도 조건에 맞아 h(3)=4로 값이 정해지지 않음)')
# h(4)=3: 값을 바꾸면 d가 달라짐 / 없으면 d≤2가 모두 가능
s6 = solve_all(-1, 2, 'R', 5, 4, 4); assert len(s6) == 1 and hval(s6[0][0], s6[0][1], 2, 'R', 3) == 12 != 8
abl('h(4)=3', '필요(h(4)=4이면 d=0, h(3)=12로 바뀜; 없으면 2 이하의 모든 d가 가능)')
print('ALL OK')
