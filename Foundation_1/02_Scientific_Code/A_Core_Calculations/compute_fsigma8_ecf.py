#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation I -- The Metric Universe
Script      : compute_fsigma8_ecf.py
Author      : Pascal Fichant
Date        : 05/09/2026
Description :
    Solves the linear growth equation of Foundation I (Eq. growth_ode_geff)
    and returns f*sigma_8(z) for the ECF background, alongside LambdaCDM.

WHY THIS SCRIPT EXISTS
----------------------
Foundation I *writes* the growth equation with an effective modifier,

    D'' + 2 H D' - 4 pi G mu(a,k) rho_m D = 0        (Eq. growth_ode_geff)

but no script in this corpus ever *solved* it: S_8 is obtained from the
algebraic suppression formula in script_06_S8_resolution.py, and the growth
history itself was never integrated. This script closes that gap.

MOTIVATION (05/09/2026 literature review)
-----------------------------------------
Three independent 2026 results converge on structure growth as the
observable that discriminates the ECF from its background-degenerate
competitors:

  [1] Petri, Marra & von Marttens, Phys. Rev. D 113, 023504 (2026),
      arXiv:2508.17955 -- construct an interacting dark-sector model
      *exactly degenerate with CPL at the background level*; the models are
      "indistinguishable in background observables". Their interacting model
      is ruled out not by expansion but by growth: it predicts a sharp
      suppression of f*sigma_8(z) at z <~ 0.8, in tension with measurements.

  [2] Wang, Yu & Wu, arXiv:2609.03062 (02/09/2026) -- "These contrasting
      growth signatures, despite substantial degeneracies at the background
      level, highlight late-time large-scale-structure observations as a
      promising avenue for distinguishing dark-energy dynamics from
      dark-sector interactions."

  [3] Linder, arXiv:2512.03139 -- warns that both interacting and modified-
      gravity models built to cross the phantom divide "tend to run afoul of
      cosmic growth". The ECF trajectory *does* cross w = -1, at z = 1.684
      (see F1, Sec. dark energy). This script tests whether the ECF inherits
      that failure mode.

WHAT IS COMPUTED, AND WHAT IS NOT
---------------------------------
Computed: the linear growth factor D(a) on the ECF background, the growth
rate f = dlnD/dlna, and f*sigma_8(z), compared to LambdaCDM.

NOT computed: a full Boltzmann treatment. mu(a,k) is the phenomenological
Lorentzian modifier of F1 Eq. (geff_lorentzian), whose amplitude A_sup = 0.15
is phenomenological, not canonical and not derived (PO-F1-SIGMA0,
DEC-A7-POST-07C): it is not calibrated on S8 = 0.766, and its articulation
with gamma_spin is not demonstrated (no double counting). sigma8_ECF is the
S8 = 0.766 target converted with Omega_m = 0.2669, not a computed sigma8.
Scale dependence is evaluated at a
single reference k; the result is a background-level growth history, not a
substitute for CLASS-EC (PO-F3-9).

Usage:
    python compute_fsigma8_ecf.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# 1. Background -- imported from the solver that produces r_s = 135.65 Mpc (A-6)
#    (rule R13: the script is the reference, not the paper text)
# ---------------------------------------------------------------------------
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "_sh", os.path.join(_HERE, "script_01_solve_sound_horizon.py"))
_sh = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_sh)
except SystemExit:
    pass

Om_r     = _sh.Om_r
Om_m     = _sh.Om_m
Om_L     = _sh.Om_L
Om_spin  = _sh.Om_spin_0          # 2.72e-13, anchored at z_ref = 5600 (I82)
h_ecf    = 0.7304                 # ECF calibrated H0 = 73.04
h_lcdm   = 0.6736                 # Planck
# [A-7, 22/09/2026] ECF background uses Omega_i = omega_i / h_ECF^2 (physical
# densities of the solver divided by h_ECF^2). LCDM keeps the solver's Planck-h values.
_r2 = (h_lcdm / h_ecf) ** 2
Om_m_E    = Om_m * _r2              # = (omega_b+omega_c)/h_ECF^2 = 0.26687
Om_r_E    = Om_r * _r2
Om_spin_E = Om_spin * _r2
Om_L_E    = 1.0 - Om_m_E - Om_r_E - Om_spin_E
import os as _os
_KEEP_S8 = _os.environ.get('LOTA67_SIGMA8_MODE', 'fromS8') == 'fromS8'

# ---------------------------------------------------------------------------
# 2. Growth modifier -- F1 Eq. (geff_lorentzian)
#    mu(k) = 1 - A_sup * (k/k_*)^2 / [1 + (k/k_*)^2]
# ---------------------------------------------------------------------------
A_SUP  = 0.15          # phenomenological amplitude, not canonical, NOT derived (DEC-A7-POST-07C)
K_STAR = 0.10          # h/Mpc, characteristic scale, F1
K_REF  = 0.10          # h/Mpc, reference scale for f*sigma8 (~ survey scale)

# [E2, 22/09/2026 -- DEC-A7-POST-07] SIGMA8_ECF below is the S8 = 0.766 TARGET
# converted with Om_m = 0.2669, NOT a computed sigma8. The CAMB LCDM reference
# on the A-7 background gives sigma8 = 0.8252, S8 = 0.7800
# (calc_S8_reference_camb_A7.py, CALCULATED-CONDITIONAL, not an ECF result).
SIGMA8_LCDM = 0.812    # Planck 2018
SIGMA8_ECF  = (0.766 / (Om_m_E / 0.3) ** 0.5) if _KEEP_S8 else 0.747   # [A-7] sigma8 = S8/sqrt(Om_m/0.3) with Om_m = 0.2669 ; was 0.747 (Om_m = 0.315)


def mu_geff(k):
    """Effective gravitational modifier, scale-dependent, time-independent
    in the calibrated regime (F1 Sec. structure growth)."""
    x2 = (k / K_STAR) ** 2
    return 1.0 - A_SUP * x2 / (1.0 + x2)


def E2_ecf(a):
    """Dimensionless H^2/H0^2 on the ECF background.
    Positive spin term: this is the branch that produces the published
    results (registry entry I81)."""
    z = 1.0 / a - 1.0
    return (Om_r_E * (1 + z) ** 4 + Om_m_E * (1 + z) ** 3
            + Om_spin_E * (1 + z) ** 6 + Om_L_E)


def E2_lcdm(a):
    z = 1.0 / a - 1.0
    return Om_r * (1 + z) ** 4 + Om_m * (1 + z) ** 3 + (1.0 - Om_m - Om_r)


# ---------------------------------------------------------------------------
# 3. Growth equation, in ln a
#     D'' + [2 + dlnE/dlna] D' - (3/2) Om_m(a) mu D = 0
# ---------------------------------------------------------------------------
def _growth_rhs(lna, y, E2fun, mu):
    a = np.exp(lna)
    D, dD = y
    eps = 1e-6
    dlnE = (np.log(E2fun(a * (1 + eps))) - np.log(E2fun(a * (1 - eps)))) \
        / (2 * eps) / 2.0                       # /2 because E2 -> E
    Om_a = (Om_m_E if E2fun is E2_ecf else Om_m) / (a ** 3 * E2fun(a))
    d2D = -(2.0 + dlnE) * dD + 1.5 * Om_a * mu * D
    return [dD, d2D]


def solve_growth(E2fun, mu, a_ini=1e-3, a_end=1.0, n=4000):
    """Integrate from matter domination (D ∝ a) to today."""
    lna = np.linspace(np.log(a_ini), np.log(a_end), n)
    sol = solve_ivp(_growth_rhs, (lna[0], lna[-1]), [a_ini, a_ini],
                    t_eval=lna, args=(E2fun, mu),
                    rtol=1e-10, atol=1e-12, method="RK45")
    a = np.exp(sol.t)
    D = sol.y[0]
    f = np.gradient(np.log(D), sol.t)           # f = dlnD/dlna
    return a, D, f


# ---------------------------------------------------------------------------
# 4. Run and report
# ---------------------------------------------------------------------------
def main():
    mu = mu_geff(K_REF)
    print("=" * 70)
    print("  f*sigma_8(z) on the ECF background -- linear growth")
    print("=" * 70)
    print(f"\n  Background LCDM: Om_m={Om_m:.4f}  Om_r={Om_r:.3e}  Om_L={Om_L:.4f}")
    print(f"  Background ECF : Om_m={Om_m_E:.5f}  Om_r={Om_r_E:.3e}  "
          f"Om_spin,0={Om_spin_E:.3e}  Om_L={Om_L_E:.5f}")
    print(f"  Modifier  : mu(k={K_REF} h/Mpc) = {mu:.5f}   "
          f"(A_sup={A_SUP}, k_*={K_STAR})")
    print(f"  sigma_8   : LCDM {SIGMA8_LCDM}  |  ECF {SIGMA8_ECF:.4f}")

    a_e, D_e, f_e = solve_growth(E2_ecf, mu)
    a_l, D_l, f_l = solve_growth(E2_lcdm, 1.0)

    D_e /= np.interp(1.0, a_e, D_e)             # normalise D(a=1) = 1
    D_l /= np.interp(1.0, a_l, D_l)

    print("\n" + "-" * 70)
    print("  f*sigma_8(z) -- ECF vs LambdaCDM")
    print("-" * 70)
    print(f"  {'z':>6} | {'f_ECF':>8} | {'fs8_ECF':>9} | "
          f"{'fs8_LCDM':>9} | {'ratio':>7}")
    print("  " + "-" * 60)

    rows = []
    for z in (0.0, 0.15, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0):
        a = 1.0 / (1.0 + z)
        fe = np.interp(a, a_e, f_e)
        fl = np.interp(a, a_l, f_l)
        fs8_e = fe * SIGMA8_ECF * np.interp(a, a_e, D_e)
        fs8_l = fl * SIGMA8_LCDM * np.interp(a, a_l, D_l)
        rows.append((z, fe, fs8_e, fs8_l, fs8_e / fs8_l))
        print(f"  {z:6.2f} | {fe:8.4f} | {fs8_e:9.4f} | "
              f"{fs8_l:9.4f} | {fs8_e/fs8_l:7.4f}")

    # --- the test that matters: is there a sharp drop at z < 0.8 ? ---
    print("\n" + "=" * 70)
    print("  TEST -- the failure mode of the interacting model [1]")
    print("=" * 70)
    r08 = [r[4] for r in rows if r[0] <= 0.8]
    swing = (max(r08) - min(r08)) / np.mean(r08) * 100
    print(f"\n  ECF/LCDM ratio over z = 0 - 0.8 : "
          f"{min(r08):.4f} to {max(r08):.4f}  (swing {swing:.2f} %)")
    print("\n  Reference [1] rules out its interacting model because it predicts")
    print("  a *sharp suppression* of f*sigma_8 below z ~ 0.8. The ECF")
    print("  suppression here is nearly redshift-independent: it rescales the")
    print("  amplitude without distorting the shape, so it does not reproduce")
    print("  that failure mode.")
    print("\n  CAVEAT: linear, single-k, phenomenological mu. A_sup = 0.15 is")
    print("  phenomenological, not canonical and not derived (PO-F1-SIGMA0,")
    print("  DEC-A7-POST-07C); its articulation with gamma_spin is not demonstrated")
    print("  (no double counting). sigma8_ECF is the S8 = 0.766 target converted,")
    print("  not computed. Not a substitute for a Boltzmann treatment (PO-F3-9, CLASS-EC).")
    print("=" * 70)


if __name__ == "__main__":
    main()
