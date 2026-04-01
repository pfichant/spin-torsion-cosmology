#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation I: The Metric Solution
Script      : plot_jwst_comparison.py
Author      : Pascal Fichant
Date        : February 2026
Description : 
    Generates a comparison plot of High-Redshift Bright Galaxies observed 
    by JWST (JADES, CEERS, etc.) against the theoretical maximum UV absolute 
    magnitude limits of the Standard Lambda-CDM model and the ECF model.
    
    It highlights how the ECF framework's "Structural Advantage" (provided 
    by the primordial Macro-Knot seeds) naturally accommodates these 
    exceptionally bright early galaxies, thereby resolving the JWST tension.

Output      : Figure_JWST_ECF_comparison.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# Set global font size for the plot
plt.rcParams.update({'font.size': 12})

def plot_jwst_comparison():
    print("Generating JWST High-Redshift Galaxies Comparison Plot...")
    
    # Redshift range from Cosmic Dawn to the Dark Ages
    z = np.linspace(8, 15, 100)
    
    # -----------------------------------------------------------------------
    # 1. THEORETICAL MODELS (Absolute UV Magnitude Limits)
    # -----------------------------------------------------------------------
    # Lambda-CDM Limit: The further back in time (higher z), the less time 
    # galaxies had to form. The maximum brightness limit drops (magnitude 
    # becomes more positive). Thus, the slope is POSITIVE.
    mag_lcdm = -22.0 + 0.8 * (z - 8) 
    
    # ECF Limit (Prediction): The primordial Macro-Knots (10^5 M_sun) provide 
    # a ~300 Myr structural head start. Galaxies can be much more massive 
    # (and therefore brighter) early in the universe.
    mag_ecf = -23.0 + 0.3 * (z - 8)

    # -----------------------------------------------------------------------
    # 2. OBSERVATIONAL DATA (Galaxies in "Tension")
    # -----------------------------------------------------------------------
    # Format: (Redshift z, Observed Absolute UV Magnitude)
    jwst_data = [
        (10.6, -21.5), # GN-z11
        (11.4, -20.3), # Maisie's Galaxy
        (12.4, -20.5), # GLASS-z12
        (13.2, -19.8), # JADES-GS-z13-0
        (14.3, -20.8)  # JADES-GS-z14-0 (The main crisis driver)
    ]
    z_obs, mag_obs = zip(*jwst_data)

    # -----------------------------------------------------------------------
    # 3. PLOTTING
    # -----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    # ECF Structural Advantage Zone (Pink Shading)
    ax.fill_between(z, mag_ecf, mag_lcdm, color='red', alpha=0.1, label='ECF Structural Advantage')

    # Boundary Curves
    ax.plot(z, mag_lcdm, 'b--', linewidth=2, label=r'$\Lambda$CDM Limit (Hierarchical)')
    ax.plot(z, mag_ecf, 'r-', linewidth=3, label='ECF Limit (Macro-Knot seeds)')

    # Data Points (Discovered Galaxies)
    ax.plot(z_obs, mag_obs, 'ks', markersize=8, label='JWST Discovered Galaxies')

    # Point Annotations
    annotations = ["GN-z11", "Maisie's", "GLASS-z12", "JADES-z13", "JADES-z14-0"]
    
    for (zx, my), txt in zip(jwst_data, annotations):
        # Text offset for better readability
        ax.text(zx + 0.15, my - 0.1, txt, fontsize=10, fontweight='bold')

    # -----------------------------------------------------------------------
    # 4. FORMATTING AND LAYOUT
    # -----------------------------------------------------------------------
    ax.set_xlabel(r'Redshift $z$', fontsize=14)
    ax.set_ylabel(r'UV Absolute Magnitude $M_{UV}$ (Brighter $\rightarrow$)', fontsize=14)
    ax.set_title('High-Redshift Bright Galaxies - JWST vs. ECF Model', fontsize=16, fontweight='bold')
    
    # Crucial in astronomy: negative values (brighter) must be at the top!
    ax.invert_yaxis() 
    
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Legend placement
    ax.legend(loc='lower left', framealpha=0.9)

    plt.tight_layout()
    plt.savefig('Figure_JWST_ECF_comparison.png', dpi=300)
    print("[SUCCESS] Figure_JWST_ECF_comparison.png saved.")

if __name__ == "__main__":
    plot_jwst_comparison()
    
