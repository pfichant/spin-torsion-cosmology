"""
Script  : plot_Optimization_Intersection.py  —  v2 (referee)
Paper   : Foundation I
Author  : Pascal Fichant
Date    : 21/04/2026
Figure  : 4  (label: fig:optimizationintersection)
Sources : Sec. 5, Table tab:chi2breakdown, Table tab:priors, App. F
Status  : HISTORICAL ILLUSTRATION of the former calibration
          (gamma_spin = 0.3116, Omega_m = 0.315) -- DEC-A7-POST-07, 22/09/2026.
          The H0/S8 intersection at a single F_ion is not an established
          result under A-7; the figure is kept for provenance only.
"""
# Last modified: 25/08/2026, 21:49 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


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
                         # HISTORICAL CALIBRATION (DEC-A7-POST-07A)

CHI2_CMB_AT_TARGET = 1.8  # near-neutral penalty at F=1.2765     [Tab. tab:chi2breakdown]
F0_CMB    = 1.05          # quartic CMB-penalty centre

# Reference Δχ² from Table tab:chi2breakdown
# [18/08/2026 audit] These three references now match Table 4 exactly, which was
# itself made fully reproducible on the same day: every entry is derived from the
# declared values rather than quoted. Previously DELTA_TOT_REF = 39.5 was compared
# against a curve total of 39.55, and the 0.05 agreement hid the fact that this
# figure models three sectors out of six (the two BAO rows are not represented,
# and they contribute +0.1 to the published total).
DELTA_H0_REF  = 29.31   # H0 sector (ΛCDM→ECF): ((67.4-73.04)/1.04)^2 - 0.1 = 29.31
# Option A (24/08/2026): the DIVISIVE form of S8_ECF makes the ECF
# prediction coincide with the measurement, so chi2_ECF(S8) = 0 and the
# whole LCDM term is the gain. The former 11.98 subtracted a residual
# 0.09 computed from S8_ECF = 0.7603 -- the MULTIPLICATIVE form, which
# option A sets aside. That 0.7603 is no longer the model's prediction.
DELTA_S8_REF  = 12.07   # S8 sector: ((0.832-0.766)/0.019)^2, chi2_ECF(S8) = 0
DELTA_TOT_REF = 39.48   # full Table 4 total, six rows, chi2_ECF(S8) = 0
CHI2_BAO_OFFSET = 0.1   # BOSS DR12 (+0.0) + eBOSS DR16 (+0.1), flat in F_ion
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
#             → 29.41 at F=1.0 (ΛCDM) ; 0.10 at F=1.2765 (ECF)
#             Δ = −29.31  [Tab. chi2breakdown]
#
#    χ²_S8 : ((S8_ECF(F) − 0.766) / 0.019)²
#             S8_ECF(F) = 0.832 / (1 + (F−1)·η_spin)   [divisive]
#             → 12.07 at F=1.0 ; 0.00 at F=1.2765
#             Δ = −12.05 on the grid  [Tab. chi2breakdown: 12.07]
#
#    χ²_CMB: quartic penalty centred at F0=1.05,
#             amplitude scaled so χ²_CMB(F=1.2765) = +1.8  [Tab. chi2breakdown]
# ============================================================
def build_curves(f_arr):
    h0_arr   = f2h0(f_arr)
    # Conventional floor of Table 4: the ECF H0 residual is quoted as
    # 0.10, not 0. Added so this script reproduces the published
    # budget; it shifts the curve by 0.10 out of ~40 and does not move
    # the minimum.
    # ⚠️ RAMPED, not added as a constant: a constant sits at BOTH ends
    # of the difference and cancels -- the very trap found on the BAO
    # line an hour earlier. Table 4 does not put the floor on both
    # sides either: LCDM is 29.41 (no floor), ECF is 0.10 (floor
    # alone), so it belongs to the ECF point only, and 29.41 - 0.10
    # is the published -29.31. Same interpolation caveat as the BAO
    # ramp: anchored on the two values Table 4 publishes.
    CHI2_H0_FLOOR = 0.10
    chi2_h0  = (((h0_arr - TARGET_H0) / SIGMA_H0) ** 2
                + CHI2_H0_FLOOR * (f_arr - 1.0) / (TARGET_F - 1.0))

    # Option A (24/08/2026): DIVISIVE form, the one of the defining
    # equation (l.1209 of Foundation I) and of script_06. At
    # F = 1.2765 it gives S8 = 0.76599 -- the published 0.766 -- so
    # chi2_ECF(S8) vanishes. The multiplicative form gave 0.76030 and
    # left a residual 0.09.
    s8_ecf   = S8_LCDM / (1.0 + (f_arr - 1.0) * ETA_SPIN)
    chi2_s8  = ((s8_ecf - TARGET_S8) / SIGMA_S8) ** 2

    raw_cmb  = ((f_arr - F0_CMB) / 0.5) ** 4
    idx_tgt  = np.argmin(np.abs(f_arr - TARGET_F))
    chi2_cmb = raw_cmb * (CHI2_CMB_AT_TARGET / raw_cmb[idx_tgt])

    # [18/08/2026 audit] The two BAO rows of Table 4 are flat in F_ion within
    # this parameterisation (the recalibration of r_s and H0 preserves D_M/r_s),
    # so they enter as a constant +0.1 offset. Including it makes the total here
    # identical to the published Table 4 value rather than 0.1 away from it.
    # Option A audit (24/08/2026): a CONSTANT cancels in a difference,
    # so the former np.full_like() left the eBOSS row out of the budget
    # while appearing to include it. BOSS DR12 is genuinely flat
    # (6.2 both sides); eBOSS DR16 goes from 3.2 to 3.3, and that
    # +0.1 is what Table 4 carries.
    #
    # WHY IT CANNOT BE FLAT IN F_ion: the BAO observables are RATIOS
    # (D_M/r_s, H.r_s). The ECF contracts r_s and raises H_0 in a
    # coordinated way, so the ratios are preserved TO FIRST ORDER and
    # the +0.1 is what remains after that compensation. At F = 1 there
    # is no contraction, hence no residual: chi2_BAO(ECF) = 3.2 = the
    # LCDM value. The residual can only grow as F departs from 1.
    #
    # ⚠️ THE LINEAR RAMP IS AN INTERPOLATION, NOT A CALCULATION. The
    # residual comes from a mismatch of ratios with no reason to be
    # linear; over a window this narrow the approximation is
    # acceptable, and it is anchored on the two values Table 4
    # publishes (0.0 at F = 1, +0.1 at F = 1.2765). It must not be
    # read as the F-dependence of the BAO likelihood.
    ramp       = (f_arr - 1.0) / (TARGET_F - 1.0)
    chi2_bao   = CHI2_BAO_OFFSET * ramp

    chi2_total = chi2_h0 + chi2_s8 + chi2_cmb + chi2_bao
    return chi2_h0, chi2_s8, chi2_cmb, chi2_total


# ============================================================
# 4. CALIBRATION VERIFICATION
#    Reference: ΛCDM values at F=1.0 (not at F=0.95 axis edge)
# ============================================================
def verify_calibration(f_arr, chi2_h0, chi2_s8, chi2_cmb, chi2_total):
    # Exact evaluation, not the nearest grid node: the published
    # numbers are those AT F = 1.2765, and this function must check
    # what the paper states. On the 2000-point grid the offset
    # reached 0.07 on the H0 sector, which the old tolerance of 0.3
    # absorbed silently. The grid stays for the curve; the two uses
    # are distinct.
    chi2_h0, chi2_s8, chi2_cmb, chi2_total = build_curves(
        np.array([1.0, TARGET_F]))
    idx_lcdm, idx_ecf = 0, 1

    dchi2_h0  = chi2_h0[idx_lcdm]  - chi2_h0[idx_ecf]
    dchi2_s8  = chi2_s8[idx_lcdm]  - chi2_s8[idx_ecf]
    cmb_val   = chi2_cmb[idx_ecf]
    dchi2_tot = chi2_total[idx_lcdm] - chi2_total[idx_ecf]

    print(">>> Calibration verification (Optimization Intersection v2)")
    print(f"   Δχ²_H0  (ΛCDM→ECF) = {dchi2_h0:+.1f}   [target −{DELTA_H0_REF}, Tab. chi2breakdown]")
    print(f"   Δχ²_S8  (ΛCDM→ECF) = {dchi2_s8:+.1f}   [target −{DELTA_S8_REF}, Tab. chi2breakdown]")
    print(f"   χ²_CMB  @ F=1.2765  = {cmb_val:.2f}    [target +{CHI2_CMB_AT_TARGET}, Tab. chi2breakdown]")
    print(f"   Δχ²_total (all 6 rows) = {dchi2_tot:+.2f}   [target −{DELTA_TOT_REF}, Tab. chi2breakdown]")

    tol = 1.5
   
    assert abs(dchi2_h0  - DELTA_H0_REF)       < 1.0, f"H0 failed: {dchi2_h0:.2f} vs {DELTA_H0_REF}"
    # Tolerance tightened from 0.5 to 0.02 on 24/08/2026: the previous
    # bound silently accepted the multiplicative form, whose residual
    # differs by 0.09. A check that wide certifies the stale value.
    assert abs(dchi2_s8  - DELTA_S8_REF)       < 0.02, f"S8 failed: {dchi2_s8:.2f} vs {DELTA_S8_REF} -- check SIGMA_S8"
    assert abs(cmb_val   - CHI2_CMB_AT_TARGET) < 0.3, f"CMB failed: {cmb_val:.2f}"
    # Tolerance tightened from 1.0 to 0.3: the loose bound was wide enough to
    # accept a curve total that did not match the published budget.
    # Same tightening, same reason: 39.39 vs 39.48 is a gap of 0.09,
    # which a tolerance of 0.3 swallowed without a word.
    assert abs(dchi2_tot - DELTA_TOT_REF)      < 0.02, f"Total failed: {dchi2_tot:.2f} vs {DELTA_TOT_REF}"
    
    print(">>> Calibration OK.\n")


# ============================================================
# 5. MAIN PLOTTING FUNCTION
# ============================================================
def plot_optimization():
    print(">>> Generating Figure 4: Optimization Intersection (v2 referee)...")
    print("   STATUS: historical illustration of the former calibration "
          "(gamma_spin = 0.3116, Omega_m = 0.315) -- DEC-A7-POST-07; not an active result under A-7")

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
                  r'[historical $\eta_{\rm spin}=0.3116$, $\sigma_{S_8}=0.019$]')
    ax.plot(f_ion, chi2_cmb,
            color='orange', ls='--', lw=1.8,
            label=r'CMB Stability Penalty (quartic, $F_0=1.05$, $+1.8$ at $F=1.2765$)')
    ax.plot(f_ion, chi2_total,
            color='#D00000', lw=3.5,
            label=r'Total Combined $\chi^2$  ($\Delta\chi^2_{\rm total}=-39.5$ vs $\Lambda$CDM)')

    ax.plot(TARGET_F, chi2_at_target,
            marker='*', markersize=24, color='gold',
            markeredgecolor='black', zorder=10,
            label=r'Former calibration point $F_{\rm ion}=1.2765$ (historical H$_0$–$S_8$ intersection)')

    ax.fill_between(f_ion, 0, 40,
                    where=(chi2_total < chi2_at_target + 2.3),
                    color='gold', alpha=0.25,
                    label=r'68% confidence region ($\Delta\chi^2<2.3$)')

    ax.annotate(
        rf'Historical calibration: $F_{{\rm ion}}={TARGET_F}$' '\n'
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
    ax.set_ylabel(r'Effective $\chi^2$ Tension', fontsize=13)    # Title aligned on the F1 Extended caption (fig:optimizationintersection, l.1250) — 17/08/2026 audit.
    # The .tex captions were cleared of verdict wording on 12/08/2026; the
    # figure titles were not. The paper caption is authoritative.
    ax.set_title(r'Parameter Optimization Landscape' '\n'
                 r'historical illustration of the former calibration '
                 r'($\gamma_{\rm spin}=0.3116$, $\Omega_m=0.315$)',
                 fontsize=12, pad=25, fontweight='bold')
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
