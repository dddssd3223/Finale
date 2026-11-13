# -*- coding: utf-8 -*-
"""블라인드 측정 세트 만들기: 회차 문항 + 학교 앵커(2학기 중간) 8개를 섞어 풀이자용 폴더를 만든다.
사용: python3 measure_gen.py <회차 폴더> <출력 폴더> <문항 목록> [--anchors 3,6,8,10,12,15,17,18] [--school <학교 20문항 폴더>] [--study <분석집 md 폴더>] [--noise 12]
  문항 목록: 1,3,5,S1 처럼 쉼표로. 출력 폴더에 problems.md · key.json · meta.json(문항 해시·분석집 여부) · TASK.md · 그림 png.
  --study를 주면 study.md(분석집 공부 노트: 회차 원문 중 분석집에 있는 카드 + 관계없는 카드 noise개, 섞음)와 TASK_study.md도 만든다.
  학교 20문항(problems.md, fig_17.png)과 분석집 원문은 저작권 자료라 저장소 밖(스크래치패드)에 둔다. 출력 폴더도 저장소 밖에 만든다.
측정 뒤 문항을 고쳤는지: python3 measure.py stale <회차 폴더> 가 meta.json 해시로 확인한다."""
import os, re, sys, json, random, hashlib, importlib.util, shutil, argparse

def load_round(rdir):
    sys.path.insert(0, rdir)
    spec = importlib.util.spec_from_file_location('content3_' + os.path.basename(rdir), os.path.join(rdir, 'content3.py'))
    m = importlib.util.module_from_spec(spec); cwd = os.getcwd(); os.chdir(rdir)
    try: spec.loader.exec_module(m)
    finally: os.chdir(cwd)
    P = {str(k): v for k, v in m.ITEMS.items()}; P.update({str(k): v for k, v in m.SITEMS.items()})
    return P

def txt(it):
    b = it['body']
    if it.get('cond'): b += '\n[조건] ' + ' '.join(f'({k}) {v}' if k else v for k, v in it['cond']) + ' '
    if it.get('bogi'): b += '\n[보기] ' + ' '.join(f'{k}. {v}' for k, v in it['bogi']) + ' '   # 보기형(2026-11-07 3회 측정에서 빠져 있던 것)
    if it.get('after'): b += it['after']
    b = re.sub(r'<div class="fig"><img src="([^"]+?)(\.svg)?"[^>]*></div>', lambda m: f' [그림: {os.path.basename(m[1])}.png] ', b)
    b = re.sub(r'\\\(.*?\\\)|\\\[.*?\\\]', lambda m: m.group(0).replace('<', '&lt;').replace('>', '&gt;'), b, flags=re.S)   # 수식 안 맨 '<'가 태그로 지워지지 않게(5회 5번: '-2<x_1<x_2<-1'이 통째로 빠짐)
    b = re.sub(r'<[^>]+>', ' ', b).replace('&lt;', '<').replace('&gt;', '>').replace('\n', ' ')
    if it.get('subs'): b += ' ' + ' '.join(f'({i}) {q[0]}' for i, q in enumerate(it['subs'], 1)) + ' [서답형: 각 소문항 답을 적는다]'
    if it.get('choices'): b += '  ' + ' '.join(f'{"①②③④⑤"[i]} {str(c).removeprefix("T:")}' for i, c in enumerate(it['choices']))
    return re.sub(r'  +', ' ', b).strip()

def item_hash(it):
    return hashlib.sha1(json.dumps([txt(it), str(it.get('ans'))], ensure_ascii=False).encode()).hexdigest()[:12]

def figs_of(it): return re.findall(r'<img src="([^"]+)"', it['body'] + str(it.get('after', '')))

def svg2png(svg, png):
    import pymupdf
    doc = pymupdf.open(svg); pdf = pymupdf.open('pdf', doc.convert_to_pdf())
    pdf[0].get_pixmap(dpi=200).save(png)

def school_items(sdir):
    t = open(os.path.join(sdir, 'problems.md')).read()
    bl = re.split(r'\n## 문항 (\d+)\n', t)
    S = {int(bl[i]): re.sub(r'\s*\[\d\.\d점\]', '', bl[i + 1].strip()) for i in range(1, len(bl), 2)}
    return {n: s.replace('fig_17.png', 'fig_A17.png').replace('fig_1.png', 'fig_A1.png') for n, s in S.items()}

SCHOOL_ANS = {1: '② -1', 2: '④ 4', 3: '① 7/2', 4: '② 13', 5: '③ 7/5', 6: '② (0,1)', 7: '④ 2', 8: '③ 1', 9: '④ 5', 10: '⑤ -20', 11: '① 1',
              12: '⑤ 6', 13: '⑤ 20', 14: '④ 1/5', 15: '② 20', 16: '③ 61', 17: '① 4', 18: '④ 30'}

def study_cards(sdir):
    C = {}
    for f in sorted(os.listdir(sdir)):
        if not f.endswith('.md'): continue
        t = open(os.path.join(sdir, f)).read()
        for m in re.finditer(r'\n## (0[4-7])-(\d+)\. (.*?)\n(.*?)(?=\n## 0[4-7]-\d+\.|\n# PART|\Z)', t, re.S):
            key = {'04': 'D', '05': 'M', '06': 'I', '07': 'J'}[m[1]] + m[2]
            C[key] = f'## {m[3]}\n{m[4].strip()}'
    return C

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rdir'); ap.add_argument('out'); ap.add_argument('items')
    ap.add_argument('--anchors', default='3,6,8,10,12,15,17,18')
    ap.add_argument('--school', default='/tmp/claude-0/-home-user/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/base')
    ap.add_argument('--study'); ap.add_argument('--noise', type=int, default=12); ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--base', default='기준프로필', help="기준 프로필 폴더 이름(풀이/ 아래). 기말 범위는 기준프로필_기말 + --school <작년 기말 폴더> --anchors 3,7,10,12,14,16,17,18")
    a = ap.parse_args()
    rdir = os.path.abspath(a.rdir); rname = os.path.basename(rdir.rstrip('/'))
    os.makedirs(a.out, exist_ok=True); P = load_round(rdir); S = school_items(a.school)
    ap_ = os.path.join(a.school, 'answers.json')                       # 앵커 정답: 학교 폴더에 answers.json이 있으면 그것(작년 기말 등)
    if os.path.exists(ap_): SCHOOL_ANS.clear(); SCHOOL_ANS.update({int(k): v for k, v in json.load(open(ap_)).items()})
    items = a.items.split(','); anchors = [int(x) for x in a.anchors.split(',') if x]
    rnd = random.Random(a.seed)
    # 앵커를 번호대가 흩어지게 끼운다: 회차 문항 순서는 유지, 앵커는 고르게 섞음
    seq = [('item', t) for t in items]
    for i, an in enumerate(anchors):
        pos = round((i + 0.5) * (len(seq) + 1) / len(anchors)); seq.insert(min(pos, len(seq)), ('anchor', an))
    out = [f'# 풀이 실험 문항 {len(seq)}개 (고2 미적분Ⅰ)\n']; key, meta, figs = {}, {}, set()
    for i, (kind, t) in enumerate(seq, 1):
        if kind == 'anchor':
            out.append(f'## 문항 {i}\n{S[t]}\n'); key[str(i)] = [f'앵커-{t}', SCHOOL_ANS[t]]
            if t == 17 and os.path.exists(os.path.join(a.school, 'fig_17.png')): figs.add(('school', 'fig_17.png', 'fig_A17.png'))
            if t == 1 and os.path.exists(os.path.join(a.school, 'fig_1.png')): figs.add(('school', 'fig_1.png', 'fig_A1.png'))
        else:
            it = P[t]; out.append(f'## 문항 {i}\n{txt(it)}\n')
            ans = it['ans'] if 'subs' not in it else ' / '.join(map(str, it['ans']))
            key[str(i)] = [f'{rname}-{t}', ans]
            meta[f'{rname}-{t}'] = dict(hash=item_hash(it), bunseok=str(it.get('bunseok')) == 'True', key=it.get('key'))
            for f in figs_of(it): figs.add(('round', f, os.path.basename(re.sub(r'\.svg$', '', f)) + '.png'))
    for src, f, dst in figs:
        if src == 'school': shutil.copy(os.path.join(a.school, f), os.path.join(a.out, dst))
        else:
            p = next((os.path.join(rdir, d, f) for d in ('parts', '후보', 'figs', '.') if os.path.exists(os.path.join(rdir, d, f))), None)
            if p is None: sys.exit(f'그림 없음: {f}')
            svg2png(p, os.path.join(a.out, dst)) if p.endswith('.svg') else shutil.copy(p, os.path.join(a.out, dst))
    open(os.path.join(a.out, 'problems.md'), 'w').write('\n'.join(out))
    json.dump(key, open(os.path.join(a.out, 'key.json'), 'w'), ensure_ascii=False)
    json.dump(dict(round=rname, base=a.base, anchors=anchors, items=meta), open(os.path.join(a.out, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
    fl = ', '.join(sorted(d for *_, d in figs)) or '없음'
    N = len(seq)
    task = (f'당신은 고2 미적분Ⅰ 학생이 시험장에서 푸는 것처럼 문제를 푸는 풀이자다. 이 실험은 문항별 난도와 풀이 시간을 재는 것이다. '
            f'이 폴더의 `problems.md`(문항 1–{N})와 그림 파일({fl})만 쓰고, 다른 파일은 찾거나 열지 않는다.\n\n'
            '- 코드 실행·계산기는 쓰지 않는다. 파일을 읽고 쓰는 것만 하고, 손으로 푸는 것처럼 추론만으로 푼다.\n'
            f'- {N}문항을 1번부터 차례로 풀면서, 각 문항에 실제 시험장에서 들일 시간을 상위권 학생 기준으로 어림한다.\n\n'
            '문항마다 아래 표의 한 줄을 채운다.\n\n| 번호 | 답 | 예상 시간(분) | 체감 난도(1–10) | 확신도(%) | 막힌 곳·함정(한 줄) |\n\n'
            '체감 난도 눈금: 1 = 교과서 예제, 5 = 학교 내신 중상, 8 = 내신 최고난도, 10 = 수능 30번급.\n\n'
            f'표 아래에 다음을 적는다.\n1. {N}문항 예상 시간 합계(분)\n2. 가장 어려운 문항 3개\n'
            "3. '문장은 짧은데 생각이 필요한' 문항과 '계산이 길어서 오래 걸리는' 문항을 각각 골라 적기\n\n"
            '결과는 지시받은 파일 이름으로 이 폴더에 쓴다.\n\n'
            '- 서답형 문항은 답 칸에 소문항 답을 순서대로 적는다(예: (1) a / (2) b / (3) c 꼴). 시간과 체감은 문항 전체 기준으로 적는다.\n')
    open(os.path.join(a.out, 'TASK.md'), 'w').write(task)
    if a.study:
        C = study_cards(a.study); used = [m['key'] for m in meta.values() if m['key'] in C]
        rest = sorted(set(C) - set(P[t].get('key') for t in P)); noise = rnd.sample(rest, min(a.noise, len(rest)))
        cards = used + noise; rnd.shuffle(cards)
        open(os.path.join(a.out, 'study.md'), 'w').write('# 분석집 공부 노트 (시험 전에 공부한 내용)\n\n' + '\n\n---\n\n'.join(C[k] for k in cards))
        meta['_study'] = dict(cards=len(cards), round_cards=used, noise=len(noise))
        json.dump(dict(round=rname, base=a.base, anchors=anchors, items={k: v for k, v in meta.items() if k != '_study'}, study=meta['_study']),
                  open(os.path.join(a.out, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
        st = task.replace('당신은 고2 미적분Ⅰ 학생이', '당신은 시험 전에 학교 부교재 분석집을 공부한 고2 미적분Ⅰ 상위권 학생이') \
                 .replace('다른 파일은 찾거나 열지 않는다.', '다른 파일은 찾거나 열지 않는다. 단, 시험 전에 `study.md`(분석집 공부 노트)를 먼저 끝까지 읽고 공부한다. 공부 시간은 시험 시간에 넣지 않는다. 문제를 풀기 시작한 뒤에는 study.md를 다시 열지 않고 기억한 것만 쓴다.')
        st += ("- 분석집에서 익힌 판정·TIP·함정·계산 정리가 실제로 도움이 된 문항은 '막힌 곳·함정' 칸 맨 앞에 '[분석집]'을 붙이고 무엇이 도움이 됐는지 짧게 적는다. "
               '도움이 안 됐으면 붙이지 않는다. 시간은 분석집을 공부한 학생으로서 실제로 들일 시간을 어림한다.\n')
        open(os.path.join(a.out, 'TASK_study.md'), 'w').write(st)
    print(f'{a.out}: {N}문항(회차 {len(items)} + 앵커 {len(anchors)}), 그림 {fl}' + (f", 분석집 카드 {meta['_study']['cards']}(회차 원문 {len(meta['_study']['round_cards'])})" if a.study else ''))

if __name__ == '__main__':
    main()
