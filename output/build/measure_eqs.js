const fs=require('fs'),path=require('path');const katex=require('../node_modules/katex');
const {chromium}=require('../node_modules/playwright-core');
(async()=>{const L=JSON.parse(fs.readFileSync(process.argv[2]));
let body=L.map((x,i)=>{let h=katex.renderToString('\\displaystyle '+x,{throwOnError:true,strict:false});return `<div><span class="eq" id="e${i}">${h}<span class="bl" style="display:inline-block;width:0;height:0;vertical-align:baseline"></span></span></div>`}).join('');
fs.writeFileSync('me.html',`<html><head><meta charset=utf-8><link rel=stylesheet href="file://${path.resolve('../node_modules/katex/dist/katex.min.css')}"><style>.katex{font-size:9pt}</style></head><body>${body}</body></html>`);
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
await p.goto('file://'+path.resolve('me.html'));
const r=await p.evaluate(()=>{const o={};[...document.querySelectorAll('.eq')].forEach((e,i)=>{const k=e.querySelector('.katex');const bs=[...k.querySelectorAll('.katex-base')].map(x=>x.getBoundingClientRect());const R={top:Math.min(...bs.map(x=>x.top)),bottom:Math.max(...bs.map(x=>x.bottom)),left:Math.min(...bs.map(x=>x.left)),right:Math.max(...bs.map(x=>x.right))};const B=e.querySelector('.bl').getBoundingClientRect();o[i]={w:(R.right-R.left)*0.75,h:(R.bottom-R.top)*0.75,asc:(B.top-R.top)*0.75}});return o});
fs.writeFileSync(process.argv[3],JSON.stringify(r));await b.close()})();
