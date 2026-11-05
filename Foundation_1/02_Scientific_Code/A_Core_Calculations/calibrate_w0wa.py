#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate_w0wa.py  --  ECF Foundation I
==========================================================================
Origin of the ECF dark-energy trajectory parameters (w0, wa).

EPISTEMIC STATUS (honest; cf. open problem PO-F1-B):
--------------------------------------------------------------------------
  * w0 comes from an EMPIRICAL IDENTIFICATION: w0 = -1 + Omega_spin,peak
#   (wording corrected 23/08/2026 -- this said DERIVED; Foundation I calls
#   the same relation "an EMPIRICAL identification". The numbers match,
#   but the relation does not come from the action.)  (direct geometric relation
    between the dark-energy deficit and the residual spin density).
      -> -1 + 0.093 = -0.907, i.e. -0.904 to within 0.3%.

  * wa is NOT derived ab initio. It is written wa = -xi * Omega_spin,peak
    where xi ~ 1.6 is a PHENOMENOLOGICAL factor encoding the dilution
    rate of the torsion debt. The value of xi is calibrated to reproduce
    the DESI preference; deriving it from the condensate dynamics
    <dS^2>(z) remains an open problem (cf. Foundation II, PO-F2-4).

This script (i) computes w0 from Omega_spin, (ii) reports the xi required
for a given wa, and (iii) tests the resulting CPL trajectory against the
a ten-observable subset of the DESI DR1 BAO data, with diagonal errors -- not the
global DESI DR1 chi2. It does NOT claim to derive wa; it isolates exactly
what is missing.
==========================================================================
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
from scipy.integrate import quad

# --------------------------------------------------------------------------
# 1. ECF inputs (calibrated upstream; NOT fitted here)
# --------------------------------------------------------------------------
OMEGA_SPIN_PEAK = 0.093     # spin/rad ratio -> Omega_spin (script_01_solve_sound_horizon.py)
# [02/09/2026] 1-sigma on Omega_spin_peak. UPDATED same day: an initial value
# of 0.0050 came from the "acceptable region" method (dossier section 2), a
# cruder one-sided tolerance scan. profile_likelihood_calibrated.py already
# existed with a more rigorous method (proper Delta-chi2 <= 1 likelihood
# profiling against r_s = 135.8 +/- 0.2 Mpc) and gives 0.004 -- close, but not
# identical, and that script is authoritative: deferring to it here avoids
# two scripts quoting different sigma for the same quantity.
SIGMA_OMEGA_SPIN_PEAK = 0.004
XI_TORSION      = 1.645     # phenomenological factor (NOT derived, PO-F1-B)
H0_ECF          = 73.04     # km/s/Mpc  (ECF calibration)
RS_ECF          = 135.65    # Mpc  [A-6 22/09/2026] was 135.8
C_KM            = 299792.458
# [D3, 22/09/2026 -- DEC-A7-POST-05] OMEGA_R = omega_r/h_ECF^2 (same rule as A-7 for
# OMEGA_M; was 9.24e-5, a Planck-h value).
OMEGA_M, OMEGA_R = (0.02237 + 0.1200)/0.7304**2, 2.4728e-5*(1 + (7/8)*(4/11)**(4/3)*3.046)/0.7304**2   # [A-7] OMEGA_M was 0.315
OMEGA_DE        = 1.0 - OMEGA_M - OMEGA_R

# --------------------------------------------------------------------------
# 2. (w0, wa) from physics + phenomenological factor
# --------------------------------------------------------------------------
def w0_from_spin(omega_spin):
    """DERIVED: dark-energy deficit = residual spin density."""
    return -1.0 + omega_spin

def wa_from_spin(omega_spin, xi):
    """PHENOMENOLOGICAL: xi not derived (PO-F1-B)."""
    return -xi * omega_spin

# --------------------------------------------------------------------------
# 3. CPL distances for the BAO test
# --------------------------------------------------------------------------
def rho_de(z, w0, wa):
    a = 1.0/(1.0+z)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*(1-a))

def E(z, w0, wa):
    return np.sqrt(OMEGA_M*(1+z)**3 + OMEGA_R*(1+z)**4 + OMEGA_DE*rho_de(z,w0,wa))

def DM_rs(z, w0, wa):
    I,_ = quad(lambda zp: 1.0/E(zp,w0,wa), 0, z)
    return (C_KM/H0_ECF)*I / RS_ECF

def DH_rs(z, w0, wa):
    return (C_KM/H0_ECF)/E(z,w0,wa) / RS_ECF

# [Q5, 22/09/2026 -- Audit decision] TEN-OBSERVABLE SUBSET of DESI DR1, diagonal errors.
# D_M/r_d and D_H/r_d of LRG1 (z=0.510), LRG2 (0.706), LRG3+ELG1 (0.930), ELG2 (1.317)
# and Lyman-alpha (2.330), each checked line by line against Table 1 of Adame et al. 2024
# (arXiv:2404.03002). NOT included: BGS (D_V/r_d), QSO (D_V/r_d), and the published
# intra-bin D_M-D_H correlations. The chi2 below is therefore a subset chi2 under a
# diagonal approximation, and must NOT be quoted as the global DESI DR1 chi2.
BAO = [  # DESI DR1 (Adame et al. 2024), ten-observable subset, diagonal errors
    (0.510, 13.62, 0.25, 20.98, 0.61), (0.706, 16.85, 0.32, 20.08, 0.60),
    (0.930, 21.71, 0.28, 17.88, 0.35), (1.317, 27.79, 0.69, 13.82, 0.42),
    (2.330, 39.71, 0.94, 8.52, 0.17),
]
def chi2(w0, wa):
    x=0.0
    for z,dm,sdm,dh,sdh in BAO:
        x += ((DM_rs(z,w0,wa)-dm)/sdm)**2 + ((DH_rs(z,w0,wa)-dh)/sdh)**2
    return x

# --------------------------------------------------------------------------
# 4. Run
# --------------------------------------------------------------------------
if __name__ == "__main__":
    w0 = w0_from_spin(OMEGA_SPIN_PEAK)
    wa = wa_from_spin(OMEGA_SPIN_PEAK, XI_TORSION)

    print("="*60)
    print("  ECF dark-energy trajectory: origin of the parameters")
    print("="*60)
    print(f"\n  [EMPIRICAL ID] w0 = -1 + Omega_spin = -1 + {OMEGA_SPIN_PEAK}")
    print(f"             w0 = {w0:+.4f}   (corpus: -0.904, offset {abs(w0+0.904)/0.904*100:.1f}%)")
    print(f"\n  [PHENOM ]  wa = -xi * Omega_spin,  xi = {XI_TORSION} (NOT derived, PO-F1-B)")
    print(f"             wa = {wa:+.4f}   (corpus: -0.153, offset {abs(wa+0.153)/0.153*100:.1f}%)")
    print(f"\n  xi required for exact wa = -0.153: {0.153/OMEGA_SPIN_PEAK:.3f}")

    print("\n  --- uncertainty propagation from Omega_spin_peak [02/09/2026] ---")
    sigma_w0 = SIGMA_OMEGA_SPIN_PEAK                    # d(w0)/d(Omega_spin) = 1
    sigma_wa = XI_TORSION * SIGMA_OMEGA_SPIN_PEAK        # d(wa)/d(Omega_spin) = -xi, held fixed
    print(f"  sigma(Omega_spin_peak) = {SIGMA_OMEGA_SPIN_PEAK}  (floor, see header)")
    print(f"  sigma(w0) = {sigma_w0:.4f}   ->  w0 = {w0:+.4f} +/- {sigma_w0:.4f}")
    print(f"  sigma(wa) = {sigma_wa:.4f}   ->  wa = {wa:+.4f} +/- {sigma_wa:.4f}")
    print(f"  NOTE: xi itself is held FIXED here -- it is phenomenological, reverse-")
    print(f"  engineered to match wa = -0.153, not an independently measured input,")
    print(f"  so it has no natural sigma of its own to propagate (PO-F1-B).")
    print(f"  Both bars are floors: covering Omega_spin_peak alone, one parameter")
    print(f"  at a time (see script_01 for the same caveat on r_s).")

    print("\n  --- trajectory test vs a TEN-OBSERVABLE SUBSET of DESI DR1 BAO ---")
    print("      (diagonal errors; NOT the global DESI DR1 chi2)")
    print(f"  chi^2(ECF w0,wa) = {chi2(w0,wa):.2f}")
    print(f"  chi^2(LCDM)      = {chi2(-1.0,0.0):.2f}")
    print(f"  ({2*len(BAO)} observables: 5 tracers x (D_M/r_d, D_H/r_d); no BGS, no QSO, no covariance)")

    print("\n  STATUS: w0 from an empirical identification with the spin; xi (hence wa) remains")
    print("  phenomenological. Deriving xi from <dS^2>(z): open problem")
    print("  PO-F1-B / PO-F2-4.")
    print("="*60)
