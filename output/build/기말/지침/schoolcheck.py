# -*- coding: utf-8 -*-
"""학교 선례 검사 (지침 front.md 0-8). 학교 실제 시험 3회 60문항(school_recipes.json)과 2학기 중간 실측에서 뽑은 기준.
  item  <parts.py>      문항별: 변형 기록(vtype·effect·bunseok·precedent), 회차 유형 규칙, 원문과의 거리, 선지 방식
  round <회차 폴더>     회차 전체 분포: 난도 효과, 함정·분석집 문항 수, 내림차순 선지 수, 그림 위치·수, 정답 분포
회차 유형은 <회차>/round.json {"type": "학교형"|"복습형"} (없으면 학교형).
2026-11-07부터 새 회차는 {"type": "학교형", "db": true}: 변형 DB 방식(front.md 0-8·2절·4-4). 문항에 db_ref·ops를 요구하고,
회차 분포는 기말 기준(예상밖 4–6, 그림 1–3, 내림차순 ≤4, 공차 1 8–12, 보기형 ≤1)으로 본다. db가 없는 옛 회차는 옛 기준 그대로."""
import sys, os, re, json, runpy, collections
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '부교재_기말'))
sys.path.insert(0, '/home/user/Finale/template/db/parts')
import dupcheck as DC

VTYPES = ['숫자 변경', '조건 변경', '함수 교체', '구하는 대상 변경', '형식 변경', '구조 변경', '함정 추가', '소재 결합', '그래프·그림 제시', '자체 출제']
EFFECTS = ['같음', '쉬워짐', '어려워짐']
# 2학기 중간 실측: 원문과의 골격 유사도(shingle Jaccard). 1–16 0.29–0.71(중앙 0.46), 17·18 0.06–0.15
DIST = {'front': (0.28, 0.72), 'top': (0.0, 0.25)}
# 2학기 중간 실측: 숫자 선지 17개 중 오름차순 15, 공차 1이 10개, 2가 3개, 그 밖 1/2·1/5·1/20·5
GOOD_D = {Fraction(x) for x in (1, 2, 3, 4, 5, 10)} | {Fraction(1, k) for k in (2, 3, 4, 5, 10, 20)}

def rtype(d):
    f = os.path.join(d, 'round.json')
    return json.load(open(f)).get('type', '학교형') if os.path.exists(f) else '학교형'

def isdb(d):
    f = os.path.join(d, 'round.json')
    return bool(json.load(open(f)).get('db')) if os.path.exists(f) else False

OPIDS = {f'OP{i:02d}' for i in range(1, 56)}
DBF = os.path.join(HERE, 'db', 'variation_db.json')
_DB = None
def dbref_ok(it):
    """db_ref = '<원문키> <칸> <n>' (후보_순위 n | 예상밖 n | v3_추가 n | 결합 n | 학교식_예상 n | 킬러 설계A/B) 또는 '자체'."""
    global _DB
    r = str(it.get('db_ref') or '')
    if not r: return 'db_ref 없음 (front.md 0-8: 예 \'J60 후보_순위 2\', \'M26 예상밖 1\', \'I66 킬러 설계A\')'
    if r.startswith('자체'): return None
    if _DB is None: _DB = json.load(open(DBF)) if os.path.exists(DBF) else {}
    m = re.match(r'(\w+)\s+(후보_순위|예상밖|v3_추가|결합|학교식_예상|킬러)\s*(\S*)', r)
    if not m: return f'db_ref 꼴이 다름({r})'
    k, kind, n = m.groups()
    if _DB and k not in _DB: return f'db_ref 원문 키 {k}가 DB에 없음'
    if it.get('key') and k != it.get('key') and kind != '결합': return f"db_ref 키 {k} ≠ 문항 key {it.get('key')}"
    e = _DB.get(k, {})
    fld = {'후보_순위': '후보_순위', '예상밖': '예상밖_포인트', 'v3_추가': 'v3_추가_예상', '결합': '결합_후보', '학교식_예상': '학교식_예상'}.get(kind)
    if fld and n.isdigit() and not (1 <= int(n) <= len(e.get(fld, []))): return f'db_ref {kind} {n}번이 DB에 없음(있는 수 {len(e.get(fld, []))})'
    if kind == '킬러' and '킬러' not in e: return f'{k}는 DB 킬러 원문이 아님'
    return None

def unexpected(it):
    return bool(re.search(r'예상밖|v3_추가|결합', str(it.get('db_ref') or '')))

def band(n):
    n = 19 if n == 'S1' else 20 if n == 'S2' else int(n)
    return '1–4' if n <= 4 else '5–8' if n <= 8 else '9–12' if n <= 12 else '13–16' if n <= 16 else '17–18' if n <= 18 else '서답'

def val(c):
    c = re.sub(r'\\\(|\\\)|\\displaystyle|\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', c)
    if m: return Fraction(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    try: return Fraction(c)
    except Exception: return None

def body(it):
    from items_common import COND
    return it['body'] + (COND(it['cond']) if it.get('cond') else '') + (it.get('after') or '')

def odist(it):
    try:
        import items_final as F
        o = F.I.get(it.get('key'))
    except Exception: o = None
    if not o: return None
    A = set(DC.shingles(DC.skel(DC.norm(re.split('①', body(it))[0])))); B = set(DC.shingles(DC.skel(DC.norm(re.split('①', o[0])[0]))))
    return len(A & B) / max(1, len(A | B))

def check_item(n, it, rt, db=False):
    msg, warn = [], []
    if db:
        e = dbref_ok(it)
        if e: msg.append(e)
        ops = it.get('ops') or []
        if not ops or any(o not in OPIDS for o in ops): msg.append(f'ops 없음/잘못({ops}) — school_ops_v3 OP01–OP55')
        if it.get('bunseok'): msg.append('분석집 중지(2026-11-07) — bunseok=False')
    vt = it.get('vtype'); ef = it.get('effect'); bs = it.get('bunseok'); pc = it.get('precedent')
    if not vt or any(v not in VTYPES for v in vt): msg.append(f'vtype 없음/잘못({vt}) — {"·".join(VTYPES)} 중에서')
    if ef not in EFFECTS: msg.append(f'effect 없음/잘못({ef}) — 같음·쉬워짐·어려워짐')
    if bs not in (True, False) and not db: msg.append('bunseok(분석집 방향·TIP 사용 여부) 없음')
    if not pc: msg.append("precedent(따른 학교 선례, 예: '2학기 중간 7번' 또는 라이브 문항 id) 없음")
    if rt == '복습형' and bs:   # 분석집 복습 4요소 (2회 지적)
        bm = it.get('bunseok_map') or {}
        miss = [k for k in ('tip', 'direction', 'traps', 'calc') if not bm.get(k)]
        if miss: warn.append(f"분석집 복습 4요소 빠짐: {'·'.join(miss)} (bunseok_map: tip·direction·traps·calc)")
    if rt == '학교형':
        if vt and '함정 추가' in vt: msg.append('학교형 회차에 함정 추가(학교 3회 60문항 중 0회)')
        if bs: msg.append('학교형 회차에 분석집 방향·TIP 저격')
    b = band(n)
    if b in ('1–4', '5–8', '9–12') and ef == '어려워짐': warn.append('1–12번 어려워짐(학교 36문항 중 4개, 회당 1개까지)')
    if vt and b in ('1–4', '5–8', '9–12') and len(vt) > 3: warn.append(f'변경 {len(vt)}가지(학교 1–12번 평균 2–3가지)')
    d = None if '자체' in str(it.get('src', '')) else odist(it)   # 자체 출제는 원문 거리 제외
    if d is not None:
        lo, hi = DIST['top'] if b == '17–18' else DIST['front'] if b != '서답' else (0, 1)
        if db and b != '17–18': hi = 1.0   # DB 회차: 학교식은 '발문 유지 + 숫자 교체'(2025 기말 연계 6·10·11·13·14·20이 발문 그대로) — 상한 없음
        if not (lo <= d <= hi): warn.append(f'원문 골격 유사도 {d:.2f} (학교 {b} 범위 {lo:.2f}–{hi:.2f})')
    try:
        import items_final as F
        o = F.I.get(it.get('key'))
    except Exception: o = None
    if o:   # 원문에 없던 줄 바꾼 식(조각함수 제외) — 억지 들여쓰기 (1회 지적)
        dv = [x for x in re.findall(r'\\\[(.*?)\\\]', body(it), re.S) if 'cases' not in x]
        do = [x for x in re.findall(r'\\\[(.*?)\\\]', o[0], re.S) if 'cases' not in x]
        import html as _h
        nz = lambda t: re.sub(r'\\[()]|\s|<[a-zA-Z/][^>]*>', '', _h.unescape(t.replace('&nbsp;', ' ')))
        DAN = r'\(단,([^()]*(?:\([^()]*\)[^()]*)*)\)'
        dan_o = {nz(x) for x in re.findall(DAN, o[0])}
        for x in re.findall(DAN, body(it)):
            if nz(x) not in dan_o and '단서' not in str(it.get('note', '')): warn.append(f'원문과 다른 단서 (단,{x.strip()[:40]}) — 원문 단서 그대로, 범위를 좁히거나 새로 붙이지 않음 (1회 16번)')
        if len(dv) > len(do): warn.append(f'줄 바꾼 식 {len(dv)}개 (원문 {len(do)}개) — 원문에 없던 짧은 식은 문장 안에')
    ch = it.get('choices') or []
    if ch:   # 그럴듯한 오답이 선지 안에 (1회 지적)
        ws = [str(w) for w in (it.get('wrongs') or [])]
        bad = [w for w in ws if w not in [str(c) for c in ch]]
        need = 2 if b in ('13–16', '17–18') else 1
        if bad: warn.append(f'wrongs {bad}가 선지에 없음')
        if len(ws) - len(bad) < need: warn.append(f'선지 안 그럴듯한 오답 {len(ws) - len(bad)}개 (기준 {need}개 이상, wrongs 필드)')
    if ch and not str(ch[0]).startswith('T:'):
        v = [val(c) for c in ch]
        if None not in v and len(v) == 5:
            dd = v[1] - v[0]
            if abs(dd) not in GOOD_D: warn.append(f'선지 공차 {dd} (학교는 1 위주, 2·5·1/2·1/5 등 — 오답 근거를 넣으려고 공차를 키우지 않음)')
    return msg, warn, d

def item(path):
    rd = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    rt = rtype(rd); db = isdb(rd)
    ns = runpy.run_path(path); bad = 0
    print(f"== 학교 선례 ({rt}{', DB' if db else ''})")
    for n, it in list(ns.get('ITEMS', {}).items()) + list(ns.get('SITEMS', {}).items()):
        msg, warn, d = check_item(n, it, rt, db)
        bad += bool(msg)
        if msg or warn: print(f'{n}: ' + ' | '.join(['✗ ' + m for m in msg] + ['△ ' + w for w in warn]))
    print('학교 선례 표시', bad, '개'); return bad

def round_(d):
    sys.path.insert(0, d); import content3 as C
    rt = rtype(d); db = isdb(d); its = dict(C.ITEMS); S = dict(C.SITEMS); out = []
    eff = collections.Counter((band(n), it.get('effect')) for n, it in its.items())
    trap = [n for n, it in its.items() if '함정 추가' in (it.get('vtype') or [])]
    bun = [n for n, it in its.items() if it.get('bunseok') and int(n) <= 16]
    desc = [n for n, it in its.items() if (lambda v: None not in v and v == sorted(v, reverse=True))([val(c) for c in it.get('choices') or []])]
    figs = [n for n, it in its.items() if 'class="fig"' in it['body'] + (it.get('after') or '')]
    ans = collections.Counter(it['ans'] for it in its.values())
    hard12 = sum(c for (b, e), c in eff.items() if b in ('1–4', '5–8', '9–12') and e == '어려워짐')
    hard16 = eff.get(('13–16', '어려워짐'), 0)
    out.append(('1–12 어려워짐 ≤1 (학교 회당 0–2)', hard12 <= 1, hard12))
    out.append(('13–16 어려워짐 1–2', 1 <= hard16 <= 2 or hard16 == 3, hard16))
    if rt == '학교형': out.append(('함정 추가 0 (학교형)', not trap, trap))
    else:
        out.append(('분석집 문항 = 1–16의 절반(8) (복습형)', len(bun) == 8, bun))
        out.append(('분석집 문항은 5–16번 (1–4번 없음, 2회 재측정)', not [n for n in bun if int(n) <= 4], [n for n in bun if int(n) <= 4]))
    if rt == '학교형': out.append(('분석집 저격 0 (학교형)', not bun, bun))
    if db:
        ux = [n for n, it in its.items() if unexpected(it) and int(n) <= 16]
        out.append(('예상밖 자리 4–6개, 5–16번 (front 4-4)', 4 <= len(ux) <= 6 and all(5 <= int(n) <= 16 for n in ux), ux))
        bogi = [n for n, it in its.items() if '보기' in it['body']]
        out.append(('보기형 ≤1 (2025 기말 1)', len(bogi) <= 1, bogi))
        k1718 = [str(its[n].get('db_ref', '')) for n in (17, 18) if n in its]
        out.append(('17·18 중 설계A ≥1 · 설계B ≤1', any('설계A' in r or r.startswith('자체') for r in k1718) and sum('설계B' in r for r in k1718) <= 1, k1718))
    out.append(('내림차순 선지 ≤4 (2025 기말 4)' if db else '내림차순 선지 ≤2 (학교 17개 중 2)', len(desc) <= (4 if db else 2), desc))
    num = [(lambda v: (v[1] - v[0]) if None not in v and len(v) == 5 else None)([val(c) for c in it.get('choices') or []]) for it in its.values()]
    d1 = sum(1 for x in num if x is not None and abs(x) == 1); nn = sum(1 for x in num if x is not None)
    lo1, hi1 = (8, 12) if db else (10, 13)
    out.append((f'공차 1 선지 {lo1}–{hi1}개 (숫자 선지 {nn}개)', lo1 <= d1 <= hi1, d1))
    tc = collections.Counter()
    try:
        sys.path.insert(0, HERE); import predict as _P
        for n, it in list(its.items()) + list(S.items()):
            if it.get('key') in _P.F.I: tc.update(_P.topics(it['key']))
        out.append(('소재 상한 (1회 지적: 수직선 운동 ≤2 등)', all(tc[t] <= _P.TOPIC_LIMIT[t] for t in tc), dict(tc)))
    except Exception as e: out.append(('소재 상한', False, f'검사 실패 {e}'))
    flo = 1 if db else 2
    out.append((f'그림 {flo}–3개, 모두 9번 이후', flo <= len(figs) <= 3 and all(int(n) >= 9 for n in figs), figs))
    out.append(('정답 ①–⑤ 각 3–4', all(3 <= ans.get(k, 0) <= 4 for k in range(1, 6)), dict(sorted(ans.items()))))
    print(f"== 회차 분포 ({rt}{', DB' if db else ''})")
    for name, ok, v in out: print(f"{'✓' if ok else '✗'} {name}: {v}")
    return sum(not ok for _, ok, _ in out)

if __name__ == '__main__':
    sys.exit(1 if (item(sys.argv[2]) if sys.argv[1] == 'item' else round_(os.path.abspath(sys.argv[2]))) else 0)
