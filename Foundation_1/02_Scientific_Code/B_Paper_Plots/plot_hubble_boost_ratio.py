# plot_hubble_boost_ratio.py  —  v2 referee
# =============================================================================
# SCRIPT  : Pre-recombination Torsion Boost — H(z) ratio (Figure 3 / Fig. boost)
# Paper   : Foundation I: The Metric Universe (Extended v2)
# Author  : Pascal Fichant (2026)
# Section : Section 3 (Sound Horizon Reduction), cross-check: script01solvesoundhorizon.py
#
# INPUTS (F1 Table tabpriors, Section 3):
#   H0_LCDM = 67.4 km/s/Mpc           [Planck2020]
#   H0_ECF  = 73.04 km/s/Mpc          [F1 Section 5, best-fit]
#   Om      = 0.315                    [both models, fixed]
#   omega_r = 4.15e-5 (h^2 units)     [universal, T_CMB=2.725K]
#   Or_LCDM = omega_r / h_LCDM^2 = 9.135e-5   (h=0.674)
#   Or_ECF  = omega_r / h_ECF^2  = 7.779e-5   (h=0.7304)
#   Physical rho_r identical: Or*h^2 = 4.15e-5 in both models. ✓
#   z_peak  = 7500   (spin injection peak, F1 Section 2)
#   Omega_spin,peak = 0.093 (= spin_peak parameter, F1 Table tabpriors)
#   Os0 = 0.093 * Or_ECF * a_peak^2 = 1.286e-13   (today's spin density)
#   Closure: Ol_ECF = 1 - Om - Or_ECF - Os0 = 0.684922
#
# INDEPENDENT VERIFICATION (computed before plotting):
#   ratio(z=0)    = H0_ECF/H0_LCDM = 1.0837  ✓  (flat-universe closure verified)
#   ratio(z=1100) = 1.0643
#   ratio(z=7500) = 1.0576   (spin/rad = 0.093 at z_peak by construction ✓)
#   ratio(z_max)  = 1.584 at 1+z ~ 31623  (within ylim 1.62 ✓)
#
# BUG FIX v1->v2:
#   - LaTeX double-escape: r'H_{\\Lambda CDM}' -> r'H_{\Lambda\mathrm{CDM}}' (fixed)
#   - Legend moved below plot (was overlapping title/axis at upper-left)
#   - print() calls removed (referee version)
#   - Newlines in annotation: literal \n in non-raw string is correct (kept)
#   - set_ylim upper bound raised 1.60->1.62 for headroom above max ratio 1.584
# =============================================================================

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
    Or_lcdm = 4.15e-5 / h_lcdm**2   # 9.135e-5
    Or_ecf  = 4.15e-5 / h_ecf**2    # 7.779e-5 — same omega_r, different h
    Ol_lcdm = 1.0 - Om - Or_lcdm
    z_peak  = 7500
    a_peak  = 1.0 / (1.0 + z_peak)
    Os0     = 0.093 * Or_ecf * a_peak**2   # spin density today (Section 2)
    Ol_ecf  = 1.0 - Om - Or_ecf - Os0      # closure
    h_ratio = H0_ecf / H0_lcdm             # 1.0837

    z    = np.logspace(0, 4.5, 2000) - 1.0
    z[0] = 0
    a    = 1.0 / (1.0 + z)

    E_l   = np.sqrt(Or_lcdm*a**-4 + Om*a**-3 + Ol_lcdm)
    E_e   = np.sqrt(Or_ecf *a**-4 + Om*a**-3 + Ol_ecf + Os0*a**-6)
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
    ax.text(1650, 1.575, 'Recomb.\n$z=1100$', color='steelblue',
            va='top', ha='left', fontsize=10)

    # Torsion boost annotation
    ax.annotate('Torsion Boost\n' + r'(reduces $r_s$, §3)',
                xy=(9000, 1.28), xytext=(500, 1.50),
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
    ax.set_ylim(1.00, 1.62)
    ax.grid(True, which='both', linestyle=':', alpha=0.4)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.14),
              ncol=3, frameon=True, framealpha=0.92, fontsize=11)

    plt.savefig('Figure_Hubble_Boost_Ratio.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    plot_hubble_boost()
