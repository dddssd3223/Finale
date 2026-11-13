# -*- coding: utf-8 -*-
"""미적분Ⅰ 부교재 기말 범위(p.80–189) 문항 DB. I[key] = (본문, 보기 또는 None, 정답, 출처), D[key] = (난도, 구역, 풀이 메모)
키: 04 도함수의 활용(1) D9–D72 · 05 도함수의 활용(2) M1–M68 · 06 부정적분과 정적분 I1–I76 · 07 정적분의 활용 J1–J72"""
import os, importlib.util
_P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts')
I, D = {}, {}
for _k in range(1, 9):
    _s = importlib.util.spec_from_file_location(f'wbfinal_p{_k}', os.path.join(_P, f'items_p{_k}.py'))
    _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
    I.update(_m.I); D.update(_m.D)
def _fix(b):   # 수식 안의 &lt; &gt; → < >
    import re
    return re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), b)
I = {k: (_fix(v[0]), [_fix(c) for c in v[1]] if v[1] else v[1]) + tuple(v[2:]) for k, v in I.items()}
FIGDIR = _P
NOTES = {
    'D16': '빠른정답 ②(24)는 오류로 보임. 직접 풀이·정수 전수 검사 모두 ①(22). DB는 빠른정답 유지, 출제 시 22 기준.',
    'D51': '빠른정답표에 ⑤로 인쇄됐으나 단답형. 답 5로 저장.',
    'M65': '부교재 인쇄 오타 −f(x)+2f(x) → 원 평가원(2023 9월 22번) −f(x)+2f(t)로 수정해 저장. 답 58.',
    'J46': '선지 ③ 120/27은 20/27의 인쇄 오타로 보임(인쇄대로 저장). 정답 ⑤와 무관.',
    'J43': 'g가 감소함수여야 f, g가 x=6에서만 만남 — 문제에 암묵적인 조건.',
}
