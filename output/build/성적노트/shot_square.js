// 정사각형 성적표 PNG(기본 1440×1440) — 문자(MMS) 한 장용. 솔라피 한도 1500×1440 안.
// 왼쪽 단: 점수·선택형·서답형·회차별 점수 / 오른쪽 단: 감점 내역. 내용 높이가 폭 안에 드는 가장 좁은 폭을 찾아 정사각형으로 맞춤.
// 사용: node shot_square.js <성적표.html> <out.png> [픽셀=1440]
const {chromium}=require('playwright');const fs=require('fs');
const css='<style>html,body{margin:0}body{padding:22px!important;box-sizing:border-box}.wrap{max-width:none!important}'+
'.sq{display:flex;gap:16px;align-items:stretch}.sq>div{flex:1;display:flex;flex-direction:column;gap:12px;min-width:0}.sq>div>*{margin:0!important}.sq>div:last-child>*:last-child{flex:1}footer{margin-top:12px}</style>';
const arrange=()=>{const w=document.getElementById('app');
 // 감점 내역 줄이기: 첫 문장(표기·정답, 문항 칸에 이미 있음)과 '설계된 오답' 문장을 빼고 이유 한 문장만 남김. 칭찬 줄은 코멘트 문자로 감.
 document.querySelectorAll('.notes li p').forEach(p=>{const ss=p.textContent.split(/(?<=[.다함음])\s+/).filter(x=>!/(표기|기재), 정답|설계된 오답/.test(x));if(ss.length)p.textContent=ss[0]});
 document.querySelectorAll('section .good').forEach(e=>{if(e.closest('section')&&/감점/.test(e.closest('section').textContent.slice(0,10)))e.remove()});const L=document.createElement('div'),R=document.createElement('div');
 const kids=[...w.children];const foot=kids.find(k=>k.tagName=='FOOTER');
 for(const k of kids){if(k===foot)continue;(/^\s*(감점|내 위치)/.test(k.textContent)?R:L).appendChild(k)}
 const box=document.createElement('div');box.className='sq';box.append(L,R);w.replaceChildren(box);if(foot)w.appendChild(foot);w.style.display='block'};
async function page(b,html,w,dsf=1){const p=await b.newPage({viewport:{width:w,height:w},deviceScaleFactor:dsf,colorScheme:'light'});
 await p.setContent(html,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.evaluate(arrange);
 const h=await p.evaluate(()=>document.documentElement.scrollHeight);return [p,h]}
(async()=>{const [inp,out,px='1440']=process.argv.slice(2);const b=await chromium.launch();
const html='<!doctype html><html><head><meta charset="utf-8"></head><body>'+fs.readFileSync(inp,'utf8')+css+'</body></html>';
let best=null;for(let w=700;w<=1200;w+=10){const [p,h]=await page(b,html,w);await p.close();if(h<=w){best=w;break}}
if(!best)throw new Error('정사각형에 맞는 폭을 못 찾음');
const [p,h]=await page(b,html,best,(+px)/best);
await p.evaluate(pad=>{document.body.style.paddingTop=(22+pad)+'px'},Math.floor((best-h)/2));
await p.screenshot({path:out,clip:{x:0,y:0,width:best,height:best}});console.log('width',best,'content',h);await b.close()})();
