// 아이패드 가로(1194×834, 2배율)로 성적표 PNG
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [inp,out]=process.argv.slice(2);
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1194,height:834},deviceScaleFactor:2,colorScheme:'light'});
const css='<style>body{padding:18px 22px!important}.wrap{max-width:none!important;display:block!important;column-count:3;column-gap:16px}.wrap>*{break-inside:avoid;margin:0 0 12px!important;display:block}.wrap>.card.notes,.wrap>.notes{break-inside:auto}</style>';
await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+fs.readFileSync(inp,'utf8')+css+'</body></html>',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);
const h=await p.evaluate(()=>document.documentElement.scrollHeight);
console.log('height',h);
await p.screenshot({path:out,fullPage:h>834});await b.close()})();
