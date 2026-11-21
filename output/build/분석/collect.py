import sys, os, json, re, importlib, runpy
rd=sys.argv[1]
os.chdir(rd); sys.path.insert(0,'.')
c=importlib.import_module('content3')
sol=importlib.import_module('sol3')
src=open('report.py').read()
MARK=eval(re.search(r'MARK = (\[.*?\])',src).group(1))
SA=eval(re.search(r'SA = (\[.*?\]\)\])',src,re.S).group(1)) if re.search(r'SA = (\[.*?\]\)\])',src,re.S) else None
out={'ANS':c.ANS,'MARK':MARK,'SA':SA,'PTS':{n:c.Q[n][0] for n in c.Q},
     'Q':{n:[c.Q[n][1],c.Q[n][2]] for n in c.Q},
     'D':{n:list(sol.D[n]) for n in sol.D},
     'S1':{'q':c.S1,'sub':c.S1S,'d':sol.S1},'S2':{'q':c.S2,'sub':c.S2S,'d':sol.S2}}
print(json.dumps(out,ensure_ascii=False,default=str))
