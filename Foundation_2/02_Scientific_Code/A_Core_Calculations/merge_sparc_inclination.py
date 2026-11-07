#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge the SPARC master table (inclination, quality flag) into the fit results.

WHY THIS EXISTS (audit of 24/08/2026)
--------------------------------------
Foundation II explains its 23 poorly-fitting galaxies by "n_pts < 8 kinematic
points or inclination i < 30 deg". The first half is testable from
output/sparc175_fit_results.csv and turns out to be WRONG: only 1 of the 23
outliers has fewer than 8 points, and their median sampling is 24 points
against 13 for the rest -- the outliers are the BEST-sampled galaxies.

The second half was not testable at all, because the inclination is not in the
*_rotmod.dat files that fit_sparc175.py reads: those carry only radius,
velocity, error, gas, disk and bulge. The inclination lives in the SPARC master
table (Lelli, McGaugh & Schombert 2016, AJ 152, 157).

Publishing an explanation a reader cannot check is worse than publishing none
(rule 5octovicies + the reproducibility requirement raised by a cosmologist
at the Laboratoire Univers et Particules de Montpellier). This script closes
that gap: it makes the inclination part of the deposited data, so any referee
can redo the cut.

DATA SOURCE
-----------
VizieR catalogue J/AJ/152/157, file table1.dat -- fixed-width, 175 rows.
  https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat
Mirror (same content, MRT header) published by AJ:
  https://content.cld.iop.org/journals/1538-3881/152/6/157/revision1/ajaa3207t1_mrt.txt

Byte-by-byte layout used below (from the VizieR ReadMe):
     1- 11  A11        Name      Galaxy name
    13- 14  I2         Type      Numerical Hubble type
    16- 21  F6.2  Mpc  Dist      Distance
    32- 35  F4.1  deg  Inc       Inclination        <-- what we need
    37- 40  F4.1  deg  e_Inc     Error on Inc
The quality flag Q (1 = high quality, 2 = minor asymmetries, 3 = major
asymmetries) sits near the end of the row; it is read by keyword below rather
than by byte offset, because it is the last small integer on the line.

USAGE
-----
    # 1. download the table once (any of the two URLs above)
    curl -o sparc_table1.dat \\
      https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat

    # 2. merge it into the fit results
    python3 merge_sparc_inclination.py \\
        --table sparc_table1.dat \\
        --fits  output/sparc175_fit_results.csv \\
        --out   output/sparc175_fit_results.csv

The output keeps every existing column and adds `inclination_deg`. Running it
twice is safe: the column is overwritten, not duplicated.
"""
import argparse
import os
import sys

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── PROVENANCE OF THE DATA ───────────────────────────────────────────────────
# Kept as constants, not only in the docstring: they are printed at every run
# and reported when the file is missing, so a reader who only has the
# repository can retrieve the exact same table.
SPARC_TABLE_URL = "https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat"
SPARC_TABLE_MIRROR = ("https://content.cld.iop.org/journals/1538-3881/152/6/"
                      "157/revision1/ajaa3207t1_mrt.txt")
SPARC_CATALOGUE = "VizieR J/AJ/152/157 (table1.dat, 175 rows)"
SPARC_REFERENCE = ("Lelli F., McGaugh S. S., Schombert J. M., 2016, AJ 152, 157 "
                   "-- doi:10.3847/0004-6256/152/6/157")
SPARC_HOME = "http://astroweb.cwru.edu/SPARC/"


def read_master(path):
    """Parse the SPARC master table. Returns name / inclination / Hubble type.

    Split on whitespace rather than byte offsets. The VizieR ReadMe documents
    Inc at bytes 32-35, but the distributed file carries the distance flag f_D
    on ONE character instead of two, so every field after it is shifted left by
    one: reading [31:35] returns e_Inc (the error, typically 3-10 deg) instead
    of Inc. That produced a median "inclination" of 3 deg on 24/08/2026 --
    physically impossible, since SPARC excludes galaxies below 30 deg.

    Whitespace splitting is safe here and was verified on the real file:
    175 rows, exactly 19 fields each, and no galaxy name contains a space.

    Field order (from the ReadMe):
        0 Name  1 Type  2 Dist  3 e_D  4 f_D  5 Inc  6 e_Inc  ...
    """
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            f = line.split()
            if len(f) < 7:
                continue                      # header, ReadMe or blank line
            try:
                typ = int(f[1])
                inc = float(f[5])
            except ValueError:
                continue                      # header line
            # SPARC selects galaxies above 30 deg; anything outside 0-90 means
            # the wrong column was read, so it is dropped rather than trusted.
            if not (0.0 <= inc <= 90.0):
                continue
            rows.append({"galaxy": f[0], "inclination_deg": inc,
                         "hubble_type": typ})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    # Default alongside the *_rotmod.dat files, where fetch_sparc_data.py puts
    # the SPARC data: the master table belongs with the data it describes, and
    # the orchestrator runs this script without arguments.
    ap.add_argument("--table",
                    default=os.path.join("data", "sparc", "sparc_table1.dat"),
                    help="SPARC master table (table1.dat from VizieR)")
    ap.add_argument("--fits", default="output/sparc175_fit_results.csv")
    ap.add_argument("--out", default="output/sparc175_fit_results.csv")
    a = ap.parse_args()

    print(f"[SOURCE] {SPARC_CATALOGUE}")
    print(f"[SOURCE] {SPARC_REFERENCE}")
    print(f"[SOURCE] {SPARC_TABLE_URL}")

    if not os.path.exists(a.table):
        print(f"[ERROR] master table not found: {a.table}")
        print( "        Download it first (either mirror gives the same table):")
        print(f"          curl -o {a.table} {SPARC_TABLE_URL}")
        print(f"          mirror: {SPARC_TABLE_MIRROR}")
        print(f"        Catalogue home page: {SPARC_HOME}")
        return 1

    master = read_master(a.table)
    print(f"[INFO] master table: {len(master)} galaxies with an inclination")
    if len(master) < 150:
        print("[ERROR] too few rows parsed -- check the file is table1.dat "
              "and not the ReadMe. Nothing written.")
        return 1

    fits = pd.read_csv(a.fits)
    print(f"[INFO] fit results  : {len(fits)} galaxies")

    if "inclination_deg" in fits.columns:
        fits = fits.drop(columns=["inclination_deg", "hubble_type"],
                         errors="ignore")

    merged = fits.merge(master, on="galaxy", how="left")
    missing = merged.inclination_deg.isna().sum()

    # A name that fails to match is a silent data loss, so it is reported
    # rather than dropped.
    if missing:
        print(f"[WARN] {missing} galaxies without a match -- names differ "
              f"between the two files:")
        for n in merged[merged.inclination_deg.isna()].galaxy.head(10):
            print(f"         {n}")
    else:
        print("[OK]   every fitted galaxy matched a master-table entry")

    merged.to_csv(a.out, index=False)
    print(f"[INFO] written: {a.out}")

    # What the paper's claim actually needs, printed straight away.
    c = "chi2_ecf" if "chi2_ecf" in merged.columns else "chi2_red"
    out = merged[merged[c] > 5]
    rest = merged[merged[c] <= 5]
    print()
    print("=" * 66)
    print("  TEST OF THE CLAIM IN Foundation II")
    print("=" * 66)
    print(f"  outliers (chi2 > 5)              : {len(out)}")
    print(f"    with inclination < 30 deg      : {(out.inclination_deg < 30).sum()}")
    print(f"    with n_points < 8              : {(out.n_points < 8).sum()}")
    print(f"    median inclination             : {out.inclination_deg.median():.1f} deg")
    print(f"    median inclination, others     : {rest.inclination_deg.median():.1f} deg")
    print()
    print("  Converse test -- do low-inclination galaxies fit badly?")
    low = merged[merged.inclination_deg < 30]
    high = merged[merged.inclination_deg >= 30]
    print(f"    i <  30 deg : {len(low):>3} galaxies, median chi2 = {low[c].median():.3f}")
    print(f"    i >= 30 deg : {len(high):>3} galaxies, median chi2 = {high[c].median():.3f}")
    try:
        from scipy.stats import spearmanr
        r, pv = spearmanr(merged.inclination_deg, merged[c])
        print(f"    rank correlation inclination vs chi2 : rho = {r:+.3f} (p = {pv:.3f})")
    except ImportError:
        pass
    print()
    print("  Sanity check: SPARC selects galaxies above ~30 deg, so a median")
    print("  inclination far below 50 deg means the WRONG COLUMN was read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
