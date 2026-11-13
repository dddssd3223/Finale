const fs=require('fs'),path=require('path');
const katex=require('../../node_modules/katex');const {chromium}=require('../../node_modules/playwright-core');
(async()=>{const [inp,out]=process.argv.slice(2);let h=fs.readFileSync(inp,'utf8');
const r=(s,d)=>katex.renderToString(s,{displayMode:d,throwOnError:true,strict:false});
h=h.replace(/\\\[([\s\S]+?)\\\]/g,(m,s)=>r(s,true)).replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>r(s,false));
fs.writeFileSync(inp.replace('_src',''),h);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
await p.goto('file://'+path.resolve(inp.replace('_src','')),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.evaluate(require('./eqfont.js'));await p.evaluate(()=>document.fonts.ready);
// 한글(HWP) '글자에 따라' 줄 간격 흉내: 키 큰 인라인 수식(분수·극한)은 위아래 여백을 높이에 비례해 준다
await p.evaluate((K)=>{for(const k of document.querySelectorAll('.katex')){if(k.closest('.katex-display')||k.closest('.s1'))continue;const h=(()=>{let t=1e9,b=-1e9;for(const e of k.querySelectorAll('*')){const r=e.getBoundingClientRect();if(r.height>0&&r.width>0){t=Math.min(t,r.top);b=Math.max(b,r.bottom)}}return b-t})(),fs=parseFloat(getComputedStyle(k).fontSize);if(h>2.1*fs){k.style.display='inline-block';k.style.padding=(K*h)+'px 0'}}},0.16);
// 원본 줄 너비보다 긴 줄은 낱말 간격을 줄여 한 줄에 맞춤
await p.evaluate(()=>{for(const e of document.querySelectorAll('.jl[style*=width]')){let ws=parseFloat(getComputedStyle(e).wordSpacing)||0;let n=0;while(e.scrollWidth>e.clientWidth+0.5&&n<60){ws-=0.25;e.style.wordSpacing=ws+'px';n++}}});
const ov=await p.evaluate(()=>[...document.querySelectorAll('.blk')].map(e=>{const r=e.getBoundingClientRect();return {k:e.dataset.k,top:r.top*0.75,bottom:r.bottom*0.75}}));
fs.writeFileSync(path.join(path.dirname(inp),'blocks.json'),JSON.stringify(ov));
const jl=await p.evaluate(()=>{const pgs=[...document.querySelectorAll('.pg')];return [...document.querySelectorAll('.jl')].map(e=>{const pg=e.closest('.pg'),R=pg.getBoundingClientRect(),r=e.getBoundingClientRect(),rs=[...e.getClientRects()];
 let x1=-1e9,y0=1e9,y1=-1e9;const rg=document.createRange();rg.selectNodeContents(e);for(const q of rg.getClientRects()){if(q.width>0){x1=Math.max(x1,q.right);y0=Math.min(y0,q.top);y1=Math.max(y1,q.bottom)}}
 return {id:e.dataset.id,pg:pgs.indexOf(pg),x0:(r.left-R.left)*0.75,x1:(x1-R.left)*0.75,top:(r.top-R.top)*0.75,bot:(r.bottom-R.top)*0.75,lines:rs.length}})});
fs.writeFileSync(path.join(path.dirname(inp),'jl.json'),JSON.stringify(jl));
const dm=await p.evaluate(()=>{const pgs=[...document.querySelectorAll('.pg')];return [...document.querySelectorAll('.katex-display')].map(e=>{const pg=e.closest('.pg'),R=pg.getBoundingClientRect();let x0=1e9,y0=1e9,y1=-1e9;for(const q of e.querySelectorAll('.katex-html *')){const r=q.getBoundingClientRect();if(r.width>0&&r.height>0){x0=Math.min(x0,r.left);y0=Math.min(y0,r.top);y1=Math.max(y1,r.bottom)}}
 const blk=e.closest('.blk');return {k:blk?blk.dataset.k:'',pg:pgs.indexOf(pg),x0:(x0-R.left)*0.75,top:(y0-R.top)*0.75,bot:(y1-R.top)*0.75}})});
fs.writeFileSync(path.join(path.dirname(inp),'dm.json'),JSON.stringify(dm));
const ch=await p.evaluate(()=>{const pgs=[...document.querySelectorAll('.pg')];return [...document.querySelectorAll('.ch')].map(e=>{const pg=e.closest('.pg'),R=pg.getBoundingClientRect(),r=e.getBoundingClientRect();return {k:e.closest('.blk').dataset.k,pg:pgs.indexOf(pg),x0:(r.left-R.left)*0.75,top:(r.top-R.top)*0.75,bot:(r.bottom-R.top)*0.75}})});
fs.writeFileSync(path.join(path.dirname(inp),'ch.json'),JSON.stringify(ch));
await p.pdf({path:out,format:'A4',preferCSSPageSize:true,printBackground:process.argv[4]==='bg'});await b.close()})();
