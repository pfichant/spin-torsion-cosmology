#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script : plot_torsion_crystallization.py
Description : Generates a visual representation of the topological phase transition
              from a continuous ECF spin-fluid to discrete micro-knots.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

def generate_phase_transition_plot():
    print("Generating Torsion Crystallization Phase Transition...")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Create spatial grid
    grid_size = 100
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    X, Y = np.meshgrid(x, y)

    # 1. Generate the Continuous Spin-Fluid (Sum of smooth Gaussians)
    Z_fluid = np.zeros((grid_size, grid_size))
    num_peaks = 25
    centers = np.random.rand(num_peaks, 2) * 10
    
    for cx, cy in centers:
        # Wide, smooth Gaussians overlapping to form a continuous fluid
        Z_fluid += np.exp(-((X - cx)**2 + (Y - cy)**2) / 3.0) 

    # 2. Generate the Crystallized Defects (Sharp, discrete peaks)
    Z_crystal = np.zeros((grid_size, grid_size))
    for cx, cy in centers:
        # Extremely narrow Gaussians to represent the 10^24 kg collapsed micro-knots
        Z_crystal += 2.0 * np.exp(-((X - cx)**2 + (Y - cy)**2) / 0.05)
        
    # Add a slight "broken vacuum" background noise to the crystal phase
    Z_crystal += 0.1 * np.random.rand(grid_size, grid_size)

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='white')
    fig.suptitle('Electroweak Phase Transition: Torsion Crystallization', fontsize=18, fontweight='bold', y=0.98)

    # Left Plot: Continuous Fluid
    im1 = ax1.imshow(Z_fluid, extent=[0, 10, 0, 10], origin='lower', cmap='magma', interpolation='bicubic')
    ax1.set_title(r"1. Stiff Era ($t < 10^{-11}$ s)" + "\nContinuous Weyssenhoff Spin-Fluid", fontsize=14, pad=15)
    ax1.axis('off')

    # Right Plot: Crystallization (Micro-Knots)
    im2 = ax2.imshow(Z_crystal, extent=[0, 10, 0, 10], origin='lower', cmap='magma', interpolation='bilinear', vmax=2.5)
    ax2.set_title(r"2. Electroweak Epoch ($t \approx 10^{-11}$ s)" + "\nTopological Defect Freeze-Out", fontsize=14, pad=15)
    ax2.axis('off')

    # Draw an arrow between the two subplots to indicate time/cooling
    xyA = (10.5, 5) # Point on the right of the first plot
    xyB = (-0.5, 5) # Point on the left of the second plot
    con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="data",
                          axesA=ax1, axesB=ax2, color="black", arrowstyle="-|>", lw=3, mutation_scale=20)
    ax1.add_artist(con)
    
    # Add temperature text above the arrow
    fig.text(0.5, 0.53, "Cooling\n" + r"$T_{EW} \approx 150$ GeV", ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkred')
    fig.text(0.5, 0.45, "Kibble-Zurek\nMechanism", ha='center', va='top', fontsize=10, style='italic')

    plt.tight_layout(rect=[0, 0.0, 1, 0.92])
    
    # Save high-res for the paper
    filename = 'Fig_Torsion_Crystallization.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved successfully as '{filename}'")
    # plt.show()

if __name__ == "__main__":
    generate_phase_transition_plot()
