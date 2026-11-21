import json, subprocess
LIM = {1: 778, 2: 778, 3: 778, 4: 778}
def run(c):
    json.dump(c, open('cuts.json', 'w'))
    subprocess.run(['python3', 'build3.py', 'exam.pdf'], check=True, capture_output=True)
    B = {b['k']: b for b in json.load(open('blocks.json'))}
    return {n: B[f'P{n}']['bottom'] - (B[f'P{n}']['top'] // 842) * 842 for n in range(1, 5)}
cuts = [0, 18, 38, 58]
for col in range(1, 4):           # 단 col의 끝 = cuts[col]
    while True:
        h = run(cuts)
        if h[col] > LIM[col]: cuts[col] -= 1; continue
        cuts[col] += 1; h2 = run(cuts)
        if h2[col] > LIM[col]: cuts[col] -= 1; break
    print(col, cuts)
h = run(cuts); print(cuts, h)
