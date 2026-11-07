# -*- coding: utf-8 -*-
"""시험지 그림 도구 (부교재 그림과 같은 모양: 검은 선, 화살표 축, 채운 점/빈 점, 점선, 회색 칠, 빗금, 수식 글꼴 라벨)

사용 예
    import sys; sys.path.insert(0, '/home/user/Finale/output/build/기말/지침'); import figkit as K
    fig, ax = K.new((-2, 3), (-1, 3), size=(2.6, 2.0))      # x범위, y범위, 크기(인치)
    K.curve(ax, lambda x: x**2 - 1, -1.8, 1.8)               # 곡선
    K.dot(ax, 1, 0, open=True); K.dot(ax, 0, 1)              # 빈 점 / 채운 점
    K.dash(ax, [1, 1], [0, 2])                               # 점선
    K.shade(ax, lambda x: x**2 - 1, -1, 1)                   # 회색 칠 (곡선~x축)
    K.hatch(fig, ax, lambda x: x**2 - 1, 1, 1.6)             # 빗금
    K.label(ax, 1, -0.12, '1', 'center', 'top')              # 수식 글꼴 라벨: 문자·숫자·= ( ) -
    K.tex(ax, 1.7, -0.12, r'$\\sqrt{3}$', 'center', 'top')  # 루트·분수 등은 tex (Tinos 수식)
    K.save(fig, 'fig_b3_6.svg')
글꼴: 시험지 글꼴 폴더(FIGKIT_FONTS 또는 아래 기본 경로)가 있으면 수식 글꼴(HyhwpEQ)·Tinos를 쓰고, 없으면 DejaVu Serif로 대신한다(Codex 실행기 등).
라벨에 쓸 수 없는 글자: 수식 글꼴에 없는 √, 분수 → tex()로."""
import os, numpy as np, matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

FONTS = os.environ.get('FIGKIT_FONTS', '/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/fonts/')
HAVE = os.path.exists(os.path.join(FONTS, 'hyhwpeq_web.ttf'))
if HAVE:
    for f in ['buE4poGnedXvwgX8.ttf', 'buE2poGnedXvwjX-fmE.ttf', 'hyhwpeq_web.ttf']:
        fm.fontManager.addfont(os.path.join(FONTS, f))
    EQ = fm.FontProperties(fname=os.path.join(FONTS, 'hyhwpeq_web.ttf'), size=11)
    plt.rcParams.update({'font.family': 'Tinos', 'mathtext.fontset': 'custom', 'mathtext.it': 'Tinos:italic', 'mathtext.rm': 'Tinos'})
else:
    EQ = fm.FontProperties(family='DejaVu Serif', style='italic', size=10)
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'mathtext.fontset': 'dejavuserif'})
plt.rcParams.update({'font.size': 11, 'svg.fonttype': 'path', 'hatch.linewidth': 0.45})
LW = 0.9
from matplotlib.path import Path as _Path
# 화살촉 모양(끝점이 원점): 길이 1, 반폭 0.42, 뒤 파임 0.8(인쇄 길이 약 3.7pt·폭 약 3.1pt) — 학교 시험지 화살촉
_AV = [(0, 0), (-1, 0.42), (-0.8, 0), (-1, -0.42), (0, 0)]
ARROW_R = _Path(_AV, [_Path.MOVETO, _Path.LINETO, _Path.LINETO, _Path.LINETO, _Path.CLOSEPOLY])
ARROW_U = _Path([(-y, x) for x, y in _AV][:0] or [(y, -x) for x, y in _AV], ARROW_R.codes) if False else _Path([(-v, u) for u, v in [(x, y) for x, y in _AV]], ARROW_R.codes)
ARROW_MS = 11   # 화살촉 길이 ≈ ARROW_MS/2 pt (원점이 끝점이라 마커 상자의 절반)

def pua(t, it=True):
    """HyhwpEQ 글꼴의 사용자 영역 글리프로 바꿈 (소문자=이탤릭, 대문자=로만, 숫자, - = ( ))"""
    if not HAVE: return t
    o = ''
    for ch in t:
        if ch.islower() and it: o += chr(0xE0E5 + ord(ch) - 97)
        elif ch.isupper(): o += chr(0xE000 + ord(ch) - 65)
        elif ch.isdigit(): o += chr(0xE03D if ch == '0' else 0xE034 + int(ch) - 1)
        elif ch == ' ': o += '\u2009'   # 수식 글꼴에 공백 글리프가 없음 → 좁은 공백(대체 글꼴)
        else: o += {'-': chr(0xE046), '=': chr(0xE047), '(': chr(0xE044), ')': chr(0xE045), ',': chr(0xE052), '+': chr(0xE048), '|': chr(0xE04D), ':': chr(0xE04F), ';': chr(0xE04E), "'": chr(0xE050), '.': chr(0xE053), '/': chr(0xE054), '<': chr(0xE055), '>': chr(0xE056)}.get(ch, ch)
    return o

def new(xl, yl, size=(2.6, 2.0), aspect='auto', xlabel='x', ylabel='y', origin=True, dx=0.12, dy=0.12):
    """화살표 축이 있는 빈 그림. dx, dy: 축 이름·O 라벨 간격(데이터 단위 비율)"""
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect(aspect)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    # 학교 시험지 대조 2026-11-07(2025 중간 15번 인쇄 스캔·2학기 중간 17번): 뾰족하고 좁은 화살촉, 뒤가 안으로 파임(stealth꼴), 축 굵기 = 곡선 굵기
    ax.plot([xl[0], xl[1]], [0, 0], 'k', lw=LW, solid_capstyle='butt')
    ax.plot([0, 0], [yl[0], yl[1]], 'k', lw=LW, solid_capstyle='butt')
    ax.plot([xl[1]], [0], marker=ARROW_R, ms=ARROW_MS, color='k', mew=0, zorder=6)
    ax.plot([0], [yl[1]], marker=ARROW_U, ms=ARROW_MS, color='k', mew=0, zorder=6)
    sx, sy = (xl[1] - xl[0]) * dx / 3, (yl[1] - yl[0]) * dy / 3
    # 축 이름은 화살 끝 쪽에(학교 그림: x는 화살 끝 바로 아래, y는 화살 끝 높이의 오른쪽) — 2026-11-07 사용자 지적
    if xlabel: label(ax, xl[1], -sy * 0.6, xlabel, 'right', 'top')
    if ylabel: label(ax, sx * 0.7, yl[1], ylabel, 'left', 'top')
    if origin: label(ax, -sx * 0.6, -sy * 0.8, 'O', 'right', 'top')
    return fig, ax

def curve(ax, f, x0, x1, n=400, lw=LW, **k):
    x = np.linspace(x0, x1, n); ax.plot(x, f(x), 'k', lw=lw, **k)

def line(ax, xs, ys, lw=0.7):
    ax.plot(xs, ys, 'k', lw=lw)

def dash(ax, xs, ys, lw=0.5):
    ax.plot(xs, ys, 'k', ls='--', lw=lw)

def dot(ax, x, y, open=False, ms=3.2):
    ax.plot([x], [y], 'o', ms=ms, mfc='white' if open else 'black', mec='black', mew=0.8, zorder=5)

def shade(ax, f, x0, x1, g=lambda x: 0 * x, color='0.86'):
    x = np.linspace(x0, x1, 300); ax.fill_between(x, g(x), f(x), color=color, lw=0, zorder=0)

def hatch(fig, ax, f, x0, x1, g=lambda x: 0 * x, lw=0.45, gap=2.2):
    """곡선 f와 g 사이를 45° 빗금으로 채움 (gap: pt)"""
    xs = np.linspace(x0, x1, 400); fig.canvas.draw()
    T = ax.transData; inv = T.inverted()
    lo = T.transform(np.column_stack([xs, np.minimum(f(xs), g(xs))])); hi = T.transform(np.column_stack([xs, np.maximum(f(xs), g(xs))]))
    X, Lh, Hh = lo[:, 0], lo[:, 1], hi[:, 1]
    Y0, Y1 = Lh.min(), Hh.max(); step = gap * fig.dpi / 72
    c = X.min() - (Y1 - Y0)
    while c < X.max():
        u = np.linspace(0, Y1 - Y0, 600); px, py = c + u, Y0 + u
        ok = (px >= X.min()) & (px <= X.max()) & (py >= np.interp(px, X, Lh)) & (py <= np.interp(px, X, Hh))
        idx = np.where(ok)[0]
        if len(idx):
            for r in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
                d = inv.transform([(px[r[0]], py[r[0]]), (px[r[-1]], py[r[-1]])])
                ax.plot(d[:, 0], d[:, 1], 'k', lw=lw, solid_capstyle='butt')
        c += step

def label(ax, x, y, s, ha='center', va='center', size=11, roman=False, bg=False):
    """수식 글꼴 라벨 (예: 'y=f(x)', 'A', '-1', 'k'). roman=True면 소문자도 로만"""
    fp = EQ.copy(); fp.set_size(size)
    kw = dict(bbox=dict(fc='white', ec='none', pad=0.6)) if bg else {}
    return ax.text(x, y, pua(s, it=not roman), ha=ha, va=va, fontproperties=fp, zorder=6, **kw)

def rich(ax, x, y, segs, ha='center', va='center', size=10, slant=True):
    """위·아래첨자가 섞인 라벨을 시험지 수식 글꼴 하나로 (2026-11-07: tex(STIX)와 글꼴이 섞이던 것).
    segs: [(글자, 0=보통|1=위첨자|-1=아래첨자), ...] 예: [('y=x', 0), ('2', 1), ('+a', 0)], [('S', 0), ('1', -1)]
    slant=True: 대문자를 본문 수식(S_1 등)처럼 기울여 그린다(수식 글꼴에 기울인 대문자가 없어 같은 글자를 13° 기울임).
    점 이름(P, Q, O)은 label()로 똑바로 둔다."""
    from matplotlib.backends.backend_agg import RendererAgg
    from matplotlib.textpath import TextPath
    from matplotlib.patches import PathPatch
    from matplotlib.transforms import Affine2D, ScaledTranslation
    fig = ax.figure; r = RendererAgg(fig.bbox.width, fig.bbox.height, fig.dpi); inv = ax.transData.inverted()
    pt = fig.dpi / 72
    def fp(k):
        f = EQ.copy(); f.set_size(size * (0.68 if k else 1)); return f
    ms = [r.get_text_width_height_descent(pua(t), fp(k), ismath=False) for t, k in segs]   # 픽셀
    ws = [m[0] for m in ms]; hh, d0 = ms[0][1], ms[0][2]
    X0, Y0 = ax.transData.transform((x, y)); tot = sum(ws)
    X = X0 - {'left': 0, 'center': tot / 2, 'right': tot}[ha]
    Yb = Y0 - {'bottom': 0, 'center': hh / 2, 'top': hh, 'baseline': d0}[va] + d0   # 기준선
    out = []
    for (t, k), w in zip(segs, ws):
        dy = {0: 0, 1: hh * 0.42, -1: -hh * 0.18}[k]
        px, py = inv.transform((X, Yb + dy))
        if slant and k == 0 and t.isupper() and t.isalpha():
            tp = TextPath((0, 0), pua(t), prop=fp(k))   # 단위 pt, 기준선 원점
            tr = Affine2D().skew_deg(13, 0).translate(-0.4, 0).scale(1 / 72) + fig.dpi_scale_trans + ScaledTranslation(px, py, ax.transData)
            out.append(ax.add_patch(PathPatch(tp, transform=tr, fc='k', ec='none', zorder=6)))
        else:
            out.append(ax.text(px, py, pua(t), ha='left', va='baseline', fontproperties=fp(k), zorder=6))
        X += w
    return out

def sub(ax, x, y, base, s, ha='center', va='center', size=10):
    return rich(ax, x, y, [(base, 0), (s, -1)], ha, va, size)

def tex(ax, x, y, s, ha='center', va='center', size=10):
    """수식 글꼴에 없는 기호(√, 분수)용: matplotlib mathtext (Tinos)"""
    with plt.rc_context({'mathtext.fontset': 'stix'}):
        t = ax.text(x, y, s, ha=ha, va=va, fontsize=size, family='STIXGeneral')
        ax.figure.canvas.draw()
    return t

def save(fig, path):
    fig.savefig(path, bbox_inches='tight', pad_inches=0.02); plt.close(fig)
