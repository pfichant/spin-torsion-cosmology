"""
Script: S8 Effective Suppression Check  (Foundation I)
Paper:  Foundation I
        (Einstein-Cartan-Friedmann framework)
Author: Pascal Fichant
Date:   13/04/2026  (v2 — revised for submission)

Description:
    Verifies the phenomenological suppression of the weak-lensing
    clustering amplitude S8 in its HISTORICAL CALIBRATION (Eq. S8ECF,
    Section 4 of the paper). S8 = 0.766 is the KiDS-1000 target, not an ECF
    prediction (DEC-A7-POST-07, 22/09/2026).

    Physical model:
        The residual spin-torsion coupling induces a scale-dependent
        suppression of linear structure growth through an effective
        gravitational constant G_eff(k) = G_N * (1 - k^2/k_cut^2).
        At the macroscopic level this is captured by:

            S8_ECF = S8_LCDM / (1 + (F_ion - 1) * gamma_spin)

        where:
            S8_LCDM    = 0.832   Planck 2018 baseline (TT,TE,EE+lowE)
                                  [arXiv:1807.06209, Table 2]
            F_ION      = 1.2765  spin-injection stiffness parameter,
                                  calibrated on the sound-horizon reduction
                                  (Section 3, script01_solve_sound_horizon.py)
            gamma_spin = 0.3116  growth-torsion coupling efficiency,
                                  HISTORICAL CALIBRATION (DEC-A7-POST-07A,
                                  22/09/2026): fixed by inversion on
                                  S8 = 0.766 from S8_LCDM = 0.832, i.e. the
                                  former Planck background (Omega_m = 0.315);
                                  withdrawn as the canonical post-A-7 value.
                                  [The former label "MCMC fitted value,
                                  uniform prior [0.20, 0.45], Gelman-Rubin
                                  R < 1.01" was wrong: no MCMC fit of
                                  gamma_spin exists in the repository.]

    Key structural constraint (historical reading):
        F_ION is NOT a free parameter for the S8 fit; it is fixed by the
        sound-horizon calibration (Section 3). Only gamma_spin is adjusted,
        subject to the perturbative ECKS constraint gamma_spin < 1.
        The H0 and S8 sectors were therefore tied at the calibration stage
        only. Under A-7 this is no longer an established result: the S8
        reduction comes mostly from Omega_m = omega_m/h^2, and the role of
        the spin sector in growth is OPEN (DEC-A7-POST-07).

    A-7 diagnostic (added 22/09/2026, DEC-A7-POST-07B; the historical
    computation is unchanged): the same inversion on the CAMB LCDM reference
    of the A-7 background, S8_ref = 0.7800 (calc_S8_reference_camb_A7.py),
    gives gamma_cond ~ 0.066 (+0.069/-0.094), CALCULATED-CONDITIONAL /
    EXPLORATORY, compatible with zero. Physical gamma_spin: OPEN.

    Expected output:
        S8_ECF = 0.766 +/- 0.019
        consistent with KiDS-1000 [arXiv:2007.15633] and DES Y3
        [arXiv:2105.13549] at 0.0 sigma tension -- by construction, since
        gamma_spin was calibrated on 0.766 (not a test).
        [02/09/2026: corrected from 0.014, the asymmetric KiDS-1000 lower
        bound taken alone rather than the symmetrised 1-sigma; see
        ECF_DOSSIER_incertitudes_calibres.md section 6]

References:
    Planck Collaboration 2018,    arXiv:1807.06209
    Hildebrandt et al. 2020 (KiDS-1000), arXiv:2007.15633
    Abbott et al. 2022 (DES Y3), arXiv:2105.13549
    Hehl et al. 1976, Rev. Mod. Phys. 48, 393
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

# ─────────────────────────────────────────────────────────────────────────────
# 1.  INPUT PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────

# Planck 2018 LCDM baseline clustering amplitude
# Source: Planck 2018 VI, Table 2, TT,TE,EE+lowE
S8_LCDM = 0.832

# Spin-injection stiffness parameter
# Fixed by sound-horizon calibration: r_s = 135.65 Mpc  (script01; A-6)
# NOT a free parameter for the S8 sector
F_ION = 1.2765

# Growth-torsion coupling efficiency
# [E2, 22/09/2026 -- DEC-A7-POST-07A] HISTORICAL CALIBRATION: fixed by
# inversion on S8 = 0.766 from S8_LCDM = 0.832 (former Planck background,
# Omega_m = 0.315); withdrawn as the canonical post-A-7 value. The former
# comment ("MCMC fitted value, uniform prior [0.20, 0.45], Gelman-Rubin
# R < 1.01") was wrong: no MCMC fit of gamma_spin exists.
# Physical constraint: gamma_spin < 1 (perturbative ECKS expansion)
gamma_spin = 0.3116

# Weak-lensing observational target (for residual check)
# KiDS-1000 3x2pt (S8 = 0.766; not a KiDS+DES Y3 combination, §4)
# [02/09/2026] KiDS-1000 reports S8 = 0.766 +0.020/-0.014 (asymmetric); 0.014
# is the LOWER bound taken alone, not a valid symmetric 1-sigma. The correct
# symmetrised value is 0.019 (see ECF_DOSSIER_incertitudes_calibres.md section
# 6; matches chi_carre.py's own corrected header note and script_06).
S8_WL_OBS   = 0.766
S8_WL_SIGMA = 0.019

# Historical input width on gamma_spin. The former "MCMC posterior" label
# has no producer; the value is kept so that the historical output is
# reproduced unchanged (the S8_obs-only interval is +0.073/-0.100, script_06).
sigma_gamma = 0.04

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

# ─────────────────────────────────────────────────────────────────────────────
# 2.  S8 SUPPRESSION FORMULA  (Eq. S8ECF, Section 4)
# ─────────────────────────────────────────────────────────────────────────────

def s8_ecf(s8_lcdm, f_ion, gamma):
    """
    Compute the ECF-suppressed clustering amplitude.

    The denominator (1 + (F_ion - 1) * gamma_spin) encodes the combined
    effect of the stiffness calibration and the torsion-matter coupling.
    F_ion > 1 guarantees S8_ECF < S8_LCDM (suppression, not enhancement).

    Parameters
    ----------
    s8_lcdm : float   Planck LCDM baseline S8
    f_ion   : float   Spin-injection stiffness (fixed by sound horizon)
    gamma   : float   Growth-torsion coupling efficiency (historical calibration)

    Returns
    -------
    s8_val : float   ECF clustering amplitude for this gamma (calibrated, not predicted)
    denom  : float   Suppression denominator (for diagnostics)
    """
    denom  = 1.0 + (f_ion - 1.0) * gamma
    s8_val = s8_lcdm / denom
    return s8_val, denom


def s8_uncertainty(s8_lcdm, f_ion, gamma, sig_gamma):
    """
    Propagate the uncertainty on gamma_spin to S8_ECF.

    Partial derivative: dS8/d(gamma) = -S8_LCDM * (F_ion - 1) / denom^2

    Parameters
    ----------
    sig_gamma : float   1-sigma uncertainty on gamma_spin

    Returns
    -------
    sigma_s8 : float   1-sigma uncertainty on S8_ECF
    """
    denom      = 1.0 + (f_ion - 1.0) * gamma
    ds8_dgamma = -s8_lcdm * (f_ion - 1.0) / denom**2
    return abs(ds8_dgamma) * sig_gamma


# ─────────────────────────────────────────────────────────────────────────────
# 3.  MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    SEP = "=" * 65

    S8_val, denom = s8_ecf(S8_LCDM, F_ION, gamma_spin)
    sigma_s8      = s8_uncertainty(S8_LCDM, F_ION, gamma_spin, sigma_gamma)

    print(SEP)
    print(">>> S8 SUPPRESSION CHECK  (Foundation I, Section 4) -- HISTORICAL CALIBRATION")
    print(SEP)

    print("\n>>> INPUT PARAMETERS")
    print(f"    S8_LCDM     = {S8_LCDM:.3f}       [Planck 2018, arXiv:1807.06209]")
    print(f"    F_ION       = {F_ION:.4f}      [sound-horizon fit, script01]")
    print(f"    gamma_spin  = {gamma_spin:.4f}      [HISTORICAL CALIBRATION, inversion on 0.766]")
    print(f"    sigma_gamma = {sigma_gamma:.2f}        [historical input, no MCMC]")

    print("\n>>> S8 SUPPRESSION FORMULA  S8_ECF = S8_LCDM / (1 + (F_ion-1)*gamma)")
    print(f"    denom  = 1 + {F_ION - 1:.4f} * {gamma_spin:.4f} = {denom:.6f}")
    print(f"    S8_ECF = {S8_LCDM:.3f} / {denom:.6f} = {S8_val:.4f} +/- {sigma_s8:.4f}")

    print("\n>>> COMPARISON WITH PAPER AND OBSERVATIONS")
    print(f"    S8_ECF  (this script)  = {S8_val:.4f} +/- {sigma_s8:.4f}")
    print(f"    S8_ECF  (paper target) = 0.766  +/- 0.019")
    print(f"    S8_WL   (KiDS/DES obs) = {S8_WL_OBS:.3f}  +/- {S8_WL_SIGMA:.3f}")
    print(f"    Deviation from paper   = {abs(S8_val - 0.766):.4f}  "
          f"({abs(S8_val - 0.766)/0.766*100:.2f}%)")
    print(f"    Tension with KiDS/DES  = {abs(S8_val - S8_WL_OBS)/S8_WL_SIGMA:.2f} sigma")

    print("\n>>> INTERNAL CONSISTENCY CHECKS")
    assert F_ION > 1.0,              "F_ION must be > 1 for suppression"
    assert 0.0 < gamma_spin < 1.0,   "gamma_spin must satisfy perturbative bound"
    assert S8_val < S8_LCDM,         "ECF must suppress S8, not enhance it"
    print(f"    F_ION > 1            : {F_ION:.4f} > 1.0  [suppression guaranteed]  OK")
    print(f"    gamma_spin in (0,1)  : {gamma_spin:.4f}  [perturbative ECKS]        OK")
    print(f"    S8_ECF < S8_LCDM     : {S8_val:.4f} < {S8_LCDM:.3f}                OK")
    print(f"    F_ION fixed by script01 (no tuning to S8)                      OK")

    print("\n>>> NUMERICAL BACK-VERIFICATION")
    gamma_implied = (S8_LCDM / 0.766 - 1.0) / (F_ION - 1.0)
    print(f"    gamma_spin implied by S8_ECF=0.766 : {gamma_implied:.4f}")
    print(f"    gamma_spin used in this script     : {gamma_spin:.4f}")
    dg = abs(gamma_implied - gamma_spin)
    print(f"    Difference                         : {dg:.4f}  "
          f"(= {dg/sigma_gamma*100:.1f}% of sigma_gamma = {sigma_gamma})")
    print(f"    => Identical by construction (inversion on 0.766), not an MCMC result")

    # [E2, 22/09/2026 -- DEC-A7-POST-07A/B] Status, then the A-7 diagnostic.
    # The historical computation above is unchanged.
    print("\n>>> STATUS  (DEC-A7-POST-07A)")
    print(f"    gamma_spin = {gamma_spin:.4f} : HISTORICAL CALIBRATION (S8_LCDM = {S8_LCDM:.3f},")
    print("    former Planck background, Omega_m = 0.315); withdrawn as canonical post-A-7")
    s8_ref, src = load_s8_ref_a7()
    g_c = gamma_conditional(s8_ref, S8_WL_OBS)
    g_p = gamma_conditional(s8_ref, S8_WL_OBS - S8_OBS_MINUS) - g_c
    g_m = g_c - gamma_conditional(s8_ref, S8_WL_OBS + S8_OBS_PLUS)
    print("\n>>> A-7 DIAGNOSTIC  (DEC-A7-POST-07B) -- CALCULATED-CONDITIONAL / EXPLORATORY")
    print(f"    S8_ref, CAMB LCDM on the A-7 background (h = 0.7304) = {s8_ref:.4f}")
    print(f"    source: {src}")
    print(f"    gamma_cond = (S8_ref/{S8_WL_OBS:.3f} - 1)/(F_ion - 1) = {g_c:.4f} "
          f"+{g_p:.3f}/-{g_m:.3f}  (S8_obs interval only)")
    print("    conditional on the CAMB LCDM reference and on the phenomenological form;")
    print("    compatible with zero; not a canonical calibration")
    print("    physical gamma_spin: OPEN")
    print(SEP)
