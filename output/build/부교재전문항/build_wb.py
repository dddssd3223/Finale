# -*- coding: utf-8 -*-
"""부교재 전문항 시험지: 원본 양식 바탕 + 난도순 자동 배치(쪽수 가변)"""
import os, re, json, subprocess, sys
import pymupdf
from wbcore import *
from wbcore import CSS as BASECSS

def nobreak(h):
    return re.sub(r'(\\\((?:(?!\\\)).)+?\\\))([,.])', r'<span class="nw">\1\2</span>', h)

def q_html(n, key):
    body, ch, _, _ = I[key]
    g = all(c.startswith('T:') for c in ch)
    chs = ''.join(f'<span><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    m = 9.3 if n < 10 else 15
    F, C = (15.3, 9.3) if n < 10 else (19.9, 15.6)
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt"><span class="n" style="width:{F}pt">{n}.</span>{first}</div></div>'
            f'<div class="qr" style="--m:{m}pt;margin-left:{m}pt">{rest}<div class="ch{" g" if g else ""}">{chs}</div></div></div>')

def s_html(n, key):
    body = I[key][0]
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    C = 12.0
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt">'
            f'<span class="slab">단답형 {n}.</span> {first}</div></div>'
            f'<div class="qr" style="--m:{C}pt;margin-left:{C}pt">{rest}</div></div>')

SEC1 = ('<div class="sec"><div class="h">&lt;단답형 문제&gt;</div>'
        f'<div class="d">단답형 문제(단답형 1~{len(SA)}번)는 반드시</div>'
        '<div class="d"><u>서답형 답안지의 해당란에 정답만 작성</u>하시오.</div><hr></div>')

BLOCKS = [('Q%d' % (i + 1), q_html(i + 1, k)) for i, k in enumerate(MC)]
BLOCKS += [('SEC1', SEC1)] + [('S%d' % (i + 1), s_html(i + 1, k)) for i, k in enumerate(SA)]
HTML = dict(BLOCKS)

def doc_html(pages):
    out = []
    for cols in pages:
        h = '<div class="pg">'
        for x, items in cols:
            for key, y in items:
                h += f'<div class="blk" data-k="{key}" style="left:{x}pt;top:{y}pt;--w:{252 if x == LX else 251.5}pt">{HTML[key]}</div>'
        out.append(h + '</div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
            f'<style>{font_css()}{BASECSS}</style></head><body>{nobreak("".join(out))}</body></html>')

def render(pages, name):
    open(os.path.join(HERE, name + '_src.html'), 'w').write(doc_html(pages))
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), name + '_src.html', name + '.pdf'], cwd=HERE, check=True)
    return {b['k']: b['bottom'] - b['top'] for b in json.load(open(os.path.join(HERE, 'blocks.json')))}

BOT, BOT_LAST_R, GAP = 776.0, 600.0, 34.0

def pack(H):
    cols = []                                    # [(page, side, start, [keys])]
    def new_col():
        i = len(cols); p, s = divmod(i, 2)
        cols.append((p, s, 349.8 if i == 0 else TOP, []))
    def fits(c, k):
        used = sum(H[x] + GAP for x in c[3])
        return c[2] + used + H[k] <= BOT
    new_col()
    for k, _ in BLOCKS:
        if k == 'SEC1' and cols[-1][3]: new_col()
        elif cols[-1][3] and not fits(cols[-1], k): new_col()
        if k.startswith('S') and k != 'SEC1' and cols[-1][3] == ['SEC1']: pass
        cols[-1][3].append(k)
    # 마지막 쪽 오른쪽 단은 '수고하셨습니다' 자리를 비운다
    def last_ok():
        p, s, st, ks = cols[-1]
        return s == 0 or st + sum(H[x] + GAP for x in ks) - GAP <= BOT_LAST_R
    while not last_ok():
        moved = []
        while cols[-1][3] and cols[-1][2] + sum(H[x] + GAP for x in cols[-1][3]) - GAP > BOT_LAST_R:
            moved.insert(0, cols[-1][3].pop())
        new_col(); cols[-1][3].extend(moved)
    if len(cols) % 2: new_col()
    return cols

def layout(cols, H):
    pages = []
    for i in range(0, len(cols), 2):
        pg = []
        for p, s, st, ks in cols[i:i + 2]:
            bot = BOT_LAST_R if (i + 2 >= len(cols) and s == 1) else BOT
            hs = [H[k] for k in ks]
            # 남는 공간을 각 문항 아래 풀이 공간으로 고르게 나눈다(구역 머리글 뒤는 좁게)
            n_real = sum(1 for k in ks if k != 'SEC1')
            free = bot - st - sum(hs)
            g = min(max(free / max(n_real, 1), 0), 300)
            y, items = st, []
            for k, h in zip(ks, hs):
                items.append((k, round(y, 1)))
                y += h + (0 if k == 'SEC1' else g)
            pg.append((LX if s == 0 else RX, items))
        pages.append(pg)
    return pages

def make_bg(N):
    base = make_background()                       # 8쪽 원본 양식(머리글 수정 완료)
    doc = pymupdf.open()
    for i in range(N):
        doc.insert_pdf(base, from_page=0 if i == 0 else (7 if i == N - 1 else 1), to_page=0 if i == 0 else (7 if i == N - 1 else 1))
    gl = pymupdf.Font(fontfile=GULIM)
    for i, page in enumerate(doc):
        page.insert_font(fontname='GL', fontfile=GULIM)
        repl = []
        for r, o, sz in find_chars(page, '18, 서답형: 2'):
            page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, f'{len(MC)}, 단답형: {len(SA)}', sz))
        for r, o, sz in find_chars(page, '<8-', ymax=900):
            rr = pymupdf.Rect(r.x0, r.y0, r.x0 + 24, r.y1)
            page.add_redact_annot(rr, fill=(1, 1, 1)); repl.append((o, f'<{N}-{i + 1}>', sz))
        if i == 0:
            for r, o, sz in find_chars(page, '<선택형 문제'):
                page.add_redact_annot(pymupdf.Rect(r.x0, r.y0, 290, r.y1), fill=(1, 1, 1)); repl.append((o, '<선택형 문제>', sz))
            for r, o, sz in find_chars(page, '18'):
                if r.y0 > 300:
                    page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, f'{len(MC)}', sz))
        if i == N - 1:
            for t, nt in [('선택형 18문제 = 80점', f'선택형 {len(MC)}문제'), ('서답형  2문제 = 20점', f'단답형 {len(SA)}문제')]:
                for r, o, sz in find_chars(page, t, ymax=900):
                    page.add_redact_annot(r, fill=(1, 1, 1)); repl.append((o, nt, sz))
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        for o, t, sz in repl:
            if t.startswith('<') and t[1].isdigit():      # 쪽 번호는 원래 자간(약 4.8pt)을 살려 글자별로
                x = o[0]
                for ch in t:
                    page.insert_text((x, o[1]), ch, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02); x += 4.8
            else:
                page.insert_text(o, t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
    return doc

def build(out_pdf):
    # 1) 높이 측정: 문항마다 한 쪽에 하나씩 그려 본다
    H = render([[(LX, [(k, 0)])] for k, _ in BLOCKS], 'measure')
    cols = pack(H)
    pages = layout(cols, H)
    json.dump(pages, open(os.path.join(HERE, 'pages.json'), 'w'), ensure_ascii=False)
    render(pages, 'overlay')
    ov = pymupdf.open(os.path.join(HERE, 'overlay.pdf'))
    thin_boxes(ov)
    N = len(pages)
    bg = make_bg(N)
    assert len(ov) == N, (len(ov), N)
    for i, page in enumerate(bg):
        page.show_pdf_page(page.rect, ov, i, overlay=True)
    bg.set_metadata({'title': '2학년 미적분Ⅰ 부교재 전문항 시험지', 'author': '양정고등학교'})
    bg.subset_fonts()
    bg.save(out_pdf, garbage=4, deflate=True)
    print('pages', N)

if __name__ == '__main__':
    build(sys.argv[1])
