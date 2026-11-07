// 휴대폰 폭(390px, 3배율)으로 성적표 전체를 PNG로 저장 — 문자(MMS)로 보내기용
const {chromium}=require('../node_modules/playwright-core');const fs=require('fs');
(async()=>{const [inp,out]=process.argv.slice(2);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:3,colorScheme:'light'});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.setContent('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+fs.readFileSync(inp,'utf8')+'</body></html>',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);
const ov=await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
await p.screenshot({path:out,fullPage:true});console.log('overflow',ov,errs);await b.close()})();
