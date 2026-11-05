#!/usr/bin/env python3
# Last modified: 02/09/2026, 11:10 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
# =============================================================================
# plot_predict_birefringence_v2.py
# Figure figbirefringence -- Foundation I
# Tensions (fichant_ecf_F1_Extended_v2) -- Pascal Fichant, 21/04/2026
#
# Physics (Sec. secbirefringence):
#   I        = S_ref * int_0^{z_LSS} E(z)^{-1} dz = 4.32 * 3.118 = 13.48
#   g_CS_eff = beta_obs / I = 0.35 / 13.48 = 0.0260 deg
#   beta_ECF = g_CS_eff * I = 0.35 deg
#   k_obs    = beta_obs / F_ion = 0.35 / 1.2765 = 0.274 deg/unit
#   k_ECKS   = 0.27 deg/unit [Hehl1976]  -> 1.55% agreement ✓
#   n=0 resolution: k=0.274~k_ECKS; n=1 would require k=142 (excluded) ✓
#   sigma_LiteBIRD = 0.10 deg [LiteBIRD2023] -> 3.5 sigma discrimination vs LCDM
#   sigma_CMB_S4   = 0.07 deg [CMBS4]        -> 5.0 sigma discrimination vs LCDM
#
# LABELS — decision of 15/08/2026: the two sigma figures shown on the plot are
#   worded 'N sigma discrimination vs LCDM'. They are FORECAST discrimination
#   ratios against the null hypothesis beta = 0, NOT detection significances.
#   A bare 'N sigma' on a figure reads as a discovery threshold (a condensed
#   zone survives the caution of the surrounding text). The computation is
#   unchanged; only the display labels were reworded.
#
# CAVEAT, quoted from F1 Extended (Sec. secbirefringence) — 15/08/2026 audit:
#   beta_ECF is a CONSISTENCY CHECK, not a parameter-free prediction. The
#   paper states that the numerical proximity to Minami & Komatsu does not
#   by itself constitute a confirmation of the model, and that the figure
#   is an observational forecast, not a detection claim. The SNR figures
#   above are forecast discrimination ratios against the LCDM null, not
#   evidence.
#
# AUTHORITATIVE PRODUCER of Figure_Birefringence_Prediction.png (15/08/2026):
#   plot_birefringence_future.py used to write the same filename and has
#   been suffixed _SUPERSEDED. This script is the one to deposit.
#   [02/09/2026] RESOLVED: sigma_ECF is the traceable, correctly
#   propagated value (0.0206 then; 0.0246 since the provenance memo of
#   22/09/2026 replaced the untraced +-0.08 Gyr age constraint by
#   t_GC = 13.32 +- 0.10 stat, Valcin+2020), and F2 Extended has
#   been corrected to match. It is not plotted regardless (design decision of
#   15/08/2026, option b2 — see below).
# =============================================================================

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
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
MU_ECF         = 0.35   # ECF calibrated value = g_CS_eff * I [deg]  (15/08/2026: was "prediction")
# SIGMA_ECF — NO LONGER PLOTTED (decision of 15/08/2026, option b2).
#   beta_ECF is built as g_CS * I with g_CS = beta_obs / I, so it equals
#   beta_obs BY CONSTRUCTION (F1 Sec. birefringence: k = beta_obs/F_ion is a
#   derived quantity, "does not constitute an independent theoretical
#   cross-check"). It is an assumed non-zero value, not a prediction with a
#   variance of its own, so no error bar is drawn for it.
#   For the record, the only traceable propagation gives sigma_ECF = 0.014 deg:
#   sigma(F_ion) = sigma(H0)/slope = 1.04/20.398 = 0.051 from the two-point
#   F_ion<->H0 calibration (F1 App. F; former script
#   plot_Optimization_Intersection.py, archived as SUPERSEDED on 09/10/2026),
#   then sigma(beta) = k * sigma(F_ion) = 0.274 * 0.051. That band would be
#   ten times narrower than the +-0.14 deg measurement it is calibrated on,
#   which is why it is not shown.
#   [18/08/2026 correction] The earlier values 0.030 and 0.04 came from a
#   "+-0.02 on F_ion", which the 15/08 note called unsourced. It is in fact
#   the JOINT constraint: combining sigma(H0)/slope = 0.051 with the age
#   bound t_GC = 13.32 +- 0.10 stat Gyr (Valcin+2020; dt0/dF ~ -3.56 Gyr,
#   giving 0.028) yields 0.0246.
#   [P3, 22/09/2026 — provenance memo] The former +- 0.08 Gyr had no retrievable
#   source and gave 0.0206; the coincidence with the earlier "+-0.02 on F_ion"
#   is therefore no longer exact.
#   [02/09/2026 update] F2 Extended has now been corrected to match: it
#   published +-0.0030 for the same quantity (seven times smaller than this
#   traceable value), which did not reproduce from its own cited constraints.
#   F2 stated +-0.0206 (see ECF_PATCH_sigma_Fion_F2.md, applied), closing
#   the discrepancy this note used to flag; both now state +-0.0246.
SIGMA_ECF      = 0.0246  # kept for reference only; not used in the figure (see above)
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
         '#DAA520', '-.', 2.0, r'LiteBIRD forecast ($\sigma=0.10°$, $3.5\sigma$ discrimination vs $\Lambda$CDM)'),
        (norm.pdf(beta, MU_ECF,   SIGMA_S4),       MU_ECF,   SIGMA_S4,
         '#2ecc71', '--', 2.0, r'CMB-S4 forecast ($\sigma=0.07°$, $5.0\sigma$ discrimination vs $\Lambda$CDM)'),
    ]:
        ax.fill_between(beta, pdf, 0, color=color, alpha=0.13)
        ax.plot(beta, pdf, color=color, linestyle=ls, linewidth=lw, label=label)

    ax.axvline(0, color='royalblue', linestyle='--', linewidth=1.8,
               label=r'$\Lambda$CDM ($\beta=0$)')

    # ECF: a single calibrated value, deliberately drawn WITHOUT an error bar.
    # See the SIGMA_ECF note above: beta_ECF equals beta_obs by construction,
    # so it carries no variance of its own.
    ax.axvline(MU_ECF, color='#D00000', linestyle='-', linewidth=3.0,
               label=r'ECF: $\beta_{\rm ECF}=0.35°$ (calibrated on $\beta_{\rm obs}$,'
                     '\n' r'  assumed non-zero; no independent uncertainty)')

    ax.annotate(
        r'$\beta_{\rm ECF}=0.35°$' + '\n'
        r'$k_{\rm obs}=0.274\approx k_{\rm ECKS}=0.27$ ($1.6\%$)',
        xy=(MU_ECF, 9.0),
        xytext=(MU_ECF - 0.30, 11.5),
        fontsize=10.5, color='#D00000',
        arrowprops=dict(arrowstyle='->', color='#D00000', lw=1.2),
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#D00000', alpha=0.90))

    ax.set_xlim(-0.25, 0.85)
    ax.set_ylim(0, 16.5)
    ax.set_xlabel(r'Birefringence angle $\beta$ [deg]', fontweight='bold')
    ax.set_ylabel(r'Probability density [deg$^{-1}$]', fontweight='bold')
    # Title aligned on the F1 Extended caption (fig:birefringence, l.2184):
    # "Representative birefringence signal in the ECF."  15/08/2026 audit.
    ax.set_title('Representative Birefringence Signal in the ECF',
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
