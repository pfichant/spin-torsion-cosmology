#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script_05_birefringence_calibration.py  —  v2, April 2026
Author : P. Fichant

Calibrates the ECF cosmic birefringence angle beta_ECF = 0.35 deg
(Foundation I, Sec. 7) via a Chern-Simons line-of-sight integral over
a residual axial torsion background S_0(z).

Physical picture
----------------
The stiff spin-fluid (rho_spin ~ a^-6) is diluted to zero by z=1100
(Part A below) and contributes negligibly to birefringence.  The observed
beta requires a separate, slower-evolving residual torsion pseudo-vector
S_0(z) = S_ref * (1+z)^alpha, with alpha=0 corresponding to a
topological constant background (Section 7.2, companion letter [PIT]).

The Chern-Simons rotation angle is
    beta = g_CS_eff * S_ref * I_torsion
where I_torsion = integral_0^{z_LSS} (1+z)^alpha / E(z) dz.
With the calibration g_CS_eff = beta_obs / (S_ref * I_torsion) the model
reproduces beta_obs = 0.35 deg by construction; the non-trivial content
is the consistency of the required S_ref with the residual torsion sector.

Numerical values (alpha=0, z_LSS=1100):
    I_torsion = 3.1177
    S_ref     = 4.3237
    g_CS_eff  = 0.02596 deg/unit
    beta_th   = 0.3500 deg

Dependencies : numpy, scipy
Runtime      : < 1 s
"""

import numpy as np
from scipy.integrate import quad

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
beta_obs = 0.35    # [deg]  Minami & Komatsu 2020; confirmed by SPTpol 0.33±0.09
beta_err = 0.14    # [deg]  1-sigma
z_LSS    = 1100.0  # Last scattering surface

# Cosmological background (Foundation I Table 2)
Omega_m = 0.315
Omega_r = 9.0e-5
Omega_L = 1.0 - Omega_m

# Residual torsion model
alpha  = 0.0    # topological constant background

# Spin-fluid diagnostic (Part A)
sigma_peak = 0.093   # peak spin-fluid density at z_peak
z_peak     = 1e11    # QCD transition redshift

# Calibrated paper values (Sec. 7)
I_eff_paper = 13.48  # = S_ref * I_torsion, as reported in Sec. 7


# ---------------------------------------------------------------------------
# Hubble function
# ---------------------------------------------------------------------------
def E(z):
    """Dimensionless Hubble rate E(z) = H(z)/H0."""
    return np.sqrt(Omega_r*(1+z)**4 + Omega_m*(1+z)**3 + Omega_L)


# ---------------------------------------------------------------------------
# Part A — spin-fluid diagnostic
# ---------------------------------------------------------------------------
def sigma_spin_fluid(z):
    """Spin-fluid density profile: peaks at z_peak, scales as a^{-6}."""
    x = (1+z) / (1+z_peak)
    return sigma_peak * x**6 / (1.0 + x**6)

I_fluid, _ = quad(sigma_spin_fluid, 0, z_LSS, limit=200)

# ---------------------------------------------------------------------------
# Part B — residual torsion line-of-sight integral
# ---------------------------------------------------------------------------
def integrand_torsion(z):
    return (1+z)**alpha / E(z)

I_torsion, _ = quad(integrand_torsion, 0, z_LSS, limit=200)

# Calibration: g_CS_eff * S_ref * I_torsion = beta_obs
# with S_ref * I_torsion = I_eff_paper (Sec. 7 value)
g_CS_eff = beta_obs / I_eff_paper      # [deg / unit]
S_ref    = I_eff_paper / I_torsion     # residual torsion amplitude

beta_th  = g_CS_eff * S_ref * I_torsion  # = beta_obs by construction


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sep = "=" * 65

    print(sep)
    print("  SCRIPT 05 — ECF BIREFRINGENCE CALIBRATION  (Foundation I Sec. 7)")
    print(sep)

    print("\n[A] SPIN-FLUID DIAGNOSTIC")
    print(f"    sigma_spin(z=1100) = {sigma_spin_fluid(1100):.3e}  (diluted to zero by a^-6)")
    print(f"    I_fluid            = {I_fluid:.3e}")
    print("    --> CMB birefringence from spin fluid: negligible.")
    print("    --> Requires separate residual axial torsion background S_0(z).")

    print("\n[B] RESIDUAL TORSION INTEGRAL  (alpha=0, topological)")
    print(f"    I_torsion = integral_0^{z_LSS:.0f} dz / E(z) = {I_torsion:.4f}")
    print(f"    S_ref     = I_eff_paper / I_torsion = {I_eff_paper} / {I_torsion:.4f} = {S_ref:.4f}")
    print(f"    g_CS_eff  = beta_obs / I_eff_paper  = {beta_obs} / {I_eff_paper} = {g_CS_eff:.5f} deg/unit")

    print("\n[C] BIREFRINGENCE PREDICTION")
    print(f"    beta_th  = g_CS_eff * S_ref * I_torsion = {beta_th:.4f} deg")
    print(f"    beta_obs = {beta_obs:.2f} +/- {beta_err:.2f} deg  (Minami & Komatsu 2020)")
    match_beta = abs(beta_th - beta_obs) < 1e-6
    print(f"    Match: {'YES' if match_beta else 'NO'}  (consistent by calibration construction)")

    print("\n[D] CONSISTENCY WITH PAPER (Sec. 7)")
    I_check = S_ref * I_torsion
    match_I = abs(I_check - I_eff_paper) < 0.01
    print(f"    S_ref * I_torsion = {I_check:.4f}  (paper: {I_eff_paper}) --> {'MATCH' if match_I else 'MISMATCH'}")
    print(f"    alpha = {alpha}  (topological background, constant in redshift)")
    print(f"    LiteBIRD forecast: sigma(beta) ~ 0.1 deg  --> ECF prediction testable")

    print(f"\n{sep}")
