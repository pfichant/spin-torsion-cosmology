#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : plot_act2_annihilation_v2.py
Description : Generates a visual representation of Act II: 
              The Great Annihilation and Freeze-Out, highlighting the 
              dual population of surviving Macro-Knots and ubiquitous Micro-Knots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch
import matplotlib.patches as patches

def generate_act2_plot():
    print("Generating Act II (v2): Bimodal Dark Matter Spectrum plot...")
    np.random.seed(101)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), facecolor='white')
    fig.suptitle('Act II: The Great Annihilation & Bimodal Topological Freeze-Out', fontsize=18, fontweight='bold', y=0.98)

    # ==========================================
    # LEFT PLOT: Pre-Annihilation (Dense Plasma)
    # ==========================================
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_facecolor('#ffe6e6') # Light red/hot background
    
    # Generate dense plasma (Matter + Antimatter)
    matter_x, matter_y = np.random.rand(150)*10, np.random.rand(150)*10
    anti_x, anti_y = np.random.rand(150)*10, np.random.rand(150)*10
    
    ax1.scatter(matter_x, matter_y, c='blue', s=15, alpha=0.6, label='Matter ($e^-$)')
    ax1.scatter(anti_x, anti_y, c='red', s=15, alpha=0.6, label='Antimatter ($e^+$)')
    
    # Draw Merging Knots (intermediate mass)
    knot_centers = [(3, 7), (4.5, 6.5), (7, 3), (8, 4.5)]
    for cx, cy in knot_centers:
        ax1.add_patch(Circle((cx, cy), 0.8, color='black', alpha=0.8))
        
    # Draw merging arrows
    ax1.annotate('', xy=(3.8, 6.7), xytext=(3, 7), arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax1.annotate('', xy=(3.8, 6.7), xytext=(4.5, 6.5), arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax1.annotate('', xy=(7.5, 3.8), xytext=(7, 3), arrowprops=dict(arrowstyle="->", color="black", lw=2))
    ax1.annotate('', xy=(7.5, 3.8), xytext=(8, 4.5), arrowprops=dict(arrowstyle="->", color="black", lw=2))

    ax1.set_title(r"1. Hierarchical Merging ($t < 1$ s)" + "\nDense $e^+e^-$ Plasma & High Friction", fontsize=14, pad=15)
    # Add label for active knots manually to legend
    ax1.scatter([], [], c='black', s=80, alpha=0.8, label='Active Merging Knots')
    ax1.legend(loc='upper left', fontsize=10)
    ax1.axis('off')

    # ==========================================
    # RIGHT PLOT: Post-Annihilation (Bimodal Freeze-Out)
    # ==========================================
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_facecolor('#f0f8ff') # Light blue/cool background (cleared plasma)
    
    # Generate Photons and rare Baryons
    photon_x, photon_y = np.random.rand(300)*10, np.random.rand(300)*10
    survivor_x, survivor_y = np.random.rand(8)*10, np.random.rand(8)*10
    
    ax2.scatter(photon_x, photon_y, c='gold', s=10, alpha=0.4, label=r'Photons ($\gamma$)')
    ax2.scatter(survivor_x, survivor_y, c='green', s=50, marker='*', edgecolor='black', zorder=10, label='Surviving Baryons')
    
    # --- NEW: Add the ubiquitous background of Micro-Knots ---
    # A large number of small, unmerged knots forming a "fog"
    micro_x, micro_y = np.random.rand(200)*10, np.random.rand(200)*10
    ax2.scatter(micro_x, micro_y, c='black', s=15, alpha=0.7, marker='.', zorder=5, label='Surviving Micro-Knots ($10^{24}$ kg)')

    # Draw Frozen Macro-Knots (Terminal Mass 10^5 M_sun)
    frozen_centers = [(3.75, 6.75), (7.5, 3.75)]
    for i, (cx, cy) in enumerate(frozen_centers):
        circle = Circle((cx, cy), 1.6, color='black', alpha=0.95, zorder=8)
        ax2.add_patch(circle)
        ax2.text(cx, cy, r"$10^5 M_\odot$", color='white', ha='center', va='center', fontweight='bold', zorder=9)
        if i == 0: # Add label only once for legend
             ax2.scatter([], [], c='black', s=200, label=r'Frozen Macro-Knot ($10^5 M_\odot$)')


    ax2.set_title(r"2. Topological Freeze-Out ($t \approx 1$ s)" + "\nCleared Plasma & Bimodal Spectrum", fontsize=14, pad=15)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.axis('off')

    # ==========================================
    # Transition Arrow
    # ==========================================
    xyA = (10.2, 5) 
    xyB = (-0.2, 5) 
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                          axesA=ax1, axesB=ax2, color="black", arrowstyle="-|>", lw=3, mutation_scale=20)
    ax1.add_artist(con)
    
    fig.text(0.5, 0.53, "The Great Annihilation\n" + r"$T \approx 1$ MeV", ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkred')
    fig.text(0.5, 0.45, r"$e^+ + e^- \rightarrow \gamma + \gamma$", ha='center', va='top', fontsize=12)

    plt.tight_layout(rect=[0, 0.0, 1, 0.92])
    
    filename = 'Fig_Act2_Annihilation.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully as '{filename}'")
    #plt.show()

if __name__ == "__main__":
    generate_act2_plot()
