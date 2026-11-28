# -*- coding: utf-8 -*-
"""하프 모의고사(오답 재출제) 정답 및 해설: python3 haeseol_half.py <회차 폴더> <out.pdf>
haeseol2.py의 양식(표지·해설 본문·개념 상자·STEP·정답 칩)을 그대로 쓰고, 1쪽만 하프용(정답표 + 원래 문항 대응표)으로 바꾼다."""
import sys, os, re, json, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import haeseol2 as H

def build(rdir, out):
    rdir = os.path.abspath(rdir); name = os.path.basename(rdir); c = H.load(rdir)
    MAP = json.load(open(os.path.join(rdir, 'map.json'))) if os.path.exists(os.path.join(rdir, 'map.json')) else {}
    D = {}
    for f in sorted(glob.glob(os.path.join(rdir, 'haeseol', 'items_*.json'))):
        for d in json.load(open(f)): D[str(d['n'])] = H.tidy(d)
    H.stylecheck(D, {})
    css = H.CSS.replace('@N@', H.NAN).replace('@F@', H.FONTS)
    P = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{H.KATEX_CSS}"><style>{css}</style></head><body>']
    nums = sorted(c.ITEMS)
    rows = ''.join(f'<tr><td class="n">{H.num(n)}</td><td class="v">{H.CIRC[c.ANS[n] - 1]}</td><td style="text-align:left">원래 {MAP.get(str(n), "")}</td></tr>' for n in nums)
    sa = ''
    for s, it in c.SITEMS.items():
        a = it['ans'] if isinstance(it['ans'], list) else [it['ans']]
        sa += f'<div><span class="h">서답형</span>' + ' &nbsp; '.join(H.fx(x) for x in a) + f' <span style="color:#7a8699">· 원래 {MAP.get(s, "")}</span></div>'
    P.append(f'<div class="p1"><div class="l"><div class="ttl"><span>미적분Ⅰ 하프 모의고사 {name}</span><b>정답 및 해설</b></div>'
             f'<table class="ans">{rows}</table><div class="sa">{sa}</div></div>'
             f'<div class="r"><h3>이번 회차는</h3><div class="fine" style="font-size:9.5pt;line-height:1.9">8–10회에서 틀린 문항을 숫자만 바꿔 다시 낸 오답 재출제 회차다. '
             f'설정과 묻는 값, 풀이 흐름은 원래 문항과 같고 수치만 다르다. 해설마다 원래 문항에서 걸렸던 함정이 이번 수치에서 어떻게 나타나는지 마지막에 짚었다. '
             f'틀린 문항은 원래 회차 해설과 나란히 놓고 같은 판단을 두 번 확인하자.</div></div></div>')
    P.append('<div class="cols">')
    for n in nums:
        d = D.get(str(n))
        if d: P.append(H.item_html(n, d, c))
    for s, it in c.SITEMS.items():
        d = D.get(s)
        if d: P.append(H.item_html('서답형', d, c, it))
    P.append('</div></body></html>')
    hd = os.path.join(rdir, 'haeseol'); src = os.path.join(hd, 'book_src.html')
    open(src, 'w').write(H.fx(H.nodot(''.join(P))))
    body_pdf, cover_pdf = os.path.join(hd, 'book_body.pdf'), os.path.join(hd, 'cover.pdf')
    subprocess.run(['node', os.path.join(HERE, 'haeseol2.js'), src, body_pdf, f'하프 모의고사 {name}'], check=True)
    cv = H.cover(name, css).replace('기말 모의고사', '하프 모의고사').replace('>105<', '>10.5<')
    csrc = os.path.join(hd, 'cover_src.html'); open(csrc, 'w').write(cv)
    subprocess.run(['node', os.path.join(HERE, 'haeseol2.js'), csrc, cover_pdf, '-', 'plain'], check=True)
    import pymupdf
    doc = pymupdf.open(cover_pdf); doc.insert_pdf(pymupdf.open(body_pdf)); doc.save(out, garbage=4, deflate=True)
    os.remove(body_pdf); os.remove(cover_pdf)
    print(out, len(doc))

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
