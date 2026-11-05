#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script 06 — S8 Tension Resolution within the ECF Framework
Foundation I Extended v2 — Sec. 4 & 5 (Table 2, Table 3)

Computes the phenomenological suppression of the clustering amplitude S8
via integrated torsional friction accumulated during matter domination.

Key equation (Eq. 14 of the paper):
    S8_ECF = S8_LCDM / [1 + (F_ion - 1) * gamma_spin]

ECF parameters (Table 2):
    F_ion      = 1.2765   calibrated on sound-horizon reduction (Sec. 3)
    gamma_spin = 0.3116   HISTORICAL CALIBRATION (DEC-A7-POST-07A, 22/09/2026):
                          obtained by inversion so that S8_ECF = S8_obs = 0.766
                          (KiDS-1000 3x2pt, Heymans+2021) from S8_LCDM = 0.832,
                          i.e. the former Planck background (Omega_m = 0.315);
                          WITHDRAWN as the canonical post-A-7 calibration; not an
                          independent prediction; +0.073/-0.100 from
                          gamma_spin_calibration.py (S8_obs uncertainty only;
                          S8_LCDM and F_ion fixed)

The historical computation ([A]-[D]) is kept unchanged. Block [F] ("A-7
diagnostic", DEC-A7-POST-07B) applies the same phenomenological form to the
CAMB LCDM reference computed on the A-7 background, S8_ref = 0.7800
(calc_S8_reference_camb_A7.py):
    gamma_cond = (S8_ref/0.766 - 1)/(F_ion - 1) ~ 0.066 (+0.069/-0.094),
status CALCULATED-CONDITIONAL / EXPLORATORY, compatible with zero.
Physical gamma_spin: OPEN. S8 = 0.766 is a target, not an ECF prediction.
    A_grad_legacy = 0.18   gradient coupling amplitude entering G_eff(k)
                   (superseded leading-order estimate; current Lorentzian
                   calibration gives A_sup = 0.15, see paper Table 2 —
                   NOT named kappa: that symbol is already the ECF coupling
                   constant, kappa^2 = 2.0766e-43 m/J, elsewhere in the corpus)

References:
    Heymans et al. 2021  (KiDS-1000)   arXiv:2007.15632
    DES Collaboration 2022             arXiv:2105.13549
    Riess et al. 2022    (SH0ES)       arXiv:2112.04510
    Planck Collaboration 2020          arXiv:1807.06209
"""
# Last modified: 02/09/2026, 11:10 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np

# ---------------------------------------------------------------------------
# 1. OBSERVATIONAL CONSTRAINTS
# ---------------------------------------------------------------------------
# ⚠️ CORRECTED 20/08/2026: was 0.014, which is the LOWER bound of an
# ASYMMETRIC error bar. KiDS-1000 reports S8 = 0.766 +0.020/-0.014; the
# effective symmetric 1-sigma is 0.019, and that is the value used in the
# Table 4 chi2 budget (it reproduces chi2_LCDM = 12.07). Taking the lower
# bound alone inflated the quoted LCDM tension from 3.47 to 4.71 sigma.
S8_OBS, S8_ERR = 0.766, 0.019   # KiDS-1000, symmetrised 1-sigma
H0_OBS, H0_ERR = 73.04, 1.04    # SH0ES 2022

# ---------------------------------------------------------------------------
# 2. THEORETICAL BASELINES (Planck 2018 LCDM)
# ---------------------------------------------------------------------------
S8_LCDM = 0.832
H0_LCDM = 67.4

# ---------------------------------------------------------------------------
# 3. ECF PARAMETERS (Table 2)
# ---------------------------------------------------------------------------
F_ION      = 1.2765   # stiffness — fixed by Sec. 3 calibration
GAMMA_SPIN = 0.3116   # growth-torsion coupling — HISTORICAL CALIBRATION (inversion on S8 = 0.766
                      # from S8_LCDM = 0.832, Omega_m = 0.315); withdrawn as canonical post-A-7
GAMMA_ERR_PLUS  = 0.073   # from gamma_spin_calibration.py: S8_obs uncertainty only
GAMMA_ERR_MINUS = 0.100   # (S8_LCDM and F_ion held fixed); not the full model uncertainty
GAMMA_ERR  = GAMMA_ERR_MINUS  # legacy symmetric input of propagate_s8_uncertainty(); the
                              # propagated S8 interval is circular (it returns the S8_obs one)
A_GRAD_LEGACY = 0.18     # gradient coupling amplitude in G_eff(k) (superseded
                         # leading-order estimate; NOT kappa, which is the
                         # ECF coupling constant elsewhere in the corpus)
KAPPA_ERR  = 0.04

# ---------------------------------------------------------------------------
# A-7 DIAGNOSTIC INPUTS  [E2, 22/09/2026 -- DEC-A7-POST-07B]
# ---------------------------------------------------------------------------
# CAMB LCDM reference on the A-7 background (h = 0.7304; Planck physical
# densities and primordial parameters unchanged). It is read from the JSON
# written by calc_S8_reference_camb_A7.py when that file is found; otherwise
# the documented constant below is used. Provenance of the constant: CAMB 2.0.4
# run of 22/09/2026 (Omega_m = 0.2681, sigma8 = 0.8252, S8_ref = 0.7800;
# Planck control sigma8 = 0.8109, S8 = 0.8312). Status: CALCULATED-CONDITIONAL,
# a LCDM reference, NOT an ECF prediction. The historical block is unchanged.
S8_REF_A7_FALLBACK = 0.7800
S8_OBS_PLUS, S8_OBS_MINUS = 0.020, 0.014   # KiDS-1000 asymmetric interval
_S8_REF_JSON = (
    ("Scripts_F1", "A_Core_Calculations", "S8_reference_camb_A7.json"),
    ("Audit_v2", "lot_post_arbitrages_22-09", "calculs_S8_reference",
     "resultats_S8_reference_A7.json"),
)


def load_s8_ref_a7():
    """Return (S8_ref, source): CAMB LCDM S8 on the A-7 background."""
    import json
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    roots = [os.environ.get("ECF_ROOT", ""), os.path.dirname(os.path.dirname(here))]
    for root in [r for r in roots if r]:
        for parts in _S8_REF_JSON:
            try:
                with open(os.path.join(root, *parts), encoding="utf-8") as f:
                    return float(json.load(f)["A7_h0.7304"]["S8"]), "/".join(parts)
            except (OSError, ValueError, KeyError, TypeError):
                continue
    return S8_REF_A7_FALLBACK, "documented constant (CAMB 2.0.4 run of 22/09/2026)"


def gamma_conditional(s8_ref, s8_obs=0.766):
    """Inversion of S8_obs = S8_ref / [1 + (F_ion - 1) gamma] (diagnostic only)."""
    return (s8_ref / s8_obs - 1.0) / (F_ION - 1.0)

# ---------------------------------------------------------------------------
# 4. CORE FUNCTIONS
# ---------------------------------------------------------------------------
def s8_ecf(s8_ref, f_ion, gamma):
    """S8 suppression formula — Eq. (14)."""
    return s8_ref / (1.0 + (f_ion - 1.0) * gamma)


def propagate_s8_uncertainty(s8_ref, f_ion, gamma, gamma_err, dg=1e-5):
    """First-order propagation: sigma_S8 from sigma_gamma_spin."""
    s8_up   = s8_ecf(s8_ref, f_ion, gamma + dg)
    s8_down = s8_ecf(s8_ref, f_ion, gamma - dg)
    dsens   = (s8_up - s8_down) / (2.0 * dg)
    return dsens, abs(dsens) * gamma_err


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    s8_pred              = s8_ecf(S8_LCDM, F_ION, GAMMA_SPIN)
    sensitivity, s8_unc  = propagate_s8_uncertainty(S8_LCDM, F_ION, GAMMA_SPIN, GAMMA_ERR)
    denom                = 1.0 + (F_ION - 1.0) * GAMMA_SPIN
    tension_lcdm         = (S8_LCDM - S8_OBS) / S8_ERR
    tension_ecf          = abs(s8_pred - S8_OBS) / S8_ERR
    # Inversion: exact gamma that maps S8_LCDM -> S8_OBS
    gamma_exact          = (S8_LCDM / S8_OBS - 1.0) / (F_ION - 1.0)

    sep = "=" * 70
    print(sep)
    print("  SCRIPT 06 — S8 RESOLUTION  (Foundation I Sec. 4–5)")
    print(sep)

    print("\n[A] S8 SUPPRESSION  (HISTORICAL CALIBRATION, former Planck background -- see [E])")
    print(f"  Planck LCDM  : S8 = {S8_LCDM:.4f}                    ({tension_lcdm:.2f} sigma)")
    print(f"  ECF (historical calibration): S8 = {s8_pred:.4f} +/- {s8_unc:.4f} ({tension_ecf:.2f} sigma)")   # [D3] was "ECF predict"
    print(f"  KiDS-1000 obs: S8 = {S8_OBS:.4f} +/- {S8_ERR:.4f}  (symmetrised)")

    print("\n[B] PHYSICAL MECHANISM (Sec. 4)")
    print(f"  G_eff(k) = G_N [1 - (k/k_cut)^2]  (k^2 fixed by ECKS symmetry)")
    print(f"  Denominator  = 1 + (F_ion-1)*gamma_spin = {denom:.6f}")
    print(f"  F_ion        = {F_ION}   (sound-horizon calibration, Sec. 3)")
    print(f"  gamma_spin   = {GAMMA_SPIN}   (HISTORICAL calibration on S8 = 0.766 from S8_LCDM = 0.832; no MCMC)")
    print(f"  A_grad_legacy = {A_GRAD_LEGACY}       (gradient amplitude, Table 2 — superseded, see header)")
    print(f"  G_eff(z=0)   = G_N            [Omega_spin ~ a^-6 -> 0 at z=0]")

    # REWORDED 22/09/2026 -- gamma_spin IS fixed by inversion on S8 = 0.766
    # (KiDS-1000 3x2pt). No global MCMC fit of gamma_spin exists in the
    # repository; the agreement below is therefore by construction, NOT a test.
    print("\n[C] CALIBRATION STATUS  (HISTORICAL CALIBRATION -- see [E]; F1 Sec. 5)")
    print(f"  gamma_spin calibrated (inversion on S8=0.766) = {GAMMA_SPIN:.4f}")
    print(f"  gamma_exact for S8_pred = S8_obs exactly   = {gamma_exact:.6f}")
    print(f"  Difference                                  = {abs(gamma_exact-GAMMA_SPIN):.2e}")
    print(f"  gamma_spin interval (S8_obs only)           = +{GAMMA_ERR_PLUS} / -{GAMMA_ERR_MINUS}")
    print( "  ⚠️  CALIBRATED BY INVERSION -- NOT a test and not an independent")
    print( "      prediction; the interval propagates the S8_obs uncertainty only.")
    print(f"  dS8/d(gamma_spin)                           = {sensitivity:.4f}")
    print(f"  Propagated: S8 +/- {s8_unc:.4f}  from gamma_spin +/- {GAMMA_ERR}")

    print("\n[D] TENSION SUMMARY")
    print(f"  LCDM : {tension_lcdm:.2f} sigma")
    print(f"  ECF  : {tension_ecf:.2f} sigma  -> by construction (gamma_spin calibrated on S8_obs; not a test)")

    # [E2, 22/09/2026 -- DEC-A7-POST-07A/B] Status of [A]-[D], then the A-7
    # diagnostic. The historical computation above is unchanged.
    print("\n[E] STATUS OF [A]-[D]  (DEC-A7-POST-07A)")
    print(f"  gamma_spin = {GAMMA_SPIN}: HISTORICAL CALIBRATION (inversion on S8 = {S8_OBS}")
    print(f"  from S8_LCDM = {S8_LCDM}, former Planck background, Omega_m = 0.315)")
    print("  WITHDRAWN as the canonical post-A-7 calibration; [A]-[D] are the historical chain")

    s8_ref, src = load_s8_ref_a7()
    g_c = gamma_conditional(s8_ref, S8_OBS)
    g_p = gamma_conditional(s8_ref, S8_OBS - S8_OBS_MINUS) - g_c
    g_m = g_c - gamma_conditional(s8_ref, S8_OBS + S8_OBS_PLUS)
    print("\n[F] A-7 DIAGNOSTIC  (DEC-A7-POST-07B) -- CALCULATED-CONDITIONAL / EXPLORATORY")
    print(f"  S8_ref, CAMB LCDM on the A-7 background (h = 0.7304) = {s8_ref:.4f}")
    print(f"  source: {src}")
    print(f"  gamma_cond = (S8_ref/{S8_OBS} - 1)/(F_ion - 1) = {g_c:.4f} +{g_p:.3f}/-{g_m:.3f}"
          "  (S8_obs interval only)")
    print("  = the gamma that would reproduce S8 = 0.766 IF the CAMB LCDM run on the A-7")
    print("    background were the relevant perturbative reference and the phenomenological")
    print("    form still applied; compatible with zero. Not a canonical calibration,")
    print("    not a theoretical determination.")
    print("  physical gamma_spin: OPEN (requires a consistent ECF perturbation calculation)")
    print("  S8 = 0.766 is the KiDS-1000 target, not an ECF prediction.")
    print(sep)
