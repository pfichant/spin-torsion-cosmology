#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_string_tension_1D.py  --  ECF Foundation II
=============================================================================
The tension of the 1D Torsion Strings, and what follows from it.

WHY THIS SCRIPT EXISTS
----------------------
Foundation II stated two things that cannot both hold:

  (i)  "their tension is set by the electroweak VEV, not a GUT-scale VEV"
  (ii) "yielding G mu / c^2 ~ 1e-12 to 1e-11"

The relation between them is direct: G mu / c^2 = (eta / M_Pl)^2. With the
electroweak VEV, eta = 246.22 GeV, that gives 4.1e-34. To reach 1e-11 would
require eta ~ 4e13 GeV -- eleven orders above the electroweak scale and three
below the GUT scale, an energy that belongs to nothing in this framework.

[27/08/2026] The electroweak origin is kept and the value corrected, on the
grounds that a single transition producing every defect is the architecture of
the model, while 1e-11 was a number that did not follow from the formula
printed above it. The consequence is stated rather than hidden: at this
tension the strings are not detectable, and the Faraday-rotation kill-switches
that rested on 1e-11 do not survive.

A further correction: the paper used eta_EW ~ 150 GeV. That is not the VEV --
246.22 GeV (PDG) -- and looks like a confusion with the transition
temperature T_c = 159 GeV, which is a different quantity.

WHAT IS AND IS NOT SETTLED HERE
-------------------------------
IS:     mu_1D and everything algebraically downstream of it, GIVEN that the
        1D sector exists.
IS NOT: whether the strings could acquire tension from some later mechanism.
        The script computes the electroweak-VEV value, which is what the
        paper claims their origin to be; a different origin would need its
        own derivation, not a different number in the same sentence.

UPDATE (30/08/2026) -- a more fundamental gap, found after this script was
written: the 1D sector's very EXISTENCE is an open problem, not just its
tension. S^mu (the axial torsion field) is real and carries no internal
phase, so it cannot by itself supply the complex order parameter a
quantised string (pi_1 != 0) requires. Two candidate completions were
tried and failed (a trace-vector companion, a residual anisotropy seed);
a semi-topological candidate remains structurally possible but its
stability is dynamical, not topological, and depends on the unresolved
mass m_T (PO-F2-6). Retained as PO-F2-8, an explicitly open research
programme -- see F2, Sec. "1D Defects: Torsion Strings", opening warning
box. Everything this script computes is therefore conditional: "IF a 1D
sector of this kind exists, ITS tension would be...", not an established
result on its own.

Dependency: numpy. Usage: python3 compute_string_tension_1D.py
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

C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054572e-34
GEV_J = 1.602177e-10
M_PL_GEV = 1.220890e19

ETA_EW = 246.22          # GeV, electroweak VEV (PDG); NOT T_c = 159 GeV
CMB_BOUND = 1.0e-7       # G mu/c^2, current CMB limit on cosmic strings
RAD_TO_UAS = 206264.806 * 1e6


def mu_from_vev(eta_gev):
    """Linear mass density of a global string: mu ~ eta^2 (natural units)."""
    return (eta_gev * GEV_J) ** 2 / (HBAR * C ** 3)


def dimensionless_tension(eta_gev):
    """G mu / c^2 = (eta / M_Pl)^2, exact in natural units."""
    return (eta_gev / M_PL_GEV) ** 2


def main():
    print("=" * 72)
    print("  1D Torsion Strings: tension from the electroweak VEV")
    print("=" * 72)

    mu = mu_from_vev(ETA_EW)
    gmu = G * mu / C ** 2
    gmu_exact = dimensionless_tension(ETA_EW)

    print(f"\n  INPUT")
    print(f"    eta_EW = {ETA_EW} GeV   (electroweak VEV, PDG)")
    print(f"\n  DERIVED")
    print(f"    mu_1D      = {mu:.4e} kg/m")
    print(f"    G mu / c^2 = {gmu:.4e}")

    # --- cross-check: two routes to the same dimensionless number ---------
    print(f"\n  CONSISTENCY CHECK")
    print(f"    via SI units          : {gmu:.4e}")
    print(f"    via (eta/M_Pl)^2      : {gmu_exact:.4e}")
    ok = abs(gmu - gmu_exact) / gmu_exact < 0.02
    print(f"    -> {'agree' if ok else 'MISMATCH'} to {100*abs(gmu-gmu_exact)/gmu_exact:.1f} %")
    if not ok:
        print("    /!\\ check failed -- do not use these numbers")
        return 1

    # --- observables -------------------------------------------------------
    delta = 8.0 * np.pi * gmu
    v_s = 1e-3 * C
    dv = 4.0 * np.pi * gmu * v_s
    print(f"\n  OBSERVABLES")
    print(f"    conical deficit angle  = {delta:.2e} rad = {delta*RAD_TO_UAS:.2e} uas")
    print(f"    velocity kick (v_s = 0.001 c) = {dv:.2e} m/s")

    print(f"\n  AGAINST THE CMB BOUND")
    print(f"    CMB limit on cosmic strings : G mu/c^2 < {CMB_BOUND:.0e}")
    print(f"    ECF value is {CMB_BOUND/gmu:.1e} times below it.")
    print(f"    => compatible, and undetectable. Both follow from the same")
    print(f"       fact: the electroweak scale is low.")

    # --- what the superseded value would have required ---------------------
    print("\n" + "-" * 72)
    print("  SUPERSEDED VALUE (recorded, not hidden)")
    print("-" * 72)
    for target in (1e-11, 1e-12):
        eta_req = M_PL_GEV * np.sqrt(target)
        print(f"    G mu/c^2 = {target:.0e} would require eta = {eta_req:.2e} GeV")
    print(f"    i.e. {M_PL_GEV*np.sqrt(1e-11)/ETA_EW:.1e} times the electroweak VEV --")
    print(f"    an energy that corresponds to no scale in this framework.")
    print(f"\n    The paper also used eta_EW ~ 150 GeV, which is not the VEV")
    print(f"    ({ETA_EW} GeV) and looks like a confusion with T_c = 159 GeV.")

    print("\n" + "=" * 72)
    print("  CONSEQUENCE, STATED PLAINLY")
    print("=" * 72)
    print("  At G mu/c^2 = 4e-34 the strings produce no observable Faraday")
    print("  rotation, no lensing signature, and no CMB imprint. The")
    print("  kill-switches that rested on 1e-11 do not survive this")
    print("  correction. What survives is the chiral torsion charge and the")
    print("  absence of a B-mode pattern -- neither of which depends on the")
    print("  tension.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
