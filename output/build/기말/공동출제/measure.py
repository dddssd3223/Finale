# -*- coding: utf-8 -*-
"""블라인드 풀이 측정 분석: 기준 프로필(2학기 중간 20문항)과 앵커 문항으로 풀이자별 눈금을 맞춰, 회차 문항의 체감·시간을 2학기 중간 50분 눈금으로 환산.
사용: python3 measure.py <측정 폴더>        (폴더에 key.json(문항 번호 → [태그, 정답]), 풀이자별 claude_strong.md / claude_haiku.md / codex_strong.md, 선택: claude_study.md, meta.json)
      python3 measure.py stale <회차 폴더>   (측정한 뒤에 고친 문항 찾기: 측정 폴더 meta.json의 문항 해시와 지금 문항 비교)
눈금 맞추기:
  - 시간: 앵커 시간 합의 비(기준/이번). 앵커별 비의 흩어짐을 '시간 눈금 ±%'로 적는다.
  - 체감: 앵커 6개 이상이면 직선 맞춤(기준 = a + b·이번, b는 0.6–1.6로 제한), 그보다 적으면 평균 차만 더한다. 앵커 잔차의 표준편차를 '체감 ±'로 적는다.
  - claude_study.md(분석집을 공부한 강한 풀이자)는 평균에 넣지 않고, 같은 폴더의 블라인드 강한 풀이자와 시간·체감 차를 분석집 문항/일반 문항으로 나눠 본다(복습 효과).
측정 결과는 result.json에 쓰고, 풀이/측정기록.jsonl에 회차별로 쌓는다(같은 폴더는 덮어씀)."""
import sys, os, re, json, math, glob, datetime, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
PUL = os.path.join(HERE, '풀이')
BASE = os.path.join(PUL, '기준프로필')          # 기본: 2026 2학기 중간. meta.json의 "base"로 바꿀 수 있다(기말: 기준프로필_기말)
FILES = {'claude': 'claude_strong.md', 'haiku': 'claude_haiku.md', 'codex': 'codex_strong.md'}
STUDY = ('study', 'claude_study.md', 'claude_strong.md')      # (이름, 파일, 눈금을 맞출 기준 파일)
LEDGER = os.path.join(PUL, '측정기록.jsonl')
CIRC = '①②③④⑤'

def parse(f):
    R = {}
    for ln in open(f):
        m = re.match(r'\|\s*(\d+)\s*\|([^|]*)\|\s*([\d.]+)[^|]*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|([^|]*)', ln)
        if m: R[int(m[1])] = dict(ans=m[2].strip(), t=float(m[3]), d=float(m[4]), c=float(m[5]), note=m[6].strip())
    return R

def calib(R, B, anchors):
    """anchors: {이번 번호: 기준 번호}. 반환: (시간 배율 k, 체감 함수, 정보)"""
    pairs = [(R[n], B[a]) for n, a in anchors.items() if n in R and a in B]
    k = sum(b['t'] for _, b in pairs) / sum(r['t'] for r, _ in pairs)
    lr = [math.log(b['t'] / r['t']) for r, b in pairs if r['t'] > 0]
    t_sd = st.pstdev(lr) if len(lr) > 1 else 0.0
    xs = [r['d'] for r, _ in pairs]; ys = [b['d'] for _, b in pairs]
    if len(pairs) >= 6 and st.pvariance(xs) > 0:
        bb = sum((x - st.mean(xs)) * (y - st.mean(ys)) for x, y in zip(xs, ys)) / sum((x - st.mean(xs)) ** 2 for x in xs)
        bb = min(1.6, max(0.6, bb)); aa = st.mean(ys) - bb * st.mean(xs); mode = '직선'
    else:
        bb = 1.0; aa = st.mean(ys) - st.mean(xs); mode = '평균 차'
    res = [y - (aa + bb * x) for x, y in zip(xs, ys)]
    d_sd = math.sqrt(sum(e * e for e in res) / max(1, len(res) - (2 if mode == '직선' else 1)))
    return k, (lambda d: aa + bb * d), dict(k=round(k, 3), a=round(aa, 2), b=round(bb, 2), mode=mode, t_sd=round(t_sd, 3), d_sd=round(d_sd, 2), n=len(pairs))

def ans_ok(got, want):
    if isinstance(want, int): want = CIRC[want - 1]
    want = str(want).strip()
    if want[:1] in CIRC: return got.strip()[:1] == want[:1]
    return None                                                    # 서답형: 사람이 본다

def main(d):
    key = {int(k): v for k, v in json.load(open(os.path.join(d, 'key.json'))).items()}
    meta = json.load(open(os.path.join(d, 'meta.json'))) if os.path.exists(os.path.join(d, 'meta.json')) else {}
    anchors = {n: int(tag.split('-')[1]) for n, (tag, _) in key.items() if tag.startswith('앵커')}
    base = os.path.join(PUL, meta.get('base', '기준프로필'))
    print(f"기준: {os.path.basename(base)}")
    out, info, per = {}, {}, {}
    solvers = [(s, fn, fn) for s, fn in FILES.items()] + [STUDY]
    for s, fn, bfn in solvers:
        p = os.path.join(d, fn)
        if not os.path.exists(p) or not os.path.exists(os.path.join(base, bfn)): continue
        R, B = parse(p), parse(os.path.join(base, bfn))
        btot = sum(x['t'] for x in B.values())
        k, fd, inf = calib(R, B, anchors); info[s] = inf
        wrong = [f'{n}({key[n][0]})' for n in key if n in R and ans_ok(R[n]['ans'], key[n][1]) is False]
        for n, (tag, ans) in key.items():
            if tag.startswith('앵커') or n not in R: continue
            per.setdefault(s, {})[tag] = dict(t50=R[n]['t'] * k * 50 / btot, d=fd(R[n]['d']), ans=R[n]['ans'], study_note=R[n]['note'].startswith('[분석집]'))
            if s != 'study': out.setdefault(tag, {})[s] = per[s][tag]
        print(f"{s}: 앵커 {inf['n']}개, 시간 배율 {k:.2f} (앵커별 흩어짐 ±{inf['t_sd'] * 100:.0f}%), 체감 {inf['mode']} {inf['a']:+.2f}+{inf['b']:.2f}×이번 (±{inf['d_sd']:.1f})"
              + (f", 오답 {', '.join(wrong)}" if wrong else ', 오답 없음'))
    prof = json.load(open(os.path.join(base, 'profile.json')))['items']
    rows = []
    for tag, v in out.items():
        no = tag.split('-')[1]; n = int(no) if no.isdigit() else {'S1': 19, 'S2': 20}[no]
        t = st.mean(x['t50'] for x in v.values()); dd = st.mean(x['d'] for x in v.values())
        rows.append((n, tag, t, dd, prof[str(n)]['t50'], prof[str(n)]['d']))
    rows.sort()
    dsd = st.mean(i['d_sd'] for s, i in info.items() if s != 'study') if info else 0
    print(f'| 번호 | 체감(측정, ±{dsd:.1f}) | 체감(2학기 중간 같은 번호) | 차 | 시간(50분 환산) | 기준 시간 |')
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
    study = None
    if 'study' in per and 'claude' in per:
        items = meta.get('items', {}); study = []
        print('\n복습 효과 (분석집 공부한 강한 풀이자 − 블라인드 강한 풀이자, 같은 앵커 눈금)')
        print('| 문항 | 분석집 방향 | 시간 차(분) | 체감 차 | 공부자 표시 |'); print('|---|---|---|---|---|')
        for tag in sorted(per['study'], key=lambda t: (len(t), t)):
            if tag not in per['claude']: continue
            a, b = per['study'][tag], per['claude'][tag]; bs = items.get(tag, {}).get('bunseok')
            study.append(dict(tag=tag, bunseok=bs, dt=a['t50'] - b['t50'], dd=a['d'] - b['d'], mark=a['study_note']))
            print(f"| {tag} | {'O' if bs else '-'} | {a['t50'] - b['t50']:+.1f} | {a['d'] - b['d']:+.1f} | {'[분석집]' if a['study_note'] else ''} |")
        for lab, f in (('분석집 방향 문항', True), ('일반 문항', False)):
            g = [x for x in study if bool(x['bunseok']) == f]
            if g: print(f"{lab} {len(g)}개: 시간 차 평균 {st.mean(x['dt'] for x in g):+.2f}분, 체감 차 평균 {st.mean(x['dd'] for x in g):+.2f}, [분석집] 표시 {sum(x['mark'] for x in g)}개")
        # 복습형 측정 판정(front.md 0-8): 분석집 문항은 공부한 풀이자 ±1.5, 공부 효과 −0.5분 이상, 블라인드 +2.5 이하
        pr = {r[1]: r for r in rows}
        print('\n복습형 판정 (분석집 문항) | 문항 | 공부자 체감−학교 | 블라인드 평균−학교 | 공부 효과(분) | 판정 |')
        for x in study:
            if not x['bunseok'] or x['tag'] not in pr: continue
            n, tag, t, dd, bt, bd = pr[x['tag']]; sd = per['study'][tag]['d'] - bd
            ok = abs(sd) <= 1.5 and x['dt'] <= -0.5 and dd - bd <= 2.5
            print(f"| {tag} | {sd:+.1f} | {dd - bd:+.1f} | {x['dt']:+.1f} | {'통과' if ok else '걸림'} |")
        mix = sum((per['study'][r[1]]['t50'] if items.get(r[1], {}).get('bunseok') and r[1] in per['study'] else r[2]) for r in rows)
        print(f'이 폴더 시간 합(분석집 문항은 공부자 시간): {mix:.1f}분 (블라인드만 {tot:.1f}분)')
    json.dump(dict(rows=rows, calib=info, study=study), open(os.path.join(d, 'result.json'), 'w'), ensure_ascii=False, indent=1)
    ledger(d, rows, info, meta)

def ledger(d, rows, info, meta):
    name = os.path.basename(os.path.normpath(d))
    L = [json.loads(x) for x in open(LEDGER)] if os.path.exists(LEDGER) else []
    L = [x for x in L if x['folder'] != name]
    L.append(dict(folder=name, round=meta.get('round') or re.sub(r'^측정_|[a-z_]*$', '', name), date=datetime.date.today().isoformat(),
                  anchors=sorted(meta.get('anchors', [])), calib=info, rows=[dict(tag=t, d=round(dd, 2), t50=round(tt, 2)) for _, t, tt, dd, _, _ in rows]))
    open(LEDGER, 'w').write(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in L))

def stale(rdir):
    sys.path.insert(0, HERE); import measure_gen as G
    rdir = os.path.abspath(rdir); rname = os.path.basename(rdir.rstrip('/')); P = G.load_round(rdir)
    seen = {}
    for f in sorted(glob.glob(os.path.join(PUL, f'측정_{rname}*', 'meta.json'))):
        for tag, m in json.load(open(f)).get('items', {}).items(): seen.setdefault(tag, {})[m['hash']] = os.path.basename(os.path.dirname(f))
    bad = []
    for t, it in sorted(P.items(), key=lambda z: (not z[0].isdigit(), int(z[0]) if z[0].isdigit() else 0, z[0])):
        tag = f'{rname}-{t}'; h = G.item_hash(it)
        if h in seen.get(tag, {}): continue
        moved = [tg for tg, hs in seen.items() if h in hs]   # 자리만 옮긴 문항(측정 뒤 번호 바꾸기)은 내용이 같으면 통과
        if moved: print(f'{tag}: 측정 뒤 자리 옮김({moved[0]} → {tag}), 내용 같음'); continue
        bad.append(t); print(f"{tag}: {'측정 뒤 고침 (마지막 측정 ' + sorted(seen[tag].values())[-1] + ')' if tag in seen else '해시 기록 없음(이전 방식 측정 또는 미측정)'}")
    print(f'다시 잴 문항: {",".join(bad) if bad else "없음"}')
    return bad

if __name__ == '__main__':
    if sys.argv[1] == 'stale': sys.exit(1 if stale(sys.argv[2]) else 0)
    main(sys.argv[1])
