#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_smallscale_granularity.py  --  ECF Foundation II
=============================================================================
Can the granularity of the ECF halo account for the small-scale problems of
LambdaCDM? It cannot, and this script is the arithmetic.

WHY THIS SCRIPT EXISTS
----------------------
Foundation II now carries a section stating that the framework makes no claim
on the missing satellites, too-big-to-fail, or the diversity of dwarf rotation
curves. That section quotes numbers -- 1e5 knots per dwarf halo, 0.3 per cent
fluctuations, 1e8-1e9 Msun required -- and a number in a paper without a script
behind it is an assertion, not a result. This is the script.

THE ARGUMENT
------------
A halo made of N discrete objects has Poissonian density fluctuations of order
1/sqrt(N). For the diversity problem, the relevant comparison is between those
fluctuations and the profile-to-profile scatter actually observed in dwarfs,
which is several tens of per cent.

The calculation is deliberately generous to the framework: it assumes every
knot contributes independently to the local potential, ignores the smoothing
from line-of-sight integration, and takes the smallest plausible halo. Even so
the answer falls short by two orders of magnitude.

WHAT THIS DOES AND DOES NOT SETTLE
----------------------------------
SETTLES: granularity at 1e5 Msun cannot produce tens-of-per-cent profile
         variations. That is arithmetic, not interpretation.
DOES NOT SETTLE: whether some other feature of the framework might address the
         diversity problem. Nothing here rules that out; it rules out the one
         mechanism that looked promising.

Missing satellites and too-big-to-fail are not addressed at all: the first is
a star-formation question (the halos are expected to exist and stay dark), the
second concerns the inner density profile. They are computed here only to show
the scale of what would be needed.

Dependency: numpy. Usage: python3 compute_smallscale_granularity.py
=============================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

M_SUN = 1.98892e30
M_MACRO = 1.0e5              # Msun, Macro-Knot scale (Foundation II)
OBSERVED_DIVERSITY = 0.30    # profile-to-profile scatter in dwarfs, order 30%


def fluctuation(M_halo_msun, M_knot_msun):
    """Poissonian fractional fluctuation, 1/sqrt(N)."""
    N = M_halo_msun / M_knot_msun
    return N, 1.0 / np.sqrt(N)


def knot_mass_required(M_halo_msun, target_fluct):
    """Knot mass that would give the target fluctuation."""
    N = 1.0 / target_fluct ** 2
    return M_halo_msun / N


def main():
    print("=" * 70)
    print("  ECF granularity vs the small-scale problems")
    print("=" * 70)

    print(f"\n  Macro-Knot mass assumed: {M_MACRO:.0e} Msun")
    print(f"  Observed diversity to reproduce: ~{100*OBSERVED_DIVERSITY:.0f} %")

    print("\n" + "-" * 70)
    print("  POISSONIAN FLUCTUATION BY HALO MASS")
    print("-" * 70)
    print(f"  {'M_halo [Msun]':>16}{'N knots':>14}{'1/sqrt(N)':>14}{'':>6}")
    for M_halo in (1e10, 1e11, 1e12):
        N, f = fluctuation(M_halo, M_MACRO)
        print(f"  {M_halo:>16.0e}{N:>14.0e}{100*f:>13.2f} %")

    N, f = fluctuation(1e10, M_MACRO)
    print(f"\n  Shortfall for a 1e10 Msun dwarf: "
          f"{OBSERVED_DIVERSITY/f:.0f}x, i.e. "
          f"{np.log10(OBSERVED_DIVERSITY/f):.1f} orders of magnitude.")

    print("\n" + "-" * 70)
    print("  WHAT KNOT MASS WOULD BE NEEDED")
    print("-" * 70)
    for target in (0.10, 0.30, 0.50):
        Mk = knot_mass_required(1e10, target)
        print(f"    {100*target:>3.0f} % fluctuation  ->  M_knot = {Mk:.1e} Msun"
              f"   ({Mk/M_MACRO:.0e} x the ECF value)")

    print("\n" + "=" * 70)
    print("  CONCLUSION")
    print("=" * 70)
    print("  Granularity at the Macro-Knot scale is two orders of magnitude")
    print("  short of the observed diversity. The framework makes no claim on")
    print("  this problem, and the calculation above is why.")
    print()
    print("  The calculation is generous: every knot is taken to contribute")
    print("  independently, line-of-sight smoothing is ignored, and the")
    print("  smallest plausible halo is used. A more careful treatment would")
    print("  widen the gap, not close it.")
    print()
    print("  Note what this does NOT show. It rules out one mechanism, not the")
    print("  problem. Whether some other feature of the framework bears on the")
    print("  diversity of dwarf rotation curves is untouched by this script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
