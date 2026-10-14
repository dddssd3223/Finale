# -*- coding: utf-8 -*-
"""블록(문항)마다 우리 렌더와 원본 스캔을 2차원 상관으로 맞춰 세로 어긋남(pt)을 잰다."""
import json, os, sys, numpy as np, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'myexam'))
from regoff import S, off
SC = [os.path.join(HERE, '..', 'myexam', f) for f in ('a.pdf', 'b.pdf')]
z = 3
def scan_ink(pg):
    f, sp = SC[pg // 4], pg % 4
    OX, OY = off(f, sp)
    # 스캔 전체를 그린 뒤, 우리 좌표계(pt*z 픽셀)로 평행이동 (음수 OY도 정확히)
    pix = pymupdf.open(f)[sp].get_pixmap(matrix=pymupdf.Matrix(z / S, z / S))
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[..., :3].astype(int)
    ink = (a.max(-1) < 120) & ((a.max(-1) - a.min(-1)) < 60)
    out = np.zeros((int(842 * z) + 1, int(595 * z) + 1), bool)
    dx, dy = int(round(OX * z / S)), int(round(OY * z / S))
    H, W = out.shape
    ys, xs = np.arange(H) + dy, np.arange(W) + dx
    vy, vx = (ys >= 0) & (ys < ink.shape[0]), (xs >= 0) & (xs < ink.shape[1])
    out[np.ix_(vy, vx)] = ink[np.ix_(ys[vy], xs[vx])]
    return out
def our_ink(doc, pg):
    pix = doc[pg].get_pixmap(matrix=pymupdf.Matrix(z, z), colorspace=pymupdf.csGRAY)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w) < 128
if __name__ == '__main__':
    doc = pymupdf.open(os.path.join(HERE, 'exam.pdf'))
    blocks = json.load(open(os.path.join(HERE, 'blocks.json')))
    from build3 import PAGES
    order = []
    for pi, (L, R) in enumerate(PAGES):
        for x, col in ((42.2, L), (301.5, R)):
            for k, y in col:
                if y is not None: order.append((pi, x, k))
    res = {}
    for (pi, x, k), b in zip(order, blocks):
        assert b['k'] == k, (b, k)
        A, B = scan_ink(pi), our_ink(doc, pi)
        tp, bt = b['top'] - pi * 842, b['bottom'] - pi * 842
        y0, y1 = int(tp * z), int(min(tp + 160, bt, 775) * z)
        xa, xb = int((x - 4) * z), int((x + 250) * z)
        ob = B[y0:y1, xa:xb].astype(np.float32)
        best = None
        for d in range(-50 * z, 30 * z + 1):
            sb = A[y0 + d:y1 + d, xa:xb].astype(np.float32)
            if sb.shape != ob.shape: continue
            sc = (ob * sb).sum() / (np.sqrt(ob.sum() * sb.sum()) + 1e-6)
            if best is None or sc > best[0]: best = (sc, d / z)
        # 첫 글줄 띠(위·아래 끝)로 다시 맞춤
        from bands import bands
        ob_ = bands(B, x, tp - 2, tp + 30, 200)
        if ob_:
            ot, obm = ob_[0]
            sb_ = bands(A, x, ot + best[1] - 10, ot + best[1] + 30, 200)
            if sb_:
                st, sbm = min(sb_, key=lambda t: abs(t[0] - (ot + best[1])))
                best = (best[0], round(((st - ot) + (sbm - obm)) / 2, 2))
        res[k] = best
        print(f'{k:6s} p{pi+1} top {tp:.1f}  shift {best[1]:+.2f}  score {best[0]:.2f}')
    json.dump({k: v[1] for k, v in res.items()}, open(os.path.join(HERE, 'shift.json'), 'w'))
