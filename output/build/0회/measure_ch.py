# 선택지 줄의 세로 어긋남(pt): 우리 렌더 vs 원본 스캔 (2차원 상관)
import json, numpy as np, pymupdf
import align; z = align.z = 3
doc = pymupdf.open('exam.pdf'); ch = json.load(open('ch.json')); A = {}; B = {}
for c in ch:
    pg = c['pg']
    if pg not in A: A[pg] = align.scan_ink(pg); B[pg] = align.our_ink(doc, pg)
    y0, y1 = int((c['top'] - 2) * z), int((c['bot'] + 2) * z)
    xa, xb = int((c['x0'] - 2) * z), int((c['x0'] + 245) * z)
    ob = B[pg][y0:y1, xa:xb].astype(np.float32); best = None
    for d in range(-14 * z, 14 * z + 1):
        sb = A[pg][y0 + d:y1 + d, xa:xb].astype(np.float32)
        sc = (ob * sb).sum() / (np.sqrt(ob.sum() * sb.sum()) + 1e-6)
        if best is None or sc > best[0]: best = (sc, d / z)
    print(c['k'], round(best[1], 2), round(best[0], 2))
