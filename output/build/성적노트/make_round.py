# -*- coding: utf-8 -*-
"""회차 성적표 한 장: python3 make_round.py <round.json> <out.html> [out.png]
round.json = {subject, exam, label, mc:[{n,a,m,p}], sa:[{name,items:[{k,p,g}]}], notes:[{q,pt,cat,note}],
              praise, history:[{r,total}], goal, cut1, footer}"""
import json, sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))

def build(src, out, png=None):
    d = json.load(open(src))
    t = open(os.path.join(HERE, 'round_tpl.html')).read()
    html = t.replace('__TITLE__', f"{d['label']} 성적표").replace('__DATA__', json.dumps(d, ensure_ascii=False))
    open(out, 'w').write(html)
    if png:
        subprocess.run(['node', os.path.join(HERE, 'shot_round.js'), out, png], check=True)

if __name__ == '__main__':
    build(*sys.argv[1:])
