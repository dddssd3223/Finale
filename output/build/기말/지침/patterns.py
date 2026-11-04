# -*- coding: utf-8 -*-
"""17·18·서답형2 흔한 패턴 점검 (지침 0-4 규칙 B)
익스텐션·라이브에서 반복되는 변형 패턴을 문항 본문에서 찾는다. 원문에 없던 패턴을 새로 넣었으면
'구조 변경으로 치지 않음'으로 표시한다. 원문이 이미 그 패턴이면(원리 유지형) 표시하지 않는다.
빈도는 analysis.json(익스텐션·라이브 변형 요소 867개, 문항 id 1,123개)과 부교재 원문 280개에서 센다.

사용
  python3 patterns.py freq                 # 패턴별 빈도표
  python3 patterns.py check <parts.py> ... # 17·18·S2 문항 점검 (checkpart가 부른다)"""
import sys, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '부교재_기말'))
sys.path.insert(0, '/home/user/Finale/template/db/parts')

# (이름, 본문 정규식, 분석 요소 정규식, 설명)
PATTERNS = [
    ('t-개수함수',
     r'실수\s*\\\(t\\\)에\s*대하여[^.?]{0,160}(개수|미분가능하지\s*않)[^.?]{0,40}\\\((g|h|N)\(t\)\\\)',
     r'개수[^.]{0,12}\b[ghN]\(t\)|[ghN]\(t\)[^.]{0,6}(불연속|극한)|미분불가능[^.]{0,8}개수',
     "원문의 고정 상수(높이·직선·점)를 실수 t로 바꿔 '…의 개수를 g(t)'로 만드는 것"),
    ('절댓값-수평선',
     r'\|f\(x\)\|[^.?]{0,60}직선\s*\\\(y=|\|f\(x\)\|\s*=\s*[a-z0-9]',
     r'\|f\(x\)\|\s*=|\|f\|\s*=|y=\|f\(x\)\|',
     "|f(x)|의 그래프와 수평선(또는 |f(x)|=k)의 교점 개수"),
    ('높이만-교체',
     r'직선\s*\\\(y=-?f\(\d\)\\\)',
     r'직선 y=-?f\(\d\)|y=f\(√?\d\)',
     "직선 y=f(1)을 y=f(2)·f(√3) 등 다른 점의 함숫값으로 바꾸는 것"),
]

def load_analysis():
    return json.load(open(os.path.join(HERE, 'analysis.json')))

def freq():
    A = load_analysis(); import items_final as F
    out = {}
    for name, rb, ra, desc in PATTERNS:
        keys, ids = set(), 0
        for k, a in A.items():
            for v in a.get('variant_elements') or []:
                if re.search(ra, v['element']): keys.add(k); ids += len(v.get('ids', []))
        orig = [k for k, v in F.I.items() if re.search(rb, v[0])]
        out[name] = dict(desc=desc, ext_live_ids=ids, ext_live_keys=sorted(keys), originals=orig)
    return out

def plain(it):
    from items_common import COND
    return it['body'] + (COND(it['cond']) if it.get('cond') else '') + (it.get('after') or '')

def check(paths):
    import items_final as F
    flags = 0
    for p in paths:
        ns = {}; exec(open(p).read(), ns)
        for n, it in list(ns.get('ITEMS', {}).items()) + list(ns.get('SITEMS', {}).items()):
            if str(n) not in ('17', '18', 'S2'): continue
            k = it.get('key'); ob = F.I[k][0] if k in F.I else ''
            b = plain(it)
            for name, rb, ra, desc in PATTERNS:
                if re.search(rb, b) and not re.search(rb, ob):
                    flags += 1
                    print(f'{n}: 흔한 패턴 [{name}] 새로 넣음 → 구조 변경으로 치지 않음 ({desc})')
                elif re.search(rb, b):
                    print(f'{n}: [{name}] 원문에도 있음(원리 유지형이면 허용)')
    print('흔한 패턴 표시', flags, '개')
    return flags

if __name__ == '__main__':
    if sys.argv[1] == 'freq':
        for name, d in freq().items():
            print(f"{name}: 익스텐션·라이브 {d['ext_live_ids']}문항({len(d['ext_live_keys'])}개 원문) · 부교재 원문 {len(d['originals'])}개 {d['originals']} — {d['desc']}")
    else:
        sys.exit(1 if check(sys.argv[2:]) else 0)
