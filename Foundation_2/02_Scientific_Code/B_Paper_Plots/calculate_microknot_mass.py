#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calculate_microknot_mass.py  --  ECF Foundation II
=============================================================================
The Micro-Knot mass, from the electroweak horizon mass.

WHAT THIS SCRIPT COMPUTES
-------------------------
The lower cutoff of the Kibble-Zurek mass function is the horizon mass at the
electroweak transition. The standard relation (Carr, Kohri, Sendouda &
Yokoyama, Rept. Prog. Phys. 84, 116902) is

    M_H = (4 pi / 3) rho (c/H)^3 = c^3 / (2 G H),     rho = 3 H^2 / (8 pi G)

evaluated at the transition temperature T_c = 159 +/- 1 GeV (lattice
determination, D'Onofrio, Rummukainen & Tranberg, PRL 113, 141602).

[27/08/2026] CORRECTION OF RECORD -- two errors are fixed here, and recorded
rather than silently overwritten, because the value they produced (6.06e24 kg)
propagated to some thirty places in the corpus:

  (1) The factor 1/2 was missing. The script computed M = c^3 t / G. In a
      radiation era H = 1/(2t), so the horizon mass is c^3 t / (2G): the old
      expression overestimated by a factor 2.

  (2) The freeze-out time was hard-coded as t = 1.5e-11 s with no source.
      That value corresponds to T = 125.0 GeV -- neither the transition
      temperature (159 GeV) nor the sphaleron freeze-out (131.7 GeV). It was
      a choice, not a calculation. The temperature is now the input, and the
      time follows from it.

WHY T_c AND NOT A LATER FREEZE-OUT TEMPERATURE
----------------------------------------------
Kibble-Zurek defects form at the KZ freeze-out, not at the transition, and in
a laboratory quench the two differ appreciably. In cosmology they do not: the
freeze-out condition gives eps_hat = (tau_0/tau_Q)^(1/(1+nu z)) with
tau_0 ~ 1/T_c ~ 4e-27 s and tau_Q ~ 1/H ~ 1.9e-11 s -- a ratio of some fifteen
orders of magnitude. Whatever the critical exponents, eps_hat < 1e-5, so the
freeze-out occurs at T_c to better than one part in 10^5. The distinction is
real and it collapses here, for a reason that can be stated.

The sphaleron freeze-out at T_* = 131.7 GeV is a different event again: it
freezes the baryon asymmetry, not the defect network, and plays no role here.

WHAT THIS DOES NOT ESTABLISH
----------------------------
  * The Standard Model with m_H = 125 GeV has NO true phase transition at the
    electroweak scale -- the change is a crossover. Kibble-Zurek is formulated
    for a transition with symmetry breaking; the extension used in Foundation
    II relies on the torsional sector supplying the order parameter. That is
    an assumption of the framework, not a result of this script.
  * M_micro is the LOWER CUTOFF of a mass function, not a monodisperse mass.
    Observable quantities sample the distribution.
  * The 1.3% precision here does NOT make the Roman kill-switch precise to
    1.3%: t_E ~ sqrt(lambda M), and lambda is quoted as a bound (>= 26), which
    dominates the uncertainty by two orders of magnitude.

Usage: python3 calculate_microknot_mass.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

# --- constants -------------------------------------------------------------
C = 299792458.0            # m/s
G = 6.67430e-11            # m^3 kg^-1 s^-2
HBAR = 1.054572e-34        # J s
GEV_J = 1.602177e-10       # J per GeV
M_PL_GEV = 1.220890e19     # Planck mass, GeV

M_EARTH = 5.972e24
M_JUPITER = 1.898e27
M_SUN = 1.989e30

# --- inputs, each with a source --------------------------------------------
T_C = 159.0                # GeV, D'Onofrio+2014 (lattice)
SIG_T_C = 1.0              # GeV
G_STAR = 106.75            # SM relativistic dof above the EW scale


def hubble_rate(T_gev, gstar=G_STAR):
    """H(T) in the radiation era: H = 1.66 sqrt(g*) T^2 / M_Pl, in s^-1."""
    T = T_gev * GEV_J
    return 1.66 * np.sqrt(gstar) * T ** 2 / (M_PL_GEV * GEV_J) / HBAR


def horizon_mass(H):
    """M_H = (4 pi/3) rho (c/H)^3 = c^3/(2 G H), in kg."""
    return C ** 3 / (2.0 * G * H)


def main():
    print("=" * 68)
    print("  ECF Micro-Knot mass -- electroweak horizon mass")
    print("=" * 68)

    H = hubble_rate(T_C)
    M = horizon_mass(H)
    r_s = 2.0 * G * M / C ** 2
    # M ~ 1/H ~ 1/T^2  =>  sigma_M/M = 2 sigma_T/T
    sig_M = M * 2.0 * SIG_T_C / T_C

    print("\n  INPUTS")
    print(f"    T_c        = {T_C} +/- {SIG_T_C} GeV   (lattice, D'Onofrio+2014)")
    print(f"    g_*        = {G_STAR}              (SM dof above the EW scale)")
    print("\n  DERIVED")
    print(f"    H(T_c)     = {H:.4e} s^-1")
    print(f"    t = 1/(2H) = {1.0/(2*H):.4e} s")
    print(f"    M_micro    = ({M/1e24:.2f} +/- {sig_M/1e24:.2f}) x 10^24 kg"
          f"   ({100*sig_M/M:.1f} %)")
    print(f"    r_s        = {1000*r_s:.2f} mm   (diameter {2000*r_s:.1f} mm)")

    # --- consistency check: the signature of a correct horizon mass --------
    print("\n  CONSISTENCY CHECK")
    print(f"    r_s(M_H)   = {r_s:.9f} m")
    print(f"    c/H        = {C/H:.9f} m")
    ok = abs(r_s - C / H) / (C / H) < 1e-12
    print(f"    -> {'IDENTICAL' if ok else 'MISMATCH'}: the Schwarzschild radius of the")
    print("       horizon mass IS the horizon size. This is exact for")
    print("       M_H = c^3/(2GH) and fails for any other prefactor.")
    if not ok:
        print("    /!\\ check failed -- do not use these numbers")
        return 1

    print("\n  PHYSICAL PICTURE")
    print(f"    {M/M_EARTH:.2f} Earth masses, in a ball {2000*r_s:.1f} mm across.")
    print(f"    mean density = {M/((4/3)*np.pi*r_s**3):.2e} kg/m^3")
    print("    (an atomic nucleus is ~2.3e17 kg/m^3)")

    print("\n  RATIOS")
    print(f"    / Earth    = {M/M_EARTH:.3f}")
    print(f"    / Jupiter  = {M/M_JUPITER:.3e}")
    print(f"    / Sun      = {M/M_SUN:.3e}")

    # --- what the old value was, and why it differed -----------------------
    print("\n" + "-" * 68)
    print("  SUPERSEDED VALUE (recorded, not hidden)")
    print("-" * 68)
    old = C ** 3 * 1.5e-11 / G
    print(f"    previous: M = c^3 t / G with t = 1.5e-11 s  ->  {old:.3e} kg")
    print(f"    factor against the value above: {old/M:.2f}")
    print("    two causes: the missing 1/2, and t corresponding to T = 125 GeV.")

    print("\n" + "=" * 68)
    print("  SCOPE")
    print("=" * 68)
    print("  This fixes the LOWER CUTOFF of the Kibble-Zurek mass function.")
    print("  It is not a monodisperse mass: observable quantities sample the")
    print("  distribution, and the Roman event duration goes as sqrt(lambda M)")
    print("  where lambda >= 26 is a bound, not a value. The 1.3% precision")
    print("  quoted here does not transfer to the kill-switch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
