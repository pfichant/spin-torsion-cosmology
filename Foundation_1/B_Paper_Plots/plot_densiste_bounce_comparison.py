"""
================================================================================
SCRIPT: Energy Density Bounce Comparison
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant (2026)
Description: 
    Illustrates the resolution of the initial singularity.
    Compares the diverging density in standard General Relativity (GR) 
    with the saturated critical density (Cartan limit) in the ECF bounce model.
================================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Headless backend for safety
matplotlib.use('Agg')

# PRD Standard Formatting
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 14,
    'font.family': 'serif',
    'axes.linewidth': 1.5,
    'text.usetex': False  # Set to True if you have a full LaTeX distribution installed
})

def plot_density_saturation():
    print(">>> Generating Figure: Density Saturation at the Bounce...")
    
    # Cosmic time t (arbitrary scale centered around the bounce t=0)
    t = np.linspace(-3, 3, 1000)
    
    # 1. Standard General Relativity (GR) - Diverging density
    rho_gr = 1.0 / (t**2 + 0.01)
    
    # 2. ECF Bounce Model - Regularized density
    # We calibrate a_min so the peak reaches exactly rho_c = 20 for the visual schematic
    rho_c = 20.0
    a_min_sq = np.sqrt(1.0 / rho_c)
    rho_ecf = 1.0 / ((t**2 + a_min_sq)**2)
    
    # --- FIGURE SETUP ---
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.15)

    # Plot models
    ax.plot(t, rho_gr, 'b--', linewidth=2, label=r'General Relativity ($\rho \to \infty$)')
    ax.plot(t, rho_ecf, 'r-', linewidth=3, label=r'ECF Bounce ($\rho \to \rho_c$)')
    
    # Critical Density Limit
    ax.axhline(rho_c, color='black', linestyle=':', linewidth=2)
    
    # Text Box for Critical Density
    ax.text(-2.8, rho_c + 1, 'Critical Cartan Density $\\rho_c$', 
            va='bottom', ha='left', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))

    # Singularity Resolution Annotation
    ax.annotate('Singularity Resolved', xy=(0, rho_c), xytext=(0.5, rho_c + 3.5),
                arrowprops=dict(facecolor='#c0392b', edgecolor='#c0392b', shrink=0.05, width=2, headwidth=8),
                fontsize=16, color='#c0392b', fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Cosmic Time $t$', fontsize=16, fontweight='bold')
    ax.set_ylabel('Energy Density $\\rho(t)$', fontsize=16, fontweight='bold')
    ax.set_title('Density Saturation at the Primordial Spin Bounce', fontsize=18, fontweight='bold', pad=20)
    
    # Limits and Ticks
    ax.set_ylim(0, 30)
    ax.set_xlim(-3, 3)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    
    ax.legend(loc='center right', frameon=True, framealpha=0.95)

    # Save figure (Using JPG to match your LaTeX configuration)
    plt.savefig('figure_densiste_bounce_comparison.jpg', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_density_saturation()