
"""
plot_ecf_lithium_resolution.py

This script generates a plot demonstrating the resolution of the Primordial 
Lithium-7 anomaly within the Extended Cosmic Framework (ECF). 

It compares the Standard Model (Lambda-CDM) Beryllium-7 production 
(which leads to the Lithium overabundance) against the ECF model, 
where high-energy gamma rays from the Primordial Topological Annihilation 
(PTA) tail actively photodisintegrate the Beryllium, resulting in the 
observed 1/3 survival factor.

output: fig_ecf_lithium_resolution.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

def generate_lithium_plot():
    # --- 1. Time Array Configuration ---
    # Cosmic time from 0.1s to 1000s (Covering the BBN and 'Furnace' epochs)
    t = np.logspace(-1, 3, 1000)

    # --- 2. Standard Model Physics (Lambda-CDM) ---
    # Simulating the standard production of Beryllium-7 (progenitor of Li-7)
    # It starts forming significantly around 10-20s and plateaus.
    # We use a hyperbolic tangent function to smoothly simulate this step.
    Y_Be_std = 0.5 * (1 + np.tanh((np.log10(t) - 1.5) * 2.5))

    # --- 3. ECF Phenomenological Physics ---
    # The PTA Tail (Gamma-ray injection rate)
    # Peaks around 1s and decays exponentially.
    tau_pta = 5.0 # Decay time constant of the PTA tail in seconds
    injection_rate = np.exp(-t / tau_pta) * (t > 0.5)

    # Calculating the ECF destruction of Be-7 via Photodisintegration
    # The target optical depth to achieve the 1/3 survival factor is ln(3) ~= 1.1
    target_optical_depth = np.log(3) 
    coupling_constant = target_optical_depth / np.trapezoid(injection_rate, t)
    
    # The optical depth accumulates over time
    destruction_integral = cumulative_trapezoid(injection_rate * coupling_constant, t, initial=0)
    
    # Survival factor is e^(-tau)
    survival_factor = np.exp(-destruction_integral)

    # Final ECF Abundance = Standard Abundance * Survival Factor
    Y_Be_ECF = Y_Be_std * survival_factor

    # --- 4. Plotting ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # X-axis settings
    ax1.set_xscale('log')
    ax1.set_xlabel('Cosmic Time (Seconds)', fontsize=12, fontweight='bold')
    ax1.set_xlim(0.1, 1000)

    # Primary Y-axis (Abundance)
    ax1.set_ylabel(r'Relative Abundance of $^7$Be ($\propto$ $^7$Li)', fontsize=12, fontweight='bold', color='black')
    ax1.set_ylim(-0.05, 1.1)

    # Plotting the abundance curves
    line1, = ax1.plot(t, Y_Be_std, 'k--', linewidth=2.5, label=r'$\Lambda$CDM Production (Overabundance)')
    line2, = ax1.plot(t, Y_Be_ECF, color='#d62728', linewidth=3, label='ECF Survival (Observed: 1/3 factor)')

    # Shaded area representing the destroyed Lithium/Beryllium
    ax1.fill_between(t, Y_Be_ECF, Y_Be_std, color='red', alpha=0.1, label='Destroyed $^7$Be (Photodisintegration)')

    # Secondary Y-axis (Gamma Flux / PTA Tail)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Gamma Photodisintegration Rate (PTA Tail)', fontsize=12, fontweight='bold', color='#1f77b4')
    line3, = ax2.plot(t, injection_rate, color='#1f77b4', linewidth=2, linestyle='-.', label=r'ECF Gamma Flux ($\Gamma_{\gamma}^{ECF}$)')
    ax2.set_ylim(-0.05, 1.1)
    ax2.tick_params(axis='y', labelcolor='#1f77b4')

    # Visualizing the "Furnace Epoch" (1s to 10s)
    ax1.axvspan(1, 10, color='gray', alpha=0.15)
    ax1.text(1.5, 0.5, 'The "Furnace"\n(PTA Tail &\nGamma Rays)', fontsize=10, rotation=0, verticalalignment='center',
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

    # Global Legend handling (combining both axes)
    lines = [line1, line2, line3]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', fontsize=11, framealpha=0.9)

    # Title and grid
    plt.title('Resolution of the Primordial Lithium Anomaly via ECF Photodisintegration', fontsize=14, fontweight='bold')
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    
    # Layout adjustments and save
    plt.tight_layout()
    output_filename = 'fig_ecf_lithium_resolution.png'
    plt.savefig(output_filename, dpi=300)
    print(f"Plot successfully saved as '{output_filename}'")
    # plt.show()

if __name__ == "__main__":
    generate_lithium_plot()

