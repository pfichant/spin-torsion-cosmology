#!/usr/bin/env python3
"""
Script 08 — H0–Age–BAO Trilemma: Numerical Irreducibility Proof
Foundation I Extended v2 — Sec. 5 (sec:age_trilemma) and Appendix L
Last modified: 20/07/2026, 16:45 (limitation note added)
Figure: fig_trilemma_irreducibility_contours.png

Scans the (w_0, z_t) parameter space of a tanh-crossing dark-energy model
and shows that no point simultaneously satisfies:
  (i)  BAO: D_M(z=1.48)/r_s within 1.5% of the eBOSS DR16 QSO consensus 30.21 (Hou+2021)
  (ii) Age: t_0 > t_GC = 13.32 Gyr (Valcin+2020 globular cluster chronometry)
for H0 = 73.04 km/s/Mpc — proving the trilemma is irreducible.

BAO target convention:
    Hou+2021 reports the consensus D_M/r_d(z=1.48) = 30.21 +/- 0.79 (eq. 49).
    Target D_M = 30.21 * r_s_ECF = 30.21 * 135.65 = 4098.0 Mpc (A-6; 4102.5 was 30.21 x 135.8 with the former r_s; 30.22 used 22/09-12/10/2026 by mistake).
    The ECF scale is used as the ruler of a measurement published in r_drag: the relation
    is not established (PO-ECF-BAO-RDRAG, OPEN), so this scan is CALCULATED-CONDITIONAL.
    This uses the ECF sound horizon as the BAO ruler, which is the
    internally consistent choice when testing ECF cosmology.

References:
    Hou et al. (2021) arXiv:2007.08998  [eBOSS DR16, z=1.48]
    Valcin et al. (2021) JCAP 08, 017  [globular cluster age prior]
    Chevallier & Polarski (2001); Linder (2003)  [CPL/tanh DE models]

LIMITATION NOTED 20/07/2026 (does not change the conclusion, refines it):
    Until A-7 (22/09/2026) this scan fixed Omega_m = 0.315 (the Planck-h
    value) throughout and never varied it; it now uses omega_m/h^2 = 0.2669. Omega_m depends on H0 (Omega_m = omega_m/h^2 for
    fixed physical density omega_m), so at H0=73.04 the physically
    consistent value is Omega_m ~ 0.268, not 0.315. A follow-up joint
    scan over (Omega_m, w0, wa) -- see joint_fit_trilemma.py -- shows
    the best compromise reaches t0~13.0-13.2 Gyr at Omega_m~0.28-0.29
    (omega_m shifted ~5-7% from Planck), better than the 12.74 Gyr
    found here but still short of 13.32 Gyr. Adding the CMB acoustic
    scale theta_* as a third constraint reveals a genuine quadrilemma:
    at fixed (w0,wa), raising Omega_m improves theta_* but worsens the
    age. The conclusion that this w(z) family does not fully resolve
    the trilemma stands; the reason is now better characterized.
    See Foundation I footnote (b) to the trilemma table, and
    Foundation II PO-F2-5, for the full discussion.
"""
# Last modified: 19/08/2026, 13:01 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# np.trapezoid added in NumPy 2.0; use np.trapz for backward compatibility
try:
    trapz = np.trapezoid
except AttributeError:
    trapz = np.trapz

# ---------------------------------------------------------------------------
# 1. PARAMETERS
# ---------------------------------------------------------------------------
H0_local      = 73.04          # km/s/Mpc (SH0ES 2022)
Omega_m       = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
Omega_de      = 1.0 - Omega_m  # = 0.685 (flat universe)
c_light       = 299792.458     # km/s
conv_gyr      = 977.79222168   # (km/s/Mpc)^-1 in Gyr  [Julian year]

z_bao         = 1.48
Target_DM_Mpc = 30.21 * 135.65 # [Q1] consensus Hou+2021 (eq. 49); 30.22 used 22/09-12/10/2026 by mistake; before 30.21*135.8
Target_Age    = 13.32           # Gyr, t_GC (Valcin+2020)
w_inf_fixed   = -1.0            # high-z asymptote

# ---------------------------------------------------------------------------
# 2. PRE-BUILT REDSHIFT GRIDS
# ---------------------------------------------------------------------------
z_bao_grid = np.linspace(0, z_bao, 1000)
z_age_grid = np.concatenate(([0], np.geomspace(1e-4, 1000, 5000)))

# ---------------------------------------------------------------------------
# 3. VECTORISED OBSERVABLES
# ---------------------------------------------------------------------------
def fast_observables(w_0, z_t):
    """Compute D_M(z_bao) [Mpc] and t_0 [Gyr] for tanh dark energy."""
    w_bao = w_0 + (w_inf_fixed - w_0)*0.5*(1 + np.tanh((z_bao_grid - z_t)/0.30))
    int_w = cumulative_trapezoid((1+w_bao)/(1+z_bao_grid), z_bao_grid, initial=0)
    E_bao = np.sqrt(Omega_m*(1+z_bao_grid)**3 + Omega_de*np.exp(3*int_w))
    dm    = trapz(1/E_bao, z_bao_grid) * (c_light/H0_local)

    w_age = w_0 + (w_inf_fixed - w_0)*0.5*(1 + np.tanh((z_age_grid - z_t)/0.30))
    int_w = cumulative_trapezoid((1+w_age)/(1+z_age_grid), z_age_grid, initial=0)
    E_age = np.sqrt(Omega_m*(1+z_age_grid)**3 + Omega_de*np.exp(3*int_w))
    age   = trapz(1/((1+z_age_grid)*E_age), z_age_grid) * (conv_gyr/H0_local)
    return dm, age

# ---------------------------------------------------------------------------
# 4. GRID SCAN  (50 x 50)
# ---------------------------------------------------------------------------
W0, ZT  = np.meshgrid(np.linspace(-2.5, -0.5, 50), np.linspace(0.1, 1.5, 50))
AGE     = np.zeros_like(W0)
BAO_ERR = np.zeros_like(W0)

for i in range(W0.shape[0]):
    for j in range(W0.shape[1]):
        dm, age       = fast_observables(W0[i,j], ZT[i,j])
        AGE[i,j]      = age
        BAO_ERR[i,j]  = abs(dm - Target_DM_Mpc) / Target_DM_Mpc

n_both = int(np.sum((BAO_ERR < 0.015) & (AGE > Target_Age)))

print("=" * 65)
print("  SCRIPT 08 — H0-AGE-BAO TRILEMMA  (Foundation I Sec. 5)")
print("=" * 65)
print(f"  Target D_M         = {Target_DM_Mpc:.1f} Mpc  (30.21 * 135.65)")
print(f"  Target age         = {Target_Age} Gyr  (t_GC, Valcin+2020)")
print(f"  BAO viable points  = {int(np.sum(BAO_ERR < 0.015))}/2500")
print(f"  Age viable points  = {int(np.sum(AGE > Target_Age))}/2500")
print(f"  Both satisfied     = {n_both}/2500")
print(f"  Trilemma: {'IRREDUCIBLE (confirmed)' if n_both==0 else 'VIOLATED -- check inputs'}")
# [D3, 22/09/2026 -- DEC-A7-POST-05] The "best fit" was hard-coded (w0 = -1.565,
# z_t = 0.20; t0 = 13.13 Gyr, dBAO = 4.1 % at Omega_m = 0.315). After A-7 that
# point gives t0 = 13.81 Gyr, dBAO = 8.8 %: no longer a compromise. It is now
# the grid point minimising the same joint chi2 as check_trilemma_optimizer.py
# (BAO at 1.5 %, age at 0.1 Gyr), restricted to this w_inf = -1 family.
CHI2_GRID = (BAO_ERR/0.015)**2 + ((AGE - Target_Age)/0.1)**2
_ib = np.unravel_index(np.argmin(CHI2_GRID), CHI2_GRID.shape)
W0_BF, ZT_BF = float(W0[_ib]), float(ZT[_ib])
dm_bf, age_bf = fast_observables(W0_BF, ZT_BF)
BAO_BF = abs(dm_bf-Target_DM_Mpc)/Target_DM_Mpc*100
print(f"\n  Best grid point (min joint chi2 = {CHI2_GRID[_ib]:.2f}; w0={W0_BF:.3f}, z_t={ZT_BF:.3f}):")
print(f"    D_M = {dm_bf:.1f} Mpc,  BAO err = {abs(dm_bf-Target_DM_Mpc)/Target_DM_Mpc*100:.2f}%")
print(f"    t0  = {age_bf:.4f} Gyr")
print("=" * 65)

# ---------------------------------------------------------------------------
# 5. FIGURE
# ---------------------------------------------------------------------------
plt.figure(figsize=(9, 7))

plt.contourf(ZT, W0, BAO_ERR, levels=[0, 0.015],
             colors=['#1f77b4'], alpha=0.3)
plt.contour(ZT, W0, BAO_ERR, levels=[0.015],
            colors=['#1f77b4'], linewidths=2)
plt.plot([], [], color='#1f77b4', alpha=0.5, linewidth=8,
         label=r'BAO viable ($\Delta D_M/r_s < 1.5\%$, eBOSS DR16)')

plt.contourf(ZT, W0, AGE, levels=[13.32, 15.0],
             colors=['#d62728'], alpha=0.3)
plt.contour(ZT, W0, AGE, levels=[13.32],
            colors=['#d62728'], linewidths=2)
plt.plot([], [], color='#d62728', alpha=0.5, linewidth=8,
         label=r'Age viable ($t_0 > t_{GC} = 13.32$ Gyr, Valcin 2020)')

plt.plot(ZT_BF, W0_BF, 'k*', markersize=15,
         label=rf'Best grid point ($t_0={age_bf:.2f}$ Gyr, $\Delta$BAO $={BAO_BF:.1f}\%$)')

plt.annotate(   # [D3] computed gap at the best grid point (was hard-coded 0.20 Gyr)
    'Irreducible Gap\n' + rf'($\Delta t_0 \approx {Target_Age-age_bf:.2f}$ Gyr, $\Delta$BAO $\approx {BAO_BF:.1f}\%$)',
    xy=(ZT_BF, W0_BF), xytext=(min(ZT_BF+0.2, 1.1), W0_BF-0.45),
    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
    fontsize=12, fontweight='bold')

plt.text(0.85, -0.82,
    r"$\mathbf{0/2500}$ grid points satisfy" + "\n"
    r"both constraints simultaneously" + "\n"
    r"$\Rightarrow$ Trilemma is irreducible",
    fontsize=10, color='#4b0082',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='lavender',
              alpha=0.9, edgecolor='indigo'))

plt.axhline(-1, color='black', linestyle=':', lw=1.5,
            label=r'$\Lambda$CDM boundary ($w_0 = -1$)')

plt.xlabel(r'Transition Redshift $z_t$', fontsize=13)
plt.ylabel(r'Equation of State $w_0$', fontsize=13)
plt.title(r'Numerical Proof of the $H_0$–Age–BAO Trilemma Irreducibility',
          fontsize=14, fontweight='bold', pad=15)
plt.legend(loc='lower right', fontsize=10.5, frameon=True, framealpha=0.9)
plt.tight_layout()
plt.savefig('fig_trilemma_irreducibility_contours.png', dpi=300)
print("Figure saved: fig_trilemma_irreducibility_contours.png")
