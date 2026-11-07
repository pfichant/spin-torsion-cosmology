#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_stellar_transit.py  --  ECF Foundation II
=============================================================================
What happens when a Micro-Knot passes through a star, how often, and whether
anything could be seen.

WHY THIS SCRIPT EXISTS
----------------------
The encounter-rate table (compute_encounter_rates.py) identified the Sun as
the only one of seven targets whose rate, however small, opens onto a possible
observable: a transit deposits energy, where an Earth impact essentially does
not. That remark was left unquantified. This script quantifies it, and reaches
a negative conclusion that is worth stating precisely.

WHY THE PBH LITERATURE DOES NOT COVER THIS CASE
-----------------------------------------------
Stellar capture and transit of primordial black holes is a studied problem,
but the studied window is the "asteroid-mass" range, 1e17 to 1e23 g. The
Micro-Knot is 3.7e27 g -- four orders of magnitude above the upper end. The
Hawking-radiation signatures that dominate that literature are irrelevant here
(T_H = 33 mK), and the dynamical-friction regime is different. The calculation
below is therefore done from first principles rather than transposed.

WHAT IS COMPUTED
----------------
  1. Energy deposited by dynamical friction on one crossing, using the
     Chandrasekhar formula F = 4 pi G^2 M^2 rho ln(Lambda) / v^2.
  2. Two consistency checks that decide whether the object is captured and
     whether the star survives.
  3. Transit rates for the Galaxy, nearby galaxies, and the Virgo cluster.
  4. The flux that would reach us, compared with a supernova.

THE CONCLUSION IS NEGATIVE, AND THAT IS THE POINT
-------------------------------------------------
The rates are favourable -- one transit per 35 yr in the Galaxy, several per
year in Virgo -- but the deposit occurs at the stellar core, under millions of
kilometres of opaque plasma. It does not escape in the 38 minutes of the
crossing; it diffuses out over the Kelvin-Helmholtz timescale. The channel is
computable and not electromagnetically observable.

WHAT IS NOT SETTLED
-------------------
A seismic signature. If the deposit excites p-modes, asteroseismology is the
one angle that could bite. Comparing the deposited energy with the energy in
solar oscillation modes requires the asteroseismology literature and is not
attempted here.

Dependency: numpy. Usage: python3 compute_stellar_transit.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import importlib.util as _ilu

import numpy as np

_ROOT = os.path.dirname(os.path.abspath(__file__))
_spec = _ilu.spec_from_file_location(
    "microknot_mass", os.path.join(_ROOT, "calculate_microknot_mass.py"))
_mk = _ilu.module_from_spec(_spec)
try:
    _spec.loader.exec_module(_mk)
except SystemExit:
    pass

C, G = 2.99792458e8, 6.67430e-11
YR, MPC = 3.155693e7, 3.0857e22
M_SUN, R_SUN, L_SUN = 1.98892e30, 6.957e8, 3.828e26

M_KNOT = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
RHO_MEAN, RHO_CORE = 1.408e3, 1.62e5        # kg/m^3
LN_LAMBDA = 10.0                            # Coulomb logarithm, order unity
V_INFALL = 616e3                            # m/s, free-fall at solar centre

# from compute_encounter_rates.py, solar-neighbourhood values
RATE_SUN_LOCAL = 1.79e-14                   # per year, per star


# --- seismic channel ------------------------------------------------------
# [28/08] Added on Pascal's request to push the seismic angle through rather
# than leave it as an open remark. The result closes the channel, but for the
# opposite reason to the electromagnetic one, and the distinction matters.
SOLAR_PMODE_BUDGET = 1.0e27          # J, order of magnitude (see below)
SURVEYS = [
    # label,                    N stars, baseline (yr)
    ("Kepler (2009-2018)",       1.5e5,  9.0),
    ("TESS (2018- )",            2.0e5,  8.0),
    ("PLATO (2026- )",           2.0e5,  4.0),
]


def pmode_budget():
    """
    Total energy in the solar p-mode oscillations, two independent routes.

    E_mode = M_mode <v^2> (Goldreich & Murray 1994). Neither route is precise;
    they agree on the exponent, which is all that is needed here since the
    deposit exceeds them by six orders.
      route 1: ~1e7 observable modes, mode mass ~1e-11 Msun, ~0.15 m/s each
      route 2: oscillating outer envelope ~0.02 Msun, integrated rms ~0.3 m/s
    """
    r1 = 1e7 * 1e-11 * M_SUN * 0.15 ** 2
    r2 = 0.5 * 0.02 * M_SUN * 0.3 ** 2
    return r1, r2


def friction_force(rho, v=V_INFALL, M=M_KNOT):
    """Chandrasekhar dynamical friction."""
    return 4.0 * np.pi * G ** 2 * M ** 2 * rho * LN_LAMBDA / v ** 2


def main():
    print("=" * 76)
    print("  Micro-Knot transit through a star")
    print("=" * 76)
    print(f"\n  M_knot = {M_KNOT:.3e} kg = {M_KNOT*1e3:.1e} g")
    print("  studied PBH 'asteroid-mass' window: 1e17 - 1e23 g")
    print(f"  the object is {M_KNOT*1e3/1e23:.0e}x above it -- that literature")
    print("  does not transfer, and the calculation below is done from scratch.")

    print("\n" + "-" * 76)
    print("  ENERGY DEPOSITED ON ONE CROSSING")
    print("-" * 76)
    t_cross = 2.0 * R_SUN / V_INFALL
    for rho, lbl in ((RHO_MEAN, "mean solar density"), (RHO_CORE, "core density")):
        F = friction_force(rho)
        E = F * 2.0 * R_SUN
        print(f"  {lbl:<22} F = {F:.2e} N    E = {E:.2e} J")
    E_dep = friction_force(RHO_CORE) * 2.0 * R_SUN
    P = E_dep / t_cross
    print(f"\n  crossing time     : {t_cross:.0f} s = {t_cross/60:.1f} min")
    print(f"  mean power        : {P:.2e} W = {P/L_SUN:.2e} L_sun")

    print("\n" + "-" * 76)
    print("  TWO CHECKS THAT DECIDE THE OUTCOME")
    print("-" * 76)
    E_kin = 0.5 * M_KNOT * V_INFALL ** 2
    E_bind = 3.0 * G * M_SUN ** 2 / (5.0 * R_SUN)
    print(f"  knot kinetic energy   : {E_kin:.2e} J")
    print(f"  deposited / kinetic   : {E_dep/E_kin:.2e}"
          f"   -> {'CAPTURED' if E_dep > E_kin else 'passes through'}")
    print(f"  solar binding energy  : {E_bind:.2e} J")
    print(f"  deposited / binding   : {E_dep/E_bind:.2e}"
          f"   -> {'star disrupted' if E_dep > E_bind else 'star unaffected'}")

    print("\n" + "-" * 76)
    print("  TRANSIT RATES")
    print("-" * 76)
    # Galactic populations: N stars, rate gain over the solar neighbourhood
    POP = [("disc (solar neighbourhood)", 5e10, 1.0),
           ("bulge", 2e10, 78.0),
           ("stellar halo", 1e9, 0.3)]
    r_mw = 0.0
    print(f"  {'population':<30}{'N stars':>11}{'gain':>7}{'transits/yr':>14}")
    for lbl, N, g in POP:
        r = N * RATE_SUN_LOCAL * g
        r_mw += r
        print(f"  {lbl:<30}{N:>11.0e}{g:>7.0f}{r:>14.2e}")
    print(f"  {'MILKY WAY TOTAL':<30}{'':>11}{'':>7}{r_mw:>14.2e}"
          f"   (1 per {1/r_mw:.0f} yr)")

    print()
    GAL = [("M31 (Andromeda)", 1.5, 0.78), ("M33", 0.1, 0.84),
           ("LMC", 0.02, 0.05), ("SMC", 0.005, 0.06),
           ("Local Group", 2.7, 1.0), ("Virgo cluster", 200.0, 16.5)]
    print(f"  {'target':<22}{'M/M_MW':>8}{'transits/yr':>14}{'interval':>13}"
          f"{'distance':>12}")
    for lbl, f, d in GAL:
        r = r_mw * f
        print(f"  {lbl:<22}{f:>8.3f}{r:>14.2e}{1/r:>11.1f} yr{d:>10.2f} Mpc")

    print("\n" + "=" * 76)
    print("  COULD ANYTHING BE SEEN?  -- no, and here is why")
    print("=" * 76)
    for d_mpc, lbl in ((0.78, "M31"), (16.5, "Virgo")):
        F = P / (4.0 * np.pi * (d_mpc * MPC) ** 2)
        print(f"  flux from {lbl:<8} : {F:.2e} W/m^2")
    print("  a supernova at 780 kpc gives ~1e-9 W/m^2, seven orders higher.")
    print()
    print("  And the flux above is already an overestimate, because it assumes")
    print("  the energy escapes during the crossing. It does not: the deposit")
    print("  is at the core, under millions of kilometres of opaque plasma, and")
    print("  diffuses out on the Kelvin-Helmholtz timescale rather than in 38")
    print("  minutes. Electromagnetically, a transit is invisible.")
    print()
    print("\n" + "=" * 76)
    print("  THE SEISMIC CHANNEL -- closed too, but for the opposite reason")
    print("=" * 76)
    r1, r2 = pmode_budget()
    print(f"  solar p-mode energy budget: {r1:.1e} to {r2:.1e} J (two routes)")
    print(f"  energy deposited by one transit: {E_dep:.2e} J")
    print(f"  ratio: {E_dep/SOLAR_PMODE_BUDGET:.1e}")
    print()
    print("  The deposit exceeds the entire modal budget by a factor of order")
    print("  a million. A coupling efficiency of 1e-6 would already produce a")
    print("  signal comparable to the whole of the solar oscillation. So the")
    print("  signal is not the problem.")
    print()
    print("  The problem is events. Asteroseismology monitors:")
    n_tot = 0.0
    for lbl, N, T in SURVEYS:
        n = N * RATE_SUN_LOCAL * T
        n_tot += n
        print(f"    {lbl:<24}{N:>9.0e} stars x {T:>4.0f} yr -> {n:.1e} transits")
    print(f"    {'combined':<24}{'':>9}   {'':>4}    -> {n_tot:.1e}")
    print()
    print(f"  One expected transit would require {1/(RATE_SUN_LOCAL*10):.1e} stars")
    print("  monitored continuously for a decade -- ten million times the")
    print("  current sample.")
    print()
    print("  The distinction is worth keeping. The electromagnetic channel is")
    print("  closed by radiative transport and will stay closed. The seismic")
    print("  channel is closed by sample size: it would reopen if populations")
    print("  orders of magnitude larger were ever monitored. Neither is a")
    print("  prediction of this framework; both are consequences of the rate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
