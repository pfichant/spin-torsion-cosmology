#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Script      : plot_ecf_timeline.py
Description : Generates a visual infographic timeline of the ECF Chiral Universe
              from the Big Spin Bounce to present-day geometric halos.
Output      : Fig_ECF_Cosmic_Timeline.png
=============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np

def generate_timeline():
    print("Generating ECF Cosmic Timeline...")

    # Define the events (Time/Epoch, Title, Description)
    events = [
        ("t ~ 10^{-44} s\n(Planck Time)", "The Big Spin Bounce", "Singularity avoided via repulsive fermion spin-torsion."),
        ("t ~ 10^{-11} s\n(Electroweak)", "Topological Crystallization", "Kibble-Zurek freeze-out into 10^{24} kg Micro-Knots.\nChiral Baryogenesis creates matter surplus."),
        ("t ~ 1 s\n(Annihilation)", "Macro-Knot Freeze-Out", "Hierarchical merging halts at 10^5 M_sun.\nOnly the baryonic surplus survives."),
        ("t ~ 365,000 yr\n(Recombination)", "CMB Kinematic Imprint", "Residual Lense-Thirring twist imprints the CMB 'Axis of Evil'."),
        ("z ~ 30 to 10\n(Cosmic Dawn)", "JWST Heavy Seeds", "Macro-Knots act as early incubators. Accretion initiates at z~30."),
        ("z = 0\n(Present Day)", "Geometric Galactic Halos", "SPARC rotation curves driven by ECF topological defects.")
    ]

    # Plot settings
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    # Draw central timeline line
    y_positions = np.linspace(10, 1, len(events))
    ax.plot([0, 0], [0.5, 10.5], color='#2c3e50', lw=4, zorder=1)

    # Plot each event
    for i, (y, event) in enumerate(zip(y_positions, events)):
        time_text, title, desc = event
        
        # Draw dot on the timeline
        ax.scatter([0], [y], s=200, color='#e74c3c', edgecolor='#c0392b', zorder=2, lw=2)
        
        if i % 2 == 0:
            # TEXTE À DROITE
            # La date (texte bleu) est placée explicitement au-dessus de la boîte blanche (y + 0.45)
            ax.text(0.12, y + 0.45, f"{time_text}", fontsize=11, fontweight='bold', color='#2980b9', va='bottom', ha='left')
            
            # La boîte de titre (blanc) et la description
            bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="#bdc3c7", lw=1.5)
            ax.text(0.12, y, f"{title}\n", fontsize=13, fontweight='bold', va='center', ha='left', bbox=bbox_props)
            ax.text(0.12, y - 0.25, f"{desc}", fontsize=10, color='#34495e', va='top', ha='left')
            
            # Ligne pointillée
            ax.plot([0, 0.1], [y, y], color='#7f8c8d', lw=1.5, zorder=1, ls='--')
        else:
            # TEXTE À GAUCHE
            # La date (texte bleu) est placée explicitement au-dessus de la boîte blanche (y + 0.45)
            ax.text(-0.12, y + 0.45, f"{time_text}", fontsize=11, fontweight='bold', color='#2980b9', va='bottom', ha='right')
            
            # La boîte de titre (blanc) et la description
            bbox_props = dict(boxstyle="round,pad=0.5", fc="white", ec="#bdc3c7", lw=1.5)
            ax.text(-0.12, y, f"{title}\n", fontsize=13, fontweight='bold', va='center', ha='right', bbox=bbox_props)
            ax.text(-0.12, y - 0.25, f"{desc}", fontsize=10, color='#34495e', va='top', ha='right')
            
            # Ligne pointillée
            ax.plot([0, -0.1], [y, y], color='#7f8c8d', lw=1.5, zorder=1, ls='--')

    # Formatting (élargi pour s'assurer que tout rentre)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(0, 11)
    ax.axis('off')
    plt.title("Chronological Roadmap of the ECF Chiral Universe", fontsize=16, fontweight='bold', pad=20)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('Fig_ECF_Cosmic_Timeline.png', dpi=300, bbox_inches='tight')
    print("Saved timeline to 'Fig_ECF_Cosmic_Timeline.png'")

if __name__ == "__main__":
    generate_timeline()