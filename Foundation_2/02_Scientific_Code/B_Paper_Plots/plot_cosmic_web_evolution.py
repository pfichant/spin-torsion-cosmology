"""
=============================================================================
ECF COSMOLOGICAL FRAMEWORK - FOUNDATION II (Version 1.0.9)
Script: plot_cosmic_web_evolution.py
Author: Pascal Fichant
Date: February 2026
=============================================================================

DESCRIPTION:
This script generates a publication-quality 4-panel figure illustrating the 
top-down geometric formation of the Cosmic Web within the Einstein-Cartan-Fichant 
(ECF) cosmological framework.

THEORETICAL CONTEXT:
Unlike standard Lambda-CDM bottom-up hierarchical clustering, the ECF model 
relies on the Kibble-Zurek mechanism during the primordial chiral phase transition. 
This script simulates:
1. Phase I (t ~ 1s): The crystallization of the vacuum into a Voronoi-like 
   topological foam (domain boundaries).
2. Phase II & III (z ~ 30 to 10): The violent, top-down baryonic siphoning 
   (gravitational vacuuming) from the topologically trivial void centers 
   towards the macroscopic defects (Macro-Knots) located on the filamentary walls.
3. Phase IV (z ~ 0): The mature Cosmic Web with sharply defined luminous nodes 
   and profound, giant cosmic voids.

OUTPUT:
- 'Fig_Cosmic_Web_Evolution.png' (High-resolution image for LaTeX manuscript)
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

def generate_cosmic_web_evolution():
    # Set random seed for scientific reproducibility
    np.random.seed(42)
    
    # 1. Kibble-Zurek Topological Freeze-out: Generate domain centers (future voids)
    n_voids = 40
    points = np.random.rand(n_voids, 2)
    vor = Voronoi(points)
    
    # 2. Primordial Baryonic Gas: Uniformly distributed at initial time
    n_gas = 18000
    gas_x = np.random.rand(n_gas)
    gas_y = np.random.rand(n_gas)
    gas_points = np.vstack((gas_x, gas_y)).T
    
    # Initialize high-resolution, publication-quality figure
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})
    fig, axes = plt.subplots(1, 4, figsize=(22, 5.5), facecolor='black')
    fig.subplots_adjust(wspace=0.05) # Minimize whitespace between panels
    
    # Panel titles matching the theoretical ECF timeline
    titles = [
        r"Phase I: Topological Freeze-out ($t \approx 1$s)",
        r"Phase II: Baryonic Siphoning ($z \approx 30$)",
        r"Phase III: Filament Ignition ($z \approx 10$)",
        r"Phase IV: Mature Cosmic Web ($z \approx 0$)"
    ]
    
    # Top-down attraction strength towards the geometric skeleton
    attraction_factors = [0.0, 0.45, 0.80, 0.96]
    
    for i, ax in enumerate(axes):
        ax.set_facecolor('black')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(titles[i], color='white', fontsize=15, pad=15, fontweight='bold')
        
        # Draw the Kibble-Zurek geometric skeleton (the invisible Macro-Knot network)
        for simplex in vor.ridge_vertices:
            if -1 not in simplex:
                p1, p2 = vor.vertices[simplex[0]], vor.vertices[simplex[1]]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#444444', alpha=0.4, lw=0.8)
                
        # Simulate the baryonic gas falling into the topological potential wells
        current_gas_x = gas_points[:, 0].copy()
        current_gas_y = gas_points[:, 1].copy()
        
        if i > 0:
            for j in range(n_gas):
                # Find the nearest Macro-Knot (Voronoi vertex)
                dist = np.sqrt((vor.vertices[:, 0] - current_gas_x[j])**2 + 
                               (vor.vertices[:, 1] - current_gas_y[j])**2)
                nearest = np.argmin(dist)
                target_x, target_y = vor.vertices[nearest]
                
                # Apply simulated non-linear top-down gravitational acceleration
                move_factor = attraction_factors[i] * np.random.uniform(0.4, 1.0)
                current_gas_x[j] += (target_x - current_gas_x[j]) * move_factor
                current_gas_y[j] += (target_y - current_gas_y[j]) * move_factor
                
        # Render the baryonic gas (temperature/density color mapping)
        cmap = plt.cm.magma if i > 1 else plt.cm.Blues_r
        ax.scatter(current_gas_x, current_gas_y, s=0.4, color=cmap(0.9), alpha=0.5)
        
        # Render the mature galaxies/quasars at the Macro-Knot intersections (Phases III & IV)
        if i > 1:
            valid_vertices = vor.vertices[(vor.vertices[:,0] >= 0) & (vor.vertices[:,0] <= 1) & 
                                          (vor.vertices[:,1] >= 0) & (vor.vertices[:,1] <= 1)]
            glow_size = 25 if i == 2 else 40
            ax.scatter(valid_vertices[:, 0], valid_vertices[:, 1], 
                       s=glow_size, color='white', edgecolor='gold', linewidth=1.5, zorder=5)

    # Main Figure Title
    plt.suptitle("ECF Top-Down Structure Formation: From Kibble-Zurek Foam to the Cosmic Web", 
                 color='white', fontsize=20, fontweight='bold', y=1.05)
    
    # Export for publication
    plt.savefig('Fig_Cosmic_Web_Evolution.png', dpi=300, bbox_inches='tight', facecolor='black')
    print("[SUCCESS] Publication-ready figure generated: Fig_Cosmic_Web_Evolution.png")

if __name__ == "__main__":
    generate_cosmic_web_evolution()
