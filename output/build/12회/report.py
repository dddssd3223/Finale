# -*- coding: utf-8 -*-
# 개인 성적표 (A4 세로)
import os, subprocess, sys
from content3 import Q, ANS
from build3 import font_css, HERE, KATEX_CSS

MARK = [2, 4, 2, 5, 3, 2, 4, 1, 5, 3, 2, 4, 1, 3, 1, 5, 4, 4]      # OMR 판독 (12회, 확대 대조)
SA = [('단답형 1', [('(1)', 3, 3), ('(2)', 3, 0), ('(3)', 4, 0)]),
      ('서술형 1', [('(1)', 2, 2), ('(2)', 4, 3), ('(3)', 4, 4)])]
CIRC = '①②③④⑤'
CSS = r"""
@page{size:A4;margin:16mm 15mm 14mm 15mm}
html,body{margin:0;background:#fff}
body{font-family:'GL';font-size:9.5pt;color:#000}
h1{font-size:17pt;font-weight:400;text-align:center;margin:0 0 3pt;letter-spacing:1pt;-webkit-text-stroke:.3pt #000}
.sub{text-align:center;font-size:10pt;margin-bottom:10pt}
.rule{border-top:2.2pt solid #000;border-bottom:.7pt solid #000;height:1.5pt;margin:0 0 10pt}
table{border-collapse:collapse;width:100%}
td,th{border:.6pt solid #000;padding:3pt 2pt;text-align:center;font-weight:400}
th{background:#ececec;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.info td,.info th{padding:5pt 4pt;font-size:10.5pt}
h2{font-size:11pt;font-weight:400;margin:14pt 0 5pt;-webkit-text-stroke:.2pt #000}
.x{color:#c8141a}
.sum td,.sum th{font-size:11pt;padding:6pt 4pt}
.sum .tot{font-size:15pt;-webkit-text-stroke:.3pt #000}
.note{font-size:9.5pt;line-height:1.7;border:.6pt solid #000;padding:6pt 9pt}
"""

def build(out):
    mc = [(n, ANS[n], MARK[n-1], Q[n][0]) for n in range(1, 19)]
    mc_score = sum(p for n, a, m, p in mc if a == m)
    sa_score = sum(g for _, items in SA for _, _, g in items)
    def row(cells, tag='td'):
        return '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
    def part(rng):
        r = row(['번호'] + [str(n) for n in rng], 'th')
        r += row(['정답'] + [CIRC[ANS[n]-1] for n in rng])
        r += row(['표기'] + [(CIRC[MARK[n-1]-1] if MARK[n-1] == ANS[n] else f'<span class="x">{CIRC[MARK[n-1]-1]}</span>') for n in rng])
        r += row(['채점'] + [('○' if MARK[n-1] == ANS[n] else '<span class="x">×</span>') for n in rng])
        r += row(['배점'] + [f'{Q[n][0]:.1f}' for n in rng])
        r += row(['득점'] + [(f'{Q[n][0]:.1f}' if MARK[n-1] == ANS[n] else '<span class="x">0</span>') for n in rng])
        return '<table style="margin-bottom:6pt">' + r + '</table>'
    sa = '<table>' + row(['문항', '(1)', '(2)', '(3)', '소계'], 'th')
    for name, items in SA:
        sa += row([name] + [f'{g} / {p}' if g == p else f'<span class="x">{g}</span> / {p}' for _, p, g in items] +
                  [f'{sum(g for *_, g in items)} / {sum(p for _, p, _ in items)}'])
    sa += '</table>'
    h = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}"><style>{font_css()}{CSS}</style></head><body>
<h1>2026학년도 1학기 중간고사 성적표 (12회)</h1>
<div class="sub">미적분Ⅰ · 시행일 2026년 10월 13일(화) 1교시</div><div class="rule"></div>
<table class="info">{row(['학년','반','번호','이름','과목'],'th')}{row(['2','3','13','우정빈','미적분Ⅰ'])}</table>
<h2>■ 점수 요약</h2>
<table class="sum">{row(['선택형 (80점)','단답형 (10점)','서술형 (10점)','총점 (100점)'],'th')}
{row([f'{mc_score:.1f}', str(sum(g for *_, g in SA[0][1])), str(sum(g for *_, g in SA[1][1])), f'<span class="tot">{mc_score + sa_score:.1f}</span>'])}</table>
<h2>■ 선택형 채점 결과 ({sum(1 for n, a, m, p in mc if a == m)}문항 정답 / 18문항)</h2>
{part(range(1, 10))}{part(range(10, 19))}
<h2>■ 서답형 채점 결과</h2>
{sa}
<h2>■ 감점 내역</h2>
<div class="note">
· 선택형 3번 (−4.0점): ② 3을 표기, 정답은 ① 2. \\(f'(x)=2x(x^2+ax+1)+(x^2+2)(2x+a)\\)이므로 \\(f'(1)=2(2+a)+3(2+a)=5(2+a)=20\\), \\(a=2\\)입니다. 첫 항의 \\(2x\\)를 \\(1\\)로 계산하면 \\(4(2+a)=20\\), \\(a=3\\)이 나옵니다.<br>
· 선택형 15번 (−4.7점): ① ㄱ을 표기, 정답은 ② ㄱ, ㄴ. ㄴ에서 \\(x=0\\)의 좌미분계수는 \\(\\lim_{{x\\to0-}}\\dfrac{{p(x)(1-x)}}{{x}}=p'(0)\\), 우미분계수는 \\(\\lim_{{x\\to0+}}\\dfrac{{p(x)(x-1)}}{{x}}=-p'(0)\\)이므로 \\(p'(0)=0\\)까지 필요합니다. \\(x=2\\)에서는 \\(p(2)(1-3)=0\\). 따라서 \\(p\\)는 \\(x^2(x-2)\\)로 나누어떨어집니다(참). ㄷ은 \\(\\{{f(x)\\}}^2\\)이 \\(x=0\\) 근처에서 \\((x-1)^2\\)으로 이어져 \\(p=x-2\\)가 반례(거짓).<br>
· 선택형 18번 (−5.2점): ④ −5를 표기, 정답은 ③ −6. \\(f-x=x^2(x-1)(x-w)\\), \\(w=\\pm3\\). \\(w=3\\)이면 \\(g=f\\) (\\(1\\le x\\le3\\)), \\(g(-2)=-2\\), \\(g(2)=f(2)=-2\\)로 비 \\(1\\). \\(w=-3\\)이면 \\(g=f\\) (\\(-3\\le x\\le1\\)), \\(g(-2)=f(-2)=-2+4\\cdot(-3)\\cdot1=-14\\), \\(g(2)=2\\)로 비 \\(-7\\). 합 \\(-6\\).<br>
· 단답형 1 (2) (−3점): 8을 썼고 정답은 10. \\(f=c(x-4)^2(x-14)\\)에서 \\(f(s)=f'(s)(s+2)\\)를 정리하면 \\((s-4)(s^2-4s-60)=0\\), \\(s>4\\)이므로 \\(s=10\\)입니다(8은 원본 문항 \\(g(\\tfrac{{21}}2)=0\\)일 때의 값).<br>
· 단답형 1 (3) (−4점): 421을 썼고 정답은 85. 두 접선이 같은 직선 \\(y=3x+6\\)이어야 하므로 \\(f'(10)=c\\cdot6\\cdot(-2)=3\\), \\(c=-\\tfrac14\\), \\(g(13)=-\\tfrac14\\cdot81\\cdot(-1)=\\tfrac{{81}}4\\)입니다.<br>
· 서술형 1 (2) (−1점): \\(k<0\\)인 경우만 남겼는데, \\(k=1\\)(중근, \\(f=(x-1)^2\\))이면 \\(f(x^2)=(x^2-1)^2\\)이라 불연속점이 \\(\\pm1\\)뿐이어서 조건을 만족합니다. 9회 서술형과 같은 실수입니다. 이 경우를 남겨 두고 (3)에서 극한 조건으로 배제해야 합니다.
</div>
</body></html>"""
    src = os.path.join(HERE, 'rep_src.html')
    open(src, 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'rep_src.html', 'rep_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'rep_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
