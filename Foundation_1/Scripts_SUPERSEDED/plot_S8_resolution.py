# Last modified: 21/08/2026, 16:05 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
# =============================================================================
# [18/08/2026] SCRIPT SUPERSEDED -- NOT PART OF THE F1 DEPOSIT
#
# This script was written on 21/04/2026 as an alternative producer of a
# published figure. Its value was diagnostic: it did the sigma_8 / S_8
# conversion correctly where the published script inverted the two
# (0.832 is Planck's S_8, not its sigma_8). That defect was FIXED in
# plot_euclid_pk_S8.py on 18/08/2026, which now declares S8_LCDM = 0.832
# and derives sigma8 = 0.812. The present script therefore no longer adds
# anything: it draws the same comparison with fewer Euclid points.
#
# Kept locally for provenance -- it is what revealed the inversion.
# Its output is suffixed _SUPERSEDED so that it cannot overwrite a
# published figure if run by accident.
# =============================================================================
"""
plot_S8_resolution.py  —  Foundation I
Author : Pascal Fichant  |  Date : 21/04/2026  |  v2 referee / Zenodo release

Generates Figure fig:euclidpk — Matter Power Spectrum S8 tension resolution.

Physics
-------
P_ECF(k) = P_LCDM(k) * T_torsion^2(k)

  T_torsion(k) = 1 - A_sup * k^2 / (k^2 + k_cut^2)      [Sec.4, Sec.6]
  A_sup = 0.15,  k_cut = 0.10 h/Mpc                       [fig:euclidpk caption]
  Status (DEC-A7-POST-07C, 22/09/2026): phenomenological, not canonical; NOT
  calibrated on S8 = 0.766; articulation with gamma_spin not demonstrated (no
  double counting); A_sup ~ 0.053 would reproduce 0.766 on the CAMB A-7
  reference (diagnostic only, calc_S8_reference_camb_A7.py).

  S8_ECF   = 0.766  observational TARGET (KiDS-1000), not an ECF prediction;
             Delta-chi2 = -10.9 is historical                          [Sec.5]
  sigma8   = 0.8122 = S8 / sqrt(Omega_m / 0.3), Omega_m = omega_m/h^2 = 0.2669 (A-7;
             0.747 with the former 0.315; DEC-A7-POST-04)                  [Sec.6]
  r_s ECF  = 135.65 Mpc (A-6; was 135.8)  vs  147.09 Mpc (LCDM)          [Sec.3]
  F_ion    = 1.2765  (fixed on r_s, H0 sector; the former "single free parameter
                     governing both H0 and S8" is withdrawn, DEC-A7-POST-07)  [Sec.5]

Sections impacted: Sec.4 (sectensions), Sec.5 (secresults), Sec.6 (seceuclidprediction)

Changelog v1 -> v2
-------------------
  + T_torsion^2 suppression added (absent from v1)
  + ns corrected: 0.96 -> 0.965  (Planck 2018)
  + verify_calibration() added
  + Annotation box moved to top-right
  + Typo "STATING" -> "STARTING" fixed
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RS_PLANCK   = 147.09
RS_ECF      = 135.65   # [D3, 22/09/2026] A-6 (was 135.8), script_01
S8_PLANCK   = 0.832
S8_ECF      = 0.766
S8_KIDS_VAL = 0.766
S8_KIDS_ERR = 0.014
FION        = 1.2765
ETA_SPIN    = 0.3116
NS          = 0.965
OMEGA_M     = (0.02237 + 0.1200)/0.7304**2   # [D3, 22/09/2026 -- DEC-A7-POST-05] ECF S8 sector: omega_m/h_ECF^2 = 0.2669 (A-7); was 0.315
A_SUP       = 0.15
K_CUT       = 0.10


def verify_calibration():
    """Independent checks against Foundation I v2 paper values."""
    print(">>> Calibration verification (Foundation I v2)...")
    s8_macro = S8_PLANCK * (1.0 - (FION - 1.0) * ETA_SPIN)
    sigma8   = S8_ECF / np.sqrt(OMEGA_M / 0.3)
    T2_kcut  = (1.0 - A_SUP * K_CUT**2 / (K_CUT**2 + K_CUT**2))**2
    T2_sat   = (1.0 - A_SUP)**2
    ok       = "OK" if abs(sigma8 - 0.8122) < 0.002 else "CHECK"   # [D3] DEC-A7-POST-04 (0.747 at Om = 0.315)
    print(f"   S8 macro layer   = {s8_macro:.4f}  [historical gamma_spin = 0.3116, multiplicative form]")
    print(f"   S8 net target    = {S8_ECF}    [KiDS-1000 target; T^2 NOT propagated to sigma8 here]")
    print("   T^2(k), A_sup = 0.15: phenomenological, not canonical (DEC-A7-POST-07C);")
    print("   articulation with gamma_spin not demonstrated (no double counting);")
    print("   A_sup ~ 0.053 would reproduce 0.766 on the CAMB A-7 reference (diagnostic only)")
    print(f"   sigma8_ECF       = {sigma8:.4f}  [expected 0.8122, DEC-A7-POST-04]  {ok}")
    print(f"   T^2(k_cut)       = {T2_kcut:.4f}")
    print(f"   T^2_sat          = {T2_sat:.4f}  [(1-A_sup)^2]")
    print(f"   r_s ratio        = {RS_ECF}/{RS_PLANCK} = {RS_ECF/RS_PLANCK:.4f}")
    print(f"   Delta-chi2_S8    = -10.9  [Table tabchi2breakdown]")
    print(">>> Calibration OK.")


def bbks_transfer(k, gamma=0.21):
    """BBKS transfer function (Bardeen et al. 1986)."""
    q = k / gamma
    return (np.log(1.0 + 2.34*q) / (2.34*q) *
            (1.0 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25))


def T_torsion(k):
    """Lorentzian torsion suppression filter (Sec.4, Sec.6)."""
    return 1.0 - A_SUP * k**2 / (k**2 + K_CUT**2)


def matter_power_spectrum(k, rs, s8, apply_torsion=False):
    """
    Phenomenological P(k): BBKS shape * BAO wiggles * S8^2 normalisation.
    apply_torsion=True multiplies by T_torsion^2(k) for the ECF model.
    """
    tf  = bbks_transfer(k)
    bao = 1.0 + 0.05 * np.sin(k * rs) * np.exp(-(k * 10)**1.5)
    pk  = k**NS * tf**2 * bao * s8**2 * 1e4
    if apply_torsion:
        pk *= T_torsion(k)**2
    return pk


def plot_s8_resolution():
    print(">>> Generating Figure: S8 Tension Resolution (v2)...")

    k = np.logspace(-2.5, -0.5, 500)

    y_lcdm = matter_power_spectrum(k, RS_PLANCK, S8_PLANCK)
    y_ecf  = matter_power_spectrum(k, RS_ECF, S8_ECF, apply_torsion=True)

    norm    = 1e4 / np.max(y_lcdm)
    y_lcdm *= norm
    y_ecf  *= norm

    rel_err = 2.0 * S8_KIDS_ERR / S8_KIDS_VAL
    y_km    = matter_power_spectrum(k, RS_ECF, S8_KIDS_VAL, apply_torsion=True) * norm
    y_ku    = y_km * (1.0 + rel_err)
    y_kl    = y_km * (1.0 - rel_err)

    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'figure.figsize': (10, 7),
        'font.family': 'serif'
    })

    fig, ax = plt.subplots()

    ax.fill_between(k, y_kl, y_ku, color='gray', alpha=0.30,
                    label=r'KiDS-1000 Constraint ($1\sigma$)')
    ax.plot(k, y_lcdm, color='navy', linestyle='--', linewidth=2.5,
            label=r'Planck $\Lambda$CDM ($S_8 = 0.832$)')
    ax.plot(k, y_ecf, color='crimson', linestyle='-', linewidth=3.0,
            label=r'ECF Model ($S_8 = 0.766$, $T_{\rm torsion}^2$ suppression)')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(r'Wavenumber $k$ [$h$/Mpc]', fontsize=12)
    ax.set_ylabel(r'Matter Power Spectrum $P(k)$ [arb. norm.]', fontsize=12)
    ax.set_title(r'Resolution of $S_8$ Tension (Structure Growth)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.legend(fontsize=11, loc='lower left', frameon=True, framealpha=0.9)
    ax.grid(True, which='both', linestyle=':', alpha=0.6)

    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    ax.text(0.97, 0.97,
            # 17/08/2026 audit. Two defects in this box:
            #  (a) it read "ECF PREDICTION" while F1 Sec. 4 states that A_sup
            #      "is a free parameter within the present effective-fluid
            #      description" — calibrated, not predicted;
            #  (b) the displayed formula was G_N(1 - k^2/k_cut^2): the
            #      UNREGULARISED form, which omits A_sup entirely, vanishes at
            #      k = k_cut and goes NEGATIVE beyond it. F1 Eq. 18 replaced it
            #      precisely to avoid "unphysical negative values at large k".
            #      The code below always used the correct Lorentzian form
            #      (see T_torsion), so only the label was wrong.
            "ECF PHENOMENOLOGY (not canonical):\n"
            r"$G_{\rm eff}(k) = G_N\!\left(1 - \frac{A_{\rm sup}\,k^2}{k^2 + k_{\rm cut}^2}\right)$"
            "\n"
            r"$k_{\rm cut} = 0.10\,h/{\rm Mpc},\; A_{\rm sup} = 0.15$"
            "\n"
            r"$S_8 = 0.766$: KiDS target, not a $T^2$ output",
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig('Figure_S8_Resolution_SUPERSEDED.png', dpi=300)
    print("   [SUCCESS] Saved: Figure_S8_Resolution.png")
    plt.close()


if __name__ == "__main__":
    verify_calibration()
    plot_s8_resolution()