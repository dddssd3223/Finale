# -*- coding: utf-8 -*-
"""학생용 해설지(변형 포인트 + 해설) — 채점기준(sol3)과 따로, 읽기 좋게 디자인한 판.
사용: python3 haeseol.py <회차 폴더> <출력 PDF>
문항마다: 문제 · 변형 포인트(원문 출처·바꾼 자리) · 핵심 · 해설 · 함정. 맨 앞에 정답표와 회차 구성.
글꼴은 시스템 나눔(나눔스퀘어·나눔바른고딕), 수식은 KaTeX. 렌더러는 haeseol.js(회차 폴더의 빌드 파일은 건드리지 않음)."""
import os, re, sys, html, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말'); import items_final as F
NAN = '/usr/share/fonts/truetype/nanum/'
KATEX_CSS = os.path.join(HERE, '..', 'node_modules', 'katex', 'dist', 'katex.min.css')
CIRC = '①②③④⑤'
UNIT = {'D': '도함수의 활용 (1)', 'M': '도함수의 활용 (2)', 'I': '부정적분과 정적분', 'J': '정적분의 활용'}
LVC = {'하': '#5b9bd5', '중하': '#5b9bd5', '중': '#3f8f6b', '중상': '#d08a1c', '상': '#c4472f', '최상': '#8e2a6b'}

def load(rdir):
    spec = importlib.util.spec_from_file_location('c3', os.path.join(rdir, 'content3.py'))
    m = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(rdir); sys.path.insert(0, rdir)
    try: spec.loader.exec_module(m)
    finally: os.chdir(cwd); sys.path.pop(0)
    return m

def fx(s):   # 수식 안의 &lt; &gt;를 KaTeX용 부등호로
    s = str(s or '')
    return re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), s)

JARGON = [(r'(?:GEN|LIVE)\d-\d\d-\d+(?:\s*[·,/]\s*)?', ''), (r'OP\d\d(?:\s*[+·,]\s*)?', ''), (r'DB\s*(?:스케치|결합|후보)?의?\s*', ''),
          (r'(?:조작_보강|학교식_예상|예상밖_포인트|v3_추가(?:_예상)?|결합_후보|후보_순위|예상밖|결합)\s*\d+', ''), (r'인쇄된\s*N제[^.)]*', ''), (r'dupcheck[^.)]*', ''),
          (r'분석집\s*변형[①②③]?', '분석집 문항'), (r'\(\s*의\s+', '('), (r'\(\s*[,·;]?\s*\)', ''), (r'\(\s*,\s*', '('), (r',\s*\)', ')'), (r'\s{2,}', ' ')]
def clean(s):
    """학생용: 출제 내부 기록(DB 칸 이름·변형 id·OP 번호)을 지운다"""
    s = str(s or '')
    for a, b in JARGON: s = re.sub(a, b, s)
    return s.strip()

def choice(c):
    c = str(c)
    return c[2:] if c.startswith('T:') else f'\\({c}\\)'

def problem(it, choices):
    h = [f'<div class="qb">{it["body"]}</div>']
    if it.get('cond'):
        h.append('<div class="cond">' + ''.join(f'<div><b>({k})</b> {v}</div>' if k else f'<div>{v}</div>' for k, v in it['cond']) + '</div>')
    if it.get('bogi'):
        h.append('<div class="bogi"><div class="bt">보 기</div>' + ''.join(f'<div><b>{k}.</b> {v}</div>' for k, v in it['bogi']) + '</div>')
    if it.get('after'): h.append(f'<div class="qb">{it["after"]}</div>')
    if choices:
        h.append('<div class="chs">' + ''.join(f'<span>{CIRC[i]} {choice(c)}</span>' for i, c in enumerate(choices)) + '</div>')
    return ''.join(h)

def points(var):
    """'[기법·기법] 원문 → 변형 · [기법] …' → (태그 목록, [(원문, 변형 또는 None), …])"""
    var = str(var or '')
    tags, rows = [], []
    for seg in re.split(r'\s+·\s+(?=\[)|\s+·\s+(?![^()]*\))', var):
        seg = seg.strip()
        if not seg: continue
        m = re.match(r'\[([^\]]+)\]\s*(.*)', seg, flags=re.S)
        if m:
            tags += [t.strip() for t in re.split(r'[·,:+]', m.group(1)) if t.strip() and len(t.strip()) <= 12]; seg = m.group(2).strip()
        if not seg: continue
        parts = re.split(r'\s+→\s+', seg, maxsplit=1)
        rows.append((parts[0], parts[1] if len(parts) > 1 else None))
    seen = []; [seen.append(t) for t in tags if t not in seen]
    return seen, rows

def src_line(key, src):
    if not key or key not in F.D: return html.escape(str(src or '학교 자체'))
    return f'부교재 <b>{key}</b> · {html.escape(F.D[key][1])} · 원문 난도 {F.D[key][0]}'

def vblock(var, key, src):
    tags, rows = points(clean(var))
    h = ['<div class="sec vp"><div class="lab">변형 포인트</div><div class="cnt">']
    h.append(f'<div class="src">{src_line(key, src)}</div>')
    if tags: h.append('<div class="tags">' + ''.join(f'<span>{html.escape(t)}</span>' for t in tags) + '</div>')
    for a, b in rows:
        h.append(f'<div class="ch"><span class="o">원문</span> {a} <span class="ar">→</span> <span class="n">변형</span> {b}</div>' if b
                 else f'<div class="ch">{a}</div>')
    h.append('</div></div>')
    return ''.join(h)

def sec(cls, lab, body):
    return f'<div class="sec {cls}"><div class="lab">{lab}</div><div class="cnt">{body}</div></div>' if body else ''

def wrong_html(w):
    if not w: return ''
    if isinstance(w, dict): w = '<br>'.join(f'{k}: {v}' for k, v in w.items())
    if isinstance(w, (list, tuple)): w = '<br>'.join(map(str, w))
    return re.sub(r'\s+(?=[②③④⑤]\s)', '<br>', str(w))

CSS = """
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareR.ttf')}
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareB.ttf');font-weight:700}
@font-face{font-family:'NSq';src:url('file://@N@NanumSquareEB.ttf');font-weight:800}
@font-face{font-family:'NBG';src:url('file://@N@NanumBarunGothic.ttf')}
@font-face{font-family:'NBG';src:url('file://@N@NanumBarunGothicBold.ttf');font-weight:700}
:root{--ac:#1f4e79;--ac2:#2e75b6;--bg:#eef4fa;--key:#e8f5ee;--keyb:#3f8f6b;--trap:#fff3e3;--trapb:#d08a1c;--ink:#1d2733;--mute:#6b7a8c}
*{box-sizing:border-box}
body{font-family:'NBG',sans-serif;font-size:9.2pt;line-height:1.72;color:var(--ink);margin:0;word-break:keep-all}
.katex{font-size:1.04em}
.katex-display{margin:.35em 0}
b{font-weight:700}
.cover{border-radius:10pt;background:linear-gradient(135deg,#1f4e79,#2e75b6);color:#fff;padding:16pt 20pt 14pt;margin-bottom:12pt}
.cover .k{font-family:'NSq';font-size:9pt;letter-spacing:2pt;opacity:.85}
.cover h1{font-family:'NSq';font-weight:800;font-size:22pt;margin:3pt 0 2pt;letter-spacing:-.5pt}
.cover .s{font-family:'NSq';font-size:10pt;opacity:.92}
h2{font-family:'NSq';font-weight:800;font-size:12pt;color:var(--ac);margin:12pt 0 6pt;padding-left:8pt;border-left:4pt solid var(--ac2)}
table.ans{border-collapse:separate;border-spacing:0;width:100%;font-family:'NSq';font-size:9pt;text-align:center;border:1pt solid #c9d6e3;border-radius:6pt;overflow:hidden}
table.ans th{background:var(--bg);color:var(--ac);font-weight:700;padding:3pt 0;border-bottom:1pt solid #c9d6e3}
table.ans td{padding:4pt 0;font-size:10.5pt;font-weight:700}
table.ans th+th,table.ans td+td{border-left:1pt solid #e1e8ef}
table.map{border-collapse:collapse;width:100%;font-size:8.3pt}
table.map th{font-family:'NSq';font-weight:700;color:#fff;background:var(--ac);padding:3pt 4pt;text-align:left}
table.map td{padding:2.5pt 4pt;border-bottom:.6pt solid #e1e8ef;vertical-align:top}
table.map tr:nth-child(even) td{background:#f7fafd}
.pill{display:inline-block;border-radius:8pt;padding:0 6pt;font-family:'NSq';font-weight:700;font-size:7.6pt;color:#fff;line-height:1.6}
.card{margin:0 0 12pt;border:1pt solid #d5e0eb;border-radius:8pt;overflow:hidden}
.head{display:flex;align-items:center;gap:8pt;background:var(--bg);padding:5pt 10pt;border-bottom:1pt solid #d5e0eb;break-after:avoid}
.num{font-family:'NSq';font-weight:800;font-size:15pt;color:var(--ac);min-width:24pt}
.head .meta{flex:1;font-family:'NSq';font-size:8.2pt;color:var(--mute)}
.head .an{font-family:'NSq';font-weight:800;font-size:10pt;color:#fff;background:var(--ac);border-radius:6pt;padding:2pt 9pt}
.q{padding:7pt 12pt 6pt;break-inside:avoid;border-bottom:1pt dashed #d5e0eb}
.qb{margin:0}
.cond{border:.8pt solid #9fb3c8;border-radius:4pt;padding:3pt 8pt;margin:4pt 0}
.bogi{border:.8pt solid #9fb3c8;border-radius:4pt;padding:3pt 8pt;margin:5pt 0;position:relative}
.bogi .bt{font-family:'NSq';font-size:7.8pt;color:var(--mute);text-align:center;letter-spacing:3pt}
.chs{display:flex;flex-wrap:wrap;gap:4pt 16pt;margin-top:4pt}
.fig{text-align:center;margin:4pt 0}
.sec{display:flex;gap:8pt;padding:6pt 12pt}
.sec .lab{flex:none;width:44pt;font-family:'NSq';font-weight:800;font-size:8.3pt;padding-top:1pt}
.sec .cnt{flex:1;min-width:0}
.vp{background:#f6f9fc}
.vp .lab{color:var(--ac2)}
.vp .src{font-family:'NSq';font-size:8.2pt;color:var(--mute)}
.tags{margin:2pt 0 3pt}
.tags span{display:inline-block;font-family:'NSq';font-size:7.6pt;font-weight:700;color:var(--ac);background:#dce8f4;border-radius:7pt;padding:0 6pt;margin:0 3pt 2pt 0}
.ch{margin:1pt 0;font-size:8.8pt}
.ch .o,.ch .n{font-family:'NSq';font-size:7.4pt;font-weight:700;border-radius:3pt;padding:0 3pt;color:#fff}
.ch .o{background:#8a99a8}.ch .n{background:var(--ac2)}
.ch .ar{color:var(--ac2);font-weight:700;margin:0 2pt}
.key{background:var(--key)}.key .lab{color:var(--keyb)}
.sol .lab{color:var(--ac)}
.trap{background:var(--trap)}.trap .lab{color:var(--trapb)}
.rub{width:100%;border-collapse:collapse;font-size:8.6pt;margin-top:3pt}
.rub td{border-top:.6pt solid #e1e8ef;padding:2pt 3pt;vertical-align:top}
""".replace('@N@', NAN)

def card(n, it, choices, ans_txt, pts, src):
    lv = it.get('level', '')
    key = it.get('key', '')
    unit = UNIT.get(str(key)[:1], '')
    h = [f'<div class="card"><div class="head"><div class="num">{n}</div>'
         f'<div class="meta"><span class="pill" style="background:{LVC.get(lv, "#6b7a8c")}">{lv}</span> &nbsp;{unit} · {pts}</div>'
         f'<div class="an">{ans_txt}</div></div>']
    h.append(f'<div class="q">{problem(it, choices)}</div>')
    h.append(vblock(it.get('var'), key, src))
    h.append(sec('key', '핵심', fx(clean(it.get('fast')))))
    return h

def build(rdir, out):
    rdir = os.path.abspath(rdir); c = load(rdir); name = os.path.basename(rdir)
    H = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{CSS}</style></head><body>']
    H.append(f'<div class="cover"><div class="k">YANGJEONG · 미적분Ⅰ 2학기 기말 대비</div><h1>모의고사 {name} 해설</h1>'
             '<div class="s">변형 포인트 · 핵심 · 해설 · 함정</div></div>')
    # 정답표
    th = ''.join(f'<th>{n}</th>' for n in range(1, 19)); td = ''.join(f'<td>{CIRC[c.ANS[n]-1]}</td>' for n in range(1, 19))
    H.append(f'<h2>정답</h2><table class="ans"><tr>{th}</tr><tr>{td}</tr></table>')
    sa = []
    for s, lab in (('S1', '서답형 1'), ('S2', '서답형 2')):
        a = c.SITEMS[s]['ans']; sa.append(f'<b>{lab}</b> ' + ' / '.join(fx(x) for x in (a if isinstance(a, (list, tuple)) else [a])))
    H.append('<div style="margin-top:4pt;font-size:8.8pt">' + ' &nbsp;&nbsp; '.join(sa) + '</div>')
    # 회차 구성
    H.append('<h2>회차 구성 — 원문과 변형 유형</h2><table class="map"><tr><th style="width:9%">번호</th><th style="width:11%">원문</th><th style="width:20%">단원</th><th style="width:9%">수준</th><th>변형 유형</th></tr>')
    rows = [(str(n), c.ITEMS[n]) for n in range(1, 19)] + [('서답 1', c.SITEMS['S1']), ('서답 2', c.SITEMS['S2'])]
    for n, it in rows:
        k = it.get('key', ''); lv = it.get('level', '')
        tg = ', '.join(points(it.get('var'))[0]) or '—'
        H.append(f'<tr><td><b>{n}</b></td><td>{k}</td><td>{UNIT.get(str(k)[:1], "")}</td><td><span class="pill" style="background:{LVC.get(lv, "#6b7a8c")}">{lv}</span></td><td>{html.escape(tg)}</td></tr>')
    H.append('</table><div style="break-after:page"></div>')
    # 문항별
    H.append('<h2>선택형</h2>')
    for n in range(1, 19):
        it = c.ITEMS[n]; ch = c.Q[n][2]; a = c.ANS[n]
        h = card(n, it, ch, f'정답 {CIRC[a-1]}', f'{c.Q[n][0]:.1f}점', c.RAW[n][4])
        h.append(sec('sol', '해설', fx(it.get('sol'))))
        h.append(sec('trap', '함정', fx(clean(wrong_html(it.get('wrong'))))))
        H.append(''.join(h) + '</div>')
    H.append('<h2>서답형</h2>')
    for s, lab in (('S1', '서답 1'), ('S2', '서답 2')):
        it = dict(c.SITEMS[s])
        subs = it.get('subs') or []
        it['after'] = (it.get('after') or '') + ''.join(f'<div class="qb">({i + 1}) {q} <span style="color:#6b7a8c;font-size:8pt">[{p}]</span></div>' for i, (q, p) in enumerate(subs))
        h = card(lab, it, None, '해설 참조', '10점', it.get('src'))
        sol = it.get('sol') or it.get('rubric')
        sol = '<br>'.join(map(str, sol)) if isinstance(sol, (list, tuple)) else str(sol or '')
        h.append(sec('sol', '해설', fx(sol)))
        if it.get('rubric') and it.get('sol'):
            rb = it['rubric']; rb = rb if isinstance(rb, (list, tuple)) else [rb]
            h.append(sec('sol', '채점', '<table class="rub">' + ''.join(f'<tr><td>{fx(r)}</td></tr>' for r in rb) + '</table>'))
        h.append(sec('trap', '함정', fx(clean(wrong_html(it.get('wrong'))))))
        H.append(''.join(h) + '</div>')
    H.append('</body></html>')
    src = os.path.join(rdir, 'haeseol_src.html')
    doc = ''.join(H)
    open(src, 'w').write(fx(doc))
    subprocess.run(['node', os.path.join(HERE, 'haeseol.js'), src, out, f'미적분Ⅰ 기말 모의고사 {name} 해설'], check=True)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
