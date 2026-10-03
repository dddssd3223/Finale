import sys, json, re
out_exam, out_sol = sys.argv[1], sys.argv[2]
sys.argv = ['build.py']
import build
build.FIGS.update(build.figs_info())
fill = {tuple(map(int, k.split(','))): v for k, v in json.load(open('fill.json')).items()}
xml = build.write_exam('x', fill=fill)
prv = '2026학년도 2학년 미적분Ⅰ 중간고사 문제\n' + '\n'.join(
    f"{n}. " + re.sub(r'\$|\{PT\}', '', build.ITEMS[f'Q{n}']['blocks'][0][1])[:60] for n in range(1, 21))
build.pack(xml, out_exam, [('image21', 'fig8.png'), ('image22', 'fig17.png')], prv, title='2026 2학년 미적분Ⅰ 중간고사')
print('exam ok')
