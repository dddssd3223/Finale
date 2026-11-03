import sys, struct, glob, zlib, bz2, lzma, os
src, out = sys.argv[1], sys.argv[2]
vols = sorted(glob.glob(os.path.join(src, '*.vol*.egg')), key=lambda p: int(p.rsplit('.vol',1)[1].split('.')[0]))
d = b''.join(open(v,'rb').read()[33:] for v in vols)
os.makedirs(out, exist_ok=True)
p = 0; END = 0x08E28222
def u(fmt):
    global p; v = struct.unpack_from('<'+fmt, d, p); p += struct.calcsize('<'+fmt); return v
name = None; buf = []
while p < len(d):
    sig, = u('I')
    if sig == 0x0A8590E3:  # file header
        if name: open(os.path.join(out, name),'wb').write(b''.join(buf))
        fid, flen = u('IQ'); name=None; buf=[]
    elif sig == 0x0A8591AC:
        flag, = u('B'); size, = u('I' if flag & 1 else 'H')
        raw = d[p:p+size]; p += size
        if flag & 8: raw = raw[2:]
        if flag & 16: raw = raw[4:]
        name = raw.decode('utf-8', 'replace').replace('\\','_').replace('/','_')
    elif sig in (0x2C86950B, 0x1EE922E5, 0x08D1470F, 0x04C63672, 0x24F5A262, 0x24E5A060, 0x07463307):
        flag, = u('B'); size, = u('I' if flag & 1 else 'H'); p += size
    elif sig == 0x02B50C13:
        m, hint, us, cs, crc = u('BBIII'); e, = u('I'); assert e == END
        c = d[p:p+cs]; p += cs
        if m == 0: x = c
        elif m == 1: x = zlib.decompress(c, -15)
        elif m == 2: x = bz2.decompress(c)
        elif m == 4:
            props = c[4:9]; x = lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[lzma._decode_filter_properties(lzma.FILTER_LZMA1, props)]).decompress(c[9:], us)
        else: raise SystemExit(f'method {m} unsupported')
        assert zlib.crc32(x) == crc, name
        buf.append(x)
    elif sig == END: pass
    else: raise SystemExit(f'unknown sig {sig:#x} at {p-4}')
if name: open(os.path.join(out, name),'wb').write(b''.join(buf))
