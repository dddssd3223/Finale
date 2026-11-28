# -*- coding: utf-8 -*-
"""형식 검사(지침서 0-7): 선지 등차 배열, 조건 상자와 질문 위치, 상자 뒤 추가 문장.
사용: python3 fmtcheck.py <회차 폴더>   (content3.py의 Q = {번호: (배점, 본문 HTML, 선지)} 사용)"""
import sys, os, re, runpy
from fractions import Fraction

def val(c):
    c = re.sub(r'\\displaystyle|\s', '', c).strip('$')
    m = re.fullmatch(r'(-?)\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', c)
    if m: return Fraction(int(m[2]), int(m[3])) * (-1 if m[1] else 1)
    m = re.fullmatch(r'(-?)(\d+)\\[dt]?frac\{?(\d+)\}?\{?(\d+)\}?', c)   # 대분수 꼴은 쓰지 않으므로 None
    if m: return None
    return Fraction(int(c)) if re.fullmatch(r'-?\d+', c) else None

def text(h): return re.sub(r'<[^>]+>', '', h)

def check(d):
    d = os.path.abspath(d); cwd = os.getcwd(); os.chdir(d); sys.path.insert(0, d)
    try: Q = runpy.run_path(os.path.join(d, 'content3.py'))['Q']
    finally: os.chdir(cwd)
    bad = 0
    for n in sorted(Q):
        _, body, ch = Q[n]; msg = []
        v = [val(c) for c in ch] if ch and not str(ch[0]).startswith('T:') else None
        if v and None not in v:
            ds = {v[i + 1] - v[i] for i in range(4)}
            if len(ds) != 1: msg.append('선지 비등차 (' + ' / '.join(ch) + ')')
        elif v: msg.append('선지 수 아님(확인)')
        i = body.find('<div class="cond"')
        if i >= 0:
            before, after = body[:i], body[i:]
            j = after.find('</div></div>') if False else None
            if '?' not in text(before):
                tail = text(re.sub(r'<div class="cond"[\s\S]*?</div>\s*</div>', '', after, count=1))
                sent = [x for x in re.split(r'(?<=[.?])\s', re.sub(r'\\\([\s\S]*?\\\)', 'Ⓜ', tail).strip()) if x.strip()]
                msg.append('상자→질문형' + (f' · 상자 뒤 {len(sent)}문장(질문 한 줄만 권장)' if len(sent) > 1 else ''))
        if msg:
            bad += 1; print(f'{n:>2}번: ' + ' | '.join(msg))
    print(f'— {len(Q)}문항 중 표시 {bad}개 (기준: 학교 선지 18/18 등차, 상자 문항 5개 중 질문→상자 4)')

if __name__ == '__main__':
    for d in sys.argv[1:]: print('['+os.path.basename(os.path.abspath(d))+']'); check(d)
