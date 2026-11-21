// 분석서2 렌더러: KaTeX로 \( \)·\[ \]를 바꾼 뒤 A4 PDF로 찍는다(시험지 전용 측정 단계 없음)
const fs=require('fs'),path=require('path');
const katex=require('../node_modules/katex');const {chromium}=require('../node_modules/playwright-core');
(async()=>{const [inp,out]=process.argv.slice(2);let h=fs.readFileSync(inp,'utf8');
const r=(s,d)=>katex.renderToString(s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&'),{displayMode:d,throwOnError:false,strict:false});
h=h.replace(/\\\[([\s\S]+?)\\\]/g,(m,s)=>r(s,true)).replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>r(s,false));
const f=inp.replace('_src','');fs.writeFileSync(f,h);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']}).catch(()=>chromium.launch());
const p=await b.newPage();await p.goto('file://'+path.resolve(f),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:out,format:'A4',preferCSSPageSize:true,printBackground:true});await b.close()})();
