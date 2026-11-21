exec(open('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb2/figs_head.py').read())
os.chdir('/tmp/claude-0/-home-user-Finale/12e2698e-3f00-52d2-bb21-f0ec4f5dc473/scratchpad/wb3/parts')
PR = chr(0xE050)  # prime glyph in the equation font

def save(fig, name):
    fig.savefig(name + '.svg', bbox_inches='tight', pad_inches=0.02); plt.close(fig)

# ---- I24: y=f'(x)=(x-1)(x-2), y-intercept high, vertex just below x-axis ----
fig, ax = plt.subplots(figsize=(1.75, 2.35))
axes(ax, (-0.55, 3.75), (-0.55, 3.35), asp='auto', dx=0.1, dy=0.08)
ax.texts[-1].set_position((-0.05, -0.06))
xs = np.linspace(-0.27, 3.27, 300)
ax.plot(xs, (xs - 1) * (xs - 2), 'k', lw=1.0)
ax.text(0.97, -0.07, '1', ha='right', va='top'); ax.text(2.06, -0.07, '2', ha='left', va='top')
ax.text(0.95, 3.15, 'y=f' + PR + '(x)', ha='left', va='center')
save(fig, 'fig_I24')
