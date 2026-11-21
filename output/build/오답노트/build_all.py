# -*- coding: utf-8 -*-
"""부교재 전문항 시험지: 원본 양식 바탕 + 난도순 자동 배치(쪽수 가변)"""
import os, re, json, subprocess, sys
import pymupdf
from wbcore import *
import pool
I, MC, SA = pool.I, pool.MC, pool.SA
from wbcore import CSS as BASECSS

def nobreak(h):
    return re.sub(r'(\\\((?:(?!\\\)).)+?\\\))([,.])', r'<span class="nw">\1\2</span>', h)

def q_html(n, key):
    body, ch, _, _ = I[key]
    g = all(c.startswith('T:') for c in ch)
    chs = ''.join(f'<span><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    m = 9.3 if n < 10 else (15 if n < 100 else 20)
    F, C = (15.3, 9.3) if n < 10 else ((19.9, 15.6) if n < 100 else (24.6, 20.3))
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt"><span class="n" style="width:{F}pt">{n}.</span>{first}</div></div>'
            f'<div class="qr" style="--m:{m}pt;margin-left:{m}pt">{rest}<div class="ch{" g" if g else ""}">{chs}</div></div></div>')

def s_html(n, key):
    v = I[key]
    body, lab, subs = v[0], v[4], v[5]
    tot = sum(int(p[0]) for _, p in subs)
    body = body + f' <span class="pt">[{lab} · {tot}점]</span>'
    cut = min([i for i in (body.find('\\['), body.find('<div'), body.find('<fieldset')) if i >= 0] or [len(body)])
    first, rest = body[:cut], body[cut:]
    C = 12.0
    sh = ''.join(f'<div class="sub">({i+1}) {t} [{p}]</div><div style="height:{h}pt"></div>'
                 for i, ((t, p), h) in enumerate(zip(subs, [26, 26, 0])))
    return (f'<div class="q"><div class="qh" style="padding-left:{C}pt"><div class="qt" style="text-indent:-{C}pt">'
            f'<span class="slab">서답형 {n}.</span> {first}</div></div>'
            f'<div class="qr" style="--m:{C}pt;margin-left:{C}pt">{rest}</div></div>{sh}')

SEC1 = ('<div class="sec"><div class="h">&lt;서답형 문제&gt;</div>'
        f'<div class="d">서답형 문제(서답형 1~{len(SA)}번)는 반드시</div>'
        '<div class="d"><u>서답형 답안지의 해당란에 풀이과정을 상세히 작성</u>하시오.</div><hr></div>')

def make_blocks(MC, SA):
    sec = SEC1.replace('1~24', f'1~{len(SA)}')
    bl = [('Q%d' % (i + 1), q_html(i + 1, k)) for i, k in enumerate(MC)]
    return bl + [('SEC1', sec)] + [('S%d' % (i + 1), s_html(i + 1, k)) for i, k in enumerate(SA)]
BLOCKS = make_blocks(MC, SA)
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

BOT, BOT_LAST_R, GAP = 776.0, 600.0, 22.0
P0_MID = 555.8                                  # 1쪽 왼쪽 단 둘째 문항 위치(원본 양식)

def col_start(i): return 349.8 if i == 0 else TOP
def col_mid(i): return P0_MID if i == 0 else MID

def place(i, ks, H, bot):
    """단 i에 문항 ks를 놓을 위치. 불가능하면 None. 구역 머리글(SEC1)은 바로 아래에 다음 문항을 붙인다."""
    y, out, real = col_start(i), [], 0
    for k in ks:
        if k != 'SEC1' and real == 1:
            y = max(y, col_mid(i))
        out.append((k, round(y, 1)))
        y += H[k] + (0 if k == 'SEC1' else GAP)
        real += k != 'SEC1'
    return out if y - GAP <= bot and real <= 2 else None

def pack(H):
    cols = [[]]
    for k, _ in BLOCKS:
        if k == 'SEC1' and cols[-1]: cols.append([])
        if cols[-1] and place(len(cols) - 1, cols[-1] + [k], H, BOT) is None: cols.append([])
        cols[-1].append(k)
    # 마지막 쪽 오른쪽 단은 '수고하셨습니다' 자리를 비운다
    while len(cols) % 2 == 0 and place(len(cols) - 1, cols[-1], H, BOT_LAST_R) is None:
        moved = [cols[-1].pop()]
        cols.append(moved)
    if len(cols) % 2: cols.append([])
    return cols

def layout(cols, H):
    pages = []
    for i in range(0, len(cols), 2):
        pg = []
        for j in (i, i + 1):
            items = place(j, cols[j], H, 2000) if cols[j] else []
            pg.append((LX if j % 2 == 0 else RX, items))
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
            page.add_redact_annot(pymupdf.Rect(r.x0, r.y0, 556, r.y1), fill=(1, 1, 1)); repl.append((o, f'{len(MC)}, 서답형: {len(SA)} )', sz))
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
            for t, nt in [('선택형 18문제 = 80점', f'선택형 {len(MC)}문제'), ('서답형  2문제 = 20점', f'서답형 {len(SA)}문제')]:
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
    import shutil, glob
    # 1) 높이 측정: 문항마다 한 쪽에 하나씩 그려 본다
    global BLOCKS, HTML, MC, SA
    # 0) 난도가 같으면 길이(높이)가 짧은 문항부터: 한 번 재고 정렬
    H0 = render([[(LX, [(k, 0)])] for k, _ in BLOCKS], 'measure')
    hk = {}
    for (k, _), key in zip(BLOCKS, MC + ['SEC1'] + SA):
        hk[key] = H0[k]
    MC = sorted(MC, key=lambda k: (pool.DIFF[k], hk[k]))
    SA = sorted(SA, key=lambda k: (pool.DIFF[k], hk[k]))
    BLOCKS = make_blocks(MC, SA); HTML = dict(BLOCKS)
    json.dump({'MC': MC, 'SA': SA}, open(os.path.join(HERE, 'order.json'), 'w'))
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
    bg.set_metadata({'title': '2학년 미적분Ⅰ 오답노트', 'author': '양정고등학교'})
    bg.subset_fonts()
    bg.save(out_pdf, garbage=4, deflate=True)
    print('pages', N)

if __name__ == '__main__':
    build(sys.argv[1])
