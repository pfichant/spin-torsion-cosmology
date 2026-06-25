"""
=============================================================================
FILENAME       : plot_ecf_mass_comparison_final.py
DESCRIPTION    : Plots Cumulative Mass (Halo vs Visible) & Ratio.
                 Includes Visible Matter Curve as requested.
Output         : Fig1_ECF_Mass_Comparison.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 1. PARAMETERS (Derived from SPARC Data - v1.0.3) ---
M_sun = 1.989e30        
kpc_to_m = 3.086e19     
g_cm3_to_kg_m3 = 1000.0 

# ECF Model (Best Fit parameters for NGC 6503 - Table 4)
# --- CORRECTION v1.0.3 ---
log_rho0 = -23.25                      
rho0 = (10**log_rho0) * g_cm3_to_kg_m3 
Rs_kpc = 1.70                          
Rs = Rs_kpc * kpc_to_m                 

# Baryons (Observed Data approximation)
M_baryon_total_Msun = 6.4e9            
M_b_tot = M_baryon_total_Msun * M_sun  
Rd_kpc = 2.0  # Rayon d'échelle du disque baryonique (approx)

# --- 2. FUNCTIONS ---
def mass_halo_ecf(r_kpc):
    """Cumulative Dark Matter Mass (kg) - Pseudo-Isothermal Profile"""
    r = r_kpc * kpc_to_m
    x = r / Rs
    # Mass enclose M(<r) = 4*pi*rho0*Rs^3 * (r/Rs - atan(r/Rs))
    mass = 4 * np.pi * rho0 * (Rs**3) * (x - np.arctan(x))
    return mass

def mass_baryons(r_kpc):
    """Cumulative Baryonic Mass (Freeman Disk approximation)"""
    # M(<R) = M_tot * (1 - (1 + R/Rd)*exp(-R/Rd))
    x = r_kpc / Rd_kpc
    return M_b_tot * (1 - (1 + x) * np.exp(-x))

def main():
    # Grid
    r_values_kpc = np.linspace(0.1, 50, 500)
    
    # Calculations
    m_halo_kg = mass_halo_ecf(r_values_kpc)
    m_bar_kg = mass_baryons(r_values_kpc)
    
    # Convert to Solar Masses for plotting
    m_halo_msun = m_halo_kg / M_sun
    m_bar_msun = m_bar_kg / M_sun
    
    # Calculate Local Ratio (avoid div by zero)
    ratio_mass = np.divide(m_halo_kg, m_bar_kg, out=np.zeros_like(m_halo_kg), where=m_bar_kg!=0)

    # --- 3. PLOTTING ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_halo = 'tab:blue'
    color_bar = 'tab:green'
    color_ratio = 'tab:red'

    # Left Axis: Cumulative Mass (Solar Masses)
    ax1.set_xlabel('Radius [kpc]', fontsize=12, fontweight='bold')
    ax1.set_ylabel(r'Cumulative Mass [$M_\odot$]', color='black', fontsize=12)
    
    # Plot Halo Mass
    lns1 = ax1.semilogy(r_values_kpc, m_halo_msun, color=color_halo, lw=3, label="ECF Halo Mass ($M_{DM}$)")
    
    # Plot Baryon Mass (Visible Matter) - NEW CURVE
    lns2 = ax1.semilogy(r_values_kpc, m_bar_msun, color=color_bar, lw=2.5, linestyle='-.', label="Visible Baryonic Mass ($M_{bar}$)")
    
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim(1e8, 1e12) # Adjusted limits for Mass
    ax1.grid(True, which="both", ls=":", alpha=0.3)

    # Right Axis: Mass Ratio
    ax2 = ax1.twinx() 
    ax2.set_ylabel(r"Local Mass Ratio ($\Omega_{DM} / \Omega_b$)", color=color_ratio, fontsize=12)
    ax2.set_ylim(0, 25)
    ax2.tick_params(axis='y', labelcolor=color_ratio)

    lns3 = ax2.plot(r_values_kpc, ratio_mass, color=color_ratio, lw=2.0, linestyle='--', label="Mass Ratio (Right Axis)")
    
    # Cosmic Average Line
    lns4 = ax2.plot([0, 50], [5.3, 5.3], color='grey', linestyle=':', lw=1.5, alpha=0.8, label="Cosmic Avg (~5.3)")

    # Legend (Combined)
    lns = lns1 + lns2 + lns3 + lns4
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left', frameon=True, fontsize=10)

    # Annotations
    ax1.text(35, 2e9, "Visible Disk Ends", color=color_bar, fontsize=10, ha='center')
    ax1.text(35, 2e11, "Dark Halo Dominates", color=color_halo, fontsize=10, ha='center')
    
    # Title
    plt.title(f"ECF Halo vs Visible Mass (NGC 6503)\n$R_s={Rs_kpc}$ kpc, $\\log(\\rho_0)={log_rho0}$", fontsize=14, pad=15)
    
    plt.tight_layout()
    plt.savefig("Fig1_ECF_Mass_Comparison.png", dpi=300)
    print(f"[OK] Generated Fig1_ECF_Mass_Comparison.png with Rs={Rs_kpc} kpc")

if __name__ == "__main__":
    main()