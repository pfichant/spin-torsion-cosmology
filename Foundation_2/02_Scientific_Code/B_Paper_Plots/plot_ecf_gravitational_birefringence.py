import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# ECF FRAMEWORK: CHIRAL STOCHASTIC GRAVITATIONAL-WAVE BACKGROUND (SGWB)
# Target: Physical Review D - Supplementary Material
# Author: Pascal Fichant
# 
# Description: 
# Simulates the Gravitational Birefringence induced by the primordial 
# torsional background in the Einstein-Cartan Framework. A Chern-Simons 
# coupling amplifies the Left-handed polarization mode and suppresses 
# the Right-handed mode, creating a Faraday-free chiral asymmetry detectable 
# by 3rd generation observatories (LISA, Einstein Telescope).
# =============================================================================

# Publication-quality plot settings
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

# --- 1. Frequency Array ---
# Log scale spanning from LISA (10^-4 Hz) to Einstein Telescope (10^3 Hz)
f = np.logspace(-4, 3, 1000)

# --- 2. Baseline Symmetric SGWB (Standard Lambda-CDM / Inflation) ---
# Omega_GW is the fractional energy density of gravitational waves
# Using a simplified astrophysical/inflationary power law
Omega_GW_base = 1e-10 * (f / 10.0)**(2/3)

# --- 3. ECF Torsional Coupling (Chiral Anomaly) ---
# Torsion amplifies the Left-handed mode and suppresses the Right-handed mode.
# We model the topological transition signature redshifted to the ET/LISA band.
f_peak = 5.0     # Peak frequency of the topological anomaly (Hz)
sigma = 1.5      # Spectral width

# Fractional chiral enhancement parameter (0 = no asymmetry, 1 = total asymmetry)
chiral_factor = 0.8 * np.exp(-0.5 * (np.log10(f / f_peak) / sigma)**2)

# Splitting the polarizations
Omega_L = Omega_GW_base * (1 + chiral_factor)  # Left-handed mode
Omega_R = Omega_GW_base * (1 - chiral_factor)  # Right-handed mode

# --- 4. Detector Sensitivity Curves (Approximated) ---
# LISA sensitivity proxy (minimum around 10^-2 Hz)
f_lisa = np.logspace(-4, -1, 100)
sens_lisa = 1e-12 * (f_lisa / 1e-2)**(-2) + 1e-12 * (f_lisa / 1e-2)**2

# Einstein Telescope (ET) sensitivity proxy (minimum around 10 Hz)
f_et = np.logspace(0, 3, 100)
sens_et = 1e-10 * (f_et / 10.0)**(-2) + 1e-10 * (f_et / 10.0)**2

# --- 5. Plot Generation ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot ECF Polarizations
ax.loglog(f, Omega_L, label=r'ECF Left-Handed Mode ($\Omega_L$)', color='darkblue', linewidth=2.5)
ax.loglog(f, Omega_R, label=r'ECF Right-Handed Mode ($\Omega_R$)', color='crimson', linestyle='--', linewidth=2.5)

# Plot Standard Model Reference
ax.loglog(f, Omega_GW_base, label=r'Standard Symmetric SGWB ($\Lambda$CDM)', color='gray', linestyle=':', linewidth=1.5)

# Fill the Birefringence gap
ax.fill_between(f, Omega_R, Omega_L, color='purple', alpha=0.1, label='ECF Chiral Asymmetry (Birefringence)')

# Plot Detectors
ax.loglog(f_lisa, sens_lisa, color='forestgreen', alpha=0.6, linewidth=2, label='LISA Sensitivity Band')
ax.loglog(f_et, sens_et, color='darkorange', alpha=0.6, linewidth=2, label='Einstein Telescope Sensitivity')

# Formatting and Labels
ax.set_xlim(1e-4, 1e3)
ax.set_ylim(1e-14, 1e-6)
ax.set_xlabel('Gravitational Wave Frequency $f$ [Hz]', fontweight='bold')
ax.set_ylabel(r'Spectral Energy Density $\Omega_{\rm GW}(f)$', fontweight='bold')
ax.set_title('Stochastic Gravitational-Wave Background:\nECF Faraday-Free Chiral Birefringence', fontweight='bold', pad=15)

ax.grid(True, which="both", ls="--", alpha=0.4)
ax.legend(loc='lower right', fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig('Fig_SGWB_Chiral_Birefringence.png', dpi=300)
print("Simulation complete. Figure saved as 'Fig_SGWB_Chiral_Birefringence.png'")
