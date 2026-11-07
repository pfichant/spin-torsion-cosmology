#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_encounter_rates.py  --  ECF Foundation II
=============================================================================
Encounter rates between Micro-Knots and the objects they might meet.

WHY THIS SCRIPT EXISTS
----------------------
A framework proposing ~1e18 compact objects per galactic halo has to say what
they run into. The question is not exotic: it is the first thing any reader
asks, and the first consistency check any referee performs. Foundation II
mentions "planetary mass" twenty-three times without once computing an
encounter with a planet.

The rates below span forty orders of magnitude, which is exactly why they
belong in one table rather than scattered through the text.

METHOD
------
For a stationary target of radius R in a sea of knots of number density n and
relative velocity v, the rate is

    Gamma = n * sigma * v,    sigma = pi R^2 (1 + v_esc^2 / v^2)

The second factor is gravitational focusing: a massive target pulls knots onto
itself, and for the Sun it dominates. Knot-knot encounters use the geometric
cross-section of the horizon, with focusing computed from the knot's own
escape velocity.

WHAT IS ASSUMED, AND WHERE IT BREAKS
------------------------------------
  * Local dark-matter density 0.4 GeV/cm^3 and dispersion 220 km/s. Both are
    solar-neighbourhood values; rates in a galactic centre or in a dwarf
    would differ by orders of magnitude.
  * All the dark matter is in Micro-Knots. If Macro-Knots hold a fraction of
    the mass, n falls proportionally and every rate falls with it.
  * Targets are treated as static spheres. For gas clouds this is crude: the
    cloud is diffuse, a knot passes through without depositing much, and the
    "encounter" is not a collision in any useful sense. The number is given
    for completeness and should not be read as a physical event rate.

WHAT THE RATES DO NOT SAY
-------------------------
An encounter is not an observable. Passing through the Sun deposits energy;
whether that energy is detectable is a separate calculation, not attempted
here. The table bounds how often something could happen, not what it looks
like.

Dependency: numpy. Usage: python3 compute_encounter_rates.py
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
YR = 3.155693e7
M_SUN, R_SUN = 1.98892e30, 6.957e8
M_EARTH, R_EARTH = 5.972e24, 6.371e6

M_KNOT = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
R_KNOT = 2.0 * G * M_KNOT / C ** 2

# solar-neighbourhood values
RHO_DM = 0.4e9 * 1.602176e-19 / C ** 2 / 1e-6      # 0.4 GeV/cm^3 -> kg/m^3
V_REL = 220e3                                       # m/s
N_KNOT = RHO_DM / M_KNOT                            # m^-3

AGE_EARTH = 4.5e9
AGE_UNIVERSE = 1.38e10


def rate(R, M_target, n=N_KNOT, v=V_REL):
    """
    Gamma = n sigma v, with Newtonian gravitational focusing.

    /!\ The focusing factor (1 + v_esc^2/v^2) is a weak-field result. For a
    Micro-Knot target v_esc = c by construction -- the escape velocity at a
    Schwarzschild radius is the speed of light -- so the formula is quoted
    there at the edge of its domain and the knot-knot rate should be read as
    an order of magnitude, not a number. The same caveat applies, less
    severely, to the neutron star (v_esc = 0.59 c).
    """
    v_esc2 = 2.0 * G * M_target / R if R > 0 else 0.0
    sigma = np.pi * R ** 2 * (1.0 + v_esc2 / v ** 2)
    return n * sigma * v, sigma, np.sqrt(v_esc2)


# --- environmental dependence ---------------------------------------------
# [28/08] Added on Pascal's remark: the rate is far higher in a galactic
# bulge, where the dark-matter density is some fifty times the local value.
# The dependence is not on density alone. Gamma = n sigma v, and the focusing
# factor is (1 + v_esc^2/v^2), so a LOWER dispersion raises sigma while
# lowering the flux. For a massive target the focusing term dominates and
# slower environments win; for a small one the two nearly cancel.
ENVIRONMENTS = {
    # label                        rho [GeV/cm^3]   v [km/s]
    "solar neighbourhood (8 kpc)":       (0.4,        220.0),
    "galactic bulge (~1 kpc)":           (20.0,       130.0),
    "galactic centre (100 pc)":          (200.0,      100.0),
    "dwarf spheroidal":                  (5.0,         30.0),
}


def rate_in(R, M_target, rho_gev, v_kms):
    """Rate for a given environment, returned per year."""
    rho = rho_gev * 1e9 * 1.602176e-19 / C ** 2 / 1e-6
    n = rho / M_KNOT
    v = v_kms * 1e3
    g, _, _ = rate(R, M_target, n=n, v=v)
    return g * YR


# --- compact-object encounters --------------------------------------------
# [28/08] The Knot-Star channel of Appendix (app:knot_star) describes three
# sub-regimes by impact parameter, but gives no rate: the upstream link was
# missing, and a referee would ask for it. Computed here.
COMPACT = [
    # label,                 R (m),   M (Msun),  N in the Galaxy
    ("neutron star",         1.2e4,   1.4,       1e9),
    ("white dwarf",          7.0e6,   0.6,       1e10),
    ("stellar-mass BH",      3.0e4,   10.0,      1e8),
]


def compact_rates():
    """Encounter rate per object and summed over the Galaxy, per year."""
    out, total = [], 0.0
    for lbl, R, Mt, N in COMPACT:
        g, _, _ = rate(R, Mt * M_SUN)
        per_yr = g * YR
        out.append((lbl, N, per_yr, per_yr * N))
        total += per_yr * N
    return out, total


def fmt_time(per_year):
    if per_year <= 0:
        return "never"
    t = 1.0 / per_year
    return f"1 per {t:.1e} yr"


def main():
    print("=" * 78)
    print("  Micro-Knot encounter rates")
    print("=" * 78)
    print(f"\n  M_knot   = {M_KNOT:.3e} kg      r_s = {1000*R_KNOT:.2f} mm")
    print(f"  rho_DM   = {RHO_DM:.2e} kg/m^3   (0.4 GeV/cm^3, solar neighbourhood)")
    print(f"  n_knot   = {N_KNOT:.2e} m^-3")
    print(f"  v_rel    = {V_REL/1e3:.0f} km/s")

    TARGETS = [
        ("Earth", R_EARTH, M_EARTH),
        ("Jupiter", 6.9911e7, 1.898e27),
        ("Sun", R_SUN, M_SUN),
        ("white dwarf", 7.0e6, 0.6 * M_SUN),
        ("neutron star", 1.2e4, 1.4 * M_SUN),
        ("another Micro-Knot", R_KNOT, M_KNOT),
    ]

    print("\n" + "-" * 78)
    print(f"  {'target':<22}{'sigma [m^2]':>14}{'v_esc [km/s]':>14}"
          f"{'rate [/yr]':>14}{'interval':>16}")
    print("-" * 78)
    rows = []
    for name, R, M in TARGETS:
        g, sig, vesc = rate(R, M)
        per_yr = g * YR
        rows.append((name, per_yr))
        print(f"  {name:<22}{sig:>14.2e}{vesc/1e3:>14.1f}"
              f"{per_yr:>14.2e}{fmt_time(per_yr):>16}")

    # diffuse gas: a knot crosses constantly, but deposits almost nothing
    n_gas = 1e6                       # m^-3, typical molecular cloud
    L_cloud = 10 * 3.0857e16          # 10 pc
    t_cross = L_cloud / V_REL
    print(f"\n  {'molecular cloud':<22}{'(diffuse)':>14}{'--':>14}"
          f"{'--':>14}{'crossing: ' + f'{t_cross/YR:.0f} yr':>16}")
    print("    a knot crosses a 10 pc cloud in ~1e4 yr; there is no collision")
    print("    in any useful sense, only a slow gravitational perturbation.")

    print("\n" + "-" * 78)
    print("  OVER RELEVANT TIMESPANS")
    print("-" * 78)
    for name, per_yr in rows:
        n_earth = per_yr * AGE_EARTH
        n_univ = per_yr * AGE_UNIVERSE
        print(f"  {name:<22} since Earth formed: {n_earth:>10.2e}"
              f"    over a Hubble time: {n_univ:>10.2e}")

    print("\n" + "-" * 78)
    print("  ENVIRONMENTAL DEPENDENCE  (Sun as target)")
    print("-" * 78)
    print(f"  {'environment':<32}{'rho':>10}{'v':>10}{'rate [/yr]':>14}{'vs local':>12}")
    ref = None
    for label, (rho_g, v_k) in ENVIRONMENTS.items():
        r = rate_in(R_SUN, M_SUN, rho_g, v_k)
        if ref is None:
            ref = r
        print(f"  {label:<32}{rho_g:>10.1f}{v_k:>10.0f}{r:>14.2e}{r/ref:>12.0f}x")
    print()
    print("    The gain is not the density ratio alone. A bulge is 50x denser")
    print("    but also slower: slower means less flux (Gamma ~ v) yet stronger")
    print("    focusing (sigma ~ 1 + v_esc^2/v^2). For the Sun the two combine")
    print("    to 78x -- more than the naive n*v scaling of 30x, less than the")
    print("    density ratio of 50x times the focusing gain.")
    print()
    print("    The dwarf spheroidal makes the point: only 12x denser than the")
    print("    solar neighbourhood, but its 30 km/s dispersion focuses so")
    print("    strongly that it matches the bulge. For a massive target,")
    print("    velocity dispersion matters as much as density.")
    print()
    print("    For the Earth the effect is different: its escape velocity is")
    print("    11 km/s, focusing is negligible, and the gain tracks n*v.")
    print()
    print(f"    Earth in a bulge:  {rate_in(R_EARTH, M_EARTH, 20.0, 130.0):.2e} /yr"
          f"   ({rate_in(R_EARTH, M_EARTH, 20.0, 130.0)/rate_in(R_EARTH, M_EARTH, 0.4, 220.0):.0f}x local)")

    print("\n" + "-" * 78)
    print("  KNOT-STAR: encounters with compact objects")
    print("-" * 78)
    rows_c, tot_c = compact_rates()
    print(f"  {'object':<22}{'N in Galaxy':>13}{'per object/yr':>16}{'Galaxy/yr':>14}")
    for lbl, N, per, gal in rows_c:
        print(f"  {lbl:<22}{N:>13.0e}{per:>16.2e}{gal:>14.2e}")
    print(f"  {'TOTAL':<22}{'':>13}{'':>16}{tot_c:>14.2e}")
    print()
    print(f"    One encounter per {1/tot_c:.0e} yr in the Galaxy, so about")
    print(f"    {tot_c*1e10:.0e} events over its lifetime. White dwarfs dominate:")
    print("    their radius is 580x that of a neutron star, and geometry beats")
    print("    the stronger focusing of the denser object.")
    print()
    print("    This is the upstream rate the Knot-Star appendix did not state.")
    print("    It is small but not vanishing, which is what makes the channel")
    print("    worth describing at all.")

    print("\n" + "=" * 78)
    print("  READING")
    print("=" * 78)
    earth = dict(rows)["Earth"]
    sun = dict(rows)["Sun"]
    knot = dict(rows)["another Micro-Knot"]
    print(f"  Earth: {earth*AGE_EARTH:.1e} impacts expected over 4.5 Gyr.")
    print("  A non-observation that is expected, not a constraint.")
    print()
    print(f"  Sun: {sun/earth:.0f}x the terrestrial rate, from radius and")
    print(f"  focusing together -- still {fmt_time(sun)}, so also unobserved,")
    print("  but this is the channel worth computing properly, since a")
    print("  transit deposits energy where it could in principle be seen.")
    print()
    print("  /!\\ The knot-knot and neutron-star rows use Newtonian focusing")
    print("      where v_esc reaches c (knot) and 0.59 c (neutron star). Read")
    print("      them as orders of magnitude; a relativistic capture")
    print("      cross-section would differ by a factor of a few.")
    print()
    print(f"  Knot-knot: {fmt_time(knot)} per knot. Multiplied by ~1e18 knots")
    print(f"  in a halo this gives ~{knot*1e18:.0e} per year per galaxy, which")
    print("  is why coagulation is treated as a network process and not as a")
    print("  two-body problem.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
