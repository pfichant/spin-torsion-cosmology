# Last modified: 21/08/2026, 16:05 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
# =============================================================================
# [18/08/2026] SCRIPT SUPERSEDED -- NOT PART OF THE F1 DEPOSIT
#
# This script plots H_ECF(z)/H_LCDM(z) and shows the intermediate minimum
# near z ~ 4360, which the Fig. 2 caption described while Fig. 2 itself
# plots the growth of perturbations. That mismatch was FIXED in the
# caption on 18/08/2026, which now states explicitly that the minimum
# lives in the H(z) ratio, "not plotted here". The point is therefore
# resolved in the text; adding a figure for it is not needed.
#
# Kept locally for provenance -- it is what revealed the mismatch.
# Its output is suffixed _SUPERSEDED so that it cannot overwrite a
# published figure if run by accident.
# =============================================================================
# plot_hubble_boost_ratio.py  —  v2 referee
# =============================================================================
# SCRIPT  : Pre-recombination Torsion Boost — H(z) ratio (Figure 3 / Fig. boost)
# Paper   : Foundation I (Extended v2)
# Author  : Pascal Fichant (2026)
# Section : Section 3 (Sound Horizon Reduction), cross-check: script01solvesoundhorizon.py
#
# INPUTS (F1 Table tabpriors, Section 3):
#   H0_LCDM = 67.4 km/s/Mpc           [Planck2020]
#   H0_ECF  = 73.04 km/s/Mpc          [F1 Section 5, best-fit]
#   Om      = 0.315 (LCDM) ; omega_m/h^2 = 0.2669 (ECF)   [A-7, 22/09/2026]
#   omega_r = 4.15e-5 (h^2 units)     [universal, T_CMB=2.725K]
#   Or_LCDM = omega_r / h_LCDM^2 = 9.135e-5   (h=0.674)
#   Or_ECF  = omega_r / h_ECF^2  = 7.779e-5   (h=0.7304)
#   Physical rho_r identical: Or*h^2 = 4.15e-5 in both models. ✓
#   z_ref   = 5600   (spin sector normalisation, solver anchor)
#   Omega_spin,peak = 0.093 (= spin_peak parameter, F1 Table tabpriors)
#   Os0 = 0.093 * Or_ECF * a_peak^2 = 1.286e-13   (today's spin density)
#   Closure: Ol_ECF = 1 - Om - Or_ECF - Os0 = 0.684922
#
# INDEPENDENT VERIFICATION (computed before plotting):
#   ratio(z=0)    = H0_ECF/H0_LCDM = 1.0837  ✓  (flat-universe closure verified)
#   ratio(z=1100) = 1.0649
#   ratio(z=5600) = see output  (spin/rad = 0.093 at z_ref by construction)
#   ratio(z_max)  = 1.921 at 1+z ~ 31623  (within ylim 1.98 ✓)
#                   [UPDATED 05/09/2026, I82: was 1.584 with the old
#                    z_peak=7500 anchor; the 5600 anchor raises Os0 by
#                    (7501/5601)^2 = 1.79, hence the higher maximum.]
#
# BUG FIX v1->v2:
#   - LaTeX double-escape: r'H_{\\Lambda CDM}' -> r'H_{\Lambda\mathrm{CDM}}' (fixed)
#   - Legend moved below plot (was overlapping title/axis at upper-left)
#   - print() calls removed (referee version)
#   - Newlines in annotation: literal \n in non-raw string is correct (kept)
#   - set_ylim upper bound 1.98 for headroom above max ratio 1.921
# =============================================================================

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 13,
    'axes.labelsize': 14,
    'legend.fontsize': 11,
    'font.family': 'serif',
    'axes.linewidth': 1.4,
})


def plot_hubble_boost():

    H0_lcdm = 67.4;  h_lcdm = H0_lcdm / 100.0
    H0_ecf  = 73.04; h_ecf  = H0_ecf  / 100.0
    Om      = 0.315
    Om_ecf  = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
    Or_lcdm = 4.15e-5 / h_lcdm**2   # 9.135e-5
    Or_ecf  = 4.15e-5 / h_ecf**2    # 7.779e-5 — same omega_r, different h
    Ol_lcdm = 1.0 - Om - Or_lcdm
    # [CORRECTED 05/09/2026, I82] was 7500; the solver normalises at 5600
    z_peak  = 5600
    a_peak  = 1.0 / (1.0 + z_peak)
    Os0     = 0.093 * Or_ecf * a_peak**2   # spin density today (Section 2)
    Ol_ecf  = 1.0 - Om_ecf - Or_ecf - Os0  # closure [A-7]
    h_ratio = H0_ecf / H0_lcdm             # 1.0837

    z    = np.logspace(0, 4.5, 2000) - 1.0
    z[0] = 0
    a    = 1.0 / (1.0 + z)

    E_l   = np.sqrt(Or_lcdm*a**-4 + Om*a**-3 + Ol_lcdm)
    E_e   = np.sqrt(Or_ecf *a**-4 + Om_ecf*a**-3 + Ol_ecf + Os0*a**-6)
    ratio = (H0_ecf * E_e) / (H0_lcdm * E_l)
    x_axis = 1.0 + z

    fig, ax = plt.subplots(figsize=(11, 7))
    plt.subplots_adjust(left=0.14, right=0.96, top=0.88, bottom=0.22)

    ax.semilogx(x_axis, ratio, 'r-', linewidth=2.8,
                label=r'$H_\mathrm{ECF}(z)\,/\,H_{\Lambda\mathrm{CDM}}(z)$')

    ax.axhline(h_ratio, color='gray', linestyle='--', alpha=0.6, linewidth=1.5,
               label=r'$H_0$ tension: ratio $=1.084$')

    ax.fill_between(x_axis, h_ratio, ratio,
                    where=(x_axis > 1000), color='red', alpha=0.13,
                    label='Torsion boost region ($z>1000$)')

    # Recombination epoch
    z_rec = 1100
    ax.axvline(1 + z_rec, color='steelblue', linestyle=':', linewidth=2)
    ax.text(1250, 1.545, 'Recomb.\n$z=1100$', color='steelblue',
            va='top', ha='left', fontsize=10)

    # Torsion boost annotation
    ax.annotate('Torsion Boost\n' + r'(reduces $r_s$, §3)',
                # 17/08/2026 audit: xytext was (500, 1.50), which placed the box
                # on top of the "Recomb. z=1100" label. Moved down and left.
                xy=(9000, 1.28), xytext=(120, 1.36),
                arrowprops=dict(facecolor='#c0392b', arrowstyle='->',
                                connectionstyle='arc3,rad=.2', lw=1.5),
                fontsize=11, fontweight='bold', color='#c0392b',
                bbox=dict(boxstyle='round', fc='white', ec='#c0392b', alpha=0.9))

    ax.set_xlabel(r'Redshift $(1+z)$', fontweight='bold', fontsize=14)
    ax.set_ylabel(r'$H_\mathrm{ECF}(z) \,/\, H_{\Lambda\mathrm{CDM}}(z)$',
                  fontweight='bold', fontsize=13)
    ax.set_title(
        r'Pre-recombination Torsion Boost — Mechanism of $r_s$ Reduction (F1 §3)',
        fontsize=13, fontweight='bold', pad=14)
    ax.set_xlim(1, 30000)
    ax.set_ylim(1.00, 1.98)
    ax.grid(True, which='both', linestyle=':', alpha=0.4)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14),
              ncol=3, frameon=True, framealpha=0.92, fontsize=11)

    plt.savefig('Figure_Hubble_Boost_Ratio_SUPERSEDED.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    plot_hubble_boost()
