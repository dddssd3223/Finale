# -*- coding: utf-8 -*-
"""원본 시험지 PDF(양정고 양식)의 벡터 페이지를 그대로 바탕으로 쓰고,
결재란 제거 · 머리글 일부 수정 · 본문 교체로 새 시험지 PDF를 만든다."""
import os, re, json, subprocess, sys
import pymupdf
from content3 import Q, ANS, S1, S1S, S2, S2S

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..')
FONTS = os.path.join(SCR, 'fonts')
TPL = os.path.join(SCR, 'src', 'f7.pdf')
GULIM = os.path.join(FONTS, 'gulim.ttf')
KATEX_CSS = os.path.join(SCR, 'node_modules', 'katex', 'dist', 'katex.min.css')

# ------------------------------------------------------------------ 본문 배치 (실제 시험지와 동일한 쪽 구성)
LX, RX, CW = 42.5, 301.6, 251.5          # 단 시작 x, 단 너비(pt)
TOP, MID = 155.0, 462.0                  # 단 첫 문항 y, 둘째 문항 y
PAGES = [
    ([('Q1', 352.0), ('Q2', 556.0)], [('Q3', TOP), ('Q4', MID)]),
    ([('Q5', TOP), ('Q6', MID)], [('Q7', TOP)]),
    ([('Q8', TOP)], [('Q9', TOP), ('Q10', MID)]),
    ([('Q11', TOP)], [('Q12', TOP)]),
    ([('Q13', TOP)], [('Q14', TOP)]),
    ([('Q15', TOP)], [('Q16', TOP)]),
    ([('Q17', TOP)], [('Q18', TOP)]),
    ([('SEC', TOP), ('S1', None)], [('S2', TOP), ('END', 640.0)]),
]

CIRC = '①②③④⑤'

def font_css():
    f = lambda n: 'file://' + os.path.join(FONTS, n)
    return f"""
@font-face{{font-family:'MJ';src:url('{f('9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf')}')}}
@font-face{{font-family:'MJ';src:url('{f('9Bty3DZF0dXLMZlywRbVRNhxy2pXV1A0.ttf')}');font-weight:700}}
@font-face{{font-family:'GL';src:url('{f('gulim_web.ttf')}')}}
@font-face{{font-family:'TN';src:url('{f('buE4poGnedXvwgX8.ttf')}')}}
@font-face{{font-family:'TN';src:url('{f('buE2poGnedXvwjX-fmE.ttf')}');font-style:italic}}
@font-face{{font-family:'TN';src:url('{f('buE1poGnedXvwj1AW0Fp.ttf')}');font-weight:700}}
@font-face{{font-family:'TN';src:url('{f('buEzpoGnedXvwjX-Rt1s0Co.ttf')}');font-weight:700;font-style:italic}}
"""

CSS = r"""
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:transparent}
body{font-family:'MJ','GL',serif;font-size:10pt;line-height:1.62;color:#000;word-break:keep-all}
.pg{width:595pt;height:842pt;position:relative;page-break-after:always;overflow:hidden}
.pg:last-child{page-break-after:auto}
.blk{position:absolute;width:251.5pt}
.katex{font-size:1.02em;font-family:'TN','KaTeX_Main',serif}
.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
.katex .text,.katex .text *{font-family:'MJ','TN'!important;font-style:normal}
.katex .mord,.katex .mbin,.katex .mrel,.katex .mpunct,.katex .mopen,.katex .mclose,.katex .mop,.katex .mathrm{font-family:'TN','KaTeX_Main'}
.katex-display{margin:.25em 0 .3em}
.q{text-align:justify;position:relative;padding-left:0}
.q .n{font-family:'TN';font-weight:700;font-style:italic;font-size:10.5pt;margin-right:2.5pt}
.pt{float:right;margin-left:4pt;white-space:nowrap}
.ch .c{font-family:'GL'}
.ch{display:flex;flex-wrap:wrap;margin-top:5pt;clear:both}
.ch>span{min-width:48pt;margin-right:0;white-space:nowrap}
.ch.g>span{width:33%}
.cond{border:.6pt solid #000;padding:3pt 6pt;margin:4pt 0;clear:both}
.ci{display:flex;gap:3pt}.ci .ck{flex:none}
.bogi{border:.6pt solid #000;margin:5pt 0 0;padding:1pt 7pt 4pt;clear:both}
.bogi legend{margin:0 auto;padding:0 5pt;font-family:'GL';font-size:9pt}
.bi{display:flex;gap:3pt;margin:1pt 0}.bi .bk{flex:none}
.fig{text-align:center;margin:4pt 0}
.sub{margin:6pt 0 0;padding-left:15pt;text-indent:-15pt;text-align:justify}
.sec .h{font-family:'GL';font-size:14pt;margin-bottom:3pt}
.sec .d{font-family:'GL';font-size:8.6pt}
.sec hr{border:0;border-top:1.4pt solid #000;margin:5pt 0 6pt}
.slab{font-family:'MJ';font-weight:700}
.end{text-align:center;font-family:'GL'}
.end .a{font-size:24pt;letter-spacing:1pt}
.end .b{font-size:14pt;line-height:1.75;margin-top:6pt}
.tot{text-align:right}
"""

def q_html(n):
    pt, body, ch = Q[n]
    body = body.replace('{PT}', f'<span class="pt">[{pt:.1f}점]</span>')
    g = all(c.startswith('T:') for c in ch)
    chs = ''.join(f'<span><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    return f'<div class="q"><span class="n">{n}.</span>{body}</div><div class="ch{" g" if g else ""}">{chs}</div>'

def s_html(lab, body, subs, total):
    sh = ''.join(f'<div class="sub">({i+1}) {t} [{p}]</div><div style="height:{h}pt"></div>'
                 for i, ((t, p), h) in enumerate(zip(subs, [26, 26, 0])))
    return (f'<div class="q"><span class="slab">{lab}</span><br>{body}'
            f'<div class="tot">[총 {total}점]</div></div>{sh}')

SEC = ('<div class="sec"><div class="h">&lt;서답형 문제 - 20점&gt;</div>'
       '<div class="d">서답형 문제(1~2번)는 서답형 답안지에 풀이과정을 상세히 쓰시오.</div><hr></div>')
END = ('<div class="end"><div class="a">♥수고하셨습니다♥</div>'
       '<div class="b">선택형 18문제 = 80점<br>서답형&nbsp;&nbsp;2문제 = 20점</div></div>')

def block(key):
    if key.startswith('Q'): return q_html(int(key[1:]))
    if key == 'S1': return s_html('서답형 1.', S1, S1S, 10)
    if key == 'S2': return s_html('서답형 2.', S2, S2S, 10)
    if key == 'SEC': return SEC
    if key == 'END': return END

def overlay_html():
    pages = []
    for L, R in PAGES:
        h = '<div class="pg">'
        for x, col in [(LX, L), (RX, R)]:
            flow = ''
            for key, y in col:
                if y is None:          # 앞 블록 바로 아래로 이어서 배치
                    flow += block(key); continue
                if flow: h += flow + '</div>'
                h += f'<div class="blk" data-k="{key}" style="left:{x}pt;top:{y}pt">'
                flow = block(key)
            if flow: h += flow + '</div>'
        h += '</div>'
        pages.append(h)
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
            f'<style>{font_css()}{CSS}</style></head><body>{"".join(pages)}</body></html>')

# ------------------------------------------------------------------ 바탕(원본 PDF) 가공
def find_chars(page, target, ymax=400):
    """target 문자열이 나타나는 글자들의 (rect, origin, size) 반환"""
    out = []
    for b in page.get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                cs = s['chars']; t = ''.join(c['c'] for c in cs)
                i = t.find(target)
                if i >= 0 and s['bbox'][1] < ymax:
                    sel = cs[i:i + len(target)]
                    r = pymupdf.Rect(sel[0]['bbox']) | pymupdf.Rect(sel[-1]['bbox'])
                    out.append((r, sel[0]['origin'], s['size']))
    return out

def make_background():
    src = pymupdf.open(TPL)
    doc = pymupdf.open()
    doc.insert_pdf(src, from_page=0, to_page=7)
    for pn, page in enumerate(doc):
        repl = []   # (origin, text, size)
        # 1) 결재란·출제 정보 행 제거 (실제 배부용 시험지와 동일하게)
        top = pymupdf.Rect(0, 28, 595, 92.5)
        # 2) 제목 '1학년 공통수학1과 중간고사 문제' → '2학년 미적분Ⅰ과 중간고사 문제'
        page.add_redact_annot(pymupdf.Rect(84, 102, 372, 129), fill=(1, 1, 1))
        # 3) 문항수
        for r, o, sz in find_chars(page, '17, 단답형: 3'):
            page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, '18, 서답형: 2', sz))
        if pn == 0:
            for r, o, sz in find_chars(page, '82'):
                page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, '80', sz))
            for r, o, sz in find_chars(page, '17'):
                if r.y0 > 300:
                    page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, '18', sz))
            body = [pymupdf.Rect(36, 336, 296, 780.5), pymupdf.Rect(299.5, 146.5, 559, 780.5)]
        else:
            body = [pymupdf.Rect(36, 146.5, 296, 780.5), pymupdf.Rect(299.5, 146.5, 559, 780.5)]
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        for r in body + [top]:
            page.add_redact_annot(r, fill=(1, 1, 1))
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
        # 머리글 다시 쓰기 (굴림)
        page.insert_font(fontname='GL', fontfile=GULIM)
        gl = pymupdf.Font(fontfile=GULIM)
        x, y = 83.28, 123.48
        for t, sz in [(' 2', 20.04), ('학년 ', 15.0), ('미적분Ⅰ', 21.0), ('과 ', 15.0), ('중간고사', 17.5), (' 문제', 15.0)]:
            page.insert_text((x, y), t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
            x += gl.text_length(t, fontsize=sz)
        for o, t, sz in repl:
            page.insert_text(o, t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
    return doc

def build(out_pdf):
    open(os.path.join(HERE, 'overlay_src.html'), 'w').write(overlay_html())
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'overlay_src.html', 'overlay.pdf'], cwd=HERE, check=True)
    ov = pymupdf.open(os.path.join(HERE, 'overlay.pdf'))
    bg = make_background()
    assert len(ov) == len(bg) == 8, (len(ov), len(bg))
    for i, page in enumerate(bg):
        page.show_pdf_page(page.rect, ov, i, overlay=True)
    bg.set_metadata({'title': '2학년 미적분Ⅰ 중간고사 문제', 'author': '양정고등학교'})
    bg.subset_fonts()
    bg.save(out_pdf, garbage=4, deflate=True)

if __name__ == '__main__':
    build(sys.argv[1])
