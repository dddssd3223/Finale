# -*- coding: utf-8 -*-
# 개인 성적표 (A4 세로)
import os, subprocess, sys
from content3 import Q, ANS
from build3 import font_css, HERE, KATEX_CSS

MARK = [3, 4, 5, 1, 5, 4, 1, 2, 3, 2, 4, 1, 3, 2, 4, 5, 3, 2]      # OMR 판독 (8회, 300dpi 재확인)
SA = [('단답형 1', [('(1)', 3, 3), ('(2)', 3, 3), ('(3)', 4, 4)]),
      ('서술형 1', [('(1)', 2, 2), ('(2)', 4, 4), ('(3)', 4, 4)])]
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
<h1>2026학년도 1학기 중간고사 성적표 (8회)</h1>
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
· 감점 없음: 선택형 18문항, 단답형, 서술형 모두 만점입니다.<br>
· 참고(감점 아님): 서술형 (3)에서 \\(h(x)=x^2-4x+5\\)가 실근을 갖지 않음(판별식 \\(-4<0\\))을 한 줄 확인해 두면 (2)에서 세운 조건 \\(h(x)>0\\)과 앞뒤가 완전히 맞습니다.
</div>
</body></html>"""
    src = os.path.join(HERE, 'rep_src.html')
    open(src, 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'rep_src.html', 'rep_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'rep_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
