# -*- coding: utf-8 -*-
"""원본 시험지 PDF(양정고 양식)의 벡터 페이지를 그대로 바탕으로 쓰고,
결재란 제거 · 머리글 일부 수정 · 본문 교체로 새 시험지 PDF를 만든다."""
import os, re, json, subprocess, sys
import pymupdf
from content3 import Q, ANS, S1, S1S, S2, S2S, CHW, CHM

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
    ([('Q1', 328.5), ('Q2', 530.0)], [('Q3', TOP), ('Q4', 433.2)]),
    ([('Q5', TOP), ('Q6', 434.4)], [('Q7', TOP), ('Q8', 437.0)]),
    ([('Q9', TOP)], [('Q10', TOP)]),
    ([('Q11', TOP)], [('Q12', TOP)]),
    ([('Q13', TOP)], [('Q14', TOP)]),
    ([('Q15', TOP)], [('Q16', TOP)]),
    ([('Q17', TOP)], [('Q18', TOP)]),
    ([('SEC1', TOP), ('S1', None)], [('S2', TOP), ('END', 693.7)]),
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
.katex{font-size:1.0em;margin:0 1.6pt;white-space:nowrap}
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
.cond{border:.6pt solid #000;padding:2pt 6pt 2pt 6pt;margin:4pt 0 4pt 0;clear:both;text-align:left;line-height:1.5}
.nw{white-space:nowrap}
.ci{display:flex;align-items:baseline;margin:0}.ci .ck{flex:none;width:22.4pt}.cit{flex:1;min-width:0;text-align:justify}.cond>div:not(.ci){text-align:justify}
.bit{flex:1;min-width:0;text-align:justify}
.bogi{min-inline-size:0;border:.6pt solid #000;margin:4pt 0 4pt 0;padding:1pt 6pt 4pt;clear:both}
.bogi legend{margin:0 auto;padding:0 3pt;font-family:'HB';font-size:9pt;line-height:1}
.bogi{line-height:1.62;padding-top:3pt!important}.bit.br{white-space:normal!important;overflow:visible!important;text-align:left}
.bi{display:flex;gap:3pt;margin:1pt 0;text-align:left;align-items:baseline}.bi .bk{flex:none}
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
.endx .a{font-family:'HB','FS';font-size:23pt;line-height:28pt;letter-spacing:-1.1pt;white-space:nowrap;-webkit-text-stroke:.32pt #000;transform:translateX(-3.4pt)}
.endx .em{font-size:19.8pt;margin-left:10.4pt}
.endx .b{font-family:'HB';font-size:14pt;line-height:19.4pt;letter-spacing:-.9pt;word-spacing:.9pt;-webkit-text-stroke:.14pt #000}
.end .a{font-size:24pt;letter-spacing:1pt}
.end .b{font-size:14pt;line-height:1.75;margin-top:6pt}
.tot{text-align:right}
"""

_BLK = re.compile(r'\\\]|</div>|<div[^>]*>|</fieldset>|<fieldset[^>]*>|<legend>.*?</legend>|<br>')

try:   # 줄별 너비(pt): 원본 스캔에서 그 줄의 오른쪽 끝을 재어 만든 값 (measure_jl.py)
    JLW = json.load(open(os.path.join(HERE, 'jlw.json')))
except FileNotFoundError:
    JLW = {}

MEASURE = False   # True: 1차 렌더(어절 폭 측정용)
BREAKS = {}       # key -> 줄을 끊을 공백 위치(문자열 오프셋) 목록 (autobreak로 계산)
COLW = 251.5      # 줄 너비(pt) 기본값
WIDTH = {}        # key -> 그 문단의 실제 너비(pt) (측정값)
SHRINK = 0.6      # 줄에 다음 어절을 붙일 때 공백을 최대 이만큼 줄일 수 있음(0.6 = 원래 폭의 40%까지)
_TOK = re.compile(r'\\\([\s\S]+?\\\)|\\\[[\s\S]+?\\\]|<[^>]+>|⏎| ')

def spaces(h):
    """최상위(상자·그림 밖) 본문의 '끊을 수 있는 공백' 위치, 문단(run) 시작·끝 위치"""
    out, run, depth, inl = [], 0, 0, 0
    starts, ends = {0: 0}, {}
    for m in _TOK.finditer(h):
        t = m.group(0)
        if t.startswith('\\['):
            if depth == 0: ends[run] = m.start(); run += 1; starts[run] = m.end()
        elif t.startswith('<'):
            name = re.match(r'</?\s*(\w+)', t)
            name = name.group(1).lower() if name else ''
            if name in ('div', 'fieldset'):
                if t.startswith('</'):
                    depth -= 1
                    if depth == 0: run += 1; starts[run] = m.end()
                else:
                    if depth == 0: ends[run] = m.start()
                    depth += 1
            elif name == 'br':
                if depth == 0: ends[run] = m.start(); run += 1; starts[run] = m.end()
            elif name in ('span', 'u', 'b', 'i', 'sup', 'sub') and not t.endswith('/>'):
                inl += -1 if t.startswith('</') else 1
        elif t == ' ' and depth == 0 and inl == 0:
            out.append((run, m.start()))
    ends.setdefault(run, len(h))
    return out, starts, ends

def mark(h, key):
    sp, starts, ends = spaces(h)
    ins = {}
    for r, st in starts.items():
        ins.setdefault(st, []).append(f'<i class="mk" data-r="{key}#{r}" data-i="-1" data-t="s"></i>')
    for r, en in ends.items():
        ins.setdefault(en, []).insert(0, f'<i class="mk" data-r="{key}#{r}" data-i="-1" data-t="e"></i>')
    for n, (r, off) in enumerate(sp):
        if h[off + 1:].startswith('\\('):          # 수식 바로 앞 공백: 이 자리에서는 줄을 바꾸지 않음(줄이 수식으로 시작하지 않게)
            NOBRK.setdefault(key, set()).add(n)
        ins.setdefault(off, []).append(f'<i class="mk" data-r="{key}#{r}" data-i="{n}" data-t="b"></i>')
        ins.setdefault(off + 1, []).append(f'<i class="mk" data-r="{key}#{r}" data-i="{n}" data-t="a"></i>')
    out, last = [], 0
    for off in sorted(ins):
        out.append(h[last:off]); out.append(''.join(ins[off])); last = off
    out.append(h[last:])
    return ''.join(out)

def jl(h, key=''):
    """'⏎' = 줄바꿈 위치. 그 줄은 단 너비까지 양끝 맞춤(넘치면 낱말 간격을 줄임)."""
    if MEASURE:
        return mark(h, key)
    if key in BREAKS:
        sp, _, ends = spaces(h)
        ed = []
        for g in BREAKS[key]:
            if isinstance(g, tuple): ed.append((ends[g[1]], 'ins', None))
            else: ed.append((sp[g][1], 'rep', g))
        rag = [g in RAGGED.get(key, ()) for _, _, g in sorted(ed)]
        for off, how, _ in sorted(ed, reverse=True):
            h = h[:off] + '⏎' + h[off + (1 if how == 'rep' else 0):]
    else:
        rag = []
    parts = h.split('⏎')
    out = []
    for p in parts[:-1]:
        i = max([m.end() for m in _BLK.finditer(p)] or [0])
        k = f'{key}.{len(out)}'
        w = JLW.get(k) or (WIDTH.get(key, COLW) if key in BREAKS else None)
        if len(out) < len(rag) and rag[len(out)]: w = None
        st = (f'width:{w:.1f}pt;text-align-last:justify;' if w else '') + JLSTYLE.get(k, '')
        st = f' style="{st}"' if st else ''
        out.append(p[:i] + f'<span class="jl" data-id="{k}"{st}>{p[i:].lstrip()}</span>')
    return ''.join(out) + parts[-1]

RAG_PT = 2.5     # 공백 하나당 2.5pt 넘게 벌어질 줄은 양끝 맞춤하지 않고 오른쪽을 비움
RAGGED = {}
NOBRK = {}       # 키별: 줄을 바꾸면 안 되는 공백 번호(바로 뒤가 수식)

def autobreak(mk):
    """측정한 어절 폭으로 줄 끊을 위치 결정 (문단 전체 최적화).
    1) 줄 수를 가장 적게, 2) 그 안에서 줄마다 벌어지는 간격(공백 하나당 늘어나는 폭)의 제곱합이 최소가 되도록.
    다음 어절은 공백을 원래 폭의 (1-SHRINK)까지 줄여서라도 들어가면 앞줄에 붙일 수 있음."""
    from collections import defaultdict
    R = defaultdict(lambda: {'s': None, 'e': None, 'b': {}, 'a': {}})
    for m in mk:
        d = R[m['r']]
        if m['t'] in 'se':
            d[m['t']] = m['x']
            if m['t'] == 's' and m.get('w'): d['w'] = m['w']
        else: d[m['t']][m['i']] = m['x']
    br = defaultdict(list)
    INF = float('inf')
    for rk, d in R.items():
        key = rk.split('#')[0]
        gaps = sorted(d['b'])
        if not gaps or d['s'] is None or d['e'] is None: continue
        W = d.get('w') or COLW; WIDTH[key] = W
        # 어절 k의 [시작, 끝]: 0번은 run 시작~첫 공백, k번은 공백 k-1 뒤~공백 k 앞(마지막은 run 끝)
        st = [d['s']] + [d['a'][g] for g in gaps]
        en = [d['b'][g] for g in gaps] + [d['e']]
        sp = [d['a'][g] - d['b'][g] for g in gaps]
        n = len(st)
        def cost(i, j, last):     # 어절 i..j 한 줄
            nat = en[j] - st[i]; S = sum(sp[i:j]); k = j - i
            if nat - SHRINK * S > W: return INF
            if last and nat <= W: return 0.0
            adj = W - nat
            if k == 0: return 1e4 if adj > 40 else (adj / 4) ** 2
            per = adj / k
            return (per ** 2) if per >= 0 else (per ** 2) * 0.5
        nob = NOBRK.get(key, set())
        for strict in (True, False):           # 먼저 '수식 앞에서 끊지 않기'를 지켜 보고, 불가능할 때만 풂
            best = [(INF, INF, -1)] * (n + 1)   # (줄 수, 비용, 앞 끊는 위치)
            best[0] = (0, 0.0, -1)
            for j in range(1, n + 1):
                for i in range(j - 1, -1, -1):
                    if en[j - 1] - st[i] > W * 2.2: break
                    if strict and i > 0 and gaps[i - 1] in nob: continue
                    c = cost(i, j - 1, j == n)
                    if c == INF or best[i][0] == INF: continue
                    cand = (best[i][0] + 1, best[i][1] + c, i)
                    if cand[:2] < best[j][:2]: best[j] = cand
            if best[n][0] != INF: break
        cuts, j = [], n
        while j > 0:
            i = best[j][2]
            if i > 0: cuts.append(gaps[i - 1])   # 어절 i 앞의 공백에서 줄바꿈
            if j < n:                            # 어절 i..j-1 줄(마지막 줄 제외)이 너무 벌어지면 왼쪽 정렬
                k = j - 1 - i; adj = W - (en[j - 1] - st[i])
                if k == 0 or adj / k > RAG_PT: RAGGED.setdefault(key, set()).add(gaps[j - 1])
            j = i
        br[key] += sorted(cuts)
        li = best[n][2]                          # 마지막 줄이 단보다 넓으면(공백을 줄여야 들어가면) 그 줄도 압축 대상으로
        if en[n - 1] - st[li] > W:
            br[key].append(('E', int(rk.split('#')[1])))
    return br

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

def _match_close(h, i, tag):
    """h[i:]가 <tag ...>로 시작할 때, 짝이 맞는 </tag>의 시작 위치"""
    d = 0
    for m in re.finditer(rf'<(/?){tag}\b[^>]*>', h[i:]):
        d += -1 if m.group(1) else 1
        if d == 0: return i + m.start()
    return len(h)

def boxes(h, key):
    """조건 상자 (가)(나)…·보기 ㄱㄴㄷ 안의 글도 본문처럼 줄바꿈 계산·양끝 맞춤"""
    out, i, n = [], 0, 0
    pat = re.compile(r'<div class="ci"><span class="ck">[^<]*</span>|<div class="cond">\s*<div>|(?<=</div>)<div>(?=[^<]*?[가-힣])|<div class="bi"><span class="bk">[^<]*</span><span>')
    while True:
        m = pat.search(h, i)
        if not m: out.append(h[i:]); break
        t = m.group(0)
        if t.endswith('<span>'):          # 보기 항목
            a = m.end(); b = _match_close(h, a - 6, 'span')
            # 실제 시험지(2025 2학기 중간 9번·기말 12번): 보기 항목은 양끝 맞춤 없이 왼쪽 정렬, 낱말 간격은 본문 그대로(줄이지 않음)
            out.append(h[i:a - 6] + '<div class="bit br">' + h[a:b] + '</div>'); i = b + 7
        elif t.startswith('<div class="ci">'):
            a = m.end(); b = _match_close(h, m.start(), 'div')
            out.append(h[i:a] + '<div class="cit">' + jl(h[a:b], f'{key}.c{n}') + '</div>')
            i = b
        else:                              # 이름표 없는 상자 줄
            a = m.end(); b = _match_close(h, a - 5, 'div')
            out.append(h[i:a] + jl(h[a:b], f'{key}.c{n}')); i = b
        n += 1
    return ''.join(out)

def q_html(n):
    pt, body, ch = Q[n]
    body = dpad(body, f'Q{n}')
    if n in CONDST: body = body.replace('<div class="cond">', f'<div class="cond" style="{CONDST[n]}">')
    body = body.replace('{PTR}', f'<div class="ptr">[{pt:.1f}점]</div>')
    body = body.replace('⏎{PT}', f'⏎<span class="pt">[{pt:.1f}점]</span>')
    body = body.replace('{PT}', f' <span class="pt">[{pt:.1f}점]</span>')
    g = all(c.startswith('T:') for c in ch)
    w = CHW.get(n)
    chs = ''.join(f'<span{f" style=width:{w}pt" if w else ""}><span class="c">{CIRC[i]}</span> ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') + '</span>' for i, c in enumerate(ch))
    # 실제 시험지 보기 제목: 본문 명조로 '< 보   기 >'(꺾쇠 안쪽 한 칸, 보·기 사이 세 칸)
    body = body.replace('<legend>&lt;보 기&gt;</legend>', '<legend>&lt;<span style="padding:0 .55em">보<span style="display:inline-block;width:1.8em"></span>기</span>&gt;</legend>')
    body = boxes(body, f'Q{n}')
    F = 15.3 if n < 10 else 19.9   # 원본 PDF 실측: 번호 폭
    # 실제 시험지: 둘째 줄·조건 상자·선택지 모두 번호와 같은 왼쪽 선에서 시작 (들여쓰기 없음), 줄바꿈 위치도 원본과 동일
    return (f'<div class="q"><div class="qt">{jl(f"<span class=n style=width:{F}pt>{n}.</span>" + body, f"Q{n}")}</div>'
            f'<div class="ch{" g" if g else ""}"{f" style=margin-top:{CHM[n]}pt" if n in CHM else ""}>{chs}</div></div>')

def s_html2(head, body, subs):
    # 실제 시험지: '서답형 n' 제목 줄 → 발문 → (1)(2)… 소문항(들여쓰기 없음), 배점은 소문항 끝 [n점, …]
    if len(subs) == 1 and subs[0][1] is None:   # 소문항 없이 발문 끝에 배점
        body = body.rstrip() + f' <span class="pt">[{subs[0][0]}]</span>'; sh = ''
    elif len(subs) == 1:   # 단일 질문(2025 기말 서답 1형): (1) 없이 발문 뒤에 질문과 배점
        body = body.rstrip() + f' {subs[0][0]} <span class="pt">[{subs[0][1]}]</span>'; sh = ''
    else:
        sh = ''.join(f'<div class="sub">{jl(f"({i+1}) {t} [{p}]", f"{head}-{i+1}")}</div>' for i, (t, p) in enumerate(subs))
    c = 's1' if head.endswith('1') else 's2'
    body = boxes(body, head)
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
END = ('<div class="endx" style="top:0"><div class="a">수고하셨습니다<span class="em">(ᐢ.꒳.ᐢ)ꕤ</span></div>'
       '<div class="b" style="margin-top:5.6pt"><span style="position:relative;left:-.8pt">선택형 18문제 = 80점</span><br><span style="word-spacing:.3pt">서답형&nbsp;&nbsp;2문제 = 20점</span></div></div>')

def block(key):
    if key.startswith('Q'): return q_html(int(key[1:]))
    if key == 'S1': return s_html2('서답형 1', S1, S1S)
    if key == 'S2': return s_html2('서답형 2', S2, S2S)
    if key == 'SEC1': return SEC1
    if key == 'SEC2': return SEC2
    if key == 'END': return END

def nobreak(h):
    # 수식 안에서는 줄바꿈 금지(.katex nowrap), 수식 바로 뒤에 붙은 조사·문장부호(가, 라, 와, 의, ',', '.' 등)도 수식과 한 덩어리로 묶음
    return re.sub(r'(\\\((?:(?!\\\)).)+?\\\))([^\s<\\(]+)', r'<span class="nw">\1\2</span>', h)

MCSS = '.qt,.s1 .q,.s2 .q{white-space:nowrap}.qt .cond,.qt .bogi,.qt .fig{white-space:normal}.cit,.cond>div,.bit{white-space:nowrap;overflow:hidden}'

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
            f'<style>{font_css()}{CSS}{MCSS if MEASURE else ""}</style></head><body>{nobreak("".join(pages))}</body></html>')

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
P1_NOTE = [(293.0, '선택형 문제(1~18번)의 정답은 반드시'), (304.9, 'OMR카드에 컴퓨터용 사인펜으로 명확히 표기하시오.')]
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

FOOT_LOGO = pymupdf.Rect(244.6, 792, 262.6, 812)

def make_background():
    src = pymupdf.open(TPL)
    doc = pymupdf.open()
    doc.insert_pdf(src, from_page=0, to_page=7)
    for pn, page in enumerate(doc):
        repl = []   # (origin, text, size)
        # 1) 결재란·출제 정보 행 제거 (실제 배부용 시험지와 동일하게)
        top = pymupdf.Rect(0, 28, 595, 92.5)
        # 2) 제목 '1학년 공통수학1과 중간고사 문제' → '2학년 미적분Ⅰ과 중간고사 문제'
        page.add_redact_annot(pymupdf.Rect(84, 100, 400, 129), fill=(1, 1, 1))
        # 시행일
        for r, o, sz in find_chars(page, '7월 11일(토) - 1교시'):
            page.add_redact_annot(pymupdf.Rect(r.x0, r.y0, 562, r.y1), fill=(1, 1, 1)); repl.append((o, '12월 24일(목) - 1교시', sz))
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
            page.insert_text((x, INFO_Y), t, fontname='GL', fontsize=INFO_FS, render_mode=2, border_width=INFO_BW,
                             morph=(pymupdf.Point(x, INFO_Y), pymupdf.Matrix(INFO_SX, 1)))
        for o, t, sz in repl:
            page.insert_text(o, t, fontname='GL', fontsize=sz, render_mode=2, border_width=0.02)
        if pn == 0:
            redraw_p1_head(page, gl)
        # 꼬리말 동그라미 '고': 최신 PyMuPDF는 redaction 뒤 이 글자를 가늘게 다시 그리므로 원본 양식에서 그대로 옮겨 붙임
        page.draw_rect(FOOT_LOGO, color=None, fill=(1, 1, 1))
        page.show_pdf_page(FOOT_LOGO, src, pn, clip=FOOT_LOGO)
    return doc

TITLE = [(92.3, '2', 20.04), (106.46, '학년', 15.0), (143.8, '미적분Ⅰ', 23.0), (246.96, '과', 15.0),
         (269.3, '기말고사', 19.0), (347.45, ' 문제', 15.0)]
# 2026-11-07 학교 스캔과 픽셀 대조(기준: 가장 최근 2026-2 미적분Ⅰ 중간 2·4·6쪽 평균, 2026-1 중간과도 1px 안): 글자 높이 9.9pt·장평 90.5%(굴림 장평 줄임),
# 낱말마다 스캔의 시작 위치(본문 틀 기준)에 놓음, 획 굵기는 스캔 잉크 밀도(≈0.20)에 맞춤
INFO_Y, INFO_FS, INFO_BW, INFO_SX = 142.5, 9.9, 0.045, 0.905
INFO = [(65.99, '과'), (79.65, '정'), (93.08, ':'), (100.52, '('), (108.41, '2022'), (133.82, '개정'), (156.24, '교육과정'), (196.8, ')'), (222.52, '과목코드'), (262.92, ':'), (270.43, '('), (278.24, '09'), (293.12, ')'), (318.62, '이수단위'), (358.98, ':'), (366.4, '('), (373.96, '4'), (383.79, ')'), (409.47, '문항수'), (440.99, '('), (448.91, '선택형:'), (483.47, '18,'), (501.03, '서답형'), (532.89, '2)')]

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
    global MEASURE, BREAKS
    RAGGED.clear(); NOBRK.clear()
    MEASURE = True
    open(os.path.join(HERE, 'overlay_src.html'), 'w').write(overlay_html())
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'overlay_src.html', 'overlay.pdf'], cwd=HERE, check=True)
    MEASURE = False
    BREAKS = autobreak(json.load(open(os.path.join(HERE, 'mk.json'))))
    # 측정 오프셋은 마킹 전 문자열 기준: 마커는 공백 앞뒤에만 끼워 넣었으므로 공백 순번으로 다시 찾는다
    open(os.path.join(HERE, 'overlay_src.html'), 'w').write(overlay_html())
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'overlay_src.html', 'overlay.pdf'], cwd=HERE, check=True)
    ov = pymupdf.open(os.path.join(HERE, 'overlay.pdf'))
    thin_boxes(ov)
    bg = make_background()
    assert len(ov) == len(bg) == 8, (len(ov), len(bg))
    for i, page in enumerate(bg):
        page.show_pdf_page(page.rect, ov, i, overlay=True)
    bg.set_metadata({'title': '2학년 미적분Ⅰ 기말고사 문제', 'author': '양정고등학교'})
    bg.subset_fonts()
    bg.save(out_pdf, garbage=4, deflate=True)

if __name__ == '__main__':
    build(sys.argv[1])
