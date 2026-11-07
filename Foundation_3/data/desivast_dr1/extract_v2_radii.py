#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_v2_radii.py  --  run this on YOUR machine, next to the FITS files
=========================================================================
Extracts just the void radii from the DESIVAST V2 catalogues, so the
600 MB files never need to be uploaded.

WHY
---
The ECF VSF kill-switch currently uses the VoidFinder catalogue alone,
whose maximum effective radius is 31.7 Mpc/h -- below the ECF threshold
(40.4 Mpc/h for xi_KZ = 60, 43.8 for 65), hence the claim that the test
is "out of reach". The published DESIVAST paper gives 43.5 and 55.9
Mpc/h for the two V2 variants, which are ABOVE that threshold. Whether
the test is actually feasible therefore depends on data we do not have.

This script prints what is needed to settle it, and nothing else: a few
dozen numbers instead of a gigabyte.

USAGE
-----
Put this file in the directory containing the .fits files, then:

    python3 extract_v2_radii.py

Then paste the printed output back into the conversation. Nothing is
written to disk and no file is modified.

Dependency: astropy, numpy.
=========================================================================
"""

import glob
import os
import sys

try:
    import numpy as np
    from astropy.io import fits
except ImportError:
    sys.exit("Please install astropy and numpy:  pip install astropy numpy")

H = 0.6732                      # DESIVAST fiducial (Planck 2018)
ECF_THRESHOLDS_H = {"xi_KZ = 60 Mpc": 60.0 * H, "xi_KZ = 65 Mpc": 65.0 * H}

print("=" * 68)
print("  DESIVAST void radii  --  extraction for the ECF VSF test")
print("=" * 68)

# [HARDENED 05/09/2026] Was a bare glob.glob("DESIVAST_BGS_VOLLIM_*.fits"),
# which only found the files if the script happened to be *run* from the
# directory containing them -- not from wherever the .py file itself sits.
# Now searches relative to its own location first (__file__), then falls
# back to the current working directory, so it works either way.
_here = os.path.dirname(os.path.abspath(__file__))
for _cand in (_here, os.getcwd()):
    files = sorted(glob.glob(os.path.join(_cand, "DESIVAST_BGS_VOLLIM_*.fits")))
    if files:
        break
if not files:
    sys.exit(f"No DESIVAST_BGS_VOLLIM_*.fits found in {_here} or the "
              f"current directory.")

print(f"\n{len(files)} file(s) found.\n")

for path in files:
    name = os.path.basename(path)
    size_mb = os.path.getsize(path) / 1e6
    print("-" * 68)
    print(f"{name}   ({size_mb:.0f} MB)")
    try:
        with fits.open(path, memmap=True) as hdul:
            print(f"   HDUs: {[h.name for h in hdul]}")
            for hdu in hdul[1:]:
                if not hasattr(hdu, "columns") or hdu.columns is None:
                    continue
                names = list(hdu.columns.names)
                # the radius columns we care about
                rad = [c for c in names
                       if c.upper() in ("R_EFF", "RADIUS", "REFF", "R_EFF_UNCERT")]
                edge = [c for c in names if "EDGE" in c.upper()]
                if not rad:
                    print(f"   [{hdu.name}] {len(names)} cols, no radius column")
                    continue
                n = len(hdu.data)
                print(f"   [{hdu.name}] {n:,} rows   radius cols: {rad}"
                      + (f"   edge flag: {edge}" if edge else ""))
                for col in rad:
                    if "UNCERT" in col.upper():
                        continue
                    r = np.asarray(hdu.data[col], dtype=float)
                    r = r[np.isfinite(r) & (r > 0)]
                    if r.size == 0:
                        continue
                    print(f"      {col}:  N={r.size:,}  median={np.median(r):.2f}"
                          f"  p90={np.percentile(r,90):.2f}"
                          f"  p99={np.percentile(r,99):.2f}"
                          f"  MAX={r.max():.2f}  [Mpc/h]")
                    for label, thr in ECF_THRESHOLDS_H.items():
                        above = int((r > thr).sum())
                        print(f"         above {thr:.1f} Mpc/h ({label}): "
                              f"{above} void(s)")
                    # the same, restricted to interior voids if the flag exists
                    if edge:
                        try:
                            e = np.asarray(hdu.data[edge[0]]).astype(int)
                            ri = np.asarray(hdu.data[col], dtype=float)[e == 0]
                            ri = ri[np.isfinite(ri) & (ri > 0)]
                            if ri.size:
                                print(f"         interior only (flag {edge[0]}=0): "
                                      f"N={ri.size:,}  MAX={ri.max():.2f} Mpc/h")
                        except Exception:
                            pass
    except Exception as exc:
        print(f"   [could not read: {type(exc).__name__}: {exc}]")

print("\n" + "=" * 68)
print("  Paste everything above back into the conversation.")
print("=" * 68)
print("\nWhat matters most:")
print("  * MAX for each algorithm, and whether it survives the interior-only cut")
print("    (an edge void touching the survey boundary is not a reliable maximum);")
print("  * how many voids sit above the threshold -- one lone object would not")
print("    make the test feasible, a populated tail would.")
