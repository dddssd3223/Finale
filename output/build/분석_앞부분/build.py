# -*- coding: utf-8 -*-
"""실제 시험 vs 모의고사 1–20회: 앞부분(1–8번) 난도 비교 보고서"""
import os, sys, json, subprocess, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(SCR, 'r20'))
from build3 import font_css, KATEX_CSS

D = json.load(open(os.path.join(SCR, 'diffcmp.json')))
F = json.load(open(os.path.join(SCR, 'front_feat.json')))
W = {'하': 1, '중하': 2, '중': 3, '중상': 4, '상': 5}
TM = {'하': 1.5, '중하': 2.5, '중': 4, '중상': 6, '상': 8}
LV = ['하', '중하', '중', '중상']
RS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20]
GRADED = {1, 2, 3, 4, 5, 7, 8, 9, 12, 13, 15, 16}
FRONT_LOSS = {12: 4.0}                     # 채점 회차 중 1–8번 실점 (12회 3번 하나)
# 실제 시험 1–8번: 같은 유형 모의 문항에 붙였던 난도로 다시 매김
REAL = [
 (1, '그래프와 좌·우극한', '하', '16회 1번 (하)', '같은 위치·같은 난도'),
 (2, '연속과 미정계수', '하', '20회 6번 (하) · 9회 3번 · 16회 6번', '같은 위치·같은 난도'),
 (3, '평균변화율 = 미분계수 (평균값 정리)', '중하', '출제 없음', '모의고사 범위에서 뺐던 단원'),
 (4, '조건 상자 + 도함수 범위로 f(3) 최대·최소', '중상', '출제 없음', '앞부분 최대 난관 · 평균값 정리 응용'),
 (5, '함수의 극한의 대소 관계', '중', '15회 10번 (중)', '모의는 10번, 실제는 5번'),
 (6, '사잇값 정리로 해의 구간 찾기', '중', '12회 16번 (상) · 18회 서술형', '모의는 16번·서술형, 실제는 6번'),
 (7, '집합 조건으로 삼차함수 결정', '중', '10회 13번 (중) · 2회 12번 (중) · 5회 13번 (중상)', '모의는 12–13번, 실제는 7번'),
 (8, '곱의 미분 + 함수 관계식', '중하', '5회 3번 (하) · 3회 7번 (중하)', '비슷하나 단계가 하나 더 많음'),
]
RL = [x[2] for x in REAL]

def labs(r): return [D[str(r)]['labels'][str(n)] for n in range(1, 9)]
def row(key, L):
    f = F[str(key)]
    return dict(score=sum(W[l] for l in L), time=sum(TM[l] for l in L), read=sum(x['hang'] for x in f.values()),
                cond=sum(1 for x in f.values() if x['cond'] or x['bogi']), cnt=[L.count(v) for v in LV])
DATA = {r: row(r, labs(r)) for r in RS}
REALD = row(0, RL)
avg = lambda k, rs=RS: st.mean(DATA[r][k] for r in rs)
LATE = [r for r in RS if r >= 12]

# ---------------------------------------------------------------- 차트 (인쇄용 정적 SVG)
C_MOCK, C_REAL = '#2a78d6', '#eb6834'          # 범주 1·2번 슬롯 (검증 통과 조합)
RAMP = ['#86b6ef', '#3987e5', '#1c5cab', '#0d366b']  # 하→중상 순서형 (검증 통과)
INK, INK2, MUTED, AXIS, GRID = '#0b0b0b', '#52514e', '#898781', '#c3c2b7', '#e9e8e4'

def bar_svg(key, title_unit, fmt=lambda v: f'{v:g}', ymax=None, ticks=None):
    keys = RS + ['실제']
    vals = [DATA[r][key] for r in RS] + [REALD[key]]
    Wd, H, L, B, T = 520, 170, 30, 22, 14
    pw, ph = Wd - L - 6, H - B - T
    ymax = ymax or max(vals) * 1.15
    n = len(keys); slot = pw / n; bw = slot * 0.62
    s = [f'<svg viewBox="0 0 {Wd} {H}" width="100%" style="display:block" font-family="GL" font-size="7.5">']
    for t in ticks:
        y = T + ph - t / ymax * ph
        s.append(f'<line x1="{L}" x2="{L+pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width=".6"/>'
                 f'<text x="{L-4}" y="{y+2.5:.1f}" text-anchor="end" fill="{MUTED}">{t:g}</text>')
    m = avg(key)
    for i, (k, v) in enumerate(zip(keys, vals)):
        x = L + i * slot + (slot - bw) / 2; h = v / ymax * ph; y = T + ph - h
        c = C_REAL if k == '실제' else C_MOCK; r = min(3, bw / 2, h)
        s.append(f'<path d="M{x:.1f},{T+ph:.1f} V{y+r:.1f} Q{x:.1f},{y:.1f} {x+r:.1f},{y:.1f} H{x+bw-r:.1f} '
                 f'Q{x+bw:.1f},{y:.1f} {x+bw:.1f},{y+r:.1f} V{T+ph:.1f} Z" fill="{c}"/>')
        s.append(f'<text x="{x+bw/2:.1f}" y="{y-2.5:.1f}" text-anchor="middle" fill="{INK if k=="실제" else INK2}"'
                 f'{" font-weight=700" if k=="실제" else ""}>{fmt(v)}</text>')
        lab = '실제' if k == '실제' else f'{k}회'
        s.append(f'<text x="{x+bw/2:.1f}" y="{T+ph+10:.1f}" text-anchor="middle" fill="{INK if k=="실제" else MUTED}">{lab}</text>')
    y = T + ph - m / ymax * ph
    s.append(f'<line x1="{L}" x2="{L+pw-slot}" y1="{y:.1f}" y2="{y:.1f}" stroke="{INK2}" stroke-width=".8" stroke-dasharray="3 2"/>'
             f'<text x="{L+pw-slot-2}" y="{y-3:.1f}" text-anchor="end" fill="{INK2}">모의 평균 {fmt(round(m,1))}</text>')
    s.append(f'<line x1="{L}" x2="{L+pw}" y1="{T+ph}" y2="{T+ph}" stroke="{AXIS}" stroke-width=".8"/></svg>')
    return ''.join(s)

def stack_svg():
    keys = RS + ['실제']
    rows = [DATA[r]['cnt'] for r in RS] + [REALD['cnt']]
    Wd, rh, L, T = 520, 13.2, 46, 18
    H = T + rh * len(keys) + 4
    pw = Wd - L - 8; u = pw / 8
    s = [f'<svg viewBox="0 0 {Wd} {H:.0f}" width="100%" style="display:block" font-family="GL" font-size="7.5">']
    lx = L
    for i, v in enumerate(LV):                 # 범례 (차트 위)
        s.append(f'<rect x="{lx}" y="3" width="9" height="9" rx="2" fill="{RAMP[i]}"/>'
                 f'<text x="{lx+12}" y="10.5" fill="{INK2}">{v}</text>'); lx += 46
    for j, (k, c) in enumerate(zip(keys, rows)):
        y = T + j * rh; x = L
        lab = '실제 시험' if k == '실제' else f'{k}회'
        s.append(f'<text x="{L-4}" y="{y+rh/2+2.6:.1f}" text-anchor="end" fill="{INK if k=="실제" else MUTED}"'
                 f'{" font-weight=700" if k=="실제" else ""}>{lab}</text>')
        for i, cnt in enumerate(c):
            if not cnt: continue
            w = cnt * u - 2                    # 2pt 표면 간격
            s.append(f'<rect x="{x:.1f}" y="{y+1.5:.1f}" width="{w:.1f}" height="{rh-3:.1f}" rx="2" fill="{RAMP[i]}"/>')
            s.append(f'<text x="{x+w/2:.1f}" y="{y+rh/2+2.6:.1f}" text-anchor="middle" fill="{"#fff" if i>=1 else INK}">{cnt}</text>')
            x += cnt * u
        if k == '실제':
            s.append(f'<rect x="{L-33}" y="{y+0.3:.1f}" width="{pw+35:.1f}" height="{rh-0.6:.1f}" fill="none" stroke="{C_REAL}" stroke-width="1" rx="2"/>')
    s.append('</svg>')
    return ''.join(s)

CSS = r"""
@page{size:A4;margin:13mm 12mm 12mm 12mm}
html,body{margin:0;background:#fff}
body{font-family:'GL';font-size:9pt;color:#111}
.katex{font-size:1em}
h1{font-size:15pt;text-align:center;margin:0 0 2pt;letter-spacing:.3pt;-webkit-text-stroke:.35pt #000}
.subt{text-align:center;font-size:9.5pt;color:#444;margin-bottom:8pt}
.tag{display:inline-block;background:#111;color:#fff;padding:2pt 8pt;font-size:9pt;letter-spacing:1pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h2{font-size:11pt;margin:9pt 0 4pt;-webkit-text-stroke:.25pt #000}
.cap{font-size:8pt;color:#52514e;margin:1pt 0 3pt}
table{border-collapse:collapse;width:100%}
th,td{border:.6pt solid #999;padding:2pt 4pt;text-align:center;vertical-align:middle;line-height:1.3;font-size:8.2pt}
th{background:#eee;font-weight:400;-webkit-text-stroke:.2pt #000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
td.l{text-align:left}
tr.real td{background:#fdeee7;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-weight:700}
.sum{display:flex;gap:8pt;margin:6pt 0}
.sum div{flex:1;border:1pt solid #ccc;border-radius:4pt;padding:5pt 8pt;font-size:8.4pt;color:#333}
.sum b{font-size:14pt;display:block;margin:2pt 0 1pt;color:#0b0b0b}
.sum span{color:#52514e}
.ins td{text-align:left;padding:4pt 7pt;line-height:1.55;font-size:8.6pt}
.chip{display:inline-block;border-radius:3pt;padding:0 5pt;color:#fff;font-size:7.8pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pb{break-before:page}
.figs{display:flex;gap:6pt;flex-wrap:wrap}
.figs div{width:calc(50% - 3pt);border:.6pt solid #ddd;padding:3pt;box-sizing:border-box}
.figs .l{font-size:8pt;color:#555;margin-bottom:2pt}
.figs img{width:100%}
"""

def chip(l):
    i = LV.index(l) if l in LV else 3
    return f'<span class="chip" style="background:{RAMP[i]};color:{"#0b0b0b" if i==0 else "#fff"}">{l}</span>'

def build(out):
    a, a12 = avg('score'), avg('score', LATE)
    head = f"""<div style="text-align:right"><span class="tag">분석 · 앞부분 1–8번</span></div>
<h1>실제 중간고사 vs 모의고사 1–20회 · 앞부분(1–8번) 난도 비교</h1>
<div class="subt">미적분Ⅰ · 2026년 10월 13일(화) 1교시 · 19회 없음 · 실제 시험은 같은 유형 모의 문항의 난도 기준으로 다시 매김</div>
<div class="sum">
<div>앞부분 난도 점수<br><b>실제 {REALD['score']} <span style="font-size:10pt">vs 모의 평균 {a:.1f}</span></b><span>12회 이후 평균 {a12:.1f} · 모의 최고 {max(DATA[r]['score'] for r in RS)}(4·5회)</span></div>
<div>앞부분 문제 읽기량 (한글 글자 수)<br><b>실제 {REALD['read']} <span style="font-size:10pt">vs 모의 평균 {avg('read'):.0f}</span></b><span>20개 시험지 중 가장 많음</span></div>
<div>앞부분 예상 풀이 시간 (추정)<br><b>실제 약 {REALD['time']:.0f}분 <span style="font-size:10pt">vs 모의 {avg('time'):.0f}분</span></b><span>12회 이후 모의는 약 {avg('time', LATE):.0f}분</span></div>
</div>
<p class="cap">난도 점수 = 1–8번 각 문항 하 1 · 중하 2 · 중 3 · 중상 4 · 상 5의 합 (8문항 모두 하면 8점). 예상 시간은 하 1.5분 · 중하 2.5분 · 중 4분 · 중상 6분으로 잡은 추정이에요.</p>
<h2>① 회차별 앞부분 난도 점수</h2>
{bar_svg('score', '점', ymax=22, ticks=[0, 5, 10, 15, 20])}
<p class="cap">12회부터 18회까지 앞부분이 거의 모두 '하'(8–9점)였어요. 실제 시험(19점)은 모의 중 가장 어려운 4·5회(16점)보다도 높았어요.</p>
<h2>② 회차별 앞부분 문제 읽기량 (한글 글자 수)</h2>
{bar_svg('read', '자', fmt=lambda v: f'{v:.0f}', ymax=320, ticks=[0, 100, 200, 300])}
<p class="cap">수식을 뺀 한글 글자 수예요. 실제 1–8번은 조건 상자 2개(4·7번)와 긴 문장(6·8번) 때문에 모의 평균의 약 {REALD['read']/avg('read'):.1f}배를 읽어야 했어요.</p>
"""
    rows = ''.join(f'<tr><td>{n}번</td><td class="l">{t}</td><td>{chip(l)}</td><td class="l">{m}</td><td class="l">{c}</td></tr>' for n, t, l, m, c in REAL)
    p2 = f"""<div class="pb"></div><h2>③ 실제 1–8번 문항별 비교</h2>
<table><colgroup><col style="width:6%"><col style="width:29%"><col style="width:8%"><col style="width:30%"><col style="width:27%"></colgroup>
<tr><th>번호</th><th>유형</th><th>난도</th><th>모의고사에서 같은 유형 (그때 매긴 난도)</th><th>차이</th></tr>{rows}</table>
<p class="cap">5·6·7번은 모의고사에서 10–16번이나 서술형에 두고 '중'–'상'으로 매겼던 유형이에요. 실제 시험은 같은 유형을 5–7번(4.2점)에 냈어요.</p>
<h2>④ 회차별 앞부분 난도 구성</h2>
{stack_svg()}
<p class="cap">막대 하나가 1–8번 8문항이에요. 칸 안의 숫자는 그 난도의 문항 수예요.</p>
<div class="pb"></div><h2>⑤ 회차별 표</h2>
<table><tr><th>회차</th><th>하</th><th>중하</th><th>중</th><th>중상</th><th>난도 점수</th><th>예상 시간(분)</th><th>읽기량</th><th>조건·보기 상자</th><th>내 1–8번 실점</th></tr>
""" + ''.join(f'<tr><td>{r}회</td>' + ''.join(f'<td>{c or "·"}</td>' for c in DATA[r]['cnt'])
              + f'<td>{DATA[r]["score"]}</td><td>{DATA[r]["time"]:g}</td><td>{DATA[r]["read"]}</td><td>{DATA[r]["cond"] or "·"}</td>'
              + f'<td>{(f"{FRONT_LOSS[r]:g}점 (3번)" if r in FRONT_LOSS else "0") if r in GRADED else "미채점"}</td></tr>' for r in RS) \
      + f'<tr class="real"><td>실제</td>' + ''.join(f'<td>{c or "·"}</td>' for c in REALD['cnt']) \
      + f'<td>{REALD["score"]}</td><td>{REALD["time"]:g}</td><td>{REALD["read"]}</td><td>{REALD["cond"]}</td><td>0</td></tr></table>'
    p3 = f"""<h2>⑥ 정리와 기말 대비</h2>

<table class="ins">
<tr><td style="width:22%;text-align:center">결론</td><td>네 느낌이 맞아요. 실제 1–8번은 난도 점수 {REALD['score']}점으로 모의 평균({a:.1f}점)의 약 {REALD['score']/a:.1f}배, 12회 이후 모의({a12:.1f}점)의 약 {REALD['score']/a12:.1f}배였어요. 모의고사 19개 회차 중 이보다 앞부분이 어려운 회차는 없었어요.</td></tr>
<tr><td style="text-align:center">왜 놓쳤나</td><td>· 이전 난도 비교는 상·최상·중상 문항만 셌어요. 그래서 '중'이 앞에 몰린 실제 시험이 모의보다 쉬워 보였어요.<br>
· 실전형으로 바꾼 12회 이후 모의고사는 1–8번을 거의 모두 '하'로 만들었어요. 뒷부분 킬러 대비에 집중하느라 앞부분을 지나치게 가볍게 만든 거예요.<br>
· 3·4번 평균값 정리는 모의고사 범위에서 뺐던 단원이었어요.</td></tr>
<tr><td style="text-align:center">점수와의 관계</td><td>1–8번은 실제 시험에서도 모의고사에서도 거의 다 맞혔어요(채점한 모의 12회분에서 1–8번 실점은 12회 3번 하나). 그래서 앞부분은 정답률보다 <b>시간</b>이 문제였을 가능성이 커요. 추정으로는 앞부분에서 모의보다 약 {REALD['time']-avg('time', LATE):.0f}분을 더 썼을 수 있고, 18번을 풀이 없이 고른 것과 이어질 수 있어요(추정).</td></tr>
<tr><td style="text-align:center">기말 모의고사</td><td>· 1–8번 난도 점수를 실제 수준(17–20점)으로 맞출게요. 하 2 · 중하 2 · 중 3 · 중상 1 정도 구성이에요.<br>
· 조건 상자형 문항을 앞부분에 1–2개 넣고, 사잇값·평균값 정리 같은 정리 활용형을 4–6번에 둘게요.<br>
· 시험지마다 앞부분(1–8번)과 뒷부분 난도를 따로 계산해서 실제 시험과 비교할게요.<br>
· 풀 때는 1–8번 목표 시간을 정해 두고 연습하는 걸 추천해요.</td></tr></table>
<div class="pb"></div><h2>⑦ 실제 시험에서 앞부분을 어렵게 만든 문항</h2>
<div class="figs"><div><div class="l">실제 4번 · 모의고사 출제 없음</div><img src="real_4.png"></div>
<div><div class="l">실제 7번 · 모의 10회 13번과 같은 유형</div><img src="real_7.png"></div>
<div><div class="l">실제 6번 · 모의 12회 16번·18회 서술형과 같은 논리</div><img src="real_6.png"></div>
<div><div class="l">실제 3번 · 모의고사 출제 없음</div><img src="real_3.png"></div></div>
"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{p2}{p3}</body></html>')
    open(os.path.join(HERE, 'rep_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'rep_src.html', 'rep_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'rep_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
