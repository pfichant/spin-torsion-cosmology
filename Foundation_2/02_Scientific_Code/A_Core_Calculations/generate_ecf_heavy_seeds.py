#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: The Chiral Universe
Script      : generate_ecf_heavy_seeds.py
Description : 
    Generates a 4-panel sequence illustrating the "Topological Heavy Seeds"
    and "Baryonic Camouflage" mechanisms.
    Panel 1: Naked Topological Super-Knot (Vacuum Torsion)
    Panel 2: Chiral Accretion (Lense-Thirring Centrifuge)
    Panel 3: Heavy Seed Ignition (Maximal Spin SMBH formation)
    Panel 4: Baryonic Camouflage (Mature SMBH hides the geometric seed)
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_spiral_data(num_particles, spirals=2, radius=1.0, spin_dir=1):
    """Generates spiral particle distributions for accretion disks."""
    theta = np.random.rand(num_particles) * 2 * np.pi * spirals
    r = radius * np.sqrt(np.random.rand(num_particles)) # Uniform area sampling
    # Tighten the spiral based on radius
    theta += spin_dir * (2.0 / (r + 0.1)) 
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y, r

def main():
    print("Generating ECF Heavy Seeds sequence (JWST updated timeline)...")

    # Aesthetic setup: dark background for space theme
    plt.style.use('dark_background')
    fig, axs = plt.subplots(2, 2, figsize=(12, 12), dpi=300)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    fig.suptitle('Evolution of Primordial Heavy Seeds in the ECF Framework', fontsize=18, fontweight='bold', color='white', y=0.96)

    # ---------------------------------------------------------
    # PANEL 1: Naked Topological Super-Knot
    # ---------------------------------------------------------
    ax1 = axs[0, 0]
    ax1.set_title(r'Phase I: Naked Super-Knot ($z \gg 25$)', fontsize=14, color='cyan')
    
    # Draw Torsion Field (Vector field)
    Y, X = np.mgrid[-2:2:15j, -2:2:15j]
    U = -Y / (X**2 + Y**2 + 0.5) # Rotational twist
    V = X / (X**2 + Y**2 + 0.5)
    ax1.quiver(X, Y, U, V, color='gray', alpha=0.5)
    
    # The knot itself
    ax1.scatter([0], [0], color='cyan', s=300, marker='x', linewidths=3)
    ax1.add_patch(patches.Circle((0, 0), 0.3, fill=False, color='cyan', linestyle='--', linewidth=2, alpha=0.8))
    
    # Fixed string formatting
    ax1.text(0, -2.5, r"Pure Vacuum Torsion Defect" + "\n" + r"Apparent Mass: $10^5 M_\odot$", color='white', ha='center', fontsize=11)
    
    # ---------------------------------------------------------
    # PANEL 2: Chiral Centrifuge (Lense-Thirring)
    # ---------------------------------------------------------
    ax2 = axs[0, 1]
    ax2.set_title(r'Phase II: Chiral Centrifuge ($z \approx 20$)', fontsize=14, color='orange')
    
    # Torsion field (weaker background)
    ax2.quiver(X, Y, U, V, color='gray', alpha=0.2)
    
    # Infalling Baryonic Gas
    x_gas, y_gas, r_gas = create_spiral_data(2000, spirals=3, radius=2.2)
    ax2.scatter(x_gas, y_gas, c=r_gas, cmap='autumn', s=5, alpha=0.6)
    ax2.scatter([0], [0], color='cyan', s=100, marker='x') # Seed still visible
    
    # Fixed string formatting
    ax2.text(0, -2.5, r"Lense-Thirring Centrifuge ($\Omega_L \sim 10^{-9}$ rad/yr)" + "\n" + r"Baryonic gas forced into rapid rotation", color='white', ha='center', fontsize=11)

    # ---------------------------------------------------------
    # PANEL 3: Heavy Seed Ignition (Maximal Spin)
    # ---------------------------------------------------------
    ax3 = axs[1, 0]
    ax3.set_title(r'Phase III: Heavy Seed Ignition ($z \approx 15$)', fontsize=14, color='yellow')
    
    # Dense Accretion Disk
    x_disk, y_disk, r_disk = create_spiral_data(5000, spirals=5, radius=1.5)
    ax3.scatter(x_disk, y_disk, c=r_disk, cmap='Wistia', s=8, alpha=0.8)
    
    # Forming Black Hole
    ax3.add_patch(patches.Circle((0, 0), 0.15, fill=True, color='black', zorder=5))
    ax3.add_patch(patches.Circle((0, 0), 0.18, fill=False, color='white', linewidth=1.5, zorder=6)) # Photon ring
    
    # Relativistic Jets
    ax3.plot([0, 0], [0, 2.2], color='cyan', linewidth=2, alpha=0.8, zorder=4)
    ax3.plot([0, 0], [0, -2.2], color='cyan', linewidth=2, alpha=0.8, zorder=4)
    
    # Fixed string formatting
    ax3.text(0, -2.5, r"Primordial SMBH Formation" + "\n" + r"Maximal Spin ($a^* \rightarrow 1$)", color='white', ha='center', fontsize=11)

    # ---------------------------------------------------------
    # PANEL 4: Baryonic Camouflage
    # ---------------------------------------------------------
    ax4 = axs[1, 1]
    ax4.set_title(r'Phase IV: Baryonic Camouflage ($z \approx 0$)', fontsize=14, color='lightgreen')
    
    # Extended Mature Disk
    x_mat, y_mat, r_mat = create_spiral_data(8000, spirals=8, radius=2.5)
    ax4.scatter(x_mat, y_mat, color='gray', s=2, alpha=0.4)
    ax4.scatter(x_disk*0.5, y_disk*0.5, c=r_disk, cmap='plasma', s=10, alpha=0.8) # Inner hot disk
    
    # Massive Mature SMBH
    ax4.add_patch(patches.Circle((0, 0), 0.5, fill=True, color='black', zorder=5))
    ax4.add_patch(patches.Circle((0, 0), 0.55, fill=False, color='white', linewidth=2, zorder=6)) # Event horizon
    
    # Fixed string formatting
    ax4.text(0, -2.5, r"Topological Seed fully screened" + "\n" + r"Mature SMBH Mass: $10^9 M_\odot$", color='white', ha='center', fontsize=11)

    # ---------------------------------------------------------
    # formatting for all panels
    # ---------------------------------------------------------
    for ax in axs.flat:
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-2.8, 2.8)
        ax.axis('off') # Hide axes for a clean space look

    # Save the figure
    output_filename = 'Fig_ECF_Heavy_Seeds.png'
    plt.savefig(output_filename, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Success! Saved as {output_filename}")

if __name__ == "__main__":
    main()
