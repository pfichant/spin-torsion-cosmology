"""
plot_desi_prediction.py  --  v2  (15 Apr 2026)
===============================================
Figure: Dark Energy Dynamics -- ECF Prediction vs DESI DR1
Paper: Foundation I: The Metric Universe (Extended), Section 6

Physical derivation  (F1 Appendix B)
--------------------------------------
From the Topological Invariance Principle (TIP, rho_DE(a) = 1 - rho_torsion(a))
and the continuity equation, the effective ECF equation of state is:

    w(a) = -1 - (1/3) d(ln rho_DE)/d(ln a)

Taylor-expanding around a=1 (z=0) and calibrating alpha_torsion=0.151 to
DESI DR1 BAO contours yields the CPL parameters (App. B, Eq. B.x):

    w0 = -0.904,   wa = -0.153

so that  w(z) = w0 + wa * z/(1+z)  [Chevallier-Polarski-Linder parametrization]

This places the ECF trajectory in the region broadly compatible with DESI DR1
(arXiv 2404.03002) while remaining close to w = -1 for z < 1.

DESI DR1 reference values (DESI+CMB, arXiv 2404.03002, Table 3)
----------------------------------------------------------------
    w0_DESI = -0.827 +/- 0.060
    wa_DESI = -0.75  +/- 0.29
    rho(w0, wa) = -0.95  (correlation coefficient)

The 1-sigma band is propagated from the published covariance:
    sigma^2(z) = sigma^2(w0) + [z/(1+z)]^2 sigma^2(wa)
               + 2 rho [z/(1+z)] sigma(w0) sigma(wa)

Output
------
    Figure_DESI_Prediction.png  (300 dpi)
    Filename consistent with LaTeX reference in F1 Section 6.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# ---------------------------------------------------------------------------
# Parameters  --  from paper Appendix B and DESI DR1 (arXiv 2404.03002)
# ---------------------------------------------------------------------------
W0_ECF, WA_ECF     = -0.904, -0.153   # App. B, calibrated via alpha_torsion=0.151
W0_DESI, WA_DESI   = -0.827, -0.75    # DESI DR1 + CMB, Table 3
SIG_W0, SIG_WA     = 0.060, 0.29      # 68% marginals, DESI+CMB
RHO_W0_WA          = -0.95            # correlation coefficient (DESI+CMB)
OUTPUT_FILE = 'Figure_DESI_Prediction.png'


# ---------------------------------------------------------------------------
# Curves
# ---------------------------------------------------------------------------
z = np.linspace(0, 1.6, 400)
a = z / (1 + z)                        # CPL pivot variable

w_ecf  = W0_ECF  + WA_ECF  * a        # ECF CPL trajectory
w_desi = W0_DESI + WA_DESI * a        # DESI DR1 best-fit CPL
w_lcdm = np.full_like(z, -1.0)        # LCDM reference

# 1-sigma band from DESI covariance
var_band = (SIG_W0**2
            + a**2 * SIG_WA**2
            + 2 * RHO_W0_WA * a * SIG_W0 * SIG_WA)
sigma = np.sqrt(np.abs(var_band))


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 11,
                     'axes.linewidth': 1.3, 'text.usetex': False})

fig, ax = plt.subplots(figsize=(9, 5.5))
fig.subplots_adjust(left=0.12, right=0.68, top=0.90, bottom=0.13)

ax.fill_between(z, w_desi - sigma, w_desi + sigma,
                color='#999', alpha=0.22)
ax.plot(z, w_desi, color='#777', ls='--', lw=1.8)
ax.plot(z, w_ecf,  color='#C00000', lw=2.8, zorder=4)
ax.plot(z, w_lcdm, color='steelblue', ls=':', lw=2.0, zorder=3)
ax.axhline(-1.0, color='steelblue', ls=':', lw=0.9, alpha=0.25)

ax.set_xlabel('Redshift $z$', fontsize=12)
ax.set_ylabel(r'Equation of state $w(z)$', fontsize=11)
ax.set_title(r'Dark Energy Dynamics: ECF Prediction vs DESI DR1', fontsize=11, pad=6)
ax.set_xlim(0, 1.6)
ax.set_ylim(-1.4, -0.6)
ax.grid(True, ls=':', alpha=0.35, color='gray')
ax.tick_params(labelsize=10)

handles = [
    Patch(fc='#999', alpha=0.35, lw=0,
          label=r'DESI DR1+CMB  $1\sigma$  [2404.03002]'),
    plt.Line2D([0], [0], color='#777', ls='--', lw=1.8,
               label=rf'DESI best fit  ($w_0={W0_DESI}$, $w_a={WA_DESI}$)'),
    plt.Line2D([0], [0], color='#C00000', lw=2.8,
               label=rf'ECF  ($w_0={W0_ECF}$, $w_a={WA_ECF}$)'),
    plt.Line2D([0], [0], color='steelblue', ls=':', lw=2.0,
               label=r'$\Lambda$CDM  ($w=-1$)'),
]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.03, 1.0),
          fontsize=9.5, framealpha=0.95, edgecolor='#ccc',
          handlelength=2.0, labelspacing=0.9)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()