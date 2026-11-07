#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive_microknot_observables.py  --  ECF Foundation II
=============================================================================
Every quantity that follows from the Micro-Knot mass, computed rather than
quoted.

WHY THIS SCRIPT EXISTS
----------------------
Foundation II quotes a Hawking temperature, an evaporation timescale, an
Einstein radius and a microlensing crossing time, all of which follow from
M_micro. Until 27/08/2026 none of them was reproducible: the numbers were in
the text and in no script. Two were wrong, and the error survived because
nothing recomputed them.

This is an open-science requirement rather than a convenience: a figure that
cannot be regenerated is a claim that cannot be checked.

WHAT IT FIXES, ON THE RECORD
----------------------------
  (1) Hawking temperature. The corpus quoted T_H = 2.7 mK and "three orders
      of magnitude below the CMB". Neither matches any mass in play: 2.7 mK
      would require 4.5e25 kg. The correct value at M = 3.74e24 kg is 33 mK,
      which is TWO orders below the CMB.

  (2) Evaporation timescale. The corpus quoted "> 1e83 yr". The Page formula
      gives ~1e50 yr -- thirty-three orders of magnitude apart. Both errors
      predate the mass revision of 27/08 and are independent of it.

The physical conclusions are unchanged: T_H stays well below the CMB, so no
evaporation; and 1e50 yr is still vastly longer than the age of the universe.
The corpus was right about the physics and wrong about the numbers.

FORMULAE, WITH SOURCES
----------------------
  Hawking temperature   T_H  = hbar c^3 / (8 pi G M k_B)          [Hawking 1975]
  Evaporation time      t_ev = 5120 pi G^2 M^3 / (hbar c^4)       [Page 1976]
  Schwarzschild radius  r_s  = 2 G M / c^2
  Einstein radius       theta_E = sqrt(4GM/c^2 * (D_S-D_L)/(D_L D_S))
  Crossing time         t_E  = theta_E D_L / v_rel                => t_E ~ sqrt(M)

Dependency: numpy. Usage: python3 derive_microknot_observables.py
=============================================================================
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

# --- constants -------------------------------------------------------------
C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054572e-34
K_B = 1.380649e-23
T_CMB = 2.72548               # K, Fixsen 2009
YR = 3.155693e7               # s
KPC = 3.0857e19               # m
M_EARTH = 5.972e24
M_SUN = 1.98892e30

# --- input: IMPORTED, not copied -------------------------------------------
# The mass is computed by calculate_microknot_mass.py and imported here rather
# than restated. A copied constant is a constant that will eventually diverge:
# if the transition temperature or the horizon-mass formula is revised there,
# this script follows automatically instead of quietly using a stale value.
import importlib.util as _ilu
import os as _os

_ROOT = _os.path.dirname(_os.path.abspath(__file__))
_spec = _ilu.spec_from_file_location(
    "microknot_mass", _os.path.join(_ROOT, "calculate_microknot_mass.py"))
_mk = _ilu.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_mk)          # name is not __main__, so main() stays put
except SystemExit:
    pass

_H = _mk.hubble_rate(_mk.T_C)
M_MICRO = _mk.horizon_mass(_H)                       # kg
SIG_M = M_MICRO * 2.0 * _mk.SIG_T_C / _mk.T_C        # sigma_M/M = 2 sigma_T/T
M_OLD = 6.0e24                # superseded, kept for the comparison table
# [CORRIGE 16/09/2026 — C-FINAL-03] L'ancre historique « 0.54 h » ne
# correspond PAS a M_OLD = 6.0e24 kg. Foundation II le dit explicitement
# (correction du 31/08/2026) : « both the 4.3e8 m and 0.54 h figures rested
# on a placeholder mass M = 1e24 kg ». Mettre 0.54 h a l'echelle depuis
# 6.0e24 divisait donc t_E par sqrt(6) = 2.45, d'ou le 2.6 h qui
# contredisait le 6.3 h du texte et le 6.27 h de
# plot_F2_Roman_EMF_prediction.py, lequel calcule la geometrie complete.
# M_PLACEHOLDER est la masse a laquelle l'ancre se rapporte.
M_PLACEHOLDER = 1.0e24        # kg, masse placeholder de l'ancre 0.54 h


LAMBDA_EMF = 36               # Poisson coagulation, a LOWER BOUND (recalibrated 27/08)


def hawking_temperature(M):
    return HBAR * C ** 3 / (8.0 * np.pi * G * M * K_B)


def evaporation_time(M):
    """Page (1976), photons + neutrinos; order of magnitude."""
    return 5120.0 * np.pi * G ** 2 * M ** 3 / (HBAR * C ** 4)


def schwarzschild_radius(M):
    return 2.0 * G * M / C ** 2


def max_angular_momentum(M):
    """Extremal Kerr: J_max = G M^2 / c, i.e. a* = Jc/(GM^2) = 1."""
    return G * M ** 2 / C


def frame_dragging(J, r):
    """
    Lense-Thirring angular velocity, Omega = 2GJ/(c^2 r^3).

    /!\ WEAK-FIELD FORMULA. It is quoted here at r = r_s, i.e. at the very
    edge of its domain of validity, because that is where Foundation II
    quotes it. Taken further in (r < r_s) it returns superluminal speeds,
    which is a failure of the approximation and not a physical statement.
    The exact extremal-Kerr result at the horizon is Omega_H = c/(2 r_s),
    computed below as a cross-check.
    """
    return 2.0 * G * J / (C ** 2 * r ** 3)


def kerr_horizon_omega(M):
    """Exact extremal Kerr: Omega_H = c/(2 r_s). No approximation."""
    return C / (2.0 * schwarzschild_radius(M))


def einstein_radius(M, D_L, D_S):
    return np.sqrt(4.0 * G * M / C ** 2 * (D_S - D_L) / (D_L * D_S))


def main():
    print("=" * 70)
    print("  Micro-Knot observables, derived from M_micro")
    print("=" * 70)
    print(f"\n  M_micro = ({M_MICRO/1e24:.2f} +/- {SIG_M/1e24:.2f}) x 10^24 kg"
          f"   [calculate_microknot_mass.py]")

    # --- Hawking -----------------------------------------------------------
    T_H = hawking_temperature(M_MICRO)
    sig_T = T_H * SIG_M / M_MICRO          # T ~ 1/M
    ratio = T_CMB / T_H
    print("\n" + "-" * 70)
    print("  HAWKING TEMPERATURE")
    print("-" * 70)
    print(f"    T_H = hbar c^3/(8 pi G M k_B) = {1000*T_H:.1f} +/- {1000*sig_T:.1f} mK")
    print(f"    T_CMB / T_H = {ratio:.0f}   ->  {np.log10(ratio):.1f} orders of magnitude")
    print(f"    => T_H is TWO orders below the CMB, not three.")
    print(f"       (the corpus quoted 2.7 mK, which would need "
          f"{HBAR*C**3/(8*np.pi*G*2.7e-3*K_B):.2e} kg)")

    # --- evaporation -------------------------------------------------------
    t_ev = evaporation_time(M_MICRO)
    print("\n" + "-" * 70)
    print("  EVAPORATION TIMESCALE")
    print("-" * 70)
    print(f"    t_ev = 5120 pi G^2 M^3/(hbar c^4) = {t_ev/YR:.2e} yr"
          f"  = 10^{np.log10(t_ev/YR):.0f} yr")
    print(f"    t_ev ~ M^3, so the uncertainty is 3 x that on M: "
          f"{300*SIG_M/M_MICRO:.1f} %")
    print("    => order 1e50 yr, not the 1e83 yr previously quoted.")
    print("       The conclusion is unaffected: 1e50 yr vastly exceeds the")
    print("       age of the universe (1.4e10 yr).")

    # --- geometry ----------------------------------------------------------
    r_s = schwarzschild_radius(M_MICRO)
    print("\n" + "-" * 70)
    print("  GEOMETRY")
    print("-" * 70)
    print(f"    r_s      = {1000*r_s:.2f} mm    (diameter {2000*r_s:.1f} mm)")
    print(f"    M/M_Earth = {M_MICRO/M_EARTH:.3f}")
    print(f"    M/M_Sun   = {M_MICRO/M_SUN:.3e}")
    print(f"    density   = {M_MICRO/((4/3)*np.pi*r_s**3):.2e} kg/m^3")

    # --- rotation ----------------------------------------------------------
    J = max_angular_momentum(M_MICRO)
    om_lt = frame_dragging(J, r_s)
    om_h = kerr_horizon_omega(M_MICRO)
    print("\n" + "-" * 70)
    print("  ROTATION AND FRAME DRAGGING")
    print("-" * 70)
    print(f"    J_max = G M^2/c        = {J:.3e} kg m^2 s^-1   (a* = 1)")
    print(f"    Omega_LT at r_s        = {om_lt:.3e} rad/s")
    print(f"    Omega_H (exact, Kerr)  = {om_h:.3e} rad/s")
    print(f"    agreement              = {om_lt/om_h:.3f}")
    print(f"    v = Omega_LT x r_s     = {om_lt*r_s/C:.3f} c")
    print()
    print("    => the dragging speed at r_s is HALF the speed of light. At the")
    print("       ergosphere it reaches c, which is the definition of that")
    print("       surface: no observer can remain static there.")
    print()
    print("    /!\\ Foundation II quoted Omega_LT ~ 1e22 rad/s. That is a")
    print("        transcription error: the same formula, with the same J,")
    print(f"        returns {om_lt:.1e} rad/s. A value of 1e22 would put the")
    print(f"        dragging speed at {1e22*r_s/C:.1e} c.")

    # --- microlensing ------------------------------------------------------
    D_S, D_L = 8.0 * KPC, 4.0 * KPC        # mid-point geometry, as in F2
    th = einstein_radius(M_MICRO, D_L, D_S)
    th_old = einstein_radius(M_OLD, D_L, D_S)
    print("\n" + "-" * 70)
    print("  MICROLENSING (mid-point geometry, D_L = 4 kpc, D_S = 8 kpc)")
    print("-" * 70)
    print(f"    theta_E     = {th*206264806:.4f} micro-arcsec")
    print(f"    ratio to the superseded mass: {th/th_old:.3f}  (= sqrt(M/M_old))")
    print(f"    t_E ~ sqrt(M): 0.54 h -> {0.54*np.sqrt(M_MICRO/M_PLACEHOLDER):.2f} h (single knot)")
    print(f"    with the Poisson coagulation, M_typ = {LAMBDA_EMF} M_micro:")
    print(f"      t_E^typ = {0.54*np.sqrt(M_MICRO/M_PLACEHOLDER)*np.sqrt(LAMBDA_EMF):.1f} h")

    # --- what dominates the uncertainty ------------------------------------
    print("\n" + "-" * 70)
    print("  WHAT DOMINATES THE UNCERTAINTY ON t_E")
    print("-" * 70)
    print(f"    from M_micro (+/- {100*SIG_M/M_MICRO:.1f} %) : "
          f"{50*SIG_M/M_MICRO:.2f} %   [t_E ~ sqrt(M)]")
    print("    from lambda: quoted as >= 36, a BOUND, not a value:")
    for lam in (36, 50, 100):
        print(f"      lambda = {lam:>3}  ->  t_E = "
              f"{0.54*np.sqrt(M_MICRO/M_PLACEHOLDER)*np.sqrt(lam):.1f} h")
    print("    => lambda dominates by roughly two orders of magnitude.")
    print("       The 1.3% precision on M_micro does NOT make the Roman")
    print("       kill-switch precise to 1.3%.")

    # --- comparison table --------------------------------------------------
    print("\n" + "=" * 70)
    print("  SUPERSEDED VALUES (recorded, not hidden)")
    print("=" * 70)
    print(f"  {'quantity':<22} {'old':>14} {'new':>14} {'factor':>9}")
    rows = [
        ("M_micro [kg]", M_OLD, M_MICRO),
        ("r_s [mm]", 1000*schwarzschild_radius(M_OLD), 1000*r_s),
        ("T_H [mK]", 1000*hawking_temperature(M_OLD), 1000*T_H),
        ("t_ev [yr]", evaporation_time(M_OLD)/YR, t_ev/YR),
        ("M/M_Earth", M_OLD/M_EARTH, M_MICRO/M_EARTH),
    ]
    for name, o, n in rows:
        print(f"  {name:<22} {o:>14.3e} {n:>14.3e} {n/o:>9.3f}")
    print()
    print("  NB (checked 30/08/2026): the corpus previously quoted T_H = 2.7 mK")
    print("      and t_ev > 1e83 yr, which matched NEITHER column -- arithmetic")
    print("      errors independent of the mass revision. VERIFIED FIXED: the")
    print("      current corpus text consistently shows T_H=33 mK, t_evap~1e50 yr")
    print("      (F2, 6 occurrences checked). No outstanding action here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
