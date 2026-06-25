"""
=============================================================================
Project:       Foundation II: The Chiral Universe
Script:        predict_roman_pbh.py
Author:        Pascal Fichant
Date:          February 2026 (New - Falsifiability Test)
Description:   Generates a prediction for the Nancy Grace Roman Space Telescope.
               Plots the expected microlensing event rate vs. Mass.
               The ECF model predicts a sharp peak of Primordial Black Holes (PBH)
               in the planetary mass range, distinguishable from astrophysical noise.
Output:        Fig6_Roman_PBH_Prediction.png
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

OUTPUT_FILE = "Fig6_Roman_PBH_Prediction.png"

def main():
    # 1. Setup Data Range (Log Space for Mass)
    # Range: 10^22 kg (Moon/Pluto size) to 10^29 kg (Brown Dwarf size)
    masses = np.logspace(22, 29, 1000) 
    
    # Constants for Reference
    M_Earth = 5.972e24  # kg
    M_Jupiter = 1.898e27 # kg
    
    # 2. Define the Background (Astrophysical Free-Floating Planets - FFPs)
    # Standard Model predicts fewer FFPs, mostly gas giants, broad distribution.
    # Modeled as a wide, low Gaussian centered near Jupiter mass.
    bg_amplitude = 20.0 
    bg_center = np.log10(M_Jupiter) # Center on Jupiter-mass objects
    bg_width = 1.5 
    
    background = bg_amplitude * np.exp(-0.5 * (np.log10(masses) - bg_center)**2 / bg_width**2)
    
    # 3. Define the ECF Signal (Primordial Black Holes)
    # ECF Theory predicts a sharp density of PBHs formed at the QCD transition/Torsion gap.
    # Peak is expected around Earth-mass (approx 10^24 - 10^25 kg).
    # This is the "Falsifiable Prediction".
    pbh_amplitude = 140.0 # High event rate due to DM density
    pbh_center = np.log10(5e24) # ~ Earth Mass
    pbh_width = 0.4 # Narrow formation window = Sharp Peak
    
    signal = pbh_amplitude * np.exp(-0.5 * (np.log10(masses) - pbh_center)**2 / pbh_width**2)
    
    # Total Rate = Signal + Background
    total_rate = background + signal

    # 4. Plotting
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plot background (Noise)
    ax.plot(masses, background, color='gray', linestyle='--', linewidth=2, label='Standard Noise (Free-Floating Planets)')
    
    # Plot Total Prediction (ECF)
    ax.plot(masses, total_rate, color='#DC143C', linewidth=3, label='ECF Prediction (PBH Signal)')
    
    # Fill the PBH Excess area
    ax.fill_between(masses, background, total_rate, color='#DC143C', alpha=0.2, label='PBH Excess (Torsion Signature)')
    
    # 5. Formatting & Annotations
    ax.set_xscale('log')
    ax.set_xlim(1e22, 1e29)
    ax.set_ylim(0, 180)
    
    # Axis Labels
    ax.set_xlabel(r'Lens Mass [kg]', fontsize=14, fontweight='bold')
    ax.set_ylabel(r'Microlensing Events / Year (Roman Telescope)', fontsize=14, fontweight='bold')
    
    # Title
    ax.set_title("Falsifiability: Roman Telescope Prediction", fontsize=16, fontweight='bold', pad=20)
    
    # Vertical Lines for Earth & Jupiter
    ax.axvline(M_Earth, color='blue', linestyle=':', alpha=0.6, linewidth=1.5)
    ax.text(M_Earth * 1.2, 170, r'$\leftarrow$ Earth Mass', color='blue', fontsize=10, va='top', fontweight='bold')
    
    ax.axvline(M_Jupiter, color='green', linestyle=':', alpha=0.6, linewidth=1.5)
    ax.text(M_Jupiter * 1.2, 30, r'$\leftarrow$ Jupiter Mass', color='green', fontsize=10, va='bottom', fontweight='bold')

    # Annotation for the Peak
    ax.annotate('Sharp PBH Peak\n(Planetary Mass)', 
                xy=(10**pbh_center, pbh_amplitude), 
                xytext=(1e26, 130),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                fontsize=12, fontweight='bold', color='#DC143C',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#DC143C", alpha=0.9))

    # Grid & Legend
    ax.grid(True, which="major", ls="-", alpha=0.3)
    ax.grid(True, which="minor", ls=":", alpha=0.1)
    
    ax.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
    
    # Explanation Text Box
    text_str = (
        "Falsifiability Condition:\n"
        "If Roman observes a smooth distribution (gray line),\n"
        "the ECF Torsion model is falsified.\n"
        "A sharp peak at $10^{24}-10^{25}$ kg confirms PBHs."
    )
    ax.text(0.02, 0.55, text_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle="round", facecolor="#FFFACD", alpha=0.8))

    # Save
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Figure saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()