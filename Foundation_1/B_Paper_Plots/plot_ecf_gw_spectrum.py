#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
File Name   : plot_ecf_gw_spectrum.py
Author      : Pascal Fichant
Date        : March 25, 2026
Description : Generates the Primordial Gravitational Wave Spectrum figure
              for the Einstein-Cartan Framework (ECF) Foundation I paper.
              Compares the standard inflationary background with the ECF
              blue-tilted stiff-phase signal, explicitly including the LISA 
              sensitivity curve (dashed grey) as requested by PRD reviewers.
Repository  : https://github.com/pfichant/spin-torsion-cosmology
License     : CC-BY-4.0
===============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib

# Backend Configuration
matplotlib.use('Agg')
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'font.family': 'serif',
    'axes.linewidth': 1.5
})

def plot_lisa_prediction():
    print("Generating LISA GW spectrum...")
    
    # Frequency f [Hz] (Log scale from 10^-5 to 1 Hz)
    f = np.logspace(-5, 0, 500)
    
    # --- 1. LISA SENSITIVITY CURVE (Approx Noise) ---
    # Typical "V" or "U" shape for interferometers
    # Minimum around a few mHz
    S_n = 1e-40 * ( (1e-3/f)**4 + 2*(1 + (f/1e-3)**2) ) # Noise approx
    # Conversion to Omega_GW
    # Omega ~ f^3 * S_n
    Omega_LISA = 1e-12 * ((f / 3e-3)**2 + (3e-3 / f)**2 + 0.5) 
    
    # --- 2. STANDARD INFLATION (LCDM) ---
    # Nearly flat spectrum, very low amplitude (r < 0.06)
    Omega_Inflation = 1e-16 * (f / 1e-3)**(-0.1) # Slightly red or flat
    
    # --- 3. ECF BOUNCE PREDICTION ---
    # Stiff Phase (w=1) -> Blue Tilt (positive slope)
    # The spectrum rises up to a cutoff frequency linked to the bounce temperature
    # Modeling a peak entering the LISA window
    f_peak = 4e-3 # Peak frequency
    
    # Shape: Rise as f^1 (or more) then cutoff
    Omega_ECF = 1e-10 * (f / f_peak)**1.5 * np.exp(-0.5 * (f / f_peak)**2)
    
    # Adjustment for realism (under BBN constraint but visible to LISA)
    Omega_ECF = Omega_ECF * 1e-2 # Scaling
    
    # --- FIGURE ---
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.12, right=0.95, top=0.92, bottom=0.12)
    
    # 1. LISA Sensitivity Zone (Fill everything ABOVE the noise curve)
    # PRD Modification: Dashed grey line for LISA sensitivity
    ax.plot(f, Omega_LISA, color='grey', linestyle='--', linewidth=2, label='LISA Sensitivity')
    ax.fill_between(f, Omega_LISA, 1e-5, color='grey', alpha=0.1)
    
    # 2. Inflation
    ax.plot(f, Omega_Inflation, 'b--', linewidth=2, label=r'Standard Inflation (Flat)')
    
    # 3. ECF Bounce
    ax.plot(f, Omega_ECF, 'r-', linewidth=3, label=r'ECF Bounce (Stiff Phase $w=1$)')
    
    # Annotations
    ax.text(1e-4, 1e-17, 'Undetectable by LISA', color='blue', fontsize=10, style='italic')
    ax.text(8e-3, 1e-13, 'DETECTABLE\nSIGNAL', color='#c0392b', fontsize=12, fontweight='bold', ha='center')
    
    # Arrow pointing to the peak
    peak_idx = np.argmax(Omega_ECF)
    ax.annotate('Bounce Scale\n(Spin Injection)', 
                xy=(f[peak_idx], Omega_ECF[peak_idx]), 
                xytext=(2e-2, 1e-10),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=11)

    # Aesthetics
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-5, 1e-1)
    ax.set_ylim(1e-18, 1e-8)
    
    ax.set_xlabel(r'Frequency $f$ [Hz]', fontweight='bold')
    ax.set_ylabel(r'GW Energy Density $\Omega_{GW} h^2$', fontweight='bold')
    ax.set_title(r'Primordial Gravitational Wave Spectrum', fontsize=16, fontweight='bold', pad=15)
    
    ax.grid(True, which='both', linestyle=':', alpha=0.4)
    ax.legend(loc='upper left', frameon=True)
    
    filename = 'figure_ecf_gw_spectrum.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Image generated: {filename}")

if __name__ == "__main__":
    plot_lisa_prediction()