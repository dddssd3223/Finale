# -*- coding: utf-8 -*-
"""N제 md: nje_pool.json(회차표에 안 들어간 DB 변형) → 단원별 N제 md (문제 / 정답·풀이 분리)
사용: python3 nje_md.py [출력 폴더]   (기본 output/N제)
- 단원별 파일 4개(04·05·06·07): DB 스케치(학교식_예상·예상밖·v3_추가·조작_보강·분석집_저격·킬러 설계). 원문 문제를 위에 붙임.
- 분석집_변형 파일 1개: 분석집 본문(db/study_local.json, 저장소에 넣지 않음)이 있으면 그 문제·답. 이 파일은 .gitignore.
- 스케치는 출제 메모라 문장이 시험지처럼 다듬어져 있지 않다. '→' 앞을 문제, 뒤를 풀이로 나눈다."""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '부교재_기말')); import items_final as F
DB = json.load(open(os.path.join(HERE, 'db', 'variation_db.json')))
POOL = json.load(open(os.path.join(HERE, 'nje_pool.json')))
SP = os.path.join(HERE, 'db', 'study_local.json')
STUDY = json.load(open(SP)) if os.path.exists(SP) else {}
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', '..', 'N제')
RWP = os.path.join(HERE, 'db', 'nje_rewrite.json')      # 메모 → 완결 문항으로 다시 쓴 것(id → problem·choices·answer·solution·trap·level 또는 drop)
RW = json.load(open(RWP)) if os.path.exists(RWP) else {}
CIRC = '①②③④⑤'
UNIT = {'D': '04 도함수의 활용(1)', 'M': '05 도함수의 활용(2)', 'I': '06 부정적분과 정적분', 'J': '07 정적분의 활용'}
KIND = {'학교식_예상': '학교식', '예상밖': '예상밖', 'v3_추가': '학교식+', '조작_보강': '계수·조건 바꾸기', '분석집_저격': '분석집 저격', '킬러': '킬러', '결합': '결합 아이디어'}
ORDER = ['학교식_예상', 'v3_추가', '조작_보강', '예상밖', '분석집_저격', '킬러', '결합']
BAND = {'1–4': 1, '5–8': 2, '9–12': 3, '13–16': 4, '17–18': 5, '서답': 4}

def split(sk):
    """'문제 → 풀이' 나누기. 화살표 앞에 '문장. 풀이 시작'이 섞이면 마지막 '. '에서 자름."""
    sk = (sk or '').strip()
    if '→' not in sk: return sk, ''
    q, a = sk.split('→', 1)
    m = list(re.finditer(r'[.。]\s', q))
    if m and len(q) - m[-1].end() < 40 and m[-1].start() > 15: a = q[m[-1].end():] + ' →' + a; q = q[:m[-1].end()]
    return q.strip().rstrip(',;:'), a.strip()

def item(k, ref):
    r = _item(k, ref)
    if r: r['id'] = ref
    return r

def _item(k, ref):
    e = DB[k]; p = ref.split(); kind = p[1]
    if kind == '킬러':
        t = p[2][-1]; d = (e.get('킬러') or {}).get('설계' + t) or {}; kv = ((e.get('킬러') or {}).get('검산') or {}).get('설계' + t) or {}
        fx = kv.get('수정_적용') or {}
        if kv and kv.get('판정') != '통과' and not fx: return None          # 검산 탈락 설계는 뺌
        q = fx.get('문항') or fx.get('수정_문항') or d.get('문항_스케치', '')
        ans = fx.get('확정답') or kv.get('내 답') or ''
        m = re.search(r'\[정답\s*([①-⑤])\]', q); q = re.sub(r'\s*\[정답[^\]]*\]', '', q)
        if m and not ans: ans = m.group(1)
        return dict(kind=kind, band=5, q=q, a=str(ans), note=(f"설계{t}: {d.get('유지_원리') or d.get('설명') or ''}"[:200]).rstrip(': '))
    i = int(p[2]) - 1
    if kind == '분석집_변형': return None
    f = {'학교식_예상': '학교식_예상', '예상밖': '예상밖_포인트', 'v3_추가': 'v3_추가_예상', '결합': '결합_후보', '조작_보강': '조작_보강', '분석집_저격': '분석집_저격'}[kind]
    x = (e.get(f) or [])[i]
    sk = x.get('스케치', '')
    if kind == '결합' and sk.startswith('설계'): return None                 # 킬러 설계와 같은 것
    q, a = split(sk)
    if x.get('답'): a = (a + ' / 답: ' if a else '답: ') + str(x['답'])
    note = x.get('학생이_걸리는_곳') or x.get('지름길_결과') or x.get('오답') or ''
    if kind == '결합': note = x.get('결합', '')
    return dict(kind=kind, band=BAND.get(str(x.get('번호대', '')).replace('형', ''), 3), q=q, a=a, note=str(note)[:260])

def fmt_choice(c):
    c = str(c).strip()
    if '\\(' in c or not re.search(r'[\\^_{}]', c): return c
    return f'\\({c}\\)'

def strip_html(t):
    import html as _h
    t = re.sub(r'<br\s*/?>', '\n', t); t = re.sub(r'<div class="fig">.*?</div>', '[그림]', t, flags=re.S)
    t = re.sub(r'<legend>.*?</legend>', '\n〈보기〉\n', t, flags=re.S); t = re.sub(r'\s*(ㄱ|ㄴ|ㄷ|ㄹ)\.', r'\n\1.', t)
    t = re.sub(r'</?(?:fieldset|div|span|table|tbody|tr|td|th|p|b|i|u|img|sup|sub|center|ol|ul|li)\b[^>]*>', ' ', t)
    return _h.unescape(t.replace('&nbsp;', ' '))

def main():
    os.makedirs(OUT, exist_ok=True)
    stat = collections.Counter(); files = []
    for u, name in UNIT.items():
        Q, A = [], []; n = 0
        keys = sorted([k for k in POOL if k[0] == u], key=lambda k: int(k[1:]))
        for k in keys:
            its = [it for it in (item(k, r) for r in POOL[k]) if it and it['q']]
            if not its: continue
            its.sort(key=lambda it: (it['band'], ORDER.index(it['kind'])))
            Q.append(f"\n## {k} (부교재 {F.D[k][1]}, 원문 난도 {F.D[k][0]})\n\n<details><summary>원문 보기</summary>\n\n{strip_html(F.I[k][0])}\n\n</details>\n")
            A.append(f"\n## {k}\n")
            for it in its:
                rw = RW.get(it['id'])
                if rw and rw.get('drop'): stat['버림'] += 1; continue
                if RW and not rw: continue                      # 다시 쓰기가 있으면 다시 쓴 것만 싣는다
                n += 1; stat[it['kind']] += 1
                if rw:
                    ch = rw.get('choices')
                    chs = ('\n\n' + '　'.join(f"{CIRC[i]} {fmt_choice(c)}" for i, c in enumerate(ch[:5]))) if ch else ''
                    lv = f" · {rw['level']}" if rw.get('level') else ''
                    Q.append(f"**{n}.** `{KIND[it['kind']]}{lv}` {rw['problem']}{chs}\n")
                    A.append(f"**{n}.** **{rw.get('answer', '')}** — {rw.get('solution', '')}" + (f"  \n  └ 주의: {rw['trap']}" if rw.get('trap') else '') + '\n')
                else:
                    Q.append(f"**{n}.** `{KIND[it['kind']]}` {it['q']}\n")
                    A.append(f"**{n}.** {it['a'] or '(풀이 메모 없음 — 원문 풀이 참고)'}" + (f"  \n  └ {('주의' if it['kind'] != '결합' else '장치')}: {it['note']}" if it['note'] else '') + '\n')
        head = (f"# 미적분Ⅰ 2학기 기말 N제 — {name}\n\n모의고사 회차표(1–60회)에 들어가지 않은 변형 {n}문항입니다. 원문마다 쉬운 것(학교식)부터 어려운 것(예상밖·킬러) 순서입니다.\n"
                + ("선지가 없는 문항은 단답형입니다. 정답과 풀이는 파일 맨 아래에 있습니다.\n" if RW else "출제 메모(스케치)를 그대로 옮긴 초안입니다. 정답과 풀이는 파일 맨 아래에 있습니다.\n"))
        fn = os.path.join(OUT, f"미적분1_기말_N제_{name.split()[0]}_{name.split(' ', 1)[1].replace(' ', '')}.md")
        open(fn, 'w').write(head + ''.join(Q) + '\n\n---\n\n# 정답 및 풀이\n' + ''.join(A)); files.append((fn, n))
    # 분석집_변형 (본문은 저장소 밖)
    if STUDY:
        Q, A = [], []; n = 0
        for k in sorted([k for k in POOL], key=lambda k: ('DMIJ'.index(k[0]), int(k[1:]))):
            refs = [r for r in POOL[k] if r.split()[1] == '분석집_변형']
            if not refs: continue
            Q.append(f"\n## {k} ({UNIT[k[0]]})\n"); A.append(f"\n## {k}\n")
            for r in refs:
                sid = (DB[k].get('분석집_변형') or [])[int(r.split()[2]) - 1]['id']; s = STUDY.get(sid)
                if not s: continue
                n += 1; stat['분석집_변형'] += 1
                Q.append(f"**{n}.** {s['problem']}\n"); A.append(f"**{n}.** {s['answer']}\n")
        fn = os.path.join(OUT, '미적분1_기말_N제_분석집변형.md')
        open(fn, 'w').write(f"# 미적분Ⅰ 2학기 기말 N제 — 분석집 변형\n\n분석집에 실린 변형 가운데 모의고사에 들어가지 않은 {n}문항입니다(개인 학습용, 공유 금지).\n" + ''.join(Q) + '\n\n---\n\n# 정답 및 풀이\n' + ''.join(A)); files.append((fn, n))
        open(os.path.join(OUT, '.gitignore'), 'w').write('미적분1_기말_N제_분석집변형.md\n')
    for fn, n in files: print(n, os.path.relpath(fn))
    print(dict(stat))

if __name__ == '__main__':
    main()
