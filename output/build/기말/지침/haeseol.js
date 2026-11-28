// 해설지 렌더러: <입력 html> <출력 pdf> <머리말 글> — KaTeX로 수식을 바꾸고 Chromium으로 PDF(쪽 번호 꼬리말)
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', 'node_modules');
const katex = require(path.join(NM, 'katex'));
const { chromium } = require(path.join(NM, 'playwright-core'));
(async () => {
  const [inp, out, title] = process.argv.slice(2);
  let h = fs.readFileSync(inp, 'utf8');
  const r = (s, d) => katex.renderToString(s, { displayMode: d, throwOnError: true, strict: false });
  h = h.replace(/\\\[([\s\S]+?)\\\]/g, (m, s) => r(s, true)).replace(/\\\(([\s\S]+?)\\\)/g, (m, s) => r(s, false));
  const done = inp.replace(/_src\.html$/, '.html');
  fs.writeFileSync(done, h);
  const exe = ['/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/opt/pw-browsers/chromium']
    .find(c => { try { return fs.statSync(c).isFile(); } catch (e) { return false; } });
  const b = await chromium.launch({ executablePath: exe });
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(done), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const foot = `<div style="width:100%;font-family:'NanumSquare',sans-serif;font-size:7.5pt;color:#6b7a8c;padding:0 14mm;display:flex;justify-content:space-between">
    <span>${title}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: foot,
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
