# -*- coding: utf-8 -*-
"""D40 변형: 사차식 세 실근의 차수 배분 세 경우를 전수 조사한다."""
from pathlib import Path
import html
import re
import runpy
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '부교재_기말'))
import items_final as original
it = runpy.run_path(str(HERE / 'c18.py'))['ITEMS'][18]
x,r = s.symbols('x r', real=True)
R = s.Rational
line = -4*x+4
# 사차식의 서로 다른 실근이 세 개이면 실근 차수 배분은 2+1+1뿐이다.
patterns = [x**2*(x-2)*(x-r), x*(x-2)**2*(x-r), x*(x-2)*(x-r)**2]
assert {tuple(sorted(v)) for v in [(2,1,1),(1,2,1),(1,1,2)]} == {(1,1,2)}
candidates = []
for H in patterns:
    values = s.solve(s.diff(H,x).subs(x,1)-4, r)
    assert len(values) == 1
    for value in values:
        f = s.expand(H.subs(r,value)+line)
        roots = s.roots(f-line,x)
        assert value not in [0,2]
        assert len(roots) == 3 and sorted(roots.values()) == [1,1,2]
        assert sum(roots.values()) == 4  # 비실근이 남지 않음
        assert f.subs(x,0)==4 and f.subs(x,2)==-4
        assert s.diff(f,x).subs(x,1)==0
        second = s.diff(f,x,2).subs(x,1)
        assert second != 0
        candidates.append((f,second))
        print(f'FAMILY H={s.factor(f-line)}: f″(1)={second}, f(1)={f.subs(x,1)}')
good = [f for f,second in candidates if second<0]
assert len(good)==1
fstar=good[0]
assert s.expand(fstar - (x*x*(x-2)*(x-6)-4*x+4)) == 0
assert fstar.subs(x,1)==5
assert s.expand(s.diff(fstar,x)-4*(x-1)*(x*x-5*x+1)) == 0
# 1의 좌우에서 f′는 양에서 음으로 바뀐다. 이계도함수의 부호와도 일치한다.
assert s.diff(fstar,x).subs(x,R(9,10))>0>s.diff(fstar,x).subs(x,R(11,10))

choices=list(map(s.sympify,it['choices']))
assert len(choices)==len(set(choices))==5
assert len(set(choices[i+1]-choices[i] for i in range(4)))==1
assert it['ans']==3 and choices[2]==5
Hstar=fstar-line
wrong={
    13: (Hstar+4*x+4).subs(x,1),
    9: (Hstar+4).subs(x,1),
    1: (Hstar-4*x).subs(x,1),
    -3: candidates[1][0].subs(x,1),
}
assert all(k==v and k in choices and k!=5 for k,v in wrong.items())
assert set(wrong)==set(choices)-{5}
print('CHOICES 정답 ③ 5, 공차 -4, 오답 4개 계산 OK')

# 조건을 뺄 때에도 남은 조건을 모두 만족하는 반례를 기호식으로 확인한다.
def check(p):
    return {
        '사차함수': s.degree(p,x)==4,
        '최고차항': s.LC(s.Poly(p,x))==1,
        '(가)': len(set(s.real_roots(p-line,x)))==3,
        '점(0,4)': p.subs(x,0)==4,
        '점(2,-4)': p.subs(x,2)==-4,
        '(다)': s.diff(p,x).subs(x,1)==0 and s.diff(p,x,2).subs(x,1)<0,
    }
def ablation(label,p,omitted):
    checks=check(p)
    assert all(v for k,v in checks.items() if k!=omitted),(label,checks)
    assert not checks[omitted] and p.subs(x,1)!=5
    print(f'ABLATION 18 {label}: 필요(f={s.factor(p)}, f(1)={p.subs(x,1)})')

ablation('(가) 세 교점',x*(x-2)*(x*x-6*x+1)+line,'(가)')
ablation('(나)의 점(0,4)',(x-R(1,2))**2*(x-2)*(x-R(20,3))+line,'점(0,4)')
ablation('(나)의 점(2,-4)',x*(x+1)*(x-3)**2+line,'점(2,-4)')
ablation('(다) 극대',candidates[1][0],'(다)')
# 위치 x=1도 필요: 접점이 0이고 제3의 근이 5인 예는 극대 위치가 달라진다.
p=x*x*(x-2)*(x-5)+line
assert s.diff(p,x).subs(x,1)!=0
ablation('(다)의 극대 위치',p,'(다)')
ablation('최고차항 계수 1',2*x*x*(x-2)*(x-4)+line,'최고차항')
Q=(x-1)**2-R(4,5)*(x-1)+2
assert s.discriminant(Q,x)<0
ablation('사차함수',Hstar*Q+line,'사차함수')

# 원문도 같은 원리로 두 경우를 모두 풀고 극대인 경우만 남긴다.
original_candidates=[]
for H in [x*(x-r)**2,x*x*(x-r)]:
    for rv in s.solve(s.diff(H+9*x,x).subs(x,3),r):
        f=s.expand(H.subs(r,rv)+9*x)
        if len(set(s.real_roots(f-9*x,x)))!=2:
            continue
        if s.diff(f,x,2).subs(x,3)<0:
            original_candidates.append(f)
assert len(original_candidates)==1
fo=original_candidates[0]
assert fo==x**3-12*x*x+45*x
cp=s.solve(s.diff(fo,x),x)
mins=[v for v in cp if s.diff(fo,x,2).subs(x,v)>0]
assert mins==[5] and fo.subs(x,5)==50
assert original.I['D40'][2]=='50'
print('ORIGINAL D40 정답 50 OK')

def length(t):
    t=html.unescape(re.sub(r'<[^>]*>','',t))
    t=re.sub(r'\\[()\[\]]','',t)
    return len(re.sub(r'\s+',' ',t).strip())
text=it['body']+''.join('('+k+')'+v for k,v in it['cond'])
old_len,new_len=length(original.I['D40'][0]),length(text)
assert new_len>=old_len and new_len>=142
assert it['author']=='codex' and it['cand']=='codex18' and it['core']['axis']=='②'
print(f'LENGTH 동일 기준 원문 {old_len}자 → 변형 {new_len}자; 지시서 142자 이상 OK')
print('ALL OK')
