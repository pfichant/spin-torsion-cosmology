import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

w0_ecf, wa_ecf = -0.904, -0.153
w0_cpl, wa_cpl = -0.70,  -1.10

def X_of_z(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return np.exp(3.0 * wa * (a - 1.0)) * (1.0 + z)**(3.0*(1.0+w0+wa))

z    = np.linspace(0, 3.5, 500)
X_lo = X_of_z(z, w0_cpl-0.08, wa_cpl-0.32)
X_up = X_of_z(z, w0_cpl+0.08, wa_cpl+0.32)

fig, ax = plt.subplots(figsize=(8, 5.2))
ax.fill_between(z, X_lo, X_up, alpha=0.20, color='steelblue')
ax.plot(z, X_of_z(z, w0_cpl, wa_cpl), '--', color='steelblue', lw=1.6)
ax.plot(z, np.ones_like(z), 'k--', lw=1.8)
ax.plot(z, X_of_z(z, w0_ecf, wa_ecf), color='crimson', lw=2.2)
ax.axhline(1.0, color='gray', lw=0.5, ls=':')
ax.set(xlim=(0, 3.5), ylim=(0.45, 2.8),
       xlabel='Redshift $z$',
       ylabel=r'$X(z)=\rho_{\rm DE}(z)\,/\,\rho_{\rm DE,0}$',
       title='Absolute dark energy density: ECF torsion vs. DESI DR1/DR2')
ax.grid(alpha=0.20, ls=':')

leg = [
    mpatches.Patch(fc='steelblue', alpha=0.35, label='DESI DR1/DR2 68% C.L.'),
    plt.Line2D([], [], color='steelblue', ls='--', lw=1.5,
               label=r'DESI CPL ($w_0=-0.70$, $w_a=-1.10$)'),
    plt.Line2D([], [], color='k', ls='--', lw=1.8,
               label=r'$\Lambda$CDM  ($X\equiv 1$)'),
    plt.Line2D([], [], color='crimson', lw=2.2,
               label=r'ECF torsion ($w_0=-0.904$, $w_a=-0.153$, 0 param.)'),
]
ax.legend(handles=leg, fontsize=8.5, loc='upper center',
          bbox_to_anchor=(0.5, -0.16), ncol=2, framealpha=0.95)
fig.subplots_adjust(bottom=0.25)
fig.savefig('Fig_RhoDEAbsolute.png', dpi=200, bbox_inches='tight')
print("Saved: Fig_RhoDEAbsolute.png")