// 해설지(시판 꼴) 렌더러: <입력 html> <출력 pdf> <머리말 글>
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', 'node_modules');
const katex = require(path.join(NM, 'katex'));
const { chromium } = require(path.join(NM, 'playwright-core'));
(async () => {
  const [inp, out, title] = process.argv.slice(2);
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
  await p.emulateMedia({ media: 'print' });
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
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: head, footerTemplate: foot,
    margin: { top: '20mm', bottom: '17mm', left: '16mm', right: '16mm' } });
  await b.close();
})();
