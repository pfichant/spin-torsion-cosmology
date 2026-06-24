"""
================================================================================
SCRIPT: plot_21cm_prediction.py — v2
Paper: Foundation I: The Metric Universe (Extended), Sec. 3 & Sec. 7
Figure: fig21cmprediction — "21 cm prediction for the acoustic scale"
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Plots the ECF sound-horizon posterior alongside the Planck ΛCDM baseline,
  showing the contraction Δr_s = −11.3 Mpc that is the H0 resolution mechanism.
  Serves as the 21cm forecast target: if future HERA/SKA measurements confirm
  r_s ≈ 135.8 Mpc, this independently validates the ECF pre-recombination sector.

VALIDATION STATUS (independent audit, 2026-04-15):
  v1 → v2 corrections:
    1. mu_planck: 147.2 → 147.1 Mpc   (NUMERICAL FIX)
       Paper Sec. 3 and Tab. trilemma consistently state r_s(ΛCDM) = 147.1 Mpc.
       Planck 2018: r_s = 147.09 ± 0.26 Mpc → rounds to 147.1.
       v1 typo propagated to Δr_s = −11.4 instead of correct −11.3.
    2. sigma_planck: 0.3 → 0.26 Mpc   (NUMERICAL FIX)
       Planck 2018: σ(r_s) = 0.26 Mpc. v1 used 0.3 (inflated uncertainty).
    3. "STRONG TENSION (> 5σ)" label → "ECF contraction (H0 mechanism)"  (CONCEPTUAL FIX)
       The ECF r_s = 135.8 is a MODEL PREDICTION, not an independent measurement.
       The comparison is a model difference, not a data tension.
       Paper sec21cmprediction uses "shift" and "contracted acoustic scale" — never "tension".
    4. Double import block removed (matplotlib.use called twice in v1).
    5. Title: "21cm Forecast - Sound Horizon Shift" →
       "ECF Sound Horizon vs. Planck ΛCDM — 21cm Forecast Target"
       (clearer: plot shows the sound horizon, not a 21cm observable directly).

INPUTS (traceable to paper):
  RS_ECF    = 135.8 Mpc    paper Sec. 3, Eq. rsECF
  SIG_ECF   = 1.5 Mpc      paper sec21cmprediction: "1.5 Mpc uncertainty"
  RS_LCDM   = 147.1 Mpc    paper Sec. 3, Eq. rsCDM; Tab. trilemma; Planck 2018
  SIG_LCDM  = 0.26 Mpc     Planck 2018: 147.09 ± 0.26 Mpc
  DELTA_RS  = −11.3 Mpc    RS_ECF − RS_LCDM (derived)

PHYSICAL INTERPRETATION:
  The two distributions represent posterior inferences of r_s under two models:
    - Planck ΛCDM: r_s = 147.1 ± 0.26 Mpc (well-constrained, narrow)
    - ECF: r_s = 135.8 ± 1.5 Mpc (broader posterior from MCMC)
  The shift Δr_s = −11.3 Mpc is the ECF mechanism for solving the H0 tension:
  at fixed angular acoustic scale θ_s = r_s/D_A, a smaller r_s requires a
  larger H0 to maintain θ_s consistent with CMB peak positions.
  The 21cm connection: BAO surveys using 21cm intensity mapping will measure
  r_s(z) through the neutral hydrogen large-scale structure. If they confirm
  r_s ~ 136 Mpc instead of 147 Mpc, this validates the ECF pre-recombination
  sector independently of the CMB distance ladder.

Cross-reference: paper Sec. 3, Sec. 7 (sec21cmprediction), Tab. trilemma
================================================================================
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm

# =============================================================================
# 1. PARAMETERS
# =============================================================================
RS_ECF   = 135.8;  SIG_ECF   = 1.5    # Mpc — paper Sec. 3, sec21cmprediction
RS_LCDM  = 147.1;  SIG_LCDM  = 0.26   # Mpc — Planck 2018: 147.09 ± 0.26
DELTA_RS = RS_ECF - RS_LCDM            # = -11.3 Mpc (paper: ~-11.3 Mpc)


# =============================================================================
# 2. STYLE
# =============================================================================
plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 13,
    'figure.figsize': (10, 6), 'font.family': 'serif'
})


# =============================================================================
# 3. PLOT
# =============================================================================
def plot_21cm_prediction():
    print(">>> Generating Figure (fig21cmprediction): 21cm Sound Horizon Forecast...")

    x = np.linspace(130, 155, 1000)
    pdf_ecf  = norm.pdf(x, RS_ECF,  SIG_ECF)
    pdf_lcdm = norm.pdf(x, RS_LCDM, SIG_LCDM)

    fig, ax = plt.subplots(figsize=(10, 6))

    # ECF posterior
    ax.plot(x, pdf_ecf,  color='#D00000', lw=3, label=f'ECF Prediction  r_s = {RS_ECF} ± {SIG_ECF} Mpc')
    ax.fill_between(x, pdf_ecf, 0, color='#D00000', alpha=0.15)
    ax.text(RS_ECF, max(pdf_ecf) + 0.04, f'{RS_ECF} Mpc',
            ha='center', color='#D00000', fontweight='bold', fontsize=12)

    # Planck ΛCDM baseline
    ax.plot(x, pdf_lcdm, color='royalblue', lw=2, ls='--',
            label=rf'Planck $\Lambda$CDM  r_s = {RS_LCDM} ± {SIG_LCDM} Mpc')
    ax.fill_between(x, pdf_lcdm, 0, color='royalblue', alpha=0.08)
    ax.text(RS_LCDM, max(pdf_lcdm) + 0.04, f'{RS_LCDM} Mpc',
            ha='center', color='royalblue', fontsize=12)

    # Shift arrow
    arrow_y = 0.13
    ax.annotate('', xy=(RS_ECF, arrow_y), xytext=(RS_LCDM, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))

    # Delta label (model difference — NOT a "tension")
    mid = (RS_ECF + RS_LCDM) / 2
    ax.text(mid, arrow_y + 0.018, rf'$\Delta r_s = {DELTA_RS:.1f}$ Mpc',
            ha='center', fontsize=12, fontweight='bold', backgroundcolor='white')

    # Physical label — replaces misleading "STRONG TENSION" of v1
    ax.text(mid, arrow_y - 0.065,
            r'ECF contraction — H$_0$ resolution mechanism',
            ha='center', color='#800000', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#800000', lw=1.5))

    ax.set_xlim(129, 156)
    ax.set_ylim(0, max(pdf_lcdm) * 1.20)
    ax.set_xlabel(r'Comoving Sound Horizon $r_s$ [Mpc]')
    ax.set_ylabel('Probability Density')
    ax.set_title(r'ECF Sound Horizon vs. Planck $\Lambda$CDM — 21cm Forecast Target',
                 fontsize=13, fontweight='bold', pad=12)
    ax.legend(loc='upper left')
    ax.grid(True, ls=':', alpha=0.5)

    plt.tight_layout()
    out = 'Figure_21cm_ECF_Prediction.png'
    plt.savefig(out, dpi=300)
    print(f"   [SUCCESS] Saved: {out}")
    print(f"   r_s(ECF)  = {RS_ECF} ± {SIG_ECF} Mpc")
    print(f"   r_s(ΛCDM) = {RS_LCDM} ± {SIG_LCDM} Mpc  (Planck 2018)")
    print(f"   Δr_s      = {DELTA_RS:.1f} Mpc  (paper: -11.3 Mpc ✓)")
    plt.close()


if __name__ == "__main__":
    plot_21cm_prediction()
