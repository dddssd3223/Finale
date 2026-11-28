# 9회 18번 해설 영상(자막형) — 장면 HTML + 상태 목록(json) 생성
import sys, json, os, re
B = '/home/user/Finale/output/build/기말'
sys.path.insert(0, B + '/지침'); import haeseol2 as H
sys.path.insert(0, B + '/9회'); import content3 as c
OUT = os.path.dirname(os.path.abspath(__file__))
it = c.ITEMS[18]
F = H.FONTS
CS = '①②③④⑤'

def cond_html():
    rows = ''.join(f'<div class="cr"><span class="cl">{"㈎㈏㈐"["가나다".index(a)]}</span><span>{t}</span></div>' for a, t in it['cond'])
    return f'<div class="cond">{rows}</div>'

prob = (f'<div class="pb"><div class="qn">18.</div><div class="qt">{it["body"]}{cond_html()}'
        f'<div class="chs">' + ''.join(f'<span>{CS[i]} \\({x}\\)</span>' for i, x in enumerate(it['choices'])) + '</div></div></div>')

# 장면: (머리 제목, [(블록 html, 자막)])  — 블록이 하나씩 나타나고 그때 자막이 바뀐다
S = []
S.append(('title', [('<div class="tt"><div class="t1">미적분Ⅰ 기말 모의고사 9회</div><div class="t2">18번 해설</div><div class="t3">적분 구간이 움직이는 함수와 감소 구간</div></div>', '9회 18번 해설을 시작한다.')]))
S.append(('문제', [(prob, '사차함수 f(x)로 만든 함수 g(x)가 세 조건을 만족시키도록 하는 k의 최댓값을 구하는 문제다.'),
                    ('<div class="hl">조건 ㈎ ㈐ 는 g가 일정한 곳, 조건 ㈏ 는 g가 감소하는 곳을 말한다.</div>', '조건 ㈎와 ㈐는 g가 일정한 구간이고, 조건 ㈏는 g가 감소하는 구간이다.')]))
S.append(('생각의 시작', [('<div class="think">적분 구간의 두 끝이 \\(x\\)에 따라 움직이므로 \\(g\'(x)\\)를 구하고,<br>\\(g(x)\\)가 일정한 곳과 감소하는 곳을 \\(f\\)의 부호로 읽는다.</div>', '먼저 g를 미분해서 g가 일정한 곳과 감소하는 곳을 f의 부호로 읽어 낸다.')]))
S.append(('실전 개념', [('<div class="cbox"><div class="ch">적분 구간이 움직이는 함수의 미분</div>\\[\\frac{d}{dx}\\int_{-x}^{kx} m(t)\\,dt=k\\,m(kx)+m(-x)\\]<div class="cb">위끝은 \\(x\\)의 \\(k\\)배 빠르기로 움직이므로 \\(k\\)가 곱해지고,<br>아래끝은 반대 방향으로 움직이므로 부호가 바뀌어 더해진다.</div></div>', '위끝이 kx이면 k가 곱해지고, 아래끝이 -x이면 부호가 바뀌어 더해진다.')]))
S.append(('STEP 1 · g\'(x)의 부호', [
    ('<p>\\(m(t)=f(t)-|f(t)|\\)로 두면</p>\\[m(t)=\\begin{cases}0 & (f(t)\\ge0)\\\\ 2f(t) & (f(t)<0)\\end{cases}\\]', '피적분함수를 m(t)로 두면 f가 0 이상인 곳에서는 0이고, f가 음수인 곳에서만 2f(t)로 음수다.'),
    ('<p>\\(f(-t)=f(t)\\)이므로 \\(m(-t)=m(t)\\)이다.</p>', 'f가 짝함수이므로 m도 짝함수다.'),
    ('\\[g\'(x)=k\\,m(kx)+m(x)\\le 0\\]', '따라서 g의 도함수는 k m(kx)와 m(x)의 합이고, 두 항이 모두 0 이하다.'),
    ('<div class="hl">\\(g\'(x)<0 \\iff f(kx)<0\\ \\text{또는}\\ f(x)<0\\)</div>', 'g가 감소하는 것은 f(kx) 또는 f(x)가 음수일 때뿐이고, 나머지에서는 g가 일정하다.')]))
S.append(('STEP 2 · f의 모양', [
    ('<p>\\(b\\le0\\)이면 \\(0\\) 근처에서 이미 감소하거나, 감소하는 곳이 아예 없다.</p>', 'b가 0 이하이면 0 근처에서 바로 감소하거나 감소하는 곳이 없어서 조건과 맞지 않는다.'),
    ('\\[f(x)=(x^2-\\alpha^2)(x^2-\\beta^2)\\quad(0<\\alpha<\\beta)\\]', '그래서 b는 양수이고, f는 두 양수 α, β로 이렇게 인수분해된다.'),
    ('<div class="hl">\\(f(t)<0 \\iff \\alpha<|t|<\\beta\\)</div>', 'f가 음수인 곳은 절댓값이 α와 β 사이인 곳이다.'),
    ('\\[g\'(x)<0 \\iff \\frac{\\alpha}{k}<x<\\frac{\\beta}{k}\\ \\ \\text{또는}\\ \\ \\alpha<x<\\beta\\]', 'x가 양수일 때 g가 감소하는 구간은 두 개다. α/k부터 β/k까지, 그리고 α부터 β까지다.')]))
S.append(('STEP 3 · 두 감소 구간 잇기', [
    ('<p>\\(k>1\\)이면 감소는 \\(x=\\dfrac{\\alpha}{k}\\)에서 시작하고 \\(x=\\beta\\)에서 끝난다.</p>\\[\\frac{\\alpha}{k}=1,\\ \\beta=9\\ \\to\\ \\alpha=k,\\ \\beta=9\\]', 'k가 1보다 크면 감소는 α/k에서 시작해 β에서 끝난다. 조건 ㈎와 ㈐에 맞추면 α는 k, β는 9다.'),
    ('<p>두 구간 \\(1<x<\\dfrac9k\\)와 \\(k<x<9\\) 사이에 틈이 생기면 안 된다.</p>', '이제 두 감소 구간, 1부터 9/k까지와 k부터 9까지가 끊기지 않아야 한다.'),
    ('FIG', '틈이 생기면 그 사이에서 g가 일정해져서 조건 ㈏를 어긴다. k가 4이면 9/4와 4 사이가 비어 버린다.'),
    ('\\[\\frac9k\\ge k\\ \\to\\ k^2\\le 9\\ \\to\\ k\\le 3\\]', '따라서 9/k가 k 이상이어야 하고, k는 3 이하다.')]))
S.append(('확인과 함정', [
    ('<p>\\(k=3\\)이면 \\(f(x)=(x^2-9)(x^2-81)\\), 감소 구간은 \\(1<x<3\\)과 \\(3<x<9\\)이다.</p><p>\\(x=3\\) 한 점에서만 \\(g\'(x)=0\\)이므로 \\(1<x<9\\)에서 감소한다.</p>', 'k가 3이면 두 구간이 x=3에서 맞닿고, 그 한 점에서만 도함수가 0이므로 1과 9 사이에서 계속 감소한다.'),
    ('<div class="trap">함정 · \\(\\alpha=k<\\beta=9\\)만 보고 \\(k\\)의 최댓값을 \\(9\\)로 고르기 쉽다.</div>', '두 구간이 이어져야 한다는 점을 놓치면 α<β만 보고 9를 고르게 된다.'),
    ('<div class="ans"><span>정답</span> ② \\(3\\)</div>', '따라서 k의 최댓값은 3이고, 정답은 2번이다.')]))

# 수직선 그림: k=3(이어짐)과 k=4(틈)
def nline(k, y, ok):
    X = lambda v: 140 + v * 140
    a1, b1, a2, b2 = 1, 9 / k, k, 9
    s = f'<text x="20" y="{y+8}" class="lab">k = {k}</text><line x1="{X(0)}" y1="{y}" x2="{X(10)}" y2="{y}" class="ax"/>'
    for v in range(0, 11): s += f'<line x1="{X(v)}" y1="{y-6}" x2="{X(v)}" y2="{y+6}" class="tk"/><text x="{X(v)}" y="{y+34}" class="tn">{v}</text>'
    s += f'<rect x="{X(a1)}" y="{y-34}" width="{X(b1)-X(a1)}" height="18" rx="4" class="b1"/><rect x="{X(a2)}" y="{y-58}" width="{X(b2)-X(a2)}" height="18" rx="4" class="b2"/>'
    if not ok: s += f'<rect x="{X(b1)}" y="{y-64}" width="{X(a2)-X(b1)}" height="54" class="gap"/><text x="{(X(b1)+X(a2))/2}" y="{y-74}" class="gt">틈: g 일정</text>'
    return s
FIG = (f'<svg class="fig" viewBox="0 0 1700 350"><g>{nline(3, 140, True)}{nline(4, 300, False)}</g>'
       f'<g class="lg"><rect x="1100" y="12" width="22" height="14" rx="3" class="b1"/><text x="1130" y="25">\u03b1/k &lt; x &lt; \u03b2/k</text><rect x="1360" y="12" width="22" height="14" rx="3" class="b2"/><text x="1390" y="25">\u03b1 &lt; x &lt; \u03b2</text></g></svg>')

css = f"""
@font-face{{font-family:'SJ';src:url('file://{F}/shinjung.ttf')}}
@font-face{{font-family:'BD';src:url('file://{F}/busan_M.ttf')}}
@font-face{{font-family:'BDB';src:url('file://{F}/busan_B.ttf')}}
@font-face{{font-family:'HYEQ';src:url('file://{F}/hyhwpeq_web.ttf')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1920px;height:1080px;background:#fff;font-family:'SJ';color:#1d2433;overflow:hidden}}
.scene{{position:absolute;inset:0;display:none}} .scene.on{{display:block}}
.hd{{position:absolute;left:0;top:0;right:0;height:96px;background:#f3f6fb;border-bottom:3px solid #3a66b0;display:flex;align-items:center;padding:0 80px;gap:28px;font-family:'BDB';font-size:34px;color:#1f3c74}}
.hd .chip{{background:#3a66b0;color:#fff;border-radius:8px;padding:6px 18px;font-size:28px}}
.main{{position:absolute;left:120px;right:120px;top:150px;bottom:190px;font-size:40px;line-height:1.9}}
.main p{{margin:6px 0}} .r{{opacity:0;transition:none}} .r.v{{opacity:1}} .r.new{{animation:fi .0s}}
.cap{{position:absolute;left:0;right:0;bottom:0;height:150px;background:#16213a;color:#fff;font-family:'BD';font-size:38px;display:flex;align-items:center;justify-content:center;padding:0 140px;text-align:center;line-height:1.5}}
.tt{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px;top:-150px}}
.t1{{font-family:'BD';font-size:40px;color:#5b6b85}} .t2{{font-family:'BDB';font-size:110px;color:#1f3c74}} .t3{{font-family:'BD';font-size:42px;color:#3a66b0}}
.pb{{display:flex;gap:22px;font-size:38px;line-height:1.85}} .qn{{font-family:'BDB';color:#1f3c74}}
.cond{{border:2px solid #333;padding:14px 26px;margin:14px 0}} .cr{{display:flex;gap:18px}} .cl{{font-family:'BD'}}
.chs{{display:flex;gap:70px;margin-top:10px}}
.hl{{margin-top:24px;background:#fff6d6;border-left:8px solid #e3a600;padding:14px 28px;font-family:'BD';font-size:38px}}
.think{{background:#eef4ff;border-radius:18px;padding:40px 54px;font-size:46px;line-height:1.9;font-family:'BD';color:#1f3c74}}
.cbox{{border:3px solid #3a66b0;border-radius:18px;padding:30px 50px}} .ch{{font-family:'BDB';color:#3a66b0;font-size:40px}} .cb{{font-family:'BD';font-size:36px}}
.trap{{background:#ffecec;border-left:8px solid #d64545;padding:16px 28px;font-family:'BD';margin-top:20px}}
.ans{{margin-top:40px;font-family:'BDB';font-size:64px;color:#1f3c74}} .ans span{{background:#3a66b0;color:#fff;border-radius:10px;padding:4px 22px;font-size:40px;margin-right:24px;vertical-align:middle}}
.fig{{width:100%;margin:6px 0}} .fig .ax{{stroke:#333;stroke-width:3}} .fig .tk{{stroke:#333;stroke-width:2}}
.fig .tn{{font-family:'SJ';font-size:26px;text-anchor:middle}} .fig .lab{{font-family:'BDB';font-size:32px;fill:#1f3c74}}
.fig .b1{{fill:#6f9be0}} .fig .b2{{fill:#e39b3a}} .fig .gap{{fill:#d64545;opacity:.18}} .fig .gt{{font-family:'BDB';font-size:28px;fill:#d64545;text-anchor:middle}}
.fig .lg text{{font-family:'BD';font-size:26px}}
.katex{{font-size:1.05em}} .katex-display{{margin:.35em 0}}
"""
html = [f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{H.KATEX_CSS}"><style>{css}</style></head><body>']
states = []
for si, (head, blocks) in enumerate(S):
    hd = '' if head == 'title' else f'<div class="hd"><span class="chip">9회 18번</span><span>{head}</span></div>'
    body = ''.join(f'<div class="r" data-i="{bi}">{FIG if b == "FIG" else b}</div>' for bi, (b, _) in enumerate(blocks))
    html.append(f'<section class="scene" id="s{si}">{hd}<div class="main">{body}</div><div class="cap"></div></section>')
    for bi, (_, cap) in enumerate(blocks):
        n = len(re.sub(r'\s', '', cap)); states.append({'s': si, 'upto': bi, 'cap': cap, 'dur': round(max(3.0, n / 6.5 + 1.6), 1)})
html.append('</body></html>')
doc = H.fx(''.join(html))
doc = re.sub(r'\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]', lambda m: m.group(0).replace("'", '^{\\prime}'), doc)
open(os.path.join(OUT, 'page_src.html'), 'w').write(doc)
json.dump(states, open(os.path.join(OUT, 'states.json'), 'w'), ensure_ascii=False, indent=0)
print(len(states), 'states', round(sum(s['dur'] for s in states)), 's')
