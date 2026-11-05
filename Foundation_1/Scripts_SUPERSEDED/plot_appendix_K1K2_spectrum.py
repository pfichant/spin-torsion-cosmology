# Last modified: 21/08/2026, 16:05 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
r"""
plot_appendix_K1K2_spectrum.py
    [SUPERSEDED 17/08/2026 — DO NOT USE FOR ANY PAPER FIGURE]

    This script no longer produces any figure used by Foundation I. Both of
    its outputs were duplicates written by other, authoritative scripts:

      K3 -> removed on 15/08/2026 (see the audit note further down).
            Authoritative: plot_Fig_k3_Residuals_Angles.py
      K1 -> output filename suffixed _SUPERSEDED on 17/08/2026.
            Authoritative: plot_Figure_K1_Global_Consistency.py

    Why this script is not the reference for K1. It keeps d_ECF = 1360 and
    noise floor = 40, whereas plot_Figure_K1_Global_Consistency.py was
    corrected to d_ECF = 1320 and floor = 50 back in April 2026, with the
    reason stated in its own header: "v1 used 1360, which was inconsistent
    with the 5.7% reduction required by Table K". Replaying the heuristic
    formula against the four Table K points (deficits -5.2 / -6.5 / -3.0 /
    -2.5 % at l = 1500 / 2000 / 2500 / 3000) confirms it: {1320, 50}
    reproduces all four to within 0.1 point; {1360, 40} yields half the
    deficit. The two scripts wrote the SAME filename, so whichever ran last
    silently overwrote the other.

    Kept locally for its version history and audit trail. NOT to be included
    in the public repository.
================================================================================
SCRIPT: plot_appendix_K1K2_spectrum.py — v2
Paper: Foundation I (Extended), Appendix K
Figures: figk1global (K1) only  [K3 retiree le 15/08/2026 — voir note d'audit]
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Generates two illustrative CMB temperature power-spectrum figures for Appendix K:
    K1 — Global geometric consistency (figk1global):
         ECF vs Planck ΛCDM over the full multipole range ℓ ∈ [20, 2500].
         Peak positions preserved: θ_s = r_s/D_A is held fixed (smaller r_s,
         smaller D_A), so acoustic peaks remain at the same ℓ in both models.
    (K3 was produced here until 15/08/2026; removed as a duplicate — see the
     audit note further down. plot_Fig_k3_Residuals_Angles.py is authoritative.)

⚠  IMPORTANT NOTE FOR REFEREE (traceable to paper Appendix K):
   These figures use a HEURISTIC spectrum formula, NOT a full Boltzmann solver.
   The formula   D_ℓ = 5000·(ℓ/100)^{-0.6}·exp(−ℓ/ℓ_D)·cos²(πℓ/220) + floor
   is intended for visual illustration of the damping-tail deficit direction only.
   It does NOT reproduce the exact values in Table tabforecastk (Appendix K).
   Reference values from Table tabforecastk:
     ℓ=1500: D_ℓ(ΛCDM)=288.6, D_ℓ(ECF)=273.6, Gap=−5.2%
     ℓ=2000: D_ℓ(ΛCDM)=232.7, D_ℓ(ECF)=217.6, Gap=−6.5%
     ℓ=2500: D_ℓ(ΛCDM)= 71.0, D_ℓ(ECF)= 68.9, Gap=−3.0%
     ℓ=3000: D_ℓ(ΛCDM)= 63.2, D_ℓ(ECF)= 61.6, Gap=−2.5%
   A first-principles Boltzmann computation is deferred to Foundation III
   (CLASS-EC modification).  These figures serve as Appendix K illustration only.

VALIDATION STATUS (independent audit, 2026-04-15):
  v1 → v2 corrections:
    1. CMB-S4 sensitivity: 0.01 (1%) → 0.015 (1.5%)            [NUMERICAL FIX]
       Paper Appendix K: "CMB-S4 expected to reach σ_S4 ≈ 1.5%".
    2. Noise floor: +200 μK² → +40 μK²                          [NUMERICAL FIX]
       +200 dominated high-ℓ values and masked the ECF−ΛCDM gap.
       At ℓ=2500 the ECF gap was −0.5% (script) vs −3.0% (paper). Reduced to +40.
    3. np.random.seed(42) added before noise generation           [REPRO FIX]
       Without seed, K1 mock data points changed on every run.
    4. K2 renamed to K3 / figk3prediction                        [WITHDRAWN 15/08/2026:
       this rename was made on the wrong premise — the paper body did include a
       K2 figure at the time. That figure has since been removed from the body.]
       Paper Appendix K has figk1global and figk3prediction/fighighldamping.
       There is no explicit "K2" in the paper. Script v1 called it K2.
    5. Missing residuals panel (ΔD_ℓ) added to K3               [CONTENT FIX]
       Paper figk3prediction caption: "Bottom Panel: The residual ΔD_ℓ.
       The predicted deficit extends beyond the forecasted sensitivity of
       CMB-S4 (green band, 1σ)." Script v1 had only the top panel.
    6. Raw-string LaTeX escapes: r'...\\Lambda...' → r'...$\Lambda$...'  [STYLE]
    7. Removed double import block (matplotlib.use called twice in v1).
    8. Heuristic disclaimer added prominently (this docstring).
    9. Paper table anchor values plotted as markers in K3 for traceability.

INPUTS (traceable to paper):
  L_PEAK      = 220        standard first acoustic peak multipole
  DS_LCDM     = 1400       Silk damping scale ΛCDM (standard)
  DS_ECF      = 1360       Silk damping scale ECF (Δzrec≈22, Appendix K)
  SIGMA_CMBS4 = 0.015      CMB-S4 relative sensitivity (paper Appendix K: 1.5%)
  NOISE_FLOOR = 40         reduced from v1's 200 μK²
  RANDOM_SEED = 42         reproducibility of K1 mock data

Physical basis of DS_ECF:
  Paper Appendix K states Δzrec ≈ 22 from the torsion-modified recombination history.
  The photon diffusion (Silk) scale r_D ∝ ∫ dτ/τ_C. A shift Δzrec=22 modifies
  this integral, reducing the effective damping multipole from ~1400 to ~1360
  (ratio 0.971, consistent with the 2.9% reduction shown by the formula).
================================================================================
"""

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

plt.rcParams.update({'font.family': 'serif', 'font.size': 11,
                     'axes.labelsize': 12, 'figure.dpi': 150})

# =============================================================================
# 1. PARAMETERS
# =============================================================================
L_PEAK      = 220          # standard first acoustic peak multipole
DS_LCDM     = 1400         # Silk damping scale ΛCDM
DS_ECF      = 1360         # Silk damping scale ECF (paper Appendix K: Δzrec≈22)
SIGMA_CMBS4 = 0.015        # CMB-S4 relative sensitivity (paper: 1.5%)
NOISE_FLOOR = 40           # μK² — reduced from v1's 200 (which masked ECF gap)
RANDOM_SEED = 42

# Paper Table tabforecastk — used as anchor markers in K3
PAPER_TABLE = {
    1500: (273.6, 288.6, -5.2),
    2000: (217.6, 232.7, -6.5),
    2500: ( 68.9,  71.0, -3.0),
    3000: ( 61.6,  63.2, -2.5),
}

# =============================================================================
# 2. HEURISTIC SPECTRUM MODEL
# =============================================================================
def spectrum(ell, ds):
    """Heuristic illustrative CMB TT spectrum. NOT a Boltzmann-code output.
    See module docstring for caveats and paper Table tabforecastk for
    the reference values that a full Boltzmann solver would reproduce."""
    osc = np.cos(np.pi * ell / L_PEAK)**2
    return 5000 * (ell / 100)**(-0.6) * np.exp(-ell / ds) * osc + NOISE_FLOOR

def l2theta(l): return 180.0 / (l + 1e-10)
def theta2l(t): return 180.0 / (t + 1e-10)

ell_full = np.linspace(2, 3000, 1500)
dl_lcdm  = spectrum(ell_full, DS_LCDM)
dl_ecf   = spectrum(ell_full, DS_ECF)

# =============================================================================
# 3. FIGURE K1 — figk1global
# =============================================================================
def generate_figure_K1():
    print(">>> Generating Figure K1 (figk1global): Global Consistency...")
    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(ell_full, dl_lcdm, color='royalblue', ls='--', lw=2,
            label=r'Planck $\Lambda$CDM ($H_0 = 67.4$ km/s/Mpc)')
    ax.plot(ell_full, dl_ecf,  color='#C00000',   lw=2,
            label=r'ECF Spin-Torsion ($H_0 = 73.0$ km/s/Mpc)')

    np.random.seed(RANDOM_SEED)
    s_ell  = np.geomspace(50, 2400, 28)
    s_dl   = np.interp(s_ell, ell_full, dl_lcdm)
    errors = s_dl * 0.04 * (s_ell / 1000)**0.5
    noise  = np.random.normal(0, s_dl * 0.04)
    ax.errorbar(s_ell, s_dl + noise, yerr=errors, fmt='o',
                color='black', alpha=0.35, ms=3,
                label=f'Planck 2018 mock data (seed={RANDOM_SEED})')

    ax.set_xlim(20, 2500);  ax.set_ylim(0, 6500)
    ax.set_xlabel(r'Multipole $\ell$')
    ax.set_ylabel(r'$\mathcal{D}_\ell^{TT}\ [\mu\mathrm{K}^2]$')
    ax.set_title('K1 — Global Geometric Consistency  (figk1global)',
                 fontweight='bold', pad=10)
    ax.legend(loc='upper right', fontsize=9.5)
    ax.grid(True, ls=':', alpha=0.45)

    ax2 = ax.secondary_xaxis('top', functions=(l2theta, theta2l))
    ax2.set_xlabel('Angular Scale [deg]', fontsize=10)
    ax2.set_ticks([1, 0.5, 0.2, 0.1])
    ax2.set_xticklabels(['1°', '0.5°', '0.2°', '0.1°'])

    plt.tight_layout()
    plt.savefig('Figure_K1_Global_Consistency_SUPERSEDED.png', dpi=300)
    print("   [SUCCESS] Saved: Figure_K1_Global_Consistency_SUPERSEDED.png")
    plt.close()

# =============================================================================
# NOTE D'AUDIT (15/08/2026) — la figure K3 a ete RETIREE de ce script.
# Elle etait un DOUBLON de plot_Fig_k3_Residuals_Angles.py, avec des parametres
# divergents : d_ECF = 1360 et plancher = 40 ici, contre 1320 et 50 la-bas.
# Test contre la Table K de F1 (deficits -5.2 / -6.5 / -3.0 / -2.5 % a
# l = 1500 / 2000 / 2500 / 3000) : le jeu {1320, 50} reproduit les quatre
# valeurs a 0.1 point pres ; le jeu {1360, 40} donne la moitie du deficit.
# plot_Fig_k3_Residuals_Angles.py fait donc foi pour K3, et produit le seul
# fichier utilise par le papier (Figure_K3_Residuals_Angles.png).
# Ce script ne produit plus que K1.
# =============================================================================

if __name__ == "__main__":
    generate_figure_K1()
