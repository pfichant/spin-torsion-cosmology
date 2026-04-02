"""
================================================================================
SCRIPT: Cosmic Energy Density Evolution (Friedmann Equations)
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant (2026)
Description: 
    Plots the evolution of background energy densities vs scale factor 'a'.
    Highlights the distinct scaling behavior:
    - Dark Energy (~ constant)
    - Matter (~ a^-3)
    - Radiation (~ a^-4)
    - Primordial Spin/Torsion (~ a^-6) -> Dominates the ultra-early universe.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Headless backend for server compatibility and Open Science
matplotlib.use('Agg')

# PRD Standard Formatting
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 13,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})

def plot_friedmann_densities():
    print(">>> Generating Figure: Evolution of Energy Densities (Figure 11)...")
    
    # Scale factor 'a' from the deep primordial era to today (log scale)
    a = np.logspace(-10, 0, 1000)
    
    # --- 1. THEORETICAL DENSITIES ---
    # Values are scaled for visual clarity (Arbitrary Units preserving the correct slopes)
    rho_lambda = 0.7 * np.ones_like(a)                  # Dark Energy (Constant)
    rho_matter = 0.3 * a**(-3)                          # Dust/Matter (a^-3)
    rho_rad    = 9.0e-5 * a**(-4)                       # Radiation (a^-4)
    
    # ECF Spin Density: Calibrated to dominate before Big Bang Nucleosynthesis (BBN)
    rho_spin   = 1.0e-17 * a**(-6)                      # Torsion/Spin (a^-6)

    # --- 2. FIGURE SETUP ---
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.12)

    # Plotting the densities on a log-log scale
    ax.plot(a, rho_spin,   color='purple', linestyle='-',  linewidth=3, label=r'Spin Density ($\rho_{spin} \propto a^{-6}$)')
    ax.plot(a, rho_rad,    color='red',    linestyle='--', linewidth=2, label=r'Radiation ($\rho_r \propto a^{-4}$)')
    ax.plot(a, rho_matter, color='blue',   linestyle='-.', linewidth=2, label=r'Matter ($\rho_m \propto a^{-3}$)')
    ax.plot(a, rho_lambda, color='green',  linestyle=':',  linewidth=2.5, label=r'Dark Energy ($\rho_\Lambda \approx$ const)')

    # --- 3. ANNOTATIONS & FORMATTING ---
    # The CRITICAL CORRECTION: Y-axis is absolute energy density, NOT Omega parameter!
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.set_xlim(1e-10, 1)
    ax.set_ylim(1e-2, 1e45) # Adjusted to show the a^-6 divergence clearly
    
    ax.set_xlabel(r'Scale Factor $a$', fontweight='bold')
    ax.set_ylabel(r'Energy Density $\rho_i(a)$ [Arbitrary Units]', fontweight='bold')
    ax.set_title('Dominance of Torsion in the Early Universe', fontsize=18, fontweight='bold', pad=15)
    
    # Add vertical lines for important epochs
    # Equality Matter-Radiation
    a_eq = 3.0e-4 
    ax.axvline(a_eq, color='gray', linestyle='-', alpha=0.3)
    ax.text(a_eq * 1.2, 1e5, 'Matter-Radiation\nEquality', color='gray', fontsize=11, rotation=90)

    # ECF Bounce / Spin Dominance epoch
    a_spin = 1.0e-7
    ax.axvline(a_spin, color='purple', linestyle='-', alpha=0.3)
    ax.text(a_spin * 1.2, 1e25, 'Spin Dominance\nEpoch', color='purple', fontsize=11, rotation=90)

    # Grid and Legend
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend(loc='upper right', framealpha=0.95, edgecolor='black')

    # --- 4. OUTPUT ---
    # Saving as JPG to perfectly match your LaTeX \includegraphics call
    filename = 'Figure_Friedmann_Evolution.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"    -> Saved successfully as {filename}")
    plt.close()

if __name__ == "__main__":
    plot_friedmann_densities()