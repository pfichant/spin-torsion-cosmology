
"""
=============================================================================
NOTE: This script generates ILLUSTRATIVE schematic figures for visualization.
The shapes and ratios shown are qualitative representations of ECF predictions,
not fits to observational data. See Foundation II §bounce for the physical basis.
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_cosmic_evolution_final.py
Author:        Pascal Fichant
Date:          February 2026 (v1.3 - Added Radius Ratio Calculation)
Description:   Visualizes the geometric evolution of the Universe.
               Uses 2D Polar Cross-sections with pseudo-3D styling.
Output:        Fig5_Cosmic_Evolution_Final.png
=============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np

OUTPUT_FILE = "Fig5_Cosmic_Evolution_Final.png"

def draw_pseudo_3d_ellipsoid(ax, width, height, main_color):
    """Draws an ellipse with a gradient fill to fake a 3D volume."""
    base_rgb = mcolors.to_rgb(main_color)
    center_rgb = tuple([min(1.0, c + 0.5) for c in base_rgb])
    cmap = mcolors.LinearSegmentedColormap.from_list("glow", [center_rgb, base_rgb])

    # Draw concentric ellipses
    n_layers = 30
    for i in range(n_layers):
        scale = 1.0 - (i / n_layers) * 0.9 
        color_val = cmap(i / n_layers)
        alpha_val = 0.8 - (i / n_layers) * 0.6
        el = patches.Ellipse((0, 0), width * scale, height * scale, 
                             fc=color_val, ec='none', alpha=alpha_val)
        ax.add_patch(el)

    # Outer edge
    edge = patches.Ellipse((0, 0), width, height, 
                           fc='none', ec=main_color, linewidth=2.5, alpha=1.0)
    ax.add_patch(edge)


def draw_era(ax, title, subtitle, flattening_visual, main_color, time_label, ratio_label, centrifugal_strength):
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 2.4) # Increased top limit for labels
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 1. The Cosmic Shape (Pseudo-3D)
    draw_pseudo_3d_ellipsoid(ax, 2.8, flattening_visual, main_color)
    
    # 2. Spin Axis
    ax.plot([0, 0], [-1.3, 1.5], color='black', lw=2, linestyle='--', zorder=10)
    ax.text(0, 1.6, r"$\vec{\omega}$", ha='center', fontsize=14, fontweight='bold', zorder=10)
    
    # 3. Rotation Arrow
    style = "Simple, tail_width=0.5, head_width=5, head_length=10"
    kw = dict(arrowstyle=style, color="black", zorder=10)
    rot_arrow = patches.FancyArrowPatch((-0.5, 1.3), (0.5, 1.3), connectionstyle="arc3,rad=-0.3", **kw)
    ax.add_patch(rot_arrow)
    
    # 4. Centrifugal Force
    if centrifugal_strength > 0:
        arrow_len = 0.3 + (centrifugal_strength * 0.15)
        f_style = "Simple, tail_width=1.5, head_width=6, head_length=8"
        f_kw = dict(arrowstyle=f_style, color="#FF2400", zorder=5) 
        
        start_x = 1.45 if flattening_visual > 1.0 else 1.4
        ar_r = patches.FancyArrowPatch((start_x, 0), (start_x + arrow_len, 0), **f_kw)
        ax.add_patch(ar_r)
        ar_l = patches.FancyArrowPatch((-start_x, 0), (-start_x - arrow_len, 0), **f_kw)
        ax.add_patch(ar_l)
        
        if centrifugal_strength >= 3:
            ax.text(1.8, 0.3, "Centrifugal\nForce", fontsize=9, color='#FF2400', ha='center', fontweight='bold')

    # 5. LABELS & LEGENDS
    # Title Era
    ax.text(0, -1.7, title, ha='center', fontsize=13, fontweight='bold')
    
    # Subtitle Description
    ax.text(0, -2.0, subtitle, ha='center', fontsize=11, color='gray')
    
    # Time Box
    ax.text(0, -2.35, time_label, ha='center', fontsize=10, color='white', 
            bbox=dict(facecolor=main_color, alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3'))
            
    # --- NEW: RATIO CALCULATION LEGEND ---
    # Display the Shape Ratio Req/Rpol
    ax.text(0, 2.1, r"Shape Ratio $R_{eq}/R_{pol}$", ha='center', fontsize=9, color='black', fontweight='bold')
    ax.text(0, 1.85, ratio_label, ha='center', fontsize=11, color='darkblue', fontweight='bold')


def main():
    fig, axes = plt.subplots(1, 4, figsize=(18, 8)) # Increased height slightly
    
    fig.suptitle("The Geometric Evolution of the Cosmic Discus (ECF Model)", fontsize=18, fontweight='bold', y=0.98)
    fig.text(0.99, 0.20, "View: 2D Polar Cross-Section (Slice along spin axis)", 
             ha='right', fontsize=10, color='gray', style='italic', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 1. PLANCK BOUNCE
    draw_era(axes[0], "1. The Bounce", "Ultra-flat Discus", 
             flattening_visual=0.4, main_color='#00CED1',
             time_label=r"$t \sim 10^{-43}$s", 
             ratio_label=r"$\gg 1$ (Disk)", # Ratio Legend
             centrifugal_strength=5)

    # 2. BBN
    draw_era(axes[1], "2. BBN Era", "Oblate Spheroid", 
             flattening_visual=1.2, main_color='#FF4500',
             time_label=r"$t \sim 1$s", 
             ratio_label=r"$\gg 1$ (stiff era)", # Ratio Legend [illustrative]
             centrifugal_strength=3)

    # 3. CMB
    draw_era(axes[2], "3. CMB Era", "The 'Rugby Ball'", 
             flattening_visual=2.2, main_color='#FFD700',
             time_label=r"$z \sim 1100$", 
             ratio_label=r"$\approx 1 + 10^{-5}$", # Ratio Legend (Epsilon)
             centrifugal_strength=1)
    
    axes[2].text(0, 0, "Axis of Evil\nImprinted", ha='center', va='center', fontsize=9, fontweight='bold', color='black', alpha=0.6)

    # 4. TODAY
    draw_era(axes[3], "4. Today", "Pseudo-Isotropy", 
             flattening_visual=2.8, main_color='#0000CD',
             time_label=r"$z = 0$", 
             ratio_label=r"$\approx 1.0$", # Ratio Legend
             centrifugal_strength=0)

    # Timeline Arrow
    arrow = patches.FancyArrowPatch((0.15, 0.03), (0.85, 0.03), 
                                    arrowstyle='Simple, tail_width=3, head_width=12, head_length=15', 
                                    color='gray', alpha=0.4, transform=fig.transFigure, zorder=0)
    fig.patches.append(arrow)
    fig.text(0.5, 0.05, "Cosmic Time Evolution (Spin-Down & Relaxation towards Isotropy)", 
             ha='center', fontsize=12, fontweight='bold', color='gray')

    plt.subplots_adjust(top=0.85, bottom=0.28, wspace=0.15, left=0.05, right=0.95)
    
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    
