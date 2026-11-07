# -*- coding: utf-8 -*-
"""N제 풀: schedule.json(모의고사 회차표)에 들어가지 않은 DB 변형 목록 → nje_pool.json (front.md 4-0)
사용: python3 nje.py   (predict.py schedule 다음에 돌린다)"""
import json, os, collections
import predict as P
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'schedule.json')))
used = set()
for r in S.values():
    for v in r.values():
        ref = v['db_ref'].replace(' (다시)', ''); used |= {ref, P.canon(ref)}
pool = {}
for k, e in P.DB.items():
    L = [f'{k} {lab} {i + 1}' for f, lab in (('학교식_예상', '학교식_예상'), ('예상밖_포인트', '예상밖'), ('v3_추가_예상', 'v3_추가'), ('결합_후보', '결합')) for i in range(len(e.get(f, [])))]
    if e.get('킬러'): L += [f'{k} 킬러 설계{t}' for t in 'AB']
    L = [x for x in L if x not in used]
    if L: pool[k] = L
json.dump(pool, open(os.path.join(HERE, 'nje_pool.json'), 'w'), ensure_ascii=False, indent=0)
print('N제 변형', sum(map(len, pool.values())), dict(collections.Counter(x.split()[1] for v in pool.values() for x in v)))
