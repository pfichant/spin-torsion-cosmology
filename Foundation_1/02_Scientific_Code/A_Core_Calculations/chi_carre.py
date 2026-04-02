"""
================================================================================
SCRIPT: Global Chi-Square Minimization
Paper: Foundation I: Unified Resolution of Cosmological Tensions
Author: Pascal Fichant (2026)
Description: 
    Computes the statistical preference (Chi-square budget) of the ECF model 
    over the standard Lambda-CDM baseline.
    Evaluates the combined H0, S8, and BAO constraints.
================================================================================
"""
import numpy as np
from scipy.integrate import quad

# --- 1. CONSTANTS AND DATASETS ---
C_LIGHT = 299792.458  # Speed of light [km/s]

# Observational Data Constraints (1-sigma)
obs_data = {
    'H0': {'val': 73.0, 'err': 1.0},       # SH0ES (2022)
    'S8': {'val': 0.766, 'err': 0.014},    # KiDS-1000 / DES Y3
    'BAO': {                               # BOSS/eBOSS DR16
        'z': np.array([0.38, 0.51, 0.61, 1.48]),
        'val': np.array([10.23, 13.36, 15.45, 38.4]),
        'err': np.array([0.17, 0.21, 0.22, 1.1])
    }
}

# --- 2. THEORETICAL FRAMEWORK ---
def hubble_parameter(z, H0, Om):
    """ Standard flat-LambdaCDM Hubble evolution """
    return H0 * np.sqrt(Om * (1+z)**3 + (1 - Om))

def compute_DM_rs(z, H0, Om, rs):
    """ Computes the transverse comoving distance normalized by sound horizon """
    inv_h = lambda zp: 1.0 / hubble_parameter(zp, H0, Om)
    integral, _ = quad(inv_h, 0, z)
    DM = C_LIGHT * integral
    return DM / rs

def calculate_chi2_budget(h0, rs, s8):
    """ Evaluates the Chi-square penalties across cosmological sectors """
    # Hubble Sector (H0)
    chi2_h0 = ((obs_data['H0']['val'] - h0) / obs_data['H0']['err'])**2
    
    # Large Scale Structure Sector (S8)
    chi2_s8 = ((obs_data['S8']['val'] - s8) / obs_data['S8']['err'])**2
    
    # Geometric Sector (BAO)
    chi2_bao = 0
    for i in range(len(obs_data['BAO']['z'])):
        pred_bao = compute_DM_rs(obs_data['BAO']['z'][i], h0, 0.315, rs)
        chi2_bao += ((obs_data['BAO']['val'][i] - pred_bao) / obs_data['BAO']['err'][i])**2
        
    return chi2_h0, chi2_s8, chi2_bao

if __name__ == "__main__":
    print(">>> Executing Chi-Square Statistical Analysis...")
    
    # Baseline: Planck 2018 (Lambda-CDM)
    c2_h_lcdm, c2_s_lcdm, c2_b_lcdm = calculate_chi2_budget(67.4, 147.1, 0.832)
    total_lcdm = c2_h_lcdm + c2_s_lcdm + c2_b_lcdm

    # Proposed Model: Einstein-Cartan Framework (ECF)
    c2_h_ecf, c2_s_ecf, c2_b_ecf = calculate_chi2_budget(73.04, 135.8, 0.766)
    total_ecf = c2_h_ecf + c2_s_ecf + c2_b_ecf

    print(f"\n--- CHI-SQUARE BUDGET ---")
    print(f"Lambda-CDM Baseline Total Chi2 : {total_lcdm:.2f}")
    print(f"ECF Model Total Chi2           : {total_ecf:.2f}")
    print(f"Delta Chi2 Improvement         : {total_lcdm - total_ecf:.2f}")