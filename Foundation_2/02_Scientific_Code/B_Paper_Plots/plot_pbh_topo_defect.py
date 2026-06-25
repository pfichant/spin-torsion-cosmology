"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_pbh_topological_defect.py
Author:        Pascal Fichant
Date:          February 2026 (Revised - Granularity Visualization)
Description:   Generates a 3D visualization of an ECF PBH as a topological 
               torsion defect ("vacuum knot"). Replaces the simple sphere scheme.
               Uses a randomized torus knot to represent field line granularity.
Output:        Fig4_PBH_Topological_Defect.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

OUTPUT_FILE = "Fig4_PBH_Topological_Defect.png"

def generate_pbh_defect_plot():
    """
    Generates a 3D visualization of an ECF PBH as a topological torsion defect.
    Represented as a complex "knot" of field lines (a "ball of wool").
    """
    # Set up a dark-themed 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#050505') # Almost black cosmic background
    fig.patch.set_facecolor('#050505')

    # --- 1. Generate the "Tangle" (Torus Knot + Noise) ---
    # Parameters for a complex (p,q) torus knot
    p, q = 3, 7  # Higher numbers = more twists
    n_points = 4000 # More points = smoother lines
    t = np.linspace(0, 12 * np.pi, n_points) # Many turns
    
    r_major = 2.0 
    # Modulate minor radius for a "messy" look
    r_minor = 1.0 + 0.3 * np.sin(3 * t) + 0.2 * np.cos(5 * t) 

    # Torus knot parametric equations
    x = (r_major + r_minor * np.cos(q * t)) * np.cos(p * t)
    y = (r_major + r_minor * np.cos(q * t)) * np.sin(p * t)
    z = r_minor * np.sin(q * t)

    # Add "Granularity" (Quantum Jitter)
    np.random.seed(42) # For reproducibility
    jitter_scale = 0.12
    x += np.random.normal(0, jitter_scale, n_points)
    y += np.random.normal(0, jitter_scale, n_points)
    z += np.random.normal(0, jitter_scale, n_points)

    # --- 2. Color Mapping (Field Strength / Chirality) ---
    # Color based on distance from center (Hot core -> Cool halo)
    r_dist = np.sqrt(x**2 + y**2 + z**2)
    # Normalize distance for colormap
    norm = plt.Normalize(r_dist.min(), r_dist.max())
    # Use 'plasma' or 'magma' for a glowing effect
    colors = cm.magma(1 - norm(r_dist)) 
    
    # --- 3. Plot the Field Lines ---
    # Plot as a collection of segments to apply varying colors
    # We plot multiple slightly offset lines to give "volume" to the wool strand
    for offset in np.linspace(-0.05, 0.05, 3):
        ax.plot(x + offset, y + offset, z + offset, 
                color=colors[len(t)//2], # Use a central color for simplicity in loop
                lw=1.0, alpha=0.6)
        
    # To get the gradient correctly, we must plot segment by segment (slower but better)
    # Clearing the previous quick attempt and doing it right:
    ax.clear()
    ax.set_axis_off()
    for i in range(n_points - 1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], 
                color=colors[i], lw=1.8, alpha=0.7)

    # --- 4. Add a "Core" (The Defect Center / Horizon) ---
    # A small, dark, central sphere representing the collapsed vacuum state
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    r_core = 0.6
    x_c = r_core * np.cos(u) * np.sin(v)
    y_c = r_core * np.sin(u) * np.sin(v)
    z_c = r_core * np.cos(v)
    ax.plot_surface(x_c, y_c, z_c, color='black', alpha=0.95, 
                    edgecolor='#300000', lw=0.5, shade=True, zorder=10)

    # --- 5. Formatting & Annotations ---
    
    # Main Title
    ax.set_title("The ECF Topological Defect\n(Primordial Black Hole as a Vacuum Knot)", 
                 color='white', fontsize=16, fontweight='bold', y=0.95)
    
    # Annotation 1: The Core
    ax.text2D(0.5, 0.48, "Vacuum Defect Core\n(Event Horizon)", 
              transform=ax.transAxes, color='white', ha='center', fontsize=10,
              bbox=dict(facecolor='black', edgecolor='#FF4500', alpha=0.7, boxstyle='round,pad=0.3'))

    # Annotation 2: The Granularity
    ax.text2D(0.82, 0.65, "Twisted Torsion\nField Lines\n('Granularity')", 
              transform=ax.transAxes, color='#FFD700', ha='left', fontsize=10)

    # Set view and limits
    ax.view_init(elev=25, azim=-45)
    limit = 3.5
    ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit); ax.set_zlim(-limit, limit)
    ax.set_aspect('equal')

    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='#050505')
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_pbh_defect_plot()