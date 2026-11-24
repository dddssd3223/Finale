# -*- coding: utf-8 -*-
"""회차 성적표 한 장: python3 make_round.py <round.json> <out.html> [out.png]
round.json = {subject, exam, label, mc:[{n,a,m,p}], sa:[{name,items:[{k,p,g}]}], notes:[{q,pt,cat,note}],
              praise, history:[{r,total}], goal, cut1, footer}"""
import json, sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))

# 예상 등급컷: 난도 지수 = 1등급 변별 배점 + 0.5 × 2등급 변별 배점 (서답형 고난도 소문항 6점)
# 실제 1컷 기준점: 1학기 기말(지수 15.2) 90.1, 2학기 중간(지수 25.6) 90.1 → 지수 25.6 이하에서는 1컷 90.1로 고정.
# 그보다 어려우면 1학기 중간(지수 37.1, 1컷 약 81) 쪽으로 지수 1당 0.75점씩 내려감. 2컷은 1학기 기말 76.1·학원 예상 75.3 기준.
def cuts(idx):
    c1 = 90.1 - 0.75 * max(0.0, idx - 25.6)
    c2 = 75.8 - 1.0 * max(0.0, idx - 25.6)
    return round(c1, 1), round(c2, 1)

# 내 위치(370명 환산, 5등급제 누적 10·34·66·90%): 3·4컷은 1학기 기말 실제 컷 간격(90.1/76.1/55.8/27.7)을
# 이번 회 1·2컷 간격에 맞춰 늘리거나 줄여 정하고, 컷 사이는 직선으로 이어 백분위를 구함.
REAL = (90.1, 76.1, 55.8, 27.7)
def rank(total, c1, c2, n=370):
    k = (c1 - c2) / (REAL[0] - REAL[1])
    c3, c4 = c2 - k * (REAL[1] - REAL[2]), c2 - k * (REAL[1] - REAL[3])
    pts = [(100, 0), (c1, 10), (c2, 34), (c3, 66), (max(c4, 1), 90), (0, 100)]
    for (s0, p0), (s1, p1) in zip(pts, pts[1:]):
        if s1 <= total <= s0:
            pct = p0 + (s0 - total) / (s0 - s1) * (p1 - p0); break
    return dict(n=n, cuts=[round(c, 1) for c in (c1, c2, c3, c4)], pct=round(pct, 1), pos=max(1, round(pct / 100 * n)))

def build(src, out, png=None):
    d = json.load(open(src))
    if 'idx' in d and 'cut1' not in d:
        d['cut1'], d['cut2'] = cuts(d['idx'])
    tot = sum(q['p'] for q in d['mc'] if q['a'] == q['m']) + sum(i['g'] for s in d['sa'] for i in s['items'])
    d['rank'] = rank(tot, d['cut1'], d['cut2'])
    for h in d.get('history', []):
        if 'idx' in h and 'cut1' not in h: h['cut1'] = cuts(h['idx'])[0]
    t = open(os.path.join(HERE, 'round_tpl.html')).read()
    html = t.replace('__TITLE__', f"{d['label']} 성적표").replace('__DATA__', json.dumps(d, ensure_ascii=False))
    open(out, 'w').write(html)
    if png:
        subprocess.run(['node', os.path.join(HERE, 'shot_round.js'), out, png], check=True)

if __name__ == '__main__':
    build(*sys.argv[1:])
