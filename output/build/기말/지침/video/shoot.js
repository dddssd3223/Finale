const fs=require('fs'),path=require('path');const B='/home/user/Finale/output/build/기말';
const katex=require(B+'/node_modules/katex');const {chromium}=require(B+'/node_modules/playwright-core');
(async()=>{const D=__dirname;let h=fs.readFileSync(D+'/page_src.html','utf8');
const r=(s,d)=>katex.renderToString(s,{displayMode:d,throwOnError:true,strict:false,trust:true});
h=h.replace(/\\\[([\s\S]+?)\\\]/g,(m,s)=>r(s,true)).replace(/\\\(([\s\S]+?)\\\)/g,(m,s)=>r(s,false));
fs.writeFileSync(D+'/page.html',h);const st=JSON.parse(fs.readFileSync(D+'/states.json','utf8'));
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1920,height:1080}});await p.goto('file://'+D+'/page.html',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);await p.evaluate(require(B+'/지침/eqfont.js'));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.nodeValue.includes('\uE050')){n.nodeValue=n.nodeValue.replace(/\uE050/g,'\u2032');n.parentElement.style.fontFamily='KaTeX_Main';n.parentElement.style.marginLeft='0.04em';}}});
fs.mkdirSync(D+'/fr',{recursive:true});
for(let i=0;i<st.length;i++){const s=st[i];await p.evaluate(({s,u,c})=>{document.querySelectorAll('.scene').forEach(e=>e.classList.remove('on'));const sc=document.getElementById('s'+s);sc.classList.add('on');
sc.querySelectorAll('.r').forEach(e=>e.classList.toggle('v',+e.dataset.i<=u));sc.querySelector('.cap').textContent=c;},{s:s.s,u:s.upto,c:s.cap});
await p.screenshot({path:`${D}/fr/${String(i).padStart(3,'0')}.png`});}
await b.close();})();
