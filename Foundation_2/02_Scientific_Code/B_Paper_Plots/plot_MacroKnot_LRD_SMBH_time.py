
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from matplotlib.lines import Line2D

plt.style.use('default')
fig, ax = plt.subplots(figsize=(12.8, 7.4), facecolor='white')
ax.set_facecolor('white')

z_pts = np.array([3.0, 5.5, 8.0, 10.073, 11.1, 12.0, 14.44], dtype=float)
m_pts = np.array([8.0e8, 3.2e8, 1.4e6, 1.0e6, 5.0e5, 4.0e5, 2.0e5], dtype=float)
order = np.argsort(z_pts)
z_sorted = z_pts[order]
m_sorted = m_pts[order]
interp = PchipInterpolator(z_sorted, np.log10(m_sorted))
z_curve = np.linspace(z_sorted.min(), z_sorted.max(), 800)
m_curve = 10**interp(z_curve)

for x0, x1, c, label in [
    (14.0, 15.5, '#f4dede', 'Earliest JWST era'),
    (10.0, 14.0, '#e8f0fa', 'Macro-Knot seeds'),
    (6.0, 10.0, '#e6f3e6', 'Little Red Dots'),
    (0.0, 6.0, '#eef3ff', 'SMBH assembly')
]:
    ax.axvspan(x0, x1, color=c, alpha=0.78, lw=0, zorder=0)
    ax.text((x0+x1)/2, 0.955, label, transform=ax.get_xaxis_transform(), ha='center', va='top', fontsize=11.0, color='0.25')

ax.plot(z_curve, m_curve, color='#8c2f2f', lw=2.9, zorder=3)
ax.scatter(z_pts, m_pts, s=34, color='#8c2f2f', zorder=5)

obs = {
    'MoM-z14': {'z': 14.44, 'zerr': 0.02, 'y': 2.0e5, 'yerr': 0.22e5, 'c':'#1f77b4', 'm':'o'},
    'UHZ-1': {'z': 10.073, 'zerr': 0.002, 'y': 1.0e6, 'yerr': 0.30e6, 'c':'#ff7f0e', 'm':'s'},
    'LRD sample': {'z': 8.0, 'zerr': 1.0, 'y': 1.4e6, 'yerr': 0.35e6, 'c':'#2ca02c', 'm':'D'},
    'GN-z11-like': {'z': 11.1, 'zerr': 0.2, 'y': 5.0e5, 'yerr': 2.0e5, 'c':'#9467bd', 'm':'^'}
}
for d in obs.values():
    ax.errorbar(d['z'], d['y'], xerr=d['zerr'], yerr=d['yerr'], fmt=d['m'], color=d['c'], ecolor='0.42', elinewidth=1.15, capsize=3, capthick=0.95, markersize=6.2, zorder=6)

ax.annotate('Macro-Knot seed', xy=(14.44, 2.0e5), xytext=(13.45, 7.0e5), arrowprops=dict(arrowstyle='-', color='0.35', lw=0.9), fontsize=10.3, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='0.35', lw=0.8), zorder=7)
ax.annotate('UHZ-1', xy=(10.073, 1.0e6), xytext=(11.0, 3.3e6), arrowprops=dict(arrowstyle='-', color='0.35', lw=0.9), fontsize=10.3, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='0.35', lw=0.8), zorder=7)
ax.annotate('GN-z11-like', xy=(11.1, 5.0e5), xytext=(12.2, 1.3e6), arrowprops=dict(arrowstyle='-', color='0.35', lw=0.9), fontsize=10.1, bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='0.35', lw=0.8), zorder=7)

ax.set_yscale('log')
ax.set_xlim(15.5, 0.0)
ax.set_ylim(8e4, 1e9)
ax.set_xlabel('Redshift $z$  (decreases toward the present)', fontsize=13)
ax.set_ylabel(r'Central mass [$M_\odot$] (log)', fontsize=13)
ax.set_title('Illustrative growth of a primordial compact seed (JWST survey anchors)', fontsize=16, pad=12)
ax.grid(True, which='major', color='0.86', lw=0.75)
ax.grid(True, which='minor', color='0.93', lw=0.5)
ax.tick_params(labelsize=11)

legend_elements = [
    Line2D([0],[0], marker='o', color='w', label='Schematic track', markerfacecolor='#8c2f2f', markersize=7.5),
    Line2D([0],[0], marker='o', color='w', label='MoM-z14', markerfacecolor='#1f77b4', markersize=7.5),
    Line2D([0],[0], marker='s', color='w', label='UHZ-1', markerfacecolor='#ff7f0e', markersize=7.5),
    Line2D([0],[0], marker='D', color='w', label='LRD sample', markerfacecolor='#2ca02c', markersize=7.5),
    Line2D([0],[0], marker='^', color='w', label='GN-z11-like', markerfacecolor='#9467bd', markersize=7.5)
]
ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=True, framealpha=1.0, facecolor='white', edgecolor='0.8', fontsize=10.0)

plt.tight_layout()
out='fig_MacroKnot_LRD_SMBH_time.py'
plt.savefig('fig_MacroKnot_LRD_SMBH_time.png', dpi=220, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close(fig)
