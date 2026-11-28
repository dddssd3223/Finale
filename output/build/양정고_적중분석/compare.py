# -*- coding: utf-8 -*-
"""양정고 실제 문항 ↔ 우리 자료 1:1 대조"""
import os, sys, subprocess, importlib.util
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
AIM = os.path.dirname(HERE)
CON = os.path.join(AIM, 'concept')
sys.path.insert(0, CON)
from build import CSS, font_css, KATEX_CSS, CIRC
import re
from extra import EXTRA
from calc import CALC

def load(r):
    s = importlib.util.spec_from_file_location(f'cc{r}', os.path.join(AIM, f'r{r}', 'content3.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
C = {r: load(r) for r in range(1, 6)}

# 실제 문항 crop: (쪽, x0, y0, x1, y1)  — 원본 1512×2016 기준
CROP = {
 '1': (1, 120, 800, 780, 1070), '2': (1, 120, 1265, 780, 1565), '3': (1, 770, 255, 1445, 545), '4': (1, 770, 700, 1445, 1135),
 '5': (1, 770, 1300, 1445, 1595), '6': (2, 85, 265, 775, 725), '7': (2, 60, 1055, 775, 1525), '8': (2, 760, 265, 1460, 885),
 '9': (2, 760, 1075, 1460, 1365), '10': (3, 40, 235, 765, 725), '11': (3, 40, 935, 765, 1585), '12': (3, 740, 225, 1455, 765),
 '13': (3, 740, 955, 1455, 1405), '14': (4, 100, 185, 775, 945), '15': (4, 760, 185, 1465, 1185), '16': (5, 40, 155, 775, 1240),
 '단답 1': (5, 760, 300, 1500, 965), '단답 2': (6, 140, 185, 805, 1505), '단답 3': (6, 790, 185, 1465, 615), '단답 4': (7, 190, 375, 795, 1795),
}

def rq(r, n):
    q = C[r].Q[n]; stem = q[1].replace('{PT}', '').replace('src="fig', f'src="file://{AIM}/r{r}/fig')
    cs = [c[2:] if c.startswith('T:') else rf'\({c}\)' for c in q[2]]
    return stem, cs, CIRC[C[r].ANS[n] - 1]

def rsa(r, i):
    m = C[r]; s = m.SA[i].replace(m.SAP, '').replace('src="fig', f'src="file://{AIM}/r{r}/fig')
    return s, None, m.SA_ANS[i]

def ex(i):
    e = EXTRA[i]; return e['q'], e['c'], CIRC[e['a'] - 1]

def cl(t, k):
    q, a = dict(CALC)[t][k]; return q, None, a

# 실제 번호, 등급, 우리 자료 이름, 문항, 한 줄 비교
PAIRS = [
 ('1', 'A', '4회 2번', rq(4, 2), '① 선지가 실제 문제의 설명 문장과 같다.'),
 ('2', 'A', '3회 3번', rq(3, 3), '자율 주행 시뮬레이션 + 보상 = 강화학습. 교과서 15쪽 사례 그대로.'),
 ('3', 'B', '1회 8번', rq(1, 8), '집합 ↔ 0/1 포함 여부 벡터. 실제는 벡터에서 집합을 거꾸로 찾는 방향.'),
 ('4', 'A', '2회 17번', rq(2, 17), '“유클리드는 작을수록, 코사인은 클수록 유사”, 정확도 비교 — 같은 함정.'),
 ('5', 'B', '1회 12번', rq(1, 12), '세 입력 가중합 → 활성화함수. 실제는 f(x)=x (x≥3)로 값 자체를 출력.'),
 ('6', 'A', '1회 17번', rq(1, 17), '③ IDF 방향 뒤집기 함정이 실제 ㄴ으로, ④가 실제 ㄷ으로.'),
 ('7', 'B', '3회 7번', rq(3, 7), '세 명제 (p∨q)∧r, (p⊕q) 연산 — 같은 식이 실제 진리표에.'),
 ('8', 'A', '3회 21번', rq(3, 21), 'ㄹ “d(a,a)=0, C(a,a)=1”이 실제 ㄱ. ㄷ “크기 정보” 문장이 실제 ㄴ·ㄷ의 배경.'),
 ('9', 'B', '1회 15번', rq(1, 15), 'AND 임곗값 범위 → 실제는 정수 c의 개수로.'),
 ('10', 'B', '1회 19번', rq(1, 19), '단어 집합들의 자카드 유사도 비교.'),
 ('11', 'A', '계산 연습 18번', cl('감성 분석', 1), '긍정 3 + 부정 1, n(P)=n(N)=5 → 1/2, 1/8, 긍정 — 숫자까지 같다.'),
 ('12', 'A', '3회 20번', rq(3, 20), '같은 U·p·n, a의 7번째 성분 1 → x로만 바뀜.'),
 ('13', 'C', '5회 21번', rq(5, 21), '(1,0) 같은 단위벡터(원-핫 벡터)와의 코사인 유사도 → 실제는 이를 조건으로 x, y 결정.'),
 ('14', 'B', '1회 21번', rq(1, 21), '다층 퍼셉트론 출력 계산. 실제는 은닉 노드 3개, f(x)=x (x≥10).'),
 ('15', 'B', '2회 단답 3', rsa(2, 2), '순서도 출력 조건을 만족하는 값의 개수 세기.'),
 ('16', 'B', '4회 21번', rq(4, 21), '같은 텍스트들을 유클리드·코사인으로 각각 판단하는 보기형.'),
 ('단답 1', 'A', '보충 6번', ex(5), '교과서 33쪽 문장이 그대로 — 빈칸 위치만 다름.'),
 ('단답 2', 'B', '1회 단답 2', rsa(1, 1), 'TF·TF-IDF 표 빈칸 채우기 — 같은 형식.'),
 ('단답 3', 'B', '2회 16번', rq(2, 16), '미지수가 있는 빈도수 벡터 + 유클리드 유사도 조건.'),
 ('단답 4', 'B', '5회 4번', rq(5, 4), '순서도 빈칸 채우기.'),
]
LV = {'A': ('문장·숫자 적중', 'la'), 'B': ('유형 적중', 'lb'), 'C': ('개념 적중', 'lc')}

def crops():
    os.makedirs(os.path.join(HERE, 'crop'), exist_ok=True)
    pages = {}
    out = {}
    for k, (p, x0, y0, x1, y1) in CROP.items():
        if p not in pages: pages[p] = ImageOps.exif_transpose(Image.open(os.path.join(HERE, 'real', f'p{p}.jpg'))).convert('RGB')
        fn = os.path.join(HERE, 'crop', f'q{k.replace(" ", "")}.jpg')
        pages[p].crop((x0, y0, x1, y1)).save(fn, quality=88)
        out[k] = (fn, (x1 - x0) / (y1 - y0))
    return out

def lay(cs):
    plain = [re.sub(r'\\\(.*?\\\)', lambda m: 'x' * max(2, len(m.group(0)) // 4), c) for c in cs]
    w = max(sum(1 if '가' <= ch <= '힣' else 0.55 for ch in p) for p in plain)
    return 'chs r5' if w <= 4.5 else ('chs r2' if w <= 15 else 'chs')

def ours(stem, cs, ans):
    chs = ''
    if cs:
        chs = f'<div class="{lay(cs)}">' + ''.join(f'<div class="cc"><span class="cn">{CIRC[j]}</span><span>{c}</span></div>' for j, c in enumerate(cs)) + '</div>'
    return f'<div class="oq">{stem}{chs}</div><div class="oa">정답 {ans}</div>'

def build(out):
    cr = crops()
    body = ('<h1>양정고 2026-2 중간 인공지능수학 · 적중 1:1 대조</h1>'
            '<div class="sub">왼쪽: 실제 시험지(2026. 10. 14.) · 오른쪽: 1~5회 모의고사 / 개념형 분석자료에서 대응하는 문항</div>')
    for no, lv, src, (stem, cs, ans), note in PAIRS:
        fn, ar = cr[no]
        w = 250 if ar < 0.75 else 262
        body += (f'<div class="pair"><div class="ph"><span class="rl">실제 {no}번</span><span class="ar">⇄</span><span class="sr">{src}</span>'
                 f'<span class="lv {LV[lv][1]}">{LV[lv][0]}</span><span class="nt">{note}</span></div>'
                 f'<div class="pb2"><div class="real"><img src="file://{fn}" style="width:{w}pt"></div><div class="our">{ours(stem, cs, ans)}</div></div></div>')
    css = CSS + r"""
.pair{border:.7pt solid #999;border-radius:3pt;margin:0 0 8pt;break-inside:avoid}
.ph{display:flex;align-items:center;gap:6pt;background:#f2f2f2;border-bottom:.6pt solid #ccc;padding:3pt 8pt;font-family:'GY','GL';font-size:9pt}
.ph .rl{color:#b42318}.ph .sr{color:#1f4e9a}.ph .ar{color:#999}
.ph .nt{margin-left:auto;font-family:'HB';font-size:8pt;color:#555;text-align:right;max-width:52%}
.lv{display:inline-block;font-family:'GY','GL';font-size:7.6pt;padding:.5pt 6pt;border-radius:7pt;white-space:nowrap;color:#fff}
.lv.la{background:#c4741c}.lv.lb{background:#2f8a4f}.lv.lc{background:#6b7280}
.pb2{display:flex;gap:0}
.real{flex:none;width:268pt;padding:5pt;border-right:.6pt dashed #bbb;text-align:center;background:#fafafa}
.real img{max-width:100%;border:.4pt solid #ddd}
.our{flex:1;min-width:0;padding:5pt 8pt;font-size:8.6pt;line-height:1.55}
.our .bogi{margin:3pt 0}.our .gt{font-size:7.8pt}.our .fig img{max-width:100%}
.oa{margin-top:3pt;color:#b42318;font-family:'GY','GL';font-size:8.6pt}
"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{css}</style></head><body>{body}</body></html>')
    open(os.path.join(HERE, 'cmp_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(CON, 'render3.js'), os.path.join(HERE, 'cmp_src.html'), os.path.join(HERE, 'cmp_tmp.pdf'), 'bg'], cwd=CON, check=True)
    os.replace(os.path.join(HERE, 'cmp_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
