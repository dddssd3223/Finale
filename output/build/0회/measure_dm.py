# 원본 스캔에서 디스플레이 수식의 왼쪽 끝(pt) 재기
import json, numpy as np
import align; align.z = 4; z = 4
dm = json.load(open('dm.json')); cache = {}; cnt = {}
for d in dm:
    pg = d['pg']
    if pg not in cache: cache[pg] = align.scan_ink(pg)
    ink = cache[pg]
    cl = 42.2 if d['x0'] < 290 else 301.5
    ya, yb = int((d['top'] + 1) * z), int((d['bot'] - 1) * z)
    xa, xb = int((cl + 7) * z), int((cl + 120) * z)
    cols = np.nonzero(ink[ya:yb, xa:xb].sum(0) > 1)[0]
    real = cl + 7 + cols[0] / z if len(cols) else None
    i = cnt.get(d['k'], 0); cnt[d['k']] = i + 1
    print(f"{d['k']}.{i}", round(d['x0'], 1), None if real is None else round(real, 1))
