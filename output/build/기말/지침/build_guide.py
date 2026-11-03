# -*- coding: utf-8 -*-
"""기말 출제 지침서: front.md(번호대·기법·단원·운영) + 문항별 지침(analysis.json) → PDF"""
import os, sys, json, html, re, subprocess, collections, importlib.util
import markdown
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get('FONTS', '/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/fonts')
NODE = os.environ.get('NODE_MODULES', '/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/node_modules')
WB = os.path.join(HERE, '..', '..', '부교재_기말')
A = json.load(open(os.path.join(HERE, 'analysis.json')))
L = json.load(open(os.path.join(HERE, 'livestats.json')))
meta = json.load(open(os.path.join(WB, 'meta.json')))
spec = importlib.util.spec_from_file_location('itf', os.path.join(WB, 'items_final.py'))
m = importlib.util.module_from_spec(spec); sys.path.insert(0, WB); spec.loader.exec_module(m)
E = lambda s: html.escape(str(s or ''))
CH = {'D': '04 도함수의 활용(1)', 'M': '05 도함수의 활용(2)', 'I': '06 부정적분과 정적분', 'J': '07 정적분의 활용'}
TC = {'구조 변경': '#c0392b', '역문제화': '#8e44ad', '소재 결합': '#2c6fb7', '조건 변경': '#16805b', '함수 교체': '#b7701b',
      '구하는 대상 변경': '#555', '함정 추가': '#a33f7a', '형식 변경': '#6b6b2a', '그래프·표 제시': '#3a7a8a'}
LV = {'하': 1, '중': 2, '중상': 3, '상': 4, '최상': 5}

def short(i):  # GEN1-01-005 → G1-005, LIVE2-03-176 → L2-176
    mm = re.match(r'(GEN|LIVE)(\d)-\d\d-(\d+)', i)
    return f"{'G' if mm.group(1) == 'GEN' else 'L'}{mm.group(2)}-{mm.group(3)}" if mm else i

def slots_str(k):
    s = L.get(k)
    if not s: return '라이브 없음'
    c = collections.Counter('1–6' if v <= 6 else '7–12' if v <= 12 else '13–16' if v <= 16 else '17+' for v in s['slots'])
    parts = ' · '.join(f'{b} {c[b]}' for b in ('1–6', '7–12', '13–16', '17+') if c[b])
    return f"라이브 {s['n']}회 ({parts}{' · 서답 ' + str(s['seo']) if s['seo'] else ''})"

def card(k):
    a = A[k]; g = a.get('exam_guide', {}); mt = meta.get(k, ['', '', '', '']); d = m.D.get(k)
    stag = '<span class="stg">분석집</span>' if a.get('study') else ''
    head = (f'<div class="kh"><span class="key">{k}</span>{stag}<span class="sec">{E(mt[3])}</span>'
            f'<span class="src">{E(mt[1])}</span><span class="dif">난도 {E(mt[2])}</span></div>')
    info = (f'<div class="inf"><span>{E(slots_str(k))}</span><span>추천 <b>{E(g.get("slot"))}</b></span>'
            f'<span>수준 <b>{E(g.get("level"))}</b></span></div>')
    core = f'<div class="core">{E(a.get("original_core"))}</div>'
    if a.get('calc_only'):
        rec = g.get('recipes') or []
        return (f'<div class="card calc">{head}{info}{core}<div class="cn">단순 계산형: 숫자 변형으로 충분 (변형 분석 생략)'
                + (f' · {E(rec[0])}' if rec else '') + '</div></div>')
    rows = ''.join(f'<tr><td class="t" style="color:{TC.get(e.get("type"), "#333")}">{E(e.get("type"))}</td><td class="l">{E(e.get("element"))}'
                   f'<div class="why">{E(e.get("why"))}</div></td><td class="ef">{E(e.get("effect"))}</td>'
                   f'<td class="ids">{E(" ".join(short(i) for i in (e.get("ids") or [])))}</td></tr>'
                   for e in a.get('variant_elements', []))
    tab = f'<table class="ve"><tr><th>변형</th><th>내용</th><th>효과</th><th>자료</th></tr>{rows}</table>' if rows else ''
    no = a.get('number_only_ids') or []
    nos = f'<div class="no">숫자만 바꾼 변형 {len(no)}개 (분석 생략)</div>' if no else ''
    lp = f'<div class="lp"><span class="lb">라이브 경향</span>{E(a.get("live_pattern"))}</div>' if a.get('live_pattern') else ''
    li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs or [])
    st = a.get('study')
    marks = {r.get('i'): r.get('overlap') for r in (st or {}).get('recipes', [])}
    MK = {'same': '<span class="mk s">분석집과 같음</span>', 'direction': '<span class="mk d">분석집 방향</span>'}
    rec = ''.join(f'<li>{E(x)}{MK.get(marks.get(i), "")}</li>' for i, x in enumerate(g.get('recipes') or []))
    if st and st.get('extra_recipe'):
        rec += f'<li class="ex">{E(st["extra_recipe"])}<span class="mk n">분석집 대비 추가</span></li>'
    rec = f'<div class="bx rec"><div class="lb">새 변형 레시피</div><ol>{rec}</ol></div>'
    tr = f'<div class="bx"><div class="lb">함정</div><ul>{li(g.get("traps"))}</ul></div>' if g.get('traps') else ''
    av = f'<div class="bx av"><div class="lb">겹치면 안 되는 기존 변형</div><ul>{li(g.get("avoid"))}</ul></div>' if g.get('avoid') else ''
    sb = ''
    if st:
        dirs = ''.join(f'<li>{E(x)}</li>' for x in st.get('directions', []))
        sb = (f'<div class="bx sb"><div class="lb">분석집 (학생 공부 자료)</div>'
              f'<div><span class="k2">학생이 아는 판정</span>{E(st.get("known") or st.get("note_core"))}</div>'
              f'<div><span class="k2">분석집 변형 방향</span><ul>{dirs}</ul></div></div>')
    return f'<div class="card">{head}{info}{core}{tab}{nos}{lp}{sb}{rec}<div class="two">{tr}{av}</div></div>'

def main(out):
    front = open(os.path.join(HERE, 'front.md')).read()
    fh = markdown.markdown(front, extensions=['tables'])
    order = sorted(A, key=lambda k: ('DMIJ'.index(k[0]), int(k[1:])))
    # 요약표: 라이브 빈출 상위 30
    top = sorted(order, key=lambda k: -(L.get(k, {}).get('n', 0)))[:30]
    toprows = ''.join(f'<tr><td>{k}</td><td class="l">{E(meta.get(k, ["", "", "", ""])[3])}</td><td>{L[k]["n"]}</td>'
                      f'<td>{E(" ".join(map(str, L[k]["slots"])))}</td><td>{E(A[k]["exam_guide"].get("slot"))}</td><td>{E(A[k]["exam_guide"].get("level"))}</td></tr>' for k in top)
    toptab = f'<h2>부록 A. 라이브 빈출 원본 30</h2><table class="sum"><tr><th>원본</th><th>유형</th><th>라이브</th><th>실제 문항 번호</th><th>추천</th><th>수준</th></tr>{toprows}</table>'
    body = []
    cur = None
    for k in order:
        if k[0] != cur:
            cur = k[0]; body.append(f'<h2 class="pb">5. 문항별 지침 — {CH[cur]}</h2>')
        body.append(card(k))
    tc = collections.Counter(e.get('type') for a in A.values() for e in a.get('variant_elements', []))
    nkey = len(A); ncalc = sum(1 for a in A.values() if a.get('calc_only')); nrec = sum(len(a['exam_guide'].get('recipes') or []) for a in A.values())
    cover = (f'<div class="cover"><div class="tag">출제 지침서</div><h1>미적분Ⅰ 2학기 기말 · 부교재 변형 출제 지침</h1>'
             f'<div class="subt">일반 익스텐션 768문항 · 익스텐션 라이브(전국 학교 기출) 978문항 → 부교재 원본 {nkey}문항 전수 분석</div>'
             f'<div class="cards"><div><b>{nkey}</b>원본</div><div><b>1,746</b>변형 자료</div><div><b>{sum(tc.values())}</b>구조적 변형 요소</div>'
             f'<div><b>{nrec}</b>새 레시피</div><div><b>{ncalc}</b>단순 계산형</div></div>'
             f'<div class="legend">자료 표기: G1-005 = 일반 익스텐션 1권 5번, L2-176 = 익스텐션 라이브 2권 176번 · 효과 = 원본 대비 난도 변화</div></div>')
    css = open(os.path.join(HERE, 'guide.css')).read().replace('FONTS', 'file://' + FONTS)
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{cover}<div class="front">{fh}</div>{toptab}{"".join(body)}</body></html>'
    src = os.path.join(HERE, 'guide_src.html'); open(src, 'w').write(doc)
    js = f"""const {{chromium}}=require('{NODE}/playwright-core');(async()=>{{const b=await chromium.launch({{executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'}});const p=await b.newPage();
await p.goto('file://{src}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);
await p.pdf({{path:'{out}',format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;width:100%;text-align:center;color:#777"><span class=pageNumber></span> / <span class=totalPages></span></div>',margin:{{top:'12mm',bottom:'13mm',left:'11mm',right:'11mm'}}}});await b.close()}})();"""
    jp = os.path.join(HERE, '_render.js'); open(jp, 'w').write(js)
    subprocess.run(['node', jp], check=True); os.remove(jp); os.remove(src)

if __name__ == '__main__':
    main(sys.argv[1])
