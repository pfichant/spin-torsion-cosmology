#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ecf_timeline.py  --  ECF Foundation II
=============================================================================
The ECF timeline, rebuilt from standard cosmology alone.

WHY THIS SCRIPT EXISTS
----------------------
Foundation II quotes epochs, redshifts and collision rates that were found on
27/08/2026 to be mutually inconsistent:

  * z_EW ~ 1.5e11 is quoted for the electroweak crystallisation, but the
    electroweak transition (T_c = 159 GeV) sits at z ~ 7e14. The quoted value
    corresponds to T ~ 35 MeV -- neither electroweak, nor QCD, nor the Great
    Annihilation.
  * The two collision rates quoted, Gamma(1.5e11) = 1e-16 and Gamma(1e12) =
    1e-4, differ by 1e12 where the stated scaling Gamma ~ (1+z)^{3/2} predicts
    a factor 17.
  * "1 encounter every ~300 s" is stated for Gamma = 1e-16 s^-1, whose inverse
    is 1e16 s -- three hundred million years, not three hundred seconds.
  * "1e4 collisions per second" is stated for Gamma = 1e-4 s^-1, which is one
    collision every 1e4 s.

A correction of 17/07/2026 had already relabelled the epochs in the Jeans-mass
section, having found the same class of error there. It did not reach this
section: four occurrences survived.

Rather than patch the numbers one by one, this script rebuilds the timeline
from standard cosmology and takes NOTHING from the corpus. The corpus values
are then compared against it, at the end, so that discrepancies are visible
rather than assumed away.

WHAT IS ASSUMED
---------------
Standard radiation-era cosmology: T ~ 1/a with entropy corrections through
g_*s, H = 1.66 sqrt(g_*) T^2 / M_Pl, and t = 1/(2H). Nothing else. In
particular no ECF-specific physics enters the timeline itself -- the stiff
spin fluid modifies H at very early times, and where that matters it is
stated rather than folded in silently.

Dependency: numpy. Usage: python3 build_ecf_timeline.py
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
HBAR = 1.054572e-34
K_B = 1.380649e-23
GEV_J = 1.602177e-10
M_PL_GEV = 1.220890e19
T_CMB = 2.72548               # K
YR = 3.155693e7               # s
C = 2.99792458e8
G_NEWTON = 6.67430e-11
M_SUN = 1.98892e30

# g_*s today, for the entropy-conserving redshift relation
GS_TODAY = 3.938


def hubble(T_gev, gstar):
    """H(T) in the radiation era, s^-1."""
    return 1.66 * np.sqrt(gstar) * (T_gev * GEV_J) ** 2 / (M_PL_GEV * GEV_J) / HBAR


def redshift(T_gev, gs):
    """
    1+z from entropy conservation: g_*s T^3 a^3 = const, so
    (1+z) = (T/T_0) (g_*s/g_*s,0)^{1/3}.
    Ignoring the g_*s factor -- as a naive T/T_0 does -- overstates z by up to
    a factor ~3 at high temperature.
    """
    T_K = T_gev * GEV_J / K_B
    return (T_K / T_CMB) * (gs / GS_TODAY) ** (1.0 / 3.0)


def horizon_mass(H):
    return C ** 3 / (2.0 * G_NEWTON * H)


# --- the epochs, each with its source --------------------------------------
EPOCHS = [
    # (label, T [GeV], g_*, g_*s, source)
    ("Electroweak transition", 159.0, 106.75, 106.75,
     "lattice, D'Onofrio+2014 (T_c = 159 +/- 1 GeV)"),
    ("Sphaleron freeze-out", 131.7, 106.75, 106.75,
     "lattice, D'Onofrio+2014 (T_* = 131.7 +/- 2.3 GeV)"),
    ("QCD / QGP-hadron", 0.155, 47.5, 47.5,
     "lattice, Bazavov+2014 (T_c = 155 +/- 9 MeV)"),
    # NB: "the Great Annihilation" names a process, not an instant. F2 works
    # throughout with the WINDOW T ~ 0.16--1.6 MeV (z_t in [6.9e8, 6.9e9]),
    # yielding M_K ~ 1e5--1e6 Msun. Three reference points sit inside it, all
    # legitimate, each marking something different:
    #   T = 1.02  MeV = 2 m_e c^2 -- kinematic threshold: below it, photon
    #                   pairs can no longer create e+e-. Quoted in F2's
    #                   figure caption as the upper-middle reference point.
    #   T = 0.511 MeV = m_e c^2   -- the value usually quoted in the
    #                   cosmological literature for the annihilation epoch
    #                   itself: the Boltzmann tail keeps the process running
    #                   below the strict threshold. Used here.
    #   T ~ 0.16  MeV             -- lower bound of the window, used by
    #                   plot_ECFLRDJeansMass.py for the Jeans-mass estimate.
    # None of them is the end: complete freeze-out is near 16 keV
    # (Phys. Rev. D 101, 063507). Since M_H ~ 1/T^2, the window spans a
    # factor ~100 in mass -- which is why F2 quotes a RANGE, not a value.
    # Neither is wrong; quoting one without saying which is.
    # NB: the label below says "onset" but 0.511 MeV is the standard epoch
    # marker, not the kinematic onset (that is 1.02 MeV). Kept for continuity
    # of the timeline labels; the distinction is documented above.
    ("Great Annihilation (onset)", 0.511e-3, 10.75, 10.75,
     "T = m_e c^2 = 0.511 MeV, pair-production threshold"),
    ("Great Annihilation (end)", 0.162e-3, 3.36, 3.91,
     "T ~ m_e/3, effective end of e+e- annihilation"),
    ("BBN (deuterium)", 0.070e-3, 3.36, 3.91,
     "T ~ 70 keV, deuterium bottleneck"),
]


def main():
    print("=" * 78)
    print("  ECF timeline, rebuilt from standard cosmology")
    print("=" * 78)
    print("\n  Nothing below is taken from the corpus. The comparison comes after.")

    print(f"\n  {'epoch':<28}{'T':>12}{'z':>12}{'t':>12}{'M_H [Msun]':>14}")
    print(f"  {'':<28}{'':>12}{'':>12}{'':>12}{'':>14}")
    rows = []
    for label, T, gstar, gs, src in EPOCHS:
        H = hubble(T, gstar)
        z = redshift(T, gs)
        t = 1.0 / (2.0 * H)
        M = horizon_mass(H)
        rows.append((label, T, z, t, M, src))
        T_disp = f"{T*1e3:.3g} MeV" if T < 1 else f"{T:.4g} GeV"
        print(f"  {label:<28}{T_disp:>12}{z:>12.2e}{t:>12.2e}{M/M_SUN:>14.3e}")

    print("\n  sources:")
    for label, _, _, _, _, src in rows:
        print(f"    {label:<28} {src}")

    # --- the ordering check, which is what failed in the corpus ------------
    print("\n" + "-" * 78)
    print("  ORDERING CHECK")
    print("-" * 78)
    ok = all(rows[i][2] > rows[i + 1][2] for i in range(len(rows) - 1))
    print(f"    redshift strictly decreasing with time: {'OK' if ok else 'FAILED'}")
    print("    (a later epoch must have a SMALLER z; the corpus placed the QCD")
    print("     transition at z = 1e12 and the electroweak one at z = 1.5e11,")
    print("     which puts QCD BEFORE the electroweak transition)")

    # --- what the corpus says ----------------------------------------------
    print("\n" + "=" * 78)
    print("  COMPARISON WITH THE VALUES QUOTED IN FOUNDATION II")
    print("=" * 78)
    z_ew = rows[0][2]
    z_qcd = rows[2][2]
    print(f"  {'quantity':<34}{'corpus':>14}{'rebuilt':>14}{'factor':>12}")
    print(f"  {'z, electroweak':<34}{'1.5e+11':>14}{z_ew:>14.2e}{z_ew/1.5e11:>12.1e}")
    print(f"  {'z, QCD/QGP':<34}{'1.0e+12':>14}{z_qcd:>14.2e}{z_qcd/1.0e12:>12.2f}")
    print()
    print("  => the QCD value is right to within a factor 2; the electroweak")
    print("     one is low by some three to four orders of magnitude.")
    print(f"     A redshift of 1.5e11 corresponds to T ~ "
          f"{1.5e11*T_CMB*K_B/GEV_J*1e3:.0f} MeV, which is no ECF epoch at all.")

    # --- the collision rates ----------------------------------------------
    print("\n" + "-" * 78)
    print("  COLLISION RATES: internal consistency of Gamma ~ (1+z)^{3/2}")
    print("-" * 78)
    z1, G1 = 1.5e11, 1e-16
    z2, G2 = 1.0e12, 1e-4
    print(f"    quoted: Gamma({z1:.1e}) = {G1:.0e} s^-1, "
          f"Gamma({z2:.1e}) = {G2:.0e} s^-1")
    print(f"    the stated scaling predicts a ratio of {(z2/z1)**1.5:.1f}")
    print(f"    the quoted values differ by {G2/G1:.0e}")
    print(f"    => inconsistent by {(G2/G1)/((z2/z1)**1.5):.1e}")
    print()
    print(f"    'one encounter every ~300 s' for Gamma = 1e-16 s^-1:")
    print(f"       1/Gamma = {1/G1:.0e} s = {1/G1/YR:.0e} yr, not 300 s")
    print(f"    '1e4 collisions per second' for Gamma = 1e-4 s^-1:")
    print(f"       1/Gamma = {1/G2:.0e} s -- one collision every ~3 hours,")
    print(f"       which is the reciprocal of what is written")

    print("\n" + "=" * 78)
    print("  WHAT THIS SCRIPT DOES NOT SETTLE")
    print("=" * 78)
    print("  * Which Gamma^(0) is correct: the rate depends on the defect number")
    print("    density and cross-section, neither of which is rebuilt here.")
    print("  * Whether coagulation can reach 1e5 Msun: that needs the rate AND")
    print("    a Smoluchowski-type integration, not an order-of-magnitude check.")
    print("  * The ECF background modifies H at very early times through the")
    print("    stiff spin fluid; the redshifts above are standard-cosmology")
    print("    values and would shift if that term is included before the QCD")
    print("    epoch. That is a deliberate choice: mixing the two is what")
    print("    produced the inconsistency in the first place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
