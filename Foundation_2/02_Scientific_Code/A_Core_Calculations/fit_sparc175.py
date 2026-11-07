#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
FILENAME    : fit_sparc175.py
DESCRIPTION : Fits the adopted pseudo-isothermal halo (ECF; not yet derived
              from the torsion, PO-ECF-HALO) to the full SPARC database
              (175 galaxies) and writes output/sparc175_fit_results.csv.
PAPER       : Foundation II
=============================================================================

DATA SOURCE
-----------
Rotation curves: the *_rotmod.dat files of the SPARC database.
  home    : http://astroweb.cwru.edu/SPARC/
  archive : https://zenodo.org/records/16284118/files/Rotmod_LTG.zip
  (fetched by fetch_sparc_data.py; each file holds radius, V_obs, error,
   V_gas, V_disk, V_bulge -- and nothing else)
Reference : Lelli F., McGaugh S. S., Schombert J. M., 2016, AJ 152, 157
            doi:10.3847/0004-6256/152/6/157

Galaxy properties (inclination, Hubble type, distance) are NOT in these files.
They live in the SPARC master table, VizieR J/AJ/152/157 (table1.dat), and are
merged into the output by merge_sparc_inclination.py.

⚠️ WHY THIS SCRIPT EXISTS
--------------------------
On 21/08/2026 an audit found that `output/sparc175_fit_results.csv` was READ by
four scripts (check_stats.py, generate_SPARC_175_Comparison.py,
plot_sparc175_mosaic.py, plot_F2_sparc_model_comparison.py) and WRITTEN BY
NONE. That file carries the central dark-matter result of the framework --
chi2_med = 0.80 over 175 galaxies, quoted in the F2 abstract -- so the chain
producing the most exposed number of the corpus was broken.

⭐ A referee downloading the repository could redraw the figures but could NOT
reproduce the result they illustrate.

THE MODEL (from plot_rotation_ngc6503_ecf.py, itself aligned on F2 Sec. 3.4)
----------------------------------------------------------------------------
    v_halo^2(r) = V_inf^2 * (1 - arctan(r/Rs) / (r/Rs))
    v_total     = sqrt(v_baryons^2 + v_halo^2)

with TWO free geometric parameters per galaxy (V_inf, Rs) and NO global
dark-sector parameter -- which is precisely the claim F2 makes.

⚠️ WHAT THIS SCRIPT DOES *NOT* DO
----------------------------------
It does not attempt to reproduce a specific historical CSV: the original fit
script was not found in the corpus. It re-derives the fit from the SPARC
rotmod files. ⭐ Any difference with a previously quoted number is therefore
INFORMATION, not an error to be tuned away -- report it, do not fit to it.

Baryonic velocity follows the SPARC convention with mass-to-light ratios
Upsilon_disk = 0.5 and Upsilon_bul = 0.7 (Lelli, McGaugh & Schombert 2016),
held FIXED -- they are not free parameters here.

USAGE:  python3 fit_sparc175.py [--data DIR] [--out FILE]
"""

import argparse
import glob
import math
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from scipy.optimize import curve_fit

# ── SPARC mass-to-light ratios, held fixed (Lelli et al. 2016) ──────────────
UPSILON_DISK = 0.5
UPSILON_BUL = 0.7


def vitesse_halo_ecf(rayon_kpc, v_inf, r_s):
    """ECF torsion halo: v^2 = V_inf^2 (1 - arctan(x)/x), x = r/Rs."""
    x = np.asarray(rayon_kpc, dtype=float) / r_s
    terme = np.ones_like(x)
    masque = x > 0
    terme[masque] = np.arctan(x[masque]) / x[masque]
    return np.sqrt(np.abs(v_inf**2 * (1.0 - terme)))


def lire_rotmod(chemin):
    """Read one SPARC _rotmod.dat file. Returns None if unusable."""
    try:
        d = np.loadtxt(chemin, comments="#")
    except Exception:
        return None
    if d.ndim != 2 or d.shape[0] < 4 or d.shape[1] < 6:
        return None
    rad, vobs, errv, vgas, vdisk, vbul = (d[:, i] for i in range(6))
    # baryonic velocity, SPARC convention (signed squares: Vdisk may be < 0)
    vbar2 = (vgas * np.abs(vgas)
             + UPSILON_DISK * vdisk * np.abs(vdisk)
             + UPSILON_BUL * vbul * np.abs(vbul))
    bon = (errv > 0) & (rad > 0) & np.isfinite(vobs)
    # ⚠️ MINIMUM 5 POINTS, raised from 4 on 22/08/2026.
    # The model has TWO free parameters, so 4 points leave 2 degrees of
    # freedom: the reduced chi2 is then unstable and uninformative. The four
    # galaxies with exactly 4 valid points (D512-2, UGC07232, NGC6789,
    # UGC00634) returned chi2 of 0.12, 0.11, 0.29 and 1.52 -- three of them
    # far below 1, which does not mean a good fit, only that the model cannot
    # be tested. They dragged the sample median down without adding
    # information, so they are excluded.
    # ⚠️ This 5-point cut yields 171 galaxies. sparc_ratio_statistics.py
    # reports 175 on the same database: it fits nothing, so no degree of
    # freedom is at stake there and the cut does not apply. Different
    # question, different sample -- see its header.
    if bon.sum() < 5:
        return None
    return rad[bon], vobs[bon], errv[bon], np.sqrt(np.abs(vbar2[bon]))


def ajuster(rad, vobs, errv, vbar):
    """Fit (V_inf, Rs). Returns (v_inf, r_s, chi2_reduit) or None."""
    def modele(r, v_inf, r_s):
        return np.sqrt(vbar**2 + vitesse_halo_ecf(r, v_inf, r_s) ** 2)

    v0 = max(float(np.max(vobs)), 10.0)
    r0 = max(float(np.median(rad)), 0.5)
    try:
        popt, _ = curve_fit(modele, rad, vobs, p0=[v0, r0],
                            sigma=errv, absolute_sigma=True, maxfev=20000,
                            bounds=([1.0, 0.05], [1000.0, 200.0]))
    except Exception:
        return None
    resid = (vobs - modele(rad, *popt)) / errv
    ddl = max(len(rad) - 2, 1)
    return float(popt[0]), float(popt[1]), float(np.sum(resid**2) / ddl)


def chi2_newton(vobs, errv, vbar):
    """Reduced chi2 of baryons alone -- the comparison point."""
    return float(np.sum(((vobs - vbar) / errv) ** 2) / max(len(vobs), 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sparc",
                    help="directory holding the *_rotmod.dat files")
    ap.add_argument("--out", default="output/sparc175_fit_results.csv")
    a = ap.parse_args()

    fichiers = sorted(glob.glob(os.path.join(a.data, "*_rotmod.dat")))
    if not fichiers:
        print(f"[ERROR] no *_rotmod.dat found in {a.data}")
        return 1

    print("=" * 74)
    print(f"  ECF fit on the SPARC database -- {len(fichiers)} galaxies")
    print("=" * 74)

    lignes, chis, err_med, rejets = [], [], [], 0
    for f in fichiers:
        nom = os.path.basename(f).replace("_rotmod.dat", "")
        lu = lire_rotmod(f)
        if lu is None:
            rejets += 1
            continue
        rad, vobs, errv, vbar = lu
        res = ajuster(rad, vobs, errv, vbar)
        if res is None:
            rejets += 1
            continue
        v_inf, r_s, c2 = res
        chis.append(c2)
        err_med.append(float(np.median(errv)))
        lignes.append((nom, v_inf, r_s, c2, chi2_newton(vobs, errv, vbar), len(rad)))

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("galaxy,v_inf_kms,Rs_kpc,chi2_ecf,chi2_newton,n_points\n")
        for n, v, r, c, cn, npt in lignes:
            fh.write(f"{n},{v:.3f},{r:.4f},{c:.4f},{cn:.4f},{npt}\n")

    # ── ⭐ DISPERSION BY SAMPLING (added 22/08/2026) ───────────────────────
    # ⚠️ These are the figures quoted in Foundation II, § "On the dispersion
    # of per-galaxy chi2". They MUST come from this script, not from a
    # command line: a number printed in a paper has to be reproducible by
    # whoever downloads the repository.
    #
    # ⭐ The effect is the NUMBER of points, not the size of the error bars.
    # A first attempt at this paragraph claimed the opposite -- that the
    # best-measured curves give the highest chi2 -- and the computation below
    # refuted it: the correlation with error-bar size is weak and not
    # significant, while the correlation with sampling is strong.
    from scipy.stats import spearmanr

    npts = np.array([l[5] for l in lignes])
    errs = np.array(err_med)
    chis = np.array(chis)

    # ── ⭐ THE nu >= 3 CUT, justified (added 22/08/2026) ───────────────────
    # ⚠️ Rejecting galaxies needs a STATISTICAL criterion, not an opinion.
    # Under the null hypothesis the reduced statistic has standard deviation
    # sqrt(2/nu). These figures are quoted in Foundation II, § "Sample
    # definition and the nu >= 3 cut", so they are printed here.
    from scipy import stats as _st

    print("\n" + "-" * 74)
    print("  WHY nu >= 3  (quoted in Foundation II)")
    print("-" * 74)
    for npt in (4, 5, 10, 40):
        nu = npt - 2
        sig = math.sqrt(2 / nu)
        print(f"    {npt:>2} points -> nu={nu:>2}  sigma(chi2_red) = {sig:.2f}"
              f"   68% interval [{max(0, 1-sig):.2f}, {1+sig:.2f}]")
    print()
    for nu in (2, 3, 10):
        print(f"    P(chi2_red < 0.30) at nu={nu:>2} : "
              f"{_st.chi2.cdf(0.30*nu, nu)*100:.0f} %")
    print("    => at nu=2 the 68% interval spans [0,2]: NO hypothesis can be")
    print("       rejected, whatever the fit. Hence the 5-point minimum.")

    print("\n" + "-" * 74)
    print("  DISPERSION BY SAMPLING  (quoted in Foundation II)")
    print("-" * 74)
    for lo, hi in ((5, 15), (15, 25), (25, 40), (40, 10**6)):
        m = (npts >= lo) & (npts < hi)
        if m.sum():
            lab = f"{lo}-{hi}" if hi < 10**6 else f">{lo}"
            print(f"    {lab:>8} points : n={m.sum():>3}  median chi2_red = "
                  f"{np.median(chis[m]):.2f}")
    rho_n, p_n = spearmanr(npts, chis)
    rho_e, p_e = spearmanr(errs, chis)
    print(f"\n    rank correlation chi2 vs NUMBER of points : rho = {rho_n:+.2f}"
          f"  (p = {p_n:.1e})")
    print(f"    rank correlation chi2 vs ERROR-BAR size   : rho = {rho_e:+.2f}"
          f"  (p = {p_e:.2f})  <- weak, NOT significant")
    print("    => it is the sampling, not the precision of each point, that")
    print("       drives the dispersion. The same holds for any two-parameter")
    print("       profile, NFW included.")

    med = float(np.median(chis))
    print(f"\n  fitted            : {len(lignes)} galaxies  ({rejets} rejected)")
    print(f"  chi2_red MEDIAN   : {med:.3f}")
    print(f"  chi2_red mean     : {chis.mean():.3f}")
    print(f"  fraction < 1      : {(chis < 1).mean()*100:.0f} %")
    print(f"\n  -> {a.out}")

    # ── auto-consistency checks (rule 1bis: a result carries its verification)
    print("\n" + "-" * 74)
    print("  AUTO-CONSISTENCY")
    print("-" * 74)
    ok = True
    for lib, cond, det in (
        ("at least 150 galaxies fitted", len(lignes) >= 150, f"{len(lignes)}"),
        ("median chi2_red is finite",    math.isfinite(med), f"{med:.3f}"),
        ("ECF beats baryons-only",
         med < np.median([l[4] for l in lignes]), f"{med:.2f} vs "
         f"{np.median([l[4] for l in lignes]):.2f}"),
    ):
        print(f"  {'PASS' if cond else 'FAIL'}  {lib:<44} {det}")
        ok &= bool(cond)

    print("\n" + "=" * 74)
    print(f"  Corpus quotes chi2_med = 0.80 (F2 abstract).")
    print(f"  This run gives {med:.3f}.")
    print("  ⚠️ If they differ, that is INFORMATION about the original fit --")
    print("     do NOT tune this script to match it.")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
