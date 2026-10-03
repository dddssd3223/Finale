import re

def _match_brace(s, i):
    # s[i]=='{' -> index of matching '}'
    d = 0
    for j in range(i, len(s)):
        if s[j] == '{': d += 1
        elif s[j] == '}':
            d -= 1
            if d == 0: return j
    raise ValueError('unbalanced: ' + s)

def _group_before(s, i):
    # group ending right before index i (skip spaces); return (start, inner)
    j = i - 1
    while j >= 0 and s[j] == ' ': j -= 1
    if s[j] != '}': raise ValueError('over needs braces: ' + s)
    d = 0
    for k in range(j, -1, -1):
        if s[k] == '}': d += 1
        elif s[k] == '{':
            d -= 1
            if d == 0: return k, s[k+1:j]
    raise ValueError(s)

def _group_after(s, i):
    j = i
    while s[j] == ' ': j += 1
    if s[j] != '{': raise ValueError('over needs braces after: ' + s)
    e = _match_brace(s, j)
    return e, s[j+1:e]

def to_latex(eq):
    s = ' ' + eq + ' '
    # over (process left to right; nested handled by recursion on inner text)
    while True:
        m = re.search(r'\bover\b', s)
        if not m: break
        st, num = _group_before(s, m.start())
        en, den = _group_after(s, m.end())
        s = s[:st] + '\\frac{' + num + '}{' + den + '}' + s[en+1:]
    # cases{ a & b # c & d }
    while True:
        m = re.search(r'\bcases\s*\{', s)
        if not m: break
        b = s.index('{', m.start())
        e = _match_brace(s, b)
        inner = s[b+1:e].replace('#', r' \\ ')
        s = s[:m.start()] + r'\begin{cases}' + inner + r'\end{cases}' + s[e+1:]
    rep = [
        (r'\bLEFT\s*\{', r'\\left\\{'), (r'\bRIGHT\s*\}', r'\\right\\}'),
        (r'\bLEFT\s*\|', r'\\left|'), (r'\bRIGHT\s*\|', r'\\right|'),
        (r'\bLEFT\s*\(', r'\\left('), (r'\bRIGHT\s*\)', r'\\right)'),
        (r'\bLEFT\s*\[', r'\\left['), (r'\bRIGHT\s*\]', r'\\right]'),
        (r'\blim\b', r'\\lim'), (r'->', r'\\to '), (r'\binf\b', r'\\infty '),
        (r'\bleq\b', r'\\le '), (r'\bgeq\b', r'\\ge '), (r'!=', r'\\ne '),
        (r'\bTIMES\b', r'\\times '), (r'\bcdot\b', r'\\cdot '), (r'\bcdots\b', r'\\cdots '),
        (r'\balpha\b', r'\\alpha '), (r'\bbeta\b', r'\\beta '), (r'\bgamma\b', r'\\gamma '),
        (r'\bsqrt\b', r'\\sqrt'), (r'\bin\b', r'\\in '), (r'\bphi\b', r'\\phi '), (r'\boverline\b', r'\\overline'),
        (r'\bTHEREFORE\b', r'\\therefore '), (r'\bpm\b', r'\\pm '),
        (r'\bLARROW\b', r'\\Leftarrow '), (r'\bRARROW\b', r'\\Rightarrow '), (r'\bLRARROW\b', r'\\Leftrightarrow '),
        (r'~', r'\\ '), (r'`', r'\\,'),
    ]
    for a, bb in rep:
        s = re.sub(a, bb, s)
    # rm X  -> \mathrm{X} for the following token/group
    def rm(m):
        return r'\mathrm{' + m.group(1) + '}'
    s = re.sub(r'\brm\s*\{([^{}]*)\}', rm, s)
    s = re.sub(r'\brm\s+([A-Za-z]+)', rm, s)
    s = s.replace('&', '&')
    return s.strip()
