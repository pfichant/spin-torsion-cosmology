"""
generate_sparc175_mosaic.py
ECF Foundation II — Pascal Fichant, May 2026 v1.1.0

Downloads SPARC archive (Lelli+2016, Zenodo), fits ECF torsion-halo
to all 175 galaxies, saves mosaic + CSV.

Usage:
    python generate_sparc175_mosaic.py

Outputs:
    output/Fig_SPARC_175_Mosaic.png
    output/sparc175_fit_results.csv
"""

import os, io, hashlib, zipfile, warnings
import requests
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── CONFIG ────────────────────────────────────────────────────────────────────
SPARC_URL   = "http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip"
DATA_DIR    = Path("data/sparc")
OUTPUT_DIR  = Path("output")
MOSAIC_FILE = OUTPUT_DIR / "Fig_SPARC_175_Mosaic.png"
CSV_FILE    = OUTPUT_DIR / "sparc175_fit_results.csv"
ML_DISK     = 0.50
ML_BULGE    = 0.70
NCOLS       = 13
DPI         = 300
PANEL_W     = 2.2
PANEL_H     = 1.8

# ── PHYSICS ───────────────────────────────────────────────────────────────────
def v_ecf(r, v_inf, R_s):
    x   = np.where(r > 0, r / R_s, 1e-10)
    val = v_inf**2 * (1.0 - (1.0 / x) * np.arctan(x))
    return np.sqrt(np.abs(val))

def v_total(r, v_inf, R_s, v_bar):
    return np.sqrt(v_bar**2 + v_ecf(r, v_inf, R_s)**2)

# ── DOWNLOAD ──────────────────────────────────────────────────────────────────
def download_sparc():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive = DATA_DIR / "RotmodLTG.zip"
    if not archive.exists():
        print("Downloading SPARC archive from Zenodo ...")
        headers = {"User-Agent": "Mozilla/5.0 (ECF-Foundation-II/1.0)"}
        r = requests.get(SPARC_URL, headers=headers, timeout=60)
        r.raise_for_status()
        archive.write_bytes(r.content)
        sha = hashlib.sha256(r.content).hexdigest()
        print("  SHA-256: " + sha)
    else:
        print("SPARC archive already cached.")
    with zipfile.ZipFile(archive) as z:
        z.extractall(DATA_DIR)
    return archive

# ── LOAD ONE GALAXY ───────────────────────────────────────────────────────────
def load_galaxy(filepath):
    try:
        df = pd.read_csv(
            filepath, sep=r'\s+', comment='#',
            names=["Rad","Vobs","errV","Vgas","Vdisk","Vbul","SBdisk","SBbul"],
            usecols=[0,1,2,3,4,5]
        )
        df = df.dropna()
        df = df[(df["Rad"] > 0) & (df["errV"] > 0)]
        if len(df) < 4:
            return None
        df["Vbar"] = np.sqrt(
            df["Vgas"]**2
            + ML_DISK  * df["Vdisk"]**2
            + ML_BULGE * df["Vbul"]**2
        )
        return df
    except Exception:
        return None

# ── FIT ONE GALAXY ────────────────────────────────────────────────────────────
def fit_galaxy(df):
    r    = df["Rad"].values
    vobs = df["Vobs"].values
    verr = df["errV"].values
    vbar = df["Vbar"].values
    try:
        popt, _ = curve_fit(
            lambda x, vi, rs: v_total(x, vi, rs, np.interp(x, r, vbar)),
            r, vobs,
            p0=[vobs.max(), r.mean()],
            sigma=verr,
            bounds=([10.0, 0.1], [1000.0, 200.0]),
            maxfev=8000
        )
        v_inf, R_s = popt
        v_mod = v_total(r, v_inf, R_s, vbar)
        dof   = max(1, len(r) - 2)
        chi2_ecf    = np.sum(((vobs - v_mod) / verr)**2) / dof
        chi2_newton = np.sum(((vobs - vbar)  / verr)**2) / dof
        return v_inf, R_s, chi2_ecf, chi2_newton
    except Exception:
        return None

# ── MOSAIC ────────────────────────────────────────────────────────────────────
def make_mosaic(galaxies_data, results_df):
    n     = len(galaxies_data)
    nrows = int(np.ceil(n / NCOLS))
    fig, axes = plt.subplots(
        nrows, NCOLS,
        figsize=(PANEL_W * NCOLS, PANEL_H * nrows),
        facecolor="white"
    )
    axes = axes.flatten()

    for idx, (name, df, fit) in enumerate(galaxies_data):
        ax   = axes[idx]
        r    = df["Rad"].values
        vobs = df["Vobs"].values
        verr = df["errV"].values
        vbar = df["Vbar"].values

        ax.errorbar(r, vobs, yerr=verr, fmt="o", color="black",
                    ms=1.5, elinewidth=0.5, alpha=0.75)
        ax.plot(r, vbar, "--", color="#1f77b4", lw=0.8, alpha=0.8)

        if fit is not None:
            v_inf, R_s, chi2_ecf, _ = fit
            r_fine    = np.linspace(r.min(), r.max(), 300)
            vbar_fine = np.interp(r_fine, r, vbar)
            v_mod     = v_total(r_fine, v_inf, R_s, vbar_fine)
            ax.plot(r_fine, v_mod, "-", color="#d62728", lw=1.0)
            col = "green" if chi2_ecf < 1.5 else ("darkorange" if chi2_ecf < 3.0 else "red")
            title_str = name + "  x2=" + "{:.2f}".format(chi2_ecf)
            ax.set_title(title_str, fontsize=4.5, color=col, pad=1)
        else:
            ax.set_title(name + "  no fit", fontsize=4.5, color="gray", pad=1)

        ax.tick_params(labelsize=3.5, length=2, width=0.4)
        for sp in ax.spines.values():
            sp.set_linewidth(0.4)

    for idx in range(len(galaxies_data), len(axes)):
        axes[idx].axis("off")

    fig.text(0.5, 0.01, "Radius [kpc]", ha="center",
             fontsize=7, fontweight="bold")
    fig.text(0.01, 0.5, "V [km/s]", va="center",
             rotation="vertical", fontsize=7, fontweight="bold")

    med = results_df["chi2_ecf"].median()
    suptitle = (
        "ECF Torsion-Halo Fits - Full SPARC Sample (175 galaxies)  |  "
        + "Median chi2_red={:.2f}".format(med)
        + "  |  Black: data  Blue--: Newton  Red: ECF"
    )
    fig.suptitle(suptitle, fontsize=6, fontweight="bold", y=1.002)
    plt.tight_layout(rect=[0.02, 0.02, 1, 1], pad=0.3, h_pad=0.6, w_pad=0.3)
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.savefig(MOSAIC_FILE, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Mosaic saved: " + str(MOSAIC_FILE))

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    # MANUALLY download_sparc()

    rot_files = sorted(DATA_DIR.rglob("*_rotmod.dat"))
    if not rot_files:
        rot_files = sorted(DATA_DIR.rglob("*.dat"))
    print("Found {:d} rotation-curve files.".format(len(rot_files)))

    records       = []
    galaxies_data = []

    for fp in rot_files:
        name = fp.stem.replace("_rotmod", "").replace("_ROTMOD", "")
        df   = load_galaxy(fp)
        if df is None:
            continue
        fit = fit_galaxy(df)
        if fit is not None:
            v_inf, R_s, chi2_ecf, chi2_newton = fit
            records.append({
                "galaxy"      : name,
                "v_inf_kms"   : round(v_inf, 2),
                "R_s_kpc"     : round(R_s,   3),
                "chi2_ecf"    : round(chi2_ecf, 3),
                "chi2_newton" : round(chi2_newton, 3),
                "delta_chi2"  : round(chi2_newton - chi2_ecf, 3),
                "n_points"    : len(df)
            })
            galaxies_data.append((name, df, fit))
        else:
            records.append({
                "galaxy": name, "v_inf_kms": np.nan, "R_s_kpc": np.nan,
                "chi2_ecf": np.nan, "chi2_newton": np.nan,
                "delta_chi2": np.nan, "n_points": len(df)
            })
            galaxies_data.append((name, df, None))

    n_fitted = sum(1 for r in records if not np.isnan(r["chi2_ecf"]))
    print("Fitted: {:d} / {:d} galaxies".format(n_fitted, len(records)))

    # Sort by V_inf ascending (as stated in caption)
    galaxies_data.sort(key=lambda x: x[2][0] if x[2] is not None else 0)

    results_df = pd.DataFrame(records)
    results_df.to_csv(CSV_FILE, index=False)
    print("Results CSV: " + str(CSV_FILE))

    valid = results_df.dropna(subset=["chi2_ecf"])
    print("ECF  chi2_red  mean={:.3f}  median={:.3f}".format(
          valid["chi2_ecf"].mean(), valid["chi2_ecf"].median()))
    print("Newton chi2_red mean={:.3f}".format(valid["chi2_newton"].mean()))

    make_mosaic(galaxies_data, valid)
    print("Done.")

if __name__ == "__main__":
    main()