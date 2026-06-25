
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse

def mk_ellipse(center, sw0, swa, rho, scale, color, alpha, ls='-'):
    cov = np.array([[sw0**2, rho*sw0*swa], [rho*sw0*swa, swa**2]])
    vals, vecs = np.linalg.eigh(cov)
    idx = vals.argsort()[::-1]; vals = vals[idx]; vecs = vecs[:, idx]
    ang = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    return Ellipse(center, 2*scale*np.sqrt(vals[0]), 2*scale*np.sqrt(vals[1]),
                   angle=ang, fc=color, alpha=alpha, ec=color, lw=1.6, ls=ls)

c1=(-0.72,-0.50); s1=(0.17,0.51); r1=-0.55   # DR1
c2=(-0.75,-0.65); s2=(0.14,0.42); r2=-0.58   # DR2

fig, ax = plt.subplots(figsize=(7.5, 6.5))
for sc, al in [(2.0, 0.09), (1.0, 0.22)]:
    ax.add_patch(mk_ellipse(c1, *s1, r1, sc, 'steelblue', al, ls='--'))
for sc, al in [(2.0, 0.13), (1.0, 0.32)]:
    ax.add_patch(mk_ellipse(c2, *s2, r2, sc, 'royalblue', al))

ax.plot(-1.0, 0.0, 's', color='black',  ms=10, zorder=6)
ax.plot(-0.904, -0.153, '*', color='crimson', ms=18, zorder=7)
ax.annotate(r'$\Lambda$CDM', xy=(-1.0, 0.0), xytext=(-1.28, 0.28), fontsize=9.5,
            color='black', arrowprops=dict(arrowstyle='->', color='black', lw=0.9))
ax.annotate(r'ECF $(w_0, w_a)=(-0.904,-0.153)$' + '\n' + r'\textit{a priori prediction}',
            xy=(-0.904, -0.153), xytext=(-0.65, 0.15),
            fontsize=9.5, color='crimson',
            arrowprops=dict(arrowstyle='->', color='crimson', lw=0.9))
ax.axhline(0, color='gray', lw=0.5, ls=':')
ax.axvline(-1, color='gray', lw=0.5, ls=':')
ax.set(xlim=(-1.40, -0.35), ylim=(-1.75, 0.70),
       xlabel=r'$w_0$', ylabel=r'$w_a$',
       title=r'ECF vs. DESI DR1/DR2 in the $w_0$–$w_a$ plane')
ax.grid(alpha=0.18, ls=':')

leg = [
    mpatches.Patch(fc='steelblue', alpha=0.45, ec='steelblue', ls='--',
                   label='DESI DR1 (68%, 95% C.L.)'),
    mpatches.Patch(fc='royalblue', alpha=0.55, ec='royalblue',
                   label='DESI DR2 (68%, 95% C.L.)'),
    plt.Line2D([], [], marker='s', color='w', mfc='black', ms=9,
               label=r'$\Lambda$CDM: $5.1\sigma$ DR1 / $4.9\sigma$ DR2'),
    plt.Line2D([], [], marker='*', color='w', mfc='crimson', ms=14,
               label=r'ECF prediction (a priori, 0 free param.)'),
]
ax.legend(handles=leg, fontsize=8.8, loc='upper center',
          bbox_to_anchor=(0.5, -0.12), ncol=2, framealpha=0.95)
fig.subplots_adjust(bottom=0.22)
fig.text(0.5, 0.01,
         "Distances from DESI published central values with diagonal errors only"
         " — see Foundation II §DESI scope note for full methodology.",
         ha='center', fontsize=7, style='italic', color='gray')
fig.savefig('Fig_w0wa_DESI_ECF.png', dpi=200, bbox_inches='tight')
print("Saved: Fig_w0wa_DESI_ECF.png")
