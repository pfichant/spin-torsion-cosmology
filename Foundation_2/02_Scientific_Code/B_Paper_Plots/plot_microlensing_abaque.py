"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        plot_microlensing_abaque.py
Author:        Pascal Fichant
Date:          February 2026
Description:   Generates the Microlensing Parameter Space (Abaque) for the 
               ECF 10^24 kg Topological Defects (Micro-Knots).
               Panel A: Einstein Crossing Time (t_E) vs Lens Distance (D_L).
               Panel B: Magnification Heatmap (A) vs D_L and Impact Parameter.
Output:        Fig_Microlensing_Abaque.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

OUTPUT_FILE = "Fig_Microlensing_Abaque.png"

def main():
    print("Generating ECF Microlensing Abacus (Roman Space Telescope Prediction)...")

    # =========================================================================
    # 1. PHYSICAL CONSTANTS & ECF PARAMETERS
    # =========================================================================
    G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
    c = 299792458.0        # Speed of light (m/s)
    M_knot = 1e24          # Mass of ECF Micro-Knot (kg) - Planetary mass
    D_S_kpc = 8.0          # Distance to Source Star (Galactic Bulge) in kpc
    v_perp_km_s = 220.0    # Transverse velocity of the galactic halo (km/s)
    
    # Unit Conversions
    kpc_to_m = 3.085677581e19
    D_S_m = D_S_kpc * kpc_to_m
    v_perp_m_s = v_perp_km_s * 1000.0

    # Array of Lens Distances (D_L) from 0.1 kpc to 7.9 kpc
    D_L_kpc = np.linspace(0.1, 7.9, 500)
    D_L_m = D_L_kpc * kpc_to_m

    # =========================================================================
    # 2. CALCULATIONS (Einstein Radius & Time)
    # =========================================================================
    # Einstein Radius Equation: R_E = sqrt( (4GM/c^2) * (D_L * (D_S - D_L)) / D_S )
    term_1 = (4.0 * G * M_knot) / (c**2)
    term_2 = (D_L_m * (D_S_m - D_L_m)) / D_S_m
    R_E_m = np.sqrt(term_1 * term_2)

    # Einstein Crossing Time (t_E) in seconds, then converted to hours
    t_E_seconds = R_E_m / v_perp_m_s
    t_E_hours = t_E_seconds / 3600.0

    # Maximum time for annotation (occurs exactly at D_L = 4.0 kpc)
    max_t_E = np.max(t_E_hours)
    mid_kpc = 4.0

    # =========================================================================
    # 3. CALCULATIONS (Magnification Heatmap)
    # =========================================================================
    # Impact parameter u_min (normalized by R_E)
    u_min = np.linspace(0.1, 3.0, 500)
    
    # Create 2D grid for Heatmap
    U, D = np.meshgrid(u_min, D_L_kpc)
    
    # Magnification Equation: A = (u^2 + 2) / (u * sqrt(u^2 + 4))
    A_mag = (U**2 + 2.0) / (U * np.sqrt(U**2 + 4.0))

    # =========================================================================
    # 4. PLOTTING SETUP
    # =========================================================================
    # Increased height slightly to 7 to give room for the suptitle comfortably
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1, 1.25]})
    
    # The suptitle is placed at the top
    fig.suptitle('Microlensing Parameter Space for $10^{24}$ kg ECF Topological Defects', 
                 fontsize=16, fontweight='bold')

    # -------------------------------------------------------------------------
    # PANEL A: Transit Duration (t_E) vs Lens Distance
    # -------------------------------------------------------------------------
    ax1.plot(D_L_kpc, t_E_hours, color='#2c3e50', lw=3, label=r'Crossing Time $t_E$')
    
    # Fill the area under the curve to highlight the transient nature
    ax1.fill_between(D_L_kpc, 0, t_E_hours, color='#3498db', alpha=0.2)
    
    # Mark the absolute maximum at D_L = 4 kpc
    ax1.scatter([mid_kpc], [max_t_E], color='#e74c3c', s=80, zorder=5)
    ax1.annotate(f'Absolute Maximum\n$\\sim {max_t_E:.2f}$ hours\n(at 4 kpc)', 
                 xy=(mid_kpc, max_t_E), xytext=(mid_kpc, max_t_E - 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                 ha='center', va='top', fontsize=11, fontweight='bold', color='#c0392b')

    # Formatting Panel A
    ax1.set_title(r"A. Transit Duration Timescale ($t_E$)", fontsize=14, pad=15)
    ax1.set_xlabel(r"Distance to Lens $D_L$ [kpc] (Source $D_S = 8$ kpc)", fontsize=12)
    ax1.set_ylabel(r"Einstein Crossing Time $t_E$ [hours]", fontsize=12)
    ax1.set_xlim(0, 8)
    ax1.set_ylim(0, max_t_E * 1.2)
    ax1.grid(True, linestyle=':', alpha=0.7)
    
    # Add an observation cadence threshold line
    ax1.axhline(24.0, color='gray', linestyle='--', alpha=0.5)
    ax1.text(0.5, 24.5, "Historical Surveys (24h cadence) - Blind Spot", color='gray', fontsize=10)
    ax1.axhline(0.25, color='green', linestyle='--', alpha=0.8, lw=2)
    ax1.text(0.5, 0.3, "Roman Telescope Cadence (15 min)", color='green', fontsize=10, fontweight='bold')

    # -------------------------------------------------------------------------
    # PANEL B: Magnification Heatmap (Abaque)
    # -------------------------------------------------------------------------
    # MODERN SYNTAX: Use plt.get_cmap instead of plt.cm.get_cmap
    cmap = plt.get_cmap('magma')
    
    # Plot the heatmap (contourf)
    c = ax2.contourf(D, U, np.clip(A_mag, 1.0, 5.0), levels=50, cmap=cmap)
    
    # Add the critical threshold contour line (A = 1.34)
    contour_line = ax2.contour(D, U, A_mag, levels=[1.34], colors='white', linewidths=2.5, linestyles='dashed')
    ax2.clabel(contour_line, inline=True, fontsize=12, fmt="A = 1.34")

    # Formatting Panel B
    ax2.set_title(r"B. Magnification Abacus ($A$) vs Impact Parameter ($u_{min}$)", fontsize=14, pad=15)
    ax2.set_xlabel(r"Distance to Lens $D_L$ [kpc]", fontsize=12)
    ax2.set_ylabel(r"Impact Parameter $u_{min}$ [$R_E$ units]", fontsize=12)
    ax2.set_xlim(0.1, 7.9)
    ax2.set_ylim(0.1, 3.0)
    
    # Add Colorbar
    cbar = fig.colorbar(c, ax=ax2, pad=0.02)
    cbar.set_label(r'Magnification Factor ($A$)', fontsize=12, rotation=270, labelpad=20)
    cbar.set_ticks([1, 2, 3, 4, 5])
    cbar.set_ticklabels(['1.0', '2.0', '3.0', '4.0', '> 5.0'])

    # Annotation inside Panel B
    ax2.text(4.0, 0.5, "Definitive Detection Zone\n(Roman Space Telescope)", 
             color='white', fontsize=12, fontweight='bold', ha='center', va='center',
             bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))

    # =========================================================================
    # 5. FINAL ADJUSTMENTS & SAVE
    # =========================================================================
    # MANUAL MARGINS (Bulletproof method - replaces tight_layout)
    # top=0.85 ensures the suptitle has enough room. wspace=0.2 spaces the panels.
    fig.subplots_adjust(top=0.85, bottom=0.1, left=0.05, right=0.95, wspace=0.2)
    
    plt.savefig(OUTPUT_FILE, dpi=300, facecolor='white')
    print(f"[SUCCESS] Saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    