#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script Name : plot_inflation_comparison.py
Author      : Pascal Fichant
Description : 
    Plots the cosmic acceleration (a'') and scale factor (a) comparing the 
    Standard Inflationary Model (Guth, scalar field) vs the ECF Geometric 
    Bounce Model (Spin-Torsion repulsion).
    Highlights the "Graceful Exit" naturally present in the ECF model.
Output      : 'Fig_Inflation_Acceleration_Comparison.png'
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Starting Cosmic Acceleration Simulation (ECF vs Standard Inflation)...")
    
    # ---------------------------------------------------
    # 1. PARAMÈTRES DE TEMPS (Échelle Logarithmique en secondes)
    # Modelled from 10^-45 s to 10^-30 s
    # ---------------------------------------------------
    t_log = np.linspace(-44, -30, 1000)
    t = 10**t_log
    
    # ---------------------------------------------------
    # 2. MODÈLE STANDARD (Lambda-CDM + Inflaton)
    # - Before 10^-36 s: radiation, a ~ t^(1/2) -> negative acceleration
    # - 10^-36 s to 10^-32 s: inflation, a ~ e^(Ht) -> large positive constante
    # - After 10^-32 s: radiation, a ~ t^(1/2) -> negative acceleration
    # ---------------------------------------------------
    accel_standard = np.zeros_like(t)
    
    # Time masks for the standard model
    mask_pre_inf = t < 10**-36
    mask_inf = (t >= 10**-36) & (t <= 10**-32)
    mask_post_inf = t > 10**-32
    
    # Normalised illustrative values, for display only
    accel_standard[mask_pre_inf] = -1e5 
    # The standard inflation plateau (constant)
    accel_standard[mask_inf] = 1e12 
    accel_standard[mask_post_inf] = -1e4 
    
    # ---------------------------------------------------
    # 3. MODÈLE ECF (Big Spin Bounce)
    # The acceleration follows the (rho - rho^2/rho_c) term
    # - Maximum absolu au rebond (t ~ 10^-43)
    # - Steep fall-off with the a^-6 dilution
    # - Turns negative (deceleration) naturally (stiff era)
    # ---------------------------------------------------
    t_cartan = 10**-41  # Fin de la domination du spin
    
    # Conceptual form of the ECF bounce acceleration (decaying Gaussian peak)
    # which then decelerates naturally
    accel_ecf = 5e13 * np.exp(- (t / (10**-43))**0.5 ) - 2e5
    
    # ---------------------------------------------------
    # 4. CRÉATION DU GRAPHIQUE
    # ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Plot the accelerations
    ax.plot(t, accel_standard, label=r'Standard Inflation ($\Lambda$CDM + Inflaton)', 
             color='blue', linestyle='--', linewidth=2.5)
    
    ax.plot(t, accel_ecf, label=r'ECF Natural Bounce (Spin-Torsion)', 
             color='red', linewidth=3)
    
    # Zero line (boundary between acceleration and deceleration)
    ax.axhline(0, color='black', linewidth=1.2, linestyle='-')
    
    # Solve for the exact point where the ECF curve crosses zero
    zero_cross_idx = np.where(accel_ecf < 0)[0][0]
    t_zero_cross = t[zero_cross_idx]

    # Highlight the graceful exit of the ECF
    ax.annotate('ECF Natural Graceful Exit', 
                xy=(t_zero_cross, 0),          # Pointe EXACTEMENT sur le croisement zéro
                xytext=(10**-38, 1e7),         # Texte placé au-dessus et à droite
                arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                fontsize=11, color='red', fontweight='bold')
    
    # Highlight the end of standard inflation
    ax.annotate('Standard Reheating Exit\n(Abrupt Drop)', 
                xy=(10**-32, 1e12),            # Pointe EXACTEMENT sur la chute de l'inflaton
                xytext=(10**-31, 1e9),         # Texte placé en dessous et à droite
                arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5, headwidth=8),
                fontsize=11, color='blue', fontweight='bold')

    # Key time markers
    ax.axvline(10**-41, color='grey', linestyle=':', alpha=0.7)
    ax.text(10**-41, 1e11, ' Cartan Time\n (ECF Stiff Era Starts)', color='grey', fontsize=9, rotation=90, verticalalignment='center')

    # Axis formatting
    ax.set_xscale('log')
    # Asymmetric pseudo-log scale, to show both the extreme positive and the negative
    ax.set_yscale('symlog', linthresh=1e6) 
    
    ax.set_xlim(10**-44, 10**-30)
    ax.set_ylim(-1e7, 1e14)
    
    ax.set_xlabel('Cosmic Time (Seconds after Singularity/Bounce)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Cosmic Acceleration $\ddot{a}$ (Normalized)', fontsize=12, fontweight='bold')
    ax.set_title('Early Universe Acceleration: ECF Model vs Standard Inflation', fontsize=14, fontweight='bold')
    
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(loc='upper right', fontsize=11)
    
    # ---------------------------------------------------
    # 5. SAUVEGARDE
    # ---------------------------------------------------
    output_filename = 'Fig_Inflation_Acceleration_Comparison.png'
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"Success! Plot saved as: {output_filename}")

if __name__ == "__main__":
    main()
