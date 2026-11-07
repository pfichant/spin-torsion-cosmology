#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_selfinteraction_bound.py  --  ECF Foundation II
=============================================================================
The self-interaction cross-section of the ECF dark sector, against the
merging-cluster bound.

WHY THIS SCRIPT EXISTS
----------------------
Foundation II states that the framework is "qualitatively consistent" with the
Bullet Cluster. That is true but weak: the constraint is quantitative, it is
the single most-cited empirical bound on dark-matter self-interaction, and the
ECF happens to satisfy it by a very wide margin. Stating a number costs one
calculation and turns a concession into a result.

WHAT IS COMPUTED
----------------
Micro-Knots interact gravitationally and nothing else: they carry no gauge
charge, and their topological charge is conserved rather than exchanged. Their
geometric cross-section is therefore bounded above by the horizon area,

    sigma_geo = pi r_s^2,     r_s = 2GM/c^2

which is the largest area a body of that mass can present. The observational
constraint is quoted as sigma/m, so that is what is compared.

This is an UPPER BOUND, and deliberately a generous one: a genuine encounter
cross-section would be smaller still, since two knots must pass within r_s to
interact at all, and gravitational scattering at cluster velocities deflects
without merging. Quoting the bound rather than the true value keeps the
argument conservative.

WHAT IT DOES NOT SHOW
---------------------
  * It does not prove the knots are collisionless -- that follows from the
    absence of non-gravitational couplings, which is an assumption of the
    framework, not a result of this script.
  * Macro-Knots (1e5 Msun) are the more constrained population, not the
    less: for a geometric cross-section sigma/m = pi r_s^2/M scales as M, so
    the ratio grows with mass. Both are computed below, and both pass, but
    quoting only the Micro-Knot figure would understate the constraint.

Dependency: numpy. Usage: python3 compute_selfinteraction_bound.py
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
M_SUN = 1.98892e30
M_MICRO = _mk.horizon_mass(_mk.hubble_rate(_mk.T_C))
M_MACRO = 1.0e5 * M_SUN

# observational bounds, sigma/m in cm^2/g
BOUNDS = {
    "Bullet Cluster (Randall+2008)": 1.25,
    "cluster ellipticity (Peter+2013)": 1.0,
    "Abell 3827 (Massey+2018)": 1.5,
}


def sigma_over_m(M):
    """Geometric upper bound: pi r_s^2 / M, converted to cm^2/g."""
    r_s = 2.0 * G * M / C ** 2
    sig_si = np.pi * r_s ** 2          # m^2
    return sig_si / M * 10.0           # m^2/kg -> cm^2/g (1e4 cm^2 / 1e3 g)


def main():
    print("=" * 70)
    print("  ECF self-interaction vs merging-cluster bounds")
    print("=" * 70)

    for label, M in (("Micro-Knot", M_MICRO), ("Macro-Knot (1e5 Msun)", M_MACRO)):
        r_s = 2.0 * G * M / C ** 2
        som = sigma_over_m(M)
        print(f"\n  {label}")
        print(f"    M      = {M:.3e} kg")
        print(f"    r_s    = {r_s:.3e} m")
        print(f"    sigma  = {np.pi*r_s**2:.3e} m^2   (geometric, pi r_s^2)")
        print(f"    sigma/m = {som:.3e} cm^2/g")

    som = sigma_over_m(M_MICRO)
    print("\n" + "-" * 70)
    print("  AGAINST THE OBSERVATIONAL BOUNDS")
    print("-" * 70)
    print(f"  {'bound':<36}{'limit':>10}{'margin':>16}")
    for label, lim in BOUNDS.items():
        print(f"  {label:<36}{lim:>10.2f}{lim/som:>16.1e}")

    print("\n" + "=" * 70)
    print("  READING")
    print("=" * 70)
    print(f"  The ECF value is {BOUNDS['Bullet Cluster (Randall+2008)']/som:.0e} times")
    print("  below the tightest bound. This is not a marginal pass: the")
    print("  framework has no non-gravitational coupling to violate, so the")
    print("  cross-section is bounded by geometry alone.")
    print()
    print("  Note the sign of the argument. A particle candidate must be TUNED")
    print("  to be collisionless. A topological defect is collisionless because")
    print("  it has nothing to collide with -- which is a structural statement,")
    print("  and structurally weaker to falsify.")
    print()
    print("  Macro-Knots are the harder case, and worth stating plainly:")
    print("  for a geometric cross-section sigma/m = pi r_s^2/M grows LINEARLY")
    print("  with M, so the heavier population is the MORE constrained one.")
    print(f"  At 1e5 Msun: {sigma_over_m(M_MACRO):.1e} cm^2/g, still")
    print(f"  {BOUNDS['Bullet Cluster (Randall+2008)']/sigma_over_m(M_MACRO):.0e} times below the bound, but by a smaller margin.")
    print("  Quoting only the Micro-Knot figure would understate the constraint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
