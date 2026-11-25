// half.py 보조: <입력 html> <출력 pdf> — KaTeX 변환, 수식 글꼴(HyhwpEQ), A4 인쇄
const fs = require('fs'), path = require('path');
const NM = path.join(__dirname, '..', 'node_modules');
const katex = require(path.join(NM, 'katex')); const { chromium } = require(path.join(NM, 'playwright-core'));
(async () => {
  const [inp, out] = process.argv.slice(2); let h = fs.readFileSync(inp, 'utf8');
  const r = (s, d) => katex.renderToString(s, { displayMode: d, throwOnError: true, strict: false, trust: true });
  h = h.replace(/\\\[([\s\S]+?)\\\]/g, (m, s) => r(s, true)).replace(/\\\(([\s\S]+?)\\\)/g, (m, s) => r(s, false));
  const html = inp + '.k.html'; fs.writeFileSync(html, h);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage(); await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.evaluate(require('./eqfont.js')); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:7.5pt;text-align:center;color:#555"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
  await b.close(); fs.unlinkSync(html);
})();
