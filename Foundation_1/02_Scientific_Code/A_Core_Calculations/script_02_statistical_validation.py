"""
================================================================================
SCRIPT 02 v2: S8 TENSION & STATISTICAL VALIDATION
Paper: Foundation I — The Metric Universe (Extended)
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Computes the S8 tension resolution via torsion-induced structure suppression.
  Evaluates the two-dataset Chi-square proxy (H0 + S8) of the ECF model
  against the standard Lambda-CDM baseline.

SCOPE:
  This script is a 2-observable proxy {H0, S8}.
  The full multi-dataset budget (Planck + BAO + eBOSS + SH0ES + WL)
  yielding Delta-chi2 = -39.5 is computed in chicarre.py (public repository).
  Results here are a transparent, self-contained sanity check.

VALIDATION STATUS (independent audit, 2026-04-14):
  v1 → v2 corrections:
    1. sigma_S8 : 0.014 → 0.019  (combined obs+theory, consistent with
                                   paper Table 6 chi2_S8_LCDM = 12.1)
    2. ndof     : 1    → 2       (2 observables compared, not 1 extension)
    3. Added uncertainty propagation on S8_ECF (±0.0078, paper: ±0.008)
    4. All inputs traced to explicit literature references

INPUTS (traceable to literature):
  H0_obs  = 73.04 ± 1.04  km/s/Mpc   SH0ES 2022 (Riess et al. 2022, ApJ 934 L7)
  S8_obs  = 0.766 ± 0.019            KiDS-1000 3x2pt (Heymans+2021)
                                      sigma = combined obs+theory
  H0_LCDM = 67.4  km/s/Mpc           Planck 2018 (Planck Collaboration 2020)
  S8_LCDM = 0.832                     Planck 2018 (Planck Collaboration 2020)
  F_ion   = 1.2765                    ECF effective amplitude, calibrated on rs (Sec. 3)
  gamma   = 0.3116 +0.073/-0.100     Spin-growth coupling, calibrated on S8 = 0.766 (KiDS-1000 3x2pt);
                                      interval propagates S8_obs only (gamma_spin_calibration.py). No MCMC.
                                      HISTORICAL CALIBRATION (S8_LCDM = 0.832, former Planck background,
                                      Omega_m = 0.315): withdrawn as canonical post-A-7 (DEC-A7-POST-07A).
                                      The proxy below therefore belongs to the historical chain.

FORMULA (Eq. 11, Sec. 4):
  S8_ECF = S8_LCDM / [1 + (F_ion - 1) * gamma_spin]
================================================================================
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
from scipy import stats


# =============================================================================
# 1. OBSERVATIONAL CONSTRAINTS
# =============================================================================
H0_OBS     = 73.04   # km/s/Mpc  — SH0ES 2022 (Riess et al. 2022)
H0_OBS_SIG = 1.04    # 1-sigma

S8_OBS     = 0.766   # KiDS-1000 3x2pt
S8_OBS_SIG = 0.019   # combined obs+theory sigma (consistent with paper Table 6)


# =============================================================================
# 2. MODEL PREDICTIONS
# =============================================================================
# Lambda-CDM — Planck 2018 baseline
H0_LCDM = 67.4
S8_LCDM = 0.832

# ECF model
H0_ECF     = 73.04
F_ION      = 1.2765   # effective amplitude, fixed on r_s (H0 sector). [E2, 22/09/2026] The former
                      # "single dof for H0 and S8" reading is withdrawn (DEC-A7-POST-07)
GAMMA_SPIN = 0.3116   # Spin-growth coupling -- calibrated by inversion on S8 = 0.766 (KiDS-1000 3x2pt); no MCMC;
                      # HISTORICAL CALIBRATION, withdrawn as canonical post-A-7 (DEC-A7-POST-07A)
# [D3, 22/09/2026 -- DEC-A7-POST-05] Was GAMMA_SIG = 0.04 ("Table 2"), a value no
# producer supports. The producer (Audit_v2/lot_SPARC_22-09/gamma_spin/
# gamma_spin_calibration.py) gives +0.073/-0.100, propagating S8_obs only.
GAMMA_SIG_PLUS  = 0.073
GAMMA_SIG_MINUS = 0.100
GAMMA_SIG  = GAMMA_SIG_MINUS   # symmetric bound = widest side (linear propagation below)


# =============================================================================
# 3. S8 SUPPRESSION  (Eq. 11, Sec. 4)
# =============================================================================
def compute_s8_suppression(s8_ref, f_ion, gamma):
    """
    S8_ECF = S8_LCDM / [1 + (F_ion - 1) * gamma_spin]

    The residual torsion-matter coupling induces a scale-dependent suppression
    of structure growth via Geff(k) < GN for k > k_cut. In this historical
    calibration F_ion (fixed on the sound horizon) and gamma_spin (calibrated
    on S8) enter the same denominator, which ties the two sectors at the
    calibration stage only. It does not establish that one parameter treats
    H0 and S8 (withdrawn under A-7, DEC-A7-POST-07); the role of the spin
    sector in growth is OPEN.
    """
    denom = 1.0 + (f_ion - 1.0) * gamma
    return s8_ref / denom


s8_ecf = compute_s8_suppression(S8_LCDM, F_ION, GAMMA_SPIN)

# First-order Gaussian uncertainty propagation
dS8_dgamma  = -S8_LCDM * (F_ION - 1.0) / (1.0 + (F_ION - 1.0) * GAMMA_SPIN) ** 2
sigma_s8_ecf = abs(dS8_dgamma) * GAMMA_SIG
# [D3] exact asymmetric propagation (S8 decreases when gamma_spin increases)
s8_up   = compute_s8_suppression(S8_LCDM, F_ION, GAMMA_SPIN - GAMMA_SIG_MINUS) - s8_ecf
s8_down = s8_ecf - compute_s8_suppression(S8_LCDM, F_ION, GAMMA_SPIN + GAMMA_SIG_PLUS)


# =============================================================================
# 4. TWO-DATASET CHI-SQUARE PROXY
# =============================================================================
def chi2(obs, sigma, pred):
    return ((obs - pred) / sigma) ** 2


def evaluate_statistical_budget():
    # Lambda-CDM
    chi2_h0_lcdm = chi2(H0_OBS, H0_OBS_SIG, H0_LCDM)
    chi2_s8_lcdm = chi2(S8_OBS, S8_OBS_SIG, S8_LCDM)
    total_lcdm   = chi2_h0_lcdm + chi2_s8_lcdm

    # ECF
    chi2_h0_ecf = chi2(H0_OBS, H0_OBS_SIG, H0_ECF)
    chi2_s8_ecf = chi2(S8_OBS, S8_OBS_SIG, s8_ecf)
    total_ecf   = chi2_h0_ecf + chi2_s8_ecf

    delta = total_lcdm - total_ecf

    # ndof=2: two observables compared
    pval       = stats.chi2.sf(delta, df=2)
    sigma_pref = stats.norm.ppf(1.0 - pval / 2.0)

    return {
        "s8_ecf":       s8_ecf,
        "sigma_s8":     sigma_s8_ecf,
        "chi2_h0_lcdm": chi2_h0_lcdm,
        "chi2_s8_lcdm": chi2_s8_lcdm,
        "total_lcdm":   total_lcdm,
        "chi2_h0_ecf":  chi2_h0_ecf,
        "chi2_s8_ecf":  chi2_s8_ecf,
        "total_ecf":    total_ecf,
        "delta_chi2":   delta,
        "sigma_pref":   sigma_pref,
    }


# =============================================================================
# 5. MAIN
# =============================================================================
if __name__ == "__main__":
    r = evaluate_statistical_budget()

    print("=" * 70)
    print(">>> SCRIPT 02 v2 — S8 SUPPRESSION & CHI-SQUARE PROXY")
    print("=" * 70)

    lcdm_tension = (S8_LCDM - S8_OBS) / S8_OBS_SIG
    ecf_tension  = abs(r["s8_ecf"] - S8_OBS) / S8_OBS_SIG

    print("\n[1] Structure Growth S8:")
    print(f"   Planck ΛCDM prediction  : {S8_LCDM:.3f}"
          f"   (tension: {lcdm_tension:.1f}σ vs KiDS-1000 3x2pt)")
    print(f"   ECF  (historical calib.): {r['s8_ecf']:.4f} +{s8_up:.4f}/-{s8_down:.4f}"
          f"  (gamma_spin +{GAMMA_SIG_PLUS}/-{GAMMA_SIG_MINUS}; linear bound ± {r['sigma_s8']:.4f})")
    print(f"   ECF  residual tension   : {ecf_tension:.2f}σ  (by construction: gamma_spin is calibrated on S8_obs -- not a test)")

    print("\n[2] Two-dataset Chi-square proxy {H0, S8}:")
    print(f"   chi2_H0  (ΛCDM)   : {r['chi2_h0_lcdm']:.2f}")
    print(f"   chi2_S8  (ΛCDM)   : {r['chi2_s8_lcdm']:.2f}")
    print(f"   Total chi2 (ΛCDM) : {r['total_lcdm']:.2f}")
    print(f"   Total chi2 (ECF)  : {r['total_ecf']:.4f}")
    print(f"   Delta chi2 (proxy): -{r['delta_chi2']:.2f}")
    print(f"   [Full multi-dataset budget Delta-chi2 = -39.5: historical (Omega_m = 0.315), NOT RECOMPUTED -- PO-F3-9; see chi_carre.py]")

    print("\n[3] Model preference (ndof=2):")
    print(f"   ECF favored at    : {r['sigma_pref']:.1f}σ  (historical proxy)")

    # [E2, 22/09/2026 -- DEC-A7-POST-07A] status of gamma_spin in this proxy
    print("\n[4] Status (DEC-A7-POST-07A):")
    print(f"   gamma_spin = {GAMMA_SPIN} is a HISTORICAL CALIBRATION (inversion on S8 = {S8_OBS}")
    print(f"   from S8_LCDM = {S8_LCDM}, former Planck background, Omega_m = 0.315); withdrawn as")
    print("   canonical post-A-7. Physical gamma_spin: OPEN. The proxy above and the")
    print("   AIC/BIC built on it are HISTORICAL (no recount by removing a parameter).")
    print("   A-7 diagnostic (CAMB LCDM reference, CALCULATED-CONDITIONAL): script_06 [F].")

    print("-" * 70)
    print("NOTE: 2-observable proxy only; the S8 term is zero by calibration. Full budget in chi_carre.py.")
    print("-" * 70)
