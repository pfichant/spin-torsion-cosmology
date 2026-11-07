#!/usr/bin/env python3
"""
prepare_fig10_csv.py
====================
ECF Foundation II — builds the ten per-galaxy CSV files that
`plot_fig10_analysis.py` expects in `data/`.

WHY THIS SCRIPT EXISTS
----------------------
On 25/08/2026 Pascal reported that Figure 29 of F2 ("Universality of the ECF
Torsion Halo") printed TEN PANELS EACH READING "File Not Found".

That is a THIRD kind of hole, and the nastiest of the three:
  1. a missing PNG with \\includegraphics  -> LaTeX error          (loud)
  2. a missing PNG with \\safeincludegraphics -> "[Figure: ...]"    (visible)
  3. a PNG that EXISTS but whose CONTENT is empty -> NOTHING AT ALL (silent)
Case 3 passes every check: the file is there, LaTeX is happy, pdftotext finds
no placeholder. Only looking at the figure reveals it. The generating script
had failed gracefully -- it drew "File Not Found" in each panel and exited 0.

=> Lesson recorded: a script that degrades gracefully must NOT exit 0.
   `plot_fig10_analysis.py` should fail loudly when its inputs are absent.

WHAT IT DOES
------------
Reads the SPARC rotation curves (Lelli+2016, Rotmod_LTG) already present in
`data/sparc/` and writes `data/<GALAXY>.csv` for the ten targets, with the
columns the plotting script reads: Radius, Vobs, Verr, Vbar.

The baryonic velocity uses THE SAME mass-to-light ratios as
`plot_sparc175_mosaic.py` (M/L disk = 0.50, bulge = 0.70) so that Figure 29
and the 171-galaxy mosaic cannot disagree on the same galaxy. Choosing
different ratios here would silently make two figures of the same paper
contradict each other.

    Vbar^2 = Vgas^2 + 0.50 * Vdisk^2 + 0.70 * Vbul^2
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ML_DISK = 0.50      # identical to plot_sparc175_mosaic.py -- do not diverge
ML_BULGE = 0.70

HERE = Path(__file__).resolve().parent
SPARC = HERE / "data" / "sparc"
OUT = HERE / "data"

TARGETS = [
    "NGC 6503", "NGC 3198", "NGC 2403", "NGC 2841", "NGC 2903",
    "NGC 3521", "NGC 5055", "NGC 7331", "DDO 154", "NGC 7814",
]

COLS = ["Rad", "Vobs", "errV", "Vgas", "Vdisk", "Vbul", "SBdisk", "SBbul"]


def load_rotmod(path):
    df = pd.read_csv(path, sep=r"\s+", comment="#",
                     names=COLS, usecols=[0, 1, 2, 3, 4, 5])
    df = df.dropna()
    df = df[(df["Rad"] > 0) & (df["errV"] > 0)]
    return df


def main():
    if not SPARC.is_dir():
        sys.exit(f"ERROR: {SPARC} not found. Extract Rotmod_LTG.zip there first.")

    OUT.mkdir(parents=True, exist_ok=True)
    missing, written = [], 0

    for name in TARGETS:
        src = SPARC / (name.replace(" ", "") + "_rotmod.dat")
        if not src.exists():
            missing.append(name)
            continue
        df = load_rotmod(src)
        vbar = np.sqrt(df["Vgas"] ** 2
                       + ML_DISK * df["Vdisk"] ** 2
                       + ML_BULGE * df["Vbul"] ** 2)
        out = pd.DataFrame({
            "Radius": df["Rad"].values,
            "Vobs": df["Vobs"].values,
            "Verr": df["errV"].values,
            "Vbar": vbar.values,
        })
        dest = OUT / f"{name}.csv"
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(f"# {name} -- SPARC (Lelli+2016), Rotmod_LTG\n")
            fh.write(f"# Vbar = sqrt(Vgas^2 + {ML_DISK}*Vdisk^2 + {ML_BULGE}*Vbul^2)\n")
            fh.write("# M/L identical to plot_sparc175_mosaic.py -- do not diverge\n")
            out.to_csv(fh, index=False)
        written += 1
        print(f"  {name:<10} {len(out):>3} points -> {dest.name}")

    print(f"\n{written}/{len(TARGETS)} CSV written.")
    if missing:
        # Loud failure: a silently incomplete input set is what produced the
        # ten "File Not Found" panels in the first place.
        sys.exit("ERROR: missing SPARC files for: " + ", ".join(missing))


if __name__ == "__main__":
    main()
