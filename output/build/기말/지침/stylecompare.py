# -*- coding: utf-8 -*-
"""출제자별 문장 스타일 비교: 학교(2학기 중간 선택형 18문항) 기준치와 회차 문항을 출제자(author 필드: claude/codex)별로 비교.

사용
  python3 stylecompare.py build <format.json>          # 학교 기준치 school_style.json 만들기 (원문은 저장소 밖, 수치·어절 빈도만 저장)
  python3 stylecompare.py check <회차 폴더> [...]      # 출제자별 지표 표 (마크다운) 출력, --json 으로 JSON
지표: 문항당 문장 수, 본문 글자 수(수식은 Ⓜ 한 글자), 수식 비율, 조건 상자 비율, 질문→상자 비율, 학교 어절 겹침률, 출제자 특유 어절(학교 대비)"""
import sys, os, re, json, math, runpy, collections
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'school_style.json')
sys.path.insert(0, '/home/user/Finale/template/db/parts')

def strip(t):
    t = re.sub(r'\[(?:그림|상자|라벨 없는 상자)[^\]]*\]', ' ', t)
    t = re.sub(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)', 'Ⓜ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\[[0-9.]+점\]', ' ', t)
    t = re.split(r'①', t)[0]
    return re.sub(r'\s+', ' ', t).strip()

def mathlen(t):
    return sum(len(m) for m in re.findall(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)', t))

def eoj(t):
    return [w.strip('.,?()') for w in strip(t).split() if re.search(r'[가-힣]', w)]

def metrics(items):
    """items: [(text, has_box, q_before_box)]"""
    n = len(items) or 1
    sent = [len([s for s in re.split(r'(?<=[.?])\s', strip(t)) if s.strip()]) for t, _, _ in items]
    chars = [len(strip(t)) for t, _, _ in items]
    mr = [mathlen(t) / max(1, len(re.sub(r'<[^>]+>', '', t))) for t, _, _ in items]
    box = [b for _, b, _ in items]; qb = [q for _, b, q in items if b]
    return dict(n=len(items), sent=sum(sent) / n, chars=sum(chars) / n, math=sum(mr) / n,
                box=sum(box) / n, q_before=(sum(qb) / len(qb)) if qb else None)

def build(fmt):
    d = json.load(open(fmt)); items = []; voc = collections.Counter()
    for it in d['items']:
        t = it['exam_text']
        if '①' not in t: continue
        hasbox = '[상자' in t or '[라벨 없는 상자' in t
        qb = hasbox and t.find('?') < t.find('[상자') if '[상자' in t else (hasbox and t.find('?') < t.find('[라벨'))
        items.append((t, hasbox, bool(qb))); voc.update(eoj(t))
    json.dump(dict(source='양정고 2학기 중간 선택형 18문항(전사본은 저장소 밖)', metrics=metrics(items), vocab=voc), open(OUT, 'w'), ensure_ascii=False, indent=1)
    print('saved', OUT, metrics(items))

def load_round(d):
    from items_common import COND, BOGI
    ns = runpy.run_path(os.path.join(d, 'content3.py')); out = collections.defaultdict(list)
    for n, it in ns['ITEMS'].items():
        b = it['body'] + ' ' + (it.get('after') or '')   # 상자·보기 내용은 빼고 본문만 (학교 기준치와 같게)
        b = re.sub(r'<div class="fig">.*?</div>', ' ', b)
        hasbox = bool(it.get('cond'))
        out[it.get('author', 'claude')].append((b, hasbox, hasbox and '?' in re.sub(r'<[^>]+>', '', it['body'])))
    return out

def check(dirs, as_json=False):
    S = json.load(open(OUT)); sv = collections.Counter(S['vocab']); stot = sum(sv.values())
    groups = collections.defaultdict(list)
    for d in dirs:
        for a, its in load_round(os.path.abspath(d)).items(): groups[a] += its
    rows = {'학교(2학기 중간)': S['metrics']}; special = {}
    for a, its in groups.items():
        m = metrics(its); v = collections.Counter(w for t, _, _ in its for w in eoj(t)); tot = sum(v.values()) or 1
        m['school_overlap'] = sum(c for w, c in v.items() if w in sv) / tot
        # 학교 대비 특유 어절 (로그 오즈, 가법 평활)
        lo = {w: math.log((c + .5) / (tot + .5)) - math.log((sv.get(w, 0) + .5) / (stot + .5)) for w, c in v.items() if c >= 2}
        special[a] = [w for w, _ in sorted(lo.items(), key=lambda x: -x[1])[:12]]
        rows[a] = m
    if as_json: print(json.dumps(dict(rows=rows, special=special), ensure_ascii=False, indent=1)); return
    f = lambda x, p=2: '—' if x is None else (f'{x:.{p}f}' if isinstance(x, float) else str(x))
    print('| 출제자 | 문항 | 문장 수 | 본문 글자 | 수식 비율 | 상자 비율 | 질문→상자 | 학교 어절 겹침 |')
    print('|---|---|---|---|---|---|---|---|')
    for a, m in rows.items():
        print(f"| {a} | {m['n']} | {f(m['sent'],1)} | {f(m['chars'],0)} | {f(m['math'])} | {f(m['box'])} | {f(m['q_before'])} | {f(m.get('school_overlap'))} |")
    for a, ws in special.items(): print(f'\n{a} 특유 어절(학교 대비): ' + ', '.join(ws))

if __name__ == '__main__':
    if sys.argv[1] == 'build': build(sys.argv[2])
    else: check([x for x in sys.argv[2:] if not x.startswith('--')], '--json' in sys.argv)
