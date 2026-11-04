# -*- coding: utf-8 -*-
"""블라인드 풀이 측정 분석: 기준 프로필(2학기 중간 20문항)과 앵커 문항으로 풀이자별 눈금을 맞춰, 회차 문항의 체감·시간을 2학기 중간 50분 눈금으로 환산.
사용: python3 measure.py <측정 폴더>   (폴더에 key.json(문항 번호 → [태그, 정답]), 풀이자별 *_strong.md / *_haiku.md / codex_*.md)"""
import sys, os, re, json, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '풀이', '기준프로필')
FILES = {'claude': 'claude_strong.md', 'haiku': 'claude_haiku.md', 'codex': 'codex_strong.md'}

def parse(f):
    R = {}
    for ln in open(f):
        m = re.match(r'\|\s*(\d+)\s*\|([^|]*)\|\s*([\d.]+)[^|]*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|', ln)
        if m: R[int(m[1])] = dict(ans=m[2].strip(), t=float(m[3]), d=float(m[4]), c=float(m[5]))
    return R

def main(d):
    key = {int(k): v for k, v in json.load(open(os.path.join(d, 'key.json'))).items()}
    anchors = {n: int(tag.split('-')[1]) for n, (tag, _) in key.items() if tag.startswith('앵커')}
    out = {}
    for s, fn in FILES.items():
        p = os.path.join(d, fn)
        if not os.path.exists(p): continue
        R, B = parse(p), parse(os.path.join(BASE, fn))
        btot = sum(x['t'] for x in B.values())
        k = sum(B[a]['t'] for a in anchors.values()) / sum(R[n]['t'] for n in anchors)        # 이번 회 시간 → 기준 회 눈금
        off = st.mean(B[a]['d'] for a in anchors.values()) - st.mean(R[n]['d'] for n in anchors)  # 체감 눈금 차
        for n, (tag, ans) in key.items():
            if tag.startswith('앵커') or n not in R: continue
            out.setdefault(tag, {})[s] = dict(t50=R[n]['t'] * k * 50 / btot, d=R[n]['d'] + off, ans=R[n]['ans'])
        print(f'{s}: 앵커 시간 배율 {k:.2f}, 체감 보정 {off:+.2f}')
    prof = json.load(open(os.path.join(BASE, 'profile.json')))['items']
    rows = []
    for tag, v in out.items():
        no = tag.split('-')[1]; n = int(no) if no.isdigit() else {'S1': 19, 'S2': 20}[no]
        t = st.mean(x['t50'] for x in v.values()); dd = st.mean(x['d'] for x in v.values())
        rows.append((n, tag, t, dd, prof[str(n)]['t50'], prof[str(n)]['d']))
    rows.sort()
    print('| 번호 | 체감(측정) | 체감(2학기 중간 같은 번호) | 차 | 시간(50분 환산) | 기준 시간 |')
    print('|---|---|---|---|---|---|')
    for n, tag, t, dd, bt, bd in rows:
        flag = ' ▲' if dd - bd >= 1.5 else (' ▼' if dd - bd <= -1.5 else '')
        print(f'| {tag} | {dd:.1f} | {bd:.1f} | {dd-bd:+.1f}{flag} | {t:.1f} | {bt:.1f} |')
    bands = {'1–4': range(1, 5), '5–8': range(5, 9), '9–12': range(9, 13), '13–16': range(13, 17), '17–18': range(17, 19), '서답': range(19, 21)}
    print('\n| 번호대 | 체감 측정 | 기준 | 시간 측정 | 기준 |'); print('|---|---|---|---|---|')
    tot = 0
    for b, r in bands.items():
        sel = [x for x in rows if x[0] in r]
        if not sel: continue
        tot += sum(x[2] for x in sel)
        print(f'| {b} | {st.mean(x[3] for x in sel):.1f} | {st.mean(x[5] for x in sel):.1f} | {sum(x[2] for x in sel):.1f} | {sum(x[4] for x in sel):.1f} |')
    print(f'\n총 시간(50분 환산): {tot:.1f}분 (기준 50분)')
    json.dump(dict(rows=rows), open(os.path.join(d, 'result.json'), 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1])
