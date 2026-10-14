# -*- coding: utf-8 -*-
"""우리 렌더의 '⏎' 줄(jl.json)마다, 원본 스캔에서 같은 줄의 오른쪽 끝(pt)을 잰다 → jlw.json(줄 너비)."""
import json, os, sys, numpy as np, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'myexam'))
from regoff import S, off
SC = [os.path.join(HERE, '..', 'myexam', f) for f in ('a.pdf', 'b.pdf')]
z = 4
from align import scan_ink as _si
import align; align.z = z
def page_img(pg):
    return _si(pg)
cache = {}
jl = json.load(open(os.path.join(HERE, 'jl.json')))
out, rep = {}, []
for L in jl:
    pg = L['pg']
    if pg not in cache: cache[pg] = page_img(pg)
    ink = cache[pg]
    P = lambda x, y: (int(round(x * z)), int(round(y * z)))
    colR = 295 if L['x0'] < 200 else 556
    xa, ya = P(L['x0'], L['top'] - 8); xb, yb = P(colR, L['bot'] + 8)
    reg = ink[ya:yb, xa:xb]
    rows = reg[:, :int(60 * z)].sum(1) > 0                          # 줄 왼쪽 60pt 안에 글자가 있는 행
    # 행 묶음(글줄) 찾기 → 우리 줄 중심에 가장 가까운 묶음
    bands, cur = [], None
    for i, r in enumerate(rows):
        if r and cur is None: cur = i
        if not r and cur is not None:
            if i - cur > 3 * z: bands.append((cur, i))
            cur = None
    if cur is not None: bands.append((cur, len(rows)))
    mid = ((L['top'] + L['bot']) / 2 - (L['top'] - 8)) * z
    if not bands: rep.append((L['id'], 'no band')); continue
    b0, b1 = min(bands, key=lambda b: abs((b[0] + b[1]) / 2 - mid))
    cols = reg[b0:b1].sum(0) > 0
    last, gap = 0, 0
    for x, c in enumerate(cols):
        if c: last, gap = x, 0
        else:
            gap += 1
            if gap > 14 * z and last > 0: break
    right = L['x0'] + last / z
    out[L['id']] = round(right - L['x0'], 1)
    rep.append((L['id'], round(L['x1'], 1), round(right, 1)))
json.dump(out, open(os.path.join(HERE, 'jlw_meas.json'), 'w'), indent=0)
for r in rep: print(*r)
