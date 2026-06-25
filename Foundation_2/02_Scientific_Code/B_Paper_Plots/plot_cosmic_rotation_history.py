#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: The Chiral Universe
Script      : plot_cosmic_rotation_history.py
Description : 
    Generates the "Dilution of Cosmic Rotation" log-log plot: 'Fig5_Cosmic_Rotation_History.png'
    Crucially, it demonstrates the 'Kinematic Bifurcation':
    1. The global background dilutes to < 10^-13 rad/yr (Planck CMB limit).
    2. The local topological halos retain a chiral twist of ~ 10^-9 rad/yr.
    *PHYSICAL REALISM UPDATE*: The local ECF twist (red dashed line) 
    only originates AT the Topological Crystallization epoch (z ~ 1e10).
=============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt

def rad_yr_to_rad_s(val_rad_yr):
    """Converts radians per year to radians per second."""
    seconds_in_year = 365.25 * 24 * 3600
    return val_rad_yr / seconds_in_year

def main():
    print("Generating Cosmic Rotation History Plot (Strict Physical Model)...")

    # 1. PARAMETERS & CONVERSIONS
    # ---------------------------------------------------------
    z_factors = np.logspace(0, 32, 500)
    
    global_omega_today_rad_yr = 1e-13  # CMB Limit
    local_twist_today_rad_yr = 1e-9    # ECF Halo Twist
    
    global_omega_today_s = rad_yr_to_rad_s(global_omega_today_rad_yr)
    local_twist_today_s = rad_yr_to_rad_s(local_twist_today_rad_yr)

    # 2. CALCULATE EVOLUTION
    # ---------------------------------------------------------
    omega_global_s = global_omega_today_s * (z_factors ** 2)

    # 3. PLOT CREATION
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

    # Plot global background (Black line, exists for all time)
    ax.plot(z_factors, omega_global_s, color='black', linewidth=3, 
            label=r'Global Background $\omega \propto (1+z)^2$')

    # Plot local twist (Red dashed line, only exists AFTER crystallization: z=1 to z=1e10)
    ax.plot([1, 1e10], [local_twist_today_s, local_twist_today_s], color='red', linestyle='--', linewidth=2,
            label=r'ECF Local Halo Twist ($\sim 10^{-9}$ rad/yr)')

    # Markers for specific Cosmic Eras with explicit safe offsets
    eras = {
        'Today\n(CMB Limit)': (1, global_omega_today_s, 'blue', 'o', (15, -15), 'top', 'left'),
        'Recombination': (1100, global_omega_today_s * 1100**2, 'red', 'D', (15, -15), 'top', 'left'),
        'Matter-Rad Eq.': (3400, global_omega_today_s * 3400**2, 'green', 's', (-15, 15), 'bottom', 'right'),
        'Electroweak': (1e15, global_omega_today_s * (1e15)**2, 'purple', '^', (15, -15), 'top', 'left'),
        'Planck Bounce': (1e32, global_omega_today_s * (1e32)**2, 'orange', '*', (-15, 0), 'center', 'right')
    }

    # Plot markers and smart annotations
    for name, (z_fact, w_val, color, marker, offset, va, ha) in eras.items():
        ax.scatter(z_fact, w_val, color=color, s=120, marker=marker, zorder=5)
        
        # Add value explicitly for "Today"
        text_label = f"{name}\n< 1e-13 rad/yr" if "Today" in name else name
        
        # Using 'offset points' guarantees the text never touches the line
        ax.annotate(text_label, xy=(z_fact, w_val), xytext=offset, textcoords='offset points',
                    color=color, fontsize=10, fontweight='bold', va=va, ha=ha)

    # Topological Crystallization Arrow (Points exactly where the red line starts!)
    ax.annotate('Topological\nCrystallization\n(Kinematic Bifurcation)', xy=(1e10, local_twist_today_s), 
                xytext=(1e10, local_twist_today_s * 1e5),
                arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
                color='red', fontsize=11, fontweight='bold', ha='center', va='bottom')

    # Formatting
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(0.5, 1e34)
    ax.set_ylim(1e-22, 1e46)

    # Info Box
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    ax.text(0.05, 0.95, r'$\omega(z) = \omega_0(1+z)^2$' + '\nConservation of Angular Momentum\n' + r'$L \propto M R^2 \omega = const$', 
            transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=props)

    ax.set_xlabel(r'Redshift Factor $(1+z) = a_0/a(t)$', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Cosmic Angular Velocity $\omega(z)$ [rad/s]', fontsize=12, fontweight='bold')
    ax.set_title('The Dilution of Cosmic Rotation: Global vs Local Twist', fontsize=14, fontweight='bold')
    ax.grid(True, which="both", ls="--", alpha=0.3)
    
    # Legend safely placed
    ax.legend(loc='lower right', fontsize=11, bbox_to_anchor=(0.98, 0.12))

    # Save
    plt.tight_layout()
    output_filename = 'Fig5_Cosmic_Rotation_History.png'
    plt.savefig(output_filename)
    print(f"Success! Saved as {output_filename}")

if __name__ == "__main__":
    main()