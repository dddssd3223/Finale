# -*- coding: utf-8 -*-
"""부품 파일 하나 검사: 중복(dupcheck items) · 말투(stylecheck) · 형식(선지 등차, 상자 위치)
사용: python3 checkpart.py parts/p3.py"""
import sys, os, re, subprocess, tempfile
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HERE, '..', '지침')
sys.path.insert(0, '/home/user/Finale/template/db/parts')
from items_common import COND, BOGI
p = os.path.abspath(sys.argv[1])
print('== 중복'); r1 = subprocess.run([sys.executable, os.path.join(G, 'dupcheck.py'), 'items', p]).returncode
ns = {}; exec(open(p).read(), ns)
IT, SI = ns.get('ITEMS', {}), ns.get('SITEMS', {})
def body(it):
    return it['body'] + (COND(it['cond']) if it.get('cond') else '') + (BOGI(it['bogi']) if it.get('bogi') else '') + (it.get('after') or '')
tmp = tempfile.NamedTemporaryFile('w', suffix='.py', delete=False)
tmp.write('RAW = ' + repr({n: (body(it), it.get('choices')) for n, it in IT.items()}) + '\n')
for s, it in SI.items():
    tmp.write(f'{s} = {body(it)!r}\n{s}S = {[(q[0],) for q in it.get("subs", [])]!r}\n')
tmp.close()
print('== 말투'); subprocess.run([sys.executable, os.path.join(G, 'stylecheck.py'), 'check', tmp.name]); os.unlink(tmp.name)
print('== 형식')
def val(c):
    c = re.sub(r'\\displaystyle|\s', '', str(c))
    m = re.fullmatch(r'(-?)\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', c)
    if m: return Fraction(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    return Fraction(int(c)) if re.fullmatch(r'-?\d+', c) else None
bad = 0
for n, it in IT.items():
    ch = it.get('choices') or []; v = [val(c) for c in ch]; msg = []
    if ch and not str(ch[0]).startswith('T:'):
        if None in v: msg.append('선지가 수가 아님(확인)')
        elif len({v[i + 1] - v[i] for i in range(4)}) != 1: msg.append('선지 비등차')
    if it.get('cond') and '?' not in re.sub(r'<[^>]+>', '', it['body']): msg.append('상자→질문형(18번 같은 최고난도 한 문항만 허용)')
    if re.search(r'(?<![a-zA-Z\\])[loWVYZ](?![a-zA-Z])', ''.join(re.findall(r'\\\((.*?)\\\)', body(it)))): msg.append('수식에 l·o·W·V·Y·Z 변수(글꼴에 없음)')
    if msg: bad += 1; print(f'{n}: ' + ' | '.join(msg))
print('형식 표시', bad, '개'); sys.exit(1 if r1 or bad else 0)
