
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
# Grille 3x4 (suffisant pour 10 plots)
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
        ax.plot(r, v_bar, color='green', linestyle='--', label='Baryons')
        ax.plot(r, v_model, color='red', linewidth=2, label='ECF Fit')
        
        # Titre avec raw string (r"") pour éviter le warning SyntaxWarning
        ax.set_title(rf"{name} ($\chi^2_\nu={chi2_red:.2f}$)", fontsize=10)
        
        if i >= 6: ax.set_xlabel("Radius (kpc)") # Ajusté pour la grille
        if i % 4 == 0: ax.set_ylabel("Velocity (km/s)")
        
    except Exception as e:
        print(f"[FAIL] Fit failed for {name}: {e}")

# Masquer les axes vides (il y en a 2 maintenant: 10 plots sur 12 places)
for j in range(len(galaxy_targets), len(axes)):
    axes[j].axis('off')

axes[0].legend(loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('Fig_10_Galaxies_Analysis.png', dpi=300)
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
