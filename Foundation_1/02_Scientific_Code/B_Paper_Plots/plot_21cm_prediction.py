"""
================================================================================
SCRIPT: plot_21cm_prediction.py — v2
Paper: Foundation I (Extended), Sec. 3 & Sec. 7
Figure: fig21cmprediction — "21 cm prediction for the acoustic scale"
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Plots the ECF sound-horizon posterior alongside the Planck ΛCDM baseline,
  showing the contraction Δr_s = −11.45 Mpc (A-6; −11.3 with the former 135.8)
  that is the r_s reduction mechanism. Serves as the 21cm forecast target: a
  future HERA/SKA measurement of r_s would provide a consistency test of the ECF
  pre-recombination calibration. [02/10/2026] r_s = 135.65 Mpc is the CALIBRATION
  TARGET (it jointly fixes Omega_spin^peak and tau_tor, F1 l.1782-1789), not an independent
  prediction; the +/- 1.5 Mpc is an ILLUSTRATIVE width (the MCMC posterior is not
  reproducible from the deposited scripts, F1 l.3268-3272).

VALIDATION STATUS (independent audit, 2026-04-15):
  v1 → v2 corrections:
    1. mu_planck: 147.2 → 147.1 Mpc   (NUMERICAL FIX)
       Paper Sec. 3 and Tab. trilemma consistently state r_s(ΛCDM) = 147.1 Mpc.
       Planck 2018: r_s = 147.09 ± 0.26 Mpc → rounds to 147.1.
       v1 typo propagated to Δr_s = −11.4 instead of correct −11.3.
    2. sigma_planck: 0.3 → 0.26 Mpc   (NUMERICAL FIX)
       Planck 2018: σ(r_s) = 0.26 Mpc. v1 used 0.3 (inflated uncertainty).
    3. "STRONG TENSION (> 5σ)" label → "ECF contraction (H0 mechanism)"  (CONCEPTUAL FIX)
       The ECF r_s = 135.65 (A-6) is a CALIBRATED VALUE (target), not an independent measurement
       nor an independent prediction [02/10/2026; was "MODEL PREDICTION"].
       The comparison is a model difference, not a data tension.
       Paper sec21cmprediction uses "shift" and "contracted acoustic scale" — never "tension".
    4. Double import block removed (matplotlib.use called twice in v1).
    5. Title: "21cm Forecast - Sound Horizon Shift" →
       "ECF Sound Horizon vs. Planck ΛCDM — 21cm Forecast Target"
       (clearer: plot shows the sound horizon, not a 21cm observable directly).

INPUTS (traceable to paper):
  RS_ECF    = 135.65 Mpc   paper Sec. 3, Eq. rsECF (A-6)
  SIG_ECF   = 1.5 Mpc      paper sec21cmprediction: "1.5 Mpc uncertainty"
  RS_LCDM   = 147.1 Mpc    paper Sec. 3, Eq. rsCDM; Tab. trilemma; Planck 2018
  SIG_LCDM  = 0.26 Mpc     Planck 2018: 147.09 ± 0.26 Mpc
  DELTA_RS  = −11.45 Mpc   RS_ECF − RS_LCDM (derived; −11.3 with the former 135.8)

PHYSICAL INTERPRETATION:
  The two distributions represent r_s under two models (ECF: calibrated value, illustrative width):
    - Planck ΛCDM: r_s = 147.1 ± 0.26 Mpc (well-constrained, narrow)
    - ECF: r_s = 135.65 ± 1.5 Mpc (calibrated value; illustrative width, not a reproducible posterior)
  The shift Δr_s = −11.45 Mpc (A-6) is the ECF r_s reduction mechanism for the H0 tension:
  at fixed angular acoustic scale θ_s = r_s/D_A, a smaller r_s requires a
  larger H0 to maintain θ_s consistent with CMB peak positions.
  The 21cm connection: BAO surveys using 21cm intensity mapping will measure
  r_s(z) through the neutral hydrogen large-scale structure. If they confirm
  r_s ~ 136 Mpc instead of 147 Mpc, this would be a consistency test of the ECF
  pre-recombination calibration through a channel independent of the CMB distance ladder.

Cross-reference: paper Sec. 3, Sec. 7 (sec21cmprediction), Tab. trilemma
================================================================================
"""
# Last modified: 21/08/2026, 16:05 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm

# =============================================================================
# 1. PARAMETERS
# =============================================================================
RS_ECF   = 135.65;  SIG_ECF   = 1.5   # [A-6] was 135.8    # Mpc — paper Sec. 3, sec21cmprediction
RS_LCDM  = 147.1;  SIG_LCDM  = 0.26   # Mpc — Planck 2018: 147.09 ± 0.26
DELTA_RS = RS_ECF - RS_LCDM            # = -11.45 Mpc (A-6; -11.3 with the former 135.8)


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
    ax.plot(x, pdf_ecf,  color='#D00000', lw=3, label=f'ECF calibrated value  r_s = {RS_ECF} ± {SIG_ECF} Mpc (illustrative width)')
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
    arrow_y = 0.60
    ax.annotate('', xy=(RS_ECF, arrow_y), xytext=(RS_LCDM, arrow_y),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))

    # Delta label (model difference — NOT a "tension")
    mid = (RS_ECF + RS_LCDM) / 2
    ax.text(mid, arrow_y + 0.04, rf'$\Delta r_s = {DELTA_RS:.2f}$ Mpc',
            ha='center', fontsize=12, fontweight='bold', backgroundcolor='white')

    # Physical label — replaces misleading "STRONG TENSION" of v1
    ax.text(mid - 2.5, arrow_y - 0.14,
            # 17/08/2026 audit: read « H_0 resolution mechanism ». The corpus
            # removed verdict wording (« resolution », « resolves ») from the
            # .tex on 12/08; this annotation had kept it. F1 §3 calls the same
            # thing the « sound horizon reduction mechanism », which is what is
            # actually shown here — a contraction of r_s, not a resolution.
            r'ECF contraction — $r_s$ reduction mechanism (F1 §3)',
            ha='center', color='#800000', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#800000', lw=1.5))

    ax.set_xlim(129, 156)
    ax.set_ylim(0, max(pdf_lcdm) * 1.45)
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
    print(f"   Δr_s      = {DELTA_RS:.2f} Mpc  (= RS_ECF - RS_LCDM, computed; -11.3 with the former"
          f" r_s = 135.8, A-6)")   # [D3, 22/09/2026] was a hard-coded "(paper: -11.3 Mpc ✓)"
    plt.close()


if __name__ == "__main__":
    plot_21cm_prediction()
