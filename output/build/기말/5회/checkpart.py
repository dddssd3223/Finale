# -*- coding: utf-8 -*-
"""부품 파일 하나 검사: 중복(dupcheck items) · 말투(stylecheck) · 형식(선지 등차, 상자 위치)
17·18·서답형2는 지침 0-4 관문도 본다: 흔한 패턴(patterns.py) · 독립 검토 기록(<회차>/review/<번호>.json의 핵심 한 줄·d_step).
학교 선례(0-8: 변형 기록·회차 유형·원문 거리·선지)도 본다.
관문 순서: 1 중복·정답·빼 보기 → 2 흔한 패턴 → 3 독립 검토(핵심 한 줄 불통·d_step 0.75 이상) → 4 블라인드 측정 → 5 형식·말투.
3을 통과하기 전에는 측정하지 않는다.
사용: python3 checkpart.py parts/p3.py   (후보 폴더 파일도 됨)"""
import sys, os, re, subprocess, tempfile
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(HERE, '..', '지침')
sys.path.insert(0, '/home/user/Finale/template/db/parts')
from items_common import COND, BOGI
p = os.path.abspath(sys.argv[1])
_rj = os.path.join(os.path.dirname(os.path.dirname(p)), 'round.json')
RT = __import__('json').load(open(_rj)).get('type', '학교형') if os.path.exists(_rj) else '학교형'
os.environ['DUP_ROUND_TYPE'] = RT
if os.path.exists(_rj) and __import__('json').load(open(_rj)).get('db'): os.environ['DUP_DB'] = '1'   # 분석집 중지: 분석집과 같은 문항만 금지
print(f'== 중복 ({RT})'); r1 = subprocess.run([sys.executable, os.path.join(G, 'dupcheck.py'), 'items', p]).returncode
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
    _t = str(it.get('body', '')) + ' '.join(str(v) for _, v in (it.get('cond') or [])) + str(it.get('after', '')) + ' '.join(str(q) for q, _ in (it.get('subs') or []))
    _m = [x.group(0) for x in re.finditer(r'\\\(.*?\\\)|\\\[.*?\\\]', _t, re.S) if '<' in x.group(0) or '>' in x.group(0)]
    if _m: msg.append(f"수식 안 맨 '<'·'>' {len(_m)}곳 → &lt;·&gt;로(HTML 태그로 먹힘, 5회 5번 측정 때 조건이 통째로 빠짐): {_m[0][:40]}")
    if msg: bad += 1; print(f'{n}: ' + ' | '.join(msg))
print('형식 표시', bad, '개')
gate = 0
big = [str(n) for n in list(IT) + list(SI) if str(n) in ('17', '18', 'S2')]
if big:
    print('== 관문 (17·18·서답형2, 지침 0-4)')
    gate = subprocess.run([sys.executable, os.path.join(G, 'patterns.py'), 'check', p]).returncode
    rdir = os.path.join(os.path.dirname(os.path.dirname(p)), 'review')
    for n in big:
        it = IT.get(int(n)) if n.isdigit() else SI.get(n)
        tag = it.get('cand', n) if it else n
        f = os.path.join(rdir, f'{tag}.json')
        if not os.path.exists(f):
            print(f'{n}: 독립 검토 기록 없음 ({os.path.relpath(f, os.path.dirname(rdir))}) → 관문 3 미완, 블라인드 측정 금지'); continue
        R = __import__('json').load(open(f)); ok = []
        if R.get('학교식_예외'):   # 학교식 서답형2(front 0-4·0-0: 0-8 학교 습관이 이김) — 축·d_step 기준 제외, 결정 기록 필수
            print(f"{n}: 관문 3 학교식 예외(검토 판정 {R.get('verdict')}, d_step {R.get('d_step')}) — {str(R.get('결정', ''))[:60]}"); continue
        ax = str(R.get('axis', ''))[:1]; ct = {k: ('불통' if str(v).lstrip().startswith('불통') else ('통' if str(v).lstrip().startswith('통') else '')) for k, v in R.get('core_test', {}).items()}
        if ax == '①' and ct.get('principle') != '불통': ok.append('원리 교체형인데 원문 원리 줄이 통함')
        if ax == '②' and ct.get('setting') != '불통': ok.append('설정 교체형인데 원문 설정 줄이 통함')
        if ax not in ('①', '②'): ok.append(f'축 {ax!r}(①·②만 허용)')
        if float(R.get('d_step', 0)) < 0.75: ok.append(f"d_step {R.get('d_step')} < 0.75")
        if R.get('verdict') != '통과': ok.append(f"검토 판정 {R.get('verdict')}")
        print(f"{n}: 관문 3 {'통과' if not ok else '미통과: ' + ' / '.join(ok)} (검토 {R.get('reviewer', '?')}, 축 {ax}, d_step {R.get('d_step')})")
        gate |= bool(ok)
r_s = subprocess.run([sys.executable, os.path.join(G, 'schoolcheck.py'), 'item', p]).returncode   # 학교 선례(0-8)
sys.exit(1 if r1 or bad or gate or r_s else 0)
