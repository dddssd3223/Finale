const fs=require('fs'),path=require('path');
let R=__dirname;while(!(fs.existsSync(path.join(R,'fonts'))&&fs.existsSync(path.join(R,'src')))){const q=path.dirname(R);if(q===R)throw new Error('template root not found');R=q}
const katex=require(path.join(R,'node_modules','katex'));const {chromium}=require(path.join(R,'node_modules','playwright-core'));
(async()=>{const [inp,out]=process.argv.slice(2);let h=fs.readFileSync(inp,'utf8');
const r=(s,d)=>katex.renderToString(s,{displayMode:d,throwOnError:true,strict:false});
h=h.replace(/\\\[([\s\S]+?)\\\]/g,(m,s)=>r(s,true)).replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>r(s,false));
fs.writeFileSync(inp.replace('_src',''),h);
const b=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});const p=await b.newPage();
await p.goto('file://'+path.resolve(inp.replace('_src','')),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.evaluate(require('./eqfont.js'));await p.evaluate(()=>document.fonts.ready);
const ov=await p.evaluate(()=>[...document.querySelectorAll('.blk')].map(e=>{const r=e.getBoundingClientRect();return {k:e.dataset.k,top:r.top*0.75,bottom:r.bottom*0.75}}));
fs.writeFileSync(path.join(path.dirname(inp),'blocks.json'),JSON.stringify(ov));
await p.pdf({path:out,format:'A4',preferCSSPageSize:true,printBackground:process.argv[4]==='bg'});await b.close()})();
