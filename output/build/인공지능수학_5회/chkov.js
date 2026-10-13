const path=require('path');const {chromium}=require('../../node_modules/playwright-core');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
await p.goto('file://'+path.resolve(process.argv[2]||'overlay.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const r=await p.evaluate(()=>{const out=[];for(const s of document.querySelectorAll('.ch>span')){if(s.scrollWidth>s.clientWidth+1)out.push(s.closest('.blk').dataset.k+': '+s.textContent.slice(0,30))}return out});
console.log(r.length?r.join('\n'):'no overflow');await b.close()})();
