#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script      : plot_scale_factor_comparison.py
Author      : Pascal Fichant
Description : 
    Compares the evolution of the scale factor a(t) (the "size" of the 
    universe) between the Standard Model (Lambda-CDM + Inflation) and 
    the ECF Model (Geometric Spin-Torsion Bounce).
    Demonstrates that the ECF universe reaches a macroscopic scale almost 
    instantaneously without needing the delayed standard inflation.
Output      : 'Fig_Scale_Factor_Comparison.png'
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Generating the Scale Factor (Universe Size) curve...")

    # ---------------------------------------------------
    # 1. TIME PARAMETERS
    # Logarithmic scale from 10^-44 s to 10^-30 s
    # ---------------------------------------------------
    t_log = np.linspace(-44, -30, 1000)
    t = 10**t_log

    # ---------------------------------------------------
    # 2. STANDARD MODEL (Lambda-CDM + Inflaton)
    # ---------------------------------------------------
    a_standard = np.zeros_like(t)

    # Key epochs for the standard model
    t_start_inf = 10**-36  # Start of standard inflation
    t_end_inf = 10**-32    # End of standard inflation

    # For a fair comparison, we fix the same final size at t = 10^-30 s
    a_final = 1e30 

    # Backward calculation: 
    # After inflation, radiation phase: a(t) is proportional to t^(1/2)
    a_end_inf = a_final * (t_end_inf / 10**-30)**0.5

    # During inflation, exponential expansion of ~60 e-folds (factor e^60)
    e_folds = 60
    a_start_inf = a_end_inf / np.exp(e_folds)

    # Fill the array for the standard curve
    for i, ti in enumerate(t):
        if ti < t_start_inf:
            # Pre-inflation (Radiation domination assumed)
            a_standard[i] = a_start_inf * (ti / t_start_inf)**0.5
        elif ti <= t_end_inf:
            # Inflation (Exponential growth)
            a_standard[i] = a_start_inf * np.exp(e_folds * (ti - t_start_inf) / (t_end_inf - t_start_inf))
        else:
            # Post-inflation (Return to Radiation domination)
            a_standard[i] = a_end_inf * (ti / t_end_inf)**0.5

    # ---------------------------------------------------
    # 3. ECF MODEL (Big Spin Bounce)
    # ---------------------------------------------------
    a_ecf = np.zeros_like(t)
    
    # Cartan time (end of the bounce geometric impulse)
    t_cartan = 10**-41

    # Backward calculation from the same final size a_final:
    # From t_cartan to the end, the universe is in the Stiff phase (w=1).
    # In the Stiff phase, the scale factor grows as t^(1/3).
    a_cartan = a_final * (t_cartan / 10**-30)**(1/3)
    
    # Minimum quantum size at the bounce (cannot be a pure zero singularity)
    a_min = 1e-5 

    # Fill the array for the ECF curve
    for i, ti in enumerate(t):
        if ti < t_cartan:
            # Colossal geometric impulse due to repulsive torsion
            # Rapid (cubic) interpolation between the minimum size and Cartan size
            a_ecf[i] = a_min + (a_cartan - a_min) * (ti / t_cartan)**3
        else:
            # Natural Stiff Era phase (gravitational braking)
            a_ecf[i] = a_cartan * (ti / t_cartan)**(1/3)

    # ---------------------------------------------------
    # 4. PLOT CREATION
    # ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Plot both models
    ax.plot(t, a_standard, label=r'Standard Inflation ($a(t)$)', color='blue', linestyle='--', linewidth=2.5)
    ax.plot(t, a_ecf, label=r'ECF Natural Bounce ($a(t)$)', color='red', linewidth=3)

    # Annotations: Cartan Time (ECF)
    ax.axvline(t_cartan, color='red', linestyle=':', alpha=0.5)
    ax.text(10**-41.2, 1e15, ' Cartan Time ($10^{-41}$ s)\n ECF Reaches Macro Scale', 
            color='red', fontsize=10, rotation=90, verticalalignment='center')

    # Annotations: Standard Inflation Period
    ax.axvspan(t_start_inf, t_end_inf, color='blue', alpha=0.1)
    ax.text(10**-34, 1e15, ' Delayed Standard Inflation', 
            color='blue', fontsize=10, rotation=90, verticalalignment='center')

    # Log-Log axis formatting
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(10**-44, 10**-30)

    # Titles and labels
    ax.set_xlabel('Cosmic Time (Seconds after Singularity/Bounce)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Scale Factor / "Size" of the Universe $a(t)$ (Normalized)', fontsize=12, fontweight='bold')
    ax.set_title('Evolution of Cosmic Size: ECF Model vs Standard Inflation', fontsize=14, fontweight='bold')

    # Grid and legend
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(loc='lower right', fontsize=11)

    # ---------------------------------------------------
    # 5. SAVE IMAGE
    # ---------------------------------------------------
    output_file = 'Fig_Scale_Factor_Comparison.png'
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Success! The image has been saved as: {output_file}")

if __name__ == "__main__":
    main()