# -*- coding: utf-8 -*-
"""부교재 분석집(143원문·변형 290)의 변형 문제를 변형 DB에 넣는다 (2026-11-11 사용자: "분석집의 문제만 다 db에 넣어").
- 저장소(공개)의 variation_db.json에는 번호·정답만: 원문키 → '분석집_변형' = [{"id": "STUDY-J33-변형①", "정답": "③"}].
- 문제 전문·풀이는 저장소 밖: db/study_local.json (.gitignore). vdb.py show가 있으면 합쳐 보여 준다.
사용: python3 db/study_import.py <study.json>   (study.json = 분석집 md에서 뽑은 것, 스크래치패드 study/an/study.json)"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(sys.argv[1]))
dbp = os.path.join(HERE, 'variation_db.json'); DB = json.load(open(dbp))
local, n = {}, 0
for s in src:
    k = s['key']
    if k not in DB: print('DB에 없는 원문', k); continue
    ids = []
    for v in s['variants']:
        vid = f"STUDY-{k}-변형{v['no']}"
        m = re.match(r'\s*([①②③④⑤]|[-\d./]+)', v['answer']); ans = m.group(1) if m else ''
        ids.append({'id': vid, '정답': ans})
        local[vid] = {'원문': k, 'no': v['no'], 'problem': v['problem'], 'answer': v['answer']}
        n += 1
    DB[k]['분석집_변형'] = ids
    local[f'STUDY-{k}-변형포인트'] = s.get('var_summary', [])
json.dump(DB, open(dbp, 'w'), ensure_ascii=False, indent=0)
json.dump(local, open(os.path.join(HERE, 'study_local.json'), 'w'), ensure_ascii=False, indent=1)
print(f'원문 {len(src)}개, 변형 {n}개 → variation_db.json(번호·정답), study_local.json(전문, 저장소 밖)')
