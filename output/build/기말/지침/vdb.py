# -*- coding: utf-8 -*-
"""원문별 변형 DB 보기 (front.md 2절). DB: db/variation_db.json(원문 280개), 학교 조작: db/school_ops_v3.json(OP01–OP55).
사용: python3 vdb.py show <키> [칸 쉼표목록]     # 원문 한 개의 칸들(기본: 핵심·후보_순위·학교식·예상밖·v3·오답·결합)
      python3 vdb.py killer <키>                 # 17·18 설계 A·B와 검산(수정_적용 포함)
      python3 vdb.py op <OP번호>                 # 학교 조작 설명·학교 사례
      python3 vdb.py used <회차 폴더>...         # 이미 쓴 DB 후보(문항 dict의 key·db_ref) 목록 — 같은 후보 두 번 쓰지 않기
칸 이름: 원문_핵심 원문_장치 변형_목록 숫자만_ids 숫자만_재판정 LIVE_요약 학교식_예상 예상밖_포인트 출제_우선 후보_순위
        v3_추가_예상 조작_보강 조작_점검 오답_설계 결합_후보 서답형_버전 그림_버전 기말_기출_연결 킬러 최종검토_정정 후보_순위_이전
정정 우선: 최종검토_정정 > 오답_설계[].검토_정정·전수검산 > 원래 값. 킬러는 검산.설계X.수정_적용 > 원래 설계."""
import sys, os, json, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
DB = json.load(open(os.path.join(HERE, 'db', 'variation_db.json')))
OPS = json.load(open(os.path.join(HERE, 'db', 'school_ops_v3.json')))
DEF = ['원문_핵심', '후보_순위', '학교식_예상', '예상밖_포인트', 'v3_추가_예상', '조작_보강', '오답_설계', '결합_후보', '기말_기출_연결', '최종검토_정정']
# 오답_설계 항목의 '검토_정정'(표본 최종 검토)·'전수검산'(판정 고침이면 그 값이 맞는 값)이 원래 값보다 우선한다.

def pr(name, v):
    print(f'── {name}')
    if isinstance(v, list):
        for i, x in enumerate(v, 1): print(f'  {i}. ' + (json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x))
    elif isinstance(v, dict): print('  ' + json.dumps(v, ensure_ascii=False, indent=1).replace('\n', '\n  '))
    else: print('  ' + str(v))

def show(k, fields=None):
    e = DB[k]
    for f in (fields or DEF):
        if f in e: pr(f, e[f])

def used(dirs):
    out = []
    for d in dirs:
        for f in sorted(os.listdir(os.path.join(d, 'parts'))):
            if not f.endswith('.py') or f.startswith('verify'): continue
            try: ns = runpy.run_path(os.path.join(d, 'parts', f))
            except Exception: continue
            for n, it in list(ns.get('ITEMS', {}).items()) + list(ns.get('SITEMS', {}).items()):
                out.append((os.path.basename(d.rstrip('/')), n, it.get('key'), it.get('db_ref', '-')))
    for r in out: print(*r)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'show': show(sys.argv[2], sys.argv[3].split(',') if len(sys.argv) > 3 else None)
    elif c == 'killer': pr('킬러', DB[sys.argv[2]].get('킬러', '없음(17·18 후보 아님)'))
    elif c == 'op':
        o = next(x for x in OPS['ops'] if x['id'] == sys.argv[2])
        for f in ('이름', '층위', '설명', '방법_전환', '재사용_조건', '기말_적용', '학교_사례'): pr(f, o.get(f))
    elif c == 'used': used(sys.argv[2:])
