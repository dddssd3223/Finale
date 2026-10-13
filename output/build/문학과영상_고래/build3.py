# -*- coding: utf-8 -*-
"""원본 시험지 PDF(양정고 양식)의 벡터 페이지를 그대로 바탕으로 쓰고,
결재란 제거 · 머리글 일부 수정 · 본문 교체로 새 시험지 PDF를 만든다."""
import os, re, json, subprocess, sys
import pymupdf
from content3 import Q, ANS, SA, CHW, CHM, P

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..')
FONTS = os.path.join(SCR, 'fonts')
TPL = os.path.join(SCR, 'src', 'form2.pdf')
GULIM = os.path.join(FONTS, 'gulim.ttf')
KATEX_CSS = os.path.join(SCR, 'node_modules', 'katex', 'dist', 'katex.min.css')

# ------------------------------------------------------------------ 본문 배치 (실제 시험지와 동일한 쪽 구성)
LX, RX, CW = 42.2, 301.5, 252.0          # 단 시작 x, 단 너비(pt)
TOP = 150.2                              # 단 첫 문항 y (원본 스캔 실측으로 맞춤)
PAGES = [
    ([('P1', 320), ('Q1', None)], [('Q2', TOP), ('Q3', 400)]),
    ([('Q4', TOP), ('Q5', 395)], [('Q6', TOP)]),
    ([('Q7', TOP), ('Q8', 490)], [('SEC1', TOP), ('S1', None), ('S2', None), ('END', 650)]),
]

CIRC = '①②③④⑤'

def font_css():
    f = lambda n: 'file://' + os.path.join(FONTS, n)
    return f"""
@font-face{{font-family:'MJ';src:url('{f('9Btx3DZF0dXLMZlywRbVRNhxy1Lr.ttf')}')}}
@font-face{{font-family:'MJ';src:url('{f('9Bty3DZF0dXLMZlywRbVRNhxy2pXV1A0.ttf')}');font-weight:700}}
@font-face{{font-family:'GL';src:url('{f('gulim_web.ttf')}')}}
@font-face{{font-family:'HB';src:url('{f('hbatang_web.ttf')}')}}
@font-face{{font-family:'HCRB';src:url('{f('hcrbatang.ttf')}')}}
@font-face{{font-family:'HCRD';src:url('{f('hcrdotum.woff')}')}}
@font-face{{font-family:'FS';src:url('file:///usr/share/fonts/truetype/freefont/FreeSans.ttf')}}
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
body{font-family:'HB','MJ','GL',serif;font-size:9pt;line-height:1.78;color:#000;word-break:keep-all}
.pg{width:595pt;height:842pt;position:relative;page-break-after:always;overflow:hidden}
.pg:last-child{page-break-after:auto}
.blk{position:absolute;width:var(--w)}
.katex{font-size:1.0em;margin:0 1.6pt}
.katex-display>.katex{margin:0}
.katex .text,.katex .text *{font-family:'HB'!important;font-style:normal}
.katex-display{margin:2pt 0 2.5pt;padding-left:24pt}
.katex-display>.katex{text-align:left}
.dw .katex-display{padding-left:0}
.q{text-align:justify;position:relative;padding-left:0;word-spacing:1.8pt}
.q .katex{word-spacing:0}
.q .katex .mspace{margin-right:0.17em!important}
.jl{display:block;text-align:left;text-align-last:left;white-space:nowrap}
.ptr{text-align:right}
.ul{text-decoration:underline;text-decoration-thickness:.6pt;text-underline-offset:8pt;text-decoration-skip-ink:none}
.qh{}.qh .n,.qt .n{display:inline-block;text-indent:0;vertical-align:baseline;font-family:'HB';font-weight:700;font-style:italic;font-size:10pt;letter-spacing:-.2pt}
.qt{text-align:justify}.qr{text-align:justify}
.pt{white-space:nowrap}
.ch .c{font-family:'GL'}
.ch{display:flex;flex-wrap:wrap;align-items:baseline;margin-top:1pt;margin-left:0;clear:both}
.ch>span{width:50pt;white-space:nowrap}
.ch.g>span{width:77pt}
.sa{margin-bottom:30pt}
.ph{font-family:'HB';margin:0 0 4pt;-webkit-text-stroke:.2pt #000}
.psg{border:.6pt solid #000;padding:5pt 7pt 6pt;font-size:8.3pt;line-height:1.43;text-align:justify}
.psg .sc{font-family:'GL';font-weight:700;margin:5pt 0 1pt;-webkit-text-stroke:.15pt #000}
.psg .sc:first-child{margin-top:0}
.psg .dl{padding-left:2.9em;text-indent:-2.9em}
.psg .dl .nm{display:inline-block;min-width:2.6em;text-indent:0;font-family:'GL';font-weight:700;margin-right:.3em}
.psg .sd{padding-left:1em;text-indent:0;margin:1pt 0}
.psg .nt{font-size:8.2pt;margin:0 0 4pt;padding:3pt 5pt;border:.5pt dashed #555}
.psg .mid{text-align:center;margin:3pt 0}
.psg .src{text-align:right;margin-top:4pt}
.psg .gl{font-size:7.6pt;line-height:1.45;margin-top:4pt;color:#111}
.br{position:relative;border-right:.7pt solid #000;margin-right:17pt;padding-right:3pt}
.br::before{content:'';position:absolute;right:-.7pt;top:0;width:5pt;border-top:.7pt solid #000}
.br::after{content:attr(data-l);position:absolute;right:-18pt;top:46%;font-size:8.4pt}
.bogi .bp{text-align:justify;padding:1pt 0}
.poem{padding:5pt 10pt 3pt 10pt;font-size:9.2pt;line-height:1.42}
.psg + .q{margin-top:12pt}
.poem .st{margin-bottom:4pt}
.gt{border-collapse:collapse;width:100%;margin:5pt 0;font-size:8.6pt}
.gt td{border:.6pt solid #000;padding:2pt 4pt;text-align:center}
.cond{border:.6pt solid #000;padding:2pt 6pt 2pt 6pt;margin:4pt 0 4pt 0;clear:both;text-align:left;line-height:1.5}
.nw{white-space:nowrap}
.ci{padding-left:22.4pt;text-indent:-22.4pt;margin:0}.ci .ck{display:inline-block;width:22.4pt;text-indent:0}
.bogi{border:.6pt solid #000;margin:4pt 0 4pt 0;padding:1pt 6pt 4pt;clear:both}
.bogi legend{margin:0 auto;padding:0 5pt;font-family:'GL';font-size:9pt}
.bi{display:flex;gap:3pt;margin:1pt 0;text-align:left}.bi .bk{flex:none}
.fig{text-align:center;margin:4pt 0}
.sub{margin:0;text-align:justify;line-height:13.4pt}
.s1 .sub{line-height:14.3pt}
.s2 .q{line-height:13.4pt}
.sec{padding-top:4.5pt}.sec .h{font-family:'GL';font-size:11.5pt;line-height:13pt;margin-bottom:2.1pt;-webkit-text-stroke:.15pt #000}
.sec .d{font-family:'GL';font-size:9pt;line-height:11.25pt;-webkit-text-stroke:.1pt #000}
.sec hr{border:0;border-top:1.4pt solid #000;margin:7.3pt 0 12.7pt}
.slab{font-family:'HB';font-weight:700;font-style:italic;font-size:11pt}
.end{text-align:center}
.sech{font-family:'HCRB';font-size:13pt;line-height:16pt;-webkit-text-stroke:.2pt #000;padding-top:2pt}
.secr{border:0;border-top:1.4pt solid #000;margin:8pt 0 5.7pt}
.sh{font-family:'HCRB';font-size:13pt;line-height:16pt;-webkit-text-stroke:.35pt #000;margin:0 0 3pt}
.endx{position:absolute;left:0;width:100%;text-align:center}
.endx .a{font-family:'HB','FS';font-size:20.5pt;line-height:26pt;white-space:nowrap}
.endx .b{font-family:'HB';font-size:14pt;line-height:19.7pt}
.end .a{font-size:24pt;letter-spacing:1pt}
.end .b{font-size:14pt;line-height:1.75;margin-top:6pt}
.tot{text-align:right}
"""

_BLK = re.compile(r'\\\]|</div>|<div[^>]*>|</fieldset>|<fieldset[^>]*>|<legend>.*?</legend>|<br>')

try:   # 줄별 너비(pt): 원본 스캔에서 그 줄의 오른쪽 끝을 재어 만든 값 (measure_jl.py)
    JLW = json.load(open(os.path.join(HERE, 'jlw.json')))
except FileNotFoundError:
    JLW = {}

def jl(h, key=''):
    """'⏎' = 원본 시험지의 줄바꿈 위치. 그 줄은 원본에서 잰 오른쪽 끝까지 양끝 맞춤."""
    parts = h.split('⏎')
    out = []
    for p in parts[:-1]:
        i = max([m.end() for m in _BLK.finditer(p)] or [0])
        k = f'{key}.{len(out)}'
        w = JLW.get(k)
        st = (f'width:{w:.1f}pt;text-align-last:justify;' if w else '') + JLSTYLE.get(k, '')
        st = f' style="{st}"' if st else ''
        out.append(p[:i] + f'<span class="jl" data-id="{k}"{st}>{p[i:].lstrip()}</span>')
    return ''.join(out) + parts[-1]

# 디스플레이 수식 왼쪽 여백(pt): 원본 스캔 실측 (measure_dm.py)
DPAD = {}

# 조건 상자 줄 간격 등(원본 실측)
CONDST = {}
# 줄별 추가 스타일(원본 실측: 키 큰 수식 뒤 줄 간격 등)
JLSTYLE = {}

def dpad(body, key):
    cnt = [0]
    def rep(m):
        k = f'{key}.{cnt[0]}'; cnt[0] += 1
        return f'<div class="dw" style="padding-left:{DPAD[k]}pt">{m.group(0)}</div>' if k in DPAD else m.group(0)
    return re.sub(r'\\\[[\s\S]+?\\\]', rep, body)

def q_html(n):
    pt, body, ch = Q[n]
    body = dpad(body, f'Q{n}')
    if n in CONDST: body = body.replace('<div class="cond">', f'<div class="cond" style="{CONDST[n]}">')
    body = body.replace('{PTR}', f'<div class="ptr">[{pt:.1f}점]</div>')
    body = body.replace('⏎{PT}', f'⏎<span class="pt">[{pt:.1f}점]</span>')
    body = body.replace('{PT}', f' <span class="pt">[{pt:.1f}점]</span>')
    g = all(c.startswith('T:') for c in ch)
    w = CHW.get(n)
    chs = ''.join(f'<span{(f" style=width:{w}pt" if w < 200 else f" style=width:{w}pt;white-space:normal;padding-left:11pt;text-indent:-11pt;text-align:left") if w else ""}><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    F = 15.3 if n < 10 else 19.9   # 원본 PDF 실측: 번호 폭
    # 실제 시험지: 둘째 줄·조건 상자·선택지 모두 번호와 같은 왼쪽 선에서 시작 (들여쓰기 없음), 줄바꿈 위치도 원본과 동일
    return (f'<div class="q"><div class="qt">{jl(f"<span class=n style=width:{F}pt>{n}.</span>" + body, f"Q{n}")}</div>'
            f'<div class="ch{" g" if g else ""}"{f" style=margin-top:{CHM[n]}pt" if n in CHM else ""}>{chs}</div></div>')

def s_html2(head, body, subs):
    # 실제 시험지: '서답형 n' 제목 줄 → 발문 → (1)(2)… 소문항(들여쓰기 없음), 배점은 소문항 끝 [n점, …]
    sh = ''.join(f'<div class="sub">{jl(f"({i+1}) {t} [{p}]", f"{head}-{i+1}")}</div>' for i, (t, p) in enumerate(subs))
    c = 'sa'
    return f'<div class="{c}"><div class="sh">{head}</div><div class="q"><div class="qt">{jl(body, head)}</div></div>{sh}</div>'

def s_html(lab, body, subs, total, gaps=(26, 26, 0)):
    # 원본 양식: '단답형 1.'(11pt 굵은 기울임)과 발문이 한 줄에 이어지고, 배점은 발문 끝에 [n점]
    sh = ''.join(f'<div class="sub">({i+1}) {t} [{p}]</div><div style="height:{h}pt"></div>'
                 for i, ((t, p), h) in enumerate(zip(subs, gaps)))
    body = body + f' <span class="pt">[{total}점]</span>'
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    C = 12.0    # 원본 PDF 실측: 둘째 줄부터의 시작 위치
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt">'
            f'<span class="slab">{lab}</span> {first}</div></div>'
            f'<div class="qr" style="--m:{C}pt;margin-left:{C}pt">{rest}</div></div>{sh}')

def SEC(kind, total, rng, how):
    return (f'<div class="sec"><div class="h">&lt;{kind} 문제 – {total}점&gt;</div>'
            f'<div class="d">{kind} 문제({rng})는 반드시</div>'
            f'<div class="d"><u>서답형 답안지의 해당란에 {how}</u>하시오.</div><hr></div>')
SEC1 = '<div class="sech">&lt;서답형 문제 – 20점&gt;</div><hr class="secr">'
SEC2 = ''
END = ('<div class="endx" style="top:0"><div class="a">수고하셨습니다 (ᐢ.꒳.ᐢ)ꕤ</div>'
       '<div class="b" style="margin-top:7.6pt">선택형 8문제 = 80점<br>서답형 2문제 = 20점</div></div>')

def block(key):
    if key.startswith('Q'): return q_html(int(key[1:]))
    if key in P: return P[key]
    if key[0] == 'S' and key[1:].isdigit(): return s_html2(f'서답형 {key[1:]}', SA[int(key[1:]) - 1], [])
    if key == 'SEC1': return SEC1
    if key == 'SEC2': return SEC2
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

# 실제 시험지 1쪽 위 영역 실측값 (스캔을 테두리 기준으로 맞춰 잰 pt 좌표)
P1_BOX = (46.0, 160.4, 291.4, 279.0)
P1_TITLE = ('<정기고사 준수사항>', 9.4, 165.2)            # 글자, 크기, 기준선
P1_LINES = [  # (기준선 y, 글머리표 여부, 글, 양끝 맞춤 여부)
    (180.4, True, '아래의 내용을 반드시 읽고 시험에 임하시기 바랍니다!', False),
    (191.4, True, '휴대폰 등 전자기기는 전원을 꺼 가방 속에 넣어야 합니다.', False),
    (202.0, True, '선택형 답안지에는 반드시 컴퓨터용 사인펜으로 표기해야', True),
    (212.8, False, '합니다. 답안을 수정할 경우 답안지를 교체하거나 수정테이', True),
    (225.6, False, '프를 사용하기 바랍니다.', False),
    (237.8, True, '시험지 아래쪽에 적힌 총 쪽수를 참조하여 받은 시험지의', True),
    (248.8, False, '매수를 확인하기 바랍니다.', False),
    (260.6, True, '정해진 시험 종료 시각을 확인하여 답안지를 미리 작성하기', True),
    (271.6, False, '바랍니다.', False),
]
P1_TX, P1_TX2, P1_TR, P1_FS = 66.0, 61.0, 287.6, 8.65   # 글머리 뒤 시작, 이어지는 줄 시작, 오른쪽 끝, 글자 크기
P1_BUL = (51.6, 59.6)                                   # 글머리표(■) 좌우
P1_NOTE = [(293.0, '선택형 문제(1~8번)의 정답은 반드시'), (304.9, 'OMR카드에 컴퓨터용 사인펜으로 명확히 표기하시오.')]
P1_NX, P1_NFS, P1_UL = 44.0, 9.25, (44.0, 240.0, 306.3)
P1_RULE = (43.0, 295.0, 313.8, 1.44)

def redraw_p1_head(page, gl):
    put = lambda o, t, sz: page.insert_text(o, t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
    x0, y0, x1, y1 = P1_BOX
    page.draw_rect(pymupdf.Rect(x0, y0, x1, y1), color=(0, 0, 0), width=0.36)
    t, sz, by = P1_TITLE
    tw = gl.text_length(t, fontsize=sz); cx = (x0 + x1) / 2
    page.draw_rect(pymupdf.Rect(cx - tw / 2 - 3, y0 - 4, cx + tw / 2 + 3, y0 + 4), color=None, fill=(1, 1, 1), width=0)
    put((cx - tw / 2, by), t, sz)
    for by, bul, t, just in P1_LINES:
        if bul:
            page.draw_rect(pymupdf.Rect(P1_BUL[0], by - 7.0, P1_BUL[1], by + 0.4), color=None, fill=(.25, .25, .25), width=0)
        x = P1_TX if bul else P1_TX2
        words = t.split(' ')
        if just and len(words) > 1:
            ws = [gl.text_length(w, fontsize=P1_FS) for w in words]
            gap = (P1_TR - x - sum(ws)) / (len(words) - 1)
            for w, wl in zip(words, ws):
                put((x, by), w, P1_FS); x += wl + gap
        else:
            put((x, by), t, P1_FS)
    for by, t in P1_NOTE:
        put((P1_NX, by), t, P1_NFS)
    ux0, ux1, uy = P1_UL
    page.draw_line((ux0, uy), (ux1, uy), color=(0, 0, 0), width=0.36)
    rx0, rx1, ry, rw = P1_RULE
    page.draw_line((rx0, ry), (rx1, ry), color=(0, 0, 0), width=rw)

def make_background():
    src = pymupdf.open(TPL)
    doc = pymupdf.open()
    doc.insert_pdf(src, from_page=0, to_page=len(PAGES) - 1)
    for pn, page in enumerate(doc):
        repl = []   # (origin, text, size)
        # 1) 결재란·출제 정보 행 제거 (실제 배부용 시험지와 동일하게)
        top = pymupdf.Rect(0, 28, 595, 92.5)
        # 2) 제목 '1학년 공통수학1과 중간고사 문제' → '2학년 미적분Ⅰ과 중간고사 문제'
        page.add_redact_annot(pymupdf.Rect(84, 100, 428, 129), fill=(1, 1, 1))
        page.add_redact_annot(pymupdf.Rect(343.6, 801.6, 348.6, 809.2), fill=(1, 1, 1)); repl.append(((343.8, 808.2), str(len(PAGES)), 8.04))
        # 시행일
        for r, o, sz in find_chars(page, '7월 11일(토) - 1교시'):
            page.add_redact_annot(pymupdf.Rect(r.x0, r.y0, 562, r.y1), fill=(1, 1, 1)); repl.append((o, '10월   일(   )', sz))
        # 3) 정보 줄(과정·과목코드·이수단위·문항수) 전체 다시 씀
        page.add_redact_annot(pymupdf.Rect(40, 135.0, 558, 143.3), fill=(1, 1, 1))
        if pn == 0:
            # 1쪽 위: 준수사항 상자·안내문·굵은 선을 모두 지우고 실제 시험지 배치대로 다시 그림 (redraw_p1_head)
            body = [pymupdf.Rect(36, 146.5, 296, 780.5), pymupdf.Rect(299.5, 146.5, 559, 780.5)]
        elif pn == 7:
            body = [pymupdf.Rect(36, 146.5, 296, 780.5), pymupdf.Rect(299.5, 146.5, 559, 780.5)]
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
        # 제목·정보 줄: 실제 시험지 스캔에서 잰 글자 위치·크기
        for x, t, sz in TITLE:
            page.insert_text((x, 123.48), t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
        for x, t in INFO:
            page.insert_text((x, INFO_Y), t, fontname='GL', fontsize=INFO_FS, render_mode=2, border_width=0.02)
        for o, t, sz in repl:
            page.insert_text(o, t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
        if pn == 0:
            redraw_p1_head(page, gl)
    return doc

TITLE = [(92.3, '2', 20.04), (106.46, '학년', 15.0), (143.8, '문학과 영상', 21.0), (266.96, '과', 15.0),
         (289.3, '중간고사', 19.0), (367.45, ' 문제', 15.0)]
INFO_Y, INFO_FS = 142.3, 9.4
INFO = [(70.2, '과 정 : ( 2022 개정 교육과정 )'), (223.4, '과목코드 : (    )'), (319.4, '이수단위 : (    )'),
        (409.8, '문항수 ( 선택형: 8, 서답형 2)')]

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

def build(out_pdf):
    open(os.path.join(HERE, 'overlay_src.html'), 'w').write(overlay_html())
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'overlay_src.html', 'overlay.pdf'], cwd=HERE, check=True)
    ov = pymupdf.open(os.path.join(HERE, 'overlay.pdf'))
    thin_boxes(ov)
    bg = make_background()
    assert len(ov) == len(bg) == len(PAGES), (len(ov), len(bg))
    for i, page in enumerate(bg):
        page.show_pdf_page(page.rect, ov, i, overlay=True)
    bg.set_metadata({'title': '2학년 문학과 영상 중간고사 문제', 'author': '양정고등학교'})
    bg.subset_fonts()
    bg.save(out_pdf, garbage=4, deflate=True)

if __name__ == '__main__':
    build(sys.argv[1])
