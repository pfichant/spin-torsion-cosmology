#!/usr/bin/env python3
# =============================================================================
# plot_predict_birefringence_v2.py
# Figure figbirefringence -- Foundation I: Unified Resolution of Cosmological
# Tensions (fichant_ecf_F1_Extended_v2) -- Pascal Fichant, 21/04/2026
#
# Physics (Sec. secbirefringence):
#   I        = S_ref * int_0^{z_LSS} E(z)^{-1} dz = 4.32 * 3.118 = 13.48
#   g_CS_eff = beta_obs / I = 0.35 / 13.48 = 0.0260 deg
#   beta_ECF = g_CS_eff * I = 0.35 deg
#   k_obs    = beta_obs / F_ion = 0.35 / 1.2765 = 0.274 deg/unit
#   k_ECKS   = 0.27 deg/unit [Hehl1976]  -> 1.55% agreement ✓
#   n=0 resolution: k=0.274~k_ECKS; n=1 would require k=142 (excluded) ✓
#   sigma_LiteBIRD = 0.10 deg [LiteBIRD2023] -> SNR = 3.5 sigma
#   sigma_CMB_S4   = 0.07 deg [CMBS4]        -> SNR = 5.0 sigma
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import norm

matplotlib.use('Agg')
plt.rcParams.update({'font.size': 13, 'axes.labelsize': 15,
                     'xtick.labelsize': 12, 'ytick.labelsize': 12,
                     'font.family': 'serif', 'axes.linewidth': 1.5})

# --- Physical constants (Sec. secbirefringence) ---
MU_OBS         = 0.35   # Planck [Minami & Komatsu 2020, deg]
SIGMA_OBS      = 0.14   # [deg]
MU_ECF         = 0.35   # ECF prediction = g_CS_eff * I [deg]
SIGMA_ECF      = 0.030  # propagated from F_ion uncertainty +-0.02 [deg]
SIGMA_LITEBIRD = 0.10   # LiteBIRD 1-sigma [LiteBIRD2023, deg]
SIGMA_S4       = 0.07   # CMB-S4 1-sigma [CMBS4, deg]


def verify_calibration():
    I_F      = 13.48
    g_cs     = MU_OBS / I_F
    k_obs    = MU_OBS / 1.2765
    k_ecks   = 0.27
    print(f"g_CS_eff = {g_cs:.4f} deg  [paper: 0.0260] {'OK' if abs(g_cs-0.026)<1e-3 else 'FAIL'}")
    print(f"beta_ECF = {g_cs*I_F:.4f} deg  [paper: 0.35]   {'OK' if abs(g_cs*I_F-0.35)<0.005 else 'FAIL'}")
    print(f"k_obs    = {k_obs:.4f}       [paper: 0.274]  {'OK' if abs(k_obs-0.274)<0.002 else 'FAIL'}")
    print(f"k_ECKS   diff = {100*abs(k_obs-k_ecks)/k_ecks:.2f}%  [paper: <1.6%]  {'OK' if 100*abs(k_obs-k_ecks)/k_ecks<1.6 else 'FAIL'}")
    print(f"SNR LiteBIRD = {MU_ECF/SIGMA_LITEBIRD:.1f} sigma  [paper: 3.5] {'OK' if abs(MU_ECF/SIGMA_LITEBIRD-3.5)<0.05 else 'FAIL'}")
    print(f"SNR CMB-S4   = {MU_ECF/SIGMA_S4:.1f} sigma  [paper: 5.0] {'OK' if abs(MU_ECF/SIGMA_S4-5.0)<0.05 else 'FAIL'}")


def plot_birefringence(outfile="Figure_Birefringence_Prediction.png"):
    beta = np.linspace(-0.25, 0.85, 1000)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    plt.subplots_adjust(left=0.10, right=0.72, top=0.91, bottom=0.13)

    for pdf, mu, sig, color, ls, lw, label in [
        (norm.pdf(beta, MU_OBS,   SIGMA_OBS),      MU_OBS,   SIGMA_OBS,
         '#444444', ':',  2.2, 'Planck 2018 (Minami & Komatsu 2020)\n'
                              r'  $\mu=0.35°,\ \sigma=0.14°$'),
        (norm.pdf(beta, MU_ECF,   SIGMA_LITEBIRD), MU_ECF,   SIGMA_LITEBIRD,
         '#DAA520', '-.', 2.0, r'LiteBIRD forecast ($\sigma=0.10°$, $3.5\sigma$)'),
        (norm.pdf(beta, MU_ECF,   SIGMA_S4),       MU_ECF,   SIGMA_S4,
         '#2ecc71', '--', 2.0, r'CMB-S4 forecast ($\sigma=0.07°$, $5.0\sigma$)'),
        (norm.pdf(beta, MU_ECF,   SIGMA_ECF),      MU_ECF,   SIGMA_ECF,
         '#D00000', '-',  3.2, r'ECF prediction ($\beta_{\rm ECF}=0.35°$, $\sigma=0.030°$)'),
    ]:
        ax.fill_between(beta, pdf, 0, color=color, alpha=0.13)
        ax.plot(beta, pdf, color=color, linestyle=ls, linewidth=lw, label=label)

    ax.axvline(0, color='royalblue', linestyle='--', linewidth=1.8,
               label=r'$\Lambda$CDM ($\beta=0$)')

    ax.annotate(
        r'$\beta_{\rm ECF}=0.35°$' + '\n'
        r'$k_{\rm obs}=0.274\approx k_{\rm ECKS}=0.27$ ($1.6\%$)',
        xy=(MU_ECF, norm.pdf(MU_ECF, MU_ECF, SIGMA_ECF)),
        xytext=(MU_ECF - 0.21, norm.pdf(MU_ECF, MU_ECF, SIGMA_ECF) - 2.8),
        fontsize=10.5, color='#D00000',
        arrowprops=dict(arrowstyle='->', color='#D00000', lw=1.2),
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#D00000', alpha=0.90))

    ax.set_xlim(-0.25, 0.85)
    ax.set_ylim(0, 16.5)
    ax.set_xlabel(r'Birefringence angle $\beta$ [deg]', fontweight='bold')
    ax.set_ylabel(r'Probability density [deg$^{-1}$]', fontweight='bold')
    ax.set_title(r'Cosmic Birefringence: ECF Prediction vs Observations \& Forecasts',
                 fontsize=14, fontweight='bold', pad=10)
    ax.grid(True, linestyle=':', alpha=0.55)
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0),
              frameon=True, framealpha=0.95, fontsize=11,
              borderpad=0.8, handlelength=2.2, labelspacing=0.9)

    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved: {outfile}")
    plt.close()


if __name__ == "__main__":
    verify_calibration()
    plot_birefringence()
