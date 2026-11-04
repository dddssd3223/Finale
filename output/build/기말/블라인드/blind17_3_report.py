# -*- coding: utf-8 -*-
"""블라인드 3차: 중간 17번 원문(L42)을 현재 지침(0-4 통합판, 실제 17·18 정보 삭제본)만 보고 Claude·Codex(gpt-6-astra, medium)가 각각 변형 → 실제 17번과 비교 + 블라인드 풀이 패널
사용: python3 blind17_3_report.py <RUN(build3.py·render3.js·../fonts 폴더)> <출력 PDF>"""
import os, sys, re, subprocess
RUN, OUT = sys.argv[1], sys.argv[2]
ROOT = '/home/user/Finale'
P = ROOT + '/output/build/기말/공동출제/풀이/'
sys.path.insert(0, RUN); from build3 import font_css, KATEX_CSS
sys.path.insert(0, ROOT + '/template/db/parts')
from items_common import COND, FIG

def load(f):
    ns = {}; exec(open(f).read(), ns); return ns['ITEMS'][17], ns.get('DESIGN', {})
CL, DC = load(P + '블라인드17_claude/p17.py')
CX, DX = load(P + '블라인드17_codex/p17.py')
I = {}
s = open(f'{ROOT}/template/db/parts/items_p2.py').read(); exec(s[s.index("I['L42']"):s.index("I['L43']")], {'COND': COND, 'FIG': FIG, 'I': I})
C = '①②③④⑤'
FIGSRC = 'file://' + ROOT + '/template/db/parts/fig_L42.svg'
SCAN = 'file://' + ROOT + '/output/build/분석_정기고사3회_변형/an1718/real17.png'

def chs(ch, a):
    return '<div class="chs">' + ''.join(f'<span class="{"ok" if i == a else ""}">{C[i-1]} \\({c}\\)</span>' for i, c in enumerate(ch, 1)) + '</div>'
def figfix(h):
    return re.sub(r'src="fig_L42\.svg"', f'src="{FIGSRC}"', h)
def item(it):
    b = re.sub(r'\s*\[5\.2점\]', '', it['body'])
    return figfix(b + (COND(it['cond']) if it.get('cond') else '') + (it.get('after') or '') + chs(it['choices'], it['ans']))
ORIG = figfix(I['L42'][0]) + '<div class="chs"><span class="ok">단답형 · 정답 \\(12\\)</span></div>'

ROWS = [
    ('축', '설정 유지(같은 그래프, 식 삭제)·원리 교체: 몫 극한 → 합성 \\(f\\circ g\\)의 극한', '설정 유지(그래프)·원리 교체: 몫 극한 → 합성 \\(f(g(x))\\)의 연속', '설정 유지(그래프)·원리 교체: 몫 극한 → 높이별 교점 개수 \\(N(t)\\)와 \\(\\{f\\}^2+af+b\\)'),
    ('함수 교체', '\\(g\\): 삼차 → 이차(계수 1), 연산 몫 → 합성', '\\(g\\): 근 모르는 삼차 → \\(x^3-3x^2+k\\), 몫 → 합성', '\\(g\\): 독립 삼차 → \\(f\\)의 이차식(바깥 함수 합성)'),
    ('조건', '극한 없는 \\(t\\)가 \\(\\alpha,\\beta\\)뿐(개수) + \\(\\alpha\\beta=0\\)(수치)', '(가) 불연속점 4개(개수) + (나) \\(x=-1\\)에서 불연속(위치)', '(가) 실근 5개(개수) + (나) \\(g(0)+g(1)=0\\)(수치)'),
    ('조건 빼 보기', '—', '두 조건 모두 필요(빼면 답 2개 또는 무수히 많음)', '두 조건 모두 필요(빼면 최댓값 없음 / 더 큰 값)'),
    ('구하는 것', '\\(g(3)\\)의 최솟값(연속 자유도, 경계 \\(q=0\\))', '불연속점의 합(값)', '\\(a+b\\)의 최댓값(연속 자유도, 경계 \\(r=1, s=2\\))'),
    ('경계 함정', '꼭짓점에서 0·1에 닿으면 한쪽에서만 다가가 극한 존재', '극솟값으로 0·1에 위에서 닿는 점은 연속(\\(x=2\\))', '빈 점 \\((1,0)\\) 제외, 채운 점 \\((0,1)\\), \\((1,2)\\) 포함'),
    ('골격(dupcheck)', '0.15', '0.23 (통과)', '0.29 (통과)'),
    ('선지', '4–8 공차 1', '2–6 공차 1, 근거 3(4: 접점 포함, 3: \\(g=1\\) 누락, 6: 근과 계수 그대로)', '−3–1 공차 1, 근거 4'),
    ('체감 난도 · 시간 (Claude 풀이자)', '5/10 · 6–8분', '5.5/10 · 7–9분', '6.5/10 · 9–11분'),
    ('체감 난도 · 시간 (Codex 풀이자)', '5/10 · 6분', '6/10 · 8분', '4/10 · 5분'),
    ('두 풀이자 평균', '5.0', '5.8', '5.3'),
    ('풀이자 지적', '\\(\\alpha\\beta=0\\)이 조금 노골적', '없음. 접점을 잘못 세면 답이 없어져 스스로 고치게 됨(변별에 좋음)', '그림에 왼쪽 가지가 \\(y=2\\) 위까지 보이지 않음 → \\(N(t)\\) 판독에 그림 보강 필요'),
]
TAB = ('<table class="cmp"><tr><th></th><th>실제 2학기 중간 17번</th><th>Claude 블라인드</th><th>Codex 블라인드 (gpt-6-astra · medium)</th></tr>'
       + ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in ROWS) + '</table>')

SUM = ('<div class="box key"><div class="lab">결론</div>'
       '<p>현재 지침(0-4 통합판)만으로 두 출제자 모두 <b>실제 17번과 같은 축</b>(원문 그래프 유지 + 판정 원리 교체 + 합성 구조)을 골랐고, '
       '블라인드 풀이 패널 체감 난도는 <b>5.8 · 5.3으로 실제 17번(5.0)과 거의 같다</b>. 견본3 17번(7)보다 크게 가벼워져 \'더 멀리, 더 가볍게\'가 작동했다.</p>'
       '<p>차이: Claude 변형은 구하는 것이 \'값\'(합), Codex 변형은 실제 17번처럼 \'연속 자유도 + 경계 최댓값\'. '
       'Codex 변형은 그림 보강(왼쪽 가지가 \\(y=2\\)를 넘는 것이 보이게)이 필요하다.</p>'
       '<p>관찰: 두 풀이자가 서로 <b>상대 모델이 낸 문항을 더 어렵게</b> 평가했다(Claude 풀이자 → Codex 문항 6.5, Codex 풀이자 → Claude 문항 6). '
       '출제자 스타일에 익숙하면 쉽게 느낀다는 뜻이라, 공동 출제·교차 풀이의 필요성을 뒷받침한다.</p></div>')

body = ('<h1>2학기 중간 17번 블라인드 변형 (3차) · Claude · Codex · 실제 시험</h1>'
        '<div class="sub">원문 L42 (2024 수능특강 [24009-0025]). 두 출제자에게 같은 꾸러미(현재 지침 0-4·0-6·0-7·17–18번 절에서 실제 17·18 정보를 지운 발췌본, 원문, 그림)만 줌. Codex는 GitHub Actions에서 작업 폴더만 받은 상태로 실행. 정답·빼 보기는 sympy 검증, 체감 난도는 순서를 섞은 블라인드 풀이(해설 없음, 코드 없음)</div>'
        + SUM +
        f'<div class="grid"><div class="col"><div class="lab">부교재 원문 (L42)</div>{ORIG}</div>'
        f'<div class="col"><div class="lab">실제 2학기 중간 17번 (시험지)</div><img class="scan" src="{SCAN}"></div>'
        f'<div class="col"><div class="lab">Claude 블라인드 · 정답 {C[CL["ans"]-1]}</div>{item(CL)}</div>'
        f'<div class="col"><div class="lab">Codex 블라인드 · 정답 {C[CX["ans"]-1]}</div>{item(CX)}</div></div>'
        + TAB +
        f'<div class="box"><div class="lab">Claude 블라인드 풀이</div>{CL["sol"]}</div>'
        f'<div class="box"><div class="lab">Codex 블라인드 풀이</div>{CX["sol"]}</div>')

CSS = r"""@page{size:A4;margin:10mm 9mm}body{font-family:'HB','MJ';font-size:8.4pt;line-height:1.5;margin:0}
.katex{font-family:'TN','KaTeX_Main'}.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
h1{font-family:'GL';font-weight:400;font-size:13pt;text-align:center;margin:0 0 1mm}.sub{text-align:center;font-family:'GL';font-size:7.3pt;color:#555;margin-bottom:2mm}
b{font-family:'GL';font-weight:400}
.grid{display:grid;grid-template-columns:1fr 1fr;border:.8pt solid #333;font-size:7.9pt;margin-top:2mm}.col{padding:4pt 6pt;min-width:0;border-bottom:.6pt solid #999}.col:nth-child(odd){border-right:.6pt solid #999}
.lab{font-family:'GL';font-size:7.6pt;color:#1f4e9a;margin-bottom:2pt}.chs{display:flex;flex-wrap:wrap;gap:1pt 9pt;margin-top:3pt}.ok{color:#c0392b}
.cond{border:.6pt solid #000;padding:2pt 4pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}.ck{margin-right:3pt}.dm{text-align:center;margin:2pt 0}
.fig{text-align:center;margin:2pt 0}.fig img{max-width:100%}.scan{width:100%}
.box{border:.6pt solid #999;padding:4pt 7pt;margin-top:2.5mm}.key{background:#fbf6ee;border-color:#b7701b}.box p{margin:2pt 0}
table.cmp{border-collapse:collapse;width:100%;margin-top:2.5mm}
.cmp th,.cmp td{border:.5pt solid #999;padding:2.5pt 4pt;font-size:7.6pt;vertical-align:top;text-align:left}.cmp th{font-family:'GL';font-weight:400;background:#eef0f3}
.cmp tr th:first-child{white-space:nowrap}.cmp td{width:30%}"""

fix = lambda s: re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div class="dm">\\(\\displaystyle ' + m.group(1) + '\\)</div>', s)
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{fix(body)}</body></html>'
h = re.sub(r'\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), h)
open(os.path.join(RUN, 'b17_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(RUN, 'render3.js'), 'b17_src.html', 'b17_tmp.pdf', 'bg'], cwd=RUN, check=True)
os.replace(os.path.join(RUN, 'b17_tmp.pdf'), OUT)
