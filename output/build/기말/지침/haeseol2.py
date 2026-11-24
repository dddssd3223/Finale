# -*- coding: utf-8 -*-
"""시판 모의고사 해설지 꼴의 학생용 해설(사용자 2026-11-23 샘플: 이해원 모의고사 시즌3 정답 및 해설, 앞의 설명·목차는 뺌).
사용: python3 haeseol2.py <회차 폴더> <출력 PDF>
- 1쪽: 정답표 · 2026-2 중간 대비 번호대 난도 비교(측정) · 예상 등급컷
- 2쪽: 검수 코멘트 · 출제자의 총평 (<회차>/haeseol/front.json)
- 3쪽부터 2단: 번호 · 해법 꼬리표 · 교과서/실전 개념 상자 · 생각의 시작 · STEP 흐름 정리 · 본문 · 논리적 정당화 · CHECK 각주 · 원문 연계(변형 포인트) · 정답
  문항별 글은 <회차>/haeseol/items_*.json (haeseol/TASK.md 형식)."""
import os, re, sys, json, glob, html, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말'); import items_final as F
NAN = '/usr/share/fonts/truetype/nanum/'
FONTS = os.path.join(BASE, 'fonts')
KATEX_CSS = os.path.join(BASE, 'node_modules', 'katex', 'dist', 'katex.min.css')
CIRC = '①②③④⑤'
PROFILE = os.path.join(BASE, '공동출제', '풀이', '기준프로필', 'profile.json')
PTS = {n: (4.0 if n <= 4 else 4.2 if n <= 8 else 4.4 if n <= 10 else 4.5 if n <= 12 else 4.7 if n <= 15 else 4.9 if n == 16 else 5.2) for n in range(1, 19)}

def load(rdir):
    spec = importlib.util.spec_from_file_location('c3', os.path.join(rdir, 'content3.py'))
    m = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(rdir); sys.path.insert(0, rdir)
    try: spec.loader.exec_module(m)
    finally: os.chdir(cwd); sys.path.pop(0)
    return m

def fx(s):
    s = str(s or '')
    return re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>').replace("\\'", "'"), s)

def feels(rdir, c):
    """측정 결과 → 시험지 번호별 체감(마지막 측정이 이김). A·B·C는 출제 때 번호, 뒤 측정은 meta의 번호 기준."""
    name = os.path.basename(rdir); inv = {}
    ren = getattr(c, 'RENUM', {}) or {}
    out = {}
    for f in sorted(glob.glob(os.path.join(BASE, '공동출제', '풀이', f'측정_{name}*', 'result.json')), key=os.path.getmtime):   # 나중에 잰 것이 이김
        r = json.load(open(f)); meta = json.load(open(os.path.join(os.path.dirname(f), 'meta.json')))
        post = bool(meta.get('renum')) or os.path.basename(os.path.dirname(f)) > f'측정_{name}C'   # C까지는 출제 번호, 그 뒤는 시험지 번호
        for row in r['rows']:
            lab = row[1].split('-', 1)[1]
            if lab.startswith('S'): out[lab] = row[3]; continue
            n = int(lab); n = n if post else ren.get(n, n)
            out[str(n)] = row[3]
    return out

def num(n):
    s = f'{int(n):02d}' if str(n).isdigit() else str(n)
    return f'<span class="z">{s[0]}</span>{s[1:]}' if s[0] == '0' else s

CSS = r"""
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareR.ttf')}
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareB.ttf');font-weight:700}
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareEB.ttf');font-weight:800}
@font-face{font-family:'NBG';src:url('file://@N@NanumBarunGothic.ttf')}
@font-face{font-family:'NBG';src:url('file://@N@NanumBarunGothicBold.ttf');font-weight:700}
@font-face{font-family:'BD';src:url('file://@F@/busan_L.ttf');font-weight:300}
@font-face{font-family:'BD';src:url('file://@F@/busan_M.ttf');font-weight:500}
@font-face{font-family:'BD';src:url('file://@F@/busan_B.ttf');font-weight:700}
@font-face{font-family:'HYEQ';src:url('file://@F@/hyhwpeq_web.ttf')}
@font-face{font-family:'SJ';src:url('file://@F@/shinjung.ttf')}
@font-face{font-family:'HB';src:url('file://@F@/hbatang_web.ttf')}
@font-face{font-family:'NMJ';src:url('file://@N@NanumMyeongjo.ttf')}
@font-face{font-family:'NMJ';src:url('file://@N@NanumMyeongjoBold.ttf');font-weight:700}
:root{--b:#5f8fd8;--bl:#8fb2e6;--bp:#e9f0fb;--bd:#2f5fae;--g:#8a8f98;--gl:#e9eaec;--ink:#222}
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:'SJ','HB','NMJ',serif;font-size:8.7pt;line-height:2.0;letter-spacing:-.015em;word-spacing:-.08em;color:var(--ink);word-break:keep-all}
.katex{font-size:1.0em;margin:0 1.6pt;word-spacing:0}.katex-display>.katex{margin:0}
.katex-display{margin:.6em 0}
p{margin:.25em 0 .6em}
b{font-weight:700}
/* 1쪽 */
.p1{display:flex;gap:9mm;break-after:page}
.p1 .l{flex:1.05}.p1 .r{flex:1}
.ttl{background:var(--bl);color:#fff;font-family:'NSq';font-weight:700;font-size:11pt;padding:3pt 10pt;display:flex;justify-content:space-between}
.ttl b{color:#1b2a4a;font-weight:800}
table.ans{width:100%;border-collapse:collapse;font-family:'NSq';font-size:10pt}
table.ans td{padding:3.2pt 6pt;border-bottom:.5pt solid var(--gl);text-align:center}
table.ans td.n{color:var(--bl);font-weight:700;text-align:left;width:14%}
table.ans td.v{width:19%}
.sa{font-size:8.8pt;margin-top:5pt;line-height:1.75}
.sa .h{display:inline-block;background:var(--bp);color:var(--bd);font-family:'NSq';font-weight:700;font-size:8pt;padding:0 6pt;border-radius:2pt;margin-right:4pt}
h3{font-family:'NSq';font-weight:700;font-size:10.5pt;margin:0 0 6pt}
.cmp{margin-bottom:9pt}
.cmp .k{display:inline-block;background:var(--g);color:#fff;font-family:'NSq';font-size:7.6pt;font-weight:700;padding:0 6pt;border-radius:2pt}
.bar{display:flex;align-items:center;margin:2pt 0;font-family:'NSq';font-size:7.4pt;color:#9aa2ad}
.bar .t{height:12pt;border-radius:0 7pt 7pt 0;background:#eef1f5;display:flex;align-items:center;justify-content:flex-end;padding-right:6pt;color:#8a93a0}
.bar.me .t{background:var(--bp);color:var(--bd);font-weight:700}
.bar .v{margin-left:5pt}
table.cut{border-collapse:separate;border-spacing:3pt;font-family:'NSq';font-size:9pt;margin-top:4pt}
table.cut th{background:var(--bl);color:#fff;padding:2pt 14pt;font-weight:700;border-radius:2pt}
table.cut td{padding:2pt 14pt;text-align:center}
table.cut td.h{font-weight:700;text-align:left;padding-left:0}
.fine{font-family:'NSq';font-size:7.4pt;color:var(--g);margin-top:4pt}
/* 2쪽 */
.p2{display:flex;gap:9mm;break-after:page}
.p2 .l{flex:1}.p2 .r{flex:1}
.ctag{display:inline-block;background:var(--b);color:#fff;font-family:'NSq';font-weight:800;font-size:8.6pt;padding:2pt 8pt;margin-bottom:6pt}
.cm{background:#f4f6f9;border-radius:3pt;padding:9pt 11pt;margin-bottom:10pt;font-family:'NBG';font-size:8pt;line-height:2.05}
.cm .who{display:flex;align-items:center;gap:6pt;font-family:'NSq';font-weight:700;font-size:8.6pt;margin-bottom:4pt}
.cm .ic{width:18pt;height:18pt;border-radius:50%;background:var(--b);color:#fff;display:flex;align-items:center;justify-content:center;font-size:8pt}
.cm b{font-weight:700}
.chong{font-family:'NBG';font-size:8.3pt;line-height:2.15}
.chong .hd{display:flex;align-items:center;gap:7pt;margin-bottom:6pt}
.chong .hd .bub{width:32pt;height:32pt;border-radius:50%;background:var(--bp);display:flex;align-items:center;justify-content:center;font-family:'NSq';font-weight:800;color:var(--bd);font-size:8pt;text-align:center;line-height:1.15}
.chong p{margin:0 0 7pt}
.chong b{font-weight:700;color:#111}
/* 본문 2단 */
.cols{column-count:2;column-gap:11mm;column-fill:auto}
.it{margin:0 0 18pt}
.no{font-family:'NSq';font-weight:700;font-size:17pt;color:var(--b);line-height:1.1;margin:2pt 0 3pt;break-after:avoid}
.no .z{color:var(--bl);opacity:.75}
.mt{display:inline-flex;font-family:'NSq';font-size:7.6pt;font-weight:700;margin-bottom:5pt;break-after:avoid}
.mt span{padding:0 5pt;line-height:1.75}
.mt .a{background:#8c9097;color:#fff}.mt .b{background:#e3e5e8;color:#5e636b}
.mt.sj .a{background:#8c9097}
.cb{border:1pt solid var(--bl);border-radius:2pt;margin:4pt 0 10pt;break-inside:avoid;font-size:8.3pt;line-height:2}
.cb .h{display:flex;justify-content:space-between;align-items:center;padding:2pt 7pt;border-bottom:.6pt solid var(--bl);font-family:'NSq';font-size:8.2pt;color:var(--b);font-weight:700}
.cb .h .k{font-size:7pt;color:var(--b);font-weight:400}
.cb .bd{padding:3pt 8pt}
.cref{display:inline-flex;margin:0 4pt 0 3pt;font-family:'NSq';font-size:7pt;font-weight:700;vertical-align:1pt;border:.6pt solid var(--bl)}
.cref .a{background:#fff;color:var(--b);padding:0 3pt}.cref .b{background:var(--b);color:#fff;padding:0 4pt}
.tg{display:inline-flex;font-family:'NSq';font-size:7.6pt;font-weight:700;margin:5pt 0 3pt;break-after:avoid}
.tg span{padding:0 5pt;line-height:1.75}
.tg .a{background:#8c9097;color:#fff}.tg .b{background:#e3e5e8;color:#5e636b}
.tg.th .a{background:var(--b)}.tg.th .b{background:var(--bp);color:var(--bd)}
.flow{margin:4pt 0 8pt;break-inside:avoid}
.flow .fh{display:inline-flex;font-family:'NSq';font-size:7.6pt;font-weight:700;margin-bottom:4pt}
.flow .fh span{padding:0 5pt;line-height:1.75}.flow .fh .a{background:var(--b);color:#fff}.flow .fh .b{background:var(--bp);color:var(--bd)}
.st{position:relative;padding-left:11pt;margin-bottom:5pt}
.st:before{content:'';position:absolute;left:3.5pt;top:13pt;bottom:-6pt;width:3pt;background:linear-gradient(var(--bl),var(--bp))}
.st:last-child:before{bottom:2pt}
.st .sh{display:flex;align-items:center;gap:6pt;border:.6pt dashed var(--bl);border-radius:2pt;padding:1pt 6pt;margin-left:-11pt;background:#fff;position:relative;font-family:'NBG';font-size:8.4pt;font-weight:700}
.st .sh .s{font-family:'NSq';font-size:6.5pt;color:var(--bl);line-height:1;text-align:center}
.st .sh .s b{display:block;font-size:10pt;color:var(--b)}
.st ul{margin:3pt 0 0;padding-left:12pt;font-size:8.2pt;line-height:2}
.jt{margin-top:6pt}
.ck{background:#f4f6f9;border-radius:2pt;padding:5pt 9pt;margin:6pt 0;font-size:8.6pt;break-inside:avoid}
.ck .h{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.6pt solid #555;padding-bottom:1pt;margin-bottom:3pt;font-family:'NSq';font-weight:700;font-size:8pt}
.ck .h .c{color:var(--b);font-weight:800;font-size:9pt}
.ck .h .r{font-weight:400;font-size:7.4pt}
.ck ol{margin:0;padding-left:13pt}
.og{border:.6pt solid #c8cdd4;border-radius:2pt;margin:10pt 0 4pt;break-inside:avoid;font-size:8.1pt;line-height:2}
.og .h{display:flex;justify-content:space-between;padding:1.5pt 7pt;font-family:'NSq';font-size:7.4pt;font-weight:700;border-bottom:.5pt dotted #c8cdd4}
.og .h .r{color:var(--bl);font-weight:400}
.og .bd{padding:4pt 8pt}
.og .row{display:flex;gap:5pt;margin:1pt 0}
.og .row .k{flex:none;font-family:'NSq';font-size:7pt;font-weight:700;color:#fff;background:#9aa3ae;border-radius:2pt;padding:0 4pt;height:12pt;line-height:12pt;margin-top:3pt}
.og .row .k.c{background:var(--b)}.og .row .k.p{background:var(--bd)}
.og ul{margin:0;padding-left:12pt}
.an{text-align:right;font-family:'NSq';font-size:8.4pt;margin-top:4pt;break-before:avoid}
.an span{display:inline-block;background:var(--bp);color:var(--b);font-weight:700;font-size:7.4pt;padding:0 5pt;margin-right:5pt;border-radius:1pt}
.sec{column-span:all;font-family:'NSq';font-weight:800;font-size:10pt;color:#fff;background:var(--b);display:inline-block;padding:2pt 10pt;margin:6pt 0 8pt;position:relative}
/* 박스 안 글꼴: 부산단디고딕 — 본문 M, 제목 B, 보조 L (사용자 2026-11-24) */
.cb .bd,.og .bd,.st ul,.cm{font-family:'BD','NBG',sans-serif;font-weight:500}
.cb,.og,.flow,.cm,.ck,.tg,.mt,.cref,.p1,.p2,.ab .abh{word-spacing:normal}   /* 띄어쓰기 줄임은 본문(신중명조)만 — 박스는 원래대로(2026-11-24) */
.cb .h,.og .h,.st .sh,.cm .who{font-family:'BD','NSq',sans-serif;font-weight:700}
.cb .h .k,.og .h .r{font-family:'BD','NSq',sans-serif;font-weight:300}
.cb .bd b,.og .bd b,.cm b{font-weight:700}
/* 부록 빠른 정답 */
.apqa{break-before:page}.qas{display:grid;grid-template-columns:repeat(5,1fr);gap:4pt 8pt;font-family:'NSq';font-size:9pt}
.qa{border-bottom:.6pt solid #e1e8ef;padding:3pt 4pt;display:flex;justify-content:space-between}.qa b{color:var(--b)}
/* 부록: 원본 문항 (사용자 2026-11-24) — 한 쪽에 위 둘·여백·아래 둘 */
#apx-src{width:100%}
.apxh{display:inline-flex;font-family:'NSq';font-size:9pt;font-weight:800;margin:0 0 8pt}
.apxh span{padding:1pt 9pt;line-height:1.7}.apxh .a{background:var(--b);color:#fff}.apxh .b{background:var(--bp);color:var(--bd)}
.ab{border:.8pt solid #c8cdd4;border-radius:2pt;padding:6pt 8pt 7pt;font-size:8.1pt;line-height:1.9;box-sizing:border-box;width:100%}
.ab .abh{display:flex;align-items:center;gap:6pt;margin-bottom:4pt}
.ab .abh .chip{display:inline-flex;font-family:'NSq';font-size:7.4pt;font-weight:700}
.ab .abh .chip span{padding:0 5pt;line-height:1.75}.ab .abh .chip .a{background:#8c9097;color:#fff}.ab .abh .chip .b{background:#e3e5e8;color:#5e636b}
.ab .abh .src{font-family:'BD','NSq',sans-serif;font-weight:300;font-size:7pt;color:#8a8f98}
.ab .cond{border:.6pt solid #555;padding:2pt 6pt;margin:3pt 0}
.ab .ci{display:block;padding-left:2.4em;text-indent:-2.4em}.ab .ck{display:inline-block;width:2.4em;text-indent:0;background:none;border-radius:0;padding:0;margin:0;font-size:inherit;break-inside:auto}.ab .cond{background:none}
.ab fieldset.bogi{border:.6pt solid #555;margin:4pt 0;padding:1pt 6pt 3pt}.ab fieldset.bogi legend{font-size:7.4pt;padding:0 4pt;margin:0 auto}
.ab .bi{display:block;padding-left:1.6em;text-indent:-1.6em}.ab .bk{display:inline-block;width:1.6em;text-indent:0}
.ab .fig{text-align:center;margin:3pt 0}
.ab .chs{display:flex;flex-wrap:wrap;gap:1pt 10pt;margin-top:3pt}
.apg{height:968px;display:flex;flex-direction:column;break-after:page;break-inside:avoid}
.apg:last-child{break-after:auto}
.ahalf{flex:1 1 0;display:grid;grid-template-columns:1fr 1fr;column-gap:11mm;align-items:start;min-height:0}
.ahalf.full{flex:2 1 0;grid-template-columns:1fr}
"""

def tag(a, b, cls=''):
    return f'<div class="tg {cls}"><span class="a">{a}</span><span class="b">{b}</span></div>'

def cref(h):   # <span class="cref">실전 개념|제목</span> → 꼬리표
    return re.sub(r'<span class="cref">([^|<]+)\|([^<]+)</span>', r'<span class="cref"><span class="a">\1</span><span class="b">\2</span></span>', h)

def item_html(n, d, c, sitem=None):
    h = [f'<div class="it"><div class="no">{num(n) if str(n).isdigit() else n}</div>']
    m = d.get('method') or '교과서적'
    h.append(f'<div class="mt"><span class="a">{m}</span><span class="b">해법</span></div>')
    for cb in d.get('concepts') or []:
        h.append(f'<div class="cb"><div class="h"><span>✎ {cb.get("title", "")}</span><span class="k">• {cb.get("kind", "실전 개념")}</span></div><div class="bd">{cb.get("body", "")}</div></div>')
    if d.get('think'): h.append(tag('생각의', '시작', 'th') + f'<p>{d["think"]}</p>')
    if d.get('flow'):
        st = ''.join(f'<div class="st"><div class="sh"><span class="s">STEP<b>{i + 1:02d}</b></span><span class="tt">{s.get("title", "")}</span></div><ul>' + ''.join(f'<li>{p}</li>' for p in s.get('points') or []) + '</ul></div>' for i, s in enumerate(d['flow']))
        h.append(f'<div class="flow"><div class="fh"><span class="a">흐름</span><span class="b">정리</span></div>{st}</div>')
    bd = re.split(r'<p>\s*<b>\s*채점\s*기준', d.get('body') or '')[0]   # 사용자 2026-11-23: 채점 기준 뺌
    h.append(re.sub(r'<sup>[^<]*</sup>', '', cref(bd)))
    if d.get('justify'): h.append('<div class="jt">' + tag('논리적', '정당화') + cref(d['justify']) + '</div>')
    if False and d.get('notes'):   # 사용자 2026-11-23: 각주 뺌
        h.append('<div class="ck"><div class="h"><span><span class="c">✓ CHECK</span>&nbsp; 각주</span><span class="r">해설 본문의 각주</span></div><ol>' + ''.join(f'<li>{x}</li>' for x in d['notes']) + '</ol></div>')
    v = d.get('variation') or {}
    it0 = sitem if sitem is not None else c.ITEMS[int(n)]
    _tags = ''.join(re.findall(r'\[([^\]]+)\]', str(it0.get('var', ''))))
    only_num = bool(_tags) and re.sub(r'숫자 변경|[\s·,]', '', _tags) == ''
    if (str(n).isdigit() and int(n) <= 8) or str(n) in ('S1', '서답형 1') or only_num: v = {}   # 사용자 2026-11-23: 앞 번호대·숫자만 바꾼 문항은 변형 포인트 상자 뺌
    key = (sitem if sitem is not None else c.ITEMS[int(n)]).get('key', '')
    if v:
        src = f'부교재 {key}&nbsp;&nbsp;{F.D[key][1]}' if key in F.D else '학교 자체'
        rows = ''
        if v.get('origin'): rows += f'<div class="row"><span class="k">원문</span><div>{v["origin"]}</div></div>'
        if v.get('changes'): rows += '<div class="row"><span class="k c">변형</span><ul>' + ''.join(f'<li>{x}</li>' for x in v['changes']) + '</ul></div>'
        if v.get('point'): rows += f'<div class="row"><span class="k p">포인트</span><div>{v["point"]}</div></div>'
        h.append(f'<div class="og"><div class="h"><span>원문 연계&nbsp;&nbsp;변형 포인트</span><span class="r">{src}</span></div><div class="bd">{rows}</div></div>')
    if str(n).isdigit():
        a = c.ANS[int(n)]; ch = str(c.Q[int(n)][2][a - 1]); ct = ch[2:] if ch.startswith('T:') else f'\\({ch}\\)'
        h.append(f'<div class="an"><span>정답</span>{CIRC[a - 1]}</div>')
    h.append('</div>')
    return ''.join(h)

MATHRE = re.compile(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)')
def outside(s, f):
    """수식 밖 글에만 f를 적용"""
    s = str(s or ''); out, i = [], 0
    for m in MATHRE.finditer(s):
        out.append(f(s[i:m.start()])); out.append(m.group(0)); i = m.end()
    out.append(f(s[i:])); return ''.join(out)
SUBN = lambda t: re.sub(r'\(([가나다라])\)', lambda m: '㈎㈏㈐㈑'['가나다라'.index(m.group(1))], re.sub(r'\(([1-5])\)', lambda m: '⑴⑵⑶⑷⑸'[int(m.group(1)) - 1], t))
DFR = lambda t: re.sub(r'\\\(([\s\S]+?)\\\)', lambda m: '\\(' + re.sub(r'\\frac(?=\s*[{0-9])', r'\\dfrac', m.group(1)) + '\\)', t)
def tidy(d):
    """소문항 번호 (1) → ⑴ (사용자 2026-11-23 괄호 금지)"""
    for k in ('body', 'think', 'justify'):
        if d.get(k): d[k] = DFR(outside(d[k], SUBN))
    for st in d.get('flow') or []:
        st['points'] = [outside(p, SUBN) for p in st.get('points') or []]
    v = d.get('variation') or {}
    for k in ('origin', 'point'):
        if v.get(k): v[k] = outside(v[k], SUBN)
    if v.get('changes'): v['changes'] = [outside(x, SUBN) for x in v['changes']]
    return d

def nodot(doc):
    """가운데점 없애기, 짧은 항목(STEP·변형 항목·꼬리표) 끝 온점 없애기 (사용자 2026-11-23)"""
    body = doc.split('<body>', 1)
    def t(x):
        x = re.sub(r'\s*·\s*', lambda m: ' ' if m.group(0).strip() == '·' and m.group(0) != '·' else ', ', x)
        return x
    rest = re.sub(r'>([^<]+)<', lambda m: '>' + outside(m.group(1), t) + '<', body[1])
    rest = re.sub(r'([다])\.(\s*</li>)', r'\1\2', rest)                       # 목록 항목 끝 온점
    rest = re.sub(r'(<div class="row"><span class="k[^"]*">[^<]+</span><div>[^<]*?)\.(\s*</div>)', r'\1\2', rest)
    return body[0] + '<body>' + rest

def stylecheck(D, front):
    """사용자 규칙(2026-11-23): 모든 문장 '-다.'로 끝, 글 속 괄호 금지, 각주 없음. 어긴 곳을 출력한다."""
    bad = []
    MATH = re.compile(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)')
    def txt(x): return html.unescape(re.sub(r'<[^>]+>', ' ', MATH.sub(' M ', str(x or ''))))
    def chk(where, x):
        t = txt(x)
        i = t.find('(') if '(' in t else t.find(')')
        if i >= 0: bad.append(f'{where}: 괄호 — ' + t[max(0, i - 20):i + 25].strip())
        for sen in re.split(r'(?<=[.!?])\s+', t.strip()):
            sen = sen.strip()
            if len(sen) > 8 and not re.search(r'다\.?$|M\s*\.?$|[:]$', sen): bad.append(f'{where}: 끝맺음 — …' + sen[-25:])
    for n, d in D.items():
        for k in ('body', 'think'): chk(f'{n}.{k}', d.get(k))   # 괄호는 ★ 논리적 정당화에서만 허용(사용자 2026-11-23)
        for cb in d.get('concepts') or []: chk(f'{n}.개념', cb.get('body'))
        for st in d.get('flow') or []:
            for pt in st.get('points') or []: chk(f'{n}.STEP', pt)
        v = d.get('variation') or {}
        for k in ('origin', 'point'): chk(f'{n}.변형', v.get(k))
        for x in v.get('changes') or []: chk(f'{n}.변형', x)
        if d.get('notes'): bad.append(f'{n}: 각주 남음')
    for x in front.get('chongpyeong', []): chk('총평', x)
    for x in front.get('comments', []): chk('코멘트', x['text'])
    print('문체 검사:', len(bad), '곳'); [print('  ', b) for b in bad[:40]]
    return bad

def cover(name, css):
    """표지(흰 배경) + 빈 쪽 하나 (사용자 2026-11-23)"""
    no = re.sub(r'\D', '', name).zfill(2)
    rings = ('<svg width="794" height="400" viewBox="0 0 595 300" style="position:absolute;left:0;top:330pt">'
             '<circle cx="110" cy="150" r="62" fill="none" stroke="#5f8fd8" stroke-width="26"/>'
             '<circle cx="300" cy="150" r="62" fill="none" stroke="#8fb2e6" stroke-width="26"/><circle cx="300" cy="150" r="16" fill="#8fb2e6"/>'
             '<circle cx="490" cy="150" r="62" fill="#5f8fd8"/>'
             '<path d="M40 150 C 160 60, 240 240, 360 150 S 520 60, 595 150" fill="none" stroke="#c9d6ea" stroke-width="2" stroke-dasharray="3 5"/></svg>')
    pg = 'width:210mm;height:297mm;position:relative;overflow:hidden;background:#fff;page-break-after:always'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body style="margin:0">'
            f'<div style="{pg}">'
            '<div style="position:absolute;left:24mm;top:28mm;font-family:NSq;font-size:9pt;letter-spacing:4pt;color:#8fb2e6">2026&nbsp;&nbsp;2학년 2학기</div>'
            '<div style="position:absolute;left:24mm;top:40mm;font-family:NSq;font-weight:800;font-size:38pt;line-height:1.25;color:#2f5fae;letter-spacing:-1pt">미적분Ⅰ<br>기말 모의고사</div>'
            f'<div style="position:absolute;right:24mm;top:40mm;font-family:NSq;font-weight:800;font-size:72pt;color:#5f8fd8;letter-spacing:4pt">{no}</div>'
            f'{rings}'
            '<div style="position:absolute;left:24mm;top:230mm;font-family:NSq;font-weight:700;font-size:13pt;letter-spacing:6pt;color:#5f8fd8">정 답 및 해 설</div>'
            f'<div style="position:absolute;left:24mm;top:240mm;font-family:NSq;font-size:9pt;color:#8a8f98">기말 {name}  ·  해설  변형 포인트  출제자의 총평</div>'
            '<div style="position:absolute;left:0;right:0;bottom:16mm;text-align:center;font-family:NSq;font-size:9pt;color:#5f8fd8">양정고 미적분Ⅰ 기말 대비</div>'
            f'</div><div style="{pg.replace("page-break-after:always", "")}">&nbsp;</div></body></html>').replace('  ·  ', '&nbsp;&nbsp;&nbsp;')

def appendix(c):
    """부록: 시험지 번호 순서로 부교재 원본 문항을 박스로. 배치는 haeseol2.js가 쪽마다 위 둘·아래 둘로 나눈다."""
    PARTS = '/home/user/Finale/output/build/부교재_기말/parts'
    rows = [(f'{n:02d}', c.ITEMS[n]) for n in range(1, 19)] + [('서답 1', c.SITEMS['S1']), ('서답 2', c.SITEMS['S2'])]
    out = ['<div class="apxh"><span class="a">부록</span><span class="b">원본 문항</span></div><div id="apx-src">']
    for lab, it in rows:
        k = it.get('key', '')
        if k not in F.I: continue
        body, ch = F.I[k][0], F.I[k][1]
        body = re.sub(r'src="(fig_[^"]+)"', lambda m: f'src="file://{PARTS}/{m.group(1)}"', body)
        chs = ('<div class="chs">' + ''.join(f'<span>{CIRC[i]} {(x[2:] if str(x).startswith("T:") else chr(92) + "(" + str(x) + chr(92) + ")")}</span>' for i, x in enumerate(ch[:5])) + '</div>') if ch else ''
        src = f'부교재 {k}&nbsp;&nbsp;{F.D[k][1]}'.replace(' · ', ' ')
        out.append(f'<div class="ab"><div class="abh"><span class="chip"><span class="a">원본</span><span class="b">{lab}</span></span><span class="src">{src}</span></div>{body}{chs}</div>')
    out.append('</div>')
    qa = ''.join(f'<span class="qa"><b>{lab}</b>{F.I[it.get("key")][2] if it.get("key") in F.I else ""}</span>' for lab, it in rows)
    out.append(f'<div class="apqa"><div class="apxh"><span class="a">부록</span><span class="b">원본 빠른 정답</span></div><div class="qas">{qa}</div></div>')
    return ''.join(out)

def build(rdir, out):
    rdir = os.path.abspath(rdir); name = os.path.basename(rdir); c = load(rdir)
    D = {}
    for f in sorted(glob.glob(os.path.join(rdir, 'haeseol', 'items_*.json'))):
        for d in json.load(open(f)): D[str(d['n'])] = tidy(d)
    front = json.load(open(os.path.join(rdir, 'haeseol', 'front.json'))) if os.path.exists(os.path.join(rdir, 'haeseol', 'front.json')) else {}
    stylecheck(D, front)
    css = CSS.replace('@N@', NAN).replace('@F@', FONTS)
    H = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{css}</style></head><body>']
    # 1쪽 — 정답표
    cols = [list(range(1, 9)), list(range(9, 17)), [17, 18]]
    rows = ''
    for i in range(8):
        tds = ''
        for col in cols:
            if i < len(col): n = col[i]; tds += f'<td class="n">{num(n)}</td><td class="v">{CIRC[c.ANS[n] - 1]}</td>'
            else: tds += '<td class="n"></td><td class="v"></td>'
        rows += f'<tr>{tds}</tr>'
    sa = ''
    for s, lab in (('S1', '서답형 1'), ('S2', '서답형 2')):
        a = c.SITEMS[s]['ans']; a = a if isinstance(a, (list, tuple)) else [a]
        sa += f'<div><span class="h">{lab}</span>' + ' &nbsp; '.join(fx(x) for x in a) + '</div>'
    # 난도 비교(측정 체감, 번호대 평균)
    fe = feels(rdir, c); prof = json.load(open(PROFILE)) if os.path.exists(PROFILE) else {}
    pv = {str(k): v for k, v in (prof.get('feel') or prof.get('d') or {}).items()} if isinstance(prof, dict) else {}
    if not pv:
        pv = dict(zip([str(i) for i in range(1, 19)] + ['S1', 'S2'], [1.3, 1.7, 1.3, 3.0, 3.3, 4.7, 4.7, 4.0, 5.7, 5.0, 3.7, 5.3, 4.7, 5.0, 5.7, 7.0, 7.3, 7.7, 3.0, 6.3]))
    bands = [('1–4번', range(1, 5)), ('5–8번', range(5, 9)), ('9–12번', range(9, 13)), ('13–16번', range(13, 17)), ('17–18번', range(17, 19)), ('서답형', ['S1', 'S2'])]
    cmp = ''
    for lab, rg in bands:
        ks = [str(k) for k in rg]
        mine = [fe[k] for k in ks if k in fe]; base = [pv[k] for k in ks if k in pv]
        if not mine or not base: continue
        m, b = sum(mine) / len(mine), sum(base) / len(base)
        w = lambda x: f'{18 + 8.2 * x:.0f}%'
        cmp += (f'<div class="cmp"><span class="k">{lab}</span>'
                f'<div class="bar"><div class="t" style="width:{w(b)}">2026-2 중간</div><span class="v">{b:.1f}</span></div>'
                f'<div class="bar me"><div class="t" style="width:{w(m)}">기말 {name}</div><span class="v">{m:.1f}</span></div></div>')
    lv = {n: it.get('level') for n, it in c.ITEMS.items()}
    idx = sum(PTS[k] for k, l in lv.items() if l in ('상', '최상')) + 0.5 * sum(PTS[k] for k, l in lv.items() if l == '중상') + (3 if c.SITEMS['S2'].get('level') == '중상' else 6 if c.SITEMS['S2'].get('level') in ('상', '최상') else 0)
    # 등급컷: 측정 체감이 2026-2 중간 같은 번호보다 배점 가중으로 얼마나 높은지(ex)로 낸다(2026-11-24 사용자 지적: 지수만 쓰면 7–10회 컷이 똑같음).
    _pt = {str(k): v for k, v in PTS.items()}; _ks = [k for k in pv if k in fe]
    ex = sum(_pt.get(k, 10) * (fe[k] - pv[k]) for k in _ks) / max(1, sum(_pt.get(k, 10) for k in _ks)) if _ks else None
    if ex is not None: c1 = 90.1 - 2.1 * max(0, ex); c2 = 75.8 - 2.8 * max(0, ex)
    else: c1 = 90.1 - 0.75 * max(0, idx - 25.6); c2 = 75.8 - 1.0 * max(0, idx - 25.6)
    finecut = (f'<div class="fine">블라인드 풀이로 잰 문항별 체감 난도가 2026 2학기 중간고사 같은 번호보다 배점 가중 평균으로 {ex:.2f}만큼 높아, 그만큼 중간고사 성적에서 내려 환산한 값이다.</div></div>' if ex is not None else f'<div class="fine">난도 지수 {idx:.1f}을 2026 2학기 중간고사 성적에 맞춰 환산한 값이다.</div></div>')
    H.append(f'<div class="p1"><div class="l"><div class="ttl"><span>미적분Ⅰ 기말 모의고사 {name}</span><b>정답 및 해설</b></div>'
             f'<table class="ans">{rows}</table><div class="sa">{sa}</div>'
             f'<h3 style="margin-top:16pt">기말 {name} &nbsp;<b>예상 등급컷</b></h3>'
             f'<table class="cut"><tr><td></td><th>원점수</th></tr><tr><td class="h">1등급컷</td><td>{round(c1)}</td></tr><tr><td class="h">2등급컷</td><td>{round(c2)}</td></tr></table>'
             f'{finecut}'
             f'<div class="r"><h3>기말 {name} VS 2026-2 중간 &nbsp;난도 비교</h3>{cmp}'
             f'<div class="fine">번호대별 평균 체감 난도를 10점 만점으로 나타냈다. 2026 2학기 중간고사 같은 번호를 기준으로 맞춘 블라인드 풀이 측정값이다.</div></div></div>')
    # 2쪽 — 검수 코멘트 · 총평
    if front:
        cm = ''.join(f'<div class="cm"><div class="who"><span class="ic">✎</span>{x["who"]}</div>{x["text"]}</div>' for x in front.get('comments', []))
        ch = ''.join(f'<p>{p}</p>' for p in front.get('chongpyeong', []))
        H.append(f'<div class="p2"><div class="l"><span class="ctag">검수 코멘트</span>{cm}</div>'
                 f'<div class="r chong"><div class="hd"><span class="bub">출제자의<br>총평</span></div>{ch}</div></div>')
    # 해설 본문
    H.append('<div class="cols">')
    for n in range(1, 19):
        d = D.get(str(n))
        if d: H.append(item_html(n, d, c))
    for s, lab in (('S1', '서답형 1'), ('S2', '서답형 2')):
        d = D.get(s)
        if d: H.append(item_html(lab, d, c, c.SITEMS[s]))
    H.append('</div>')
    H.append('<div style="break-before:page"></div>' + appendix(c))
    H.append('</body></html>')
    src = os.path.join(rdir, 'haeseol', 'book_src.html')
    open(src, 'w').write(fx(nodot(''.join(H))))
    body_pdf = os.path.join(rdir, 'haeseol', 'book_body.pdf'); cover_pdf = os.path.join(rdir, 'haeseol', 'cover.pdf')
    subprocess.run(['node', os.path.join(HERE, 'haeseol2.js'), src, body_pdf, f'기말 모의고사 {name}'], check=True)
    csrc = os.path.join(rdir, 'haeseol', 'cover_src.html'); open(csrc, 'w').write(cover(name, css))
    subprocess.run(['node', os.path.join(HERE, 'haeseol2.js'), csrc, cover_pdf, '-', 'plain'], check=True)
    import pymupdf
    doc = pymupdf.open(cover_pdf); doc.insert_pdf(pymupdf.open(body_pdf)); doc.save(out, garbage=4, deflate=True)
    os.remove(body_pdf); os.remove(cover_pdf)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
