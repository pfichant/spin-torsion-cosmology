#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_ecf_des_pivot.py  --  ECF Foundation I/II
==========================================================================
Compatibility of the calibrated ECF dark-energy trajectory (w0, wa) with
the Dark Energy Survey's full six-year dataset (DES Y6), via the pivot
parameter w_p.

WHY THE PIVOT, NOT A MARGINAL (w0, wa) COMPARISON
--------------------------------------------------
w0 and wa are strongly correlated in every w0waCDM fit (DES included):
a marginal comparison of each parameter separately overstates or understates
compatibility depending on the direction of the correlation, and does not
answer a well-posed statistical question on its own. DES Y6 reports, for
each dataset combination, a pivot redshift z_p chosen so that
Cov(w_p, wa) = 0, where w_p = w(z_p) under the CPL parametrisation
w(a) = w0 + wa*(1-a). This single decorrelated number per combination is
the quantity compared here.

SOURCE OF THE DES NUMBERS
--------------------------
DES Collaboration, "Constraints on Dynamical Dark Energy from Multiple
Probes in the Full Dark Energy Survey", arXiv:2605.27221 (Letter, 3 June
2026), Table S1 (supplementary; cited as Table I before 20/10/2026) and
Fig. 2. Three combinations are used below (68% C.L.); the first is the row
"All DES" of Table S1 (the paper's own "3x2pt" row is DES 3x2pt only):
    DES alone           (3x2pt+SN+BAO)         : w_p=-0.91+/-0.04, z_p=0.19
    DES + DESI DR2 BAO  (All except CMB)        : w_p=-0.94+/-0.03, z_p=0.22
    All data            (+ Planck+ACT+SPT CMB)  : w_p=-0.97+/-0.02, z_p=0.32

STATUS
------
This compares a calibration point (ECF) to a measurement (DES), exactly as
in compute_ecf_aic_desi.py: no new fit is performed here, the arithmetic
of Eq. (1) is simply not left for the reader to redo silently.

Dependency: none beyond the standard library. Usage: python3 compute_ecf_des_pivot.py
==========================================================================
"""
# Last modified: 03/09/2026 (Paris time)
# Corpus: Foundation I / Foundation II — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# --- ECF calibrated trajectory (Foundation I, Sec. 5) ---
W0_ECF = -0.904
WA_ECF = -0.153


def w_p_ecf(z_p: float) -> float:
    """CPL trajectory w(a) = w0 + wa*(1-a), evaluated at the pivot redshift."""
    a = 1.0 / (1.0 + z_p)
    return W0_ECF + WA_ECF * (1.0 - a)


# --- DES Y6 pivot constraints (arXiv:2605.27221, Table S1 / Fig. 2) ---
DES_COMBINATIONS = [
    ("DES alone (3x2pt+SN+BAO)",       -0.91, 0.04, 0.19, "2.2"),
    ("DES + DESI DR2 BAO (all-CMB)",   -0.94, 0.03, 0.22, "2.3"),
    ("All data (+CMB)",                -0.97, 0.02, 0.32, "3.0"),
]


def main() -> None:
    print("ECF vs DES Y6, compatibility via the pivot parameter w_p")
    print("=" * 74)
    print(f"  ECF trajectory: w0={W0_ECF}, wa={WA_ECF} (Foundation I, calibrated)")
    print()
    for label, wp_obs, sigma, zp, lcdm_tension in DES_COMBINATIONS:
        wp_ecf = w_p_ecf(zp)
        diff_sigma = abs(wp_ecf - wp_obs) / sigma
        print(f"  {label}")
        print(f"    z_p = {zp}")
        print(f"    DES: w_p = {wp_obs:+.2f} +/- {sigma:.2f}  "
              f"(DES vs LambdaCDM: {lcdm_tension} sigma)")
        print(f"    ECF: w_p = {wp_ecf:+.3f}")
        print(f"    |difference| = {diff_sigma:.2f} sigma")
        print()

    print("-" * 74)
    print("NOTE: this compares a calibration point (ECF) to a measurement (DES);")
    print("no new fit is performed. See Foundation I/II, Sec. dark energy, for the")
    print("full discussion and for the separate DESI-only Mahalanobis comparison")
    print("(full 13x13 covariance, Foundation III), which is not superseded by")
    print("this pivot-based cross-check: the two use different probe combinations")
    print("and neither reduces to the other.")

    # --- auto-consistency check (rule 1bis: a result carries its verification) ---
    print()
    print("-" * 74)
    print("AUTO-CONSISTENCY")
    print("-" * 74)
    ok = True
    expected = [0.46, 0.28, 1.45]
    for (label, wp_obs, sigma, zp, _), exp in zip(DES_COMBINATIONS, expected):
        got = abs(w_p_ecf(zp) - wp_obs) / sigma
        cond = abs(got - exp) < 0.01
        print(f"  {'PASS' if cond else 'FAIL'}  {label:<32} "
              f"{got:.2f} sigma (expected {exp})")
        ok &= cond
    print()
    print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
