# -*- coding: utf-8 -*-
"""블라인드 2차: 중간 17·18번 원문(L42·C30)을 지침서(실제 17·18 정보를 지운 발췌본 guide_blind.md)만 보고 변형 → 실제 시험과 비교
사용: python3 blind1718_report.py <RUN(build3.py·render3.js·../fonts 폴더)> <출력 PDF>"""
import os, sys, re, subprocess
RUN, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/Finale'
sys.path.insert(0, RUN); from build3 import font_css, KATEX_CSS
sys.path.insert(0, ROOT + '/template/db/parts')
from items_common import COND, FIG

def load(f, n):
    ns = {}; exec(open(os.path.join(HERE, f)).read(), ns); return ns['ITEMS'][n], ns['DESIGN']
B17, D17 = load('p17.py', 17)
B18, D18 = load('p18.py', 18)
I = {}
for f, a, b in (('items_p2.py', "I['L42']", "I['L43']"), ('items_p4.py', "I['C30']", "I['C31']")):
    s = open(f'{ROOT}/template/db/parts/{f}').read(); exec(s[s.index(a):s.index(b)], {'COND': COND, 'FIG': FIG, 'I': I})
C = '①②③④⑤'
FIGDIR = ROOT + '/template/db/parts/'
SCAN = ROOT + '/output/build/분석_정기고사3회_변형/an1718/'

def chs(ch, a):
    return '<div class="chs">' + ''.join(f'<span class="{"ok" if i == a else ""}">{C[i-1]} \\({c}\\)</span>' for i, c in enumerate(ch, 1)) + '</div>'
def figfix(h):
    return re.sub(r'src="(fig_[A-Za-z0-9_]+\.svg)"', lambda m: f'src="file://{FIGDIR}{m.group(1)}"', h)
def orig(k):
    b, ch, a, src = I[k]
    return figfix(b) + (chs(ch, C.index(a) + 1) if ch else f'<div class="chs"><span class="ok">단답형 · 정답 \\({a}\\)</span></div>')
def mine(it):
    return figfix(it['body'] + (COND(it['cond']) if it.get('cond') else '') + (it.get('after') or '') + chs(it['choices'], it['ans']))
def scan(n):
    return f'<img class="scan" src="file://{SCAN}real{n}.png">'

ROW17 = [
    ('유지한 축', r"설정: 원문 \(f\)의 그래프(그림 그대로, 조각함수 식 삭제)", r"설정: 같은 그래프(식 삭제, 그림만)", '같음'),
    ('교체한 축', r"원리: 몫 \(g/f\)의 극한 존재 → 합성 \(f(g(x))\)의 <b>불연속점 개수</b>", r"원리: 몫 \(g/f\)의 극한 존재 → 합성 \(f\circ g\)의 <b>극한이 존재하지 않는 점</b>", '거의 같음'),
    ('함수 교체', r"\(g\): 계수 \(1\)인 삼차 → 계수 \(-1\)인 이차(차수 −1)", r"\(g\): 계수 \(1\)인 삼차 → 계수 \(1\)인 이차(차수 −1)", '같음'),
    ('조건', r"개수 조건 '불연속인 \(x\)의 개수 \(3\)' + 보조 수치 '\(h(1)=0\)'", r"개수 조건 '극한이 없는 \(t\)는 \(\alpha\), \(\beta\)뿐' + 보조 수치 '\(\alpha\beta=0\)'", '같은 틀'),
    ('구하는 것', r"\(g(3)\)의 최댓값", r"\(g(3)\)의 최솟값", '같은 틀'),
    ('경우 분기 · 함정', r"꼭짓점 높이 \(M\) 5가지(0·1·2·3·4개), 꼭짓점이 아래에서 닿을 때 극한은 있으나 불연속", r"꼭짓점 높이 5가지, 접할 때 한쪽에서만 다가감, 경계 \(q=0\)에서 최솟값", '같은 틀'),
    ('최댓값·최솟값의 성격', r"(가)·(나)를 만족하는 \(g\)가 <b>2개뿐</b>(꼭짓점 \(x=3\) 또는 \(x=-1\)) → 둘 중 큰 값", r"\(g\)가 <b>연속적으로 움직이고</b> 경계에서만 최솟값이 생김(경계 포함 여부가 변별)", '<b>약함</b>'),
    ('선지', r"\(-15\)부터 \(1\)까지 공차 \(4\). 근거 있는 오답 2(다른 후보, 빈 점 오독), 채움 2", r"\(4\)부터 \(8\)까지 공차 \(1\). 근거 있는 오답 2(경계 제외 등), 채움 2", '같은 수준'),
    ('형식', r"그림 첫 문장 → \(g\) 소개 → 질문 → 상자 (가)(나)", r"그림 첫 문장 → \(g\) 소개 → 질문 → 라벨 없는 상자", '같음'),
]
ROW18 = [
    ('유지한 축', r"원리: 분모가 합성식인 유리함수에서 불연속점 = 분모의 실근, 개수는 속함수의 최솟값과 \(f\)의 근 비교, 극한 존재 ⇔ \(\frac00\)", r"원리: 분모 \(f(x^2)\)의 근 \(\pm\sqrt r\), 극한 존재 ⇒ 분자도 \(0\)", '같은 축'),
    ('교체한 축', r"설정: 두 함수 \(g,\ h\) → <b>하나</b> \(\dfrac{x-k}{f(f(x))}\) (\(f\)가 속·겉 함수 둘 다)", r"설정: 두 함수 → <b>하나</b> \(\dfrac{f(x)}{f(x^2)}\) (분자·분모가 같은 \(f\))", '같은 방식'),
    ('함수 교체', r"합치기만 (이차 그대로)", r"합치기 + 이차 → <b>사차</b>", '한 단계 약함'),
    ('조건', r"(가) 극한이 존재하지 않는 \(t\)의 개수 \(2\) + (나) \(\displaystyle\lim_{x\to k}g(x)=-\frac1{16}\)", r"(가) 불연속점 \(a, b, c\) + (나) 극한이 없는 점 오직 한 개 + (다) \(\displaystyle\lim_{x\to-3}g(x)=0\)", '조건 하나 적음'),
    ('새 단계', r"중근에서 극한 발산 → 제외, 근 개수 5경우에서 \(\alpha=m\), 극한값 부호로 좌우 근 선택", r"\(x=0\)에서 차수 비교(\(f(x^2)\)이 두 배), \(\sqrt r=r\) 고정점, (다)의 연속 판정", '같은 수(3)'),
    ('구하는 것', r"\(f(1)+k\)", r"\(f(2)\)", '같은 틀'),
    ('선지', r"\(-3\)부터 \(5\)까지 공차 \(2\). 근거 있는 오답 3, 채움 1", r"\(24\)부터 \(32\)까지 공차 \(2\). 근거 있는 오답 1–2", '블라인드가 촘촘'),
    ('형식', r"\(g\)를 첫 문장에 정의 → 질문 → 상자", r"\(g\)를 첫 문장에 정의 → 상자 → 질문", '질문 위치만 다름'),
]
def tab(rows):
    return ('<table class="cmp"><tr><th></th><th>블라인드 변형</th><th>실제 2학기 중간</th><th>판정</th></tr>'
            + ''.join(f'<tr><th>{a}</th><td>{b}</td><td>{c}</td><td class="v">{d}</td></tr>' for a, b, c, d in rows) + '</table>')
def three(n, k, it):
    return (f'<div class="three"><div class="col"><div class="lab">부교재 원문 ({k})</div>{orig(k)}</div>'
            f'<div class="col"><div class="lab">블라인드 변형 (지침 발췌본만 보고 작성)</div>{mine(it)}</div>'
            f'<div class="col"><div class="lab">실제 2학기 중간 {n}번 (시험지)</div>{scan(n)}</div></div>')
def solbox(it):
    return (f'<div class="box"><div class="lab">블라인드 변형 풀이</div>{it["sol"]}'
            f'<div class="lab" style="margin-top:3pt">오답 설계</div>{it["wrong"]}</div>')

V17 = ("판정 원리 교체 방향(몫 극한 → 합성 함수), 함수 교체(삼차 → 이차), 그림만 남기는 형식, 개수 + 보조 수치 조건, 꼭짓점 높이 5가지 분기까지 실제 17번과 같은 자리를 짚었다. "
       "차이는 최댓값의 성격이다. 블라인드는 조건을 만족하는 \\(g\\)가 두 개뿐이라 '둘 중 큰 값'이고, 실제 17번은 \\(g\\)가 연속적으로 움직이며 접하는 경계에서만 최솟값이 생겨 경계를 넣느냐가 변별이었다.")
V18 = ("원리를 남기고 설정을 바꾸는 축 선택, 두 함수를 하나로 합치고 같은 \\(f\\)를 두 번 쓰는 자기참조 구조는 실제 18번과 같은 방식이다. "
       "차이는 두 가지다. 실제는 합치기에 이차 → 사차를 더해 함수 교체가 두 겹이고, 조건이 하나 더(극한 미존재 개수 + 특정 점 극한값 + 불연속점 개수) 있다. 블라인드는 이차 그대로라 경우 분류가 한 겹 얕다.")
SUM = ('<div class="box key"><div class="lab">블라인드 2차 결론</div>'
       '<p>지침서(실제 17·18번 정보를 지운 발췌본)만으로 두 문항 모두 <b>학교와 같은 축 선택</b>(17: 설정 유지·원리 교체, 18: 원리 유지·설정 교체)과 <b>같은 변형 방식</b>(17: 몫 → 합성·차수 −1, 18: 두 함수 합치기·자기참조)이 나왔다. '
       '1차 블라인드(옛 지침, 원본 틀을 거의 그대로 두고 판정 원리 하나만 바꿈)보다 학교에 훨씬 가깝다.</p>'
       '<p>남은 차이 → 지침 보강안</p><ol>'
       '<li><b>최댓값·최솟값 문항</b>: 조건을 만족하는 함수가 이산 후보 몇 개로 끝나면 안 된다. 자유도 1이 남아 함수가 연속적으로 움직이고, 경계(접함·등호)에서 극값이 생기게 한다.</li>'
       '<li><b>함수 교체 두 겹</b>: 18번(최고난도)은 합치기와 차수 ±1을 함께 넣는다. 17번은 한 겹으로 충분하다.</li>'
       '<li><b>18번 조건 수</b>: 18번은 개수 조건 2개(불연속점 개수, 극한 미존재 개수) + 보조 수치 조건 1개, 모두 3개.</li></ol>'
       '<p>선지 등차 배열, 질문 위치, 함수 소개 순서 같은 형식 규칙(0-7)은 두 문항 모두 지켰다.</p></div>')

body = ('<h1>2학기 중간 17·18번 블라인드 변형 (2차) · 실제 시험 비교</h1>'
        '<div class="sub">원문: L42 (2024 수능특강 [24009-0025]) · C30 (2024 수능완성 [24054-0106]). 변형은 실제 17·18번 서술을 모두 지운 지침 발췌본(0-4 변형 거리, 0-6 말투, 0-7 형식, 17–18번 절)만 준 별도 출제자가 작성. 정답은 sympy 전수 검증(verify17.py, verify18.py)</div>'
        + SUM +
        '<h2>17번</h2>' + three(17, 'L42', B17) + tab(ROW17) + f'<div class="box"><div class="lab">비교</div>{V17}</div>' + solbox(B17) +
        '<h2 class="pb">18번</h2>' + three(18, 'C30', B18) + tab(ROW18) + f'<div class="box"><div class="lab">비교</div>{V18}</div>' + solbox(B18))

CSS = r"""@page{size:A4;margin:10mm 9mm}body{font-family:'HB','MJ';font-size:8.5pt;line-height:1.5;margin:0}
.katex{font-family:'TN','KaTeX_Main'}.katex .mathnormal{font-family:'TN','KaTeX_Math';font-style:italic}
h1{font-family:'GL';font-weight:400;font-size:13.5pt;text-align:center;margin:0 0 1mm}.sub{text-align:center;font-family:'GL';font-size:7.4pt;color:#555;margin-bottom:2mm}
h2{font-family:'GL';font-weight:400;font-size:11pt;border-bottom:1.2pt solid #222;margin:5pt 0 3pt;padding-bottom:1pt}h2.pb{break-before:page}
b{font-family:'GL';font-weight:400}
.three{display:grid;grid-template-columns:1fr 1fr 1fr;border:.8pt solid #333;font-size:7.9pt}.col{padding:4pt 5pt;min-width:0}.col+.col{border-left:.6pt solid #999}
.lab{font-family:'GL';font-size:7.6pt;color:#1f4e9a;margin-bottom:2pt}.chs{display:flex;flex-wrap:wrap;gap:1pt 8pt;margin-top:3pt}.ok{color:#c0392b}
.cond{border:.6pt solid #000;padding:2pt 4pt;margin:3pt 0}.ci{display:block;padding-left:1.9em;text-indent:-1.9em}.ck{margin-right:3pt}.dm{text-align:center;margin:2pt 0}
.fig{text-align:center;margin:2pt 0}.fig img{max-width:100%}.scan{width:100%}
.box{border:.6pt solid #999;padding:4pt 7pt;margin-top:2.5mm}.key{background:#fbf6ee;border-color:#b7701b}.box p{margin:2pt 0}.box ol{margin:2pt 0 2pt 1.2em;padding:0}
table.cmp{border-collapse:collapse;width:100%;margin-top:2.5mm}
.cmp th,.cmp td{border:.5pt solid #999;padding:2.5pt 4pt;font-size:7.8pt;vertical-align:top;text-align:left}.cmp th{font-family:'GL';font-weight:400;background:#eef0f3;white-space:nowrap}
.cmp td{width:40%}.cmp td.v{width:auto;white-space:nowrap;font-family:'GL'}"""

fix = lambda s: re.sub(r'\\\[([\s\S]+?)\\\]', lambda m: '<div class="dm">\\(\\displaystyle ' + m.group(1) + '\\)</div>', s)
h = f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>{fix(body)}</body></html>'
h = re.sub(r'\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), h)
open(os.path.join(RUN, 'b1718_src.html'), 'w').write(h)
subprocess.run(['node', os.path.join(RUN, 'render3.js'), 'b1718_src.html', 'b1718_tmp.pdf', 'bg'], cwd=RUN, check=True)
os.replace(os.path.join(RUN, 'b1718_tmp.pdf'), OUT)
