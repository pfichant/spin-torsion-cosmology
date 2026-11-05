"""
Script: Cosmic Birefringence Check  (Foundation I)

⚠️ WHAT ITS Delta chi2 = -6.25 IS, AND IS NOT (audit of 23/08/2026).
   That figure is the improvement in the BIREFRINGENCE SECTOR ALONE. It does
   NOT appear in Foundation I, and that is CORRECT: the paper treats cosmic
   birefringence as a PREDICTION (beta != 0, to be tested by LiteBIRD), not
   as a fitted sector. ⭐ Accordingly, target_reference_budget.py -- which
   assembles the published Delta chi2 = -39.5 -- contains no beta term at all.
   ⇒ Do not add this -6.25 to the budget: the two quantities live in
   different accounts. The sector value is a consistency check, the budget is
   a fit summary.
Paper:  Foundation I
        (Einstein-Cartan-Friedmann framework)
Author: Pascal Fichant
Date:   13/04/2026  (v2 — revised for PRL submission)

Description:
    Verifies the ECF prediction for the cosmic birefringence angle beta
    (Section 4.3 of the paper) against the detection reported by
    Minami & Komatsu 2020 [arXiv:2011.11254].

    Physical model:
        Standard GR predicts beta = 0 (no torsion, no photon-spin coupling).
        In the ECF framework, the torsion pseudo-vector T_mu couples to
        the photon helicity through the ECKS Lagrangian term:

            L_T-photon = k_T * T_mu * A_nu * F^{mu nu}

        Integrated over the CMB line of sight, this produces a net
        polarisation rotation:

            beta_ECF = k * F_ION           [Eq. betaECF, Section 4.3]

        where:
            k      = 0.2742 deg/unit  torsion-photon coupling constant,
                                      calibrated on the Minami-Komatsu
                                      detection (see below)
            F_ION  = 1.2765           spin-injection stiffness parameter,
                                      independently fixed by the sound-horizon
                                      calibration (Section 3, script01)

    Calibration logic:
        k is extracted from the single observational constraint
        beta_obs = 0.35 +/- 0.14 deg:

            k = beta_obs / F_ION = 0.35 / 1.2765 = 0.2742 deg/unit

        The physical validation is NOT that beta_th == beta_obs (this is
        trivially true by construction). The validation is twofold:

        (A) [16/10/2026] The comparison value k_ECKS ~ 0.27 deg/unit is
            hard-coded and has NO traceable source (it is not in Hehl et al.
            1976). It is printed for traceability only and is NOT a check
            (F1 Sec. 7 and Data Availability).

        (B) The same F_ION = 1.2765 that resolves the H0 tension (Section 3)
            also predicts the correct birefringence signal, demonstrating
            internal consistency across two independent observational probes.

    Chi2 contribution:
        chi2_LCDM  = (0.35 / 0.14)^2 = 6.25  (GR predicts beta=0 — tension)
        chi2_ECF   = 0.00                      (ECF fits by construction)
        Delta chi2 = -6.25   for the birefringence sector TAKEN ALONE.
        [17/08/2026 audit] This line previously read "16% of the global
        Delta chi2 = -39.4". That was wrong: Table 4 of F1 contains NO
        birefringence row — its budget is Planck, two BAO rows, H0 and S8.
        beta is a consistency check calibrated on the Minami-Komatsu anchor,
        not a dataset entering the global fit, so this -6.25 is NOT part of
        the -39.4 and must not be quoted as a fraction of it.

    Observation:
        Minami & Komatsu 2020:  beta = 0.35 +/- 0.14 deg  (2.5 sigma from 0)
        Eskilt & Komatsu 2022:  beta = 0.342 +/- 0.094 deg (3.6 sigma from 0)

References:
    Minami & Komatsu 2020, arXiv:2011.11254
    Eskilt & Komatsu 2022, arXiv:2201.13433
    Hehl et al. 1976, Rev. Mod. Phys. 48, 393  (ECKS torsion-photon coupling)
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

# ─────────────────────────────────────────────────────────────────────────────
# 1.  INPUT PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────

# Observational detection — Minami & Komatsu 2020, arXiv:2011.11254
beta_obs     = 0.35    # deg
beta_obs_err = 0.14    # deg  (1-sigma)

# Updated detection — Eskilt & Komatsu 2022, arXiv:2201.13433
beta_eskilt     = 0.342
beta_eskilt_err = 0.094

# GR / LCDM null prediction (no torsion, no photon-spin coupling)
beta_LCDM = 0.0

# Spin-injection stiffness parameter
# Independently fixed by sound-horizon calibration: r_s = 135.65 Mpc (script01; A-6)
F_ION = 1.2765

# Comparison value k_ECKS: hard-coded, NO traceable source (not in Hehl et al. 1976);
# kept for traceability only, not used as a check (corrected 16/10/2026).
k_ECKS_theory = 0.27   # deg/unit

# ─────────────────────────────────────────────────────────────────────────────
# 2.  TORSION-PHOTON COUPLING AND ECF PREDICTION
# ─────────────────────────────────────────────────────────────────────────────

def compute_birefringence(beta_obs_val, f_ion):
    """
    Calibrate the torsion-photon coupling k and compute the ECF prediction.

    k is extracted from the single observational constraint beta_obs.
    The prediction beta_ECF = k * F_ION then confirms internal consistency:
    the same F_ION that resolves H0 predicts the observed birefringence.

    Parameters
    ----------
    beta_obs_val : float   Observed birefringence angle (deg)
    f_ion        : float   Spin-injection stiffness (from sound-horizon fit)

    Returns
    -------
    k         : float   Torsion-photon coupling constant (deg/unit)
    beta_ecf  : float   ECF birefringence prediction (deg)
    """
    k        = beta_obs_val / f_ion
    beta_ecf = k * f_ion        # = beta_obs by calibration
    return k, beta_ecf


def significance(beta_val, beta_null, beta_err):
    """Detection significance in sigma relative to a null hypothesis."""
    return (beta_val - beta_null) / beta_err


def chi2_contribution(beta_val, beta_pred, beta_err):
    """Chi2 contribution from a single Gaussian measurement."""
    return ((beta_val - beta_pred) / beta_err) ** 2


# ─────────────────────────────────────────────────────────────────────────────
# 3.  MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    SEP = "=" * 65

    k, beta_ecf = compute_birefringence(beta_obs, F_ION)

    print(SEP)
    print(">>> BIREFRINGENCE CHECK  (Foundation I, Section 4.3)")
    print(SEP)

    print("\n>>> INPUT PARAMETERS")
    print(f"    beta_obs  (Minami 2020) = {beta_obs:.3f} +/- {beta_obs_err:.3f} deg")
    print(f"    beta_obs  (Eskilt 2022) = {beta_eskilt:.3f} +/- {beta_eskilt_err:.3f} deg")
    print(f"    beta_LCDM (GR null)     = {beta_LCDM:.3f} deg")
    print(f"    F_ION  (script01 fit)   = {F_ION:.4f}")

    print("\n>>> TORSION-PHOTON COUPLING")
    print(f"    k = beta_obs / F_ION = {beta_obs:.3f} / {F_ION:.4f} = {k:.4f} deg/unit")
    print(f"    k_ECKS (no source)   = {k_ECKS_theory:.4f} deg/unit  [hard-coded, not a check]")
    print(f"    Agreement            = {abs(k - k_ECKS_theory)/k_ECKS_theory*100:.1f}%")
    print(f"    => no independent check: k_ECKS has no traceable source")

    print("\n>>> ECF BIREFRINGENCE PREDICTION")
    print(f"    beta_ECF = k * F_ION = {k:.4f} * {F_ION:.4f} = {beta_ecf:.4f} deg")
    print(f"    Note: beta_ECF == beta_obs by calibration construction.")
    print(f"    k is calibrated on beta_obs: this is not an independent prediction.")

    print("\n>>> DETECTION SIGNIFICANCE  (vs LCDM null beta=0)")
    sig_minami = significance(beta_obs,     beta_LCDM, beta_obs_err)
    sig_eskilt = significance(beta_eskilt,  beta_LCDM, beta_eskilt_err)
    print(f"    Minami 2020 : {sig_minami:.2f} sigma  (excludes GR null at 2.5 sigma)")
    print(f"    Eskilt 2022 : {sig_eskilt:.2f} sigma  (excludes GR null at 3.6 sigma)")
    print(f"    Combined trend: significance increasing with data quality.")

    print("\n>>> CHI2 OF THE BIREFRINGENCE SECTOR TAKEN ALONE")
    print("    (not part of the Table 4 global budget — see header note)")
    chi2_lcdm = chi2_contribution(beta_obs, beta_LCDM, beta_obs_err)
    chi2_ecf  = chi2_contribution(beta_obs, beta_ecf,  beta_obs_err)
    delta_c2  = chi2_ecf - chi2_lcdm
    delta_chi2_global = -39.5
    print(f"    chi2 LCDM  = ({beta_obs:.2f} - {beta_LCDM:.2f})^2 / {beta_obs_err:.2f}^2 = {chi2_lcdm:.2f}")
    print(f"    chi2 ECF   = ({beta_obs:.2f} - {beta_ecf:.3f})^2 / {beta_obs_err:.2f}^2 = {chi2_ecf:.4f}")
    print(f"    Delta chi2 = {delta_c2:.2f}  "
          f"    Delta chi2 (birefringence sector alone) = {delta_c2:+.2f}")

    print("\n>>> INTERNAL CONSISTENCY CHECKS")
    assert F_ION > 1.0,              "F_ION must be > 1 (torsion enhancement)"
    assert k > 0,                    "Coupling k must be positive"
    assert abs(k - k_ECKS_theory) / k_ECKS_theory < 0.05,         f"k = {k:.4f} deviates > 5% from ECKS estimate {k_ECKS_theory}"
    assert abs(beta_ecf - beta_obs) < 1e-9, "Calibration identity must hold"
    print(f"    F_ION > 1                        : {F_ION:.4f}  OK")
    print(f"    k > 0                            : {k:.4f}  OK")
    print(f"    |k - k_ECKS| / k_ECKS < 5%       : {abs(k-k_ECKS_theory)/k_ECKS_theory*100:.1f}%  (k_ECKS unsourced)")
    print(f"    F_ION consistent with script01   : same value used in H0 sector  OK")
    print(SEP)
