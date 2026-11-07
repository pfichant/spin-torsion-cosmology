#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vsf_observed_dr1.py  --  ECF Foundation III
======================================================================
The observed void size function, measured from DESIVAST DR1 itself.

WHY THIS SCRIPT EXISTS
----------------------
plot_F3_ecf_vsf_desivast_fits.py carries this warning about the counts
it compares against:

    "DR1_COUNTS is NOT a theoretical LCDM void size function. It is a
     crude PLACEHOLDER: the *shape* is taken from an older SDSS
     VoidFinder catalogue, rescaled to an *expected* DESI DR1 total
     (N_DR1=1484) and multiplied by a hand-tuned depth factor
     (DEPTH_F=1.4), with an extra ad hoc x1.5 on the last bin. None of
     these numbers is derived from a theory, a simulation, or an
     excursion-set calculation. [...] the large deficits reported
     (about -6 to -19 sigma) are therefore very likely an ARTEFACT of
     the rescaling, NOT evidence of a real cosmological tension. They
     must not be quoted as such, in the papers or elsewhere."

    "TODO: replace with a proper LCDM VSF [...] before any of these
     significances is used as a published result."

The catalogue is now in hand, so the first half of that TODO can be
settled: the OBSERVED counts no longer need to be guessed from SDSS.
This script measures them directly.

WHAT IT DOES, AND WHAT IT DOES NOT
----------------------------------
DOES: measures N(R_eff) from the DESIVAST DR1 VoidFinder catalogue,
      NGC + SGC, with and without the interior-void cut, and compares
      the result to the placeholder.

DOES NOT: supply a theoretical LambdaCDM prediction. Replacing the
      placeholder observed counts removes one of the two defects; the
      other -- having no LambdaCDM baseline to compare against --
      remains, and no significance can be quoted until it is fixed
      (excursion-set model, or the AbacusSummit BGS mocks that
      DESIVAST itself provides). This script does not pretend
      otherwise, and prints no sigma.

WHY EDGE MATTERS
----------------
The MAXIMALS HDU carries an EDGE flag with values 0, 1, 2. EDGE = 0
marks interior voids -- those not touching the survey boundary. Summing
over NGC + SGC gives 1,489 interior voids, exactly the number quoted in
the DESIVAST paper, which confirms the flag is being read as intended.
A boundary void has an ill-constrained volume and an overestimated
effective radius, so a void size function must be built on interior
voids; the "all voids" column is printed only for comparison.

Data: place the VoidFinder FITS files under desivast_dr1/ (or pass
--dir). They are small (0.6-3.9 MB), unlike the V2 catalogues.

Usage: python3 build_vsf_observed_dr1.py [--dir PATH]
======================================================================
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
import os

import numpy as np

H = 0.6732                       # DESIVAST fiducial (Planck 2018)

# The binning of the existing script, kept so the two are comparable.
BINS_H = np.array([10, 13, 16, 19, 22, 25, 28, 32, 36, 42, 54], dtype=float)

# The placeholder currently in plot_F3_ecf_vsf_desivast_fits.py
SDSS_COUNTS = np.array([155, 210, 215, 185, 150, 110, 70, 40, 20, 8], dtype=float)
N_DR1_ASSUMED = 1484
DEPTH_F = 1.4


def placeholder_counts():
    c = SDSS_COUNTS * (N_DR1_ASSUMED / SDSS_COUNTS.sum()) * DEPTH_F
    c = c.copy()
    c[-1] *= 1.5
    return c


def load_voidfinder(d):
    from astropy.io import fits
    r, e = [], []
    found = []
    for hemi in ("NGC", "SGC"):
        p = os.path.join(d, f"DESIVAST_BGS_VOLLIM_VoidFinder_{hemi}.fits")
        if not os.path.exists(p):
            continue
        with fits.open(p) as hdul:
            t = hdul["MAXIMALS"].data
            r.append(np.asarray(t["R_EFF"], dtype=float))
            e.append(np.asarray(t["EDGE"]))
        found.append(hemi)
    if not r:
        return None, None, found
    return np.concatenate(r), np.concatenate(e), found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None)
    a = ap.parse_args()

    if a.dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        parent = os.path.dirname(here)
        repo_root = os.path.dirname(parent)   # .../Foundation_3, two levels up
        # Canonical location: Foundation_3/data/desivast_dr1/, a single
        # visible data folder at repo root, independent of which category
        # subfolder (A_Core_Calculations, B_Paper_Plots, ...) the script
        # itself lives in. Checked first; older layouts kept as fallback
        # for anyone who has not moved their files yet.
        for c in (
            os.path.join(repo_root, "data", "desivast_dr1"),
            "data/dr1/desivast_dr1", "desivast_dr1", ".",
            os.path.join(here, "desivast_dr1"),
            os.path.join(here, "data", "dr1", "desivast_dr1"),
            os.path.join(parent, "B_Paper_Plots", "desivast_dr1"),
            os.path.join(parent, "A_Core_Calculations", "desivast_dr1"),
            here,
        ):
            if os.path.exists(os.path.join(
                    c, "DESIVAST_BGS_VOLLIM_VoidFinder_NGC.fits")):
                a.dir = c
                break
        else:
            a.dir = os.path.join(repo_root, "data", "desivast_dr1")

    print("=" * 68)
    print("  Observed void size function, measured from DESIVAST DR1")
    print("=" * 68)

    r, e, found = load_voidfinder(a.dir)
    if r is None:
        print(f"\n  VoidFinder catalogues not found in '{a.dir}/'.")
        print("  They are small (0.6-3.9 MB); see plot_F3_ecf_vsf_desivast_fits.py")
        print("  for the download URL.")
        return 1

    print(f"\n  hemispheres read: {', '.join(found)}")
    print(f"  voids: {len(r):,}   interior (EDGE == 0): {int((e == 0).sum()):,}")
    if int((e == 0).sum()) == 1489:
        print("  -> matches the 1,489 interior voids quoted by DESIVAST: the")
        print("     EDGE flag is being read as intended.")

    n_all, _ = np.histogram(r, bins=BINS_H)
    n_int, _ = np.histogram(r[e == 0], bins=BINS_H)
    ph = placeholder_counts()

    print("\n" + "-" * 68)
    print("  Counts per bin in R_eff [Mpc/h]")
    print("-" * 68)
    print(f"  {'bin':>12} {'measured':>10} {'interior':>10} {'placeholder':>12}"
          f" {'ratio':>8}")
    for i in range(len(n_all)):
        lo, hi = BINS_H[i], BINS_H[i + 1]
        ratio = (n_int[i] / ph[i]) if ph[i] > 0 else float("nan")
        print(f"  {lo:>5.0f}-{hi:<6.0f} {n_all[i]:>10,} {n_int[i]:>10,}"
              f" {ph[i]:>12.0f} {ratio:>8.2f}")
    print(f"  {'TOTAL':>12} {n_all.sum():>10,} {n_int.sum():>10,} {ph.sum():>12.0f}")

    print("\n" + "-" * 68)
    print("  What the placeholder got wrong")
    print("-" * 68)
    print(f"  total:  measured interior {n_int.sum():,}  vs  placeholder "
          f"{ph.sum():.0f}   ({100*(n_int.sum()/ph.sum()-1):+.0f} %)")
    print(f"  peak :  measured peaks in bin {BINS_H[int(np.argmax(n_int))]:.0f}"
          f"-{BINS_H[int(np.argmax(n_int))+1]:.0f}, placeholder in bin "
          f"{BINS_H[int(np.argmax(ph))]:.0f}-{BINS_H[int(np.argmax(ph))+1]:.0f}")
    print(f"  tail :  measured max R_eff = {r[e == 0].max():.2f} Mpc/h (interior),"
          f" {r.max():.2f} (all)")
    empty = [f"{BINS_H[i]:.0f}-{BINS_H[i+1]:.0f}" for i in range(len(n_int))
             if n_int[i] == 0 and ph[i] > 0]
    if empty:
        print(f"  bins where the placeholder predicts voids and none exist:")
        print(f"          {', '.join(empty)}  "
              f"(placeholder: {', '.join(f'{ph[i]:.0f}' for i in range(len(n_int)) if n_int[i] == 0 and ph[i] > 0)})")

    print("\n" + "=" * 68)
    print("  READING THIS")
    print("=" * 68)
    print("  The measured distribution is far more peaked than the placeholder")
    print("  and dies out much sooner. Deficits computed against the")
    print("  placeholder were therefore comparing the data to a shape the data")
    print("  never had -- which is what the original warning said, and this")
    print("  quantifies it.")
    print()
    print("  The observed side of the comparison is now measured rather than")
    print("  assumed. The THEORETICAL side is not: there is still no LambdaCDM")
    print("  VSF to compare against, so NO SIGNIFICANCE IS QUOTED HERE and none")
    print("  should be quoted elsewhere until an excursion-set model or the")
    print("  AbacusSummit BGS mocks are used.")


if __name__ == "__main__":
    sys.exit(main() or 0)
