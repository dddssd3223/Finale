# -*- coding: utf-8 -*-
"""원본 시험지 PDF(양정고 양식)의 벡터 페이지를 그대로 바탕으로 쓰고,
결재란 제거 · 머리글 일부 수정 · 본문 교체로 새 시험지 PDF를 만든다."""
import os, re, json, subprocess, sys
import pymupdf
from items import I, MC, SA

HERE = os.path.dirname(os.path.abspath(__file__))
def _kit_root(p):
    p = os.path.abspath(p)
    while not (os.path.isdir(os.path.join(p, 'fonts')) and os.path.isdir(os.path.join(p, 'src'))):
        q = os.path.dirname(p)
        if q == p: raise SystemExit('template 루트(fonts/, src/가 있는 폴더)를 찾지 못했습니다')
        p = q
    return p
SCR = _kit_root(HERE)
FONTS = os.path.join(SCR, 'fonts')
TPL = os.path.join(SCR, 'src', 'form2.pdf')
GULIM = os.path.join(FONTS, 'gulim.ttf')
KATEX_CSS = os.path.join(SCR, 'node_modules', 'katex', 'dist', 'katex.min.css')

# ------------------------------------------------------------------ 본문 배치 (실제 시험지와 동일한 쪽 구성)
LX, RX, CW = 42.2, 301.5, 252.0          # 단 시작 x, 단 너비(pt)
TOP, MID = 152.2, 460.7                  # 단 첫 문항 y, 둘째 문항 y
PAGES = [
    ([('Q1', 349.8), ('Q2', 555.8)], [('Q3', TOP), ('Q4', MID)]),
    ([('Q5', TOP), ('Q6', MID)], [('Q7', TOP)]),
    ([('Q8', TOP)], [('Q9', TOP), ('Q10', MID)]),
    ([('Q11', TOP)], [('Q12', TOP)]),
    ([('Q13', TOP)], [('Q14', TOP)]),
    ([('Q15', TOP)], [('Q16', TOP)]),
    ([('Q17', TOP)], [('Q18', TOP)]),
    ([('SEC1', TOP), ('S1', None)], [('SEC2', TOP), ('S2', None)]),
]

CIRC = '①②③④⑤'

def font_css():
    f = lambda n: 'file://' + os.path.join(FONTS, n)
    return f"""
@font-face{{font-family:'MJ';src:url('{f('9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf')}')}}
@font-face{{font-family:'MJ';src:url('{f('9Bty3DZF0dXLMZlywRbVRNhxy2pXV1A0.ttf')}');font-weight:700}}
@font-face{{font-family:'GL';src:url('{f('gulim_web.ttf')}')}}
@font-face{{font-family:'HB';src:url('{f('hbatang_web.ttf')}')}}
@font-face{{font-family:'HYEQ';src:url('{f('hyhwpeq_web.ttf')}')}}
@font-face{{font-family:'TN';src:url('{f('buE4poGnedXvwgX8.ttf')}')}}
@font-face{{font-family:'TN';src:url('{f('buE2poGnedXvwjX-fmE.ttf')}');font-style:italic}}
@font-face{{font-family:'TN';src:url('{f('buE1poGnedXvwj1AW0Fp.ttf')}');font-weight:700}}
@font-face{{font-family:'TN';src:url('{f('buEzpoGnedXvwjX-Rt1s0Co.ttf')}');font-weight:700;font-style:italic}}
"""

CSS = r"""
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:transparent}
body{font-family:'HB','MJ','GL',serif;font-size:9pt;line-height:1.61;color:#000;word-break:keep-all}
.pg{width:595pt;height:842pt;position:relative;page-break-after:always;overflow:hidden}
.pg:last-child{page-break-after:auto}
.blk{position:absolute;width:var(--w)}
.katex{font-size:1.0em;margin:0 1.6pt}
.katex-display>.katex{margin:0}
.katex .text,.katex .text *{font-family:'HB'!important;font-style:normal}
.katex-display{margin:4.5pt 0 7pt;padding-left:calc(33pt - var(--m,0pt))}
.katex-display>.katex{text-align:left}
.q{text-align:justify;position:relative;padding-left:0}
.qh{}.qh .n{display:inline-block;text-indent:0;vertical-align:baseline;font-family:'HB';font-weight:700;font-style:italic;font-size:10pt;letter-spacing:-.2pt}
.qt{text-align:justify}.qr{text-align:justify}
.pt{white-space:nowrap}
.ch .c{font-family:'GL'}
.ch{display:flex;flex-wrap:wrap;margin-top:9pt;margin-left:calc(12pt - var(--m,0pt));clear:both}
.ch>span{width:46.4pt;white-space:nowrap}
.ch.g>span{width:77pt}
.cond{border:.6pt solid #000;padding:2.2pt 6pt 1.8pt 7pt;margin:8.5pt 5pt 10.5pt calc(13pt - var(--m,0pt));clear:both;text-align:left}
.nw{white-space:nowrap}
.ci{padding-left:22.4pt;text-indent:-22.4pt;margin:0}.ci .ck{display:inline-block;width:22.4pt;text-indent:0}
.bogi{border:.6pt solid #000;margin:8.5pt 5pt 4pt calc(12pt - var(--m,0pt));padding:1pt 6pt 4pt;clear:both}
.bogi legend{margin:0 auto;padding:0 5pt;font-family:'GL';font-size:9pt}
.bi{display:flex;gap:3pt;margin:1pt 0}.bi .bk{flex:none}
.fig{text-align:center;margin:4pt 0}
.sub{margin:9pt 0 0;padding-left:14pt;text-indent:-14pt;text-align:justify}
.sec{padding-top:4.5pt}.sec .h{font-family:'GL';font-size:11.5pt;line-height:13pt;margin-bottom:2.1pt;-webkit-text-stroke:.15pt #000}
.sec .d{font-family:'GL';font-size:9pt;line-height:11.25pt;-webkit-text-stroke:.1pt #000}
.sec hr{border:0;border-top:1.4pt solid #000;margin:7.3pt 0 12.7pt}
.slab{font-family:'HB';font-weight:700;font-style:italic;font-size:11pt}
.end{text-align:center;font-family:'GL'}
.end .a{font-size:24pt;letter-spacing:1pt}
.end .b{font-size:14pt;line-height:1.75;margin-top:6pt}
.tot{text-align:right}
"""


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
        elif pn == 7:
            body = [pymupdf.Rect(36, 146.5, 296, 780.5), pymupdf.Rect(299.5, 146.5, 559, 610),
                    pymupdf.Rect(299.5, 670, 559, 780.5)]
            repl += [((355.44, 694.80), '선택형 18문제 = 80점', 13.8), ((355.92, 715.56), '서답형  2문제 = 20점', 13.8)]
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

BOX_LW = 0.36  # 양식 박스 선 두께(pt); Chromium은 1px(0.75pt) 미만 테두리를 1px로 올리므로 PDF에서 직접 조정

def thin_boxes(doc):
    """조건/보기 박스(re S 사각형 테두리)의 선 두께를 BOX_LW로 낮춘다."""
    pat = re.compile(rb'(?<=\n)([-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+) re\nS\n)')
    for page in doc:
        for xref in page.get_contents():
            c = doc.xref_stream(xref)
            def rep(m):
                if float(m.group(2)) < 100: return m.group(0)
                return b'q\n%.4f w\n' % (BOX_LW / 0.75) + m.group(1) + b'Q\n'
            n = pat.sub(rep, c)
            if n != c: doc.update_stream(xref, n)

