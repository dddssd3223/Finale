const fs=require('fs'),path=require('path');
const katex=require('../node_modules/katex');
const {chromium}=require('../node_modules/playwright-core');
(async()=>{
  let h=fs.readFileSync('preview_src.html','utf8');
  h=h.replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>katex.renderToString(s,{throwOnError:true,strict:false})+'<span class="bl" style="display:inline-block;width:0;height:0;vertical-align:baseline"></span>');
  fs.writeFileSync('preview.html',h);
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1800,height:1200}});
  await p.goto('file://'+path.resolve('preview.html'),{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  const r=await p.evaluate(()=>{
    const pt=v=>v*0.75; // px->pt
    const eq={};
    document.querySelectorAll('.eq').forEach(e=>{const i=e.dataset.i; if(eq[i])return;
      const k=e.querySelector('.katex'); const bs=[...k.querySelectorAll('.katex-base')].map(x=>x.getBoundingClientRect());const R={left:Math.min(...bs.map(x=>x.left)),right:Math.max(...bs.map(x=>x.right)),top:Math.min(...bs.map(x=>x.top)),bottom:Math.max(...bs.map(x=>x.bottom))};R.width=R.right-R.left;R.height=R.bottom-R.top; const B=e.querySelector('.bl').getBoundingClientRect();
      eq[i]={w:pt(R.width),h:pt(R.height),asc:pt(B.top-R.top)};});
    const items=[...document.querySelectorAll('.item')].map(e=>{const R=e.getBoundingClientRect();const C=e.parentElement.getBoundingClientRect();
      return {k:e.dataset.k,c:+e.parentElement.dataset.c,top:pt(R.top-C.top),h:pt(R.height)}});
    const boxes={};document.querySelectorAll('.item').forEach(it=>{boxes[it.dataset.k]=[...it.querySelectorAll('.box')].map(x=>pt(x.getBoundingClientRect().height))});
    return {eq,items,boxes};
  });
  fs.writeFileSync('measure.json',JSON.stringify(r));
  await p.screenshot({path:'preview.png',fullPage:true});
  await b.close();
})();
