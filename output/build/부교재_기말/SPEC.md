# 부교재(미적분Ⅰ) 04·05·06단원 문항 전사 작업 명세

SCR = /tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad
Source page images (170dpi), named by PRINTED page number PPP: `SCR/wb3/img/fullPPP.png` (whole page) and `SCR/wb3/img/pPPPL.png`, `pPPPR.png` (left/right column halves).
Available printed pages: 78–103, 106–131, 134–161, 164–189 (104–105, 132–133, 162–163 are chapter-opening pages without problems).

Chapters: **04 도함수의 활용(1)** problems 1–72 (p.78–103), **05 도함수의 활용(2)** problems 1–68 (p.106–131), **06 부정적분과 정적분** problems 1–76 (p.134–161), **07 정적분의 활용** problems 1–72 (p.164–189).
Keys: ch04 problem n → `'D%d' % n`, ch05 → `'M%d' % n`, ch06 → `'I%d' % n`, ch07 → `'J%d' % n`.
Concept-summary pages (if any) have no problems: skip them.

## Official answers (빠른 정답) — use these; verify each with your own solution (sympy where helpful) and report any mismatch
04 도함수의 활용(1): 1 25 2③ 3③ 4① 5⑤ 6④ 7 33 8④ 9③ 10⑤ 11④ 12③ 13 67 14 28 15② 16② 17 6 18④ 19② 20⑤ 21③ 22⑤ 23① 24② 25③ 26④ 27③ 28⑤ 29 11 30② 31③ 32④ 33⑤ 34⑤ 35⑤ 36④ 37③ 38 59 39③ 40 50 41④ 42⑤ 43④ 44⑤ 45 102 46② 47 19 48③ 49④ 50② 51⑤ 52① 53③ 54① 55② 56 4 57③ 58⑤ 59④ 60⑤ 61④ 62 39 63⑤ 64 11 65 42 66 105 67 9 68 13 69① 70 380 71① 72①
05 도함수의 활용(2): 1⑤ 2⑤ 3③ 4④ 5③ 6⑤ 7② 8① 9⑤ 10④ 11② 12② 13⑤ 14④ 15④ 16② 17 22 18④ 19① 20 11 21① 22④ 23 35 24 13 25⑤ 26⑤ 27② 28② 29② 30 5 31⑤ 32 19 33⑤ 34③ 35④ 36 10 37 17 38① 39③ 40④ 41④ 42④ 43 7 44③ 45 15 46 8 47② 48 27 49③ 50① 51① 52② 53⑤ 54 65 55 51 56 21 57 61 58 14 59 296 60③ 61 40 62 5 63 19 64 38 65 58 66② 67 108 68 483
06 부정적분과 정적분: 1④ 2② 3① 4③ 5② 6③ 7④ 8⑤ 9 39 10④ 11④ 12 27 13① 14 84 15③ 16② 17② 18③ 19 100 20 45 21① 22④ 23③ 24① 25② 26 11 27① 28 9 29④ 30① 31 32 32② 33④ 34④ 35② 36⑤ 37② 38④ 39① 40② 41④ 42③ 43 21 44④ 45⑤ 46④ 47① 48④ 49 10 50 16 51① 52② 53③ 54② 55 10 56 25 57 5 58② 59 10 60 7 61④ 62④ 63 8 64 110 65⑤ 66 13 67① 68④ 69⑤ 70② 71⑤ 72④ 73② 74④ 75④ 76⑤
07 정적분의 활용: 1③ 2⑤ 3① 4② 5④ 6 6 7 40 8④ 9 4 10④ 11① 12③ 13④ 14④ 15 42 16③ 17④ 18② 19④ 20② 21② 22⑤ 23⑤ 24④ 25② 26③ 27① 28 127 29③ 30③ 31① 32 63 33② 34⑤ 35② 36④ 37 16 38 28 39③ 40 5 41① 42⑤ 43 36 44④ 45⑤ 46⑤ 47② 48② 49② 50⑤ 51 14 52① 53 6 54④ 55③ 56③ 57④ 58⑤ 59 80 60④ 61② 62③ 63⑤ 64④ 65④ 66③ 67 16 68⑤ 69 17 70③ 71⑤ 72③
(A number without a circle = 단답형/short answer.) If the official answer looks wrong after careful checking, keep the official one in the item and flag MISMATCH in the report with your reasoning.

## Output 1: `SCR/wb3/parts/items_pK.py`
```python
# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, 'SCR/wb2/parts')   # use the absolute path
from items_common import COND, BOGI, FIG
I = {}
I['D12'] = (r"""body html""", ['c1','c2','c3','c4','c5'] or None, '③' or '36', '출처 그대로, e.g. 2025년 수능특강 [25009-0083]')
D = {'D12': (4, '유형 n 이름 (구역: 유형/대표기출/Level Up/평가원 기출)', 'one-line solution sketch / note')}   # difficulty 1–10
```
Body rules (identical to the existing DB; see examples in `/home/user/Finale/output/build/부교재전문항/items.py` and `SCR/wb2/parts/items_p1.py`):
- Korean text with inline math `\(...\)`; display math on its own line `\[...\]` (long limits/fractions/integrals display; piecewise functions always display with `\begin{cases}...\end{cases}`). Integrals: `\displaystyle\int_0^2 f(t)\,dt` inline or display.
- Use `&lt;` `&gt;` for < > in TEXT and inside math (auto-converted) — never a bare `<` in text.
- Conditions boxes (가)(나)… → `COND([('가', r"..."), ('나', r"...")])`; a box without labels → `COND([('', r"...")])`.
- 보기 ㄱㄴㄷ → `BOGI([('ㄱ', r"..."), ...])` and choices `['T:ㄱ','T:ㄴ','T:ㄱ, ㄷ',...]` (prefix `T:` = plain text choice).
- Other choices: LaTeX strings without `\( \)`, e.g. `r'\dfrac32'`, `'-1'`, `r'2\sqrt6'`.
- Do NOT include the point marker [3점]/[4점] in the body. Short-answer: choices `None`, answer as number string.
- A figure → `FIG('fig_D12', W)` where it appears (W in pt, 110–150 typical; column 252pt).
- Raw strings; single quotes inside HTML attributes. Transcribe faithfully (no rewording, no variation). Keep "(단, ...)" notes and underlines (`<u>...</u>`).
- In `D[key][1]` record the section the problem sits in, e.g. '유형2 함수의 증가와 감소 · 대표기출', '유형3 · 일반', 'Level Up', '평가원 기출'. This matters: the exam-analysis uses section kinds.

## Output 2: `SCR/wb3/parts/figs_pK.py`
Matplotlib code drawing every figure of your part to `SCR/wb3/parts/fig_D12.svg` etc. Start with `exec(open('SCR/wb2/figs_head.py').read())` (absolute path) — it defines `plt`, `axes(ax,xl,yl,...)`, `dash(ax,xs,ys)` and text in the exam equation font (ASCII letters/digits/()=- converted; avoid Greek). Reproduce faithfully (shape, tick labels, open/closed dots: open `ax.plot(x,y,'o',ms=3,mfc='white',mec='k',mew=0.8)`, closed `'ko',ms=3`, dashed guides, shaded regions for areas with light gray). Render each svg to PNG (pymupdf `pymupdf.open(svg).convert_to_pdf()`) and LOOK at it beside the source crop; fix overlaps.

## Output 3: `SCR/wb3/parts/report_pK.md`
One line per key: answer (official) | your check (OK / MISMATCH + why) | difficulty | figure yes/no | section.

Difficulty scale (1–10): 1 = plug-in, 3 = routine 3점, 5 = typical 4점, 7 = hard 4점 (21번급 아래), 8+ = killer. Include computation length.

Finally: `python3 -c "import sys; sys.path.insert(0,'SCR/wb3/parts'); import items_pK"` must import, and `cd SCR/wb3/parts && node SCR/wb2/katex_check.js items_pK` must print OK (if katex_check.js can't find the module from wb3/parts, copy it into wb3/ and adjust the path; do not edit the wb2 copy).
