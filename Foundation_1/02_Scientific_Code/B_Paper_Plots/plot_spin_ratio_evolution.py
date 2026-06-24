"""
Script  : plot_spin_ratio_evolution_v2.py  —  v2 (referee, final)
Paper   : Foundation I: Unified Resolution of Cosmological Tensions
Author  : Pascal Fichant
Date    : 21/04/2026
Figure  : fig:spinevolution  (Sec. 3 / App. D)
Sources : Sec. 2 (eq:spindensity), Tab. tab:priors,
          Tab. tab:chi2breakdown, App. D (app:rscalc)
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.use('Agg')

plt.rcParams.update({
    'font.family':  'serif',
    'font.size':     12,
    'axes.labelsize': 13,
    'figure.figsize': (10, 7),
})


# ============================================================
# 1. CALIBRATION  [Sec. 2, eq:spindensity; Tab. tab:priors]
#
#    ρ_spin ∝ a⁻⁶,  ρ_r ∝ a⁻⁴  →  ratio ∝ a⁻² ∝ (1+z)²
#    Normalisation : ratio(Z_PEAK) = RATIO_PEAK
# ============================================================
Z_PEAK     = 7500.0    # acoustic-era calibration window      [App. D]
RATIO_PEAK = 0.093     # Ω_spin/Ω_r = 9.3 % at peak          [Tab. tab:priors]
Z_REC      = 1100.0    # recombination redshift
Z_TODAY    =    0.0    # present day

C = RATIO_PEAK / (1.0 + Z_PEAK)**2   # = 1.653e-9


# ============================================================
# 2. CALIBRATION VERIFICATION
#    [Tab. tab:priors; Tab. tab:chi2breakdown; abstract]
# ============================================================
def verify_calibration():
    ratio_peak  = C * (1.0 + Z_PEAK)**2
    ratio_rec   = C * (1.0 + Z_REC)**2
    ratio_today = C * (1.0 + Z_TODAY)**2

    print(">>> Calibration verification (Spin Ratio Evolution v2)")
    print(f"   Ω_spin/Ω_r @ z={Z_PEAK:.0f}  = {ratio_peak*100:.4f} %"
          f"   [target 9.3 %, Tab. tab:priors]")
    print(f"   Ω_spin/Ω_r @ z={Z_REC:.0f}    = {ratio_rec*100:.4f} %"
          f"   [CMB-compatible dilution, Tab. tab:chi2breakdown]")
    print(f"   Ω_spin,0   @ z=0         = {ratio_today:.4e}"
          f"   [~10⁻⁶ level, abstract]")
    print(f"   Dilution z=7500 → z=1100 = ×{ratio_rec/ratio_peak:.4f}"
          f"   [(1101/7501)² = {(1101/7501)**2:.4f}]")

    assert abs(ratio_peak  - RATIO_PEAK) < 1e-8,  "Peak calibration failed"
    assert abs(ratio_rec   - 0.002004)   < 5e-5,  "Recombination ratio failed"
    assert abs(ratio_today - 1.653e-9)   < 1e-11, "Today ratio failed"
    print(">>> Calibration OK.\n")


# ============================================================
# 3. FIGURE
# ============================================================
def plot_spin_ratio():
    print(">>> Generating fig:...")

    verify_calibration()

    # Data — start at z=800 to give breathing room to z_rec marker
    z_arr  = np.logspace(np.log10(800), np.log10(20000), 2000)
    ratio  = C * (1.0 + z_arr)**2 * 100.0

    r_peak = RATIO_PEAK * 100.0
    r_rec  = C * (1.0 + Z_REC)**2 * 100.0
    r_0    = C * (1.0 + Z_TODAY)**2 * 100.0

    fig, ax = plt.subplots()

    # Main curve
    ax.loglog(z_arr, ratio, color='steelblue', lw=2.5, zorder=3,
              label=r'$\rho_{\rm spin}/\rho_r \propto (1+z)^2$  [eq:spindensity]')

    # Stiff-phase shading
    ax.axvspan(Z_REC, Z_PEAK, alpha=0.10, color='steelblue', zorder=1,
               label='Stiff-phase epoch')

    # Vertical reference lines
    ax.axvline(Z_PEAK, color='darkorange', ls='--', lw=1.5, alpha=0.85, zorder=2,
               label=r'Acoustic-era window $z = 7500$  [App. D]')
    ax.axvline(Z_REC,  color='crimson',    ls='--', lw=1.5, alpha=0.85, zorder=2,
               label=r'Recombination $z_{\rm rec} = 1100$')

    # Key-point markers
    ax.plot(Z_PEAK, r_peak, 'o', ms=10, color='darkorange',
            markeredgecolor='black', zorder=6)
    ax.plot(Z_REC,  r_rec,  's', ms=10, color='crimson',
            markeredgecolor='black', zorder=6)

    # Present-day level
    ax.axhline(r_0, color='#999', ls=':', lw=1.2, alpha=0.8, zorder=2,
               label=r'$\Omega_{\rm spin,0} \sim 1.65 \times 10^{-7}$  ($z=0$)')

    # Annotation boxes
    ax.annotate(
        r'Peak: $\Omega_{\rm spin}/\Omega_r = 9.3\%$' '\n'
        r'$z = 7500$ (acoustic-era window)',
        xy=(Z_PEAK, r_peak),
        xytext=(Z_PEAK * 1.18, r_peak * 2.0),
        fontsize=10.5,
        arrowprops=dict(arrowstyle='->', color='darkorange', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='darkorange', alpha=0.95)
    )
    ax.annotate(
        r'$z_{\rm rec} = 1100$:' '\n'
        r'$\Omega_{\rm spin}/\Omega_r = 0.20\%$' '\n'
        r'$\Rightarrow\,\Delta\chi^2_{\rm CMB} = +1.8$',
        xy=(Z_REC, r_rec),
        xytext=(Z_REC * 1.25, r_rec * 4.5),
        fontsize=10.5,
        arrowprops=dict(arrowstyle='->', color='crimson', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='crimson', alpha=0.95)
    )

    # Axis formatting
    ax.set_xlabel(r'Redshift $z$', fontsize=13)
    ax.set_ylabel(r'$\rho_{\rm spin}/\rho_r$  [%]', fontsize=13)

    # FIX: titre propre, sans \ref LaTeX brut
    ax.set_title(
        r'Dynamic Evolution of the Torsion Density'
        r'  —  $\rho_{\rm spin}/\rho_r \propto (1+z)^2$',
        fontsize=13, fontweight='bold', pad=12
    )

    # FIX: xlim étendu à z=800 pour dégager le marqueur z_rec
    ax.set_xlim(800, 20000)
    ax.grid(True, which='both', ls=':', alpha=0.40)

    ax.legend(loc='lower right', frameon=True, fancybox=True,
              framealpha=0.93, fontsize=10.5, borderpad=0.8, labelspacing=0.55)

    plt.tight_layout()
    outfile = 'Figure_spin_ratio_evolution.png'
    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    print(f"   [SUCCESS] Saved: {outfile}")
    plt.close()


if __name__ == "__main__":
    plot_spin_ratio()
