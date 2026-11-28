// KaTeX가 그린 수식 글자를 한글 수식 글꼴(HyhwpEQ, PUA 인코딩)로 바꾼다.
module.exports = function () {
  const UP = {}, IT = {};
  for (let i = 0; i < 26; i++) { UP[String.fromCharCode(65 + i)] = 0xE000 + i; UP[String.fromCharCode(97 + i)] = 0xE01A + i; IT[String.fromCharCode(97 + i)] = 0xE0E5 + i; }
  for (let d = 1; d <= 9; d++) UP[String(d)] = 0xE034 + d - 1; UP['0'] = 0xE03D;
  const sym = {'!':0xE03E,'@':0xE03F,'#':0xE040,'$':0xE041,'%':0xE042,'*':0xE043,'(':0xE044,')':0xE045,'−':0xE046,'-':0xE046,'=':0xE047,'+':0xE048,'[':0xE049,']':0xE04A,'{':0xE04B,'}':0xE04C,'|':0xE04D,'\u2223':0xE04D,';':0xE04E,':':0xE04F,'′':0xE050,'″':0xE051,',':0xE052,'.':0xE053,'/':0xE054,'<':0xE055,'>':0xE056,'?':0xE057};
  Object.assign(UP, sym);
  const greek = 'αβγδϵζηθικλμνξοπρστυϕχψω';
  for (let i = 0; i < greek.length; i++) IT[greek[i]] = 0xE09D + i;
  IT['φ'] = 0xE0B1; IT['ε'] = 0xE10E;
  const KEEP = '±×÷→←↔⇒⇔⇐∞≤≥≠≈∼⋅∈∉⊂⊃∴∵∩∪∠△';
  const walk = (el) => {
    for (const node of [...el.childNodes]) {
      if (node.nodeType === 1) {
        const cls = node.className && node.className.baseVal === undefined ? node.className : '';
        if (/delimsizing|delimcenter|mult|katex-mathml|text/.test(cls) || node.tagName === 'svg') continue;
        const ff = getComputedStyle(node).fontFamily;
        if (/KaTeX_Size/.test(ff)) continue;
        walk(node);
      } else if (node.nodeType === 3 && node.nodeValue.trim()) {
        const p = node.parentElement;
        const ital = !!p.closest('.mathnormal,.mathit');
        // 다시 만든 HyhwpEQ에 없는 글리프(예: 기울임 l, o)가 하나라도 있으면 그 글자 덩어리는 KaTeX 글꼴로 둔다
        const MISSING = new Set([0xE004,0xE015,0xE016,0xE01B,0xE01D,0xE01E,0xE01F,0xE021,0xE023,0xE024,0xE029,0xE02A,0xE02B,0xE02D,0xE02E,0xE02F,0xE030,0xE032,0xE033,0xE03E,0xE03F,0xE040,0xE041,0xE042,0xE043,0xE04E,0xE051,0xE057,0xE0B1,0xE0F0,0xE0F3]);
        const tgt = ch => (ital && IT[ch]) ? IT[ch] : ((ital && /[A-Z]/.test(ch)) || UP[ch] !== undefined) ? UP[ch] : null;
        if ([...node.nodeValue].some(ch => MISSING.has(tgt(ch)))) continue;
        let out = '', any = false, upperIt = false;
        for (const ch of node.nodeValue) {
          if (ital && IT[ch]) { out += String.fromCharCode(IT[ch]); any = true; }
          else if (ital && /[A-Z]/.test(ch)) { out += String.fromCharCode(UP[ch]); any = true; upperIt = true; }
          else if (UP[ch] !== undefined) { out += String.fromCharCode(UP[ch]); any = true; }
          else { out += ch; if (KEEP.includes(ch)) any = true; }
        }
        if (any) {
          node.nodeValue = out;
          p.style.fontFamily = "'HYEQ','HB'";
          p.style.fontStyle = upperIt ? 'italic' : 'normal';
        }
      }
    }
  };
  document.querySelectorAll('.katex-html').forEach(walk);
};
