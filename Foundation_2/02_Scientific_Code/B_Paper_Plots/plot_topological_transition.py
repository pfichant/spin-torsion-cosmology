"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_topological_transition.py
Author:        Pascal Fichant
Date:          February 2026 (New - Appendix B Illustration)
Description:   Generates a 3-panel schematic illustrating the formation of an
               ECF PBH: transforming a fermion plasma into a geometric knot.
Output:        FigB1_Topological_Transition.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

OUTPUT_FILE = "FigB1_Topological_Transition.png"

def setup_axis(ax, title):
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-3, 3)
    ax.set_axis_off()
    ax.set_title(title, color='white', fontsize=12, fontweight='bold', pad=20)
    ax.view_init(elev=25, azim=30)

def generate_fermion_cloud(n_points, radius, disorder=0.2):
    """Generates points in a sphere representing fermions"""
    u = np.random.rand(n_points, 1)
    v = np.random.rand(n_points, 1)
    phi = u * 2 * np.pi
    theta = np.arccos(2 * v - 1)
    r = radius * np.cbrt(np.random.rand(n_points, 1))
    
    # Add some noise
    x = r * np.sin(theta) * np.cos(phi) + np.random.normal(0, disorder, (n_points, 1))
    y = r * np.sin(theta) * np.sin(phi) + np.random.normal(0, disorder, (n_points, 1))
    z = r * np.cos(theta) + np.random.normal(0, disorder, (n_points, 1))
    return x, y, z

def generate_torus_knot(n_points=1000, scale=1.0):
    """Generates the final geometric knot"""
    t = np.linspace(0, 8 * np.pi, n_points)
    p, q = 3, 4
    r_tube = 1.5 * scale
    r_cross = 0.7 * scale
    x = (r_tube + r_cross * np.cos(q * t)) * np.cos(p * t)
    y = (r_tube + r_cross * np.cos(q * t)) * np.sin(p * t)
    z = r_cross * np.sin(q * t)
    return x, y, z

def main():
    fig = plt.figure(figsize=(15, 5))
    fig.patch.set_facecolor('#050505') # Dark background

    # --- PANEL 1: Initial Collapse (Fermion Plasma) ---
    ax1 = fig.add_subplot(131, projection='3d', facecolor='#050505')
    setup_axis(ax1, "t1: Gravitational Collapse\n(Fermion Plasma)")
    
    # Particles
    xf, yf, zf = generate_fermion_cloud(800, radius=2.5)
    ax1.scatter(xf, yf, zf, s=5, c='#00BFFF', alpha=0.6, label='Fermions') # Blue particles

    # Inflow arrows
    for _ in range(8):
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2*np.pi)
        r_start = 3.2
        x_s = r_start * np.sin(theta) * np.cos(phi)
        y_s = r_start * np.sin(theta) * np.sin(phi)
        z_s = r_start * np.cos(theta)
        # Arrow pointing inward
        ax1.quiver(x_s, y_s, z_s, -x_s, -y_s, -z_s, length=1.0, color='white', alpha=0.5, lw=1.5, arrow_length_ratio=0.3)
    ax1.text2D(0.5, -0.1, "Matter Dominated", transform=ax1.transAxes, color='#00BFFF', ha='center')


    # --- PANEL 2: The Critical Transition ---
    ax2 = fig.add_subplot(132, projection='3d', facecolor='#050505')
    setup_axis(ax2, "t2: Spin-Spin Repulsion\n(Critical Density)")
    
    # Denser, smaller particle cloud
    xf_d, yf_d, zf_d = generate_fermion_cloud(1000, radius=1.2, disorder=0.1)
    ax2.scatter(xf_d, yf_d, zf_d, s=8, c='#4169E1', alpha=0.4) # Darker blue

    # Central "hot" core representing repulsion/torsion generation
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x_c = 0.8 * np.cos(u) * np.sin(v)
    y_c = 0.8 * np.sin(u) * np.sin(v)
    z_c = 0.8 * np.cos(v)
    ax2.plot_surface(x_c, y_c, z_c, color='#FF4500', alpha=0.6, edgecolor='none') # Orange core

    # Emergent twisted field lines mixed with particles
    xk, yk, zk = generate_torus_knot(n_points=500, scale=0.6)
    ax2.plot(xk, yk, zk, c='#FFD700', lw=2, alpha=0.7) # Gold lines emerging
    ax2.text2D(0.5, -0.1, "Matter-Geometry Mixing", transform=ax2.transAxes, color='#FFD700', ha='center')


    # --- PANEL 3: Final State (Geometric Knot) ---
    ax3 = fig.add_subplot(133, projection='3d', facecolor='#050505')
    setup_axis(ax3, "t3: Fossilization\n(Topological Defect)")
    
    # No particles, just the knot
    xk_f, yk_f, zk_f = generate_torus_knot(n_points=2000, scale=1.2)
    # Color gradient for the knot
    colors = cm.plasma(np.linspace(0, 1, len(xk_f)))
    for i in range(len(xk_f)-1):
        ax3.plot(xk_f[i:i+2], yk_f[i:i+2], zk_f[i:i+2], color=colors[i], lw=2.5, alpha=0.8)
        
    # Stable Core
    x_c_f = 0.5 * np.cos(u) * np.sin(v)
    y_c_f = 0.5 * np.sin(u) * np.sin(v)
    z_c_f = 0.5 * np.cos(v)
    ax3.plot_surface(x_c_f, y_c_f, z_c_f, color='black', edgecolor='#FF4500', alpha=0.9)
    ax3.text2D(0.5, -0.1, "Geometry Dominated (Stable)", transform=ax3.transAxes, color='#FF4500', ha='center')

    # --- Arrows between panels ---
    # This is tricky in 3D layouts, using figure coordinates
    fig.text(0.34, 0.5, "→", fontsize=40, color='white', ha='center', va='center')
    fig.text(0.34, 0.45, "Collapse", fontsize=10, color='gray', ha='center', va='center')
    
    fig.text(0.64, 0.5, "→", fontsize=40, color='white', ha='center', va='center')
    fig.text(0.64, 0.45, "Repulsion", fontsize=10, color='gray', ha='center', va='center')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='#050505')
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()