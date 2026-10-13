# -*- coding: utf-8 -*-
"""경문고 2026-1 중간 인공지능수학 — 범위(교과서 Ⅰ~Ⅱ) 안 문항 분석지"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
CON = os.path.join(HERE, '..', 'concept')
sys.path.insert(0, CON)
from build import CSS, font_css, KATEX_CSS, CIRC, tagO
from extra import TB, BX, BOGI

STEP = lambda c: rf"\(f(x)=\begin{{cases}}0 & (x<{c})\\ 1 & (x\ge {c})\end{{cases}}\)"
TBL11 = TB(['', '판타지', '액션', '코미디', '공포'], [['A', 3, 4, 1, 2], ['B', 3, 2, 1, 4], ['C', 4, 3, 2, 1]])
NOTE11 = ("세 학생 A, B, C가 네 영화 장르에 대해 선호도가 낮은 순위부터 높은 순위로 1부터 4까지 점수를 부여한 것이다. "
          r"(판타지, 액션, 코미디, 공포)의 순위 점수를 벡터 \(\vec a\), \(\vec b\), \(\vec c\)라 하자. 예를 들어 \(\vec a=(3,\,4,\,1,\,2)\)이다.")
TBL89 = TB(['', '양파', '김치', '된장', '돼지고기', '감자', '고춧가루', '소고기'],
           [['조리법 A', 3, 3, 0, 2, 0, 3, 0], ['조리법 B', 3, 0, 3, 0, 3, 1, 2], ['조리법 C', 3, 1, 1, 3, 1, 3, 0]])

# kind: X1/O1/B/M(여러 개 고르기, ans=집합)/None
ITEMS = [
 ('학습 방법', [
  dict(no='1번', t='지도학습 사례 3가지', k='개념', q="‘지도학습’에 더 가까운 사례 3가지를 고르시오.",
       c=['스팸 메일 분류', '사진 속 인물 성별 구분', '사진이나 음성 데이터에서 본질적인 특징은 남기고 불필요한 잡음(Noise)만 골라내어 제거하기', '동작 모방 로봇 제어', '질병 유무 판단'],
       kind='M', a={1, 2, 5},
       p="교과서 15쪽 <b>지도학습 활용 사례</b> 박스 그대로(스팸·질병·성별·날씨·음악 식별). ③ 정답 없이 특징만 찾기 → 비지도, ④ 동작 모방 로봇 → <b>강화학습</b> 사례.",
       m='2회 4번 · 3회 3번 · 4회 2번'),
  dict(no='2번', t='비지도학습 사례 3가지', k='개념', q="‘비지도학습’에 더 가까운 사례 3가지를 고르시오.",
       c=['음악 일부를 들려주면 제목, 가수 식별', '자율 주행 자동차 시뮬레이션', '구매자별 소비 패턴 파악 후 추천 상품 광고 제공', 'SNS업체에서 설문 조사 결과를 토대로 회원들을 분류', '구입 정보를 바탕으로 쇼핑몰 회원들을 그룹별로 묶기'],
       kind='M', a={3, 4, 5},
       p="15쪽 <b>비지도학습 활용 사례</b> 박스 그대로. ① 음악 식별 → 지도, ② 자율 주행 시뮬레이션 → 강화.",
       m='3회 3번'),
  dict(no='3번', t='강화학습 사례 3가지', k='개념', q="‘강화학습’에 더 가까운 사례 3가지를 고르시오.",
       c=['자율 주행 자동차 시뮬레이션', '내일 날씨 예측', '전략 게임 인공지능', '알파고(인공지능 바둑 프로그램)', '부동산 가격 예측'],
       kind='M', a={1, 3, 4},
       p="15쪽 <b>강화 학습 활용 사례</b>(자율 주행 시뮬레이션·동작 모방 로봇·알파고·전략 게임). 날씨 예측은 교과서 <b>지도학습</b> 사례, 가격 예측도 정답 있는 과거 데이터로 학습 → 지도.",
       m='3회 3번'),
 ]),
 ('인공지능의 역사 (인물)', [
  dict(no='4번', t='마빈 민스키', k='개념', q="다음과 같은 업적을 이룬 사람의 이름은?"
       + BX("• 인공지능 연구의 시발점이 된 다트머스 회의 주도<br>• 단층 퍼셉트론이 XOR과 같은 비선형 문제는 해결할 수 없음을 수학적으로 증명<br>• 다층 퍼셉트론의 필요성 언급"),
       c=['앨런 튜링', '프랭크 로젠블랫', '마빈 민스키', '시모어 페퍼트', '데이비드 럼멜하트'], kind=None, a=3,
       p="XOR 한계 증명은 <b>민스키·페퍼트</b> 공동이지만, <b>다트머스 회의 주도</b>까지 만족하는 사람은 민스키. 세 조건을 다 맞춰야 하는 함정.",
       m='3회 9번 ㄹ · 4회 3번'),
  dict(no='5번', t='프랭크 로젠블랫', k='개념', q="다음과 같은 업적을 이룬 사람의 이름은?"
       + BX("• 뉴런의 특징을 분석하여 인공 뉴런의 수학적 모델을 정리하고, 퍼셉트론 알고리즘을 제안함"),
       c=['프랭크 로젠블랫', '마빈 민스키', '시모어 페퍼트', '데이비드 럼멜하트', '제프리 힌턴'], kind=None, a=1,
       p="1957년 단층 인공신경망인 <b>퍼셉트론</b> 제안 = 로젠블랫.",
       m='3회 2번 ③'),
  dict(no='6번', t='제프리 힌턴 (선지 없음)', k='개념', q="다음과 같은 업적을 이룬 사람의 이름은?"
       + BX("• 오류 역전파 알고리즘을 통해 XOR 문제 해결<br>• 수학적으로 더 안정적인 활성화함수를 제안하는 등 다층 퍼셉트론의 학습 효율성을 개선하며 ‘딥러닝’의 시대를 엶."),
       c=['앨런 튜링', '프랭크 로젠블랫', '마빈 민스키', '시모어 페퍼트', '이세돌'], kind=None, a=None,
       p="설명은 <b>제프리 힌턴</b>(1986 럼멜하트·힌턴·윌리엄스 오류 역전파, 딥러닝의 아버지). 시험지 선지에 힌턴·럼멜하트가 없어 <b>출제 오류(정답 없음)</b>로 보인다. 원문 그대로 옮김.",
       m='3회 2번 ④ · 4회 9번 ㄹ'),
 ]),
 ('데이터 단위', [
  dict(no='7번', t='페타바이트와 비트', k='계산', q="1 PB(페타바이트)는 몇 Bit인지 올바르게 표현한 것은?",
       c=[r'\(1\times10^{12}\) Bit', r'\(8\times10^{12}\) Bit', r'\(1\times10^{15}\) Bit', r'\(8\times10^{15}\) Bit', r'\(1\times10^{18}\) Bit'], kind=None, a=4,
       p=r"1 PB \(=10^{15}\) 바이트, 1 바이트 = 8 비트 → \(8\times10^{15}\) Bit. <b>바이트↔비트 함정</b>(③은 바이트 기준).",
       m='1회 5번 · 3회 13번 ⑤'),
 ]),
 ('퍼셉트론', [
  dict(no='8번', t='OR·AND 임곗값 범위', k='계산',
       q=r"두 입력값 \(x_1\), \(x_2\)(0 또는 1)에 대한 퍼셉트론의 가중치가 \(w_1=3\), \(w_2=2\)이고 활성화함수가 " + STEP('c')
         + r"일 때, 논리합(OR)을 가능하게 하는 임곗값 \(c\)의 범위가 \(a<c\le b\)이고 논리곱(AND)을 가능하게 하는 \(c\)의 범위가 \(d<c\le e\)이다. \(b\times d\times e\)의 값은?",
       c=['16', '20', '24', '30', '40'], kind=None, a=4,
       p=r"가중합: \((0,0)\) 0, \((0,1)\) 2, \((1,0)\) 3, \((1,1)\) 5. OR \(0<c\le2\), AND \(3<c\le5\) → \(2\times3\times5=30\).",
       m='1회 15번 · 3회 8번 · 4회 단답'),
 ]),
 ('자카드 유사도', [
  dict(no='9번', t='자카드 유사도 계산', k='계산',
       q=r"세 텍스트 데이터의 단어 집합이 다음과 같을 때, \(J(A,B)+2\times J(B,C)+3\times J(C,A)\)의 값은?"
         + BX(r"\(A=\){생애, 영화, 인생, 제일}<br>\(B=\){기억, 생애, 인생, 지우다, 최악}<br>\(C=\){기억, 남는다, 영화, 인생, 제일}"),
       c=[r'\(\dfrac{16}7\)', r'\(\dfrac{65}{28}\)', r'\(\dfrac{33}{14}\)', r'\(\dfrac{67}{28}\)', r'\(\dfrac{17}7\)'], kind=None, a=1,
       p=r"\(J(A,B)=\dfrac27\), \(J(B,C)=\dfrac28=\dfrac14\), \(J(C,A)=\dfrac36=\dfrac12\) → \(\dfrac27+\dfrac12+\dfrac32=\dfrac{16}7\).",
       m='1회 13·19번 · 2회 15번'),
  dict(no='10번', t='자카드 유사도 부등식', k='계산',
       q=r"두 집합 \(A\), \(B\)가 (가) \(n(A)=8\), \(n(B)=6\) (나) \(J(A,B)>\dfrac25\)를 만족시킬 때, \(n(A\cap B)\)의 최솟값은?",
       c=['1', '2', '3', '4', '5'], kind=None, a=5,
       p=r"\(n(A\cap B)=x\)이면 \(J=\dfrac{x}{14-x}>\dfrac25\) → \(7x>28\) → \(x>4\). 최솟값 5. (=4이면 \(\dfrac4{10}\)으로 같아서 안 됨)",
       m='2회 18번'),
 ]),
 ('유클리드·코사인 유사도', [
  dict(no='11번', t='유클리드 유사도 대소', k='계산', q=TBL11 + NOTE11 + "<br>다음 중 옳은 것은?",
       c=[r'\(d(\vec a,\vec b)>d(\vec b,\vec c)>d(\vec c,\vec a)\)', r'\(d(\vec a,\vec b)>d(\vec c,\vec a)>d(\vec b,\vec c)\)', r'\(d(\vec b,\vec c)>d(\vec a,\vec b)>d(\vec c,\vec a)\)',
          r'\(d(\vec b,\vec c)>d(\vec c,\vec a)>d(\vec a,\vec b)\)', r'\(d(\vec c,\vec a)>d(\vec a,\vec b)>d(\vec b,\vec c)\)'], kind=None, a=3,
       p=r"\(d(\vec a,\vec b)=\sqrt8\), \(d(\vec b,\vec c)=\sqrt{12}\), \(d(\vec c,\vec a)=\sqrt4=2\). 제곱한 값끼리 비교하면 빠르다.",
       m='2회 16·19번 · 4회 21번'),
  dict(no='12번', t='코사인 유사도 계산', k='계산', q=r"(11번의 표) \(C(\vec a,\vec b)+2\times C(\vec b,\vec c)+4\times C(\vec c,\vec a)\)의 값은?",
       c=[r'\(\dfrac{89}{15}\)', r'\(\dfrac{93}{15}\)', r'\(\dfrac{94}{15}\)', r'\(\dfrac{98}{15}\)', r'\(\dfrac{33}5\)'], kind=None, a=2,
       p=r"세 벡터 크기가 모두 \(\sqrt{30}\). \(C(\vec a,\vec b)=\dfrac{26}{30}\), \(C(\vec b,\vec c)=\dfrac{24}{30}\), \(C(\vec c,\vec a)=\dfrac{28}{30}\) → \(\dfrac{26+48+112}{30}=\dfrac{93}{15}\).",
       m='1회 20번 · 2회 14번'),
 ]),
 ('명제와 진리표', [
  dict(no='15번', t='세 명제 진리표', k='계산',
       q=r"세 명제 \(p\), \(q\), \(r\)에 대한 진리표의 빈칸 \(i\)에 들어갈 숫자가 0이면 \(a_i=10\), 1이면 \(a_i=i\)일 때, \(a_1+a_2+\cdots+a_9\)의 값은?"
         + TB([r'\(p\)', r'\(q\)', r'\(r\)', r'\((p\wedge q)\wedge r\)', r'\((p\vee q)\vee r\)', r'\((p\oplus q)\oplus r\)'],
              [['0', '1', '0', '빈칸 1', '빈칸 2', '빈칸 3'], ['1', '0', '0', '빈칸 4', '빈칸 5', '빈칸 6'], ['0', '0', '1', '0', '1', '1'], ['1', '1', '1', '빈칸 7', '빈칸 8', '빈칸 9']], first=False),
       c=['45', '60', '65', '70', '85'], kind=None, a=2,
       p=r"빈칸 값: 0,1,1 / 0,1,1 / 1,1,1 → \(10+2+3+10+5+6+7+8+9=60\). \((1\oplus1)\oplus1=0\oplus1=1\)에 주의.",
       m='3회 7번 · 3회 단답1'),
 ]),
 ('단답형 — 용어', [
  dict(no='단답형 1 (16번)', t='인공지능 + 구성 요소', k='개념', q="다음 설명하는 개념과 그 세 가지 핵심 구성 요소(교과서 기준)를 쓰시오."
       + BX("• 인식, 학습, 추론, 행동 등과 같은 인간의 지적 능력이나 사고 과정을 컴퓨터가 실행할 수 있도록 구현하는 기술<br>• 단답형 2에서 설명하는 것을 포함하는 상위 개념"),
       c=None, a='인공지능 / 데이터, 모델, 학습', p="교과서 11쪽 첫 문장 그대로. 구성 요소 3개까지 4점(각 1점).", m='3회 1번 · 5회 1번'),
  dict(no='단답형 2 (17번)', t='기계학습', k='개념', q="다음 설명하는 개념을 쓰시오."
       + BX("• 사람이 학습하듯 컴퓨터가 주어진 자료를 스스로 학습하여 문제를 해결하는 기술<br>• 단답형 1의 하위 개념이면서, 단답형 4를 포함하는 기술"),
       c=None, a='기계학습(머신러닝)', p="인공지능 ⊃ <b>기계학습</b> ⊃ 딥러닝.", m='4회 2번'),
  dict(no='단답형 3 (18번)', t='퍼셉트론', k='개념', q="다음 설명하는 개념을 쓰시오."
       + BX("• 다수의 입력 신호에 가중치를 곱해 합산한 값이 임곗값을 넘으면 신호를 출력하는, 가장 기본적인 인공신경망 구조<br>• 단답형 4에서 설명하는 것의 가장 기초가 되는 단위"),
       c=None, a='퍼셉트론', p="가장 작은(기본) 인공신경망 단위.", m='4회 4번'),
  dict(no='단답형 4 (19번)', t='딥러닝', k='개념', q="다음 설명하는 개념을 쓰시오."
       + BX("• 뉴런을 이용하여 정보를 처리하는 인간의 뇌처럼, 단답형 3을 이용하여 작동되도록 하는 기계학습의 한 방식<br>• 인공신경망을 아주 깊게 쌓아서 학습하는 기술"),
       c=None, a='딥러닝(심층 학습)', p="퍼셉트론을 이용하는 기계학습 방식 = 딥러닝.", m='3회 5번 · 5회 2번'),
  dict(no='단답형 5 (20번)', t='전문가 시스템 + 구성 요소', k='개념', q="다음 설명하는 개념과 그 세 가지 핵심 구성 요소(교과서 기준)를 쓰시오."
       + BX("• 전문적 지식과 정보를 이용해 대형 지식 베이스를 구축하고, 사용자가 해결해야 할 문제가 주어질 때 추론을 통해 응답하는 시스템<br>• 특히 답이 명확하고 규칙이 복잡한 분야에서 유용함."),
       c=None, a='전문가 시스템 / 사용자 인터페이스, 추론 엔진, 지식 베이스', p="교과서 26쪽. 구성 요소 3개가 단답 단골.", m='1회 6번 · 3회 10번 · 5회 7번'),
  dict(no='단답형 6 (21번)', t='알고리즘·순서도', k='개념', q="(가), (나)에서 설명하는 개념을 순서대로 쓰시오."
       + BX("(가) 어떤 문제를 해결하는 계산 방법 또는 처리 과정의 순서<br>(나) (가)를 기호와 그림을 통해 나타낸 것으로, 프로그램의 논리적 흐름을 시각적으로 분석하고 설계할 때 사용하는 도구"),
       c=None, a='(가) 알고리즘 (나) 순서도', p="교과서 28쪽 정의 그대로.", m='5회 3번'),
 ]),
 ('단답형 — TF-IDF', [
  dict(no='단답형 8 (23번)', t='역문서 빈도', k='계산', q="찌개 조리법 문서 A, B, C의 단어 빈도(TF)가 다음과 같다. 소고기의 역문서 빈도(IDF)를 구하시오." + TBL89,
       c=None, a='3', p=r"소고기는 B에만 등장 → DF = 1, \(\mathrm{IDF}=\dfrac{n}{\mathrm{DF}}=\dfrac31=3\).", m='3회 18번 · 4회 19번'),
  dict(no='단답형 9 (24번)', t='문서별 최대 TF-IDF', k='계산', q="(단답형 8의 표) 각 조리법 문서에서 TF-IDF 값이 가장 큰 단어 1개씩과 그 TF-IDF 값을 쓰시오.",
       c=None, a=r"A: 김치 \(\dfrac92\) / B: 소고기 \(6\) / C: 돼지고기 \(\dfrac92\)",
       p=r"DF = (3, 2, 2, 2, 2, 3, 1), IDF = \(\left(1,\tfrac32,\tfrac32,\tfrac32,\tfrac32,1,3\right)\). 모든 문서에 나오는 양파·고춧가루는 IDF = 1이라 TF가 커도 밀린다.",
       m='1회 단답2 · 3회 18번'),
 ]),
]

OUT = [('13번', '이미지 행렬(RGB 픽셀 색상)'), ('14번', '전치행렬과 흑백 이미지'),
       ('단답형 7 (22번)', '이미지 합성 가중치 α'), ('단답형 10 (25번)', '행렬 아다마르 곱으로 이미지 그리기')]

def card(e):
    c = e['c']; kind = e.get('kind'); a = e['a']
    chs = ''
    if c:
        items = []
        for j, ch in enumerate(c, 1):
            on = (kind == 'M' and j in a) or (kind != 'M' and a == j)
            mark = tagO(j in a) if kind == 'M' else ''
            items.append(f'<div class="cc{" on" if on else ""}"><span class="cn">{CIRC[j-1]}</span>{mark}<span>{ch}</span></div>')
        wide = max(len(x) for x in c)
        cls = 'chs r5' if wide <= 8 else ('chs r2' if wide <= 30 else 'chs')
        if any('\\(' in x for x in c): cls = 'chs r5' if wide <= 26 else ('chs r2' if wide <= 60 else 'chs')
        chs = f'<div class="{cls}">' + ''.join(items) + '</div>'
    if kind == 'M': ans = ''.join(CIRC[j-1] for j in sorted(a))
    elif c: ans = CIRC[a-1] if a else '없음'
    else: ans = ''
    ansb = f'<span class="ans">정답 {ans}</span>' if ans else ''
    sa = '' if c else f'<div class="sa">정답: {a}</div>'
    kc = 'k2' if e['k'] == '개념' else 'k1'
    return (f'<div class="card"><div class="hd"><span class="no">{e["no"]}</span><span class="tt">{e["t"]}</span>'
            f'<span class="src {kc}">{e["k"]}형</span>{ansb}</div><div class="q">{e["q"]}{chs}{sa}</div>'
            f'<div class="trap"><b>포인트</b> {e["p"]}<div class="mt">우리 자료 대응: {e["m"]}</div></div></div>')

def build(out):
    n_in = sum(len(v) for _, v in ITEMS)
    body = ('<h1>경문고 2026-1 중간 인공지능수학 분석지</h1>'
            f'<div class="sub">범위(교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리)에 맞는 {n_in}문항만 · 선택형 15문항 60점 + 단답형 10문항 40점 중</div>'
            '<div class="ov"><div><b>제외(범위 밖)</b> ' + ' · '.join(f'{a} {b}' for a, b in OUT) + '</div>'
            '<div><b>눈여겨볼 점</b> ① 학습 방법 1~3번은 교과서 15쪽 <u>활용 사례 박스</u> 문구 그대로 '
            '② <u>인물 업적</u>(민스키·로젠블랫·힌턴)이 3문항 — 연도+인물 짝 외우기 '
            '③ 단답형 6개가 <u>용어 + 구성 요소</u> 쓰기 '
            '④ 계산은 퍼셉트론 범위·자카드·유클리드/코사인·진리표·TF-IDF로 우리 1~5회 유형과 같음</div></div>')
    for i, (nm, its) in enumerate(ITEMS):
        body += (f'<div class="sec{" first" if i == 0 else ""}"><div class="grp"><div class="sech"><span class="sn">{nm}</span>'
                 f'<span class="cnt">{len(its)}문항</span></div>' + card(its[0]) + '</div>' + ''.join(card(e) for e in its[1:]) + '</div>')
    css = CSS + (".ov{border:.6pt solid #bbb;background:#fafafa;padding:5pt 8pt;font-size:8.7pt;line-height:1.7;margin-bottom:4pt}"
                 ".ov b{font-family:'GY','GL';color:#1f4e9a;font-weight:400;margin-right:4pt}"
                 ".mt{color:#777;font-size:8pt;margin-top:1pt}.q .gt{font-size:8.2pt}")
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{css}</style></head><body>{body}</body></html>')
    open(os.path.join(HERE, 'km_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(CON, 'render3.js'), os.path.join(HERE, 'km_src.html'), os.path.join(HERE, 'km_tmp.pdf'), 'bg'], cwd=CON, check=True)
    os.replace(os.path.join(HERE, 'km_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
