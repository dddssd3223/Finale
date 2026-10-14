# 각 블록 높이를 재서 단에 차례로 채우는 PAGES를 만든다
import json, subprocess, os, re, sys
import build3 as B
keys = [f'Q{n}' for n in range(1, 22)] + ['SEC1'] + [f'S{n}' for n in range(1, 6)]
cols = [[(k, B.TOP)] for k in keys]
B.PAGES = [(cols[i], cols[i + 1] if i + 1 < len(cols) else []) for i in range(0, len(cols), 2)]
open('overlay_src.html', 'w').write(B.overlay_html())
subprocess.run(['node', 'render3.js', 'overlay_src.html', 'overlay.pdf'], check=True)
H = {b['k']: b['bottom'] - b['top'] for b in json.load(open('blocks.json'))}
GAP, BOT, P1 = 22, 772, 328.5
pages, col, y, start = [], [], None, None
allcols = []
first = True
for k in keys:
    h = H[k]
    y0 = (P1 if first else B.TOP) if not col else y
    if col and y + h > BOT:
        allcols.append(col); col = []; first = False; y0 = B.TOP
    if k == 'SEC1' and col:
        allcols.append(col); col = []; first = False; y0 = B.TOP
    col.append((k, round(y0, 1))); y = y0 + h + (GAP if not k.startswith('S') else 26)
    if k == 'SEC1': y = y0 + h + 4
allcols.append(col)
# 단 안의 남는 공간을 문항 사이에 고르게 나눔
out = []
for c in allcols:
    last = c[-1]; used = last[1] + H[last[0]]
    extra = max(0, BOT - used) / max(1, len(c)) if len(allcols) > 1 else 0
    extra = min(extra, 60)
    out.append([(k, round(y + i * extra, 1)) for i, (k, y) in enumerate(c)])
pp = [(out[i], out[i + 1] if i + 1 < len(out) else []) for i in range(0, len(out), 2)]
print(H)
print(len(out), 'columns')
for p in pp: print(p)
json.dump(pp, open('pages.json', 'w'))
