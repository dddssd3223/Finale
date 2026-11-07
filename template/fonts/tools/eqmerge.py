import fitz, re, io, glob, sys, copy
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4
glyphs, mets, cmap = {}, {}, {}
base = None
def parse_tu(s):
    m = {}
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', s, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk): m[int(a,16)] = int(b,16)
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', s, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            for i in range(int(a,16), int(b,16)+1): m[i] = int(c,16) + i - int(a,16)
    return m
for pdf in glob.glob('/home/user/Finale/output/**/*.pdf', recursive=True):
    try: d = fitz.open(pdf)
    except Exception: continue
    for x in range(1, d.xref_length()):
        try: o = d.xref_object(x)
        except Exception: continue
        if '/Type0' not in o or 'HyhwpEQ' not in o: continue
        desc = int(re.search(r'/DescendantFonts\s*\[\s*(\d+) 0 R', o).group(1))
        fd = int(re.search(r'/FontDescriptor (\d+) 0 R', d.xref_object(desc)).group(1))
        ff = int(re.search(r'/FontFile2 (\d+) 0 R', d.xref_object(fd)).group(1))
        t = TTFont(io.BytesIO(d.xref_stream(ff)))
        if base is None or t['maxp'].numGlyphs > base['maxp'].numGlyphs: base = t
        g = t['glyf']; order = t.getGlyphOrder()
        for gid, name in enumerate(order):
            gl = g[name]
            if gl.numberOfContours != 0 and gid not in glyphs:
                glyphs[gid] = (gl, g); mets[gid] = t['hmtx'][name]
        tu = re.search(r'/ToUnicode (\d+) 0 R', o)
        if tu:
            for cid, u in parse_tu(d.xref_stream(int(tu.group(1))).decode('latin1')).items(): cmap.setdefault(u, cid)
t = base; order = t.getGlyphOrder(); g = t['glyf']
for gid, (gl, src) in glyphs.items():
    gl.expand(src); g[order[gid]] = gl; t['hmtx'][order[gid]] = mets[gid]
c = newTable('cmap'); c.tableVersion = 0
st = cmap_format_4(4); st.platformID, st.platEncID, st.language = 3, 1, 0
st.cmap = {u: order[cid] for u, cid in cmap.items() if cid < len(order) and u < 0x10000}
c.tables = [st]; t['cmap'] = c
p = newTable('post'); p.formatType = 3.0; p.italicAngle = 0; p.underlinePosition = -100; p.underlineThickness = 50
p.isFixedPitch = 0; p.minMemType42 = p.maxMemType42 = p.minMemType1 = p.maxMemType1 = 0; t['post'] = p
t.save(sys.argv[1])
print('glyphs', len(glyphs), 'cmap', len(st.cmap))
print(' '.join(f'{u:04X}' for u in sorted(st.cmap)))
