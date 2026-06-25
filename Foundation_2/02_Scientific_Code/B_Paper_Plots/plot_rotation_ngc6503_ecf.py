#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_rotation_ngc6503_ecf.py
Author:        Pascal Fichant
Date:          February 2026 (v1.0.3 - Final)
Description:   Compares ECF Torsion-based rotation curves with SPARC data.
               Calculates Reduced Chi-Squared statistic.
Output:        Fig1_NGC6503_ECF_Rotation.png
=============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Nom du fichier de sortie
OUTPUT_FILE = "Fig1_NGC6503_ECF_Rotation.png"
DATA_FILE = "Data_S1_NGC6503_ECF.csv"

def main():
    # 1. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] Data file {DATA_FILE} not found.")
        return

    # Utilisation de comment='#' pour sauter les en-têtes texte
    df = pd.read_csv(DATA_FILE, comment='#')
    
    # Extraction des colonnes (Noms harmonisés avec Data_S1)
    cols = df.columns
    col_r = 'Radius_kpc' if 'Radius_kpc' in cols else 'Radius'
    col_vobs = 'V_obs' if 'V_obs' in cols else 'Vobs'
    col_verr = 'V_err' if 'V_err' in cols else 'Verr'
    col_vnewt = 'V_Newton' if 'V_Newton' in cols else 'Vbar'

    r = df[col_r].values
    v_obs = df[col_vobs].values
    v_err = df[col_verr].values
    v_newt = df[col_vnewt].values

    # 2. ECF Model Definition (Mise à jour v1.0.3)
    # ============================================
    # Alignement avec Table 4 et Section 3.4
    Rs_best = 1.70            # kpc
    V_inf_best = 114.0        # km/s
    
    def vel_halo_ecf(radius_kpc):
        """ Vitesse induite par le Halo Torsion ECF """
        term = np.zeros_like(radius_kpc)
        mask = radius_kpc > 0
        x = radius_kpc[mask] / Rs_best
        # Formule du potentiel ECF (dérivée de la force)
        term[mask] = (1.0 / x) * np.arctan(x)
        v_sq = V_inf_best**2 * (1 - term)
        return np.sqrt(np.abs(v_sq))

    v_halo = vel_halo_ecf(r)
    
    # Vitesse Totale = sqrt(V_baryons^2 + V_halo^2)
    v_ecf = np.sqrt(v_newt**2 + v_halo**2)

    # 3. Statistics
    chi2 = np.sum(((v_obs - v_ecf) / v_err)**2)
    dof = len(df) - 2 # 2 paramètres libres
    chi2_red = chi2 / dof
    print(f"[INFO] NGC 6503: Reduced Chi2 = {chi2_red:.4f}")

    # 4. Plotting
    plt.figure(figsize=(10, 7))
    
    # Observed Data (SPARC)
    plt.errorbar(r, v_obs, yerr=v_err, fmt='o', color='black', 
                 ecolor='gray', elinewidth=1, capsize=2, label='SPARC Data (NGC 6503)')

    # Newtonian Prediction (Baryons only)
    plt.plot(r, v_newt, '--', color='blue', linewidth=2, label='Newtonian (Stars+Gas)')

    # ECF Prediction (Total)
    plt.plot(r, v_ecf, '-', color='red', linewidth=3, label='ECF Geometric DM')

    # Formatting
    plt.title("Galaxy Rotation Curve: NGC 6503 (ECF Model)", fontsize=16, fontweight='bold')
    plt.xlabel("Radius [kpc]", fontsize=14)
    plt.ylabel("Velocity [km/s]", fontsize=14)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12, loc='lower right')
    
    # 5. Annotation Box (Utilisation de raw strings r"" pour le LaTeX)
    stats_text = (f"Fit Quality:\n"
                  r"$\chi^2_\nu$ = " + f"{chi2_red:.2f}\n"
                  fr"$R_s = {Rs_best}$ kpc" "\n"
                  fr"$V_\infty = {V_inf_best}$ km/s")
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red')
    plt.text(0.02, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"[OK] Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()