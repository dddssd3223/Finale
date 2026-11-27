# -*- coding: utf-8 -*-
# 14회 p4 (Claude 13·14·15·16번) 정답 검증 + 유일성(전수) + 선지 등차 + 오답 실재 + 원문 풀이 + 조건 빼 보기(ABLATION)
import os, sys, re
import sympy as sp
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, 'p4.py'), encoding='utf-8').read(), ns)
IT = ns['ITEMS']
WANT = {13: 3, 14: 5, 15: 2, 16: 4}          # 분담표 13③·14⑤·15②·16④
DBREF = {13: 'D43 예상밖 1', 14: 'D25 결합 1', 15: 'J54 후보_순위 1', 16: 'I75 후보_순위 2 (다시)'}
COEF = {'OP11', 'OP12', 'OP28', 'OP38', 'OP51'}
NEED_COEF = {13: True, 14: True, 15: False, 16: True}   # 분담표 계수 13●·14●·15○·16●
BOX = {13: True, 14: True, 15: False, 16: True}           # 원문대로(D43·D25·I75 상자 있음, J54 상자 없음)
LEVEL = {13: '중상', 14: '중상', 15: '상', 16: '상'}
x, t, a, b, p = sp.symbols('x t a b p', real=True)
R = sp.Rational
ok = True


def check(no, cond, msg):
    global ok
    print(f'[{no}] {"OK  " if cond else "FAIL"} {msg}')
    ok &= bool(cond)


def choice_val(s):
    s = re.sub(r'\s', '', s)
    m = re.fullmatch(r'(-?)\\dfrac\{?(\d+?)\}?\{?(\d+)\}?', s)
    if m:
        return sp.Rational(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    return sp.Rational(s)


def ch(no):
    return [choice_val(z) for z in IT[no]['choices']]


def ans_ok(no, val):
    v = ch(no)
    d = {v[i + 1] - v[i] for i in range(4)}
    check(no, len(set(v)) == 5 and len(d) == 1, f'선지 {v} 서로 다르고 등차(공차 {d}, {"오름차순" if list(d)[0] > 0 else "내림차순"})')
    check(no, sp.Rational(val).q == 1, f'정답 {val} 정수(13번 이상 정수화)')
    check(no, IT[no]['ans'] == WANT[no], f'정답 번호 {IT[no]["ans"]} = 지정 {WANT[no]}')
    check(no, v[IT[no]['ans'] - 1] == val, f'계산값 {val} = 선지 {v[IT[no]["ans"] - 1]}')
    cf = sorted(COEF & set(IT[no].get('ops') or []))
    check(no, IT[no].get('db_ref') == DBREF[no] and IT[no].get('bunseok') is False and (cf or not NEED_COEF[no]),
          f'db_ref={IT[no].get("db_ref")!r} ops={IT[no].get("ops")} (계수·매개변수 조작 {cf}) bunseok=False')
    check(no, ('cond' in IT[no]) == BOX[no] and 'bogi' not in IT[no], f'조건 상자 {"있음" if "cond" in IT[no] else "없음"}(분담표 상자 칸대로), 보기형 아님')
    for f_ in ('vtype', 'effect', 'precedent', 'wrongs', 'level'):
        check(no, f_ in IT[no], f'필드 {f_} = {IT[no].get(f_)!r}')
    check(no, IT[no]['level'] == LEVEL[no], f'level {IT[no]["level"]} (목표 {LEVEL[no]})')
    body = IT[no]['body'] + ''.join(c for _, c in IT[no].get('cond', [])) + (IT[no].get('after') or '')
    check(no, '이러한' not in body and '이와 같은' not in body, "'이러한'·'이와 같은' 없음")
    nums = set(re.findall(r'(?<![\w.])\d+(?![\w.])', re.sub(r'<[^>]*>|style="[^"]*"|&[lg]t;', ' ', body)))
    check(no, str(abs(val)) not in nums, f'정답 {val}이 본문에 나온 수 {sorted(nums, key=int)}와 다름')


def wrong_in(no, vals, why):
    v = ch(no)
    w = [choice_val(z) for z in IT[no]['wrongs']]
    vals = [sp.nsimplify(z) for z in vals]
    check(no, all(z in v and z != v[IT[no]['ans'] - 1] for z in vals) and sorted(w) == sorted(set(vals)) and len(set(vals)) >= 2,
          f'오답 {vals} 선지에 있음, wrongs {IT[no]["wrongs"]}와 같음 ({why})')


def ablation(no, cname, vals, ans, why='', undef=None):
    global ok
    if undef is not None:
        msg = f'필요({undef})'
    elif not vals:
        msg = f'필요(남은 조건을 만족시키는 경우가 없음{"; " + why if why else ""})'
    else:
        sv = sorted(set(vals), key=lambda z: float(z))
        if sv == [ans]:
            msg = f'군더더기(답 그대로{"; " + why if why else ""})'
        elif len(sv) >= 2:
            msg = f'필요(정해지지 않음: 가능한 답 {", ".join(map(str, sv[:6]))}{" 등" if len(sv) > 6 else ""}{"; " + why if why else ""})'
        else:
            msg = f'필요(답 바뀜 {ans} → {sv[0]}{"; " + why if why else ""})'
    print(f'ABLATION {no} {cname}: {msg}')
    ok &= not msg.startswith('군더더기')


def orig_ans(key):
    o = F.I[key]
    if o[1] is None:
        return sp.Rational(o[2])
    c = o[1]['①②③④⑤'.index(o[2])]
    return c if c.startswith('T:') else sp.nsimplify(choice_val(c)) if re.fullmatch(r'-?\d+|-?\\dfrac.*', c) else c


def nroots(poly_expr, var):
