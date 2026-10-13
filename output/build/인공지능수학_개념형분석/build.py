# -*- coding: utf-8 -*-
"""인공지능 수학 1~5회 개념형 문항 분석자료"""
import os, re, sys, subprocess, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extra import EXTRA
HERE = os.path.dirname(os.path.abspath(__file__))
AIM = os.path.dirname(HERE)
SCR = os.path.join(AIM, '..')
FONTS = os.path.join(SCR, 'fonts')
KATEX_CSS = os.path.join(SCR, 'node_modules', 'katex', 'dist', 'katex.min.css')
CIRC = '①②③④⑤'

def load(r):
    spec = importlib.util.spec_from_file_location(f'c{r}', os.path.join(AIM, f'r{r}', 'content3.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = {r: load(r) for r in range(1, 6)}

# (회, 번호, 표시형식) — X1: 옳지 않은 것 1개, O1: 옳은 것 1개, B: [보기] 고르기, None: 짝짓기·빈칸·용어
SECTIONS = [
 ('인공지능의 개념과 수학', '교과서 11–13쪽',
  ['인공지능 = 인식·학습·추론·행동 등 인간의 지적 능력을 컴퓨터로 구현하는 기술',
   '핵심 구성 요소: <b>데이터 · 모델 · 학습</b> (모델은 주로 함수 형태)',
   '<b>데이터 → 집합·벡터·행렬</b>, <b>학습 → 미분·확률</b> (이 짝을 뒤집는 함정이 반복됨)',
   '음성 = 주기가 다른 삼각함수의 합, 이미지 = 픽셀 값의 행렬, 이미지 변환 = 행렬 연산'],
  [(3, 1, 'B'), (4, 1, 'B'), (5, 1, 'X1')]),
 ('AI · 기계학습 · 딥러닝', '교과서 14–19쪽',
  ['포함 관계: <b>인공지능 ⊃ 기계학습 ⊃ 딥러닝</b>',
   '딥러닝 = 퍼셉트론(인공신경망)을 이용하는 기계학습, 심층 학습, 여러 층의 모델',
   '<b>단층 퍼셉트론 = 입력층 + 출력층</b>, 은닉층이 1개 이상이면 다층 퍼셉트론',
   '관계도: 기계학습 1980년대, 딥러닝 2010년대'],
  [(1, 1, 'O1'), (2, 1, 'X1'), (5, 2, 'B'), (3, 5, 'X1')]),
 ('학습 방법', '교과서 14–15쪽',
  ['<b>지도학습</b>: 레이블링(정답)된 데이터 — 스팸 분류',
   '<b>비지도학습</b>: 정답 없이 입력값만, 숨은 패턴·군집 — 비슷한 회원 묶기',
   '<b>강화학습</b>: 보상으로 최적 행동 강화 — 자율 주행 시뮬레이션',
   '훈련 데이터에 답을 달아 주는 것 = 레이블링'],
  [(2, 4, None), (3, 3, None), (4, 2, 'X1')]),
 ('인공지능의 역사', '교과서 16·20–25쪽',
  ['1936 튜링 기계 → <b>1950 튜링 「계산 기계와 지능」, 튜링 테스트</b>',
   '1955 존 매카시 제안서 → <b>1956 다트머스 회의, ‘인공지능’ 용어 처음 사용</b>',
   '1957 로젠블랫 퍼셉트론 → 민스키·페퍼트 XOR 한계 지적 → 1986 힌턴 등 오류 역전파',
   '1997 딥블루–카스파로프(체스), 2014 유진 구스트만 튜링 테스트 통과 발표, 2016 알파고–이세돌'],
  [(3, 2, 'X1'), (4, 3, 'B')]),
 ('뉴런 · 퍼셉트론 · 활성화함수', '교과서 16–17쪽',
  ['퍼셉트론: 여러 값을 입력받아 <b>하나의 값</b>을 출력하는 <b>가장 작은</b> 인공신경망 단위',
   '가중치 = 입력 신호의 중요도, 임곗값 = 출력이 0→1로 바뀌는 기준',
   '활성화함수: 가중합이 임곗값보다 큰지 작은지 구별해 출력에 대응 (계단·렐루·시그모이드)',
   '<b>시그모이드 f(0)=0.5</b>, 렐루는 x≥0에서 f(x)=x라 1보다 클 수 있음'],
  [(4, 4, 'X1'), (3, 4, 'B'), (5, 'S1', None)]),
 ('명제와 논리 연산', '교과서 20–22쪽',
  ['명제 = 참·거짓을 <b>명확히 판별</b>할 수 있는 문장 (거짓인 문장도 명제)',
   '명제 아님: 주관(재미없다, 즐겁다), 모호(0에 가까운), 변수에 따라 달라지는 식(x−1≤3)',
   '¬: 반대 / ∨: 하나라도 참이면 참 / ∧: 하나라도 거짓이면 거짓 / ⊕: <b>서로 다를 때만 참</b>',
   '진릿값 계산식: p∧q = pq, p∨q = p+q−pq, p⊕q = p+q−2pq'],
  [(2, 5, None), (4, 6, 'B'), (5, 5, 'B'), (5, 6, None), (2, 6, None), (4, 7, None), (3, 6, 'B')]),
 ('XOR와 단층 퍼셉트론의 한계', '교과서 24–25쪽',
  ['단층 퍼셉트론 = 직선 하나로 영역 구분 → AND·OR 가능, <b>XOR 불가능</b>',
   'x₁⊕x₂ = (¬x₁∧x₂)∨(x₁∧¬x₂) → 다층 퍼셉트론으로 구현',
   '민스키·페퍼트가 한계 지적 → 다층 퍼셉트론 + 오류 역전파(전체 오차 최소화)로 해결'],
  [(3, 9, 'B'), (4, 9, 'B')]),
 ('전문가 시스템', '교과서 26쪽',
  ['구성: <b>사용자 인터페이스 · 추론 엔진 · 지식 베이스</b>',
   '사용자 ↔ 인터페이스 ↔ 추론 엔진 ↔ 지식 베이스 ↔ 전문가 (<b>사용자와 전문가는 직접 소통 X</b>)',
   '증상 = 사실, 규칙 = 지식 베이스, 사실+규칙 → 결론 = 추론 엔진',
   '퍼지 이론·확률적 방법 활용, 1960년대 개발 → 1980년대 상업적 번영'],
  [(1, 6, 'O1'), (3, 10, 'X1'), (5, 7, None)]),
 ('알고리즘과 순서도', '교과서 28–29쪽',
  ['문제 해결의 계산 방법·처리 순서 = <b>알고리즘</b>, 이를 기호·그림으로 = <b>순서도</b>',
   '둥근 사각형 시작·끝 / 직사각형 처리 / 마름모 판단 / 화살표 흐름 / <b>물결 사각형 = 문서 출력(인쇄)</b>',
   'ax²+bx+c=0 순서도: a=0 → b=0? → c=0? (참이면 해 무수히 많음, 거짓이면 해 없음)'],
  [(5, 3, None), (3, 11, 'X1'), (5, 4, None)]),
 ('데이터의 종류', '교과서 34쪽',
  ['<b>정형</b>: 정해진 형식(수치·표) — 체력 검사 결과, 혈액형, 게시판별 글의 개수',
   '<b>비정형</b>: 고정 형식 없음 — 글, 사진, 이미지, SNS 글, 의견',
   '정형 중 <b>연속형</b>(키·몸무게) vs <b>범주형</b>(혈액형·지역·설문 단계)'],
  [(1, 3, 'B'), (4, 12, None), (3, 12, 'B')]),
 ('빅데이터', '교과서 34–36쪽',
  ['5V: <b>규모 · 속도 · 다양성 · 정확성 · 가치</b> (‘확실성’ 없음)',
   '단위: KB 10³, MB 10⁶, GB 10⁹, <b>TB 10¹²</b>, PB 10¹⁵',
   '‘21세기의 원유’, 지난 10년간 데이터의 약 90% 생산, 비정형이 약 80% 이상',
   '<b>비정형 → 정형으로 가공</b>해야 처리 쉬움, 빅데이터와 AI는 <b>상호 보완</b>'],
  [(1, 2, None), (2, 2, 'X1'), (3, 13, 'X1'), (4, 13, 'X1'), (5, 10, 'B')]),
 ('빅데이터·AI 활용 사례', '교과서 37–39쪽',
  ['장애인 콜택시 배차 → <b>합성곱 신경망(CNN)</b>',
   '맞춤형 복지 사각지대 예측 → <b>GBM 알고리즘</b>',
   '해양 안전 세이프존 → <b>다중회귀분석</b> (입력 변수 2개 이상, 출력 1개)'],
  [(3, 14, None), (5, 11, None)]),
 ('데이터 편향성', '교과서 40–41쪽',
  ['원본 데이터의 편향(불균형·편견)이 그대로 학습되어 판단이 치우침',
   '<b>양만 많다고 해결 X</b> — 양과 질 모두 중요',
   '사례: 백인 남성 위주 얼굴 인식, 하얀 백조, 2018 채용 AI(여성 감점 → <b>결국 폐기</b>)'],
  [(1, 4, None), (2, 3, 'O1'), (3, 15, 'X1'), (4, 14, 'X1')]),
 ('텍스트 데이터의 표현', '교과서 48–54쪽',
  ['어절 분리 → 기본형 → 문장 부호·<b>불용어</b> 제거 → <b>단어집합(중복 X, 순서 X)</b>',
   '원-핫 벡터: 해당 성분만 1, 차원 = 전체집합 원소 수 / 빈도수 벡터: 단어가방 모형',
   '원-핫·빈도수 벡터의 한계: 의미 X, 차원이 매우 큼 → <b>단어 임베딩(대표: Word2vec)</b>',
   '형태소 = 뜻을 가진 가장 작은 단위, 단어 구름 = 빈도에 비례한 크기'],
  [(5, 12, 'X1'), (3, 16, 'B'), (5, 14, 'B'), (5, 15, 'X1')]),
 ('TF-IDF', '교과서 57–61쪽',
  ['TF = 한 문서 안 등장 횟수, <b>DF = 그 단어가 나온 문서 수</b>, IDF = n/DF (또는 log)',
   '드문 단어 → DF 작음 → <b>IDF 큼</b>, 모든 문서에 나오는 단어 → IDF 작음',
   'TF 총합 ≥ DF, TF-IDF 크기의 <b>절대적 기준값은 없음</b>',
   'TF 단어 구름 ≠ TF-IDF 단어 구름 (다를 수 있음)'],
  [(1, 17, 'X1'), (5, 16, 'X1')]),
 ('감성 분석', '교과서 67–69쪽',
  ['감정(기쁨·슬픔·놀람·화남·두려움·혐오) vs <b>감성(긍정·중립·부정)</b>',
   'KNU 감성 사전: −2, −1, 0, 1, 2 / 사전에 없는 단어 = 중립',
   '같은 단어도 의미에 따라 점수 다름(‘잘’ 능력 긍정 1, 단순 긍정 0)',
   '감성 점수 합 규칙의 한계 → <b>기계학습 도입</b>'],
  [(5, 18, 'X1'), (5, 19, 'B')]),
 ('벡터와 유사도', '교과서 72–77쪽',
  ['kā = (ka₁, ka₂) — <b>모든 성분</b>에 k',
   '자카드: 공통 원소 많을수록 1 / <b>유클리드: 작을수록(0에 가까울수록) 유사</b> / <b>코사인: 클수록(1에 가까울수록) 유사</b>',
   '코사인 = 방향만 비교(각이 작을수록 큼), 0°→1, 90°→0 / 빈도수 벡터의 코사인은 0~1',
   '일반적으로 코사인이 더 정확·많이 사용, <b>크기가 비슷하거나 크기 정보가 중요하면 유클리드</b>'],
  [(5, 20, 'X1'), (2, 17, 'O1'), (3, 21, 'B'), (4, 21, 'B'), (5, 21, 'B')]),
]

TRAP = {
 (3, 1): 'ㄷ은 짝을 뒤집었다. <b>데이터 → 집합·벡터·행렬, 학습 → 미분·확률</b>.',
 (4, 1): 'ㄹ “인공신경망에 수학이 쓰이지 않는다” × — 행렬·합성함수·확률·미적분·통계·벡터가 쓰인다.',
 (5, 1): '‘인공지능’ 용어는 <b>1956년 다트머스 회의</b>. 1950년 튜링 논문은 튜링 테스트를 제시.',
 (1, 1): '포함 관계를 거꾸로 쓴 ①②③, 지도/비지도를 바꾼 ④가 함정.',
 (2, 1): '딥러닝은 기계학습의 <b>일부</b>이고 인공신경망 그 자체를 이용한다.',
 (5, 2): 'ㄹ은 포함 관계 방향이 반대. <b>AI ⊃ ML ⊃ DL</b>.',
 (3, 5): '단층 퍼셉트론에는 <b>은닉층이 없다</b>(입력층+출력층).',
 (2, 4): '정답 유무로 지도/비지도, 보상이면 강화.',
 (3, 3): '“정답 표시” → 지도, “비슷한 것끼리 묶기” → 비지도, “보상” → 강화.',
 (4, 2): '레이블링된 데이터로만 학습하는 것은 <b>지도학습</b>.',
 (3, 2): '딥블루–카스파로프는 <b>1997년</b>, 2016년은 알파고–이세돌.',
 (4, 3): 'ㄹ: 튜링 기계는 <b>1936년</b>, 다트머스 회의(1956)는 ‘인공지능’ 용어가 처음 쓰인 회의.',
 (4, 4): '퍼셉트론은 출력이 <b>하나</b>, <b>가장 작은</b> 단위. “여러 개 출력·가장 큰” 둘 다 틀림.',
 (3, 4): 'ㄷ 시그모이드 f(0)=<b>0.5</b>. ㄹ 렐루는 상한이 없어 1보다 클 수 있다(맞음).',
 (5, 'S1'): '순서: 가중합 → <b>임곗값</b>과 비교 → <b>활성화함수</b>로 출력. 단답 빈칸 단골.',
 (2, 5): '“수학은 재미없다” — 주관적이라 명제가 아니다. “24는 홀수이다”는 <b>거짓인 명제</b>.',
 (4, 6): '“참인 명제” 고르기: ㄱ은 거짓인 명제(4와 6의 최대공약수 2), ㄹ은 명제가 아님.',
 (5, 5): 'ㄴ은 거짓이어도 명제(2x+1=5). ㄷ 변수 의존, ㄹ 모호한 기준 → 명제 아님.',
 (5, 6): '(3) 3&lt;3은 거짓, (4) 8의 약수에 8 빠짐 → 거짓.',
 (2, 6): '⊕는 같으면 <b>거짓</b>, 다를 때만 참.',
 (4, 7): '오리너구리는 포유류 → p 거짓, q 참. ⊕는 하나만 참이므로 참.',
 (3, 6): '네 경우를 대입해 확인. p⊕q는 (1,1)에서 1+1−2=0.',
 (3, 9): 'ㄴ 단층 퍼셉트론(직선 하나)으로는 XOR <b>불가</b>.',
 (4, 9): 'ㄷ XOR은 직선 하나로 나눌 수 <b>없다</b>.',
 (1, 6): '사용자와 전문가는 직접 소통하지 않는다. 질의에 답하는 것은 <b>추론 엔진</b>.',
 (3, 10): '0과 1 사이 값을 다루는 <b>퍼지 이론</b>이 활용되었다.',
 (5, 7): '증상 = 사실, 규칙 = 지식 베이스, 결론 도출 = 추론 엔진.',
 (5, 3): '알고리즘(방법) → 순서도(그림). 순서를 바꾼 ②가 함정.',
 (3, 11): '물결 모양 사각형 = <b>문서 출력(인쇄)</b>. 반복은 마름모+화살표로 표현.',
 (5, 4): 'a=0일 때 bx+c=0: b≠0이면 x=−c/b, b=0·c=0이면 해 무수히 많음, b=0·c≠0이면 해 없음.',
 (1, 3): '글·사진은 비정형, “글의 <b>개수</b>”는 수치라 정형.',
 (4, 12): '이미지·의견·SNS 글 = 비정형, 체력 검사 결과·혈액형 = 정형.',
 (3, 12): '키·몸무게 = 연속형. 설문 단계(매우 낮음~매우 높음)도 범주형.',
 (1, 2): '여러 형태(사진·동영상·음악) → <b>다양성</b>.',
 (2, 2): '5V에 ‘확실성’은 없다.',
 (3, 13): '1 TB = <b>10¹²</b> 바이트 (10⁹은 GB).',
 (4, 13): '정형/비정형을 뒤집었다. <b>비정형 → 정형으로 가공</b>.',
 (5, 10): 'ㄹ “서로 독립” × — 상호 보완 관계.',
 (3, 14): '콜택시 = CNN, 복지 = GBM, 세이프존 = 다중회귀분석. 순서 짝짓기 단골.',
 (5, 11): '입력 변수 2개 이상 + 출력 1개의 관계 분석 = <b>다중회귀분석</b>.',
 (1, 4): '특정 집단으로 치우친 학습 → <b>데이터 편향성</b> (불균형·차별·불평등 아님).',
 (2, 3): '편향의 원인은 학습 데이터가 현실의 다양한 집단을 <b>균형 있게 반영하지 못한 것</b>.',
 (3, 15): '데이터 양만 많아도 원본이 편향되면 편향성 발생. 양과 질 모두 중요.',
 (4, 14): '개선을 시도했지만 재발하지 않는다는 확신이 없어 <b>폐기</b>되었다.',
 (5, 12): '단어집합은 <b>중복을 허용하지 않는다</b>.',
 (3, 16): 'ㄷ 단어집합은 순서·중복 횟수를 나타낼 수 <b>없다</b> → 그래서 빈도수 벡터 사용.',
 (5, 14): 'ㄹ 대표적인 단어 임베딩은 <b>Word2vec</b>. TF-IDF는 중요도 가중치.',
 (5, 15): 'TF 단어 구름(많이 나온 단어)과 TF-IDF 단어 구름(특징적인 단어)은 <b>다를 수 있다</b>.',
 (1, 17): '일부 문서에만 나오는 단어는 DF가 작아 IDF가 <b>커진다</b>. ③이 거꾸로.',
 (5, 16): 'TF-IDF에는 절대적 기준값이 <b>없다</b>(목적에 따라 상대적으로 설정).',
 (5, 18): '‘잘’도 의미에 따라 점수가 다르다(능력 긍정 1, 단순·의지 긍정 0).',
 (5, 19): '합 −6 → 규칙상 부정이지만 실제는 긍정 → 단순 규칙의 한계 → 기계학습.',
 (5, 20): 'kā는 <b>모든 성분</b>에 k를 곱한다: (ka₁, ka₂).',
 (2, 17): '유클리드는 작을수록, 코사인은 클수록 유사. ‘유클리드가 더 정확’ ×.',
 (3, 21): 'ㄷ 크기 정보가 중요할 때는 코사인이 유용하지 <b>않을</b> 수 있다(교과서 77쪽 단점).',
 (4, 21): 'ㄷ 방향만 비교하는 것은 <b>코사인</b>. ㄹ은 교과서 77쪽 문장 그대로(맞음).',
 (5, 21): 'ㄹ 각이 <b>작을수록</b> 코사인 유사도가 크다. 0°→1, 90°→0.',
}

def src_kind(s):
    if re.search(r'세화고|명지고|대일고', s): return ('학교 기출', 'k1')
    if re.search(r'평가|마무리|대비|확인하기|함께하기|개념 정리', s): return ('교과서 문제', 'k2')
    return ('교과서 본문 → 자체 제작', 'k3')

def tagO(o): return '<span class="ox o">○</span>' if o else '<span class="ox x">×</span>'

def card(r, n, kind):
    c = C[r]
    figbase = 'file://' + os.path.join(AIM, f'r{r}') + '/'
    if n == 'S1':
        stem = c.SA[0].replace(c.SAP, '').strip()
        src = c.SA_SRC[0]; ans_html = f'<div class="sa">정답: {c.SA_ANS[0]}</div>'; num = '단답형 1'
        title = '활성화함수'; chs = ''
    else:
        q = c.Q[n]; stem = q[1].replace('{PT}', ''); src = c.SRC[n]; a = c.ANS[n]; num = f'{n}번'
        sol = open(os.path.join(AIM, f'r{r}', 'sol.py')).read()
        title = re.search(rf'^ {n}: \("([^"]+)"', sol, re.M).group(1)
        if kind == 'B':
            pick = set(re.findall('[ㄱ-ㅁ]', q[2][a - 1]))
            stem = re.sub(r'<span class="bk">([ㄱ-ㅁ])\.</span>', lambda m: f'<span class="bk">{m.group(1)}.</span>{tagO(m.group(1) in pick)}', stem)
        items = []
        for i, ch in enumerate(q[2]):
            t = ch[2:] if ch.startswith('T:') else rf'\({ch}\)'
            mark = ''
            if kind == 'X1': mark = tagO(i + 1 != a)
            elif kind == 'O1': mark = tagO(i + 1 == a)
            items.append(f'<div class="cc{" on" if i + 1 == a else ""}"><span class="cn">{CIRC[i]}</span>{mark}<span>{t}</span></div>')
        hasm = any('\\(' in c2 for c2 in q[2])
        wide = max(len(c2) for c2 in q[2])
        cls = 'chs r5' if (wide <= 14 and not hasm) else ('chs r2' if wide <= 34 or (hasm and wide <= 70) else 'chs')
        chs = f'<div class="{cls}">' + ''.join(items) + '</div>'
        ans_html = ''
    stem = stem.replace('src="fig', f'src="{figbase}fig')
    k, kc = src_kind(src)
    ansb = f'<span class="ans">정답 {CIRC[c.ANS[n]-1]}</span>' if n != 'S1' else ''
    return (f'<div class="card"><div class="hd"><span class="no">{r}회 {num}</span><span class="tt">{title}</span>'
            f'<span class="src {kc}">{k}</span><span class="sr">{src}</span>{ansb}</div>'
            f'<div class="q">{stem}{chs}{ans_html}</div><div class="trap"><b>포인트</b> {TRAP[(r, n)]}</div></div>')

def summary():
    allitems = [(r, n) for _, _, _, its in SECTIONS for r, n, _ in its]
    kinds = {}
    for r, n in allitems:
        s = C[r].SA_SRC[0] if n == 'S1' else C[r].SRC[n]
        kinds.setdefault(src_kind(s), []).append((r, n))
    rows = ''.join(f'<tr><td>{r}회</td><td>{sum(1 for x in allitems if x[0] == r)}</td></tr>' for r in range(1, 6))
    kr = ''.join(f'<tr><td><span class="src {kc}">{k}</span></td><td>{len(v)}</td></tr>' for (k, kc), v in kinds.items())
    mx = max(len(its) for *_, its in SECTIONS)
    tr = ''.join(f'<tr><td class="l">{nm}</td><td class="l">{pg}</td><td>{len(its)}</td><td class="l"><span class="bar" style="width:{len(its)/mx*70:.0f}pt"></span></td>'
                 f'<td class="l sm">{", ".join(f"{r}-{n}" for r, n, _ in its)}</td></tr>' for nm, pg, _, its in SECTIONS)
    top = [
     ('포함 관계 뒤집기', 'AI ⊃ ML ⊃ DL. “인공지능은 기계학습의 일종” 같은 역방향 문장', '1-1, 2-1, 5-2'),
     ('지도/비지도 바꾸기', '레이블(정답) 있으면 지도, 없으면 비지도, 보상이면 강화', '1-1, 2-4, 3-3, 4-2'),
     ('연도·인물 섞기', '1950 튜링 테스트 / 1956 다트머스 ‘인공지능’ / 1936 튜링 기계 / 1997 딥블루 / 2016 알파고', '3-2, 4-3, 5-1'),
     ('단층 퍼셉트론과 XOR', '단층 = 은닉층 없음, 직선 하나 → XOR 불가 → 다층 + 오류 역전파', '3-5, 3-9, 4-9'),
     ('유사도 방향', '유클리드 작을수록, 코사인 클수록 유사 / 방향만 = 코사인 / 크기 비슷·중요 = 유클리드', '2-17, 3-21, 4-21, 5-21'),
     ('정형/비정형 뒤집기', '형식 없음 = 비정형, 비정형 → 정형으로 가공 / “개수”는 정형', '1-3, 4-12, 4-13'),
     ('데이터 편향성', '양만 많아선 해결 X, 채용 AI는 폐기, 원인은 불균형한 데이터', '2-3, 3-15, 4-14'),
     ('단어집합의 한계', '중복 X, 순서 X → 빈도수 벡터 → 의미 X·고차원 → 임베딩(Word2vec)', '3-16, 5-12, 5-14'),
     ('TF-IDF 성질', '드문 단어 IDF 큼, TF 합 ≥ DF, 절대 기준 없음, TF 구름 ≠ TF-IDF 구름', '1-17, 5-15, 5-16'),
     ('명제 판별', '주관·모호·변수 의존은 명제 X, 거짓인 문장도 명제', '2-5, 4-6, 5-5'),
     ('전문가 시스템 구조', '사용자–전문가 직접 소통 X, 사실/지식 베이스/추론 엔진, 퍼지 이론', '1-6, 3-10, 5-7'),
     ('활성화함수 값', '시그모이드 f(0)=0.5, 렐루는 1 초과 가능, 임곗값→활성화함수', '3-4, 5-S1'),
    ]
    tp = ''.join(f'<tr><td>{i+1}</td><td class="l" style="white-space:nowrap"><b>{a}</b></td><td class="l">{b}</td><td class="l sm">{c}</td></tr>' for i, (a, b, c) in enumerate(top))
    return (f'<h1>인공지능 수학 1~5회 개념형 문항 분석</h1>'
            f'<div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 계산 없이 개념·용어·사실로 푸는 문항 {len(allitems)}개 모음</div>'
            f'<div class="row"><table class="st"><tr><th>회차</th><th>개념형</th></tr>{rows}</table>'
            f'<table class="st"><tr><th>출처 유형</th><th>문항</th></tr>{kr}</table>'
            f'<div class="leg"><b>보는 법</b><br>· 카드 머리: 회차·번호 / 주제 / 출처 유형 / 원 출처 / 정답<br>'
            f'· <span class="ox o">○</span> 옳은 문장(또는 고르는 것), <span class="ox x">×</span> 틀린 문장<br>· 정답 선지는 음영 표시<br>· <b>포인트</b> = 함정과 교과서 문장</div></div>'
            f'<h2>주제별 출제 빈도</h2><table class="tp"><tr><th>주제</th><th>교과서</th><th>수</th><th></th><th>문항</th></tr>{tr}</table>'
            f'<h2>반복 출제 함정 TOP 12</h2><table class="tp"><tr><th>#</th><th>함정</th><th>교과서 기준</th><th>문항</th></tr>{tp}</table>')

CSS = r"""@page{size:A4;margin:13mm 12mm 12mm}
body{font-family:'HB','GL';font-size:9.3pt;color:#111;line-height:1.55;margin:0}
h1{font-family:'GY','GL';font-size:16pt;text-align:center;margin:0 0 3pt}
.sub{text-align:center;color:#555;font-family:'GY','GL';font-size:8.8pt;margin-bottom:9pt}
h2{font-family:'GY','GL';font-size:11.5pt;margin:11pt 0 5pt;border-bottom:1.2pt solid #222;padding-bottom:2pt}
.row{display:flex;gap:10pt;align-items:flex-start}
table{border-collapse:collapse}
th,td{border:.6pt solid #999;padding:2.5pt 5pt;text-align:center;font-size:8.8pt}
th{background:#eef0f3;font-family:'GY','GL';font-weight:400}
.st{width:auto}.tp{width:100%}.l{text-align:left}.sm{font-size:7.9pt;color:#444}
.bar{display:inline-block;height:7pt;background:#5b7db1;border-radius:1pt;vertical-align:middle}
.leg{margin-bottom:6pt;border:.6pt solid #bbb;background:#fafafa;padding:5pt 8pt;font-size:8.6pt;line-height:1.7}
.sec{margin-top:12pt}.sec.first{margin-top:8pt}.grp{break-inside:avoid}
.sech{display:flex;align-items:baseline;gap:8pt;border-bottom:1.4pt solid #222;padding-bottom:2pt;margin:0 0 5pt}
.sech .sn{font-family:'GY','GL';font-size:12.5pt}.sech .pg{font-family:'GY','GL';color:#666;font-size:8.6pt}
.sech .cnt{margin-left:auto;font-family:'GY','GL';font-size:8.6pt;color:#666}
.key{background:#f3f6fb;border-left:3pt solid #5b7db1;padding:4pt 8pt;margin:0 0 7pt;font-size:8.8pt;line-height:1.65}
.key div::before{content:'▪ ';color:#5b7db1}
.card{border:.6pt solid #aaa;border-radius:2pt;margin:0 0 7pt;break-inside:avoid}
.hd{display:flex;align-items:center;gap:6pt;background:#f2f2f2;padding:2.5pt 7pt;border-bottom:.6pt solid #ccc;font-family:'GY','GL';font-size:8.6pt}
.no{font-weight:400}.tt{color:#333}.sr{color:#777;font-size:8pt}
.ans{margin-left:auto;font-weight:400;color:#b42318}
.src{font-size:7.6pt;padding:.5pt 5pt;border-radius:7pt;color:#fff;font-family:'GY','GL'}
.k1{background:#3866b0}.k4{background:#7a4fb0}.sec.ex{break-before:page;margin-top:0}.ext td{font-size:8.6pt;line-height:1.5}.ansc{color:#b42318}.k2{background:#2f8a4f}.k3{background:#c4741c}
.q{padding:4pt 9pt 3pt}
.chs{margin-top:3pt}.chs.r5,.chs.r2{display:grid;column-gap:6pt}.chs.r5{grid-template-columns:repeat(5,1fr)}.chs.r2{grid-template-columns:repeat(2,1fr)}
.cc{display:flex;gap:4pt;align-items:baseline;padding:.6pt 3pt;border-radius:2pt}
.cc.on{background:#fff1c9}
.cn{flex:none;font-family:'GY','GL'}
.ox{flex:none;display:inline-block;width:10pt;text-align:center;font-family:'GY','GL';font-weight:400;margin-right:2pt}
.ox.o{color:#2f8a4f}.ox.x{color:#b42318}
.trap{border-top:.6pt dashed #bbb;padding:3pt 9pt 4pt;font-size:8.7pt;background:#fffaf2}
.trap b:first-child{font-family:'GY','GL';color:#c4741c;margin-right:4pt}
.sa{font-family:'GY','GL';color:#b42318;margin-top:3pt}
.gt{border-collapse:collapse;margin:4pt auto 5pt;font-size:8.4pt;line-height:1.35}
.gt td,.gt th{border:.6pt solid #000;padding:1.5pt 5pt;text-align:center;font-weight:400}
.bx{border:.6pt solid #000;padding:3pt 7pt;margin:4pt 0;line-height:1.55;text-align:left}
.ctr{text-align:center;margin:3pt 0}
.bogi{border:.6pt solid #000;margin:4pt 0;padding:1pt 6pt 4pt}
.bogi legend{margin:0 auto;padding:0 5pt;font-family:'GY','GL';font-size:8.6pt}
.bi{display:flex;gap:3pt;margin:1pt 0;text-align:left;align-items:baseline}.bi .bk{flex:none}
.fig{text-align:center;margin:4pt 0}
.katex{font-size:1.05em}
b,strong,th{font-weight:400}b{color:#1f4e9a}.trap b:first-child{color:#c4741c}"""

def font_css():
    f = lambda n: 'file://' + os.path.join(FONTS, n)
    return (f"@font-face{{font-family:'GY';src:url('{f('griun_yeeun.ttf')}')}}"
            f"@font-face{{font-family:'GL';src:url('{f('gulim_web.ttf')}')}}"
            f"@font-face{{font-family:'HB';src:url('{f('hbatang_web.ttf')}')}}"
            f"@font-face{{font-family:'HYEQ';src:url('{f('hyhwpeq_web.ttf')}')}}")

def chlayout(cs):
    hasm = any('\\(' in c2 for c2 in cs)
    plain = [re.sub(r'\\\(.*?\\\)', 'xx', c2) for c2 in cs]
    wide = max(sum(1 if '가' <= ch <= '힣' else 0.5 for ch in p) for p in plain)
    if hasm: return 'chs r5' if max(len(c2) for c2 in cs) <= 30 else 'chs r2'
    return 'chs r5' if wide <= 8 else ('chs r2' if wide <= 32 else 'chs')

def head():
    return ('<h1>인공지능 수학 1~5회 개념형 문항 분석</h1>'
            '<div class="sub">씨마스 교과서 Ⅰ. 인공지능과 빅데이터 ~ Ⅱ. 텍스트 데이터 처리 · 계산 없이 개념·용어·사실로 푸는 문항 모음 + 미출제 개념 보충 문항 10</div>'
            '<div class="leg"><b>보는 법</b> &nbsp;카드 머리: 회차·번호 / 주제 / 출처 유형 / 원 출처 / 정답 &nbsp;·&nbsp; '
            '<span class="ox o">○</span> 옳은 문장(또는 고르는 것) &nbsp;<span class="ox x">×</span> 틀린 문장 &nbsp;·&nbsp; 정답 선지는 음영 &nbsp;·&nbsp; <b>포인트</b> = 함정과 교과서 문장</div>')

def extra_section():
    keys = ['NAND(부정 논리곱) ∼(A∧B): 둘 다 참일 때만 거짓 / NOR(부정 논리합) ∼(A∨B): 둘 다 거짓일 때만 참 (30–31쪽 탐구 활동)',
            '데이터 = 관찰·측정으로 얻은 가공되지 않은 정보 (33쪽)',
            '정해진 범주가 있으면 수에 대응(붓꽃 0·1·2, 에너지 등급 1~5), 텍스트는 범주가 없어 집합·벡터로 (47쪽)',
            '편향성 최소화를 위한 데이터 정제, 윤리 문제(차별·불공정·사생활 침해) (40–41쪽)',
            '자카드 유사도: 0 ≤ J ≤ 1, J(A, A)=1, 공통 원소 없으면 0 (70쪽 지식 Plus)']
    out = ('<div class="sec ex"><div class="grp"><div class="sech"><span class="sn">미출제 개념 보충 문항</span><span class="pg">1~5회에서 다루지 않은 교과서 내용</span>'
           f'<span class="cnt">{len(EXTRA)}문항</span></div><div class="key">' + ''.join(f'<div>{k}</div>' for k in keys) + '</div>')
    for i, e in enumerate(EXTRA):
        cs = e['c']
        items = ''.join(f'<div class="cc"><span class="cn">{CIRC[j]}</span><span>{c2}</span></div>' for j, c2 in enumerate(cs))
        cardh = (f'<div class="card"><div class="hd"><span class="no">보충 {i+1}번</span><span class="tt">{e["t"]}</span>'
                 f'<span class="src k4">보충 문항</span><span class="sr">{e["pg"]}</span></div>'
                 f'<div class="q">{e["q"]}<div class="{chlayout(cs)}">{items}</div></div></div>')
        out += cardh + ('</div>' if i == 0 else '')
    out += '</div>'
    rows = ''.join(f'<tr><td>{i+1}</td><td class="ansc">{CIRC[e["a"]-1]}</td><td class="l">{e["t"]}</td><td class="l">{e["p"]}</td></tr>' for i, e in enumerate(EXTRA))
    out += ('<div class="sec"><div class="sech"><span class="sn">보충 문항 정답 및 해설</span></div>'
            f'<table class="tp ext"><tr><th style="width:5%">번호</th><th style="width:6%">정답</th><th style="width:20%">주제</th><th>포인트</th></tr>{rows}</table></div>')
    return out

def build(out):
    body = head()
    for i, (nm, pg, keys, its) in enumerate(SECTIONS):
        body += (f'<div class="sec{" first" if i == 0 else ""}"><div class="grp"><div class="sech"><span class="sn">{nm}</span><span class="pg">{pg}</span><span class="cnt">{len(its)}문항</span></div>'
                 f'<div class="key">' + ''.join(f'<div>{k}</div>' for k in keys) + '</div>'
                 + card(*its[0]) + '</div>' + ''.join(card(r, n, kd) for r, n, kd in its[1:]) + '</div>')
    body += extra_section()
    h = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX_CSS}">'
         f'<style>{font_css()}{CSS}</style></head><body>{body}</body></html>')
    open(os.path.join(HERE, 'an_src.html'), 'w').write(h)
    subprocess.run(['node', os.path.join(HERE, 'render3.js'), 'an_src.html', 'an_tmp.pdf', 'bg'], cwd=HERE, check=True)
    os.replace(os.path.join(HERE, 'an_tmp.pdf'), out)

if __name__ == '__main__':
    build(sys.argv[1])
