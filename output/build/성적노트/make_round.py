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

def build(src, out, png=None):
    d = json.load(open(src))
    if 'idx' in d and 'cut1' not in d:
        d['cut1'], d['cut2'] = cuts(d['idx'])
    for h in d.get('history', []):
        if 'idx' in h and 'cut1' not in h: h['cut1'] = cuts(h['idx'])[0]
    t = open(os.path.join(HERE, 'round_tpl.html')).read()
    html = t.replace('__TITLE__', f"{d['label']} 성적표").replace('__DATA__', json.dumps(d, ensure_ascii=False))
    open(out, 'w').write(html)
    if png:
        subprocess.run(['node', os.path.join(HERE, 'shot_round.js'), out, png], check=True)

if __name__ == '__main__':
    build(*sys.argv[1:])
