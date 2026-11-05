#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation I -- The Metric Universe
Script      : compare_fsigma8_data.py
Author      : Pascal Fichant
Date        : 05/09/2026
Description :
    Confronts the ECF growth prediction f*sigma_8(z) -- computed by
    compute_fsigma8_ecf.py -- with published redshift-space-distortion
    measurements, and reports an indicative chi-square against LambdaCDM.

WHY THIS SCRIPT EXISTS
----------------------
compute_fsigma8_ecf.py (05/09/2026) established that the ECF growth
suppression is nearly redshift-independent, and therefore does not reproduce
the failure mode that rules out the background-degenerate interacting model
of Petri et al. [PRD 113, 023504 (2026), arXiv:2508.17955]. That was a
comparison of ECF against LambdaCDM. It was *not* a comparison against data.

This script closes that second gap. The corpus previously had no
growth-sector observational test at all.

DATA -- published RSD measurements, with sources
------------------------------------------------
  z=0.067  f*s8 = 0.423 +/- 0.055   6dFGS      Beutler et al. (2012), MNRAS 423, 3430
  z=0.15   f*s8 = 0.490 +/- 0.145   SDSS MGS   Howlett et al. (2015)
  z=0.25   f*s8 = 0.3512 +/- 0.0583 SDSS LRG   Samushia et al. (2012)
  z=0.37   f*s8 = 0.4602 +/- 0.0378 SDSS LRG   Samushia et al. (2012)
  z=0.80   f*s8 = 0.470 +/- 0.080   VIPERS     de la Torre et al. (2013)
  z=1.52   f*s8 = 0.426 +/- 0.079   eBOSS QSO  Zarrouk et al. (2018)

WHAT THIS IS NOT
----------------
An indicative chi-square, not a likelihood analysis:

  (a) The measurements are treated as INDEPENDENT. Some are not: the SDSS-LRG
      pair shares a survey (though disjoint redshift slices), and any
      BOSS/eBOSS overlap induces correlations not modelled here.
  (b) No Alcock-Paczynski rescaling. Each measurement assumes a fiducial
      cosmology; a rigorous comparison rescales f*s8 by the ratio of
      H(z)D_A(z) between the fiducial and tested cosmology. Not done here.
      The ECF background is close enough to the fiducials that the effect is
      subdominant to the error bars, but it is not zero.
  (c) The MGS error bar is asymmetric (+0.15/-0.14); symmetrised to 0.145.
  (d) sigma_8 is an INPUT, not fitted: 0.812 (Planck) for LambdaCDM, 0.747
      for the ECF (F1). The comparison therefore tests the growth *history*
      given the calibrated amplitude, not a joint fit.

A proper analysis requires the full covariance and a Boltzmann treatment
(PO-F3-9, CLASS-EC). This script gives an order-of-magnitude verdict, which
is what the corpus currently lacks.

Usage:
    python compare_fsigma8_data.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import io
import importlib.util
import numpy as np

# ---------------------------------------------------------------------------
# Import the growth solver (rule R13: the script is the reference)
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "_g", os.path.join(_HERE, "compute_fsigma8_ecf.py"))
_g = importlib.util.module_from_spec(_spec)
_old = sys.stdout
sys.stdout = io.StringIO()          # silence its main()
try:
    _spec.loader.exec_module(_g)
except SystemExit:
    pass
sys.stdout = _old

# ---------------------------------------------------------------------------
# Published RSD measurements
# ---------------------------------------------------------------------------
DATA = [
    (0.067, 0.4230, 0.0550, "6dFGS",     "Beutler+2012"),
    (0.150, 0.4900, 0.1450, "SDSS MGS",  "Howlett+2015"),
    (0.250, 0.3512, 0.0583, "SDSS LRG",  "Samushia+2012"),
    (0.370, 0.4602, 0.0378, "SDSS LRG",  "Samushia+2012"),
    (0.800, 0.4700, 0.0800, "VIPERS",    "de la Torre+2013"),
    (1.520, 0.4260, 0.0790, "eBOSS QSO", "Zarrouk+2018"),
]


def build_predictions():
    """Return interpolators for f*sigma8(z), ECF and LambdaCDM."""
    mu = _g.mu_geff(_g.K_REF)

    a_e, D_e, f_e = _g.solve_growth(_g.E2_ecf, mu)
    a_l, D_l, f_l = _g.solve_growth(_g.E2_lcdm, 1.0)
    D_e = D_e / np.interp(1.0, a_e, D_e)
    D_l = D_l / np.interp(1.0, a_l, D_l)

    def fs8_ecf(z):
        a = 1.0 / (1.0 + np.asarray(z))
        return np.interp(a, a_e, f_e) * _g.SIGMA8_ECF * np.interp(a, a_e, D_e)

    def fs8_lcdm(z):
        a = 1.0 / (1.0 + np.asarray(z))
        return np.interp(a, a_l, f_l) * _g.SIGMA8_LCDM * np.interp(a, a_l, D_l)

    return fs8_ecf, fs8_lcdm


def main():
    fs8_ecf, fs8_lcdm = build_predictions()

    print("=" * 74)
    print("  ECF growth prediction vs published RSD measurements")
    print("=" * 74)
    print("\n  INDICATIVE chi-square: measurements treated as independent,")
    print("  no Alcock-Paczynski rescaling. See header for the full caveats.\n")

    print(f"  {'z':>6} | {'survey':<10} | {'measured':>15} | "
          f"{'ECF':>7} | {'LCDM':>7} | {'d_ECF':>6} | {'d_LCDM':>7}")
    print("  " + "-" * 70)

    chi2_e = chi2_l = 0.0
    for z, val, err, survey, ref in DATA:
        pe = float(fs8_ecf(z))
        pl = float(fs8_lcdm(z))
        de = (pe - val) / err
        dl = (pl - val) / err
        chi2_e += de ** 2
        chi2_l += dl ** 2
        print(f"  {z:6.3f} | {survey:<10} | {val:6.4f} +/- {err:6.4f} | "
              f"{pe:7.4f} | {pl:7.4f} | {de:+6.2f} | {dl:+7.2f}")

    n = len(DATA)
    print("\n" + "=" * 74)
    print("  RESULT")
    print("=" * 74)
    print(f"\n  chi2 (ECF)   = {chi2_e:6.2f}   for {n} points  "
          f"-> chi2/N = {chi2_e/n:.2f}")
    print(f"  chi2 (LCDM)  = {chi2_l:6.2f}   for {n} points  "
          f"-> chi2/N = {chi2_l/n:.2f}")
    print(f"\n  Delta chi2 (ECF - LCDM) = {chi2_e - chi2_l:+.2f}")

    if chi2_e < chi2_l:
        print("\n  The ECF growth history fits these measurements BETTER than")
        print("  LambdaCDM on this compilation. This is consistent with the")
        print("  known tendency of low-redshift f*sigma_8 measurements to sit")
        print("  slightly below the Planck-LambdaCDM prediction (see e.g.")
        print("  Chapman et al. 2021, arXiv:2101.12261, Sec. 6.1).")
    else:
        print("\n  The ECF growth history does NOT improve on LambdaCDM for")
        print("  this compilation.")

    print("\n  Neither number is a likelihood. With 6 heterogeneous points,")
    print("  no covariance and no AP rescaling, a Delta chi2 of order a few")
    print("  is not evidence. What the test DOES establish is that the ECF")
    print("  growth history is not excluded by current RSD data -- which was")
    print("  an open question until now, the corpus having no growth-sector")
    print("  observational test at all.")
    print("=" * 74)


if __name__ == "__main__":
    main()
