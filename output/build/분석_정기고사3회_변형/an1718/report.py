# -*- coding: utf-8 -*-
"""2학기 중간 17·18번 변형 완전 분석 PDF (원문 ↔ 시험: 문장 요소·풀이 단계·오답·지표 → 기말 17·18 기준)"""
import os, sys, re, json, html, subprocess
RUN, OUT = sys.argv[1], sys.argv[2]                 # RUN: build3.py·render3.js·../fonts 가 있는 빌드 폴더
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN); from build3 import font_css, KATEX_CSS
E = html.escape
D = {n: json.load(open(os.path.join(HERE, f'a{n}.json'))) for n in (17, 18)}
ST = {'그대로': 'k', '바뀜': 'c', '변형': 'c', '삭제': 'd', '없어짐': 'd', '추가': 'a', '새 단계': 'a'}
FIG = 'file:///home/user/Finale/template/db/parts/fig_L42.svg'

def t(x):  # 수식이 섞인 문자열: \( \) 는 그대로 두고 나머지만 이스케이프
    parts = re.split(r'(\\\([\s\S]+?\\\)|\\\[[\s\S]+?\\\])', str(x))
    return ''.join(p if p.startswith('\\') else E(p) for p in parts)

def section(n):
    d = D[n]; m = d['metrics']
    head = {17: '17번 · 원문 L42 (2024 수능특강 [24009-0025], 단답 12) → 시험 ① 4',
            18: '18번 · 원문 C30 (2024 수능완성 [24054-0106], ② −4) → 시험 ④ 30'}[n]
    orig = d['original_text'] + (f'<div class="fig"><img src="{FIG}" style="width:150pt"></div>' if n == 17 else '')
    scan = f'<img class="scan" src="file://{HERE}/real{n}.png">'
    em = ''.join(f'<tr class="{ST.get(r["status"], "")}"><td>{t(r["element"])}</td><td>{t(r["original"])}</td><td>{t(r["exam"])}</td>'
                 f'<td class="s">{E(r["status"])}</td><td class="nt">{t(r.get("note", ""))}</td></tr>' for r in d['element_map'])
    so = ''.join(f'<li><b>{E(s["step"])}</b> {t(s["what"])} <span class="pr">[{t(s["principle"])}]</span></li>' for s in d['original_solution'])
    se = ''.join(f'<li><b>{E(s["step"])}</b> {t(s["what"])} <span class="pr">[{t(s["principle"])}]</span></li>' for s in d['exam_solution'])
    sm = ''.join(f'<tr class="{ST.get(r["status"], "")}"><td>{E(r["original_step"])}</td><td>{E(r["exam_step"])}</td><td class="s">{E(r["status"])}</td><td class="nt">{t(r["note"])}</td></tr>' for r in d['step_map'])
    cs = ''.join(f'<li>{t(c)}</li>' for c in d['cases'])
    ch = ''.join(f'<tr><td>{E(c["choice"])}</td><td>{t(c["value"])}</td><td class="nt">{t(c["why"])}</td></tr>' for c in d['choices'])
    mt = ''.join(f'<tr><th>{k}</th><td>{t(v)}</td></tr>' for k, v in [
        ('원문 요소 유지', m['kept_elements']), ('원문 풀이 단계 유지(변형 포함)', m['kept_steps']), ('새 풀이 단계', m['new_steps']),
        ('함수 교체', m['function_change']), ('조건 수', m['conditions']), ('구하는 것', m['target_change']), ('난도', m['difficulty'])])
    nt = ''.join(f'<li>{t(x)}</li>' for x in d['notes_for_guide'])
    return (f'<h2 class="pb">{head}</h2>'
            f'<div class="two"><div class="col"><div class="lab">부교재 원문</div>{orig}</div><div class="col"><div class="lab">실제 시험 (응시 시험지)</div>{scan}</div></div>'
            f'<div class="recipe"><span class="lab">한 줄 요약</span> {t(d["recipe"])}</div>'
            f'<h3>1. 문장 요소 대응</h3><table class="tb"><tr><th>요소</th><th>원문</th><th>시험</th><th>판정</th><th>비고</th></tr>{em}</table>'
            f'<h3>2. 풀이 단계</h3><div class="two"><div class="col"><div class="lab">원문 풀이</div><ol>{so}</ol></div><div class="col"><div class="lab">시험 풀이</div><ol>{se}</ol></div></div>'
            f'<table class="tb"><tr><th>원문 단계</th><th>시험 단계</th><th>판정</th><th>비고</th></tr>{sm}</table>'
            f'<h3>3. 경우 분기와 함정</h3><ul>{cs}</ul>'
            f'<h3>4. 선지 설계</h3><table class="tb"><tr><th>선지</th><th>값</th><th>근거</th></tr>{ch}</table>'
            f'<h3>5. 변형 거리 지표</h3><table class="tb mt">{mt}</table>'
            f'<h3>6. 기말 출제에 반영할 점</h3><ul>{nt}</ul>')

SUM = r"""
<h1>2학기 중간고사 17·18번 · 부교재 원문 대비 변형 완전 분석</h1>
<div class="sub">두 문항 모두 원문과 시험 문항을 끝까지 풀어 sympy로 검증(원문 12 / −4, 시험 ① 4 / ④ 30). 문장 요소와 풀이 단계를 하나씩 대응시킨 결과</div>
<h2>종합: 학교가 17·18번을 바꾸는 방식</h2>
<table class="tb"><tr><th></th><th>17번 (L42)</th><th>18번 (C30)</th></tr>
<tr><th>그대로 둔 축</th><td><b>설정</b>: \(f\)의 그래프(불연속점 \(0,\,1\)과 좌우극한), '최고차항의 계수 1인 \(g\)', 평가점 \(g(3)\)</td><td><b>판정 원리</b>: 분모 \(f(x^2)\)의 근은 \(\pm\)쌍, 극한이 존재하려면 분자도 \(0\)(약분)</td></tr>
<tr><th>바꾼 축</th><td>판정 원리 전체: 몫 \(\dfrac{g}{f}\)의 극한 → 합성 \((f\circ g)\)의 극한</td><td>설정 전체: 이차 → 사차, 두 함수 → \(\dfrac{f(x)}{f(x^2)}\) 하나</td></tr>
<tr><th>함수 교체</th><td>\(g\): 삼차 → 이차 (차수 1 낮춤)</td><td>\(f\): 이차 → 사차, 함수 2개 → 1개</td></tr>
<tr><th>조건</th><td>'모든 점에서 극한 존재' → '극한이 없는 점이 \(\alpha,\ \beta\)뿐' + \(\alpha\beta=0\)</td><td>'지정 점에서 극한 존재' → '불연속 3점' + '극한 없는 점 오직 한 개' + \(\lim_{x\to-3}g=0\)</td></tr>
<tr><th>구하는 것</th><td>\(g(3)\)의 값 → \(g(3)\)의 최솟값 (경계에서만 최솟값)</td><td>\(f(c)\times\lim h\) → \(f(2)\)</td></tr>
<tr><th>원문 요소 유지</th><td>3/11 (약 27%)</td><td>3/12 (약 25%)</td></tr>
<tr><th>원문 풀이 단계</th><td>그대로 0, 변형 3, 사라짐 3 / 새 단계 3</td><td>그대로 0, 변형 4 / 새 단계 3</td></tr>
<tr><th>계산량 · 판단량</th><td>계산 줄고, 경우 분기 5가지(꼭짓점 높이)</td><td>최종 계산 줄고, 중복도 분류·\(\sqrt r=r\) 추론 추가</td></tr></table>
<div class="key">
<b>핵심 규칙.</b> 학교는 원문의 두 축 — <b>설정(그래프·함수 꼴)</b>과 <b>판정 원리</b> — 중 <b>하나만 그대로</b> 두고 <b>다른 하나를 통째로</b> 바꾼다.
그리고 어느 쪽이든 <b>함수 교체(차수 ±1 또는 함수 합치기)</b>를 함께 넣고, 조건은 <b>'개수 조건 + 보조 수치 조건'</b>으로 다시 짠다.
원문 풀이 단계는 <b>그대로 남는 것이 하나도 없고</b>(모두 변형 또는 삭제), 새 단계가 <b>3개</b> 생긴다. 원문 문장 요소는 <b>4개 중 1개 정도</b>만 남는다.
</div>
<h2>우리 기준과의 차이</h2>
<table class="tb"><tr><th>문항</th><th>그대로 둔 것</th><th>함수 교체</th><th>원문 요소 유지(추정)</th><th>판정</th></tr>
<tr><td>학교 17 · 18</td><td>설정 <b>또는</b> 원리 하나</td><td>있음</td><td>약 25%</td><td>기준</td></tr>
<tr><td>견본 1차 17 (M55)</td><td>설정(원점 지나는 삼차, \(y=x\))</td><td>없음</td><td>약 50%</td><td>원리만 교체 → 한 단계 약함</td></tr>
<tr><td>견본2 17 (M39) · 18 (D70)</td><td>설정 대부분 + 조건 문장</td><td>없음</td><td>약 60%</td><td>약함</td></tr>
<tr><td>블라인드 C30</td><td>함수 \(f,\ g,\ h\)와 조건 (가) 문장 그대로</td><td>없음</td><td>약 60%</td><td>약함</td></tr>
<tr><td>견본 2차 17 (M33) — 사용자가 '너무 다르다'</td><td>거의 없음(설정·원리 둘 다 교체)</td><td>있음</td><td>약 10%</td><td>과함</td></tr></table>
<div class="key">
<b>제안: 기말 17·18 기준.</b>
① 설정·원리 중 <b>정확히 하나</b>는 원문 그대로(학생이 원문을 떠올릴 수 있게), 다른 하나는 통째로 교체 — 둘 다 바꾸면 과함(M33), 둘 다 남기면 약함(지금 견본).
② <b>함수 교체 필수</b>: 차수를 하나 올리거나 내리기, 또는 두 함수를 하나로 합치기.
③ 조건은 '정확히 \(n\)개/오직 한 개' 같은 <b>개수 조건</b> + 대칭식·극한값 같은 <b>보조 수치 조건</b> 하나.
④ 원문 풀이 단계는 그대로 0개, 새 단계 2~3개. 원문 문장 요소 유지 20~40%.
⑤ 계산량은 원문 이하로, 대신 경우 분기 4~5가지와 경계(접함·등호) 함정 하나. 구하는 것은 단순 함숫값 또는 최솟값.
⑥ 오답 선지는 학교보다 촘촘하게(학교는 일부만 근거 있음): 경계 제외·경우 누락·원문 풀이 그대로 쓴 값.
</div>
"""

CSS = r"""@page{size:A4;margin:11mm 10mm}body{font-family:'HB','MJ';font-size:8.6pt;line-height:1.5;margin:0}
.katex{font-family:'TN','KaTeX_Main'}.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
h1{font-family:'GL';font-weight:400;font-size:14pt;text-align:center;margin:0 0 1mm}.sub{text-align:center;font-family:'GL';font-size:7.8pt;color:#555;margin-bottom:3mm}
h2{font-family:'GL';font-weight:400;font-size:11pt;border-bottom:1.2pt solid #222;margin:6pt 0 4pt;padding-bottom:1pt}h2.pb{break-before:page}
h3{font-family:'GL';font-weight:400;font-size:9.5pt;color:#1f4e9a;margin:6pt 0 2pt}
b{font-weight:400;font-family:'GL'}.lab{font-family:'GL';font-size:7.8pt;color:#1f4e9a}
.two{display:grid;grid-template-columns:1fr 1fr;border:.7pt solid #444}.col{padding:4pt 6pt;min-width:0}.col+.col{border-left:.6pt solid #999}
.scan{width:100%}.fig{text-align:center}.cond{border:.6pt solid #000;padding:2pt 4pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}
.recipe{background:#f4f7fb;padding:3pt 6pt;margin-top:3pt}.key{background:#fbf6ee;border-left:2.5pt solid #b7701b;padding:4pt 7pt;margin:4pt 0}
table.tb{border-collapse:collapse;width:100%;margin:2pt 0}.tb th,.tb td{border:.5pt solid #aaa;padding:2pt 4pt;font-size:7.8pt;vertical-align:top;text-align:left}
.tb th{font-family:'GL';font-weight:400;background:#eef0f3}.tb td.s{font-family:'GL';white-space:nowrap}.tb td.nt{color:#444}
tr.k td.s{color:#16805b}tr.c td.s{color:#b7701b}tr.d td.s{color:#888}tr.a td.s{color:#c0392b}
.mt th{width:30mm}ol,ul{margin:2pt 0;padding-left:15pt}li{margin:1pt 0}.pr{color:#666;font-size:7.4pt}"""

body = SUM + section(17) + section(18)
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{body}</body></html>'
h = re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div style="text-align:center">\\(\\displaystyle ' + m.group(1) + '\\)</div>', h)
h = re.sub(r'\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'), h)
h = h.replace('\\boxed{', '{')
open(os.path.join(RUN, 'an_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(RUN, 'render3.js'), 'an_src.html', 'an_tmp.pdf', 'bg'], cwd=RUN, check=True)
os.replace(os.path.join(RUN, 'an_tmp.pdf'), OUT)
