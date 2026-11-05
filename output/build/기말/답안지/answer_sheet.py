# -*- coding: utf-8 -*-
"""미적분I 서답형 답안지: 학교 실제 서답형 답안지(통합사회2, 2026 2학기 중간) 양식을 1:1로 옮김.
선 위치·굵기, 글자 크기·위치는 원본 600dpi 스캔 실측(글자는 같은 글꼴로 그려 잉크 상자를 원본과 맞춘 값, 오차 1pt 이내).
사용: python3 answer_sheet.py <출력 PDF> <글꼴 폴더: malgunbd.ttf·malgun.ttf(맑은 고딕 Bold·Regular, 원본 양식 글꼴, 저장소에 넣지 않음)>"""
import sys, os, subprocess, json
import numpy as np, fitz
OUT, FD = sys.argv[1], os.path.abspath(sys.argv[2])
SUBJ, EXAM, GRADE = '미적분I', '기말고사', '2학년'
# ---- 원본 실측 (pt) ----
VX = dict(L=54.9, N=91.5, B1=407.2, B2=433.9, C1=460.8, C2=500.4, R=540.5)
VW = dict(L=1.8, R=1.8)                          # 바깥 세로선 굵기 (나머지 0.55, 원본 단면 실측)
TOP, TOPW, HSPLIT, HBOT, HBOTW, BOT, BOTW = 215.0, 2.0, 238.3, 260.0, 0.6, 755.8, 1.75
ROWW = 0.55                                       # 번호 사이 가로선 굵기
INFO = (57.0, 139.6, 540.0, 169.7, 1.5)           # 인적 사항 상자 x0,y0,x1,y1,굵기
DOT = (57.15, 539.5, 197.4)                       # 절취 점선
HOLES = [(109.25, 58.3), (144.6, 58.5), (280.9, 58.9), (316.1, 59.0), (452.4, 59.1), (488.1, 59.1),
         (121.5, 183.5), (156.9, 183.7), (449.9, 184.4), (485.4, 184.3)]
SCORE = dict(L=229.4, a=338.3, b=361.1, c=443.2, d=463.4, R=540.4, y0=774.1, y1=835.0, w=1.6)
# 원본과 같은 글자(크기 pt, 상자 x, y): 잉크 맞춤 값
FIX = {'hn': ('번호', 14.319, 60.08, 227.741), 'hd': ('답', 14.543, 207.876, 228.583), 'hr': ('란', 15.637, 277.621, 227.865),
       'hb': ('배점', 15.6, 417.9, 228.4), 'hc': ('채점', 14.299, 487.694, 218.229), 'h1': ('초검', 13.38, 468.472, 241.384),
       'h2': ('재검', 13.174, 508.561, 241.144), 's1': ('점', 15.876, 268.71, 795.57), 's2': ('수', 15.482, 291.783, 795.692),
       'c1': ('초', 12.502, 343.992, 787.784), 'c2': ('검', 12.769, 343.992, 806.648), 'e1': ('재', 12.502, 447.4, 787.9), 'e2': ('검', 12.769, 447.5, 806.7)}
FS = dict(title=19.28, info=13.2, no=15.8, sub=14.5, pt=13.4, tot=15.8)
# 원본 인적 사항 낱말의 잉크 왼쪽·위 (그대로 둠) — 내용만 이 회차로
INFO_T = [('2026년도', 69.84, 147.08), ('2학기', 138.09, 147.32), (EXAM, 184.76, 147.68), (GRADE, 263.93, 147.92),
          ('반', 323.67, 148.28), ('번', 363.14, 148.16), ('이름:', 389.17, 148.28)]
TITLE = [f'(&nbsp;{SUBJ}&nbsp;)과', '서답형', '답안지']; TGAP = (10.44, 13.56); TCX, TTOP = 297.64, 90.5
# 답란 구성: (번호, [(소문항, 높이, 배점)], 합계) — 서답형1 풀이 서술 4+6, 서답형2 답만 4+4+2
ROWS = [('1', [('(1)', 176.0, '4'), ('(2)', 199.8, '6')], '10'),
        ('2', [('(1) :', 40.0, '4'), ('(2) :', 40.0, '4'), ('(3) :', 40.0, '2')], '10')]

def html(texts, lines):
    css = f"""@font-face{{font-family:'MB';src:url('file://{FD}/malgunbd.ttf')}}@font-face{{font-family:'NR';src:url('file://{FD}/malgun.ttf')}}
@page{{size:210mm 297mm;margin:0}}body{{margin:0}}.pg{{position:relative;width:595.28pt;height:841.89pt;page-break-after:always;overflow:hidden}}
.t{{position:absolute;white-space:nowrap;line-height:1;color:#2e2e2e}}.r{{position:absolute;background:#1a1a1a}}
.h{{position:absolute;border:.6pt solid #222;border-radius:50%;box-sizing:border-box}}"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{texts if isinstance(texts, str) else "".join(texts)}{lines}</body></html>'
def span(txt, fs, x, y, w='B'):
    return f'<span class="t" style="left:{x:.3f}pt;top:{y:.3f}pt;font-size:{fs}pt;font-family:{"MB" if w == "B" else "NR"}">{txt}</span>'
def pdf(h, out):
    src = out + '.html'; open(src, 'w').write(h)
    js = f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{src}');await p.waitForTimeout(300);await p.pdf({{path:'{out}',width:'210mm',height:'297mm',printBackground:true}});await b.close()}})()"
    subprocess.run(['node', '-e', js], check=True); os.remove(src)
# 1차: 새 글자들의 잉크 상자(상자 왼쪽 위 기준 오프셋, 폭, 높이)를 잰다
NEW = [(t, FS['title'], 'B') for t in TITLE] + [(t, FS['info'], 'B') for t, _, _ in INFO_T] + \
      [(n, FS['no'], 'B') for n, _, _ in ROWS] + [(s[0], FS['sub'], 'B') for _, subs, _ in ROWS for s in subs] + \
      [(s[2], FS['pt'], 'R') for _, subs, _ in ROWS for s in subs] + [(t, FS['tot'], 'B') for _, _, t in ROWS]
tmp = OUT + '.m.pdf'
pdf(html(''.join(f'<div class="pg">{span(t, fs, 100, 100, w)}</div>' for t, fs, w in NEW), ''), tmp)
M = {}
for (t, fs, w), pg in zip(NEW, fitz.open(tmp)):
    pix = pg.get_pixmap(dpi=600); a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[..., 0]
    ys, xs = np.nonzero(a < 140); k = pix.width / 595.28
    M[(t, fs, w)] = (xs.min() / k - 100, ys.min() / k - 100, (xs.max() + 1 - xs.min()) / k, (ys.max() + 1 - ys.min()) / k)
os.remove(tmp)
def ink(t, fs, w, x0=None, y0=None, cx=None, cy=None):   # 잉크 상자를 원하는 곳에 두는 span
    dx, dy, iw, ih = M[(t, fs, w)]
    if cx is not None: x0 = cx - iw / 2
    if cy is not None: y0 = cy - ih / 2
    return span(t, fs, x0 - dx, y0 - dy, w)
T, L = [], []
def hl(x0, x1, y, w=0.55): L.append(f'<div class="r" style="left:{x0}pt;top:{y - w / 2:.3f}pt;width:{x1 - x0}pt;height:{w}pt"></div>')
def vl(x, y0, y1, w=0.55): L.append(f'<div class="r" style="left:{x - w / 2:.3f}pt;top:{y0}pt;width:{w}pt;height:{y1 - y0}pt"></div>')
def rect(x0, y0, x1, y1, w): hl(x0 - w / 2, x1 + w / 2, y0, w); hl(x0 - w / 2, x1 + w / 2, y1, w); vl(x0, y0, y1, w); vl(x1, y0, y1, w)
# 구멍 표시·점선
for cx, cy in HOLES: L.append(f'<div class="h" style="left:{cx - 3.2:.2f}pt;top:{cy - 3.2:.2f}pt;width:6.4pt;height:6.4pt"></div>')
x = DOT[0]
while x < DOT[1]: L.append(f'<div class="r" style="left:{x:.2f}pt;top:{DOT[2] - .45}pt;width:.9pt;height:.9pt;background:#444"></div>'); x += 1.55
# 제목 (원본처럼 가운데 맞춤, 낱말 간격 유지)
ws = [M[(t, FS['title'], 'B')][2] for t in TITLE]; x = TCX - (sum(ws) + sum(TGAP)) / 2
for i, t in enumerate(TITLE):
    T.append(ink(t, FS['title'], 'B', x0=x, y0=TTOP)); x += ws[i] + (TGAP[i] if i < 2 else 0)
# 인적 사항
rect(*INFO)
for t, x0, y0 in INFO_T: T.append(ink(t, FS['info'], 'B', x0=x0, y0=y0))
# 표
hl(VX['L'] - VW['L'] / 2, VX['R'] + VW['R'] / 2, TOP, TOPW); hl(VX['C1'], VX['R'], HSPLIT); hl(VX['L'], VX['R'], HBOT, HBOTW)
for key in FIX:
    t, fs, x0, y0 = FIX[key]; T.append(span(t, fs, x0, y0))
y = HBOT
for no, subs, tot in ROWS:
    y0 = y
    for i, (lab, ht, pt) in enumerate(subs):
        tall = ht > 60
        T.append(ink(lab, FS['sub'], 'B', x0=101.64, y0=(y + 10.5) if tall else None, cy=None if tall else y + ht / 2))
        T.append(ink(pt, FS['pt'], 'R', cx=(VX['B1'] + VX['B2']) / 2, cy=y + ht / 2))
        if i < len(subs) - 1: hl(VX['B1'], VX['B2'], y + ht)       # 원본처럼 배점 칸에만
        y += ht
    T.append(ink(no, FS['no'], 'B', cx=(VX['L'] + VX['N']) / 2, cy=(y0 + y) / 2))
    T.append(ink(tot, FS['tot'], 'B', cx=(VX['B2'] + VX['C1']) / 2, cy=(y0 + y) / 2))
    hl(VX['L'], VX['R'], y, BOTW if abs(y - BOT) < 1 else ROWW)
for kx, xx in VX.items():
    ys = TOP if kx in ('L', 'N', 'B1', 'C1', 'R') else (HBOT if kx == 'B2' else HSPLIT)
    vl(xx, ys, y, VW.get(kx, 0.5))
# 점수 칸
S = SCORE; rect(S['L'], S['y0'], S['R'], S['y1'], S['w'])
for kx in 'abcd': vl(S[kx], S['y0'], S['y1'])
pdf(html(f'<div class="pg">{"".join(T)}{"".join(L)}</div>', ''), OUT)
