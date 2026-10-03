const fs=require('fs'),path=require('path');
const katex=require(path.join(__dirname,'../node_modules/katex'));
const {chromium}=require(path.join(__dirname,'../node_modules/playwright-core'));
(async()=>{
  const [inp,outHtml,outPdf]=process.argv.slice(2);
  let h=fs.readFileSync(inp,'utf8');
  const r=(s,d)=>katex.renderToString(s,{displayMode:d,throwOnError:true,strict:false});
  h=h.replace(/\\\[([\s\S]+?)\\\]/g,(m,s)=>r(s,true)).replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>r(s,false));
  fs.writeFileSync(outHtml,h);
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage();
  await p.goto('file://'+path.resolve(outHtml),{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  const ov=await p.evaluate(()=>[...document.querySelectorAll('.col,.slot')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>(e.dataset.id||e.className)+':'+e.scrollHeight+'>'+e.clientHeight));
  if(ov.length) console.log('OVERFLOW',ov);
  await p.pdf({path:outPdf,format:'A4',printBackground:true,preferCSSPageSize:true});
  await b.close();
})();
