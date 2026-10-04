# -*- coding: utf-8 -*-
# 학생용 서답형 답안지 (A4 세로)
import os, subprocess, sys
from content3 import S1S, S2S
from build3 import font_css, HERE

CSS = r"""
@page{size:A4;margin:14mm 14mm 12mm 14mm}
html,body{margin:0;background:#fff}
body{font-family:'GL';color:#000;-webkit-text-stroke:.15pt #000}
.hd{text-align:center;padding:0 2pt 4pt}
.ti{font-size:19pt;letter-spacing:.5pt}
.ti .s{font-size:14pt}
.id{font-size:11.5pt;white-space:pre;text-align:right;margin-top:7pt}
.rule{border-top:2.4pt solid #000;border-bottom:.8pt solid #000;height:1.6pt;margin-bottom:9pt}
.sec{margin-bottom:9pt}
.sh{display:flex;justify-content:space-between;align-items:center;border:1pt solid #000;border-bottom:0;
    background:#e6e6e6;padding:3pt 7pt;font-size:11pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.bx{border:1pt solid #000;position:relative}
.bx+.bx{border-top:.6pt solid #000}
.bx .l{position:absolute;left:6pt;top:4pt;font-size:10.5pt}
.bx .p{position:absolute;right:6pt;top:4pt;font-size:9.5pt}
"""
UNIT = 32.0   # 1점당 칸 높이(pt)

def sec(n, subs):
    tot = sum(float(p[:-1]) for _, p in subs)
    h = [f'<div class="sec"><div class="sh"><span>서답형 {n}</span><span>[{tot:g}점]</span></div>']
    for i, (_, p) in enumerate(subs, 1):
        h.append(f'<div class="bx" style="height:{float(p[:-1]) * UNIT:.1f}pt"><span class="l">({i})</span><span class="p">[{p}]</span></div>')
    return ''.join(h) + '</div>'

def build(out):
    h = (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>'
         '<div class="hd"><div class="ti">( 미적분Ⅰ )<span class="s">과</span> 서답형 답안지</div>'
         '<div class="id">2학년 (     )반 (     )번  이름 (                  )</div></div><div class="rule"></div>'
         + sec(1, S1S) + sec(2, S2S) + '</body></html>')
    src = os.path.join(HERE, 'ans_src.html')
    open(src, 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'ans_src.html', 'ans_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'ans_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
