# -*- coding: utf-8 -*-
"""견본 ↔ 부교재 원문 1:1 대응 · 변형 설명 PDF"""
import os, sys, re, json, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build3 import font_css, KATEX_CSS
import content3 as C
WB = '/home/user/Finale/output/build/부교재_기말'
sys.path.insert(0, WB); import items_final as F
A = json.load(open('/home/user/Finale/output/build/기말/지침/analysis.json'))
sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import dupcheck as DC
_DB = DC.load()
GRP = {'익스텐션 일반': [d for d in _DB if d['id'].startswith('GEN')], '라이브(학교 기출)': [d for d in _DB if d['id'].startswith('LIVE')], '분석집': [d for d in _DB if d['src'] == 'STUDY']}
def _txt(it):
    return (it['body'] + ''.join(v for _, v in (it.get('cond') or [])) + ''.join(v for _, v in (it.get('bogi') or [])) + (it.get('after') or '')
            + ''.join(q[0] for q in it.get('subs', [])) + ''.join('|' + str(c) for c in (it.get('choices') or [])))
def _lab(ck):
    return '숫자만 다름' if ck >= 0.85 else ('구조 유사' if ck >= 0.60 else '다름')
def nearest(it):
    out = {}
    for g, D in GRP.items():
        ck, cr, d, same = DC.score(_txt(it), D, 1)[0]
        out[g] = (ck, cr, d)
    return out
def near_html(nr):
    return ' · '.join(f'{g} <b>{E(d["hdr"])}</b> 골격 {ck:.2f}({_lab(ck)})' for g, (ck, cr, d) in nr.items())
CIRC = '①②③④⑤'
LV = {1: '하', 2: '하', 3: '하', 4: '중하', 5: '중', 6: '중상', 7: '상', 8: '최상', 9: '최상'}
FIGDIR = os.path.join(WB, 'parts')
E = html.escape
fix = lambda s: re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), s)

def chs(ch, ans=None):
    if not ch: return ''
    out = []
    for i, c in enumerate(ch, 1):
        t = c[2:] if c.startswith('T:') else f'\\({c}\\)'
        out.append(f'<span class="c{" ok" if ans == i else ""}">{CIRC[i-1]} {t}</span>')
    return '<div class="chs">' + ''.join(out) + '</div>'

def orig(key):
    body, ch, ans, src = F.I[key]
    body = body.replace('src="fig_', f'src="file://{FIGDIR}/fig_')
    a = None
    if isinstance(ans, str) and ans and ans[0] in CIRC: a = CIRC.index(ans[0]) + 1
    ans_t = '' if a else f'<div class="oa">정답 {E(str(ans))}</div>'
    return body + chs(ch, a) + ans_t

def card(no, key, mine, var, lv_new, sol, wrong, ansmark, src='', fast='', note='', near=''):
    a = A[key]; d = F.D[key]
    if src.startswith('학교 자체'):
        return self_card(no, key, mine, var, lv_new, sol, wrong, ansmark, src, fast, near)
    return f'''<div class="card"><div class="hd"><span class="no">{no}</span><span class="k">원본 {key}</span><span class="s">{E(F.I[key][3])} · {E(d[1])}</span>
<span class="lv">난도 {LV[d[0]]} → {lv_new}</span></div>
<div class="two"><div class="col"><div class="lab">부교재 원문</div>{orig(key)}</div><div class="col"><div class="lab">견본 {no}{ansmark}</div>{mine}</div></div>
<table class="ex"><tr><th>원본 핵심</th><td>{E(a["original_core"])}</td></tr>
<tr><th>변형 내용</th><td>{var}</td></tr><tr><th>견본 풀이</th><td>{sol}</td></tr>{f"<tr><th>빠른 풀이</th><td>{fast}</td></tr>" if fast else ""}{f"<tr><th>원본 대비</th><td>{note}</td></tr>" if note else ""}{f"<tr><th>오답 설계</th><td>{wrong}</td></tr>" if wrong else ""}{f"<tr><th>자료 대조</th><td>{near}</td></tr>" if near else ""}</table></div>'''

def self_card(no, key, mine, var, lv_new, sol, wrong, ansmark, src, fast='', near=''):
    return f'''<div class="card"><div class="hd"><span class="no">{no}</span><span class="k">학교 자체 출제</span><span class="s">가장 가까운 유형 {key} · {E(F.I[key][3])}</span>
<span class="lv">난도 {lv_new}</span></div>
<div class="two"><div class="col"><div class="lab">가장 가까운 부교재 유형 ({key})</div>{orig(key)}</div><div class="col"><div class="lab">견본 {no}{ansmark}</div>{mine}</div></div>
<table class="ex"><tr><th>자체 설계</th><td>{var}</td></tr><tr><th>견본 풀이</th><td>{sol}</td></tr>{f"<tr><th>빠른 풀이</th><td>{fast}</td></tr>" if fast else ""}{f"<tr><th>오답 설계</th><td>{wrong}</td></tr>" if wrong else ""}{f"<tr><th>자료 대조</th><td>{near}</td></tr>" if near else ""}</table></div>'''

def build(out):
    cards = []; NR = {}
    for n, r in sorted(C.RAW.items()):
        it = C.ITEMS[n]; NR[str(n)] = nr = nearest(it)
        mine = r[0] + chs(r[1], r[2])
        cards.append(card(f'{n}번', r[3], mine, it['var'], it['level'], it['sol'], it['wrong'], f' · 정답 {CIRC[r[2]-1]}', it['src'], it.get('fast') or '', it.get('note') or '', near_html(nr)))
    for s, lab in (('S1', '서답형 1'), ('S2', '서답형 2')):
        it = C.SITEMS[s]; NR[s] = nr = nearest(it)
        body = getattr(C, s) + ''.join(f'<div class="sub">({i}) {q[0]} <span class="pt">[{q[1]}]</span></div>' for i, q in enumerate(it['subs'], 1))
        sol = '<br>'.join(it['rubric'])
        cards.append(card(lab, it['key'], body, it['var'], it['level'], sol, it.get('wrong', ''), ' · 정답 ' + ' / '.join(it['ans']), it['src'], it.get('fast') or '', it.get('note') or '', near_html(nr)))
    def kind(r_src, key):
        if r_src.startswith('학교 자체'): return '학교 자체'
        m = json.load(open(os.path.join(WB, 'meta.json')))[key][3]
        return 'Level Up' if 'Level Up' in m else ('평가원' if ('평가원' in m or '대표기출' in m) else 'EBS 유형')
    rows = [(f'{n}', C.RAW[n][3], kind(C.RAW[n][4], C.RAW[n][3])) for n in sorted(C.RAW)] + [(s, C.SITEMS[s]['key'], kind(C.SITEMS[s]['src'], C.SITEMS[s]['key'])) for s in ('S1', 'S2')]
    import collections as _co
    cnt = _co.Counter(k for *_, k in rows)
    SUMMARY = ('<table class="sum"><tr><th>번호</th>' + ''.join(f'<td>{n.replace("S", "서")}</td>' for n, _, _ in rows) + '</tr><tr><th>원본</th>' + ''.join(f'<td>{k}</td>' for _, k, _ in rows) +
               '</tr><tr><th>출처</th>' + ''.join(f'<td class="k{"PELS"[["평가원","EBS 유형","Level Up","학교 자체"].index(t)]}">{t.replace(" 유형","").replace("학교 ","")}</td>' for *_, t in rows) + '</tr></table>'
               + '<div class="sub0">' + ' · '.join(f'{t} {cnt[t]}' for t in ('평가원', 'EBS 유형', 'Level Up', '학교 자체')) + '</div>')
    LV_ROWS = sorted(NR.items(), key=lambda kv: -kv[1]['라이브(학교 기출)'][0])
    hi = [(n, v['라이브(학교 기출)']) for n, v in LV_ROWS if v['라이브(학교 기출)'][0] >= 0.60]
    nm = lambda n: n.replace('S', '서답형') if n.startswith('S') else n + '번'
    LIVE_T = ('<div class="lv0"><div class="lab">익스텐션 라이브(전국 학교 기출) 대조</div>'
              '<p>라이브 문항을 그대로 가져온 것은 없다(동일 문항 0). 문항별로 가장 가까운 라이브 문항과의 골격 유사도(숫자를 지운 문장 틀의 겹침)를 쟀다. '
              '0.85 이상은 그 학교 기출과 틀이 같고 숫자만 다른 것, 0.60–0.85는 구조가 닮은 것이다. 숫자만 다른 출제는 1–16번에서 허용, 17·18·서답형2는 0.60 미만이어야 한다.</p>'
              '<table class="lt"><tr><th>번호</th><th>원본</th><th>가장 가까운 라이브</th><th>골격</th><th>원문</th><th>판정</th></tr>'
              + ''.join(f'<tr class="{"h" if v["라이브(학교 기출)"][0] >= 0.85 else ("m" if v["라이브(학교 기출)"][0] >= 0.60 else "")}"><td>{nm(n)}</td><td>{(C.ITEMS[int(n)]["key"] if n.isdigit() else C.SITEMS[n]["key"])}</td><td>{E(v["라이브(학교 기출)"][2]["hdr"])}</td><td>{v["라이브(학교 기출)"][0]:.2f}</td><td>{v["라이브(학교 기출)"][1]:.2f}</td><td>{_lab(v["라이브(학교 기출)"][0])}</td></tr>' for n, v in LV_ROWS)
              + '</table><p>' + ('라이브와 틀이 같거나 닮은 문항: ' + ', '.join(f'{nm(n)}({E(d["hdr"].split(" · ")[0])} 골격 {ck:.2f})' for n, (ck, cr, d) in hi)
              + '. 모두 원문이 단순한 1–13번이라 숫자만 바꾸면 학교 기출과 겹치기 쉬운 자리다. ' if hi else '') + '17·18·서답형2는 라이브와 모두 0.60 미만이다.</p></div>')
    # 17·18 관문·후보 경쟁 (지침 0-4 설계 카드): review/*.json + 블라인드 측정 result.json
    import json as _js, glob
    RV = os.environ.get('REVIEW_DIR', os.path.join(HERE, 'review'))
    MS = os.environ.get('MEASURE_DIR', '/home/user/Finale/output/build/기말/공동출제/풀이')
    meas = {}
    for f in sorted(glob.glob(os.path.join(MS, os.environ.get('MEASURE_GLOB', '측정_3회*'), 'result.json'))):   # 나중 측정이 앞 측정을 덮음
        for n, tag, t, d, bt, bd in _js.load(open(f))['rows']: meas[n] = (d, bd, t, bt)
    chosen = {str(n): it.get('cand') for n, it in list(C.ITEMS.items()) + list(C.SITEMS.items()) if it.get('cand')}
    GR = []
    for f in sorted(glob.glob(os.path.join(RV, '*.json'))):
        c = os.path.basename(f)[:-5]
        if not re.fullmatch(r'(claudeB|claude|codex|draft)(\d+|S2)', c): continue
        R = _js.load(open(f)); n = c[-2:] if c.endswith('S2') else int(re.sub(r'\D', '', c))
        who = {'claude': 'Claude A팀', 'claudeB': 'Claude B팀', 'codex': 'Codex', 'draft': '이전 초안(대조군)'}[re.sub(r'(\d+|S2)$', '', c)]
        ct = R.get('core_test', {}); sp = lambda v: ('불통' if str(v).lstrip().startswith('불통') else '변형 통' if str(v).lstrip().startswith('변형') else ('통' if str(v).lstrip().startswith('통') else '—'))
        pick = chosen.get(str(n)) == c
        m = meas.get(20 if n == 'S2' else n) if pick else None
        mtxt = f'체감 {m[0]:.1f} (학교 {m[1]:.1f}, {m[0]-m[1]:+.1f}) · {m[2]:.1f}분' if m else '—'
        why = R.get('short') or ('채택' if pick else '')
        GR.append((n, not pick, f'<tr class="{"ok" if pick else ""}"><td>{"서답형2" if n == "S2" else str(n) + "번"}</td><td>{who}</td><td>{str(R.get("axis", ""))[:1] if str(R.get("axis", ""))[:1] in "①②" else "숫자 변형"}</td><td>{sp(ct.get("setting"))} / {sp(ct.get("principle"))}</td>'
                  f'<td>{R.get("d_step")}</td><td>{E(R.get("pattern_short", "없음"))}</td><td>{R.get("verdict")}</td><td>{mtxt}</td><td>{E(why)}</td></tr>'))
    GATE_T = ('' if not GR else '<div class="lv0"><div class="lab">17·18번 관문과 후보 경쟁 (지침 0-4 설계 카드)</div>'
              '<p>관문 순서: 중복·정답·조건 빼 보기 → 흔한 패턴(patterns.py) → 독립 검토(원문 핵심 한 줄이 변형에서 통하는지, d_step 0.75 이상) → 앵커(학교 8·12·17·18)를 섞은 블라인드 측정 → 형식·말투. '
              '17·18·서답형2는 여러 출제자가 후보를 하나씩 내고, 출제에 참여하지 않은 검토자가 출제자 이름을 가린 채 골랐다.</p>'
              '<table class="lt gt"><tr><th>번호</th><th>후보</th><th>축</th><th>설정 줄 / 원리 줄</th><th>d_step</th><th>흔한 패턴</th><th>검토</th><th>측정(앵커 보정)</th><th>비고</th></tr>'
              + ''.join(r for *_, r in sorted(GR, key=lambda z: (99 if z[0] == 'S2' else z[0], z[1]))) + '</table><p>①형(17번)은 원문 원리 줄이, ②형(18번)은 원문 설정 줄이 \'불통\'이어야 통과다. 측정은 관문 3을 통과한 후보만 했다. 학교 같은 번호와의 차가 ±1.5 안이면 통과다.</p></div>')
    # 같은 번호 두 벌(Claude B팀·Codex) 비교 선택 (review/compare*.json, map.json)
    PK = []
    mp = os.path.join(RV, 'map.json')
    if os.path.exists(mp):
        M = _js.load(open(mp))
        for f in sorted(glob.glob(os.path.join(RV, 'compare*.json'))):
            for n, d in _js.load(open(f)).items():
                lab = M.get(n, {}); pick = d.get('pick', '')
                other = [k for k in lab if k != pick]
                PK.append((int(n), f'<tr><td>{n}번</td><td>{E(lab.get(pick, pick))}</td><td>{E(lab.get(other[0], "")) if other else ""}</td><td>{E(str(d.get("reason", ""))[:140])}</td></tr>'))
    PICK_T = ('' if not PK else '<div class="lv0"><div class="lab">같은 번호 두 벌 비교 (Claude B팀 · Codex)</div>'
              '<p>Codex가 사용 한도 초과로 멈춘 동안 Claude B팀이 같은 번호를 냈고, 새 키로 Codex가 다시 낸 뒤 출제자 이름을 가린 검토자가 번호마다 하나를 골랐다.</p>'
              '<table class="lt gt"><tr><th>번호</th><th>채택</th><th>탈락</th><th>이유</th></tr>' + ''.join(r for _, r in sorted(PK)) + '</table></div>')
    css = r"""@page{size:A4;margin:11mm 10mm 12mm}
body{font-family:'HB','MJ';font-size:8.8pt;line-height:1.55;margin:0;color:#111}
.katex{font-size:1.02em;font-family:'TN','KaTeX_Main'}
.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
.katex .text,.katex .text *{font-family:'HB','MJ','TN'!important;font-style:normal}
h1{font-family:'GL';font-weight:400;font-size:15pt;text-align:center;margin:0 0 1mm}
.sub0{text-align:center;font-family:'GL';font-size:8.5pt;color:#555;margin-bottom:4mm}
.card{border:.8pt solid #333;margin:0 0 4mm;break-inside:avoid}
.hd{display:flex;gap:6pt;align-items:baseline;background:#eef0f3;border-bottom:.6pt solid #333;padding:2pt 5pt;font-family:'GL'}
.no{background:#111;color:#fff;padding:0 5pt;font-size:10pt}.k{font-size:9pt}.s{flex:1;font-size:7.8pt;color:#444}.lv{font-size:8pt;color:#c0392b}
.two{display:grid;grid-template-columns:1fr 1fr}
.col{padding:4pt 6pt;min-width:0}.col+.col{border-left:.6pt solid #999}
.lab{font-family:'GL';font-size:7.8pt;color:#1f4e9a;margin-bottom:2pt}
.chs{display:flex;flex-wrap:wrap;gap:2pt 12pt;margin-top:3pt}.c.ok{color:#c0392b}
.oa{font-family:'GL';font-size:8pt;color:#c0392b;margin-top:2pt}
.cond{border:.6pt solid #000;padding:2pt 5pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}.ck{margin-right:3pt}
fieldset.bogi{border:.6pt solid #000;margin:3pt 0;padding:2pt 6pt;min-inline-size:0}fieldset.bogi legend{font-size:8pt;padding:0 4pt}
.bi{display:block;padding-left:1.4em;text-indent:-1.4em}.bk{margin-right:3pt}.fig{text-align:center;margin:3pt 0}.fig img{max-width:100%}
.dm{text-align:center;margin:2pt 0}.sub{margin-top:2pt}.pt{font-size:7.5pt;color:#555}
table.ex{border-collapse:collapse;width:100%;border-top:.6pt solid #333}
.ex th{width:17mm;font-family:'GL';font-weight:400;font-size:7.8pt;background:#fafafa;border:.4pt solid #bbb;padding:2pt 4pt;text-align:left;vertical-align:top}
.ex td{border:.4pt solid #bbb;padding:2pt 5pt;font-size:8.2pt}
table.lt{border-collapse:collapse;width:100%;margin:2pt 0}.lt th,.lt td{border:.4pt solid #aaa;font-size:7.4pt;padding:1pt 3pt;text-align:left}.lt th{font-family:'GL';font-weight:400;background:#eef0f3}.lt tr.h td{background:#fde8e4}.lt tr.m td{background:#fff6dd}
.lv0{border:.6pt solid #999;padding:3pt 6pt;margin:0 0 4mm}.lt tr.ok td{background:#e8f4ea}.gt td:nth-child(-n+8),.gt th{white-space:nowrap}.gt td:last-child{white-space:normal}.lv0 p{margin:2pt 0;font-size:8pt}
table.sum{border-collapse:collapse;width:100%;margin:0 0 1mm}.sum th,.sum td{border:.5pt solid #999;font-size:7pt;padding:1pt 1pt;text-align:center;font-family:'GL';font-weight:400}.sum th{background:#eef0f3;width:9mm}.kP{color:#c0392b}.kL{color:#1f4fd6}.kS{color:#7b3fb0}.kE{color:#555}
"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{css}</style></head><body>'
         '<h1>미적분Ⅰ 기말 3회 · 부교재 원문 1:1 대응과 변형 설명</h1>'
         '<div class="sub0">왼쪽 부교재 원문, 오른쪽 견본 문항 · 빨간 번호 = 정답 · 17·18·서답형2는 구조 변경 · 2학기 중간 출처 배치: 평가원 6 · EBS 6 · Level Up 6 · 자체 2</div>' + SUMMARY + LIVE_T + GATE_T + PICK_T
         + ''.join(cards) + '</body></html>')
    # 렌더러의 display 수식 측정은 시험지 쪽(.pg) 전용이라 가운데 정렬 인라인 수식으로 바꿈
    h = re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div class="dm">\\(\\displaystyle ' + m.group(1) + '\\)</div>', h)
    src = os.path.join(HERE, 'cmp_src.html'); open(src, 'w').write(fix(h))
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'cmp_src.html', 'cmp_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'cmp_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
