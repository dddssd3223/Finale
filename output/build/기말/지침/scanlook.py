# -*- coding: utf-8 -*-
"""시험지 PDF → 실제 학교 스캔본처럼 보정한 PDF.
사용: python3 scanlook.py <입력.pdf> <출력.pdf> [--seed N] [--white]
학교 스캔본 실측(2025 2학기 중간·기말, 2026 1학기 중간 업로드본):
  쪽 1190×1683 px(약 144dpi) JPEG, 종이 RGB≈(253,251,234) 크림색(--white면 흰 종이 253), 종이 얼룩 표준편차≈7,
  잉크≈(44,44,40) 짙은 회색, 획이 조금 굵고, 뒷면 글씨가 거울상으로 희미하게 비침, 약한 기울어짐·압축 깍두기."""
import sys, io, argparse
import numpy as np
import pymupdf
from PIL import Image, ImageFilter

W, H = 1190, 1683          # 학교 스캔 쪽 크기(px)
PAPER = np.array([253.4, 251.0, 234.5])
PAPER_W = np.array([253.3, 253.3, 253.3])
INK = np.array([44.0, 44.5, 40.0])

def gray(page, scale=2):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(W * scale / page.rect.width, H * scale / page.rect.height), colorspace=pymupdf.csGRAY)
    return Image.frombytes('L', (pix.width, pix.height), pix.samples)

def lowfreq(rng, h, w, amp, cells=6):
    """종이 밝기 얼룩(넓은 범위)"""
    g = rng.normal(0, 1, (cells, cells)).astype(np.float32)
    im = Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return (np.asarray(im, np.float32) / 255 - 0.5) * 2 * amp

def one(page, back, rng, white):
    S = 2
    g = gray(page, S)
    # 획 굵게(복사·스캔 번짐): 최소 필터를 반쯤 섞음
    thick = g.filter(ImageFilter.MinFilter(3))
    g = Image.blend(g, thick, 0.45).filter(ImageFilter.GaussianBlur(0.35 * S))
    ink = 1 - np.asarray(g.resize((W, H), Image.LANCZOS), np.float32) / 255      # 0 종이 … 1 잉크
    ink = np.clip((ink - 0.04) / 0.72, 0, 1) ** 0.8                              # 대비: 엷은 회색은 날리고 획은 진하게
    # 뒷면 비침(거울상, 흐리게)
    if back is not None:
        b = 1 - np.asarray(gray(back, 1).transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(1.6)), np.float32) / 255
        ink = np.maximum(ink, b * rng.uniform(0.06, 0.09))
    paper = (PAPER_W if white else PAPER)[None, None, :] + lowfreq(rng, H, W, 3.0)[..., None]
    paper = paper + rng.normal(0, 2.6, (H, W, 1))                                  # 종이 결
    rgb = paper * (1 - ink[..., None]) + INK[None, None, :] * ink[..., None]
    rgb += rng.normal(0, 3.0, (H, W, 3)) * ink[..., None]                          # 잉크 얼룩
    # 작은 티끌
    for _ in range(rng.integers(15, 40)):
        y, x = rng.integers(0, H), rng.integers(0, W); r = rng.integers(1, 3)
        rgb[max(0, y - r):y + r, max(0, x - r):x + r] *= rng.uniform(0.55, 0.9)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB')
    # 약한 기울어짐·밀림(스캐너 급지)
    fill = tuple(int(v) for v in (PAPER_W if white else PAPER))
    im = im.rotate(rng.uniform(-0.35, 0.35), resample=Image.BICUBIC, fillcolor=fill,
                   translate=(int(rng.integers(-6, 7)), int(rng.integers(-5, 6))))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=int(rng.integers(52, 60)), subsampling=2); return buf.getvalue()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--seed', type=int, default=7); ap.add_argument('--white', action='store_true')
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    src = pymupdf.open(a.src); out = pymupdf.open()
    for i, p in enumerate(src):
        back = src[i + 1] if i + 1 < len(src) else None      # 양면 인쇄: 다음 쪽이 뒷면
        jpg = one(p, back, rng, a.white)
        q = out.new_page(width=p.rect.width, height=p.rect.height)
        q.insert_image(q.rect, stream=jpg)
    out.set_metadata({'title': src.metadata.get('title', ''), 'author': src.metadata.get('author', '')})
    out.save(a.out, garbage=4, deflate=True)
    print(a.out, len(out), 'pages')

if __name__ == '__main__':
    main()
