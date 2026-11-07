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
    # 학교 시험지 대조 2026-11-07(2학기 중간 17번 그림·2025 중간 15번 스캔): 채운 삼각 화살촉, 길이 ≈ 선 굵기×6·폭 ≈ ×4.5, 축 굵기 = 곡선 굵기
    kw = dict(arrowstyle='-|>,head_length=0.85,head_width=0.33', lw=LW, color='k', mutation_scale=7, shrinkA=0, shrinkB=0)
    ax.annotate('', xy=(xl[1], 0), xytext=(xl[0], 0), arrowprops=kw)
    ax.annotate('', xy=(0, yl[1]), xytext=(0, yl[0]), arrowprops=kw)
    sx, sy = (xl[1] - xl[0]) * dx / 3, (yl[1] - yl[0]) * dy / 3
    if xlabel: label(ax, xl[1] - sx * 0.2, -sy, xlabel, 'right', 'top')
    if ylabel: label(ax, sx, yl[1] - sy * 0.2, ylabel, 'left', 'top')
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

def tex(ax, x, y, s, ha='center', va='center', size=10):
    """수식 글꼴에 없는 기호(√, 분수)용: matplotlib mathtext (Tinos)"""
    with plt.rc_context({'mathtext.fontset': 'stix'}):
        t = ax.text(x, y, s, ha=ha, va=va, fontsize=size, family='STIXGeneral')
        ax.figure.canvas.draw()
    return t

def save(fig, path):
    fig.savefig(path, bbox_inches='tight', pad_inches=0.02); plt.close(fig)
