#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_S8_reference_camb_A7.py  --  Foundation I
===============================================
CAMB LambdaCDM reference for S8 on the A-7 background, and the conditional
gamma_spin it implies.  (DEC-A7-POST-07 revised, 22/09/2026)

STATUS: CALCULATED-CONDITIONAL -- LambdaCDM reference on the A-7 background,
NOT an ECF prediction.
    CAMB solves LambdaCDM perturbations. It does not contain the early-time
    ECF physics (spin sector) that sets the ECF acoustic scale: the reference
    run below gives r_drag ~ 147.1 Mpc, whereas the ECF chain uses
    r_s = 135.65 Mpc. The transfer function, and hence sigma8, may be changed
    by that physics. S8 = 0.766 (KiDS-1000 3x2pt, Heymans+2021) is used here
    only as an observational TARGET.

What is computed
----------------
 1. Control: Planck 2018 TT,TE,EE+lowE+lensing parameters (h = 0.6736)
    -> sigma8, S8 (expected ~ 0.811 / ~ 0.831).
 2. Same physical densities and primordial parameters (omega_b, omega_c,
    ln10^10 A_s, n_s, tau, sum m_nu unchanged), background moved to the A-7
    value h = 0.7304 -> Omega_m = omega_m/h^2, sigma8, S8_ref.
 3. Conditional gamma_spin, same phenomenological form as script_06:
        gamma_cond = (S8_ref / 0.766 - 1) / (F_ion - 1),  F_ion = 1.2765,
    with the KiDS-1000 interval +0.020/-0.014 propagated (S8_obs only).
    Status: CALCULATED-CONDITIONAL / EXPLORATORY. Physical gamma_spin: OPEN.
 4. Phenomenological spectral suppression
        T^2(k) = 1 - A_sup k^2 / (k^2 + k_cut^2),  k_cut = 0.10 h/Mpc,
    propagated into sigma8 (top-hat window, R = 8 Mpc/h): the factor for
    the former A_sup = 0.15, and the A_sup that alone would bring S8 to 0.766.
    Diagnostic only: A_sup is not canonical, and gamma_spin and T^2(k) must
    not be added as two independent suppressions (no double counting).
 5. Sensitivity: no massive neutrino; sigma8 held at its Planck value.

Neither gamma_cond nor A_sup(0.766) is a new ECF calibration. A predictive S8
requires a closed ECF perturbation chain (A_s, n_s -> ECF perturbations ->
T(k) -> P(k, z) -> sigma8 -> S8), which does not exist yet.

Dependencies: camb (tested with 2.0.4), numpy, scipy.
Output: S8_reference_camb_A7.json, written next to this script.
Derived from the Corpus reference calculation of 22/09/2026.
"""
# Last modified: 22/09/2026 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os

import numpy as np
from scipy.optimize import brentq

try:
    import camb
except ImportError:                                   # pragma: no cover
    sys.exit("calc_S8_reference_camb_A7.py requires camb (pip install camb)")

# ---------------------------------------------------------------------------
# 1. INPUTS
# ---------------------------------------------------------------------------
S8_OBS, S8_PLUS, S8_MINUS = 0.766, 0.020, 0.014   # KiDS-1000 3x2pt target
F_ION = 1.2765                                   # fixed on r_s (script_01)
# Planck 2018 TT,TE,EE+lowE+lensing physical and primordial parameters
OMB, OMC, LN10AS, NS, TAU, MNU = 0.02237, 0.1200, 3.044, 0.9649, 0.0544, 0.06
H_PLANCK, H_A7 = 0.6736, 0.7304
A_SUP_FORMER, K_CUT = 0.15, 0.10                 # former T^2(k) amplitude, h/Mpc
S8_LCDM_HIST, GAMMA_HIST = 0.832, 0.3116         # historical calibration inputs

OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "S8_reference_camb_A7.json")

_trapz = getattr(np, "trapezoid", None) or np.trapz


# ---------------------------------------------------------------------------
# 2. FUNCTIONS
# ---------------------------------------------------------------------------
def run(h, mnu=MNU, kmax=20.0):
    """CAMB run at fixed physical densities; returns (summary, k [h/Mpc], P(k, z=0))."""
    p = camb.set_params(H0=100 * h, ombh2=OMB, omch2=OMC, mnu=mnu, omk=0, tau=TAU,
                        As=np.exp(LN10AS) * 1e-10, ns=NS, WantTransfer=True)
    p.set_matter_power(redshifts=[0.0], kmax=kmax)
    r = camb.get_results(p)
    s8 = float(r.get_sigma8_0())
    om = (OMB + OMC + mnu / 93.14) / h ** 2
    kh, _z, pk = r.get_matter_power_spectrum(minkh=1e-4, maxkh=kmax, npoints=2000)
    d = dict(h=h, Om=om, sigma8=s8, S8=s8 * np.sqrt(om / 0.3),
             theta100=100 * r.cosmomc_theta(),
             rdrag=float(r.get_derived_params()["rdrag"]))
    return d, kh, pk[0]


def sigma_R(kh, pk, R=8.0, T2=None):
    """sigma_R from P(k) with a top-hat window, optionally multiplied by T2(k)."""
    x = kh * R
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    f = pk * (T2(kh) if T2 else 1.0) * W ** 2 * kh ** 2 / (2 * np.pi ** 2)
    return np.sqrt(_trapz(f, kh))


def gamma_cond(s8_ref, s8_obs=S8_OBS):
    """Inversion of S8_obs = S8_ref / [1 + (F_ion - 1) gamma]."""
    return (s8_ref / s8_obs - 1.0) / (F_ION - 1.0)


def T2f(A, kc=K_CUT):
    return lambda k: 1.0 - A * k ** 2 / (k ** 2 + kc ** 2)


# ---------------------------------------------------------------------------
# 3. MAIN
# ---------------------------------------------------------------------------
def main():
    out = {}
    for lab, h in [("Planck_h0.6736", H_PLANCK), ("A7_h0.7304", H_A7)]:
        d, kh, pk = run(h)
        s_num = sigma_R(kh, pk)
        d["sigma8_integrated_check"] = float(s_num)
        fac = sigma_R(kh, pk, T2=T2f(A_SUP_FORMER)) / s_num
        d["sigma8_factor_T2_Asup0.15"] = float(fac)
        d["S8_with_T2_Asup0.15"] = float(d["S8"] * fac)
        try:
            A = brentq(lambda a: d["S8"] * sigma_R(kh, pk, T2=T2f(a)) / s_num - S8_OBS,
                       0.0, 0.99)
        except ValueError:
            A = float("nan")
        d["A_sup_for_0.766"] = float(A)
        g = gamma_cond(d["S8"])
        d["gamma_cond"] = float(g)
        d["gamma_cond_plus"] = float(gamma_cond(d["S8"], S8_OBS - S8_MINUS) - g)
        d["gamma_cond_minus"] = float(g - gamma_cond(d["S8"], S8_OBS + S8_PLUS))
        out[lab] = d
    d0, _, _ = run(H_A7, mnu=0.0)
    out["A7_h0.7304_no_massive_nu"] = dict(sigma8=d0["sigma8"], S8=d0["S8"], Om=d0["Om"],
                                           gamma_cond=float(gamma_cond(d0["S8"])))
    s8P, omA = out["Planck_h0.6736"]["sigma8"], out["A7_h0.7304"]["Om"]
    S8fix = s8P * np.sqrt(omA / 0.3)
    out["A7_sigma8_held_fixed"] = dict(sigma8=s8P, S8=float(S8fix),
                                       gamma_cond=float(gamma_cond(S8fix)))
    out["historical_reference"] = dict(S8_LCDM=S8_LCDM_HIST, gamma_spin_historical=GAMMA_HIST,
                                       gamma_check=float(gamma_cond(S8_LCDM_HIST)))
    out["status"] = ("CALCULATED-CONDITIONAL: CAMB LambdaCDM reference on the A-7 background, "
                     "not an ECF prediction (DEC-A7-POST-07 revised)")
    out["versions"] = dict(camb=camb.__version__, numpy=np.__version__)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    P, A7 = out["Planck_h0.6736"], out["A7_h0.7304"]
    sep = "=" * 74
    print(sep)
    print("  CAMB LCDM REFERENCE FOR S8 ON THE A-7 BACKGROUND  (DEC-A7-POST-07 revised)")
    print("  STATUS: CALCULATED-CONDITIONAL -- LCDM reference, NOT an ECF prediction")
    print(sep)
    print(f"  camb {camb.__version__}, numpy {np.__version__}")
    print("\n[1] CONTROL -- Planck 2018 background (h = 0.6736)")
    print(f"  Omega_m = {P['Om']:.4f}   sigma8 = {P['sigma8']:.4f}   S8 = {P['S8']:.4f}"
          f"   r_drag = {P['rdrag']:.1f} Mpc")
    print(f"  sigma8 from the integrated P(k) (numerical check) = {P['sigma8_integrated_check']:.4f}")
    print("\n[2] A-7 BACKGROUND (h = 0.7304, same physical densities and primordial parameters)")
    print(f"  Omega_m = {A7['Om']:.4f}   sigma8 = {A7['sigma8']:.4f}   S8_ref = {A7['S8']:.4f}"
          f"   r_drag = {A7['rdrag']:.1f} Mpc")
    print(f"  sigma8 from the integrated P(k) (numerical check) = {A7['sigma8_integrated_check']:.4f}")
    print(f"  residual to the KiDS-1000 target: {S8_OBS}/{A7['S8']:.4f} - 1 = "
          f"{(S8_OBS / A7['S8'] - 1) * 100:+.1f} %")
    print("  (the CAMB run carries no ECF early-time physics: r_drag ~ 147.1 Mpc vs r_s = 135.65 Mpc)")
    print("\n[3] CONDITIONAL gamma  -- CALCULATED-CONDITIONAL / EXPLORATORY")
    print(f"  gamma_cond = (S8_ref/{S8_OBS} - 1)/(F_ion - 1) = {A7['gamma_cond']:.4f}"
          f" +{A7['gamma_cond_plus']:.3f}/-{A7['gamma_cond_minus']:.3f}   (S8_obs interval only)")
    print(f"  same inversion on the historical S8_LCDM = {S8_LCDM_HIST}: "
          f"{out['historical_reference']['gamma_check']:.4f}  (historical calibration {GAMMA_HIST})")
    print(f"  same inversion on the CAMB Planck control: {P['gamma_cond']:.4f}"
          f" +{P['gamma_cond_plus']:.3f}/-{P['gamma_cond_minus']:.3f}")
    print("  compatible with zero; not a canonical calibration; physical gamma_spin: OPEN")
    print("\n[4] PHENOMENOLOGICAL T^2(k) = 1 - A_sup k^2/(k^2 + k_cut^2), k_cut = 0.10 h/Mpc  (diagnostic)")
    print(f"  Planck control: sigma8 factor (A_sup = 0.15) = {P['sigma8_factor_T2_Asup0.15']:.4f}"
          f"  -> S8 = {P['S8_with_T2_Asup0.15']:.4f};  A_sup for 0.766 = {P['A_sup_for_0.766']:.4f}")
    print(f"  A-7 reference : sigma8 factor (A_sup = 0.15) = {A7['sigma8_factor_T2_Asup0.15']:.4f}"
          f"  -> S8 = {A7['S8_with_T2_Asup0.15']:.4f};  A_sup for 0.766 = {A7['A_sup_for_0.766']:.4f}")
    print("  A_sup is phenomenological, not canonical; gamma_spin and T^2(k) are NOT two")
    print("  independent suppressions to be added (no double counting)")
    print("\n[5] SENSITIVITY (A-7 background)")
    n0, fx = out["A7_h0.7304_no_massive_nu"], out["A7_sigma8_held_fixed"]
    print(f"  no massive neutrino    : sigma8 = {n0['sigma8']:.4f}  S8 = {n0['S8']:.4f}"
          f"  gamma_cond = {n0['gamma_cond']:.4f}")
    print(f"  sigma8 held at Planck  : sigma8 = {fx['sigma8']:.4f}  S8 = {fx['S8']:.4f}"
          f"  gamma_cond = {fx['gamma_cond']:.4f}")
    print("-" * 74)
    print(f"  JSON written: {os.path.basename(OUT_JSON)}")
    print(sep)


if __name__ == "__main__":
    main()
