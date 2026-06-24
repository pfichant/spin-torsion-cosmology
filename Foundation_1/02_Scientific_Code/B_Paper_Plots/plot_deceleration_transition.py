"""
plot_deceleration_transition.py  --  v2  (15 Apr 2026)
=======================================================
Figure: Cosmic Deceleration--Acceleration Transition (Foundation I, Appendix G)
Author: Pascal Fichant

Physical derivation  (F1 Extended v2, Appendix G)
--------------------------------------------------
The general deceleration parameter in the ECF framework is (App. G, Eq.):

    q_ECF(z) = Omega_r(z) + (1/2) Omega_m(z) - Omega_Lambda(z) + 2 Omega_spin(z)

Because the spin density scales as rho_spin ~ a^{-6}, its present-day
fraction is Omega_spin,0 ~ 10^{-60} (calibrated ECF solution, Table 1).
The spin term at the maximum plotted redshift:

    2 * Omega_spin(z=2.5) = 2 * Omega_spin,0 * (1+2.5)^6 / E^2(2.5)
                          ~ 2 * 1e-60 * 1838 ~ 4e-57  (negligible)

Consequently, for z < 10^8:

    q_ECF(z) ≈ (1/2) Omega_m(z) - Omega_Lambda(z)  =  q_LCDM(z)

The paper caption (Fig. App. G) explicitly states:
    "the red curve closely overlaps the Lambda-CDM reference curve (blue
     dashed) for z < 2, illustrating that the spin-torsion contribution
     is effectively confined to the early Universe."

Transition redshift (analytical formula, App. G)
-------------------------------------------------
Setting q(z_t) = 0:

    (1/2) Omega_m0 (1+z_t)^3 = Omega_Lambda0
    => z_t = (2 * Omega_Lambda0 / Omega_m0)^(1/3) - 1

With Omega_m0 = 0.315, Omega_Lambda0 = 0.685 (Planck 2018):
    z_t = (2 * 0.685 / 0.315)^(1/3) - 1 = (4.349)^(1/3) - 1 = 0.6323

Note: The paper text states "approximately z_t ~ 0.64"; the analytical
value is 0.63 -- a rounding difference of 0.008, not a numerical error.

Present-day deceleration:
    q_0 = (1/2) * 0.315 - 0.685 = -0.5275   (standard: ~ -0.53)

Inputs matched to F1 Extended v2
---------------------------------
  Om0             = 0.315     Planck 2018, flat universe
  OL0             = 0.685     = 1 - Om0
  OMEGA_SPIN_0    = 1e-60     present-day spin fraction (App. G)

Output
------
  figure_deceleration_transition.png  (300 dpi)
  Filename consistent with LaTeX reference in F1 Extended v2 (Appendix G).
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Parameters  --  all values anchored to F1 Extended v2
# ---------------------------------------------------------------------------
Om0           = 0.315    # Planck 2018 matter density fraction
OL0           = 1.0 - Om0   # Cosmological constant fraction (flat universe)
OMEGA_SPIN_0  = 1e-60    # Present-day spin density fraction (App. G)

OUTPUT_FILE   = 'figure_deceleration_transition.png'


# ---------------------------------------------------------------------------
# Redshift grid and density fractions
# ---------------------------------------------------------------------------
z      = np.linspace(0, 2.5, 1000)
E2     = Om0 * (1 + z)**3 + OL0   # (H/H0)^2 for flat LCDM, negligible radiation

Om_z   = Om0 * (1 + z)**3 / E2
OL_z   = OL0 / E2
Ospin_z = OMEGA_SPIN_0 * (1 + z)**6 / E2   # ~ 4e-57 at z=2.5: negligible


# ---------------------------------------------------------------------------
# Deceleration parameter
# ---------------------------------------------------------------------------
q_lcdm = 0.5 * Om_z  -  OL_z
q_ecf  = 0.5 * Om_z  -  OL_z  +  2 * Ospin_z   # numerically indistinguishable from q_lcdm

z_t    = (2 * OL0 / Om0)**(1/3) - 1    # analytical transition: 0.6323
q0     = 0.5 * Om0 - OL0               # present-day value: -0.5275


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'axes.linewidth': 1.2})

fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.13)

ax.fill_between(z,  0,  1,  color='#d8d8d8', alpha=0.35, zorder=0)
ax.fill_between(z, -1,  0,  color='#b8d4f0', alpha=0.30, zorder=0)
ax.axhline(0, color='black', ls=':', lw=1.0, zorder=1)

ax.plot(z, q_lcdm, color='steelblue', ls='--', lw=2.2, zorder=3,
        label=r'$\Lambda$CDM  ($\Omega_m=0.315$)')
ax.plot(z, q_ecf,  color='#C00000',   ls='-',  lw=3.0, alpha=0.65, zorder=2,
        label=r'ECF  [$2\Omega_{\rm spin}(z)\lesssim10^{-57}$]')

ax.scatter([z_t], [0], color='black', s=55, zorder=5)
ax.annotate(rf'$z_t = {z_t:.2f}$', xy=(z_t, 0),
            xytext=(z_t + 0.18, 0.32),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.1),
            fontsize=11, fontweight='bold')

ax.scatter([0], [q0], s=30, color='#900000', zorder=5)
ax.text(0.06, q0 - 0.12, rf'$q_0 = {q0:.3f}$', color='#900000', fontsize=10)

ax.text(0.18,  0.80, r'Decelerating ($q>0$)', color='#444', fontsize=9.5)
ax.text(0.18, -0.85, r'Accelerating ($q<0$)', color='#1a5999', fontsize=9.5)

ax.text(1.50, -0.68,
        r'$q(z)=\frac{1}{2}\Omega_m(z)-\Omega_\Lambda(z)$',
        fontsize=11.5, color='#222', va='center',
        bbox=dict(facecolor='white', edgecolor='#777',
                  boxstyle='round,pad=0.38', alpha=0.95))

ax.text(1.50, -0.40, 'Pantheon+ compatible\n(Scolnic et al. 2022)',
        color='#1a7a40', fontsize=9.0, ha='center',
        bbox=dict(facecolor='white', edgecolor='#1a7a40',
                  boxstyle='round,pad=0.30', alpha=0.92))

ax.set_xlabel(r'Redshift $z$', fontsize=13)
ax.set_ylabel(r'Deceleration parameter $q(z)$', fontsize=13)
ax.set_xlim(0, 2.5)
ax.set_ylim(-1.0, 1.0)
ax.grid(True, ls=':', alpha=0.30, color='gray')
ax.tick_params(labelsize=11)
ax.legend(loc='upper right', fontsize=10, framealpha=0.93,
          edgecolor='#ccc', handlelength=2.2)
ax.set_title(r'Cosmic Deceleration--Acceleration Transition (Appendix G)',
             fontsize=12, pad=8)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()
