# -*- coding: utf-8 -*-
"""인쇄용 잉크 절약: 원본 시험지 PDF의 모든 쪽 위에 반투명 흰 막을 한 겹 얹어 검정을 짙은 회색으로 낮춘다(벡터 유지).
사용: python3 inksave.py <입력.pdf> [<출력.pdf>] [--level 0.14]   (출력을 빼면 제자리에 덮어씀)
2026-11-25 사용자: "인쇄할 때 잉크 많은 곳 걸리는데 약간만 줄여줘 — 스캔본 말고 원본을". 기본 0.14 = 검정 → 약 86% 농도."""
import sys, argparse, os, pymupdf

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out', nargs='?'); ap.add_argument('--level', type=float, default=0.14)
    a = ap.parse_args()
    doc = pymupdf.open(a.src)
    if doc.metadata.get('subject') == 'inksave':
        print(a.src, '이미 잉크 절약판'); return
    for p in doc:
        p.draw_rect(p.rect, color=None, fill=(1, 1, 1), fill_opacity=a.level, overlay=True, width=0)
    md = dict(doc.metadata); md['subject'] = 'inksave'; doc.set_metadata(md)
    out = a.out or a.src
    tmp = out + '.tmp.pdf'; doc.save(tmp, garbage=3, deflate=True); doc.close(); os.replace(tmp, out)
    print(out, '잉크 절약', a.level)

if __name__ == '__main__':
    main()
