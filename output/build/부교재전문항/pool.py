# -*- coding: utf-8 -*-
"""부교재 전문항 풀: 03 미분계수와 도함수 + 04 접선(일부) + 01 함수의 극한 + 02 함수의 연속"""
import sys, os, json, glob, importlib, re
HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, '..', 'wb2', 'parts')
sys.path.insert(0, PARTS)
import items as old

I, DIFF = {}, {}
dold = json.load(open(os.path.join(HERE, 'diff_old.json')))
for k, v in old.I.items():
    I[k] = v; DIFF[k] = dold[k]
EXCLUDE = {'B59', 'T3', 'T6'}            # 거리 a²−1, 평균값 정리 2문항
for f in sorted(glob.glob(os.path.join(PARTS, 'items_p*.py'))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    for k, v in m.I.items():
        I[k] = (old._fix(v[0]),) + tuple(v[1:])
        DIFF[k] = m.D[k][0]
EXCLUDE |= set(json.load(open(os.path.join(HERE, 'exclude_new.json')))) if os.path.exists(os.path.join(HERE, 'exclude_new.json')) else set()
keys = [k for k in I if k not in EXCLUDE]
MC = [k for k in keys if I[k][1]]
SA = [k for k in keys if not I[k][1]]
