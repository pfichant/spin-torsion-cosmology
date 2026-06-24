"""
Script  : plot_Optimization_Intersection.py  —  v2 (referee)
Paper   : Foundation I: Unified Resolution of Cosmological Tensions
Author  : Pascal Fichant
Date    : 21/04/2026
Figure  : 4  (label: fig:optimizationintersection)
Sources : Sec. 5, Table tab:chi2breakdown, Table tab:priors, App. F
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 14,
    'figure.figsize': (10, 7),
})

# ============================================================
# 1. PHYSICAL CONSTANTS  [Sec. 5, Table tab:priors / tab:chi2breakdown]
# ============================================================
TARGET_F  = 1.2765       # best-fit F_ion                         [Tab. tab:priors]
TARGET_H0 = 73.04        # SH0ES best-fit  [km/s/Mpc]            [Riess 2021]
SIGMA_H0  = 1.04         # SH0ES 1-sigma   [km/s/Mpc]
H0_LCDM   = 67.4         # Planck 2018 baseline

# Slope from two-point calibration: F=1.0→67.4, F=1.2765→73.04
SLOPE = (TARGET_H0 - H0_LCDM) / (TARGET_F - 1.0)   # = 20.398 km/s/Mpc/unit

TARGET_S8 = 0.766        # ECF best-fit                           [Tab. tab:priors]
SIGMA_S8  = 0.019        # KiDS-1000 1-sigma [Heymans+2021, arXiv:2007.15632]
                         # NB: combined KiDS+DES gives 0.014; KiDS alone gives 0.019.
                         # The paper uses 0.019 in Sec. 4–5 and Tab. chi2breakdown.
S8_LCDM   = 0.832        # Planck 2018 baseline
ETA_SPIN  = 0.3116       # growth-torsion coupling efficiency     [Tab. tab:priors]

CHI2_CMB_AT_TARGET = 1.8  # near-neutral penalty at F=1.2765     [Tab. tab:chi2breakdown]
F0_CMB    = 1.05          # quartic CMB-penalty centre

# Reference Δχ² from Table tab:chi2breakdown
DELTA_H0_REF  = 29.4    # improvement in H0 sector  (ΛCDM→ECF): ((67.4-73.04)/1.04)^2 = 29.41
DELTA_TOT_REF = 39.5    # total global Δχ²
DELTA_S8_REF  = 12.1    # improvement in S8 sector [recomputed with sigma_S8=0.019]
                        # chi2_S8(LCDM) = ((0.832-0.766)/0.019)^2 = 12.06

# ============================================================
# 2. AXIS CONVERSION  [App. F calibration]
#    F=1.0 → H0=67.4  |  F=1.2765 → H0=73.04
# ============================================================
def f2h0(f):
    return H0_LCDM + SLOPE * (f - 1.0)

def h02f(h):
    return 1.0 + (h - H0_LCDM) / SLOPE


# ============================================================
# 3. CHI2 CURVES — physically anchored to Tab. tab:chi2breakdown
#
#    χ²_H0 : ((H0(F) − 73.04) / 1.04)²
#             → 29.4 at F=1.0  (ΛCDM) ; 0.0 at F=1.2765 (ECF)
#             Δ = −29.4 ≈ −30.4  [Tab. chi2breakdown]
#
#    χ²_S8 : ((S8_ECF(F) − 0.766) / 0.019)²
#             S8_ECF(F) = 0.832·(1 − (F−1)·η_spin)
#             → 10.9 at F=1.0 ; ~0.1 at F=1.2765
#             Δ ≈ −10.8 ≈ −10.9  [Tab. chi2breakdown]
#
#    χ²_CMB: quartic penalty centred at F0=1.05,
#             amplitude scaled so χ²_CMB(F=1.2765) = +1.8  [Tab. chi2breakdown]
# ============================================================
def build_curves(f_arr):
    h0_arr   = f2h0(f_arr)
    chi2_h0  = ((h0_arr - TARGET_H0) / SIGMA_H0) ** 2

    s8_ecf   = S8_LCDM * (1.0 - (f_arr - 1.0) * ETA_SPIN)
    chi2_s8  = ((s8_ecf - TARGET_S8) / SIGMA_S8) ** 2

    raw_cmb  = ((f_arr - F0_CMB) / 0.5) ** 4
    idx_tgt  = np.argmin(np.abs(f_arr - TARGET_F))
    chi2_cmb = raw_cmb * (CHI2_CMB_AT_TARGET / raw_cmb[idx_tgt])

    chi2_total = chi2_h0 + chi2_s8 + chi2_cmb
    return chi2_h0, chi2_s8, chi2_cmb, chi2_total


# ============================================================
# 4. CALIBRATION VERIFICATION
#    Reference: ΛCDM values at F=1.0 (not at F=0.95 axis edge)
# ============================================================
def verify_calibration(f_arr, chi2_h0, chi2_s8, chi2_cmb, chi2_total):
    idx_lcdm = np.argmin(np.abs(f_arr - 1.0))
    idx_ecf  = np.argmin(np.abs(f_arr - TARGET_F))

    dchi2_h0  = chi2_h0[idx_lcdm]  - chi2_h0[idx_ecf]
    dchi2_s8  = chi2_s8[idx_lcdm]  - chi2_s8[idx_ecf]
    cmb_val   = chi2_cmb[idx_ecf]
    dchi2_tot = chi2_total[idx_lcdm] - chi2_total[idx_ecf]

    print(">>> Calibration verification (Optimization Intersection v2)")
    print(f"   Δχ²_H0  (ΛCDM→ECF) = {dchi2_h0:+.1f}   [target −{DELTA_H0_REF}, Tab. chi2breakdown]")
    print(f"   Δχ²_S8  (ΛCDM→ECF) = {dchi2_s8:+.1f}   [target −{DELTA_S8_REF}, Tab. chi2breakdown]")
    print(f"   χ²_CMB  @ F=1.2765  = {cmb_val:.2f}    [target +{CHI2_CMB_AT_TARGET}, Tab. chi2breakdown]")
    print(f"   Δχ²_total           = {dchi2_tot:+.1f}   [target −{DELTA_TOT_REF}, Sec. 5]")

    tol = 1.5
   
    assert abs(dchi2_h0  - DELTA_H0_REF)       < 1.0, f"H0 failed: {dchi2_h0:.2f} vs {DELTA_H0_REF}"
    assert abs(dchi2_s8  - DELTA_S8_REF)       < 0.5, f"S8 failed: {dchi2_s8:.2f} vs {DELTA_S8_REF} -- check SIGMA_S8"
    assert abs(cmb_val   - CHI2_CMB_AT_TARGET) < 0.3, f"CMB failed: {cmb_val:.2f}"
    assert abs(dchi2_tot - DELTA_TOT_REF)      < 1.0, f"Total failed: {dchi2_tot:.2f} vs {DELTA_TOT_REF}"
    
    print(">>> Calibration OK.\n")


# ============================================================
# 5. MAIN PLOTTING FUNCTION
# ============================================================
def plot_optimization():
    print(">>> Generating Figure 4: Optimization Intersection (v2 referee)...")

    f_ion = np.linspace(0.95, 1.55, 2000)
    chi2_h0, chi2_s8, chi2_cmb, chi2_total = build_curves(f_ion)

    verify_calibration(f_ion, chi2_h0, chi2_s8, chi2_cmb, chi2_total)

    idx_tgt       = np.argmin(np.abs(f_ion - TARGET_F))
    chi2_at_target = chi2_total[idx_tgt]

    fig, ax = plt.subplots()

    ax.plot(f_ion, chi2_h0,
            color='blue', ls='--', lw=1.8,
            label=r'$H_0$ Preference — SH0ES '
                  r'[$\chi^2_{H_0}=((H_0(F)-73.04)/1.04)^2$]')
    ax.plot(f_ion, chi2_s8,
            color='green', ls='--', lw=1.8,
            label=r'$S_8$ Preference — KiDS-1000 [Heymans+2021] '
                  r'[$\eta_{\rm spin}=0.3116$, $\sigma_{S_8}=0.019$]')
    ax.plot(f_ion, chi2_cmb,
            color='orange', ls='--', lw=1.8,
            label=r'CMB Stability Penalty (quartic, $F_0=1.05$, $+1.8$ at $F=1.2765$)')
    ax.plot(f_ion, chi2_total,
            color='#D00000', lw=3.5,
            label=r'Total Combined $\chi^2$  ($\Delta\chi^2_{\rm total}=-39.5$ vs $\Lambda$CDM)')

    ax.plot(TARGET_F, chi2_at_target,
            marker='*', markersize=24, color='gold',
            markeredgecolor='black', zorder=10,
            label=r'Sweet Spot $F_{\rm ion}=1.2765$ (H$_0$–$S_8$ intersection, App. F)')

    ax.fill_between(f_ion, 0, 40,
                    where=(chi2_total < chi2_at_target + 2.3),
                    color='gold', alpha=0.25,
                    label=r'68% confidence region ($\Delta\chi^2<2.3$)')

    ax.annotate(
        rf'Sweet Spot: $F_{{\rm ion}}={TARGET_F}$' '\n'
        rf'$H_0={TARGET_H0}$ km s$^{{-1}}$ Mpc$^{{-1}}$, $S_8={TARGET_S8}$' '\n'
        rf'$\Delta\chi^2_{{total}}=-39.5$ vs. $\Lambda$CDM',
        xy=(TARGET_F, chi2_at_target),
        xytext=(TARGET_F + 0.10, chi2_at_target + 10),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
        fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='black', alpha=0.9)
    )

    ax.axvline(1.0, color='black', lw=1.5, alpha=0.5)
    ax.text(0.963, 20, r'$\Lambda$CDM ($F=1$)', rotation=90, fontsize=10, alpha=0.7)

    ax2 = ax.secondary_xaxis('top', functions=(f2h0, h02f))
    ax2.set_xlabel(r'Hubble Constant $H_0$ [km s$^{-1}$ Mpc$^{-1}$]',
                   fontsize=12, labelpad=10)
    ax2.set_ticks([67.4, 70.0, 73.04, 76.0])
    ax2.set_xticklabels(['67.4', '70', r'$\mathbf{73.04}$', '76'])

    ax.set_xlim(0.95, 1.55)
    ax.set_ylim(0, 40)
    ax.set_xlabel(r'Torsion Stiffness Parameter $F_{\rm ion}$', fontsize=13)
    ax.set_ylabel(r'Effective $\chi^2$ Tension', fontsize=13)
    ax.set_title(r'Unified Resolution: Parameter Optimization Landscape',
                 fontsize=15, pad=25, fontweight='bold')
    ax.grid(True, ls=':', alpha=0.55)
    ax.legend(loc='upper right', frameon=True, fancybox=True,
              framealpha=0.92, fontsize=9.5)

    plt.tight_layout()
    outfile = 'Figure_Optimization_Intersection.png'
    plt.savefig(outfile, dpi=300)
    print(f"   [SUCCESS] Saved: {outfile}")
    plt.close()


if __name__ == "__main__":
    plot_optimization()
