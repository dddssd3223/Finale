# -*- coding: utf-8 -*-
"""학교 출제 예측 순위 + 회차 분담 초안 (front.md 0-8, 1절 출처 배치)
점수 = 라이브 빈도(전국 학교 기출 횟수) + 최근(2024–25) 가중 + 번호 자리 적합(라이브 출제 번호 중앙값과의 거리)
       + 작년 2025 기말 연계 원문 가산(원문 재사용 습관, 다른 축으로) — 분석집 가산은 2026-11-07부터 끔(분석집 중지)
사용: python3 predict.py rank                              # 원문 예측 점수표
      python3 predict.py plan <회차번호> [사용한 키 쉼표목록]  # 분담 초안(JSON): 자리·원문·예비 원문·학교식/예상밖 배정·DB 추천
      (옛 형식 plan <회차번호> <학교형|복습형> [키]도 받는다. 유형은 무시 — 2026-11-07부터 회차 유형 없음, front.md 4절)
제약 (기말 자리 규칙, front.md 1절): 평가원 5 · EBS 8 · Level Up 5 · 자체 2(4번 기본형·서답형1), 단원 D5 M5 I5 J5 ↔ D4 M5 I6 J5 회차마다 번갈아,
      1–4번 J 허용(2026-11-07 사용자 확정, 같은 단원 2개까지), 원본 난도 자리별 범위(16번 6–8), 그림 원문은 9번 이후 1–3개(1–8번 제외).
      예상밖 자리: 5–16번 중 4–6개(시험 직전 12회부터 4개), 나머지는 학교식(DB 후보_순위 1–2)."""
import sys, os, json, math, collections, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '부교재_기말')); import items_final as F
L = json.load(open(os.path.join(HERE, 'livestats.json')))
STUDY = set(json.load(open(os.path.join(HERE, 'study_keys.json'))))
# 자리: (번호, 출처, 원본 난도 범위) — 2학기 중간 출처 배치(확정·유력·유동) 그대로
# 기말 자리 (2026-11-07): 2025 기말(작년 2학기 기말) 연계 자리 + 2026 2학기 중간을 겹침. 9·16 평가원, 11·13 Level Up, 서답1 자체, 서답2 연계 단계화는
# 세 시험 공통으로 고정. 6·10·14·15는 2025 기말에서 EBS(10 J20, 14 J23, 15 D16) → 10·14는 EBS, 15는 평가원 유지(중간 대표기출). 4번은 기본형 자체.
SLOTS = [(1, 'E|평', (1, 3)), (2, 'E|평', (1, 3)), (3, 'E|평', (2, 3)), (4, '자체', (1, 3)), (5, 'E', (3, 5)), (6, 'E', (3, 5)), (7, 'LU', (4, 5)), (8, 'E', (4, 5)),
         (9, '평', (4, 6)), (10, 'E', (4, 5)), (11, 'LU', (4, 6)), (12, '평', (4, 6)), (13, 'LU', (5, 6)), (14, 'E', (4, 6)), (15, '평', (5, 6)),
         (16, '평', (6, 8)), (17, 'LU', (5, 7)), (18, 'LU', (5, 9)), ('S1', '자체', (1, 4)), ('S2', '평', (5, 7))]
QUOTA = dict(D=5, M=5, I=5, J=5)       # 부교재 비율 D64 M68 I76 J72에 맞춤(J4면 J 원문 14개가 14회까지 남음, 2026-11-07 점검)
QUOTA_ALT = dict(D=4, M=5, I=6, J=5)   # 2025 기말 단원(D4 M5 I6 J5) — 짝수 회차에 씀
Y25 = {'M23', 'J60', 'J20', 'M26', 'I31', 'D40', 'J23', 'D16', 'I66', 'M32'}   # 작년 2025 기말 연계 원문(원문 재사용: 근거 중간)
DBP = os.path.join(HERE, 'db', 'variation_db.json')
DB = json.load(open(DBP)) if os.path.exists(DBP) else {}
def band(no):
    if not isinstance(no, int): return '서답형'
    return '1–4' if no <= 4 else '5–8' if no <= 8 else '9–12' if no <= 12 else '13–16' if no <= 16 else '17–18'
def unexpected_slots(rno):
    """예상밖 자리: 5–16번 중 5개(12회부터 4개). 회차 번호로 돌려 자리마다 고르게. 9–16번에 더 많이(2025 기말은 9–16이 가장 짙었다)."""
    import random
    pool = [6, 7, 9, 10, 11, 12, 13, 14, 15, 16]
    n = 4 if rno >= 12 else 5
    r = random.Random(rno); out = set(r.sample([x for x in pool if x >= 9], n - 1)) | {r.choice([6, 7])}
    return sorted(out)
def db_hint(k, no, mode):
    e = DB.get(k)
    if not e: return {}
    b = band(no)
    if mode == '학교식':
        top = [c for c in e.get('후보_순위', []) if b in str(c.get('번호대', '')) or b == '서답형'][:2] or e.get('후보_순위', [])[:2]
        fx = [x for x in e.get('최종검토_정정', []) if str(x.get('칸', '')).startswith('후보_순위') and not isinstance(x.get('고친_값'), list)]
        return {'추천': [f"{c.get('순위')}. {c.get('출처')}" for c in top], **({'순위_정정': [str(x['고친_값'])[:160] for x in fx]} if fx else {})}
    pts = [f"예상밖 {i+1}" for i, x in enumerate(e.get('예상밖_포인트', []))] + [f"v3_추가 {i+1}" for i, x in enumerate(e.get('v3_추가_예상', []))] + [f"결합 {i+1}" for i, x in enumerate(e.get('결합_후보', []))]
    return {'추천': pts[:4]}
HARD = (15, 16, 17, 18, 'S2')   # 고난도 자리: 분담표에 예비 원문 2개를 같이 적는다(독립 검토 2번 탈락 → 교체)

def src(k):
    t = F.D[k][1]
    return 'LU' if t == 'Level Up' else '평' if t == '평가원 기출' else 'E'

def has_fig(k): return 'fig' in F.I[k][0]

# 소재 (1회 지적: 수직선 운동 4문항 겹침). 원문 본문 키워드로 분류, 한 회 상한
import re as _re
TOPIC_LIMIT = {'수직선 운동': 2, '넓이': 3, '적분함수': 3, '평행이동·주기': 2, '접선': 2, '실근·교점 개수': 3}
def topics(k):
    t = F.I[k][0]; out = set()
    if '수직선 위를 움직이는' in t or '속도' in t: out.add('수직선 운동')
    if '넓이' in t: out.add('넓이')
    if _re.search(r'\\int_\{?[^}]{0,6}\}?\^\{?x|\\int_x', t): out.add('적분함수')
    if _re.search(r'[fg]\(x[+-]\d\)', t): out.add('평행이동·주기')
    if '접선' in t: out.add('접선')
    if '실근' in t or '만나는 점의 개수' in t or '교점' in t: out.add('실근·교점 개수')
    return out

def score(k, slot=None):
    l = L.get(k, {}); n = l.get('n', 0); yr = l.get('years', {})
    s = math.log1p(n) + 0.4 * math.log1p(yr.get('2024', 0) + yr.get('2025', 0)) + (0.5 if k in Y25 else 0)
    if slot is not None and isinstance(slot, int) and n:
        s -= abs(l.get('median', slot) - slot) / 8
    return s

def rank():
    rows = sorted(F.I, key=lambda k: -score(k))
    for k in rows[:60]:
        l = L.get(k, {})
        print(f"{k:4} 점수 {score(k):.2f} 라이브 {l.get('n', 0):2} (최근 {l.get('years', {}).get('2024', 0) + l.get('years', {}).get('2025', 0)}) 자리중앙 {l.get('median', '-')} 서술 {l.get('seo', 0)} {src(k)} 난도 {F.D[k][0]} {'그림' if has_fig(k) else ''} {'작년기말' if k in Y25 else ''}")

def cap(rno):
    """원문 한 개를 몇 번까지 쓸 수 있나(3–40회 회차표, 2026-11-07): 1–14회 1번, 15–27회 2번, 28–40회 3번."""
    return 1 + (rno > 14) + (rno > 27)

def plan(rno, used=(), recent=()):
    UC = collections.Counter(used); recent = set(recent)
    used = {k for k, c in UC.items() if c >= cap(rno)} | recent; quota = dict(QUOTA_ALT if rno % 2 == 0 else QUOTA); pick = {}; reuse = set()
    def topic_ok(k):
        cnt = collections.Counter(tp for v in pick.values() for tp in topics(v))
        return all(cnt[tp] + 1 <= TOPIC_LIMIT[tp] for tp in topics(k))
    order = [s for s in SLOTS if s[0] in (17, 18, 'S2', 15, 16)] + [s for s in SLOTS if s[0] not in (17, 18, 'S2', 15, 16)]
    def cands(no, sv, rng, need_fig=None, loose=False):
        out = []
        for k in F.I:
            if k in used or k in pick.values(): continue
            u = k[0]
            if quota[u] <= 0: continue
            if isinstance(no, int) and no <= 4 and sum(1 for n2, v in pick.items() if isinstance(n2, int) and n2 <= 4 and v[0] == u) >= 2: continue   # 1–4번 같은 단원 2개까지
            if sv == '자체':
                if src(k) not in ('E', '평'): continue          # 자체 기본형: 가장 가까운 EBS·평가원 기본 원문 표시
            elif src(k) not in sv.split('|'): continue         # 1–3번은 EBS·평가원 기본 계산(LIVE 1–5번 단골 I49–I56 등)
            if not (rng[0] <= F.D[k][0] <= rng[1]): continue
            if isinstance(no, int) and no <= 8 and has_fig(k): continue          # 1–8번 그림 없음
            if need_fig is not None and has_fig(k) != need_fig: continue
            if not loose and not topic_ok(k): continue                              # 소재 겹침 상한(마지막 대체에서만 풂)
            sc = score(k, no if isinstance(no, int) else 20) - 1.5 * UC.get(k, 0) + (3 if rno > 8 and not UC.get(k) else 0)   # 덜 쓴 원문 먼저, 9회부터 미노출 원문 크게 우대
            if no == 'S1': sc += math.log1p(L.get(k, {}).get('seo', 0))       # 서술형 출제 이력
            out.append((sc, k))
        return sorted(out, reverse=True)
    backup = {}
    for no, sv, rng in order:
        c = cands(no, sv, rng)
        if not c: c = cands(no, sv, (rng[0] - 1, rng[1] + 1))
        if not c: c = cands(no, sv, (rng[0] - 2, rng[1] + 2))
        if not c and sv in ('평', 'LU'): c = cands(no, 'LU' if sv == '평' else '평', rng)    # 고난도 출처끼리 바꿈
        if not c:                                                                             # 미사용 원문이 바닥나면 재출제(다른 후보로, front 3절)
            saved = set(used); used.clear(); used |= recent | {x for x, n in UC.items() if n > cap(rno)}; c = cands(no, sv, (rng[0] - 1, rng[1] + 1)); used.clear(); used |= saved
            if c: reuse.add(no)
        if not c: c = cands(no, sv, (rng[0] - 2, rng[1] + 2), loose=True)                  # 단원 쿼터가 남은 쪽만 남았을 때
        if not c: raise SystemExit(f'{no}번 자리 후보 없음 — 출처 {sv}, 난도 {rng}, 단원 쿼터 {quota}')
        k = c[0][1]; pick[no] = k; quota[k[0]] -= 1
        if no in HARD: backup[no] = [x for _, x in c[1:8]]          # 독립 검토 2번 탈락 시 바꿀 예비 원문(5번 개선)
    # 그림 2–3개를 9번 이후로 (모자라면 같은 출처·단원 쿼터 안에서 그림 원문으로 교체)
    figs = [n for n, k in pick.items() if has_fig(k)]
    for no, sv, rng in sorted(SLOTS, key=lambda s: -score(pick[s[0]]) if s[0] not in (17, 18, 'S2') else 99):
        if len(figs) >= 1: break
        if not isinstance(no, int) or no < 9 or no in (17, 18) or has_fig(pick[no]): continue
        old = pick[no]; quota[old[0]] += 1; pick.pop(no)
        c = cands(no, sv, (rng[0] - 1, rng[1] + 1), need_fig=True)
        if c: pick[no] = c[0][1]; quota[c[0][1][0]] -= 1; figs.append(no)
        else: pick[no] = old; quota[old[0]] -= 1
    used_now = set(pick.values()); bk = {}
    for n in HARD:                                                     # 자리끼리 겹치지 않게 2개씩
        bk[n] = [b for b in backup.get(n, []) if b not in used_now][:2]; used_now |= set(bk[n])
    ux = unexpected_slots(rno)
    def mode(n): return '킬러(설계A·B)' if n in (17, 18) else '예상밖' if n in ux else '학교식'
    def kinfo(k):
        kv = (DB.get(k, {}).get('킬러') or {}).get('검산', {})
        return {t: (kv.get('설계' + t, {}).get('판정'), (kv.get('설계' + t, {}).get('수정_적용') or {}).get('확정답')) for t in 'AB'} if kv else None
    return {str(n): dict(key=k, src=src(k), level=F.D[k][0], live=L.get(k, {}).get('n', 0), score=round(score(k), 2), fig=has_fig(k), y25=k in Y25, topics=sorted(topics(k)),
                         mode=mode(n), **({'재출제': True} if n in reuse else {}), **({} if n in (17, 18) else db_hint(k, n, mode(n))), **({'killer': kinfo(k)} if n in (17, 18) else {}),
                         **({'backup': bk[n]} if n in HARD else {}))
            for n, k in sorted(pick.items(), key=lambda z: 19 if z[0] == 'S1' else 20 if z[0] == 'S2' else z[0])}

ORDER_SCHOOL = ['후보_순위']
def next_ref(k, mode, taken, rno=0):
    """원문 k에서 아직 안 쓴 DB 후보 하나. 학교식: 후보_순위 차례, 예상밖: 예상밖 → v3_추가 → 결합, 킬러: 설계A → 설계B."""
    e = DB.get(k, {})
    if mode.startswith('킬러'): opts = [f'{k} 킬러 설계A', f'{k} 킬러 설계B'] if e.get('킬러') else []
    elif mode == '학교식': opts = [f"{k} 후보_순위 {c.get('순위', i + 1)}" for i, c in enumerate(e.get('후보_순위', []))] + [f'{k} 학교식_예상 {i + 1}' for i in range(len(e.get('학교식_예상', [])))]
    else:   # 예상밖 자리: 예상밖·점검표(v3)·결합을 번갈아(점검표 조작이 두 회차마다 나오게, front 3절)
        A = [[f'{k} 예상밖 {i + 1}' for i in range(len(e.get('예상밖_포인트', [])))], [f'{k} v3_추가 {i + 1}' for i in range(len(e.get('v3_추가_예상', [])))], [f'{k} 결합 {i + 1}' for i in range(len(e.get('결합_후보', [])))]]
        A = A[rno % 3:] + A[:rno % 3]                                   # 회차마다 시작 종류를 돌림
        opts = [x for t in itertools.zip_longest(*A) for x in t if x]
    for o in opts:
        if o not in taken: return o
    return opts[0] + ' (다시)' if opts else f'{k} 자체'

def schedule(r0, r1, used=()):
    """r0–r1회 회차표: 회차마다 자리·원문·mode·db_ref. 같은 원문은 3회 안에 다시 안 씀. 원문 재사용은 cap()까지, 매번 다른 후보."""
    used = list(used); taken = set(); hist = []; out = {}
    for r in range(r0, r1 + 1):
        recent = {k for h in hist[-3:] for k in h}
        j = plan(r, used, recent); row = {}
        for n, v in j.items():
            ref = next_ref(v['key'], v['mode'], taken, r); taken.add(ref)
            row[n] = dict(key=v['key'], src=v['src'], level=v['level'], mode=v['mode'], db_ref=ref, **({'재출제': True} if v.get('재출제') else {}), **({'횟수': used.count(v['key']) + 1}))
        used += [v['key'] for v in j.values()]; hist.append([v['key'] for v in j.values()]); out[str(r)] = row
    return out

if __name__ == '__main__' and sys.argv[1] == 'schedule':
    a = sys.argv[2:]; used = a[2].split(',') if len(a) > 2 else []
    S = schedule(int(a[0]), int(a[1]), used)
    json.dump(S, open(os.path.join(HERE, 'schedule.json'), 'w'), ensure_ascii=False, indent=1)
    C = collections.Counter(used + [v['key'] for row in S.values() for v in row.values()])
    print('회차', len(S), '자리', sum(len(r) for r in S.values()), '원문 노출 횟수 분포', dict(sorted(collections.Counter(C[k] for k in F.I).items())), '미노출', sorted(set(F.I) - set(C)))
    print('db_ref 종류', dict(collections.Counter(v['db_ref'].split()[1] for row in S.values() for v in row.values())), '(다시)', sum('(다시)' in v['db_ref'] for row in S.values() for v in row.values()))
    sys.exit(0)

if __name__ == '__main__':
    if sys.argv[1] == 'rank': rank()
    else:
        a = sys.argv[2:]
        rno = int(a[0]); a = a[1:]
        if a and a[0] in ('학교형', '복습형'): a = a[1:]          # 옛 형식(유형 무시)
        P = plan(rno, a[0].split(',') if a and a[0] else ())
        print(json.dumps(P, ensure_ascii=False, indent=1))
        print('단원', collections.Counter(v['key'][0] for v in P.values()), '출처', collections.Counter(v['src'] for v in P.values()), '그림', [n for n, v in P.items() if v['fig']])
        print('소재', dict(collections.Counter(tp for v in P.values() for tp in v['topics'])), '상한', TOPIC_LIMIT)
