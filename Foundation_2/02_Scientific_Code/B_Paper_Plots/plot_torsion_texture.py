#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
FILENAME       : plot_torsion_texture.py
PROJECT        : Foundation II: The Chiral Universe
AUTHOR         : Pascal Fichant
DATE           : February 2026 (v1.0.3)
DESCRIPTION    : Visualization of the Primordial Vacuum Texture (Spin Density).

PHYSICS CONTEXT:
    In the ECF framework, the early universe is not an isotropic scalar field
    but a vector-dominated state governed by the Spin Density tensor S^mu.
    At the moment of the bounce, the conservation of angular momentum imposes
    a structured topology on the vacuum.
    
    This script visualizes this "Texture":
    1. The vector field represents the local spin orientation (torsion).
    2. The field lines are not random but form a helical structure.
    3. The central Red Axis represents the net angular momentum vector 
       (the "Axis of Evil") which breaks global isotropy.

OUTPUT         : Fig6_Torsion_Texture.png
DEPENDENCIES   : numpy, matplotlib
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

OUTPUT_FILE = "Fig6_Torsion_Texture.png"

def generate_torsion_field(n_layers=8, points_per_layer=24, height=2.0):
    """
    Generates a helical vector field representing the Spin Density.
    """
    x_list, y_list, z_list = [], [], []
    u_list, v_list, w_list = [], [], []
    colors = []

    # Construct concentric cylinders of vectors
    radii = np.linspace(0.2, 1.0, n_layers)
    
    for r in radii:
        n_points = int(points_per_layer * r * 5)
        theta = np.linspace(0, 2*np.pi, n_points)
        z_levels = np.linspace(-height/2, height/2, 12)
        
        for z in z_levels:
            for t in theta:
                # Position
                x = r * np.cos(t)
                y = r * np.sin(t)
                
                # Organic modulation (simulating quantum fluctuations)
                modulation = 0.1 * np.sin(3 * z) 
                
                # Torsion Vector Components (S^mu)
                # u, v: Rotational component (Twist)
                # w:    Longitudinal component (Alignment)
                
                twist_strength = 1.0 / (r + 0.2) # Vortex core is tighter
                
                u = -y * twist_strength + x * modulation
                v =  x * twist_strength + y * modulation
                w =  1.8 # Strong vertical alignment (Memory of the Axis)
                
                # Normalization for Quiver aesthetics
                norm = np.sqrt(u**2 + v**2 + w**2)
                scale = 0.12
                
                x_list.append(x)
                y_list.append(y)
                z_list.append(z)
                u_list.append(u / norm * scale)
                v_list.append(v / norm * scale)
                w_list.append(w / norm * scale)
                
                # Color based on local torsion intensity (Twist)
                colors.append(twist_strength)

    return x_list, y_list, z_list, u_list, v_list, w_list, colors

def main():
    # Setup 3D Figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dark Void Background
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Generate Field
    x, y, z, u, v, w, c = generate_torsion_field()
    
    # 1. Plot the Vector Field (The "Texture")
    # 'magma' colormap represents high-energy density
    ax.quiver(x, y, z, u, v, w, 
              length=0.1, 
              normalize=True,
              cmap='magma', 
              array=np.array(c), 
              alpha=0.85,
              linewidth=0.6)
    
    # 2. The Axis of Evil (Central Red Vector)
    # Thick red line representing the breaking of isotropy
    ax.plot([0, 0], [0, 0], [-1.3, 1.3], color='#FF0000', lw=5, zorder=100, alpha=0.9)
    # Arrow head
    ax.quiver(0, 0, 1.3, 0, 0, 0.4, color='#FF0000', lw=3, arrow_length_ratio=0.4)

    # 3. Formatting
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_axis_off() # Hide box/grid for pure visualization
    
    # Titles and Annotations
    ax.text2D(0.5, 0.96, "Primordial Vacuum Texture", 
              transform=ax.transAxes, color='white', ha='center', 
              fontsize=16, fontweight='bold')
    
    ax.text2D(0.5, 0.92, r"Spin Density Field $\vec{S}$ (The Cosmic Seed)", 
              transform=ax.transAxes, color='#CCCCCC', ha='center', 
              fontsize=11, style='italic')

    # Label for the Axis
    ax.text(0.1, 0, 1.5, "Preferred Direction\n(Axis of Evil)", 
            color='#FF4444', ha='center', fontsize=10, fontweight='bold')

    # View Angle (Top-down oblique to show the spiral)
    ax.view_init(elev=28, azim=45)

    # Save
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, facecolor='black', dpi=300)
    print(f"[OK] Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()