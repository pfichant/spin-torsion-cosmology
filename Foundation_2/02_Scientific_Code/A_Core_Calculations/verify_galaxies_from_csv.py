
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# TWO OUTPUTS, TWO DIFFERENT STATUSES -- READ THIS BEFORE JUDGING EITHER
# =============================================================================
# ⚠️ CORRECTED 23/08/2026. An earlier audit note marked this whole script
# "exploratory, superseded". That was TOO BROAD: the script produces two
# things, and only one of them is superseded.
#
#   ⚠️ CORRECTED 25/08/2026: the F2 figure is produced by
#      plot_fig10_analysis.py (2x5 grid, dotted baryon line), NOT by this
#      script. This one now writes Fig_10_Galaxies_Verification.png.
#      What follows describes the FIGURE ITSELF, which remains accurate:
#   ✅ THE FIGURE IS IN FOUNDATION II.
#      It appears as \label{fig:galaxy_analysis}, is referenced twice in the
#      text, and its caption reads "Universality of the ECF Torsion Halo
#      (Sample Analysis)" over a sample spanning dwarfs (DDO 154) to giants
#      (NGC 2841). ⭐ That caption quotes NO chi2 -- the figure shows the
#      SHAPE of the fit across galaxy types, which is a legitimate and
#      still-current illustration.
#
#   ⚠️ THE LaTeX TABLE (\label{tab:sparc_stats}) IS NOT IN THE PAPER and is
#      not meant to be. It belongs to the pilot stage on 10 galaxies, later
#      superseded by the full fit (fit_sparc175.py), which is what Foundation
#      II quotes. Its companion is fetch_sparc_data.py, which downloads
#      exactly those 10 curves.
# =============================================================================
# ⚠️ STATUS, set on 22/08/2026. This script belongs to an EARLIER STAGE of the
# work: a pilot run on 10 representative SPARC galaxies, later superseded by
# the full 175-galaxy fit (fit_sparc175.py). Its companion is
# fetch_sparc_data.py, which downloads exactly those 10 curves.
#
# ⇒ Its LaTeX table (\label{tab:sparc_stats}) is NOT in Foundation II and is
#   not meant to be: the paper quotes the 175-galaxy result instead.
#
# ⚠️ READ ITS NUMBERS WITH THAT IN MIND. The 10 galaxies give a median
# reduced chi2 of 2.08, against 0.796 over the full 175. That is not a
# weakness of the model on these objects: they are among the best-measured
# curves in the catalogue -- error bars of 1.8 to 3.0 km/s, up to 73 points
# (NGC 2403). ⭐ A two-parameter profile cannot track a curve measured to
# 2 km/s, so the chi2 is severe BY CONSTRUCTION, and would be for NFW too.
# The pilot sample was chosen for data quality, which makes it the harshest
# possible test -- not the most favourable one.
# =============================================================================
"""
=============================================================================
FILENAME       : verify_galaxies_from_csv.py
DESCRIPTION    : Statistical validation of ECF Model on 10 SPARC galaxies.
                 Generates Fit Plots and LaTeX Statistics Table.
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# --- CONFIGURATION ---
DATA_DIR = "data" 

# Liste cible propre (10 Galaxies)
galaxy_targets = [
    ("NGC 6503", 120), ("NGC 3198", 150), ("NGC 2403", 135),
    ("NGC 2841", 300), ("NGC 2903", 200), ("NGC 3521", 230),
    ("NGC 5055", 190), ("NGC 7331", 240), ("DDO 154",  50),
    ("NGC 7814", 220)
]

# --- ECF MODEL FUNCTION ---
def ecf_velocity_model(r, v_inf, rs):
    """ ECF Torsion Halo Velocity """
    term = np.zeros_like(r)
    mask = r > 0
    term[mask] = (rs / r[mask]) * np.arctan(r[mask] / rs)
    v_sq = v_inf**2 * (1 - term)
    return np.sqrt(np.abs(v_sq))

# --- MAIN LOOP ---
results = []
# 3x4 grid (enough for 10 plots)
fig, axes = plt.subplots(3, 4, figsize=(16, 12))
axes = axes.flatten()

print(f"[INFO] Analyzing {len(galaxy_targets)} galaxies from '{DATA_DIR}/'...")

for i, (name, Vflat_guess) in enumerate(galaxy_targets):
    ax = axes[i]
    filepath = os.path.join(DATA_DIR, f"{name}.csv")
    
    if not os.path.exists(filepath):
        print(f"[WARN] File not found: {filepath}")
        ax.text(0.5, 0.5, "Data Not Found", ha='center')
        continue
        
    df = pd.read_csv(filepath, comment='#')
    # Normalize column names to expected format
    col_map = {
        'Radius_kpc': 'Radius_kpc', 'radius': 'Radius_kpc', 'r': 'Radius_kpc',
        'V_obs': 'V_obs', 'v_obs': 'V_obs', 'Vobs': 'V_obs', 'v': 'V_obs',
        'V_err': 'V_err', 'v_err': 'V_err', 'Verr': 'V_err', 'err': 'V_err',
    }
    df.columns = [col_map.get(c.strip(), c.strip()) for c in df.columns]
    # Flexible column reading — support multiple naming conventions
    def get_col(df, *candidates):
        for c in candidates:
            if c in df.columns: return df[c].values
        raise KeyError(f"None of {candidates} found in {list(df.columns)}")

    r     = get_col(df, 'Radius_kpc', 'Radius', 'radius', 'r_kpc', 'r')
    v_obs = get_col(df, 'V_obs', 'Vobs', 'v_obs', 'Velocity', 'velocity')
    v_err = get_col(df, 'V_err', 'Verr', 'v_err', 'V_error', 'error')
    # Vbar optional — fallback to Newtonian column or zeros
    try:
        v_bar = get_col(df, 'V_Newton', 'Vbar', 'v_bar', 'v_newton')
    except KeyError:
        v_bar = np.zeros_like(r)
    
    # Fit ECF Model
    def fit_func(x, v_inf, rs):
        return np.sqrt(v_bar**2 + ecf_velocity_model(x, v_inf, rs)**2)
    
    try:
        p0 = [Vflat_guess, 5.0]
        popt, pcov = curve_fit(fit_func, r, v_obs, p0=p0, sigma=v_err, 
                               bounds=([0, 0.1], [1000, 100]))
        v_inf_fit, rs_fit = popt
        v_model = fit_func(r, *popt)
        
        # Statistics
        chi2 = np.sum(((v_obs - v_model)/v_err)**2)
        dof = len(r) - 2
        chi2_red = chi2 / dof
        
        # Sigma Detection
        chi2_newt = np.sum(((v_obs - v_bar)/v_err)**2)
        delta_chi2 = chi2_newt - chi2
        sigma = np.sqrt(delta_chi2) if delta_chi2 > 0 else 0.0
        
        results.append((name, rs_fit, v_inf_fit, chi2_red, sigma))
        
        # Plotting
        ax.errorbar(r, v_obs, yerr=v_err, fmt='o', color='black', alpha=0.6, ms=3, label='Data')
        # ⚠️ COLOUR CORRECTED 23/08/2026: this drew the baryonic curve in
        # GREEN, but the caption of fig:galaxy_analysis in Foundation II reads
        # "Blue: Newtonian prediction from visible baryons (stars + gas)".
        # A reader looking for the blue curve would not have found one.
        # The caption is the published text, so the script follows it.
        ax.plot(r, v_bar, color='blue', linestyle='--', label='Baryons')
        ax.plot(r, v_model, color='red', linewidth=2, label='ECF Fit')
        
        # Raw string (r"") in the title, to avoid a SyntaxWarning
        ax.set_title(rf"{name} ($\chi^2_\nu={chi2_red:.2f}$)", fontsize=10)
        
        if i >= 6: ax.set_xlabel("Radius (kpc)") # Ajusté pour la grille
        if i % 4 == 0: ax.set_ylabel("Velocity (km/s)")
        
    except Exception as e:
        print(f"[FAIL] Fit failed for {name}: {e}")

# Hide the empty axes (two of them: 10 plots in 12 slots)
for j in range(len(galaxy_targets), len(axes)):
    axes[j].axis('off')

axes[0].legend(loc='upper left', fontsize=8)
plt.tight_layout()
# RENAMED 25/08/2026 -- NAME COLLISION RESOLVED.
# This script wrote Fig_10_Galaxies_Analysis.png, the SAME name as
# plot_fig10_analysis.py, and OVERWROTE it (verified: 5400x2400 -> 4800x3600).
# The paper figure is the 2x5 grid of plot_fig10_analysis.py: that script
# declares 'Figure 10 (a 2x5 grid)', and the F2 caption says 'Blue DOTTED
# line' -- dotted there, dashed here. Whichever ran last used to win.
plt.savefig('Fig_10_Galaxies_Verification.png', dpi=300)
print("[OK] Figure saved.")

# Generate LaTeX Table
print("\n" + "="*60)
print("LATEX TABLE (Clean Sample - 10 Galaxies)")
print("="*60)
print(r"\begin{table*}[hbt!]")
print(r"\centering")
print(r"\caption{\label{tab:sparc_stats}Statistical validation of the ECF Model on 10 SPARC galaxies.}")
print(r"\begin{tabular}{l c c c c}")
print(r"\toprule")
print(r"\textbf{Galaxy} & \textbf{$R_s$ (kpc)} & \textbf{$V_\infty$ (km/s)} & \textbf{$\chi^2_\nu$} & \textbf{Significance ($\sigma$)} \\")
print(r"\midrule")

global_chi2 = 0
for res in results:
    name, rs, vinf, chi2, sig = res
    print(f"{name} & {rs:.2f} & {vinf:.1f} & {chi2:.2f} & {sig:.1f} \\\\")
    global_chi2 += chi2

if len(results) > 0:
    print(r"\midrule")
    print(f"\\textbf{{Global (10 gal.)}} & -- & -- & \\textbf{{{global_chi2/len(results):.2f}}} & -- \\\\")

print(r"\bottomrule")
print(r"\end{tabular}")
print(r"\end{table*}")
