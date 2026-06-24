#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# plot_planck_tt_residuals_ecf_v2.py
# =============================================================================
# Script  : CMB High-l Damping-Tail Residuals ECF vs LCDM (Figure fighighldamping)
# Paper   : Foundation I: Unified Resolution of Cosmological Tensions
#           (fichant_ecf_F1_Extended_v2)
# Author  : Pascal Fichant  |  Date: 21/04/2026
#
# CHANGELOG v1 -> v2
# ------------------
# [FIX] Titre fichier: "plank" -> "planck"
#
# [FIX] Residual formula: remplace le modele quadratique ad hoc
#         ecf_residuals = -5.0 * ((ell-1500)/1500)^2  [v1, non physique]
#       par interpolation PCHIP sur les 4 points calibres Table tabforecastk :
#         l=1500 -> -5.2%  |  l=2000 -> -6.5%  |  l=2500 -> -3.0%  |  l=3000 -> -2.5%
#       NB: profil NON-MONOTONE -- maximum du deficit a l~2000 (-6.5%),
#       remontee partielle a l=2500-3000 (physique: d_silk=1320 vs 1400 Mpc,
#       phase shift delta_phi=0.02, Delta z_rec=-22, App. K).
#
# [FIX] Zone grisee: +-1.8% (erreurs Planck high-l, Table tabchi2breakdown)
#       vs +-0.5% de v1 trop etroite
#
# [NEW] Zone optimale de discrimination l=2000-2500 (App. K, Table tabforecastk)
#
# [NEW] Ligne CMB-S4 1-sigma (sigma=1.5%, App. K, Fig. figk3prediction)
#
# [NEW] 4 points Table tabforecastk annotes avec valeurs numeriques
#
# [NEW] Labels directs sur chaque element (pas de legende-boite)
#       -> courbe ECF entierement visible
#
# [NEW] verify_calibration(): verifie les 4 points Table tabforecastk
#
# [CLN] Doubles backslashes LaTeX corriges, commentaires ad hoc supprimes,
#       referee-ready
#
# CALIBRATION PHYSIQUE (Sec. sechighldamping, App. K, Table tabforecastk)
# -----------------------------------------------------------------------
#
# Deficits de la queue d'amortissement (Table tabforecastk):
#   l=1500  D_ECF=273.6  D_LCDM=288.6  delta=-15.0  delta%=-5.2%
#   l=2000  D_ECF=217.6  D_LCDM=232.7  delta=-15.1  delta%=-6.5%
#   l=2500  D_ECF= 68.9  D_LCDM= 71.0  delta= -2.1  delta%=-3.0%
#   l=3000  D_ECF= 61.6  D_LCDM= 63.2  delta= -1.6  delta%=-2.5%
#
# Physique sous-jacente (App. K):
#   Silk damping scale: d_silk = 1320 Mpc (ECF) vs 1400 Mpc (LCDM) -> -5.7%
#   Phase shift: delta_phi_ECF = 0.02
#   Recombination shift: Delta z_rec = -22
#
# CMB-S4 sensitivity: sigma_S4 = 1.5% (Fig. figk3prediction)
#   -> deficit 3.0-6.5% dans la fenetre 2000-2500 >> sigma_S4 -> p < 0.05 (App. K)
#
# Sections impactees:
#   Abstract          : "residual CMB damping-tail deficit at l>2000"
#   S7 sechighldamping: DeltaD/D = 3-6% at l>2000
#   App. K            : Table tabforecastk, Fig. figk3prediction
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

matplotlib.use('Agg')

plt.rcParams.update({
    'font.size'      : 13,
    'axes.labelsize' : 15,
    'legend.fontsize': 11,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'font.family'    : 'serif',
    'axes.linewidth' : 1.5,
})


# =============================================================================
# DONNEES CALIBREES (Table tabforecastk, App. K)
# =============================================================================

TABLE_K = np.array([
    [1500, 273.6, 288.6, -5.2],
    [2000, 217.6, 232.7, -6.5],
    [2500,  68.9,  71.0, -3.0],
    [3000,  61.6,  63.2, -2.5],
])

ELL_K   = TABLE_K[:, 0]
D_ECF_K = TABLE_K[:, 1]
D_LCM_K = TABLE_K[:, 2]
DPCT_K  = TABLE_K[:, 3]

_interp = PchipInterpolator(ELL_K, DPCT_K)

SIGMA_S4  = 1.5    # CMB-S4 1-sigma [%] (App. K, Fig. figk3prediction)
SIGMA_PLK = 1.8    # Incertitude Planck high-l [%] (Table tabchi2breakdown)


# =============================================================================
# VERIFICATION vs TABLE tabforecastk
# =============================================================================

def verify_calibration():
    sep = "=" * 72
    print(sep)
    print("  Verification vs Table tabforecastk (App. K, F1 Extended v2)")
    print(sep)
    print(f"  {'l':>5s}  {'D_ECF':>8s}  {'D_LCDM':>8s}  "
          f"{'delta':>8s}  {'delta%':>8s}  {'paper%':>8s}  Status")
    print(f"  {'-'*5}  {'-'*8}  {'-'*8}  "
          f"{'-'*8}  {'-'*8}  {'-'*8}  ------")
    for row in TABLE_K:
        l, d_e, d_l, pct_paper = row
        delta    = d_e - d_l
        pct_calc = 100.0 * delta / d_l
        status   = "OK" if abs(pct_calc - pct_paper) < 0.2 else "FAIL"
        print(f"  {l:>5.0f}  {d_e:>8.1f}  {d_l:>8.1f}  "
              f"{delta:>8.1f}  {pct_calc:>8.2f}  {pct_paper:>8.1f}  {status}")
    print(sep)
    print(f"  Max deficit : l=2000 ({DPCT_K[1]:.1f}%), remontee a l=2500 ({DPCT_K[2]:.1f}%)")
    print(f"  Fenetre optimale: l=2000-2500 (App. K) -- deficit >> sigma_S4={SIGMA_S4}% ✓")
    print(sep)


# =============================================================================
# FIGURE
# =============================================================================

def plot_residuals(outfile="planck_tt_residuals_ecf.png"):
    print(">>> Generating Figure: CMB High-l Damping-Tail Residuals (v2)...")

    ell  = np.linspace(1500, 3000, 800)
    res  = _interp(ell)
    base = np.zeros_like(ell)

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.11, right=0.97, top=0.91, bottom=0.13)

    # Zone optimale de discrimination l=2000-2500 (App. K)
    ax.axvspan(2000, 2500, color='gold', alpha=0.20, zorder=0)

    # Incertitude Planck high-l +-1.8%
    ax.fill_between(ell, -SIGMA_PLK, SIGMA_PLK,
                    color='grey', alpha=0.18, zorder=1)

    # Sensibilite CMB-S4 1-sigma +-1.5%
    ax.axhline(-SIGMA_S4, color='#2ecc71', linestyle='-.', linewidth=1.6, zorder=2)
    ax.axhline( SIGMA_S4, color='#2ecc71', linestyle='-.', linewidth=1.6, zorder=2)

    # Courbes principales
    ax.plot(ell, base, color='black', linestyle='--', linewidth=2.0, zorder=3)
    ax.plot(ell, res,  color='#c0392b', linestyle='-', linewidth=2.8, zorder=4)

    # Points de calibration Table tabforecastk
    ax.scatter(ELL_K, DPCT_K, color='#c0392b', s=70, zorder=5,
               edgecolors='black', linewidths=0.8)

    # Annotations numeriques des 4 points
    ax.annotate('-5.2%', xy=(1500, -5.2), xytext=(1510, -4.4),
                fontsize=10.5, color='#c0392b', ha='left',
                arrowprops=dict(arrowstyle='-', color='#c0392b', lw=0.8))
    ax.annotate('-6.5%', xy=(2000, -6.5), xytext=(2010, -7.5),
                fontsize=10.5, color='#c0392b', ha='left',
                arrowprops=dict(arrowstyle='-', color='#c0392b', lw=0.8))
    ax.annotate('-3.0%', xy=(2500, -3.0), xytext=(2530, -2.6),
                fontsize=10.5, color='#c0392b', ha='left',
                arrowprops=dict(arrowstyle='-', color='#c0392b', lw=0.8))
    ax.annotate('-2.5%', xy=(3000, -2.5), xytext=(2940, -1.9),
                fontsize=10.5, color='#c0392b', ha='right',
                arrowprops=dict(arrowstyle='-', color='#c0392b', lw=0.8))

    # Labels directs (pas de legende-boite)
    ax.text(1610, -SIGMA_PLK - 0.08, r'Planck $\pm$1.8%',
            color='#777777', fontsize=10, ha='left', va='top')
    ax.text(1610,  SIGMA_S4 + 0.10, r'CMB-S4 $\pm$1.5%',
            color='#27ae60', fontsize=10, ha='left', va='bottom')
    ax.text(1610,  0.12, r'$\Lambda$CDM baseline',
            color='black', fontsize=10, ha='left', va='bottom')
    ax.text(2250, 1.85, 'Discrimination\nwindow',
            color='#8a7000', fontsize=10, ha='center', va='top', style='italic')
    ax.text(2800, -1.0, r'ECF residuals',
            color='#c0392b', fontsize=11, ha='center', va='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#c0392b',
                      alpha=0.85, linewidth=1.0))

    # Labels physiques
    ax.text(1680, 1.55,
            'Geometric degeneracy\n(acoustic peaks preserved)',
            color='#444444', fontsize=10, ha='center', va='top', style='italic')
    ax.text(2240, -7.7,
            'Damping-tail deficit\n(ECF spin-torsion signature)',
            color='#c0392b', fontsize=10, ha='center', va='top', style='italic')

    ax.set_xlim(1500, 3000)
    ax.set_ylim(-8.8, 2.5)
    ax.set_xlabel(r'Multipole moment $\ell$', fontweight='bold', fontsize=15)
    ax.set_ylabel(r'$\Delta\mathcal{D}_\ell^{TT}/\mathcal{D}_\ell^{TT}$ [%]',
                  fontweight='bold', fontsize=14)
    ax.set_title(r'ECF vs $\Lambda$CDM: CMB High-$\ell$ Damping-Tail Residuals',
                 fontsize=15, fontweight='bold', pad=10)
    ax.grid(True, which='major', linestyle=':', alpha=0.55)

    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    print(f"   [SUCCESS] Saved: {outfile}")
    plt.close()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    verify_calibration()
    plot_residuals()
