// lecture.py 보조: <작업 폴더> — page_src.html을 KaTeX로 바꾸고 states.json의 상태마다 PNG(f0000.png …)를 찍는다.
const fs = require('fs'), path = require('path'); const B = '/home/user/Finale/output/build/기말';
const katex = require(B + '/node_modules/katex'); const { chromium } = require(B + '/node_modules/playwright-core');
(async () => {
  const W = process.argv[2]; let h = fs.readFileSync(W + '/page_src.html', 'utf8');
  const r = (s, d) => katex.renderToString(s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'), { displayMode: d, throwOnError: true, strict: false, trust: true });
  h = h.replace(/\\\[([\s\S]+?)\\\]/g, (m, s) => r(s, true)).replace(/\\\(([\s\S]+?)\\\)/g, (m, s) => r(s, false));
  fs.writeFileSync(W + '/page.html', h);
  const st = JSON.parse(fs.readFileSync(W + '/states.json', 'utf8'));
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + W + '/page.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  // 넘치는 판서 페이지는 글씨를 줄인다
  await p.evaluate(() => { for (const pg of document.querySelectorAll('.pg')) { pg.classList.add('on'); const bd = pg.querySelector('.bd'); if (bd) { bd.querySelectorAll('.ln').forEach(l => l.classList.add('v')); let fs = 58; while (bd.scrollHeight > bd.clientHeight + 2 && fs > 34) { fs -= 2; bd.style.fontSize = fs + 'px'; } bd.querySelectorAll('.ln').forEach(l => l.classList.remove('v')); } const pb = pg.querySelector('.pb'); if (pb) { let fs = 40; while (pb.getBoundingClientRect().bottom > 1050 && fs > 24) { fs -= 2; pb.style.fontSize = fs + 'px'; } } pg.classList.remove('on'); } });
  for (let i = 0; i < st.length; i++) {
    const [pid, upto] = st[i];
    await p.evaluate(({ pid, upto }) => { document.querySelectorAll('.pg').forEach(e => e.classList.remove('on')); const pg = document.getElementById(pid); pg.classList.add('on'); pg.querySelectorAll('.ln').forEach(l => l.classList.toggle('v', +l.dataset.i <= upto)); }, { pid, upto });
    await p.screenshot({ path: `${W}/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
