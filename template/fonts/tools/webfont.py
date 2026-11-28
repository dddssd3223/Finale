import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
src, dst = sys.argv[1], sys.argv[2]
t = TTFont(src); order = set(t.getGlyphOrder())
for k in ('EBDT', 'EBLC', 'EBSC'):
    if k in t: del t[k]
m = {u: g for u, g in t.getBestCmap().items() if g in order and g != '.notdef'}
c = newTable('cmap'); c.tableVersion = 0; c.tables = []
for fmt, pid, eid in ((4, 3, 1), (12, 3, 10)):
    st = CmapSubtable.newSubtable(fmt); st.platformID, st.platEncID, st.language = pid, eid, 0
    st.cmap = {u: g for u, g in m.items() if fmt == 12 or u < 0x10000}; c.tables.append(st)
t['cmap'] = c; t.save(dst); print(dst, len(m))
