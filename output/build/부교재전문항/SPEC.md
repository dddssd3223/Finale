# 부교재(미적분Ⅰ) 추가본 문항 전사 작업 명세

Source page images (170dpi): `SCR/wb2/pNNL.png`, `SCR/wb2/pNNR.png` (left/right half of PDF page NN) and `SCR/wb2/fullNN.png` (whole page).
SCR = /tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad

Chapters in this file: **01 함수의 극한** (problems 1–68) and **02 함수의 연속** (problems 1–56). Concept-summary pages have no problems: skip them.
Keys: ch01 problem n → `'L%d' % n`, ch02 problem n → `'C%d' % n`.

## Official answers (빠른 정답) — use these; verify each with your own solution (sympy where helpful) and report any mismatch
01 함수의 극한: 1①2②3④4③5③6④7③8 9 9 30 10①11④12 36 13 15 14①15⑤16①17①18②19④20②21③22③23⑤24③25②26⑤27②28②29①30 18 31 40 32⑤33①34③35 22 36①37③38①39 216 40 12 41①42 12 43③44④45 62 46③47②48②49③50①51⑤52④53 13 54②55③56②57 10 58 10 59③60④61②62③63①64③65 42 66⑤67④68 16
02 함수의 연속: 1⑤2②3④4 12 5④6⑤7 14 8 11 9 13 10 20 11⑤12 3 13②14②15④16④17③18 13 19④20④21③22⑤23 5 24④25④26 127 27⑤28 3 29 15 30②31 12 32③33 12 34③35 12 36②37②38①39④40②41③42①43④44 24 45 21 46 8 47⑤48③49④50⑤51①52 20 53②54④55 65 56 19
(A number without a circle = 단답형/short answer.)

## Output 1: `SCR/wb2/parts/items_pK.py`
```python
# -*- coding: utf-8 -*-
from items_common import COND, BOGI, FIG
I = {}
I['L12'] = (r"""body html""", ['c1','c2','c3','c4','c5'] or None, '③' or '36', '출처 그대로, e.g. 2025년 수능특강 [25009-0012]')
D = {'L12': (4, '유형 n 이름', 'one-line solution sketch / note')}   # difficulty 1–10 (same scale as below)
```
Body rules (exactly like the existing exam builder; see example `SCR/wbfull/items.py`):
- Korean text with inline math `\(...\)`; display math on its own line `\[...\]` (use display for any limit/fraction-heavy expression that would be long inline; piecewise functions always display with `\begin{cases}...\end{cases}`).
- Use `&lt;` `&gt;` for < > in TEXT; inside math you may write `&lt;`/`&gt;` too (they are auto-converted) — never a bare `<` in text.
- Conditions boxes (가)(나)… → `COND([('가', r"..."), ('나', r"...")])`; a box without labels → `COND([('', r"...")])`.
- 보기 ㄱㄴㄷ → `BOGI([('ㄱ', r"..."), ...])` and choices as `['T:ㄱ','T:ㄴ','T:ㄱ, ㄷ',...]` (prefix `T:` = plain text choice).
- Other choices: LaTeX strings without `\( \)`, e.g. `r'\dfrac32'`, `'-1'`, `r'2\sqrt6'`.
- Do NOT include the point marker [3점]/[4점] in the body.
- A figure → `FIG('fig_L12', W)` placed where the figure appears (W = width in pt, 110–150 typical; column is 252pt).
- Short-answer problems: choices `None`, answer the number string.
- Use raw strings. Single quotes inside HTML attributes.
- Transcribe faithfully (no rewording, no variation). Keep "(단, ...)" notes.

## Output 2: `SCR/wb2/parts/figs_pK.py`
Matplotlib code that draws every figure of your part to `SCR/wb2/parts/fig_L12.svg` etc. Start the file with
`exec(open('SCR/wb2/figs_head.py').read())` (absolute path) — it defines `plt`, `axes(ax,xl,yl,...)` (axes with arrows, x/y/O labels), `dash(ax,xs,ys)`, and text in the exam equation font (ASCII letters/digits/()=- are converted; Greek not supported — avoid).
Reproduce the figure faithfully: same shape, tick labels, open (white fill) / closed (black) dots for piecewise graphs (`ax.plot(x,y,'o',ms=3,mfc='white',mec='k',mew=0.8)` for open, `'ko',ms=3` closed), dashed guide lines, labels like y=f(x). Run it and render each svg to PNG (pymupdf: `pymupdf.open(svg).convert_to_pdf()`) and LOOK at it next to the source crop; fix overlaps.

## Output 3: append a short report to `SCR/wb2/parts/report_pK.md`
List each key: answer (official) | your check (OK / MISMATCH + why) | difficulty | figure yes/no | scope flag (flag anything using 극대/극소, 평균값 정리, or 적분 — out of scope).

Difficulty scale (1–10): 1 = plug-in, 3 = routine 3점, 5 = typical 4점, 7 = hard 4점 (21번급 아래), 8+ = killer. Judge including amount of computation and statement length.

Finally run `python3 -c "import sys; sys.path.insert(0,'SCR/wb2/parts'); import items_pK"` to make sure it imports, and also test-render with KaTeX: `cd SCR/wb2/parts && node SCR/wb2/katex_check.js items_pK` must print OK.
