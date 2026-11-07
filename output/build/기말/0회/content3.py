# -*- coding: utf-8 -*-
# 기말 0회 = 양식 점검용. 부교재 DB 문항을 변형 없이 원문 그대로, 배치만 출제 습관 분석(번호대 규칙)대로.
import sys, re
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말')
import items_final as F

PTS = [4.0] * 4 + [4.2] * 4 + [4.4] * 2 + [4.5] * 2 + [4.7] * 3 + [4.9] + [5.2] * 2
# 번호: (DB 키, 배치 근거)
PICK = {
    1: ('D55', '1–4 최신 평가원 3점'), 2: ('I52', '1–4 최신 평가원 3점'), 3: ('J50', '1–4 최신 평가원 3점'), 4: ('M11', '1–4 유형 EBS'),
    5: ('D20', '5–8 유형 EBS'), 6: ('M35', '5–8 Level Up'), 7: ('I39', '5–8 Level Up'), 8: ('J20', '5–8 유형 EBS'),
    9: ('D71', '9 평가원 21번급'), 10: ('I58', '9–12 최신 평가원'), 11: ('J17', '9–12 대표기출'), 12: ('M53', '9–12 최신 평가원'),
    13: ('D44', '13–16 Level Up'), 14: ('J63', '13–16 최신 평가원'), 15: ('M34', '13–16 Level Up'), 16: ('J72', '16 평가원 보기형'),
    17: ('I75', '17–18 최신 평가원 킬러'), 18: ('I76', '17–18 최신 평가원 킬러'),
}
S1K, S2K = 'M17', 'M59'   # 서답형 1: 기본(대표기출), 서답형 2: 최신 평가원 킬러

def with_pt(body):
    b = body.rstrip()
    if not re.search(r'(</div>|</fieldset>|\\\])\s*$', b):
        return b + '{PT}'
    i = b.rfind('?')
    tail = re.sub(r'<[^>]+>', '', b[i + 1:]) if i >= 0 else 'x'
    if i >= 0:   # 질문 뒤에 상자·보기·그림만 있으면 질문 바로 뒤에 배점 (중간고사 실제 양식과 같음)
        rest = re.sub(r'<fieldset[\s\S]*?</fieldset>', '', b[i + 1:])
        rest = re.sub(r'<div class="(cond|fig)"[\s\S]*$', '', rest)
        if not re.search(r'[가-힣]', re.sub(r'<[^>]+>', '', rest)) or re.fullmatch(r'\s*\(단,[\s\S]*\)\s*', re.sub(r'<[^>]+>', '', rest)):
            js = [x for x in (b.find('<fieldset', i), b.find('<div class="cond"', i), b.find('<div class="fig"', i)) if x >= 0]
            j = min(js) if js else len(b)
            while j > i + 1 and b[j - 1] in ' \n': j -= 1
            return b[:j] + '{PT}' + b[j:]
    return b + '{PTR}'

Q = {}
for n, (k, _) in PICK.items():
    body, ch, ans, src = F.I[k]
    assert ch, k
    Q[n] = (PTS[n - 1], with_pt(body), ch)
ANS = {n: '①②③④⑤'.index(F.I[k][2]) + 1 for n, (k, _) in PICK.items()}
CHW, CHM = {}, {}
S1, S1S = F.I[S1K][0], [('10점, 풀이과정을 상세히 쓰시오.', None)]
S2, S2S = F.I[S2K][0], [('10점, 답만 적으시오.', None)]
