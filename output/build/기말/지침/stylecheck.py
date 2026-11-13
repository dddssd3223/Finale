# -*- coding: utf-8 -*-
"""말투 검사: 문항 문장의 어절을 자료(익스텐션 1,746 + 분석집 433 + 부교재 원문 280 = 2,459문항)의 어절과 대조.
자료에 한 번도 없는 어절을 보고한다(수식은 Ⓜ로 바꿔 비교). 어절 빈도표는 style_vocab.json (원문 없음).

사용
  python3 stylecheck.py build <freq.json>        # 어절 빈도표 갱신 (원문 corpus는 저장소 밖)
  python3 stylecheck.py check <content3.py> ...   # 시험 문항 검사 (RAW, S1/S2 본문·소문항)
"""
import sys, os, re, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
VOC = os.path.join(HERE, 'style_vocab.json')
# 자료에 거의 없거나 시험지에 쓰지 않는 표현 → 자료식 표현 (지침서 '말투' 절과 같은 목록)
REPLACE = {
    '생각하자': "'다음 조건을 만족시키는 ~' / '~라 하자'",
    '속하고': "'k<f(x)<k+c를 만족시키는 실수 x' 또는 '~에 존재한다'",
    '속한다': "'~에 존재한다' / 부등식으로",
    '이하가': "'~ 이하인' 또는 부등식(N≤10)",
    '이상이': "'~ 이상인'",
    '중근': "식으로 제시 f(x)=(x-a)^2(x-b) 등",
    '마다': "'~에 대하여'",
    '정수이고': "'~하도록 하는 정수 ~에 대하여'",
    '도형': "'둘러싸인 부분' ('도형의 넓이'는 '부분의 넓이')",
}

def norm(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\\\[[\s\S]*?\\\]', ' Ⓜ ', t)
    t = re.sub(r'\\\([\s\S]*?\\\)', 'Ⓜ', t)
    return re.sub(r'\s+', ' ', t.replace('&lt;', '<').replace('&gt;', '>')).strip()

def key(w):
    return re.sub(r'^[Ⓜ\(\)\[\]]+', '', w.strip('.,?')).lstrip('Ⓜ')

def build(freq):
    W = json.load(open(freq))['W']
    voc = {}
    for w, c in W.items():
        k = key(w)
        if k: voc[k] = voc.get(k, 0) + c
    json.dump(voc, open(VOC, 'w'), ensure_ascii=False, separators=(',', ':'))
    print('어절', len(voc), '→', VOC)

def check(paths):
    voc = json.load(open(VOC)); bad = 0
    for p in paths:
        d = os.path.dirname(os.path.abspath(p)); sys.path.insert(0, d)
        for mod in ('content3', 'items_common'): sys.modules.pop(mod, None)
        spec = importlib.util.spec_from_file_location('c3', p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        items = [(str(n), r[0]) for n, r in sorted(m.RAW.items())]
        for s in ('S1', 'S2'):
            if hasattr(m, s): items.append((s, getattr(m, s) + ' ' + ' '.join(q[0] for q in getattr(m, s + 'S', []))))
        for n, t in items:
            ws = [key(w) for w in norm(t).split() if re.search('[가-힣]', w)]
            rare = [w for w in ws if w and voc.get(w, 0) == 0]
            hint = [f'{w}→{v}' for w in rare for k2, v in REPLACE.items() if k2 in w]
            if rare:
                bad += 1
                print(f'{os.path.basename(d)} {n:>3}: 자료에 없는 어절 {rare}' + (f'  권장: {"; ".join(hint)}' if hint else ''))
        sys.path.remove(d)
    return bad

if __name__ == '__main__':
    if sys.argv[1] == 'build': build(sys.argv[2])
    else: sys.exit(1 if check(sys.argv[2:]) else 0)
