#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect_edge_area.py  --  run next to the DESIVAST .fits files
==============================================================
Are the large V2 voids edge voids, and how strongly?

WHY
---
extract_v2_radii.py showed that V2/VIDE NGC reaches 55.88 Mpc/h with 15
voids above 40.4 and 8 above 43.8 -- but that a cut EDGE_AREA == 0 drops
the maximum to 30.20 Mpc/h, i.e. below the ECF threshold and below even
the VoidFinder maximum.

That cut is almost certainly TOO STRICT: it keeps 113 voids where the
DESIVAST paper reports 297 interior voids for VIDE. EDGE_AREA is an AREA,
not a boolean flag, so the paper must use a fractional threshold rather
than exact zero.

This script does not guess the threshold. It prints the distribution, so
the right cut can be chosen from the data rather than assumed -- and it
shows where the large voids sit within it.

USAGE
-----
    python3 inspect_edge_area.py

Paste the output back. Nothing is written or modified.
==============================================================
"""

import glob
import os
import sys

try:
    import numpy as np
    from astropy.io import fits
except ImportError:
    sys.exit("pip install astropy numpy")

H = 0.6732
THR = {"60 Mpc": 60.0 * H, "65 Mpc": 65.0 * H}

print("=" * 70)
print("  EDGE_AREA distribution and the large voids")
print("=" * 70)

# [HARDENED 05/09/2026] Was a bare glob.glob("DESIVAST_BGS_VOLLIM_V2_*.fits"),
# which only found the files if run from the directory containing them.
# Now searches next to the script first, then the current directory.
_here = os.path.dirname(os.path.abspath(__file__))
for _cand in (_here, os.getcwd()):
    files = sorted(glob.glob(os.path.join(_cand, "DESIVAST_BGS_VOLLIM_V2_*.fits")))
    if files:
        break
if not files:
    sys.exit("No V2 files found here.")

for path in files:
    name = os.path.basename(path).replace("DESIVAST_BGS_VOLLIM_", "")
    print("\n" + "-" * 70)
    print(name)
    with fits.open(path, memmap=True) as hdul:
        d = hdul["VOIDS"].data
        cols = list(d.columns.names)
        print(f"   VOIDS columns: {cols}")
        r = np.asarray(d["RADIUS"], dtype=float)
        e = np.asarray(d["EDGE_AREA"], dtype=float)

        # is there also a total-area column? then a FRACTION can be formed
        area_cols = [c for c in cols if "AREA" in c.upper() and c.upper() != "EDGE_AREA"]
        print(f"   other area columns: {area_cols if area_cols else 'none'}")

        print(f"\n   EDGE_AREA over all {len(e):,} voids:")
        print(f"      == 0 exactly : {(e == 0).sum():,}")
        for q in (10, 25, 50, 75, 90, 99):
            print(f"      p{q:<3} = {np.percentile(e, q):.4g}")
        print(f"      max  = {e.max():.4g}")

        # if a total area exists, the fraction is the meaningful quantity
        frac = None
        if area_cols:
            tot = np.asarray(d[area_cols[0]], dtype=float)
            ok = tot > 0
            frac = np.full_like(e, np.nan)
            frac[ok] = e[ok] / tot[ok]
            print(f"\n   edge FRACTION = EDGE_AREA / {area_cols[0]}:")
            for q in (10, 25, 50, 75, 90):
                print(f"      p{q:<3} = {np.nanpercentile(frac, q):.4f}")
            for cut in (0.0, 0.01, 0.05, 0.10, 0.25, 0.50):
                keep = np.nan_to_num(frac, nan=1.0) <= cut
                if keep.sum():
                    print(f"      fraction <= {cut:<5}: N={keep.sum():>5,}"
                          f"   MAX radius = {r[keep].max():6.2f} Mpc/h")
                else:
                    print(f"      fraction <= {cut:<5}: N=0")

        # the large voids, one by one -- this is the decisive table
        print(f"\n   The largest voids (top 12 by radius):")
        hdr = f"      {'radius':>8} {'EDGE_AREA':>12}"
        if frac is not None:
            hdr += f" {'frac':>8}"
        print(hdr)
        order = np.argsort(r)[::-1][:12]
        for i in order:
            line = f"      {r[i]:>8.2f} {e[i]:>12.4g}"
            if frac is not None:
                line += f" {frac[i]:>8.3f}"
            for lab, t in THR.items():
                if r[i] > t:
                    line += f"  > {lab}"
            print(line)

        # how many voids clear each threshold, at a few plausible edge cuts
        print(f"\n   Voids above the ECF thresholds, by edge cut:")
        cuts = [("no cut", np.ones_like(e, dtype=bool)),
                ("EDGE_AREA == 0", e == 0)]
        if frac is not None:
            for c in (0.05, 0.10, 0.25):
                cuts.append((f"edge frac <= {c}",
                             np.nan_to_num(frac, nan=1.0) <= c))
        for lab, mask in cuts:
            s = f"      {lab:<18} N={mask.sum():>5,}"
            for tlab, t in THR.items():
                s += f"   >{tlab}: {int((r[mask] > t).sum()):>3}"
            print(s)

print("\n" + "=" * 70)
print("  Paste this back.")
print("=" * 70)
print("\nThe question it answers: are the 8 voids above 43.8 Mpc/h barely")
print("touching the survey boundary, or largely outside it? If their edge")
print("fraction is small, they are usable and the test is feasible. If it")
print("is large, the apparent reach of V2 is a boundary artefact and the")
print("corpus's conclusion holds -- for a better reason than the one written.")
