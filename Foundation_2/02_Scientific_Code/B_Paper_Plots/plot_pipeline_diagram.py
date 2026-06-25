#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_pipeline_diagram_v2.py
Author:        Pascal Fichant
Date:          February 2026
Description:   Generates the UPDATED Data Processing Pipeline (Fig S1).
               Reflects the full scope: Galaxies, Baryogenesis, and Rotation.
Output:        FigS1_Data_Pipeline.png
=============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_FILE = "FigS1_Data_Pipeline.png"

def draw_box(ax, x, y, width, height, text, color='#E0E0E0', edge='black', fontsize=9):
    # Draw rectangle with rounded corners
    rect = patches.FancyBboxPatch((x, y), width, height, 
                                  boxstyle="round,pad=0.1", 
                                  linewidth=1.5, edgecolor=edge, facecolor=color)
    ax.add_patch(rect)
    # Add text centered
    ax.text(x + width/2, y + height/2, text, 
            ha='center', va='center', fontsize=fontsize, fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color='gray'):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=2, color=color))

def main():
    # Setup Figure
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # ==============================
    # COLUMN 1: INPUTS (Sources)
    # ==============================
    draw_box(ax, 0.5, 5.5, 2.5, 1.0, "OBSERVATIONAL DATA\n------------------\n- SPARC (Rotation)\n- Planck 2018 (CMB)\n- BBN Constraints", color='#FFD700') # Gold
    
    draw_box(ax, 0.5, 3.5, 2.5, 1.0, "THEORETICAL INPUTS\n------------------\n- ECF Lagrangian\n- Standard Model Params\n(alpha_W, g*)", color='#FFD700') 

    # ==============================
    # COLUMN 2: CORE MODULES (The Brain)
    # ==============================
    
    # Module A: Galactic Dynamics
    draw_box(ax, 4.5, 5.0, 3.0, 1.5, "MODULE A: GALACTIC DYNAMICS\n(Stiff Fluid & Torsion Halo)\n------------------\n- Solve Geodesics\n- MCMC Parameter Est.\n- Chi-Squared Minimization", color='#FF6347') # Tomato Red
    
    # Module B: Cosmic History
    draw_box(ax, 4.5, 2.0, 3.0, 1.5, "MODULE B: COSMIC HISTORY\n(Thermodynamics)\n------------------\n- Baryogenesis (Calc eta)\n- Rotation Evolution w(z)\n- Dilution Factors", color='#FF6347') # Tomato Red

    # ==============================
    # COLUMN 3: OUTPUTS (Validation)
    # ==============================
    
    # Galactic Outputs
    draw_box(ax, 9.0, 6.2, 2.5, 0.6, "Fig 1: Rotation Curve\n(Chi2 Validation)", color='#90EE90') # Light Green
    draw_box(ax, 9.0, 5.3, 2.5, 0.6, "Fig 7: MCMC Corner Plot\n(Parameter Constraints)", color='#90EE90')
    draw_box(ax, 9.0, 4.4, 2.5, 0.6, "Fig New: Radial Mass Ratio\n(Dark Matter vs Baryons)", color='#90EE90')
    
    # Cosmic Outputs
    draw_box(ax, 9.0, 3.0, 2.5, 0.6, "Fig 5: Rotation History\n(Geometric Transition)", color='#90EE90')
    draw_box(ax, 9.0, 2.1, 2.5, 0.6, "Fig 3: Axis of Evil\n(Multipole Alignment)", color='#90EE90')
    draw_box(ax, 9.0, 1.2, 2.5, 0.6, "App E: Baryon Ratio\n(eta ~ 6e-10)", color='#90EE90')

    # ==============================
    # CONNECTIONS (Arrows)
    # ==============================
    
    # Inputs -> Module A (Galactic)
    draw_arrow(ax, 3.1, 6.0, 4.4, 5.75) # SPARC -> Galactic
    
    # Inputs -> Module B (Cosmic)
    draw_arrow(ax, 3.1, 6.0, 4.4, 2.75) # Planck -> Cosmic
    draw_arrow(ax, 3.1, 4.0, 4.4, 2.75) # Theory -> Cosmic
    
    # Module A -> Outputs
    draw_arrow(ax, 7.6, 5.75, 8.9, 6.5) # -> Rotation
    draw_arrow(ax, 7.6, 5.75, 8.9, 5.6) # -> MCMC
    draw_arrow(ax, 7.6, 5.75, 8.9, 4.7) # -> Mass Ratio
    
    # Module B -> Outputs
    draw_arrow(ax, 7.6, 2.75, 8.9, 3.3) # -> Rotation History
    draw_arrow(ax, 7.6, 2.75, 8.9, 2.4) # -> Axis of Evil
    draw_arrow(ax, 7.6, 2.75, 8.9, 1.5) # -> Baryogenesis

    # ==============================
    # TITLE & LABELS
    # ==============================
    ax.text(6, 7.5, "Figure S1: Unified Data Processing Pipeline", ha='center', fontsize=16, fontweight='bold')
    ax.text(1.7, 7.0, "STEP 1: INPUTS", ha='center', fontsize=12, fontweight='bold', color='gray')
    ax.text(6.0, 7.0, "STEP 2: ECF CORE MODEL", ha='center', fontsize=12, fontweight='bold', color='gray')
    ax.text(10.2, 7.0, "STEP 3: VALIDATION", ha='center', fontsize=12, fontweight='bold', color='gray')

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"[OK] Diagram successfully updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
