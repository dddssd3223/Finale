# -*- coding: utf-8 -*-
"""익스텐션(일반·라이브) 1,746문항과 새 문항의 겹침 검사.

저장소에는 문항 원문 대신 해시 지문(ext_fp.json.gz)만 둔다.
- 원문 지문 R: 숫자까지 포함한 6글자 조각
- 골격 지문 K: 숫자를 #로 바꾼 6글자 조각
- 본문 숫자 목록 nums (선지 ① 앞까지)
판정
- 금지(동일 문항): 골격 포함도 >= 0.85 이고 본문 숫자 목록이 같음, 또는 원문 포함도 >= 0.95 → 절대 출제 불가
- 허용(숫자만 다름): 골격 포함도 >= 0.85 이고 숫자 목록이 다름 → 숫자만 바꾼 문항 (사용자 허용)
- 주의(구조 유사): 골격 포함도 0.60~0.85 → 구조가 많이 닮음. 변형 정도 확인
- 금지(구조 변경 미달): 17·18·서답형2가 익스텐션·분석집 어느 문항과든 골격 0.60 이상

사용
  python3 dupcheck.py build <corpus.json> [study.json]   # 지문 만들기 (익스텐션 + 분석집, 원문은 저장소 밖)
  python3 dupcheck.py check <content3.py> [...]    # 시험 RAW 문항 검사
"""
import sys, os, re, json, gzip, base64, zlib, array, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.join(HERE, 'ext_fp.json.gz')
N = 6

def norm(t):
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    t = re.sub(r'\\(?:left|right|displaystyle|textstyle|limits|quad|qquad|,|;|!| )', '', t)
    t = re.sub(r'\\[dt]?frac', 'frac', t)
    t = re.sub(r'\\(le|leq)q?\b', '≤', t); t = re.sub(r'\\(ge|geq)\b', '≥', t)
    t = re.sub(r'\\(?:\(|\)|\[|\])', '', t)
    t = re.sub(r'\\begin\{cases\}|\\end\{cases\}|&|\\\\\[?[0-9a-z]*\]?', ' ', t)
    t = re.sub(r'[{}\s$*]', '', t)
    t = re.sub(r'[①②③④⑤]', '|', t)
    return t

def shingles(s):
    return sorted({zlib.crc32(s[i:i + N].encode()) for i in range(max(1, len(s) - N + 1))})

def skel(s):
    return re.sub(r'\d+', '#', s)

def nums(t):
    b = norm(t).split('|')[0]
    return re.findall(r'\d+(?:\.\d+)?', b)

def pack(v):
    return base64.b64encode(array.array('I', v).tobytes()).decode()

def unpack(b):
    a = array.array('I'); a.frombytes(base64.b64decode(b)); return set(a)

def build(corpus, study=None):
    """corpus: 익스텐션 1,746문항(corpus.json), study: 양정고2 부교재 분석집(study.json, 원문 143 + 변형 290)"""
    C = json.load(open(corpus))
    out = []
    def add(i, key, hdr, text, src):
        r = norm(text)
        out.append(dict(id=i, key=key, hdr=hdr, src=src, R=pack(shingles(r)), K=pack(shingles(skel(r))), nums=nums(text)))
    for o in C:
        add(o['id'], o['key'], o['hdr'], o['problem'], 'EXT')
    if study:
        for s in json.load(open(study)):
            add(f"STUDY-{s['key']}-원문", s['key'], f"분석집 {s['key']} 원문", s['problem'], 'STUDY')
            for v in s['variants']:
                add(f"STUDY-{s['key']}-변형{v['no']}", s['key'], f"분석집 {s['key']} 변형{v['no']}", v['problem'], 'STUDY')
    with gzip.open(FP, 'wt', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print('지문', len(out), '(익스텐션', sum(d['src'] == 'EXT' for d in out), '· 분석집', sum(d['src'] == 'STUDY' for d in out), ') →', FP, os.path.getsize(FP) // 1024, 'KB')

def load():
    with gzip.open(FP, 'rt', encoding='utf-8') as f:
        D = json.load(f)
    for d in D:
        d['R'] = unpack(d['R']); d['K'] = unpack(d['K'])
    return D

def score(text, D, top=3):
    r = norm(text); R = set(shingles(r)); K = set(shingles(skel(r)))
    res = []
    for d in D:
        cr = len(R & d['R']) / max(1, min(len(R), len(d['R'])))
        ck = len(K & d['K']) / max(1, min(len(K), len(d['K'])))
        res.append((ck, cr, d, nums(text) == d['nums']))
    res.sort(key=lambda x: (-x[0], -x[1]))
    return res[:top]

HIGH = {17, 18, 'S2', '17', '18'}   # 구조 변경 필수 자리: 익스텐션·분석집 모두 골격 0.60 미만이어야 함

def verdict(ck, cr, same, no=None, src='EXT', d_id=''):
    """회차 유형(DUP_ROUND_TYPE=학교형|복습형, checkpart가 <회차>/round.json에서 넣음)
    - 익스텐션(일반 GEN·라이브 LIVE 모두): 그대로 가져오지 않음 → 같은 문항 금지. 숫자만 다른 것은 1–16 허용.
      원문 숫자 변경이 아닌 독특한 변형(조건·대상·구조)은 아이디어로 참고해 다시 바꿔 쓴다.
    - 분석집: 같은 문항은 금지. 학교형 회차는 분석집 문항과 구조가 닮은 것(골격 0.60 이상)도 금지(분석집 저격 없음)
    - 17·18·서답형2: 어느 자료든 골격 0.60 미만(구조 변경)"""
    rt = os.environ.get('DUP_ROUND_TYPE', '학교형')
    if no in HIGH and ck >= 0.60: return '금지(구조 변경 미달)'
    same_item = cr >= 0.95 or (ck >= 0.85 and same)
    if src == 'STUDY':
        if same_item: return '금지(분석집 동일 문항)'
        if rt == '학교형' and ck >= 0.60 and not os.environ.get('DUP_DB'): return '금지(학교형: 분석집과 유사)'   # DB 회차(분석집 중지, 2026-11-07)는 같은 문항만 금지
        if ck >= 0.85: return '허용(분석집 숫자만 다름, 복습형)'
        if ck >= 0.60: return '주의(분석집 구조 유사, 복습형)'
        return '통과'
    if same_item: return '금지(라이브 동일 문항)' if str(d_id).startswith('LIVE') else '금지(익스텐션 동일 문항)'
    if ck >= 0.85: return '허용(숫자만 다름)'
    if ck >= 0.60: return '주의(구조 유사)'
    return '통과'

def best(text, D):
    """가장 가까운 익스텐션 1개와 분석집 1개를 따로 판정해 더 나쁜 쪽을 돌려준다"""
    res = score(text, D, 400)
    pick = {}
    for r in res:
        pick.setdefault(r[2].get('src'), r)
    return list(pick.values())

def check(paths):
    D = load(); bad = 0
    for p in paths:
        spec = importlib.util.spec_from_file_location('c3', p); m = importlib.util.module_from_spec(spec)
        sys.path.insert(0, os.path.dirname(os.path.abspath(p))); spec.loader.exec_module(m)
        raw = dict(getattr(m, 'RAW'))
        for s in ('S1', 'S2'):  # 서답형: 본문 + 소문항
            if hasattr(m, s):
                raw[s] = (getattr(m, s) + ''.join(q[0] for q in getattr(m, s + 'S', [])), None)
        for no, v in sorted(raw.items(), key=lambda x: str(x[0])):
            body = v[0] if isinstance(v, (tuple, list)) else str(v)
            ch = v[1] if isinstance(v, (tuple, list)) and isinstance(v[1], list) and v[1] and isinstance(v[1][0], str) else []
            text = body + ''.join('|' + c for c in ch)
            rk = sorted(((verdict(ck, cr, same, no, d.get('src'), d.get('id', '')), ck, cr, d) for ck, cr, d, same in best(text, D)), key=lambda z: (not z[0].startswith('금지'), -z[1]))
            vd, ck, cr, d = rk[0]
            if vd.startswith('금지'): bad += 1
            tag = '분석집' if d.get('src') == 'STUDY' else '익스텐션'
            print(f'{os.path.basename(os.path.dirname(os.path.abspath(p)))} {no:>3}: {vd:12s} 골격 {ck:.2f} 원문 {cr:.2f}  ← [{tag}] {d["id"]} {d["hdr"]}')
    return bad

def check_items(path):
    """출제 중인 부품 파일(ITEMS={번호: dict(body, choices, ...)}, SITEMS={'S1': dict(body, subs=[...])})을 검사"""
    D = load(); bad = 0
    ns = {}; exec(open(path).read(), ns)
    for no, it in list(ns.get('ITEMS', {}).items()) + list(ns.get('SITEMS', {}).items()):
        extra = ''.join(v for _, v in (it.get('cond') or [])) + ''.join(v for _, v in (it.get('bogi') or [])) + (it.get('after') or '')
        text = it['body'] + extra + ''.join(q[0] if isinstance(q, (list, tuple)) else str(q) for q in it.get('subs', [])) + ''.join('|' + str(c) for c in (it.get('choices') or []))
        rk = sorted(((verdict(ck, cr, same, no, d.get('src'), d.get('id', '')), ck, cr, d) for ck, cr, d, same in best(text, D)), key=lambda z: (not z[0].startswith('금지'), -z[1]))
        vd, ck, cr, d = rk[0]
        bad += vd.startswith('금지')
        tag = '분석집' if d.get('src') == 'STUDY' else '익스텐션'
        print(f'{no}: {vd} 골격 {ck:.2f} 원문 {cr:.2f} ← [{tag}] {d["id"]} {d["hdr"]}')
    return bad

if __name__ == '__main__':
    if sys.argv[1] == 'build': build(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif sys.argv[1] == 'items': sys.exit(1 if check_items(sys.argv[2]) else 0)
    else: sys.exit(1 if check(sys.argv[2:]) else 0)
