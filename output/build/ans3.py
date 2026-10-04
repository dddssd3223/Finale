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
.g{display:grid;grid-template-columns:1fr 38pt 38pt;border:1pt solid #000;margin-bottom:8pt}
.g>div{border-right:.6pt solid #000;border-bottom:.6pt solid #000;position:relative;box-sizing:border-box}
.g>div:nth-child(3n){border-right:0}
.g>div.last{border-bottom:0}
.sh{background:#e6e6e6;-webkit-print-color-adjust:exact;print-color-adjust:exact;
    display:flex;justify-content:space-between;align-items:center;padding:3pt 7pt;font-size:11pt}
.gh{background:#e6e6e6;-webkit-print-color-adjust:exact;print-color-adjust:exact;
    display:flex;align-items:center;justify-content:center;font-size:9.5pt}
.g .l{position:absolute;left:6pt;top:4pt;font-size:10.5pt}
.g .p{position:absolute;right:6pt;top:4pt;font-size:9.5pt}
.sub{display:flex;justify-content:flex-end;align-items:center;padding:0 7pt;font-size:10pt;height:20pt}
.tg{display:grid;grid-template-columns:1fr 38pt 38pt;border:1.2pt solid #000}
.tg>div{border-right:.6pt solid #000;border-bottom:.6pt solid #000;box-sizing:border-box;height:22pt;
    display:flex;align-items:center;justify-content:center;font-size:10pt}
.tg>div:nth-child(3n){border-right:0}
.tg>div.last{border-bottom:0}
.tg>div.k{justify-content:flex-end;padding-right:7pt}
.only{text-align:right;font-size:9pt;margin:0 0 2pt;padding-right:2pt}
"""
UNIT = 26.5   # 1점당 칸 높이(pt)

def sec(n, subs, kind='서술형', unit=None):
    unit = unit or UNIT
    tot = sum(float(p[:-1]) for _, p in subs)
    h = ['<div class="g">',
         f'<div class="sh"><span>{kind} {n}</span><span>[{tot:g}점]</span></div><div class="gh">초검</div><div class="gh">재검</div>']
    for i, (_, p) in enumerate(subs, 1):
        st = f'height:{float(p[:-1]) * unit:.1f}pt'
        h.append(f'<div style="{st}"><span class="l">({i})</span><span class="p">[{p}]</span></div><div></div><div></div>')
    h.append('<div class="sub last">소 계</div><div class="last"></div><div class="last"></div></div>')
    return ''.join(h)

def build(out):
    h = (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>'
         '<div class="hd"><div class="ti">( 미적분Ⅰ )<span class="s">과</span> 서답형 답안지</div>'
         '<div class="id">2학년 (     )반 (     )번  이름 (                  )</div></div><div class="rule"></div>'
         '<div class="only">※ 초검·재검란은 채점자 전용 (학생 기재 금지)</div>'
         + sec(1, S1S, '단답형', 15.0) + sec(1, S2S, '서술형', 42.0) +
         '<div class="tg"><div class="k">서답형 총점 (20점)</div><div></div><div></div>'
         '<div class="k last">채점자 확인</div><div class="last"></div><div class="last"></div></div>'
         '</body></html>')
    src = os.path.join(HERE, 'ans_src.html')
    open(src, 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'ans_src.html', 'ans_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'ans_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
