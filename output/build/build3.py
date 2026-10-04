# -*- coding: utf-8 -*-
"""원본 시험지 PDF(양정고 양식)의 벡터 페이지를 그대로 바탕으로 쓰고,
결재란 제거 · 머리글 일부 수정 · 본문 교체로 새 시험지 PDF를 만든다."""
import os, re, json, subprocess, sys
import pymupdf
from content3 import Q, ANS, S1, S1S, S2, S2S

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..')
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
    ([('SEC', TOP), ('S1', None)], [('S2', TOP)]),
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
.sec .h{font-family:'GL';font-size:11.5pt;margin-bottom:4pt;-webkit-text-stroke:.15pt #000}
.sec .d{font-family:'GL';font-size:9pt;line-height:1.55;-webkit-text-stroke:.1pt #000}
.sec hr{border:0;border-top:1.4pt solid #000;margin:9pt 0 12pt}
.slab{font-family:'HB';font-weight:700;font-style:italic;font-size:11pt}
.end{text-align:center;font-family:'GL'}
.end .a{font-size:24pt;letter-spacing:1pt}
.end .b{font-size:14pt;line-height:1.75;margin-top:6pt}
.tot{text-align:right}
"""

def q_html(n):
    pt, body, ch = Q[n]
    body = body.replace('{PT}', f' <span class="pt">[{pt:.1f}점]</span>')
    g = all(c.startswith('T:') for c in ch)
    chs = ''.join(f'<span><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    m = 9.3 if n < 10 else 15      # 둘째 문단부터의 들여쓰기(원본 PDF 실측)
    F, C = (15.3, 9.3) if n < 10 else (19.9, 15.6)   # 원본 PDF 실측: 첫 줄 본문 시작 / 둘째 줄 시작      # 이후 문단 들여쓰기 = 번호 폭
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt"><span class="n" style="width:{F}pt">{n}.</span>{first}</div></div>'
            f'<div class="qr" style="--m:{m}pt;margin-left:{m}pt">{rest}<div class="ch{" g" if g else ""}">{chs}</div></div></div>')

def s_html(lab, body, subs, total):
    # 원본 양식: '단답형 1.'(11pt 굵은 기울임)과 발문이 한 줄에 이어지고, 배점은 발문 끝에 [n점]
    sh = ''.join(f'<div class="sub">({i+1}) {t} [{p}]</div><div style="height:{h}pt"></div>'
                 for i, ((t, p), h) in enumerate(zip(subs, [26, 26, 0])))
    body = body + f' <span class="pt">[{total}점]</span>'
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    C = 12.0    # 원본 PDF 실측: 둘째 줄부터의 시작 위치
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt">'
            f'<span class="slab">{lab}</span> {first}</div></div>'
            f'<div class="qr" style="--m:{C}pt;margin-left:{C}pt">{rest}</div></div>{sh}')

SEC = ('<div class="sec"><div class="h">&lt;서답형 문제 – 20점&gt;</div>'
       '<div class="d">서답형 문제(서답형 1번~서답형 2번)는 반드시</div>'
       '<div class="d"><u>서답형 답안지의 해당란에 풀이과정을 상세히 작성</u>하시오.</div><hr></div>')
END = ('<div class="end"><div class="a">♥수고하셨습니다♥</div>'
       '<div class="b">선택형 18문제 = 80점<br>서답형&nbsp;&nbsp;2문제 = 20점</div></div>')

def block(key):
    if key.startswith('Q'): return q_html(int(key[1:]))
    if key == 'S1': return s_html('서답형 1.', S1, S1S, 10)
    if key == 'S2': return s_html('서답형 2.', S2, S2S, 10)
    if key == 'SEC': return SEC
    if key == 'END': return END

def nobreak(h):
    # 수식 바로 뒤의 쉼표·마침표가 다음 줄 맨 앞으로 가지 않도록 묶음
    return re.sub(r'(\\\((?:(?!\\\)).)+?\\\))([,.])', r'<span class="nw">\1\2</span>', h)

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
                h += f'<div class="blk" data-k="{key}" style="left:{x}pt;top:{y}pt;--w:{252 if x == LX else 251.5}pt">'
                flow = block(key)
            if flow: h += flow + '</div>'
        h += '</div>'
        pages.append(h)
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
            f'<style>{font_css()}{CSS}</style></head><body>{nobreak("".join(pages))}</body></html>')

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
