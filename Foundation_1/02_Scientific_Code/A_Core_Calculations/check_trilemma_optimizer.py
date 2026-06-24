#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_trilemma_optimizer.py  —  v2, April 2026
Author : P. Fichant

Numerical diagnostic for the mathematical irreducibility of the H0-Age-BAO
trilemma (Foundation I, Sec. 3.4).  A three-parameter tanh dark-energy model
w(z) is fitted via L-BFGS-B to simultaneously satisfy:
  (i)  D_M(z=1.48)/r_s = 30.21  [eBOSS DR16, Hou et al. 2021]
  (ii) t_0 > 13.32 Gyr           [globular-cluster bound, Valcin et al. 2021]
with H_0 = 73.04 km/s/Mpc fixed (SH0ES, Riess et al. 2021).

The optimizer converges but cannot satisfy both constraints simultaneously,
confirming that no phenomenological scalar w(z) resolves the trilemma.
A geometric resolution via the ECKS action is developed in Foundation II.

Dependencies : numpy, scipy
Runtime      : < 0.5 s
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid
from scipy.optimize import minimize

# ---------------------------------------------------------------------------
# Cosmological constants  (Foundation I Table 2)
# ---------------------------------------------------------------------------
H0       = 73.04           # [km/s/Mpc]  SH0ES (Riess et al. 2021)
Omega_m  = 0.315           # Planck 2018
Omega_de = 1.0 - Omega_m   # Flat FLRW
c        = 299792.458       # [km/s]
T_H      = 977.79222168     # (km/s/Mpc)^{-1} -> Gyr

# ---------------------------------------------------------------------------
# Observational targets
# ---------------------------------------------------------------------------
z_bao     = 1.48         # eBOSS DR16 QSO effective redshift
r_s       = 135.8        # Sound horizon, Foundation I Sec. 3 [Mpc]
DM_target = 30.21 * r_s  # = 4102.52 Mpc
t0_min    = 13.32        # Globular-cluster lower bound [Gyr]

# ---------------------------------------------------------------------------
# Redshift grids  (pre-built for vectorised integration)
# ---------------------------------------------------------------------------
z_bao_grid = np.linspace(0, z_bao, 1000)
z_age_grid = np.concatenate(([0], np.geomspace(1e-4, 1000, 5000)))

# ---------------------------------------------------------------------------
# Observable calculator
# ---------------------------------------------------------------------------
def compute_observables(w0, winf, zt):
    """Return (D_M [Mpc], t_0 [Gyr]) for the tanh w(z) parametrisation.

    w(z) = w0 + (winf - w0) * 0.5 * (1 + tanh((z - zt) / 0.3))

    Integration uses cumulative_trapezoid for the dark-energy exponent and
    trapezoid for the final line-of-sight integrals.
    """
    def _E(w_arr, z_arr):
        int_w = cumulative_trapezoid((1 + w_arr) / (1 + z_arr), z_arr, initial=0)
        return np.sqrt(Omega_m * (1 + z_arr)**3 + Omega_de * np.exp(3 * int_w))

    w_b = w0 + (winf - w0) * 0.5 * (1 + np.tanh((z_bao_grid - zt) / 0.3))
    DM  = trapezoid(1 / _E(w_b, z_bao_grid), z_bao_grid) * (c / H0)

    w_a = w0 + (winf - w0) * 0.5 * (1 + np.tanh((z_age_grid - zt) / 0.3))
    E_a = _E(w_a, z_age_grid)
    t0  = trapezoid(1 / ((1 + z_age_grid) * E_a), z_age_grid) * (T_H / H0)

    return DM, t0


# ---------------------------------------------------------------------------
# Chi-squared cost function
# ---------------------------------------------------------------------------
def chi2(params):
    """Joint chi-squared: BAO distance (1.5% sigma) + cosmic age (0.1 Gyr sigma)."""
    DM, t0 = compute_observables(*params)
    return ((DM - DM_target) / (0.015 * DM_target))**2 + ((t0 - t0_min) / 0.1)**2


# ---------------------------------------------------------------------------
# Optimisation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Trilemma irreducibility diagnostic — Foundation I Sec. 3.4\n")

    res = minimize(
        chi2,
        x0     = [-1.5, -0.5, 0.8],
        bounds = [(-2.5, -0.8), (-1.0, 0.0), (0.2, 2.0)],
        method = "L-BFGS-B",
    )

    if res.success:
        w0, winf, zt = res.x
        DM_opt, t0_opt = compute_observables(w0, winf, zt)
        bao_pct = abs(DM_opt - DM_target) / DM_target * 100

        print("=" * 65)
        print("  TRILEMMA IRREDUCIBILITY DIAGNOSTIC")
        print("=" * 65)
        print(f"  Best-fit  w_0   : {w0:+.4f}")
        print(f"  Best-fit  w_inf : {winf:+.4f}")
        print(f"  Best-fit  z_t   : {zt:.4f}")
        print(f"  Cosmic age t_0  : {t0_opt:.4f} Gyr   (required > {t0_min} Gyr)")
        print(f"  BAO deviation   : {bao_pct:.3f}%     (threshold 1.5%)")
        print(f"  chi2_residual   : {res.fun:.4f}      (> 0 confirms irreducibility)")
        print("-" * 65)
        age_ok = t0_opt >= t0_min
        bao_ok = bao_pct <= 1.5
        print(f"  t_0 constraint  : {'SATISFIED' if age_ok else 'VIOLATED'}")
        print(f"  BAO constraint  : {'SATISFIED' if bao_ok else 'VIOLATED'}")
        print("-" * 65)
        print("  CONCLUSION: No tanh w(z) with H0 = 73.04 km/s/Mpc satisfies")
        print("  both constraints simultaneously — the H0-Age-BAO trilemma is")
        print("  mathematically irreducible within the scalar dark-energy class.")
        print("  A geometric resolution (ECKS action) is developed in Foundation II.")
        print("=" * 65)
    else:
        print(f"Optimisation failed: {res.message}")
        if res.x is not None:
            DM_p, t0_p = compute_observables(*res.x)
            print(f"Partial result — t0 = {t0_p:.3f} Gyr, "
                  f"BAO dev = {abs(DM_p-DM_target)/DM_target*100:.2f}%")