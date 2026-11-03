# -*- coding: utf-8 -*-
# 미적분Ⅰ 기말 견본 — 출제 지침서(지침/front.md, analysis.json) 반영. 17·18·서답형2 구조 변경.
import sys, re
sys.path.insert(0, '/home/user/Finale/output/build/부교재_기말/parts')
from items_common import COND, BOGI, FIG

PTS = [4.0] * 4 + [4.2] * 4 + [4.4] * 2 + [4.5] * 2 + [4.7] * 3 + [4.9] + [5.2] * 2
CH5 = ['T:ㄱ', 'T:ㄱ, ㄴ', 'T:ㄱ, ㄷ', 'T:ㄴ, ㄷ', 'T:ㄱ, ㄴ, ㄷ']

# 번호: (본문, 선지, 정답 번호, 원본 키, 원본 출처, 변형, 난도(변형 후))
import os as _os
_P = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'parts')
ITEMS, SITEMS = {}, {}
for _f in sorted(_os.listdir(_P)):
    if _f.startswith('p') and _f.endswith('.py'):
        _ns = {}; exec(open(_os.path.join(_P, _f)).read(), _ns)
        ITEMS.update(_ns.get('ITEMS', {})); SITEMS.update(_ns.get('SITEMS', {}))

def _body(it):
    b = it['body']
    if it.get('cond'): b += COND(it['cond'])
    if it.get('bogi'): b += BOGI(it['bogi'])
    if it.get('after'): b += it['after']
    return b

# 번호: (본문, 선지, 정답 번호, 원본 키, 원본 출처, 변형, 난도(변형 후))
RAW = {n: (_body(it), it['choices'], it['ans'], it['key'], it['src'], it['var'], it['level']) for n, it in sorted(ITEMS.items())}

def with_pt(body):
    b = body.rstrip()
    if not re.search(r'(</div>|</fieldset>|\\\])\s*$', b):
        return b + '{PT}'
    i = b.rfind('?')
    if i >= 0:
        rest = re.sub(r'<fieldset[\s\S]*?</fieldset>', '', b[i + 1:])
        rest = re.sub(r'<div class="(cond|fig)"[\s\S]*$', '', rest)
        if not re.search(r'[가-힣]', re.sub(r'<[^>]+>', '', rest)) or re.fullmatch(r'\s*\(단,[\s\S]*\)\s*', re.sub(r'<[^>]+>', '', rest)):
            js = [x for x in (b.find('<fieldset', i), b.find('<div class="cond"', i), b.find('<div class="fig"', i)) if x >= 0]
            j = min(js) if js else len(b)
            while j > i + 1 and b[j - 1] in ' \n': j -= 1
            return b[:j] + '{PT}' + b[j:]
    return b + '{PTR}'

def _fix(s):
    return re.sub(r'\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)', lambda m: m.group(0).replace('&lt;', '<').replace('&gt;', '>'), s)

Q = {n: (PTS[n - 1], _fix(with_pt(r[0])), r[1]) for n, r in RAW.items()}
ANS = {n: r[2] for n, r in RAW.items()}
CHW, CHM = {}, {}

S1 = _fix(_body(SITEMS['S1']))
S1S = SITEMS['S1']['subs']
S2 = _fix(_body(SITEMS['S2']))
S2S = SITEMS['S2']['subs']
SA_ANS = {s: SITEMS[s]['ans'] for s in ('S1', 'S2')}
SRC_S = {s: (SITEMS[s]['key'], SITEMS[s]['src'], SITEMS[s]['var'], SITEMS[s]['level']) for s in ('S1', 'S2')}
