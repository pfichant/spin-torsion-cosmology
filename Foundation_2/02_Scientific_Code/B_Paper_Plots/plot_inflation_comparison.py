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
    # On modélise de 10^-45 s à 10^-30 s
    # ---------------------------------------------------
    t_log = np.linspace(-44, -30, 1000)
    t = 10**t_log
    
    # ---------------------------------------------------
    # 2. MODÈLE STANDARD (Lambda-CDM + Inflaton)
    # - Avant 10^-36s : Radiation a ~ t^(1/2) -> Accélération négative
    # - 10^-36s à 10^-32s : Inflation a ~ e^(Ht) -> Accélération positive massive et constante
    # - Après 10^-32s : Radiation a ~ t^(1/2) -> Accélération négative
    # ---------------------------------------------------
    accel_standard = np.zeros_like(t)
    
    # Masques temporels pour le modèle standard
    mask_pre_inf = t < 10**-36
    mask_inf = (t >= 10**-36) & (t <= 10**-32)
    mask_post_inf = t > 10**-32
    
    # Valeurs conceptuelles normalisées pour la visualisation
    accel_standard[mask_pre_inf] = -1e5 
    # Le plateau d'inflation standard (constant)
    accel_standard[mask_inf] = 1e12 
    accel_standard[mask_post_inf] = -1e4 
    
    # ---------------------------------------------------
    # 3. MODÈLE ECF (Big Spin Bounce)
    # L'accélération dépend du terme (rho - rho^2/rho_c)
    # - Maximum absolu au rebond (t ~ 10^-43)
    # - Chute drastique avec la dilution a^-6
    # - Devient négative (décélération) naturellement (Stiff era)
    # ---------------------------------------------------
    t_cartan = 10**-41  # Fin de la domination du spin
    
    # Formule conceptuelle de l'accélération du rebond ECF (pic gaussien décroissant)
    # qui passe en décélération naturelle
    accel_ecf = 5e13 * np.exp(- (t / (10**-43))**0.5 ) - 2e5
    
    # ---------------------------------------------------
    # 4. CRÉATION DU GRAPHIQUE
    # ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Tracé des accélérations
    ax.plot(t, accel_standard, label=r'Standard Inflation ($\Lambda$CDM + Inflaton)', 
             color='blue', linestyle='--', linewidth=2.5)
    
    ax.plot(t, accel_ecf, label=r'ECF Natural Bounce (Spin-Torsion)', 
             color='red', linewidth=3)
    
    # Ligne Zéro (Frontière entre Accélération et Décélération)
    ax.axhline(0, color='black', linewidth=1.2, linestyle='-')
    
    # Recherche mathématique du point exact où l'ECF croise la ligne zéro
    zero_cross_idx = np.where(accel_ecf < 0)[0][0]
    t_zero_cross = t[zero_cross_idx]

    # Mise en évidence de la sortie gracieuse de l'ECF
    ax.annotate('ECF Natural Graceful Exit', 
                xy=(t_zero_cross, 0),          # Pointe EXACTEMENT sur le croisement zéro
                xytext=(10**-38, 1e7),         # Texte placé au-dessus et à droite
                arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                fontsize=11, color='red', fontweight='bold')
    
    # Mise en évidence de la fin de l'inflation standard
    ax.annotate('Standard Reheating Exit\n(Abrupt Drop)', 
                xy=(10**-32, 1e12),            # Pointe EXACTEMENT sur la chute de l'inflaton
                xytext=(10**-31, 1e9),         # Texte placé en dessous et à droite
                arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5, headwidth=8),
                fontsize=11, color='blue', fontweight='bold')

    # Lignes temporelles importantes
    ax.axvline(10**-41, color='grey', linestyle=':', alpha=0.7)
    ax.text(10**-41, 1e11, ' Cartan Time\n (ECF Stiff Era Starts)', color='grey', fontsize=9, rotation=90, verticalalignment='center')

    # Formatage des axes
    ax.set_xscale('log')
    # Échelle asymétrique pseudo-log pour montrer le positif extrême et le négatif
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
