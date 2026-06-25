"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_schematic_cmb_mechanism.py
Author:        Pascal Fichant
Date:          February 2026 (v1.4 - Final Syntax Fixes)
Description:   Generates a schematic comparison with Legend for Hot/Cold spots
               and value of flattening (epsilon).
Output:        Fig4_CMB_Mechanism.png
=============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_FILE = "Fig4_CMB_Mechanism.png"

def main():
    # Setup figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # --- PANEL A: STANDARD MODEL (ISOTROPIC) ---
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.8, 1.9)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Title
    ax1.text(0, 1.8, r"A. Standard Model ($\Lambda$CDM)", ha='center', fontsize=14, fontweight='bold')
    ax1.text(0, 1.65, "(Spherical = Isotropic)", ha='center', fontsize=12, color='gray')
    
    # Sphere (Circle)
    circle = patches.Circle((0, 0), 1.0, edgecolor='gray', facecolor='#e6e6fa', linewidth=2, alpha=0.5)
    ax1.add_patch(circle)
    
    # Random Hotspots (Dots)
    np.random.seed(42) 
    for _ in range(40):
        r = np.sqrt(np.random.uniform(0, 1)) * 0.9
        theta = np.random.uniform(0, 2*np.pi)
        x, y = r * np.cos(theta), r * np.sin(theta)
        color = 'red' if np.random.rand() > 0.5 else 'blue'
        ax1.scatter(x, y, c=color, s=50, alpha=0.7, edgecolors='white', linewidth=0.5)

    # LEGEND FOR DOTS (Manually drawn box)
    # Background box
    rect = patches.Rectangle((-1.4, -1.7), 2.8, 0.35, linewidth=1, edgecolor='gray', facecolor='white', alpha=0.9)
    ax1.add_patch(rect)
    
    # Red Dot - CORRECTION ICI (ajout du r)
    ax1.scatter(-1.2, -1.53, c='red', s=60, edgecolors='none')
    ax1.text(-1.1, -1.58, r"Hot Spot ($\Delta T > 0$)", fontsize=10, va='center')
    
    # Blue Dot - CORRECTION ICI (ajout du r)
    ax1.scatter(0.1, -1.53, c='blue', s=60, edgecolors='none')
    ax1.text(0.2, -1.58, r"Cold Spot ($\Delta T < 0$)", fontsize=10, va='center')

    # Random Vectors
    ax1.arrow(0, 0, 0.7, 0.6, head_width=0.08, head_length=0.1, fc='purple', ec='purple', lw=2)
    ax1.text(0.8, 0.65, r"$l=2$", color='purple', fontsize=11)
    
    ax1.arrow(0, 0, -0.6, 0.4, head_width=0.08, head_length=0.1, fc='green', ec='green', lw=2)
    ax1.text(-0.9, 0.45, r"$l=3$", color='green', fontsize=11)
    
    ax1.text(0, -1.2, "Random Orientations", ha='center', color='red', fontsize=12, fontweight='bold')


    # --- PANEL B: ECF MODEL (ANISOTROPE) ---
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.8, 1.9)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # Title
    ax2.text(0, 1.8, "B. ECF Model (Spinning)", ha='center', fontsize=14, fontweight='bold')
    ax2.text(0, 1.65, "(Ellipsoidal = Anisotropic)", ha='center', fontsize=12, color='gray')
    
    # Ellipsoid (Flattened Sphere)
    ellipse = patches.Ellipse((0, 0), 2.2, 1.8, edgecolor='orange', facecolor='#ffefd5', linewidth=2, alpha=0.6)
    ax2.add_patch(ellipse)
    
    # Flattening Annotation
    ax2.text(1.2, 1.0, r"Flattening" "\n" r"$\epsilon \approx 10^{-5}$", fontsize=10, color='orange', fontweight='bold', ha='center')
    
    # Spin Axis
    ax2.plot([0, 0], [-1.2, 1.3], color='black', lw=2, linestyle='--')
    ax2.text(0.05, 1.35, r"Spin Axis $\vec{\omega}$", ha='left', fontsize=12, fontweight='bold')
    
    # Rotation Arrow
    style = "Simple, tail_width=0.5, head_width=4, head_length=8"
    kw = dict(arrowstyle=style, color="black")
    rot_arrow = patches.FancyArrowPatch((-0.3, 1.1), (0.3, 1.1), connectionstyle="arc3,rad=-0.5", **kw)
    ax2.add_patch(rot_arrow)

    # Centrifugal Force
    ax2.arrow(1.1, 0, 0.3, 0, head_width=0.05, head_length=0.08, fc='red', ec='red')
    ax2.arrow(-1.1, 0, -0.3, 0, head_width=0.05, head_length=0.08, fc='red', ec='red')
    ax2.text(1.4, 0.15, "Centrifugal\nForce", fontsize=9, color='red', ha='center')

    # Aligned Vectors
    wedge = patches.Wedge((0,0), 1.0, 75, 105, color='red', alpha=0.15)
    ax2.add_patch(wedge)
    
    # l=2
    ax2.arrow(0, 0, 0.1, 0.8, head_width=0.08, head_length=0.1, fc='purple', ec='purple', lw=2)
    ax2.text(0.2, 0.8, r"$l=2$", color='purple', fontsize=11, fontweight='bold')
    
    # l=3
    ax2.arrow(0, 0, -0.05, 0.6, head_width=0.08, head_length=0.1, fc='green', ec='green', lw=2)
    ax2.text(-0.4, 0.6, r"$l=3$", color='green', fontsize=11, fontweight='bold')

    # Explanation Text
    ax2.text(0, -1.2, "FORCED ALIGNMENT", ha='center', color='darkgreen', fontsize=12, fontweight='bold')
    ax2.text(0, -1.4, "(Matches Fig 3 Red Sector)", ha='center', color='darkgreen', fontsize=10)
    
    # Explanation of Epsilon visual
    ax2.text(0, -1.7, "*Flattening exaggerated for visibility", ha='center', fontsize=8, color='gray', style='italic')

    # Save
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()