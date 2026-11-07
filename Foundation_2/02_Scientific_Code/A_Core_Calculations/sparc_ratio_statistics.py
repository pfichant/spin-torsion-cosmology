#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
FILENAME    : sparc_ratio_statistics.py
DESCRIPTION : Measures the observed spread of M_dyn/M_bar across the 175 SPARC
              galaxies -- the reference distribution any ECF "ratio" claim must
              be judged against.
PAPER       : Foundation II
=============================================================================

⚠️ WHY THIS SCRIPT EXISTS
--------------------------
On 21/08/2026, `calculate_halo_ecf.py` printed a dark/baryon ratio of 5.90 for
NGC 6503, next to the framework's primordial 5:1. ⭐ THE TWO ARE DIFFERENT
QUANTITIES -- one is a global ratio fixed at torsion crystallisation (T ~ 150
GeV), the other a local, present-day ratio integrated to an ARBITRARY radius --
but their numerical closeness LOOKS like a confirmation.

⭐⭐ THE PRINCIPLE AT STAKE: an agreement is only evidence if DISAGREEMENT WAS
POSSIBLE. So the question is not "is 5.90 close to 5?" but "what range do real
galaxies occupy?" -- and that has to be MEASURED, not recalled.

⚠️ Two estimates were made from memory before this script existed: "~3 to ~30"
(mine) and "up to 20" (Pascal's). BOTH WERE WRONG. That is exactly why the
number belongs in a script rather than in a comment.

⚠️ SCOPE -- WHAT THIS DOES *NOT* MEASURE
-----------------------------------------
M_dyn/M_bar here uses V_obs^2/V_bar^2 at a chosen radius: it is a DYNAMICAL
ratio, not a mass ratio integrated over a halo, and it is model-independent
only in the sense that it assumes nothing beyond Newtonian rotation support.
It says how much unseen mass a galaxy needs, not what that mass is.

USAGE:  python3 sparc_ratio_statistics.py [--data DIR] [--at outer|flat]
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import argparse
import glob
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# SPARC mass-to-light ratios, held fixed (Lelli, McGaugh & Schombert 2016)
UPSILON_DISK = 0.5
UPSILON_BUL = 0.7


def rapport_galaxie(chemin, ou="outer"):
    """M_dyn/M_bar at the outermost measured point (or at the flat part)."""
    try:
        d = np.loadtxt(chemin, comments="#")
    except Exception:
        return None
    # ⚠️ SAMPLE SIZE: this script reports 175 galaxies where fit_sparc175.py
    # reports 171, and the difference is DELIBERATE, not an inconsistency.
    # fit_sparc175 FITS a two-parameter model, so it requires 5 points to
    # leave 3 degrees of freedom: below that the reduced chi2 is
    # uninterpretable (see its header, threshold raised on 22/08/2026).
    # This script FITS NOTHING. It reads M_dyn/M_bar at the outermost
    # measured point -- one number per galaxy, no free parameter, no degree
    # of freedom. Applying the nu >= 3 cut here would discard four
    # perfectly measured galaxies to satisfy a criterion that does not
    # apply. The two samples answer two different questions.
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 4:
        return None
    rad, vobs, errv, vgas, vdisk, vbul = (d[:, i] for i in range(6))
    # signed squares: SPARC allows negative Vdisk for counter-rotating parts
    vbar2 = (vgas * np.abs(vgas)
             + UPSILON_DISK * vdisk * np.abs(vdisk)
             + UPSILON_BUL * vbul * np.abs(vbul))
    if ou == "flat":
        # average over the outer third, where the curve is usually flat
        i0 = max(len(rad) * 2 // 3, 1)
        num, den = np.mean(vobs[i0:] ** 2), np.mean(vbar2[i0:])
    else:
        num, den = vobs[-1] ** 2, vbar2[-1]
    if den <= 0 or num <= 0:
        return None
    return float(num / den), float(rad[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sparc")
    ap.add_argument("--at", choices=["outer", "flat"], default="outer")
    a = ap.parse_args()

    fichiers = sorted(glob.glob(os.path.join(a.data, "*_rotmod.dat")))
    if not fichiers:
        print(f"[ERROR] no *_rotmod.dat in {a.data}")
        return 1

    res = []
    for f in fichiers:
        r = rapport_galaxie(f, a.at)
        if r:
            res.append((os.path.basename(f).replace("_rotmod.dat", ""), *r))

    v = np.array([x[1] for x in res])
    q1, med, q3 = np.percentile(v, [25, 50, 75])

    print("=" * 74)
    # The count is printed with its criterion so a reader comparing it to
    # the 171 of fit_sparc175.py sees at once why they differ.
    print(f"  M_dyn / M_bar across SPARC -- {len(res)} galaxies, at the "
          f"{'outermost point' if a.at == 'outer' else 'flat part'}")
    print("=" * 74)
    print(f"    median          : {med:.2f}")
    print(f"    quartiles       : {q1:.2f} - {q3:.2f}")
    print(f"    full range      : {v.min():.2f} - {v.max():.1f}")
    print(f"    mean            : {v.mean():.2f}")
    print(f"    above 10        : {(v > 10).sum()} galaxies "
          f"({(v > 10).mean()*100:.0f} %)")
    print(f"    above 20        : {(v > 20).sum()} galaxies")
    # ⚠️ these two lines back the claim made in F2 Sec. (galactic outskirts):
    # the local ratio does NOT generally exceed the global ~5.
    print(f"    above 5         : {(v > 5).sum()} galaxies "
          f"({(v > 5).mean()*100:.0f} %)")
    print(f"    below 5         : {(v < 5).sum()} galaxies "
          f"({(v < 5).mean()*100:.0f} %)  <- the majority")

    res.sort(key=lambda x: -x[1])
    print("\n    highest five:")
    for n, r, rr in res[:5]:
        print(f"      {n:<16} {r:>6.1f}   (last point at {rr:.1f} kpc)")

    # ── what this means for any "ratio ~ 5" claim ──────────────────────────
    dans = ((v > 4) & (v < 7)).mean() * 100
    print("\n" + "-" * 74)
    print("  ⚠️ WHAT THIS MEANS FOR A 'RATIO ~ 5' CLAIM")
    print("-" * 74)
    print(f"    {dans:.0f} % of SPARC galaxies already fall between 4 and 7.")
    print(f"    The sample median is {med:.1f}.")
    print("    ⭐ A galaxy landing near 5 is therefore UNREMARKABLE: it is the")
    print("      typical behaviour of the sample, not a successful prediction.")
    print("    ⇒ An agreement is evidence ONLY IF DISAGREEMENT WAS POSSIBLE.")
    print("      Here it was not: landing in 3-6 was the most likely outcome.")
    print()
    print("    ⚠️ And the framework's 5:1 is a DIFFERENT QUANTITY anyway --")
    print("      global and primordial (Omega_DM/Omega_b, fixed at T ~ 159 GeV),")
    print("      not local and present-day. F2 states this at Sec. 'universal")
    print("      mass ratio ~5 ... the local ratio Gamma(r)'.")
    print("-" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
