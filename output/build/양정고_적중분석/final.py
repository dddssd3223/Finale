# -*- coding: utf-8 -*-
"""인공지능 수학 중간고사 FINAL PAGE (미적분Ⅰ FINAL PAGE 양식) + 난이도·등급컷 근거"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
CON = os.path.join(HERE, '..', 'concept')
sys.path.insert(0, CON)
from build import font_css, KATEX_CSS

DIF = {0: ('기본 유형', '#9a9a9a'), 1: ('2등급 변별 문항', '#1f3fd6'), 2: ('1등급 변별 문항', '#e01b24')}
HIT = {'A': ('문장·숫자 적중', '#0b7a35'), 'B': ('유형 적중', '#b36b00'), 'C': ('개념 적중', '#666')}
# 번호, 구조, 문항 유형, 배점, 난이도, 교과서, 적중, 모의 출제, 1컷 경계 득점률, 2컷 경계 득점률, 비고
R = [
 ('1', '객관식', '기계학습 정의', 4.4, 0, '14쪽', 'A', '4회 2번 ①', 1.00, .98, ''),
 ('2', '객관식', '강화학습 정의·사례', 4.4, 0, '15쪽 활용 사례', 'A', '3회 3번, 2회 4번', 1.00, .97, ''),
 ('3', '객관식', '포함 여부 벡터 → 단어집합', 4.4, 0, '48–50쪽', 'B', '1회 8번, 2회 12번, 4회 17번', .99, .95, ''),
 ('4', '객관식', '유사도 개념 (옳지 않은 것)', 4.4, 0, '70·75–77쪽', 'A', '2회 17번, 3회 21번', .98, .90, ''),
 ('5', '객관식', '퍼셉트론 출력 (f(x)=x형)', 4.4, 0, '17쪽', 'B', '1회 12번, 2회 8번, 4회 5번', .97, .88, '활성화함수가 x값 자체를 출력'),
 ('6', '객관식', '빈도수·IDF·TF-IDF 보기', 4.6, 0, '51·57–61쪽', 'A', '1회 17번, 5회 16번', .95, .80, 'IDF 방향 함정'),
 ('7', '객관식', '세 명제 진리표 빈칸', 4.6, 0, '21–22쪽', 'B', '3회 7번, 3회 단답 1', .97, .88, ''),
 ('8', '객관식', '유클리드↔코사인 관계 보기', 4.6, 1, '75–77쪽', 'A', '3회 21번, 4회 21번', .80, .50, '크기 같을 때 C↔d 관계, ‘반드시’ 반례'),
 ('9', '객관식', 'AND 임곗값 정수 개수', 4.7, 0, '23–24쪽', 'B', '1회 15번, 3회 8번', .95, .80, '경계 6 제외·10 포함'),
 ('10', '객관식', '자카드 유사도 대소', 4.7, 0, '70쪽', 'B', '1회 13·19번, 2회 15번', .97, .88, ''),
 ('11', '객관식', '자카드 감성 분석', 4.8, 0, '70–71쪽', 'A', '계산 연습 18번, 4회 20번', .96, .85, ''),
 ('12', '객관식', '유클리드 감성 x 개수', 4.8, 1, '73–74쪽', 'A', '3회 20번, 4회 단답 4', .85, .55, 'x=0 포함 여부'),
 ('13', '객관식', '원-핫·코사인 → 유클리드', 5.2, 2, '50·72–75쪽', 'C', '5회 21번, 3회 16번', .75, .40, '세 개념 결합 신유형'),
 ('14', '객관식', '3노드 다층 퍼셉트론', 5.2, 1, '24쪽', 'B', '1회 21번, 4회 10번, 5회 8번', .92, .70, '가중치 9개 대입'),
 ('15', '객관식', '순서도 조건 ㉠ 개수', 5.4, 2, '28–29쪽', 'B', '2회 단답 3, 2회 11번', .70, .35, '반복 추적 + 경계 역추적'),
 ('16', '객관식', '리뷰 TF·중요도·유사도 판단', 5.4, 1, '51·57·73–77쪽', 'B', '4회 21번, 2회 21번', .80, .50, '계산량 최대'),
 ('단답 1', '단답형', '데이터 정의·정형/비정형·연속/범주', 6, 0, '33–34쪽', 'A', '보충 6번, 3회 12번', .98, .92, ''),
 ('단답 2', '단답형', 'DF·IDF·TF-IDF 표 빈칸', 6, 1, '57–61쪽', 'B', '1회 단답 2, 3회 18번', .93, .77, '빈칸 6개 · 각 1점'),
 ('단답 3', '단답형', '유클리드 조건 → x, y, 코사인', 6, 2, '72–75쪽', 'B', '2회 16번, 2회 단답 4', .87, .60, '음수 해 배제'),
 ('단답 4', '단답형', '수열 순서도 빈칸', 6, 1, '28–29쪽', 'B', '5회 4번, 1회 단답 1', .93, .75, ''),
]
K_HIGH = 0.82   # 표본이 조금 높을 때 경계 학생 오답률을 18% 줄임

def tot(f): return sum(r[3] for r in R if f(r))
def cut(col, k=1.0): return sum(r[3] * (1 - (1 - r[col]) * k) for r in R)

CSS = r"""
@page{size:A4;margin:13mm 12mm 12mm 12mm}
html,body{margin:0;background:#fff}
body{font-family:'GL';font-size:9pt;color:#111}
h1{font-size:16pt;text-align:center;margin:0 0 2pt;letter-spacing:.5pt;-webkit-text-stroke:.35pt #000}
.sub{text-align:center;font-size:9.5pt;color:#444;margin-bottom:8pt}
.tag{display:inline-block;background:#111;color:#fff;padding:2pt 8pt;font-size:9pt;letter-spacing:1pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
table{border-collapse:collapse;width:100%}
th,td{border:.6pt solid #999;padding:1.6pt 3pt;text-align:center;vertical-align:middle;line-height:1.25}
.main td,.main th{font-size:7.9pt}
.nw{white-space:nowrap}
th{background:#eee;font-weight:400;-webkit-text-stroke:.2pt #000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
td.src{font-size:7.4pt}
.dot{display:inline-block;width:7pt;height:7pt;border-radius:50%;margin-right:4pt;vertical-align:-0.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.hit{font-weight:700}
.sum{display:flex;gap:8pt;margin:6pt 0}
.sum div{flex:1;border:1pt solid #ccc;border-radius:4pt;padding:5pt 8pt;font-size:8.4pt}
.sum b{font-size:12.5pt;display:block;margin-top:1pt}
h2{font-size:11pt;margin:7pt 0 4pt;-webkit-text-stroke:.25pt #000}
.ins td{text-align:left;padding:3.5pt 7pt;line-height:1.5;font-size:8.3pt}
.ins td.k{text-align:center;width:17%}
.big{font-size:10.5pt;-webkit-text-stroke:.2pt #000}
.pb{break-before:page}
.dt td,.dt th{font-size:7.9pt;padding:1.6pt 3pt}
.bar{display:inline-block;height:6pt;background:#9bb3e0;vertical-align:middle;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.note{font-size:8.2pt;color:#444;line-height:1.55;margin-top:5pt}
"""

def build(out):
    rows = ''
    for no, kind, t, pt, d, tb, h, mock, *_ in R:
        dl, dc = DIF[d]; hl, hc = HIT[h]
        rows += (f'<tr><td class="nw">{no}</td><td class="nw">{kind}</td><td style="text-align:left">{t}</td><td class="nw">{pt:.1f}</td>'
                 f'<td class="nw" style="text-align:left;color:{dc}"><span class="dot" style="background:{dc}"></span>{dl}</td>'
                 f'<td class="src">교과서 {tb}</td><td class="hit nw" style="color:{hc}">{hl}</td><td class="src">{mock}</td></tr>')
    n = {k: sum(1 for r in R if r[6] == k) for k in 'ABC'}
    p = {k: tot(lambda r, k=k: r[6] == k) for k in 'ABC'}
    t0, t1, t2 = (tot(lambda r, d=d: r[4] == d) for d in range(3))
    c1, c2 = cut(8), cut(9); c1h, c2h = cut(8, K_HIGH), cut(9, K_HIGH)
    loss = 100 - c1
    head = f"""<div style="text-align:right"><span class="tag">FINAL PAGE · 적중 분석</span></div>
<h1>양정고등학교 2학년 2026학년도 2학기 중간고사 FINAL PAGE</h1>
<div class="sub">인공지능 수학 · 2026년 10월 14일(수) 1교시 · 모의고사 1–5회 · 개념형 분석자료 대조</div>
<table class="main"><colgroup><col style="width:5%"><col style="width:6%"><col style="width:21%"><col style="width:5%"><col style="width:13%"><col style="width:16%"><col style="width:10%"><col style="width:24%"></colgroup>
<tr><th>번호</th><th>구조</th><th>문항 유형</th><th>배점</th><th>난이도</th><th>출처</th><th>적중</th><th>모의고사·자료 출제</th></tr>{rows}</table>
<div class="sum"><div>문장·숫자 적중 (문장·수치·자료 거의 그대로)<b style="color:#0b7a35">{n['A']}문항 · {p['A']:.1f}점</b></div>
<div>유형 적중 (같은 유형·풀이 과정)<b style="color:#b36b00">{n['B']}문항 · {p['B']:.1f}점</b></div>
<div>개념 적중 (다룬 개념의 결합)<b style="color:#666">{n['C']}문항 · {p['C']:.1f}점</b></div></div>
<h2>INSIGHT</h2>
<table class="ins">
<tr><td class="k">난이도</td><td>기본 유형 <b>{t0:.1f}점</b> · <span style="color:#1f3fd6">2등급 변별 {t1:.1f}점</span> · <span style="color:#e01b24">1등급 변별 {t2:.1f}점</span>.
개념 문항(1–7번, 단답 1)은 교과서 문장 그대로라 평이하고, 변별은 <b>계산 결합형(8·12·13·15·16번, 단답 2–4)</b>에서 갈렸어요.
미적분Ⅰ과 비교하면 최상위 킬러는 없지만(1컷 경계 예상 감점 미적분Ⅰ 약 11–13점 → 인공지능 수학 약 {loss:.0f}점) 2등급 변별 점수는 1.7배(18.5 → {t1:.1f}점)라 <b>상위권은 쉽고 중위권은 촘촘한</b> 시험이에요.</td></tr>
<tr><td class="k">예상 등급컷</td><td>
<span class="big"><span class="dot" style="background:#e01b24"></span>1등급(상위 10%) {round(c1)}–{round(c1h)}점 &nbsp;&nbsp; <span class="dot" style="background:#1f3fd6"></span>2등급(34%) {round(c2)}–{round(c2h)}점</span><br>
· 표본이 미적분Ⅰ과 같을 때: 1컷 <b>{c1:.0f}</b>, 2컷 <b>{c2:.0f}</b> &nbsp;·&nbsp; 표본이 조금 높을 때: 1컷 <b>{c1h:.0f}</b>, 2컷 <b>{c2h:.0f}</b><br>
<span style="color:#666">참고: 미적분Ⅰ 예상 87 / 73 (학원 88.6 / 75.3), 1학기 기말 실제 90.1 / 76.1. 상위권 컷은 1학기처럼 예상보다 1–2점 높게 형성될 수 있어요.</span></td></tr>
<tr><td class="k">출제 분석</td><td>· 20문항 모두 모의고사·분석자료에서 같은 문제 또는 같은 유형으로 다뤘어요. 12번은 3회 20번의 리조트 리뷰가 그대로, 단답 1은 보충 6번 문장이 그대로 나왔어요.<br>
· 교과서 본문·확인하기 문장을 그대로 쓰고, 계산 문항은 숫자 하나를 미지수로 바꿔 조건을 묻는 방식이 많았어요(12번 x, 15번 ㉠, 단답 3의 x, y).<br>
· 1–5회에 없던 결합: 13번(원-핫 벡터 + 코사인 → 유클리드), 5·14번 f(x)=x형 활성화함수.</td></tr>
<tr><td class="k">본인 점수</td><td><b>100점</b> (선택형 76 + 단답형 24) → 어느 시나리오에서도 1등급. 만점자가 많아도 전체의 약 20% 이하면 동점자 중간석차가 10% 안이라 1등급이에요.</td></tr>
</table>"""
    drows = ''
    for no, kind, t, pt, d, tb, h, mock, p1, p2, memo in R:
        dl, dc = DIF[d]
        drows += (f'<tr><td class="nw">{no}</td><td style="text-align:left">{t}</td><td>{pt:.1f}</td><td class="nw" style="color:{dc}">{dl.replace(" 문항", "")}</td>'
                  f'<td>{p1*100:.0f}%</td><td style="text-align:left"><span class="bar" style="width:{p1*60:.0f}pt"></span></td><td>{p2*100:.0f}%</td>'
                  f'<td style="text-align:left"><span class="bar" style="width:{p2*60:.0f}pt;background:#c9d4ea"></span></td><td style="text-align:left;font-size:7.4pt">{memo}</td></tr>')
    top = sorted(R, key=lambda r: -r[3] * (1 - r[8]))[:5]
    detail = f"""<div class="pb"></div><h2>난이도 분석 · 등급컷 산출 근거</h2>
<table class="dt"><colgroup><col style="width:6%"><col style="width:24%"><col style="width:5%"><col style="width:10%"><col style="width:6%"><col style="width:13%"><col style="width:6%"><col style="width:13%"><col></colgroup>
<tr><th>번호</th><th>문항 유형</th><th>배점</th><th>난이도</th><th colspan="2">1컷 경계 학생 득점률</th><th colspan="2">2컷 경계 학생 득점률</th><th>변별 요소</th></tr>{drows}
<tr><th colspan="2">기대 득점 합 (= 예상 컷)</th><th>100</th><th></th><th colspan="2">{c1:.1f}점</th><th colspan="2">{c2:.1f}점</th><th></th></tr></table>
<div class="note"><b>산출 방법</b><br>
· 1컷 경계 학생(상위 10%)과 2컷 경계 학생(상위 34%)이 각 문항에서 받을 점수 비율을 문항 난이도로 추정하고, 배점을 곱해 더한 값을 예상 컷으로 봤어요. 단답형은 부분 점수를 반영했어요.<br>
· 기준점은 미적분Ⅰ이에요. 같은 학생들이 미적분Ⅰ에서 1컷 87–88.6, 2컷 73–75로 예상됐고, 미적분Ⅰ의 1등급 변별(17·18·20번, 20.4점)은 이번 시험의 1등급 변별(13·15번·단답 3, {t2:.1f}점)보다 훨씬 어려웠어요. 그래서 1컷 경계 학생의 예상 감점을 미적분Ⅰ(11–13점)보다 작은 약 {loss:.0f}점으로 잡았어요.<br>
· 표본이 조금 높은 경우는 경계 학생의 문항별 오답률을 18% 줄여서 계산했어요(1컷 {c1:.1f} → {c1h:.1f}, 2컷 {c2:.1f} → {c2h:.1f}).<br>
· 상위권 감점이 가장 많이 나올 문항: {', '.join(f'{r[0]}번({r[3]*(1-r[8]):.1f}점)' for r in top)}.<br>
<b>한계</b> 문항별 득점률은 제가 매긴 추정치라 컷은 ±1.5점 정도 오차가 있어요. 인공지능 수학을 수강하는 학생 구성(미적분Ⅰ 수강생 중 일부인지, 상위권이 더 많은지)에 따라 표본 시나리오가 달라져요. 실제 평균이나 등급컷이 나오면 바로 보정할게요.</div>"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{head}{detail}</body></html>')
    open(os.path.join(HERE, 'final_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(CON, 'render3.js'), os.path.join(HERE, 'final_src.html'), os.path.join(HERE, 'final_tmp.pdf'), 'bg'], cwd=CON, check=True)
    os.replace(os.path.join(HERE, 'final_tmp.pdf'), out)
    print(dict(n=n, p=p, tiers=(t0, t1, t2), cuts=(round(c1, 1), round(c2, 1), round(c1h, 1), round(c2h, 1))))

if __name__ == '__main__':
    build(sys.argv[1])
