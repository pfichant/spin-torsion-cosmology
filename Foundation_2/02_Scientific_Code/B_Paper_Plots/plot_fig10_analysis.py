
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
FILENAME       : plot_fig10_analysis.py
DESCRIPTION    : Statistical analysis of the ECF Torsion Halo model on a 
                 sample of 10 SPARC galaxies.
                 
                 The script performs the following tasks:
                 1. Loads .csv data files from the 'data/' directory.
                 2. Fits the ECF model (Rs, V_inf) to each galaxy.
                 3. Generates Figure 10 (a 2x5 grid of rotation curves).
                 4. Outputs the statistical summary table in LaTeX format.

DEPENDENCIES   : numpy, pandas, matplotlib, scipy
USAGE          : Ensure a folder named 'data' exists containing the 10 .csv files.
                 Run with: python plot_fig10_analysis.py
PROCESS:       : 1. Run generate_data_files.py (built 3 csv)
                 2. Run fetch_sparc_data.py (get 10 x galaxies *.csv data and save to /data folder)
                 3. Run plot_fig10_analysis.py (build Fig10.png)

=============================================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- CONFIGURATION ---
DATA_DIR = "data"
OUTPUT_IMG = "Fig_10_Galaxies_Analysis.png"

# Target List (Order of appearance in the grid)
TARGETS = [
    "NGC 6503", "NGC 3198", "NGC 2403", "NGC 2841", "NGC 2903", 
    "NGC 3521", "NGC 5055", "NGC 7331", "DDO 154", "NGC 7814"
]

# --- ECF MODEL FUNCTIONS ---
def ecf_halo(r, v_inf, rs):
    """ Calculates the ECF Torsion Halo velocity contribution. """
    term = np.zeros_like(r)
    mask = r > 0
    # Potential formula: V^2 = V_inf^2 * (1 - (Rs/r)*arctan(r/Rs))
    x = r[mask] / rs
    term[mask] = (1.0 / x) * np.arctan(x)
    return np.sqrt(np.abs(v_inf**2 * (1 - term)))

def total_velocity(r, v_inf, rs, v_bar):
    """ Total Velocity = sqrt(V_baryons^2 + V_halo^2) """
    v_h = ecf_halo(r, v_inf, rs)
    return np.sqrt(v_bar**2 + v_h**2)

# --- MAIN ANALYSIS ---
def main():
    # 1. Check Data Directory
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Directory '{DATA_DIR}' not found.")
        print("Please create a 'data' folder and place your 10 .csv files inside.")
        return

    # 2. Setup Figure (2x5 Grid)
    fig, axes = plt.subplots(2, 5, figsize=(18, 8))
    axes = axes.flatten()
    
    results_latex = [] # Stores rows for the LaTeX table
    chi2_sum = 0
    count = 0

    print(f"[INFO] Analyzing files in '{DATA_DIR}'...")

    for i, name in enumerate(TARGETS):
        ax = axes[i]
        filename = os.path.join(DATA_DIR, f"{name}.csv")
        
        # Handle missing files gracefully
        if not os.path.exists(filename):
            ax.text(0.5, 0.5, "File Not Found", ha='center')
            print(f"[WARN] Missing file: {filename}")
            continue

        # 3. Load Data
        try:
            df = pd.read_csv(filename, comment='#')
            # Normalize column names
            rename = {'Radius_kpc':'Radius','V_obs':'Vobs','V_err':'Verr','V_Newton':'Vbar','V_ECF':'Vecf'}
            df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
            # Flexible column mapping (handles 'Radius' vs 'Rad', 'Vobs' vs 'V_obs')
            cols = {c.lower(): c for c in df.columns}
            r = df[cols.get('radius', 'Radius')].values
            v_obs = df[cols.get('vobs', 'Vobs')].values
            v_err = df[cols.get('verr', 'Verr')].values
            v_bar = df[cols.get('vbar', 'Vbar')].values
        except Exception as e:
            print(f"[FAIL] Could not read {name}: {e}")
            continue

        # 4. Model Fitting (Curve Fit)
        # Initial Guess: V_inf ~ max(Vobs), Rs ~ 5 kpc
        p0 = [np.max(v_obs), 5.0]
        
        try:
            # We use lambda to pass v_bar as a fixed parameter
            popt, _ = curve_fit(lambda x, v, rs: total_velocity(x, v, rs, v_bar), 
                                r, v_obs, p0=p0, sigma=v_err, 
                                bounds=([0, 0.1], [1000, 100]))
            
            v_fit, rs_fit = popt
            
            # 5. Statistical Calculations
            v_model = total_velocity(r, v_fit, rs_fit, v_bar)
            
            # Reduced Chi-Squared
            chi2 = np.sum(((v_obs - v_model)/v_err)**2)
            dof = max(1, len(r) - 2)
            chi2_red = chi2 / dof
            
            # Significance (Comparison vs Newtonian-only model)
            chi2_newt = np.sum(((v_obs - v_bar)/v_err)**2)
            delta_chi2 = chi2_newt - chi2
            sigma_det = np.sqrt(max(0, delta_chi2))

            # Store results for Table
            # Cap at 99 for display — very large values reflect Newtonian-only baseline
            sig_str = f"{min(sigma_det, 99.9):.1f}"
            results_latex.append(f"{name} & {rs_fit:.2f} & {v_fit:.1f} & {chi2_red:.2f} & {sig_str} \\\\")
            
            chi2_sum += chi2_red
            count += 1

            # 6. Plotting
            # Data (Black dots)
            ax.errorbar(r, v_obs, yerr=v_err, fmt='o', color='black', 
                        ecolor='gray', ms=3, elinewidth=1, alpha=0.7, 
                        label='SPARC Data' if i==0 else "")
            
            # Baryons (Blue dotted line - Matches Fig 1 style)
            ax.plot(r, v_bar, ':', color='blue', lw=1.5, 
                    label='Newtonian (Baryons)' if i==0 else "")
            
            # ECF Fit (Red solid line)
            ax.plot(r, v_model, '-', color='red', lw=2.0, 
                    label='ECF Model' if i==0 else "")
            
            # Title with Chi2
            # Green if excellent (<1.5), Dark Red if poor (>5.0), Black otherwise
            col_tit = 'black'
            if chi2_red < 1.0: col_tit = 'green'
            elif chi2_red > 5.0: col_tit = 'darkred'
                
            ax.set_title(rf"{name} ($\chi^2_\nu={chi2_red:.2f}$)", fontsize=10, color=col_tit, fontweight='bold')
            ax.grid(True, linestyle=':', alpha=0.5)

            # Axis Labels (Only on outer edges to keep grid clean)
            if i >= 5: ax.set_xlabel("Radius [kpc]", fontsize=9)
            if i % 5 == 0: ax.set_ylabel("Velocity [km/s]", fontsize=9)

        except Exception as e:
            print(f"[FAIL] Fit failed for {name}: {e}")

    # --- FINALIZE FIGURE ---
    # Hide empty axes if any
    for j in range(len(TARGETS), len(axes)):
        axes[j].axis('off')

    # Global Legend
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, frameon=False, fontsize=11)
    
    # Global Title
    plt.suptitle("Figure 10: Universality of the ECF Torsion Halo (SPARC Sample Analysis)", 
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save Image
    plt.savefig(OUTPUT_IMG, dpi=300)
    print(f"\n[OK] Figure saved to: {OUTPUT_IMG}")

if __name__ == "__main__":
    main()
