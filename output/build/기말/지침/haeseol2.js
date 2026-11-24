// 해설지(시판 꼴) 렌더러: <입력 html> <출력 pdf> <머리말 글>
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', 'node_modules');
const katex = require(path.join(NM, 'katex'));
const { chromium } = require(path.join(NM, 'playwright-core'));
(async () => {
  const [inp, out, title, mode] = process.argv.slice(2);   // mode 'plain': 표지처럼 머리말·쪽 번호 없이 여백 0
  let h = fs.readFileSync(inp, 'utf8');
  const r = (s, d) => katex.renderToString(s, { displayMode: d, throwOnError: true, strict: false, trust: true });
  h = h.replace(/\\\[([\s\S]+?)\\\]/g, (m, s) => r(s, true)).replace(/\\\(([\s\S]+?)\\\)/g, (m, s) => r(s, false));
  const done = inp.replace(/_src\.html$/, '.html');
  fs.writeFileSync(done, h);
  const exe = ['/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/opt/pw-browsers/chromium']
    .find(c => { try { return fs.statSync(c).isFile(); } catch (e) { return false; } });
  const b = await chromium.launch({ executablePath: exe });
  const p = await b.newPage({ viewport: { width: 673, height: 1000 } });   // A4 - 좌우 여백 16mm = 인쇄 본문 너비
  await p.goto('file://' + path.resolve(done), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(require('./eqfont.js')); await p.evaluate(() => document.fonts.ready);   // 수식 글자를 한글 수식 글꼴(HyhwpEQ)로 — 시험지와 같은 느낌(2026-11-24)
  await p.emulateMedia({ media: 'print' });
  // 부록 배치: 박스를 두 개씩 한 줄로, 한 쪽에 위 줄·아래 줄(쪽 높이의 반씩). 한 줄이 반 쪽보다 크면 그 줄만 한 쪽을 다 쓴다.
  await p.evaluate(() => {
    const src = document.getElementById('apx-src'); if (!src) return;
    const boxes = [...src.querySelectorAll('.ab')];
    const W = src.clientWidth, colW = (W - 41.6) / 2, PAGE = 968, HALF = PAGE / 2 - 8;
    boxes.forEach(b => { b.style.width = colW + 'px'; });
    const rows = []; for (let i = 0; i < boxes.length; i += 2) rows.push(boxes.slice(i, i + 2));
    const hOf = r => Math.max(...r.map(b => b.getBoundingClientRect().height));
    const pages = []; let cur = [];
    const firstOff = (document.querySelector('.apxh') || { getBoundingClientRect: () => ({ height: 0 }) }).getBoundingClientRect().height + 12;
    for (const r of rows) {
      const big = hOf(r) > HALF - (pages.length === 0 && cur.length === 0 ? firstOff : 0);
      if (big) { if (cur.length) { pages.push(cur); cur = []; } pages.push([{ r, full: true }]); continue; }
      cur.push({ r, full: false }); if (cur.length === 2) { pages.push(cur); cur = []; }
    }
    if (cur.length) pages.push(cur);
    src.innerHTML = '';
    pages.forEach((pg, pi) => {
      const d = document.createElement('div'); d.className = 'apg'; if (pi === 0) d.style.height = (968 - firstOff) + 'px';
      pg.forEach(({ r, full }) => { const h = document.createElement('div'); h.className = 'ahalf' + (full ? ' full' : '');
        r.forEach(b => { b.style.width = ''; h.appendChild(b); }); d.appendChild(h); });
      if (pg.length === 1 && !pg[0].full) { const h = document.createElement('div'); h.className = 'ahalf'; d.appendChild(h); }
      src.appendChild(d);
    });
  });
  // 단 너비를 넘는 수식은 글자 크기를 줄여 맞춤
  const fixed = await p.evaluate(() => { let n = 0;
    const span = e => { let l = 1e9, r = -1e9; for (const q of e.querySelectorAll('.base')) { const b = q.getBoundingClientRect(); if (b.width) { l = Math.min(l, b.left); r = Math.max(r, b.right); } } return r - l; };
    for (const e of document.querySelectorAll('.katex-display > .katex')) {
      const W = (e.closest('.it') || e.parentElement).clientWidth;
      let fs = parseFloat(getComputedStyle(e).fontSize), k = 0;
      while (span(e) > W - 4 && k < 25) { fs *= 0.95; e.style.fontSize = fs + 'px'; k++; }
      if (k) n++; }
    return n; });
  console.log('수식 줄인 개수', fixed);
  const [a1, a2] = title.split(/ (?=\S+$)/);
  const head = `<div style="width:100%;margin:0 16mm;font-family:'NanumSquare',sans-serif;font-size:7.6pt;border-bottom:.8pt dotted #8fb2e6;padding-bottom:2pt;display:flex;justify-content:space-between">
    <span><span style="color:#5f8fd8">${a1}</span> <span style="color:#8fb2e6">〉</span> <b style="color:#222">${a2}</b></span><span style="color:#8fb2e6">양정고 미적분Ⅰ</span></div>`;
  const foot = `<div style="width:100%;text-align:center;font-family:'NanumMyeongjo',serif;font-size:9pt;color:#444"><span class="pageNumber"></span></div>`;
  if (mode === 'plain') { await p.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } }); await b.close(); return; }
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: head, footerTemplate: foot,
    margin: { top: '20mm', bottom: '17mm', left: '16mm', right: '16mm' } });
  await b.close();
})();
