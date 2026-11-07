import importlib.util, re, json, sys, os
def loadQ(r):
    d=f'r{r}'; sys.path.insert(0,d)
    spec=importlib.util.spec_from_file_location(f'c{r}',f'{d}/content3.py'); m=importlib.util.module_from_spec(spec)
    cwd=os.getcwd(); os.chdir(d)
    try: spec.loader.exec_module(m)
    finally: os.chdir(cwd); sys.path.pop(0)
    return m.Q
def feat(body):
    t=re.sub(r'<[^>]+>',' ',body)
    math=re.findall(r'\\\(.+?\\\)|\\\[.+?\\\]',t,re.S)
    plain=re.sub(r'\\\(.+?\\\)|\\\[.+?\\\]',' ',t,flags=re.S)
    hang=len(re.findall(r'[가-힣]',plain))
    mlen=sum(len(re.sub(r'\\[a-zA-Z]+|[{}\s]','',x)) for x in math)
    return dict(hang=hang, nmath=len(math), mlen=mlen,
        cond='class="cond"' in body or "class='cond'" in body or 'COND' in body, bogi='bogi' in body,
        fig='<img' in body, disp=body.count('\\['),
        frac=len(re.findall(r'\\[dt]?frac',body)), lim=body.count('\\lim'),
        kw=[k for k in ['조건을 만족','모든 실수','최댓값','최솟값','해가 존재','평균변화율','미분가능','연속','접선','그래프','실수 전체'] if k in plain])
R=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20]
out={}
for r in R:
    Q=loadQ(r)
    out[r]={n:feat(Q[n][1]) for n in range(1,9)}
json.dump(out,open('front_feat.json','w'),ensure_ascii=False)
for r in R:
    f=out[r]; H=sum(x['hang'] for x in f.values()); M=sum(x['mlen'] for x in f.values())
    C=sum(x['cond'] or x['bogi'] for x in f.values()); D=sum(x['disp'] for x in f.values())
    print(f'{r:2d} 한글{H:4d} 수식{M:4d} 조건/보기{C} 디스플레이{D} 문항별한글', [x['hang'] for x in f.values()])
