import sys,os,re,importlib.util,json
base='/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad'
r=int(sys.argv[1]);d=f'{base}/r{r}';os.chdir(d);sys.path.insert(0,d)
import content3 as c
s=open('sol3.py').read()
ns={'__name__':'x'}
# sol3 정의부(빌드 함수 전)까지만 실행
m_=re.search(r'^(D|EX) = .*$',s,re.M); cut=m_.end()
exec(s[:cut],ns)
D=ns.get('D') or ns.get('EX')
sa=re.findall(r"\('(단답형[^']*|서술형[^']*)',\s*\w+,\s*'([^']*)'\)",s)
one=sum(c.Q[n][0] for n in range(1,19) if D[n][4] in('상','최상'))
two=sum(c.Q[n][0] for n in range(1,19) if D[n][4]=='중상')
sahi=sum(6 for lab,dd in sa if dd.split('→')[-1].strip() in('상','최상'))
samid=sum(6 for lab,dd in sa if dd.split('→')[-1].strip()=='중상')
print(json.dumps({'r':r,'one':round(one+sahi,1),'two':round(two+samid,1),'sa':sa,'lv':[D[n][4] for n in range(1,19)]},ensure_ascii=False))
