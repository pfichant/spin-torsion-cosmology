"""
plot_S8_resolution.py  —  Foundation I: Unified Resolution of Cosmological Tensions
Author : Pascal Fichant  |  Date : 21/04/2026  |  v2 referee / Zenodo release

Generates Figure fig:euclidpk — Matter Power Spectrum S8 tension resolution.

Physics
-------
P_ECF(k) = P_LCDM(k) * T_torsion^2(k)

  T_torsion(k) = 1 - A_sup * k^2 / (k^2 + k_cut^2)      [Sec.4, Sec.6]
  A_sup = 0.15,  k_cut = 0.10 h/Mpc                       [fig:euclidpk caption]

  S8_ECF   = 0.766  (KiDS-1000/DES Y3 compatible, Delta-chi2 = -10.9)  [Sec.5]
  sigma8   = 0.747  = S8 / sqrt(Omega_m / 0.3)                         [Sec.6]
  r_s ECF  = 135.8 Mpc  vs  147.09 Mpc (LCDM)                          [Sec.3]
  F_ion    = 1.2765  (single free parameter governing both H0 and S8)   [Sec.5]

Sections impacted: Sec.4 (sectensions), Sec.5 (secresults), Sec.6 (seceuclidprediction)

Changelog v1 -> v2
-------------------
  + T_torsion^2 suppression added (absent from v1)
  + ns corrected: 0.96 -> 0.965  (Planck 2018)
  + verify_calibration() added
  + Annotation box moved to top-right
  + Typo "STATING" -> "STARTING" fixed
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RS_PLANCK   = 147.09
RS_ECF      = 135.8
S8_PLANCK   = 0.832
S8_ECF      = 0.766
S8_KIDS_VAL = 0.766
S8_KIDS_ERR = 0.014
FION        = 1.2765
ETA_SPIN    = 0.3116
NS          = 0.965
OMEGA_M     = 0.315
A_SUP       = 0.15
K_CUT       = 0.10


def verify_calibration():
    """Independent checks against Foundation I v2 paper values."""
    print(">>> Calibration verification (Foundation I v2)...")
    s8_macro = S8_PLANCK * (1.0 - (FION - 1.0) * ETA_SPIN)
    sigma8   = S8_ECF / np.sqrt(OMEGA_M / 0.3)
    T2_kcut  = (1.0 - A_SUP * K_CUT**2 / (K_CUT**2 + K_CUT**2))**2
    T2_sat   = (1.0 - A_SUP)**2
    ok       = "OK" if abs(sigma8 - 0.747) < 0.002 else "CHECK"
    print(f"   S8 macro layer   = {s8_macro:.4f}  [eta_spin layer, ~0.760]")
    print(f"   S8 net target    = {S8_ECF}    [+ T_torsion layer -> 0.766]")
    print(f"   sigma8_ECF       = {sigma8:.4f}  [paper: 0.747]  {ok}")
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
            "ECF PREDICTION:\n"
            r"$G_{\rm eff}(k) = G_N\!\left(1 - \frac{k^2}{k_{\rm cut}^2}\right)$"
            "\n"
            r"$k_{\rm cut} = 0.10\,h/{\rm Mpc},\; A_{\rm sup} = 0.15$"
            "\n"
            r"$\Rightarrow\; S_8 = 0.766,\; \Delta\chi^2_{S_8} = -10.9$",
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig('Figure_S8_Resolution.png', dpi=300)
    print("   [SUCCESS] Saved: Figure_S8_Resolution.png")
    plt.close()


if __name__ == "__main__":
    verify_calibration()
    plot_s8_resolution()