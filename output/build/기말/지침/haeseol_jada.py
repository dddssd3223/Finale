# -*- coding: utf-8 -*-
"""해설 원고의 '~하자.' 끝맺음을 '~한다.'로 바꾼다(사용자 2026-11-23: 모든 문장은 '-다.'). 사용: python3 haeseol_jada.py <items json>…"""
import re, sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__)); import haeseol2 as H
def conj(stem):
    """동사 어간(마지막 글자) → 현재형 '-ㄴ다/-는다'"""
    last = stem[-1]; code = ord(last) - 0xAC00
    if not 0 <= code < 11172: return stem + '다'
    jong = code % 28
    if jong == 0: return stem[:-1] + chr(ord(last) + 4) + '다'          # 받침 없음 → ㄴ다
    if jong == 8: return stem[:-1] + chr(ord(last) - 8 + 4) + '다'      # ㄹ 받침 → ㄹ 떨어지고 ㄴ다
    return stem + '는다'
def fix(t):
    return re.sub(r'([가-힣]+)자(?=\.)', lambda m: conj(m.group(1)), t)
def walk(d):
    for k in ('body', 'think', 'justify'):
        if d.get(k): d[k] = H.outside(d[k], fix)
    for st in d.get('flow') or []: st['points'] = [H.outside(p, fix) for p in st.get('points') or []]
    for cb in d.get('concepts') or []: cb['body'] = H.outside(cb.get('body'), fix)
    v = d.get('variation') or {}
    for k in ('origin', 'point'):
        if v.get(k): v[k] = H.outside(v[k], fix)
    if v.get('changes'): v['changes'] = [H.outside(x, fix) for x in v['changes']]
    return d
if __name__ == '__main__':
    for f in sys.argv[1:]:
        D = [walk(d) for d in json.load(open(f))]
        json.dump(D, open(f, 'w'), ensure_ascii=False, indent=1)
    print(fix('구하자. 빼자. 찾자. 세우자. 대입하자. 두자. 풀자. 살펴보자. 넣자. 쓰자. 나누자.'))
