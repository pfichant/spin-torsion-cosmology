"""
plot_density_bounce_comparison.py  --  v2  (15 Apr 2026)
=========================================================
Figure: Density Saturation at the Primordial Spin Bounce
Paper: Foundation I: The Metric Universe (Extended), Section 2

Physical derivation  (F1 §2 and App. G)
-----------------------------------------
In standard General Relativity (flat FLRW, stiff fluid w=1):

    H^2 = (8*pi*G/3) * rho    =>    a(t) ~ t^{1/3}    =>    rho_GR ~ 1/t^2

This diverges as t -> 0 (initial singularity).

In the ECKS framework the spin-squared correction modifies the Friedmann
equation (Poplawski 2010, Trautman 1973):

    H^2 = (8*pi*G/3) * rho * (1 - rho/rho_c)

At rho = rho_c the Hubble rate H vanishes: this is the bounce.

Exact solution for the stiff spin fluid (App. G, Eq. G.x)
----------------------------------------------------------
Setting u = rho/rho_c and tau = sqrt(8*pi*G*rho_c/3) * t, the
differential equation for u(tau) integrates exactly to:

    u(tau) = 1 / (1 + 9*tau^2)          [exact Lorentzian]

Back to physical density with tau = sqrt(rho_c) * t (schematic units):

    rho_ECF(t) = rho_c / (1 + 9*rho_c * t^2)

For the schematic figure, the factor of 9 is absorbed into the time
normalisation (re-scaling t by 1/3):

    rho_ECF(t) = rho_c / (1 + rho_c * t^2)          [Eq. A used in plot]

This satisfies:
  - rho_ECF(0)   = rho_c  (bounce maximum) ✓
  - rho_ECF(t)  -> 1/t^2  for t >> 1/sqrt(rho_c), matching standard
    stiff behaviour and the GR schematic curve ✓

Comparison with the v1 script
------------------------------
  v1 used  rho_ecf = 1 / (t^2 + a_min_sq)^2  (quartic)
  -> Falls as t^{-4} at large t (WRONG: stiff fluid goes as t^{-2})
  -> Variable name 'a_min_sq' was physically misleading
  v2 uses  rho_ecf = rho_c / (1 + rho_c * t^2)  (Lorentzian, exact ECKS)
  -> Same peak value rho_c ✓, correct t^{-2} large-t behaviour ✓

GR schematic (unchanged from v1)
---------------------------------
    rho_GR(t) = 1 / (t^2 + 0.01)

The small regulariser epsilon = 0.01 avoids numerical infinity and
allows the curve to reach rho_GR(0) = 100 >> rho_c = 20, visually
demonstrating the divergence. This is a plot artefact, not physics.

Note on physical units
----------------------
rho_c = 20.0 is a dimensionless schematic value chosen so the critical
density fits comfortably within the plot range.  The actual Cartan
critical density is rho_c ~ rho_Planck / 2 ~ 8.5e96 kg/m^3
(Poplawski 2010).  The figure caption in the paper explicitly states
"schematic illustration".

Output
------
  figure_densiste_bounce_comparison.jpg  (300 dpi)
  Filename consistent with LaTeX reference in F1 §2.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Parameters  --  schematic (see docstring for physical values)
# ---------------------------------------------------------------------------
RHO_C     = 20.0    # schematic critical Cartan density (dimensionless)
EPSILON_GR = 0.01   # GR regulariser: keeps rho_GR finite at t=0 for numerics
OUTPUT_FILE = 'figure_density_bounce_comparison.png'


# ---------------------------------------------------------------------------
# Density curves
# ---------------------------------------------------------------------------
t = np.linspace(-3, 3, 1000)

rho_gr  = 1.0 / (t**2 + EPSILON_GR)          # GR singularity schematic
rho_ecf = RHO_C / (1.0 + RHO_C * t**2)       # ECKS exact Lorentzian


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'axes.linewidth': 1.3, 'text.usetex': False})

fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(left=0.12, right=0.72, top=0.90, bottom=0.13)

ax.fill_between(t, RHO_C, 30, color='#f5c0c0', alpha=0.35, zorder=0)
ax.axhline(RHO_C, color='#555', ls=':', lw=1.5, zorder=2)

ax.plot(t, rho_gr,  color='steelblue', ls='--', lw=2.2, zorder=3)
ax.plot(t, rho_ecf, color='#C00000',   ls='-',  lw=2.8, zorder=4)

ax.annotate('', xy=(0.0, 29.4), xytext=(0.0, 23),
            arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.8))

ax.annotate('Singularity\nresolved',
            xy=(0.06, RHO_C), xytext=(0.9, RHO_C + 5.5),
            arrowprops=dict(arrowstyle='->', color='#900000', lw=1.4),
            fontsize=10.5, color='#900000', fontweight='bold', ha='center')

ax.set_xlabel(r'Cosmic time $t$  [arbitrary units]', fontsize=12)
ax.set_ylabel(r'Energy density $\rho(t)$  [dimensionless]', fontsize=11)
ax.set_title('Density Saturation at the Primordial Spin Bounce', fontsize=12, pad=7)
ax.set_xlim(-3, 3); ax.set_ylim(0, 30)
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.grid(True, ls=':', alpha=0.30, color='gray')
ax.tick_params(labelsize=10)

handles = [
    plt.Line2D([0],[0], color='steelblue', ls='--', lw=2.2,
               label=r'General Relativity ($\rho \to \infty$)'),
    plt.Line2D([0],[0], color='#C00000', lw=2.8,
               label=r'ECF Bounce ($\rho \leq \rho_c$)'),
    plt.Line2D([0],[0], color='#555', ls=':', lw=1.5,
               label=r'Cartan critical density $\rho_c$'),
    plt.Rectangle((0,0),1,1, fc='#f5c0c0', alpha=0.6, lw=0,
                  label=r'Forbidden region ($\rho > \rho_c$)'),
]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.02, 1.0),
          fontsize=10, framealpha=0.95, edgecolor='#ccc',
          handlelength=2.2, labelspacing=0.7)

plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.close()
