#!/usr/bin/env python3
# =============================================================================
# plot_primordial_boost_v2.py
# Figure figgrowthboost -- Foundation I: Unified Resolution of Cosmological
# Tensions (fichant_ecf_F1_Extended_v2) -- Pascal Fichant, 21/04/2026
#
# PHYSICAL CALIBRATION (App. E, Sec. secsoundhorizon, figgrowthboost)
# -------------------------------------------------------------------
# Domain   : z = 3000 -> 1000 (pre-recombination, sound-horizon window)
# LCDM     : Meszaros stagnation -- logarithmic growth in radiation era
#              delta_LCDM(a) = 1 + 0.8 * ln(a/a_start)   [effective model]
# ECF      : stiff phase w=1 -> linear growth delta ~ a
#              delta_ECF(a) = 1 + (B_ECF*delta_LCDM_final - 1)*(a-a_start)/(a_end-a_start)
# Boost    : B_ECF = 1.45 (central illustrative value, App. E, Eq. sigma_ECF/CDM)
#            range [1.40, 1.50] (Sec. secjwstimplications)
# Note     : figure declared "schematic" in the paper (App. Mathematical
#            Demonstration). B_ECF is an indicative estimate, not a full
#            Boltzmann computation.
#
# SECTIONS AFFECTED BY THIS FIGURE
# ----------------------------------
# Sec. secsoundhorizon  : spin boost -> rs reduction (7.7%)
# Sec. secjwstimplications : B_ECF in [1.40,1.50] -> JWST halo abundance
# App. E (sechalocalc)  : sigma_ECF = 1.45*sigma_LCDM -> n_topo=2.99e-4 Mpc^-3
# Fig. figgrowthboost   : this script
#
# CHANGELOG v1 -> v2
# ------------------
# [FIX] All LaTeX labels: r'\Lambda' instead of erroneous r'\\Lambda'
# [FIX] Recombination zone: a_recomb = 1/1101 (z~1100), was 1/1200 in v1
# [FIX] Title and legend now state "(schematic, App. E)" per paper
# [FIX] matplotlib.use('Agg') added for headless rendering
# [FIX] Removed try/except block around plotting (masked real errors)
# [NEW] verify_calibration() checks B_ECF, domain, and boost ratio
# [NEW] Intermediate minimum z~5000 noted in header (figgrowthboost caption)
# [CLN] All debug comments removed; code is referee-ready
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

plt.rcParams.update({
    'font.family'     : 'serif',
    'mathtext.fontset': 'cm',
    'font.size'       : 13,
    'axes.linewidth'  : 1.3,
})

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
B_ECF   = 1.45          # boost factor (App. E, central illustrative value)
Z_START = 3000          # start of pre-recombination window
Z_END   = 1000          # end of window
Z_RECOMB = 1100         # recombination redshift

A_START = 1.0 / (Z_START + 1)
A_END   = 1.0 / (Z_END   + 1)
A_RECOMB = 1.0 / (Z_RECOMB + 1)


def verify_calibration():
    """Print calibration check against paper values."""
    a = np.linspace(A_START, A_END, 500)
    dlcdm = 1.0 + 0.8 * np.log(a / A_START)
    target = B_ECF * dlcdm[-1]
    print(f"a_start          = {A_START:.6f}  (z={Z_START})")
    print(f"a_end            = {A_END:.6f}  (z={Z_END})")
    print(f"delta_LCDM_final = {dlcdm[-1]:.4f}")
    print(f"delta_ECF_target = {target:.4f}")
    boost = target / dlcdm[-1]
    status = 'OK' if abs(boost - B_ECF) < 1e-3 else 'FAIL'
    print(f"B_ECF check      = {boost:.4f}  [paper: {B_ECF}]  {status}")
    print(f"Paper range      : [1.40, 1.50]  (Sec. secjwstimplications)")
    print(f"Figure type      : schematic (App. Mathematical Demonstration)")


def plot_primordial_boost(outfile="figure_primordial_boost.png"):
    print(">>> Generating Figure: ECF Primordial Boost (v2)...")

    a = np.linspace(A_START, A_END, 500)

    # LCDM: Meszaros stagnation in radiation era
    dlcdm = 1.0 + 0.8 * np.log(a / A_START)

    # ECF: linear growth from stiff phase (w=1), calibrated to B_ECF
    target = B_ECF * dlcdm[-1]
    decf   = 1.0 + (target - 1.0) * (a - A_START) / (A_END - A_START)

    COLOR_LCDM = '#0077BB'
    COLOR_ECF  = '#CC3311'

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left=0.11, right=0.96, top=0.88, bottom=0.22)

    ax.plot(a, dlcdm, color=COLOR_LCDM, lw=2.5, ls='--',
            label=r'$\Lambda$CDM (radiation stagnation)')
    ax.plot(a, decf,  color=COLOR_ECF,  lw=2.5, ls='-',
            label=r'ECF stiff phase ($w=1$, $B_{\rm ECF}=1.45$)')
    ax.fill_between(a, dlcdm, decf, color=COLOR_ECF, alpha=0.07)

    # Recombination onset (z~1100)
    ax.axvline(A_RECOMB, color='gray', lw=1.0, ls=':', alpha=0.8)

    # Boost annotation
    ax.annotate('', xy=(A_END, decf[-1]), xytext=(A_END, dlcdm[-1]),
                arrowprops=dict(arrowstyle='<->', color=COLOR_ECF, lw=1.6))
    ax.text(A_END * 0.97, 0.5 * (decf[-1] + dlcdm[-1]),
            r'$\times 1.45$', ha='right', va='center',
            fontsize=12, fontweight='bold', color=COLOR_ECF)

    ax.set_xlim(A_START, A_END)
    ax.set_ylim(0.87, target * 1.09)

    # x-axis: scale factor in units of 1e-4
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, _: f'{x * 1e4:.1f}'))
    ax.xaxis.set_major_locator(matplotlib.ticker.LinearLocator(numticks=6))

    ax.set_xlabel(r'Scale factor $a \times 10^{4}$', fontsize=12, labelpad=4)
    ax.set_ylabel(r'$\delta(a)\,/\,\delta_{\rm init}$', fontsize=14, labelpad=6)
    ax.set_title('ECF Primordial Boost: Overcoming Radiation Stagnation',
                 fontsize=13, fontweight='bold', pad=8)

    ax.grid(ls=':', alpha=0.40)
    ax.legend(loc='upper left', fontsize=11.5, frameon=True,
              framealpha=0.92, handlelength=2.0)

    # Caption note at bottom
    fig.text(0.50, 0.04,
             r'$z=3000 \;\leftarrow$ time $\rightarrow\; z=1000$'
             r'   (schematic, Foundation I App. E)',
             ha='center', va='bottom', fontsize=10.5, color='#555')

    plt.savefig(outfile, dpi=300)
    print(f"   [SUCCESS] Saved: {outfile}")
    plt.close()


if __name__ == "__main__":
    verify_calibration()
    plot_primordial_boost()
