# -*- coding: utf-8 -*-
"""양정고 2026-2 중간 인공지능수학 — 1~5회 모의고사·분석자료 적중 정리"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
CON = os.path.join(HERE, '..', 'concept')
sys.path.insert(0, CON)
from build import CSS, font_css, KATEX_CSS

LV = {'A': ('문장·숫자 적중', 'la'), 'B': ('유형 적중', 'lb'), 'C': ('개념 적중', 'lc')}

# 번호, 배점, 실제 문제, 등급, 적중 자료 [(출처, 내용)]
ROWS = [
 ('1', 4.4, '‘사람이 학습하듯 컴퓨터가 주어진 자료를 스스로 학습하여 문제를 해결하는 것’ → 기계학습', 'A',
  [('4회 2번 ①', '“사람이 학습하듯이 컴퓨터가 자료를 스스로 학습하여 문제를 해결하는 기술” — 문장 동일'), ('경문고 분석지 단답 2', '같은 정의로 기계학습 쓰기')]),
 ('2', 4.4, '최적 행동을 찾는 학습, 자율 주행 시뮬레이션·동작 모방 로봇 제어 → 강화학습', 'A',
  [('경문고 분석지 핵심 정리', '강화 학습 사례 “자율 주행 자동차 시뮬레이션, 동작 모방 로봇 제어” 그대로'), ('3회 3번 · 2회 4번 · 용어 #15', '보상으로 최적 행동 강화')]),
 ('3', 4.4, '포함 여부 벡터 (1,1,1,0,0,1)에서 A에 없는 단어 찾기', 'B',
  [('1회 8번 · 2회 12번', '단어집합 → 0/1 벡터'), ('4회 17번', '주요 단어 포함 여부 벡터')]),
 ('4', 4.4, '유사도 설명 중 틀린 것: “유클리드·코사인 모두 0에 가까울수록 유사”', 'A',
  [('2회 17번', '“유클리드 작을수록 유사하지 않다”, “코사인 작을수록 유사” ×, “유클리드가 더 정확” × — 같은 함정'), ('3회 21번 ㄱ·ㄴ', '유클리드 0에 가까울수록 유사, 빈도수 벡터 코사인 0~1')]),
 ('5', 4.4, '세 입력 퍼셉트론 가중합 → f(x)=x (x≥3) 출력', 'B',
  [('1회 12번', '세 입력 퍼셉트론 가중합·출력'), ('2회 8번 · 4회 5번 · 계산 연습 3번', '가중합 → 활성화함수')]),
 ('6', 4.6, 'ㄱ 빈도수 성분은 음이 아닌 정수 ㄴ 등장 문서 많을수록 IDF 커진다(×) ㄷ TF-IDF 크면 중요', 'A',
  [('1회 17번 ③④', 'IDF 방향 뒤집기 함정(③), “TF-IDF 높을수록 대표 단어”(④)'), ('5회 16번', 'TF-IDF 성질'), ('개념형 분석자료 TF-IDF 핵심 정리', '드문 단어 → DF 작음 → IDF 큼')]),
 ('7', 4.6, '세 명제 진리표 (p∨q)∧r, (p⊕q)∨r 빈칸 a~d', 'B',
  [('3회 7번', '세 명제 (p∧q)∨r, (p∨q)∧r, (p⊕q)⊕r'), ('3회 단답 1 · 경문고 15번', '세 명제 진리표 빈칸')]),
 ('8', 4.6, 'ㄱ 동일 문서 → 코사인 1, 유클리드 0 ㄴ 크기 같으면 C 크면 d 작다 ㄷ “반드시” 같은 판단(×)', 'A',
  [('3회 21번 ㄹ', '“d(a,a)=0, C(a,a)=1” — ㄱ과 같은 문장'), ('경문고 분석지 핵심 정리', '“벡터 크기가 모두 같으면 코사인은 분자만 비교” → ㄴ'),
   ('4회 21번 · 1회 단답 3', '유클리드와 코사인 판단이 다른 경우 → ㄷ 반례')]),
 ('9', 4.7, 'w=(6,4) 논리곱(AND)이 되는 정수 c의 개수', 'B',
  [('1회 15번', 'AND 임곗값 범위 a<c≤b'), ('3회 8번 · 경문고 8번 · 계산 연습 4번', 'AND·OR 임곗값 범위')]),
 ('10', 4.7, '세 단어 집합 자카드 유사도 대소 비교', 'B',
  [('1회 13·19번 · 2회 15번', '자카드 계산·비교'), ('경문고 9번 · 계산 연습 13번', '세 집합 자카드')]),
 ('11', 4.8, 'P·N 각 5개, X = 긍정 3 + 부정 1 → S = 1/2 − 1/8 = 3/8, 긍정', 'A',
  [('계산 연습 18번', '“n(P)=n(N)=5, X는 P 원소 3개·N 원소 1개” → 1/2, 1/8, 긍정 — 숫자까지 동일'),
   ('4회 20번 · 1회 단답 5 · 2회 단답 2', '자카드 감성 분석 ±0.25 기준')]),
 ('12', 4.8, '리조트 리뷰 U·p·n, a=(2,0,2,2,0,1,x,0) → 긍정이 되는 x의 개수', 'A',
  [('3회 20번', '같은 U{쾌적, 친절, 경치 좋음, …, 외짐}, 같은 p·n, a=(2,0,2,2,0,1,1,0) — 7번째 성분만 x로 바뀜'),
   ('4회 단답 4 · 4회 21번', '유클리드 감성 분석, 같은 리뷰 벡터')]),
 ('13', 5.2, '원-핫 벡터와 빈도수 벡터의 코사인으로 x, y 구한 뒤 유클리드', 'C',
  [('5회 21번', '(1,0) 같은 단위벡터와의 코사인 유사도'), ('3회 16번 · 4회 17번', '원-핫 벡터 정의'), ('5회 단답 4·5', '유클리드·코사인 계산')]),
 ('14', 5.2, '은닉 노드 3개 다층 퍼셉트론, f(x)=x (x≥10) → y=21', 'B',
  [('1회 21번 · 4회 10번 · 5회 8번', '다층 퍼셉트론 출력 계산'), ('2회 단답 5', '다층 퍼셉트론 표 완성')]),
 ('15', 5.4, '순서도 S=126이 되는 ㉠의 개수', 'B',
  [('2회 단답 3', '순서도 조건을 만족하는 값의 개수 세기(세화 서답 5)'), ('2회 11번', '순서도 조건 역추적'), ('1회 단답 1 · 4회 11번 · 계산 연습 5·6번', '반복 순서도 추적')]),
 ('16', 5.4, '리뷰 밑줄 단어 TF, 가장 중요한 단어, 유클리드·코사인 판단 일치', 'B',
  [('2회 21번', '후기 밑줄 단어 → 빈도수 벡터 → 유클리드'), ('4회 21번', '같은 리뷰를 유클리드·코사인으로 각각 판단'), ('5회 17번', '후기 TF 표')]),
 ('단답 1', 6, '“몸무게와 성적 또는 여러 설문을 통해 얻는 값이나 의견처럼 …” → 정형/비정형, 연속형/범주형', 'A',
  [('보충 6번 (개념형 분석자료)', '같은 문장 그대로 + (가) 데이터, (나) 정형 데이터 빈칸'), ('3회 12번', '키·몸무게 = 연속형, 혈액형 = 범주형'), ('용어 #33·34·50', '정형/비정형, 연속형/범주형')]),
 ('단답 2', 6, '농구 기사 4개 DF·IDF·TF-IDF 표 빈칸 ㉠~㉥', 'B',
  [('1회 단답 2', 'TF·TF-IDF 표 빈칸 a~f 채우기 — 같은 형식'), ('3회 18번 · 3회 단답 5 · 4회 단답 2', 'TF → DF → IDF → TF-IDF 표'), ('경문고 단답 8·9', '조리법 TF-IDF 표')]),
 ('단답 3', 6, 'd(a,b)=3, x+2y=5로 x, y 구하고 C(a,c)', 'B',
  [('2회 16번', '미지수 성분 + 유클리드 유사도 조건(세화 12)'), ('2회 단답 4 · 4회 단답 3', '유클리드 유사도 계산'), ('5회 단답 5', '코사인 유사도')]),
 ('단답 4', 6, '수열 순서도 빈칸 ㉠~㉤ 채우기', 'B',
  [('5회 4번', '순서도 빈칸 (가)·(나)·(마) 채우기(확인하기 6)'), ('1회 단답 1 · 4회 11번', '반복 순서도')]),
]

TOP = [
 ('12번', '3회 20번', 'U = {쾌적, 친절, 경치 좋음, 주차 공간 여유, 객실 좁음, 난방 안 됨, 방음 안 됨, 외짐}<br>p = (1,1,1,1,0,0,0,0), n = (0,0,0,0,1,1,1,1)<br>a = (2,0,2,2,0,1,<b>x</b>,0)',
  '같은 U, 같은 p·n<br>a = (2,0,2,2,0,1,<b>1</b>,0)<br>→ d(p,a)=√6, d(n,a)=√14, 긍정', '리뷰 벡터 한 성분만 x로 바꿔 조건을 묻는 형태'),
 ('단답형 1', '보충 6번', '“몸무게와 성적 또는 여러 설문을 통해 얻는 값이나 의견처럼 관찰이나 측정으로 얻게 되는 가공되지 않은 정보를 데이터라고 한다. 데이터는 형태에 따라 ㉠, ㉡ 데이터로 분류한다.”',
  '“몸무게와 성적 또는 여러 설문을 통해 얻는 값이나 의견처럼 관찰이나 측정으로 얻게 되는 가공되지 않은 정보를 (가)라고 한다. (가)는 형태에 따라 (나), 비정형 데이터로 분류한다.”', '교과서 33쪽 문장 그대로 — 미출제 개념 보충에서 적중'),
 ('11번', '계산 연습 18번', 'P, N 각 5개, X = {투박하다, 좋다, 만족, 괜찮다}<br>(긍정 3 + 부정 1) → S = 3/8, 긍정', 'n(P)=n(N)=5, X는 P 원소 3개 + N 원소 1개<br>→ 1/2, 1/8, 긍정', '숫자·결론까지 동일'),
 ('1번', '4회 2번 ①', '사람이 학습하듯 컴퓨터가 주어진 자료를 스스로 학습하여 문제를 해결하는 것', '사람이 학습하듯이 컴퓨터가 자료를 스스로 학습하여 문제를 해결하는 기술이다.', '정의 문장 동일'),
 ('8번 ㄱ', '3회 21번 ㄹ', '두 벡터가 완전히 동일한 문서의 빈도수 벡터라면 코사인 유사도는 1이고 유클리드 유사도는 0이다.', '영벡터가 아닌 벡터 a에 대하여 d(a, a) = 0, C(a, a) = 1이다.', '같은 내용'),
]

def build(out):
    cnt = {k: [r for r in ROWS if r[3] == k] for k in LV}
    pts = {k: sum(r[1] for r in v) for k, v in cnt.items()}
    head = ('<h1>양정고 2026-2 중간 인공지능수학 적중 분석</h1>'
            '<div class="sub">2026. 10. 14. 시행 · 선택형 16문항 76점 + 단답형 4문항 24점 · 비교 대상: 1~5회 모의고사, 개념형 문항 분석자료(보충·용어·계산 연습), 경문고 분석지</div>'
            '<div class="sum">'
            '<div class="big"><div class="n">20 / 20</div><div class="l">전 문항 적중</div></div>'
            + ''.join(f'<div class="st {LV[k][1]}"><div class="n">{len(cnt[k])}문항</div><div class="l">{LV[k][0]}</div><div class="p">{pts[k]:.1f}점</div></div>' for k in LV)
            + '<div class="big me"><div class="n">100점</div><div class="l">실제 점수</div></div></div>'
            '<div class="legend"><span class="lv la">문장·숫자 적중</span> 문장·수치·자료가 거의 그대로 &nbsp; '
            '<span class="lv lb">유형 적중</span> 같은 유형·풀이 과정 &nbsp; <span class="lv lc">개념 적중</span> 다룬 개념을 결합한 신유형</div>')
    top = '<h2>완전 적중 비교</h2><div class="tops">'
    for real, src, a, b, note in TOP:
        top += (f'<div class="tp1"><div class="th"><span class="rl">실제 {real}</span><span class="ar">⇄</span><span class="sr">{src}</span><span class="nt">{note}</span></div>'
                f'<div class="cmp"><div class="c1"><div class="cap">실제 시험</div>{a}</div><div class="c2"><div class="cap">우리 자료</div>{b}</div></div></div>')
    top += '</div>'
    rows = ''
    for no, pt, q, lv, hits in ROWS:
        hh = ''.join(f'<div class="hit"><b>{s}</b> {t}</div>' for s, t in hits)
        rows += (f'<tr><td class="no">{no}<div class="pt">{pt}점</div></td><td class="l">{q}</td>'
                 f'<td><span class="lv {LV[lv][1]}">{LV[lv][0]}</span></td><td class="l">{hh}</td></tr>')
    tbl = ('<h2 class="pb">문항별 적중표</h2><table class="ht"><tr><th style="width:7%">번호</th><th style="width:30%">실제 문제</th>'
           f'<th style="width:11%">등급</th><th>적중 자료</th></tr>{rows}</table>')
    css = CSS + r"""
.sum{display:flex;gap:6pt;margin:4pt 0 6pt}
.sum>div{flex:1;border:.6pt solid #bbb;border-radius:3pt;text-align:center;padding:5pt 2pt}
.sum .n{font-family:'GY','GL';font-size:15pt}.sum .l{font-size:8.4pt;color:#444}.sum .p{font-size:8pt;color:#777}
.sum .big{background:#1f4e9a;color:#fff;border-color:#1f4e9a}.sum .big .l{color:#dfe7f5}
.sum .me{background:#b42318;border-color:#b42318}
.sum .st.la{background:#fff1c9}.sum .st.lb{background:#e8f3ec}.sum .st.lc{background:#eef0f3}
.legend{font-size:8.2pt;color:#444;margin-bottom:4pt}
.lv{display:inline-block;font-family:'GY','GL';font-size:7.8pt;padding:.5pt 6pt;border-radius:7pt;white-space:nowrap}
.lv.la{background:#c4741c;color:#fff}.lv.lb{background:#2f8a4f;color:#fff}.lv.lc{background:#6b7280;color:#fff}
.tops{display:flex;flex-direction:column;gap:6pt}
.tp1{border:.6pt solid #c4741c;border-radius:3pt;break-inside:avoid}
.th{display:flex;align-items:center;gap:6pt;background:#fff6e6;padding:3pt 8pt;border-bottom:.6pt solid #e7c38d;font-family:'GY','GL';font-size:9pt}
.th .rl{color:#b42318}.th .sr{color:#1f4e9a}.th .ar{color:#999}.th .nt{margin-left:auto;font-family:'HB';font-size:8.2pt;color:#666}
.cmp{display:flex}.cmp>div{flex:1;padding:4pt 8pt;font-size:8.6pt;line-height:1.55}.cmp .c1{border-right:.6pt dashed #ccc}
.cap{font-family:'GY','GL';font-size:7.6pt;color:#888;margin-bottom:1pt}
.pb{break-before:page}
.ht td,.ht th{font-size:8.2pt;padding:3pt 5pt;line-height:1.45;vertical-align:middle}.ht tr{break-inside:avoid}
.ht .no{font-family:'GY','GL';font-size:9pt}.ht .pt{font-family:'HB';font-size:7.4pt;color:#777}
.hit{margin:1pt 0}.hit b{font-family:'GY','GL';font-weight:400;color:#1f4e9a;margin-right:3pt}
"""
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{css}</style></head><body>{head}{top}{tbl}</body></html>')
    open(os.path.join(HERE, 'hit_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(CON, 'render3.js'), os.path.join(HERE, 'hit_src.html'), os.path.join(HERE, 'hit_tmp.pdf'), 'bg'], cwd=CON, check=True)
    os.replace(os.path.join(HERE, 'hit_tmp.pdf'), out)
    print({k: (len(v), pts[k]) for k, v in cnt.items()}, sum(pts.values()))

if __name__ == '__main__':
    build(sys.argv[1])
