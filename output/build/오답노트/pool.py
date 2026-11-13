# -*- coding: utf-8 -*-
"""오답노트 풀: 1~5회 선택형 오답 + 감점된 서답형 문항"""
import rounds
I, DIFF, INFO = {}, {}, {}
MC, SA = [], []
for n in range(1, 6):
    r = rounds.load_round(n); c = r['c']
    for q in range(1, 19):
        if r['mark'][q - 1] != c.ANS[q]:
            pt, body, ch = c.Q[q]
            k = f'R{n}Q{q}'
            body = rounds.fixfig(body, n).replace('{PT}', f' <span class="pt">[{n}회 {q}번 · {pt:.1f}점]</span>')
            I[k] = (body, ch, '①②③④⑤'[c.ANS[q] - 1], f'{n}회 {q}번')
            DIFF[k] = n * 100 + q; MC.append(k)
            INFO[k] = dict(n=n, q=q, pt=pt, mine=r['mark'][q - 1], ans=c.ANS[q], D=r['D'][q], ch=ch,
                           note=next((x for x in r['notes'] if f'{q}번' in x and '선택형' in x), ''))
    for j, (lab, subs_body, subs, sd) in enumerate([('단답형 1', c.S1, c.S1S, r['S1']), ('서술형 1', c.S2, c.S2S, r['S2'])]):
        got = r['sa'][j][1]
        if sum(g for _, _, g in got) < sum(m for _, m, _ in got):
            k = f'R{n}S{j + 1}'
            I[k] = (rounds.fixfig(subs_body, n), None, ' / '.join(sd['ans']), f'{n}회 {lab}', f'{n}회 {lab}', subs)
            DIFF[k] = n * 100 + 50 + j; SA.append(k)
            INFO[k] = dict(n=n, lab=lab, got=got, sd=sd, note=[x for x in r['notes'] if lab in x])
