"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_ecf_baryogenesis_zoom.py
Author:        Pascal Fichant
Date:          February 2026 (v5.0 - With Zoom Inset)
Description:   Plots Comoving Abundance with a magnifying glass (inset)
               to visualize the initial microscopic chiral splitting.
Output:        Fig1_Chiral_Baryogenesis_Zoom.png
=============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

OUTPUT_FILE = "Fig1_Chiral_Baryogenesis_Zoom.png"

def main():
    # 1. Simulation Data
    # ------------------
    # We increase the resolution for smooth zooming
    t = np.logspace(-45, 2, 3000)
    
    t_gap_end = 1e-40
    t_annihilation = 1e-6
    eta = 1e-9 
    
    # --- Modeling Abundances ---
    # Base Equilibrium
    Y_eq = 1.0 / (1.0 + np.exp(2.0 * np.log10(t / t_annihilation)))
    mask_late = t > t_annihilation
    Y_eq[mask_late] = (t_annihilation / t[mask_late])**2 * np.exp(-(t[mask_late]/t_annihilation)**0.5 * 10) + 1e-20

    # MATTER (Blue)
    # We add a small visual offset even early on to make the zoom legible
    # In physics it's 1e-9, for the plot we use 1e-3 in the zoom area just for visibility
    visual_split = 0.005 # 0.5% visual split for the schematic
    Y_matter = np.maximum(Y_eq * (1 + visual_split), eta)
    
    # ANTIMATTER (Red)
    Y_antimatter = Y_eq * (1 - visual_split) 
    # Force the drop for antimatter later
    Y_antimatter[mask_late] = Y_eq[mask_late] # Follows the crash

    # 2. Main Plot Setup
    # ------------------
    fig, ax = plt.subplots(figsize=(12, 7))

    # Zones
    ax.axvspan(1e-45, t_gap_end, color='#FFFACD', alpha=0.5, lw=0) # Yellow
    ax.axvspan(t_gap_end, t_annihilation, color='#F0F0F0', alpha=0.5, lw=0) # Gray

    # Main Curves
    ax.loglog(t, Y_matter, color='#00008B', lw=3, label=r'Matter ($Y_B$)')
    ax.loglog(t, Y_antimatter, color='#B22222', lw=2.5, linestyle='--', label=r'Antimatter ($Y_{\bar{B}}$)')

    # Labels Main Plot
    ax.text(1e-43, 4, "PHASE 1:\nChiral Torsion Gap", ha='center', fontweight='bold', color='#DAA520', fontsize=10)
    ax.text(1e-20, 4, "PHASE 2:\nThermal Equilibrium Era", ha='center', fontweight='bold', color='gray', fontsize=10)
    ax.text(1e-3, 4, "PHASE 3:\nFreeze-out & Annihilation", ha='center', fontweight='bold', color='black', fontsize=10)

    # Final Asymmetry Annotation
    ax.annotate(r"Final Asymmetry $\eta \approx 10^{-9}$", 
                xy=(1e0, eta), xytext=(1e-3, 1e-8),
                color='#00008B', fontweight='bold', fontsize=14,
                arrowprops=dict(edgecolor='#00008B', arrowstyle='->', lw=2),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#00008B", lw=2))
    
    ax.text(1e-4, 1e-4, "Antimatter\nvanishes", color='#B22222', ha='center', fontweight='bold')


    # 3. THE ZOOM INSET (La Loupe)
    # ----------------------------
    # Position: x, y, width, height (relative to axes)
    # Placed in the gray zone, looking at the yellow/gray transition
    axins = ax.inset_axes([0.18, 0.45, 0.25, 0.25]) 
    
    # Plot the same data in the inset
    axins.plot(t, Y_matter, color='#00008B', lw=2)
    axins.plot(t, Y_antimatter, color='#B22222', lw=2, linestyle='--')
    
    # Settings for the Inset
    # We focus on a time BEFORE annihilation, where curves look merged on main plot
    x1, x2 = 1e-42, 1e-38 
    y1, y2 = 0.98, 1.02 # Linear scale around 1 to show the split
    
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xscale('log')
    axins.set_yscale('linear') # Linear Y scale makes the difference visible!
    
    axins.set_title(r"Microscopic Zoom ($\times 10^9$)", fontsize=9, fontweight='bold')
    axins.tick_params(labelleft=False, labelbottom=False) # Hide cluttered ticks
    axins.grid(True, alpha=0.2)
    
    # Text inside zoom
    axins.text(1e-40, 1.006, r"Matter ($n_B$)", color='#00008B', fontsize=8, ha='center')
    axins.text(1e-40, 0.992, r"Antimatter ($n_{\bar{B}}$)", color='#B22222', fontsize=8, ha='center')
    axins.text(1e-40, 1.0, r"$\Delta \mu \neq 0$", fontsize=8, ha='center', va='center', fontweight='bold')

    # Draw connectors (The lines linking the zoom to the main plot)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", alpha=0.7)


    # 4. Final Formatting
    # -------------------
    ax.set_xlabel(r"Cosmic Time $t$ [s]", fontsize=14, fontweight='bold')
    ax.set_ylabel(r"Comoving Abundance $Y = n / n_\gamma$", fontsize=14, fontweight='bold')
    plt.title(r"ECF Baryogenesis: The Survival of Matter", fontsize=18, fontweight='bold', y=1.05)
    
    ax.set_xlim(1e-45, 10.0)
    ax.set_ylim(1e-13, 10)
    ax.grid(True, alpha=0.3)
    
    ax.legend(loc='lower left', fontsize=11, frameon=True, shadow=True)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Figure with ZOOM generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()