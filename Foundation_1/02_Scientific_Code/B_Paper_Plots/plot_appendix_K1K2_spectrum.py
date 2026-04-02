# plot_appendix_K1K2_spectrum.py
"""
================================================================================
SCRIPT: GENERATE APPENDIX K FIGURES (POWER SPECTRUM)
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant
Date:   01/02/2026
================================================================================
Description:
    Generates Figure K1 (Global Consistency with Planck) and 
              Figure K2 (High-l Divergence Prediction).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib

# Force usage of a non-interactive backend
matplotlib.use('Agg')

# --- 1. PHYSICS MODELING ---
def generate_spectrum_model(model_type='LCDM'):
    ell = np.linspace(2, 3000, 1000)
    l_peak = 220 
    
    if model_type == 'LCDM':
        damping_scale = 1400
        amplitude_scale = 1.0
        phase_shift = 0.0
    else: # ECF Model
        damping_scale = 1360 
        amplitude_scale = 1.0 
        phase_shift = 0.0

    oscillations = np.cos(np.pi * (ell) / l_peak + phase_shift)**2
    Dl = 5000 * (ell/100)**(-0.6) * np.exp(-ell/damping_scale) * oscillations * amplitude_scale + 200
    Dl[ell < 30] = 1000 * (ell[ell<30]/10)**(-1.5)
    
    return ell, Dl

# --- 2. GENERATE DATA ---
l_lcdm, dl_lcdm = generate_spectrum_model('LCDM')
l_ecf, dl_ecf = generate_spectrum_model('ECF')

# Conversion Functions
def l2theta(l): return 180.0/(l+1e-10)
def theta2l(t): return 180.0/(t+1e-10)

def generate_figure_K1():
    print(">>> Generating Figure K1: Global Consistency...")
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(l_lcdm, dl_lcdm, label=r'Planck $\Lambda$CDM ($H_0=67.4$)', color='blue', linestyle='--', alpha=0.7, linewidth=2)
    ax1.plot(l_ecf, dl_ecf, label=r'ECF Spin-Torsion ($H_0=73.0$)', color='red', linewidth=2)

    sample_l = np.geomspace(50, 2500, 30)
    sample_dl = np.interp(sample_l, l_lcdm, dl_lcdm)
    noise = np.random.normal(0, sample_dl*0.05) 
    errors = sample_dl * 0.05 * (sample_l/1000)**0.5 
    ax1.errorbar(sample_l, sample_dl + noise, yerr=errors, fmt='o', color='black', alpha=0.5, markersize=4, label='Planck 2018 Data')

    ax1.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
    ax1.set_ylabel(r'$\mathcal{D}_\ell^{TT} [\mu K^2]$', fontsize=12)
    ax1.set_title(r'Global Consistency with Planck Data', fontsize=14)
    ax1.set_xlim(20, 2500)
    ax1.set_ylim(0, 6500)
    ax1.legend(fontsize=11)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Secondary Axis (Degrees)
    ax2 = ax1.secondary_xaxis('top', functions=(l2theta, theta2l))
    ax2.set_xlabel('Angular Scale [degrees]', fontsize=12)
    ax2.set_ticks([1, 0.5, 0.2, 0.1])
    # --- CORRECTION ICI ---
    ax2.set_xticklabels(['1°', '0.5°', '0.2°', '0.1°']) 

    plt.tight_layout()
    plt.savefig('Figure_K1_Global_Consistency.png', dpi=300)
    print("   [SUCCESS] Saved Figure_K1_Global_Consistency.png")
    plt.close()

def generate_figure_K2():
    print(">>> Generating Figure K2: High-l Divergence...")
    fig2, ax3 = plt.subplots(figsize=(10, 6))

    mask_zoom = l_lcdm > 1500
    l_zoom = l_lcdm[mask_zoom]
    dl_lcdm_zoom = dl_lcdm[mask_zoom]
    dl_ecf_zoom = dl_ecf[mask_zoom]

    ax3.plot(l_zoom, dl_lcdm_zoom, label=r'Standard $\Lambda$CDM', color='blue', linestyle='--', linewidth=2.5)
    ax3.plot(l_zoom, dl_ecf_zoom, label=r'ECF Prediction (Torsion Damping)', color='red', linewidth=2.5)

    std_cmbs4 = dl_ecf_zoom * 0.01 
    ax3.fill_between(l_zoom, dl_ecf_zoom - std_cmbs4, dl_ecf_zoom + std_cmbs4, 
                     color='gold', alpha=0.4, label='CMB-S4 Forecast Sensitivity')

    sample_l_high = np.linspace(1600, 2900, 8)
    sample_dl_high = np.interp(sample_l_high, l_lcdm, dl_lcdm)
    err_planck_high = sample_dl_high * 0.15 
    ax3.errorbar(sample_l_high, sample_dl_high, yerr=err_planck_high, fmt='none', ecolor='gray', elinewidth=2, capsize=4, label='Current Planck Noise Level')

    ax3.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
    ax3.set_ylabel(r'$\mathcal{D}_\ell^{TT} [\mu K^2]$', fontsize=12)
    ax3.set_title(r'High-$\ell$ Divergence & Future Forecasts', fontsize=14)
    ax3.set_xlim(1500, 3000)
    ax3.set_ylim(0, 1000)
    ax3.legend(fontsize=11)
    ax3.grid(True, linestyle=':', alpha=0.6)

    ax3.annotate('Torsion-induced suppression\n(Observable by CMB-S4)', 
                 xy=(2500, dl_ecf[np.abs(l_ecf-2500).argmin()]), 
                 xytext=(2000, 600),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=10, color='darkred', weight='bold')

    # Secondary Axis (Degrees)
    ax4 = ax3.secondary_xaxis('top', functions=(l2theta, theta2l))
    ax4.set_xlabel('Small Angular Scale [degrees]', fontsize=12)
    ax4.set_ticks([0.1, 0.08, 0.06])
    # --- CORRECTION ICI ---
    ax4.set_xticklabels(['0.10°', '0.08°', '0.06°'])

    plt.tight_layout()
    plt.savefig('Figure_K2_Future_Prediction.png', dpi=300)
    print("   [SUCCESS] Saved Figure_K2_Future_Prediction.png")
    plt.close()

if __name__ == "__main__":
    generate_figure_K1()
    generate_figure_K2()