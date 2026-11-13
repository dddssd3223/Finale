# -*- coding: utf-8 -*-
"""문제 글 블라인드 감별용 (front.md 0-9). 회차 문항을 실제 시험 받아쓰기와 같은 표기로 뽑고, 모든 글을 같은 꼴로 맞춘다.
사용: python3 blind_text.py round <회차 폴더> > ours.md      # 회차 20문항 → '## 문항 N' 꼴
      python3 blind_text.py norm <problems.md>               # 받아쓴 글·회차 글을 같은 꼴로(그림 → [그림], 선지 숫자 괄호 빼기)
실제 시험 받아쓰기(학교 시험 원문)는 저작권 자료라 저장소 밖(스크래치패드 tr/)에 둔다."""
import re, sys, os, html, importlib.util

TAG = r'</?(?:div|span|fieldset|legend|img|br|b|i|u|sup|sub|p)\b[^>]*>'

def _conv(body, pt):
    b = body.replace('⏎', '')
    b = re.sub(r'\{PTR\}|\{PT\}', f' [{pt:.1f}점]', b)
    b = re.sub(r'<div class="fig">.*?</div>', ' [그림] ', b, flags=re.S)
    def cond(m):
        items = re.findall(r'<span class="ck">([^<]*)</span>(.*?)</div>', m.group(0), flags=re.S)
        return ' [조건] ' + (' '.join(f'{k} {v}' for k, v in items) if items else re.sub(TAG, ' ', m.group(0))) + ' '
    b = re.sub(r'<div class="cond"[^>]*>.*?</div>\s*</div>', cond, b, flags=re.S)
    def bogi(m):
        items = re.findall(r'<span class="bk">([^<]*)</span><span>(.*?)</span></div>', m.group(0), flags=re.S)
        return ' [보기] ' + ' '.join(f'{k} {v}' for k, v in items) + ' '
    b = re.sub(r'<fieldset class="bogi">.*?</fieldset>', bogi, b, flags=re.S)
    b = html.unescape(re.sub(TAG, ' ', b)).replace('\n', ' ')
    return re.sub(r'  +', ' ', b).strip()

def round_text(rdir):
    sys.path.insert(0, rdir); cwd = os.getcwd(); os.chdir(rdir)
    try:
        spec = importlib.util.spec_from_file_location('c3', os.path.join(rdir, 'content3.py')); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
    finally: os.chdir(cwd)
    out = []
    for n in range(1, 19):
        pt, body, ch = C.Q[n]; t = _conv(body, pt)
        if '점]' not in t: t += f' [{pt:.1f}점]'
        chs = ' '.join(f'{"①②③④⑤"[i]} ' + (c[2:] if c.startswith('T:') else f'\\({c}\\)') for i, c in enumerate(ch))
        out += [f'## 문항 {n}', t + '  ' + chs, '']
    for k, (body, subs) in [(19, (C.S1, C.S1S)), (20, (C.S2, C.S2S))]:
        t = _conv(body, 0).replace(' [0.0점]', '') + ' ' + ' '.join(f'({i}) {q} [{p}]' for i, (q, p) in enumerate(subs, 1))
        out += [f'## 문항 {k}', f'<서답형 {k - 18}> ' + t, '']
    return '\n'.join(out)

def norm(s):
    s = re.sub(r'\[그림[^\]]*\]', '[그림]', s).replace('\\underline', '')
    out = []
    for block in re.split(r'(?m)^## 문항 ', s)[1:]:
        n, _, body = block.partition('\n')
        body = ' '.join(l.strip() for l in body.strip().splitlines() if l.strip())
        i = body.find('①')
        if i >= 0:
            body = body[:i].rstrip() + '  ' + re.sub(r'\\\(\s*(-?\d+)\s*\\\)', r'\1', body[i:])
        out.append(f'## 문항 {n.strip()}\n{re.sub(r"\s{3,}", "  ", body)}\n')
    return '\n'.join(out)

if __name__ == '__main__':
    if sys.argv[1] == 'round': print(round_text(os.path.abspath(sys.argv[2])))
    elif sys.argv[1] == 'norm': print(norm(open(sys.argv[2]).read()), end='')
