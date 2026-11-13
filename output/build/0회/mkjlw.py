# measure_jl 결과(jlw_meas.json) + 수동 보정 → jlw.json
import json
MANUAL_RIGHT = {'서답형 1.0': 277.5, '서답형 1-2.0': 287.0, 'Q17.1': 283.0, 'Q18.2': 527.8}   # 손글씨 겹침 등으로 자동 측정이 틀린 줄
NATURAL = {'Q16.1'}                                                          # 원본에서 양끝 맞춤 아닌 줄
m = json.load(open('jlw_meas.json')); jl = {d['id']: d for d in json.load(open('jl.json'))}
w = {}
for k, d in jl.items():
    if k in NATURAL: continue
    if k in MANUAL_RIGHT: w[k] = round(MANUAL_RIGHT[k] - d['x0'], 1)
    elif k in m: w[k] = m[k]
json.dump(w, open('jlw.json', 'w'), ensure_ascii=False, indent=0)
print(len(w), 'lines')
