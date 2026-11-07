#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_ecf_aic_desi.py  --  ECF Foundation II
==========================================================================
Delta-AIC of the ECF dark-energy point against LambdaCDM, full-covariance
DESI DR1 comparison (Foundation III MCMC).

CONTEXT (correction of record, 31/08/2026):
--------------------------------------------------------------------------
  An earlier version of this paragraph quoted "Delta chi^2 ~= +16,
  Delta AIC = +14 in favour of the torsion model", computed under
  DIAGONAL-ERRORS DESI statistics. That comparison was superseded when
  Foundation III rebuilt the DESI DR1 Mahalanobis distance with the
  published covariance matrix. [Q4, 22/09/2026] That block was itself
  reconstructed: two rows attributed to the DESI QSO tracer are not published
  by DESI DR1, which gives that tracer a DV/rd only. With the 12x12 block and
  the correlations of Table 1 of Adame et al. 2024 (r in [-0.389,-0.477]),
  Delta chi^2(ECF-LambdaCDM) = +6.21 (Planck prior) and +38.59 (SH0ES prior)
  -- see plot_ecf_desi_mcmc_v3_0.py. The historical values with the former
  13-row block were +8.06 and +41.94. The "+16 / +14" figures
  are NOT reproduced by any script in this repository and should not be
  cited.

  This script computes the correctly-updated Delta-AIC using those two
  full-covariance Delta chi^2 values, with the parameter count Delta k=1
  established in Foundation II Sec. "Information-theoretic advantage":
  w0 costs nothing (empirical identification w0 = -1 + Omega_spin,peak,
  already calibrated in the background sector); wa costs one parameter,
  the phenomenological factor xi in wa = -xi * Omega_spin,peak
  (PO-F1-B, calibrate_w0wa.py).

RESULT (honest): a POSITIVE Delta AIC means the ECF point is NOT favoured
by this criterion either, consistent with the Mahalanobis-distance
conclusion already stated in the same section. This script does not
compute a new fit; it applies AIC = chi^2 + 2k to numbers already
established elsewhere, so that the arithmetic is not left for the reader
to redo silently.
==========================================================================
"""
# Last modified: 31/08/2026, tres tard (Paris time)
# Corpus: Foundation II — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Inputs, traced to their source ──────────────────────────────────────
# Delta chi^2(ECF - LambdaCDM), DESI DR1 covariance matrix, 12 observables,
# Foundation III MCMC (plot_F3_ecf_desi_mcmc_v3.py), reproduced identically
# in Foundation I (App. and main text) and Foundation II (main text).
# [Q2/Q3, 22/09/2026] The block was reconstructed: the two rows attributed to the
# DESI QSO tracer (DM/rd, DH/rd at z_eff = 1.491) are not published by DESI DR1,
# which gives that tracer a DV/rd only. Historical values with the old 13-row
# block: 8.06 (Planck) and 41.94 (SH0ES).
DCHI2_PLANCK = 6.21
DCHI2_SH0ES = 38.59

# Parameter-count delta for the ECF dark-energy trajectory relative to
# LambdaCDM: w0 is free (empirical identification, no extra parameter);
# wa costs exactly one calibrated parameter, xi (PO-F1-B).
DELTA_K_ECF = 1

# For comparison only: CPL fitted directly to DESI (2 extra parameters).
DELTA_K_CPL = 2


def delta_aic(dchi2: float, dk: int) -> float:
    """AIC = chi^2 + 2k  =>  Delta AIC = Delta chi^2 + 2 Delta k."""
    return dchi2 + 2 * dk


def main() -> None:
    print("Delta-AIC(ECF - LambdaCDM), full-covariance DESI DR1")
    print("=" * 58)
    for label, dchi2 in (("Planck prior", DCHI2_PLANCK),
                          ("SH0ES prior", DCHI2_SH0ES)):
        daic = delta_aic(dchi2, DELTA_K_ECF)
        verdict = "NOT favoured" if daic > 0 else "favoured"
        print(f"  {label:12s}: Delta chi^2 = {dchi2:+.2f}, "
              f"Delta k = {DELTA_K_ECF}  ->  Delta AIC = {daic:+.2f} "
              f"({verdict} over LambdaCDM)")

    print()
    print("Superseded figure (diagonal errors only, DO NOT CITE):")
    print(f"  Delta chi^2 ~= +16, Delta AIC = +14 "
          f"(this script does not reproduce this value)")

    print()
    print("For reference, CPL fitted directly to DESI:")
    print(f"  Delta k = {DELTA_K_CPL}  (2 free parameters, no prior "
          f"calibration)")


if __name__ == "__main__":
    main()
