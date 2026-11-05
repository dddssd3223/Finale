# -*- coding: utf-8 -*-
"""학교 출제 예측 순위 + 회차 분담 초안 (front.md 0-8, 1절 출처 배치)
점수 = 라이브 빈도(전국 학교 기출 횟수) + 최근(2024–25) 가중 + 번호 자리 적합(라이브 출제 번호 중앙값과의 거리) + 분석집 포함 가산
사용: python3 predict.py rank            # 원문 예측 점수표
      python3 predict.py plan <회차번호> <학교형|복습형> [사용한 키 쉼표목록]   # 분담 초안(JSON)
제약: 출처 평가원 6·EBS 6·Level Up 6·자체 2, 단원 D5 M5 I6 J4(1–4번 J 없음), 원본 난도 자리별 범위,
      그림 원문은 9번 이후 2–3개(1–8번 제외), 학교형은 예측 상위부터, 복습형은 분석집 원문 우선."""
import sys, os, json, math, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '부교재_기말')); import items_final as F
L = json.load(open(os.path.join(HERE, 'livestats.json')))
STUDY = set(json.load(open(os.path.join(HERE, 'study_keys.json'))))
# 자리: (번호, 출처, 원본 난도 범위) — 2학기 중간 출처 배치(확정·유력·유동) 그대로
SLOTS = [(1, 'E', (2, 3)), (2, 'E', (2, 3)), (3, 'E', (2, 3)), (4, '평', (1, 3)), (5, 'E', (4, 5)), (6, 'E', (4, 5)), (7, 'LU', (4, 5)), (8, 'E', (4, 5)),
         (9, '평', (3, 5)), (10, '평', (4, 5)), (11, 'LU', (4, 5)), (12, 'LU', (5, 6)), (13, 'LU', (4, 5)), (14, '자체', (4, 5)), (15, '평', (6, 6)),
         (16, '평', (6, 7)), (17, 'LU', (5, 7)), (18, 'LU', (5, 7)), ('S1', '자체', (1, 4)), ('S2', '평', (6, 7))]
QUOTA = dict(D=5, M=5, I=6, J=4)

def src(k):
    t = F.D[k][1]
    return 'LU' if t == 'Level Up' else '평' if t == '평가원 기출' else 'E'

def has_fig(k): return 'fig' in F.I[k][0]

def score(k, slot=None):
    l = L.get(k, {}); n = l.get('n', 0); yr = l.get('years', {})
    s = math.log1p(n) + 0.4 * math.log1p(yr.get('2024', 0) + yr.get('2025', 0)) + (0.2 if k in STUDY else 0)
    if slot is not None and isinstance(slot, int) and n:
        s -= abs(l.get('median', slot) - slot) / 8
    return s

def rank():
    rows = sorted(F.I, key=lambda k: -score(k))
    for k in rows[:60]:
        l = L.get(k, {})
        print(f"{k:4} 점수 {score(k):.2f} 라이브 {l.get('n', 0):2} (최근 {l.get('years', {}).get('2024', 0) + l.get('years', {}).get('2025', 0)}) 자리중앙 {l.get('median', '-')} 서술 {l.get('seo', 0)} {src(k)} 난도 {F.D[k][0]} {'그림' if has_fig(k) else ''} {'분석집' if k in STUDY else ''}")

def plan(rtype, used=()):
    used = set(used); quota = dict(QUOTA); pick = {}
    order = [s for s in SLOTS if s[0] in (17, 18, 'S2', 15, 16)] + [s for s in SLOTS if s[0] not in (17, 18, 'S2', 15, 16)]
    def cands(no, sv, rng, need_fig=None):
        out = []
        for k in F.I:
            if k in used or k in pick.values(): continue
            u = k[0]
            if quota[u] <= 0 or (isinstance(no, int) and no <= 4 and u == 'J'): continue
            if sv == '자체':
                if src(k) != 'E': continue
            elif src(k) != sv: continue
            if not (rng[0] <= F.D[k][0] <= rng[1]): continue
            if isinstance(no, int) and no <= 8 and has_fig(k): continue          # 1–8번 그림 없음
            if need_fig is not None and has_fig(k) != need_fig: continue
            sc = score(k, no if isinstance(no, int) else 20)
            if no == 'S1': sc += math.log1p(L.get(k, {}).get('seo', 0))       # 서술형 출제 이력
            if rtype == '복습형' and k in STUDY and isinstance(no, int) and no <= 16: sc += 1.0
            out.append((sc, k))
        return sorted(out, reverse=True)
    for no, sv, rng in order:
        c = cands(no, sv, rng)
        if not c: c = cands(no, sv, (rng[0] - 1, rng[1] + 1))
        k = c[0][1]; pick[no] = k; quota[k[0]] -= 1
    # 그림 2–3개를 9번 이후로 (모자라면 같은 출처·단원 쿼터 안에서 그림 원문으로 교체)
    figs = [n for n, k in pick.items() if has_fig(k)]
    for no, sv, rng in sorted(SLOTS, key=lambda s: -score(pick[s[0]]) if s[0] not in (17, 18, 'S2') else 99):
        if len(figs) >= 2: break
        if not isinstance(no, int) or no < 9 or no in (17, 18) or has_fig(pick[no]): continue
        old = pick[no]; quota[old[0]] += 1; pick.pop(no)
        c = cands(no, sv, (rng[0] - 1, rng[1] + 1), need_fig=True)
        if c: pick[no] = c[0][1]; quota[c[0][1][0]] -= 1; figs.append(no)
        else: pick[no] = old; quota[old[0]] -= 1
    return {str(n): dict(key=k, src=src(k), level=F.D[k][0], live=L.get(k, {}).get('n', 0), score=round(score(k), 2), fig=has_fig(k), study=k in STUDY)
            for n, k in sorted(pick.items(), key=lambda z: 19 if z[0] == 'S1' else 20 if z[0] == 'S2' else z[0])}

if __name__ == '__main__':
    if sys.argv[1] == 'rank': rank()
    else:
        P = plan(sys.argv[3], sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else ())
        print(json.dumps(P, ensure_ascii=False, indent=1))
        print('단원', collections.Counter(v['key'][0] for v in P.values()), '출처', collections.Counter(v['src'] for v in P.values()), '그림', [n for n, v in P.items() if v['fig']])
