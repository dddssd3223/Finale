# -*- coding: utf-8 -*-
# 10.5회 서답형 S1 (10회 서답형2 숫자만 바꿈) 검증 · author='claude'
import sympy as sp, os, re
x, t, c = sp.symbols('x t c', real=True)
R = sp.Rational
ns = {}; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hS.py')).read(), ns)
S = ns['SITEMS']['S1']
assert list(ns['SITEMS']) == ['S1']


def absint_num(fc, lo, hi):
    rts = sorted(r for r in set(sp.Poly(fc, x).real_roots()) if lo < r < hi)
    cuts = [lo] + rts + [hi]
    return sum(abs(sp.integrate(fc, (x, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))

def gval(cv, tv):
    fc = sp.expand(x * (x - 2) * (x - cv))
    return sp.integrate(fc, (x, tv, tv + 2)) - absint_num(fc, 0, 2)

# 본문(원문 10회 서답형2와 동일)
assert r"f(0)=f(2)=0" in S['body'] and r"\int_t^{t+2}f(x)\,dx-\int_0^2|f(x)|\,dx" in S['body'] and 'cond' not in S
f = x * (x - 2) * (x - c)
G = sp.integrate(f, (x, t, t + 2)); I = sp.integrate(f, (x, 0, 2))
g = {'lo': sp.factor(G + I), 'hi': sp.factor(G - I),
     'mid': sp.factor(G - (sp.integrate(f, (x, 0, c)) - sp.integrate(f, (x, c, 2))))}
assert sp.factor(g['lo'].subs(t, -2)) == sp.factor(-16 * (c + 2) / 3)
assert sp.factor(g['lo'].subs(t, -1)) == sp.factor(2 * (c - 4) / 3)
assert sp.factor(g['hi'].subs(t, -1)) == -2 * c
for cv in (R(-11), R(-8), R(-2), R(-1, 3), R(0), R(1, 2), R(1), R(3, 2), R(2), R(5), R(7)):
    key = 'lo' if cv <= 0 else ('hi' if cv >= 2 else 'mid')
    for tv in (-2, -1, 0, 1):
        assert sp.simplify(g[key].subs({c: cv, t: tv}) - gval(cv, tv)) == 0
CG = [R(i, 8) for i in range(-160, 81)]   # c 격자 [-20, 10]

# (1) g(0)=0 ⇔ c≥2, f(-2) 최댓값
z = [cv for cv in CG if gval(cv, 0) == 0]; assert z == [cv for cv in CG if cv >= 2]
assert sp.expand(f.subs(x, -2) + 8 * (c + 2)) == 0
A1 = max(f.subs({c: cv, x: -2}) for cv in z); assert A1 == f.subs({c: 2, x: -2}) == -32
# (2) f(1)=-9 ⇒ c=-8 유일
c2 = sp.solve(sp.Eq(f.subs(x, 1), -9), c); assert c2 == [-8]
A2 = gval(-8, 0); assert A2 == -24
# (3) 세 구간 식 전수
cands = []
for key, cond in (('lo', lambda v: v <= 0), ('hi', lambda v: v >= 2), ('mid', lambda v: 0 < v < 2)):
    for s in sp.solve(sp.Eq(g[key].subs(t, -1), -10), c):
        if s.is_real and cond(s): cands.append(s)
assert sorted(cands) == [-11, 5], cands           # 함정 후보 c=5(절댓값 무시 식 -2c) 살아 있음
mid_eq = sp.Poly(sp.expand(6 * (g['mid'].subs(t, -1) + 10)), c)
assert not [r for r in mid_eq.real_roots() if 0 < r < 2]
assert [cv for cv in CG if gval(cv, -1) == -10] == [-11, 5]
assert gval(-11, -2) > 0 and gval(5, -2) < 0
sel = [cv for cv in cands if gval(cv, -2) > 0]; assert sel == [-11]
assert [cv for cv in CG if gval(cv, -2) > 0] == [cv for cv in CG if cv < -2]
A3 = f.subs({c: -11, x: 4}); assert A3 == 120
assert S['ans'] == [rf'(1) \({A1}\)', rf'(2) \({A2}\)', rf'(3) \({A3}\)']
print('S1 정답 확인 OK (c 세 구간 식 전수 + 격자 1/8 간격)')

# 원래 10회 답·본문 수와 다름
assert (A1, A2, A3) != (-9, -8, 72) and A1 != -9 and A2 != -8 and A3 != 72
txt = S['body'] + ''.join(q[0] for q in S['subs'])
nums = set(re.findall(r'-?\d+', txt))
for v in (A1, A2, A3): assert str(v) not in nums, v
# 학생 오답 (2) -16, (3) 8 과 새 정답이 같지 않음
assert A2 != -16 and A3 != 8

# 함정(오답 경로) 값 재현
assert 8 * (2 + 2) == 32                                                    # (1) 부호 실수
assert sp.integrate(f.subs(c, -8), (x, 0, 2)) == -12                        # (2) ∫f만
assert gval(-8, 0) != 0 and (sp.integrate(f.subs(c, -8), (x, 0, 2)) - sp.integrate(f.subs(c, -8), (x, 0, 2))) == 0  # (2) 절댓값 무시 0
termabs = sum(abs(sp.integrate(m, (x, 0, 2))) for m in sp.Add.make_args(sp.expand(f.subs(c, -8))))
assert termabs == 52 and -12 - termabs == -64                              # (2) 항별 절댓값 (10회 -16 경로)
fo = x * (x - 2) * (x + 2); to = sum(abs(sp.integrate(m, (x, 0, 2))) for m in sp.Add.make_args(sp.expand(fo)))
assert sp.integrate(fo, (x, 0, 2)) - to == -16                             # 10회 학생 오답 -16 재현
assert sp.solve(-2 * c + 10, c) == [5] and f.subs({c: 5, x: 4}) == -8      # (3) 절댓값 무시
assert sp.solve(-2 * c + 6, c) == [3] and f.subs({c: 3, x: 4}) == 8        # 10회 학생 오답 8 재현
assert f.subs({c: 11, x: 4}) == -56                                         # (3) 부호 실수
for w in (r'\(32\)', r'\(g(0)=0\)', r'\(g(0)=-64\)', r'=-12\)만', r'\(f(4)=-8\)', r'\(f(4)=-56\)'): assert w in S['wrong'], w
print('함정 OK: (2) 항별 절댓값·절댓값 무시, (3) c≥2 쪽 후보(절댓값 무시 식) 살아 있음')

# 형식
assert len(S['subs']) == 3 and len(S['ans']) == 3 and len(S['sol']) == 3
assert [q[1] for q in S['subs']] == ['2점, 답만 적으시오.', '3점, 답만 적으시오.', '5점, 답만 적으시오.']
pts = [[int(v) for v in re.findall(r'\[(\d)점\]', line_)] for line_ in S['rubric'][:3]]
assert pts == [[2], [3], [5]], pts
assert not re.findall(r'\[(\d)점\]', ''.join(S['rubric'][3:]))
for k in ('body', 'subs', 'ans', 'rubric', 'sol', 'fast', 'wrong', 'level', 'key', 'src', 'note'): assert k in S, k
alltxt = S['body'] + ''.join(q[0] for q in S['subs']) + ''.join(S['sol']) + S['fast'] + S['wrong'] + S['note'] + ''.join(S['rubric'])
assert '이러한' not in alltxt
assert not [m for m in re.findall(r'\\\(.*?\\\)', alltxt) if '<' in m or '>' in m]
print('형식 OK')

def abl(cn, m): print(f'ABLATION {cn}: {m}')
abl('(3)의 g(-2)>0', f'필요(없으면 c=-11, 5 두 후보, f(4)={A3}, {f.subs({c: 5, x: 4})})')
abl('(3)의 g(-1)=-10', '필요(없으면 c<-2인 모든 c)')
assert f.subs({c: -100, x: -2}) > 0
abl('(1)의 g(0)=0', '필요(없으면 f(-2)=-8(c+2)가 위로 유계 아님)')
assert gval(-1, 0) != gval(-8, 0)
abl('(2)의 f(1)=-9', '필요(없으면 g(0)이 c에 따라 달라짐)')
p_ = sp.symbols('p', positive=True)
sp_ = sp.solve(sp.Eq(p_ * g['lo'].subs(t, -1), -10), c)
assert sp.simplify(sp_[0].subs(p_, 2)) != -11
abl('최고차항의 계수 1', '필요(계수 p이면 (3)의 c가 p마다 달라짐)')
print('ALL OK')
