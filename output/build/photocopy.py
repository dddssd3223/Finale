# -*- coding: utf-8 -*-
"""벡터 PDF를 학교 복사본처럼: 검정을 약간 회색으로, 획을 살짝 번지게, 토너 얼룩·미세 기울기"""
import sys, io, random
import numpy as np, pymupdf
from PIL import Image, ImageFilter
def copy_look(src, out, dpi=200, ink=70, seed=3):
    rng = np.random.default_rng(seed); random.seed(seed)
    d = pymupdf.open(src); o = pymupdf.open()
    for i, p in enumerate(d):
        pix = p.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
        im = Image.frombytes('L', (pix.width, pix.height), pix.samples)
        im = im.filter(ImageFilter.GaussianBlur(0.55))
        a = np.asarray(im).astype(np.float32) / 255.0
        a = ink / 255.0 + a * (1 - ink / 255.0)               # 가장 진한 부분 ≈ #464646
        a += rng.normal(0, 0.018, a.shape)                     # 종이·토너 잡음
        # 듬성듬성 옅은 얼룩
        h, w = a.shape
        yy, xx = np.mgrid[0:h, 0:w]
        for _ in range(3):
            cy, cx, r = rng.uniform(0, h), rng.uniform(0, w), rng.uniform(150, 400)
            a -= 0.02 * np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * r * r))
        # 작은 점(먼지)
        for _ in range(40):
            y, x = int(rng.uniform(0, h - 3)), int(rng.uniform(0, w - 3))
            a[y:y + 2, x:x + 2] -= rng.uniform(0.15, 0.4)
        a = np.clip(a, 0, 1)
        im = Image.fromarray((a * 255).astype(np.uint8))
        im = im.rotate(random.uniform(-0.25, 0.25), resample=Image.BICUBIC, fillcolor=250)
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=80); buf.seek(0)
        np_ = o.new_page(width=p.rect.width, height=p.rect.height)
        np_.insert_image(np_.rect, stream=buf.read())
    o.save(out, garbage=3, deflate=True)
if __name__ == '__main__':
    copy_look(sys.argv[1], sys.argv[2], ink=int(sys.argv[3]) if len(sys.argv) > 3 else 70)
