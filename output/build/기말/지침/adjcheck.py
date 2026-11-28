# -*- coding: utf-8 -*-
"""이웃·같은 쪽 소재 겹침 검사: python3 adjcheck.py <회차 폴더>
2026-11-28 사용자: '13회 1,2번 같은 속도 문제, 같은 페이지에 넓이 그래프 두 개 — 지양'.
본문 낱말로 겉 소재를 잡는다(원문 키 소재가 아니라 시험지에 보이는 소재)."""
import sys, os, re, importlib.util
PAGES = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18]]
TOPIC = {'수직선 운동': r'수직선 위를 움직이는|속도|가속도|움직인 거리',
         '넓이': r'넓이',
         '실근 개수': r'실근의 개수|서로 다른 실근|교점의 개수|만나는 점의 개수',
         '접선': r'접선|접하는',
         '절댓값 함수': r'\\left\||\|f\(|\|g\(|\\lvert|\|x'}
def load(rd):
    spec = importlib.util.spec_from_file_location('c3', os.path.join(rd, 'content3.py'))
    m = importlib.util.module_from_spec(spec); cwd = os.getcwd(); sys.path.insert(0, rd); os.chdir(rd)
    try: spec.loader.exec_module(m)
    finally: os.chdir(cwd)
    return m.ITEMS
def tags(it):
    b = it['body'] + ' '.join(t for _, t in it.get('cond') or [])
    t = {k for k, p in TOPIC.items() if re.search(p, b)}
    return t, ('<img' in b or 'fig_' in b)
def check(rd):
    I = load(rd); T = {n: tags(I[n]) for n in I}; bad = []
    for n in range(1, 18):
        c = (T[n][0] & T[n + 1][0]) - {'절댓값 함수'}
        if c: bad.append(f'{n}·{n+1}번 이웃 소재 겹침: {"·".join(sorted(c))}')
    for pg in PAGES:
        figs = [n for n in pg if T[n][1]]
        if len(figs) >= 2: bad.append(f'{pg[0]}–{pg[-1]}번 같은 쪽에 그림 {len(figs)}개({figs})')
        for i, a in enumerate(pg):
            for b in pg[i + 1:]:
                if b == a + 1: continue
                c = (T[a][0] & T[b][0]) & {'넓이', '수직선 운동'}
                if c: bad.append(f'{a}·{b}번 같은 쪽 소재 겹침: {"·".join(sorted(c))}')
    return T, bad
def schedule(r):
    """회차 준비 때: schedule.json 원문 키 소재로 이웃·같은 쪽 겹침을 미리 본다. python3 adjcheck.py --schedule 15"""
    import json, predict as P
    s = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schedule.json')))[str(r)]
    T = {int(n): set(P.topics(v['key'])) for n, v in s.items() if n.isdigit()}
    bad = [f'{n}·{n+1}번 {"·".join(sorted(T[n] & T[n+1]))}' for n in range(1, 18) if T[n] & T[n + 1]]
    for pg in PAGES:
        for i, a in enumerate(pg):
            for b in pg[i + 1:]:
                if b != a + 1 and (T[a] & T[b]) & {'넓이', '수직선 운동'}: bad.append(f'{a}·{b}번 같은 쪽 {"·".join(sorted(T[a] & T[b]))}')
    return bad

if __name__ == '__main__' and sys.argv[1] == '--schedule':
    b = schedule(sys.argv[2]); print('\n'.join(b) or '겹침 없음'); sys.exit(1 if b else 0)
if __name__ == '__main__':
    T, bad = check(os.path.abspath(sys.argv[1]))
    for n in sorted(T): print(n, sorted(T[n][0]), '그림' if T[n][1] else '')
    print('\n'.join(bad) or '겹침 없음'); sys.exit(1 if bad else 0)
