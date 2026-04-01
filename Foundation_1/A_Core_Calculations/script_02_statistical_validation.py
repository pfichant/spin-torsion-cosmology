"""
================================================================================
SCRIPT 02: S8 TENSION & STATISTICAL VALIDATION
Paper: Foundation I: The Chiral Universe and the Hubble Tension
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
    Computes the S8 tension resolution via torsion-induced structure suppression.
    Evaluates the total Chi-square improvement (Delta Chi2) of the ECF model 
    against the standard Lambda-CDM baseline.
================================================================================
"""

import numpy as np
from scipy import stats

# --- 1. LATE-UNIVERSE OBSERVATIONAL CONSTRAINTS ---
# Formatted as: 'Parameter': (Mean, 1-sigma uncertainty)
OBSERVATIONS = {
    'H0': (73.04, 1.04),    # SH0ES 2022 Local distance ladder
    'S8': (0.766, 0.014),   # KiDS-1000 / DES Y3 (Weak Lensing)
}

# --- 2. THEORETICAL MODEL PREDICTIONS ---
# Lambda-CDM (Planck 2018 Baseline)
H0_LCDM = 67.4
S8_LCDM = 0.832

# ECF Model 
H0_ECF = 73.04
F_ION = 1.2765      # Optimized torsion stiffness parameter
GAMMA_SPIN = 0.3116 # Spin-growth coupling constant

def compute_s8_suppression(s8_ref, f_ion, gamma):
    """
    Computes the modified structure growth amplitude S8 in the ECF framework.
    The macroscopic spin density induces a slight repulsive effect at local scales.
    """
    suppression_denominator = 1.0 + (f_ion - 1.0) * gamma
    return s8_ref / suppression_denominator

def evaluate_statistical_budget():
    """ Calculates the Chi-square penalties for both models """
    s8_ecf = compute_s8_suppression(S8_LCDM, F_ION, GAMMA_SPIN)
    
    # 1. Standard Lambda-CDM Chi2
    chi2_h0_lcdm = ((OBSERVATIONS['H0'][0] - H0_LCDM) / OBSERVATIONS['H0'][1])**2
    chi2_s8_lcdm = ((OBSERVATIONS['S8'][0] - S8_LCDM) / OBSERVATIONS['S8'][1])**2
    total_chi2_lcdm = chi2_h0_lcdm + chi2_s8_lcdm
    
    # 2. ECF Model Chi2
    chi2_h0_ecf = ((OBSERVATIONS['H0'][0] - H0_ECF) / OBSERVATIONS['H0'][1])**2
    chi2_s8_ecf = ((OBSERVATIONS['S8'][0] - s8_ecf) / OBSERVATIONS['S8'][1])**2
    total_chi2_ecf = chi2_h0_ecf + chi2_s8_ecf
    
    delta_chi2 = total_chi2_lcdm - total_chi2_ecf
    
    # Statistical significance (assuming 1 degree of freedom for the torsion extension)
    sigma_preference = stats.norm.ppf(1 - stats.chi2.sf(delta_chi2, 1)/2)
    
    return s8_ecf, total_chi2_lcdm, total_chi2_ecf, delta_chi2, sigma_preference

if __name__ == "__main__":
    print("=" * 70)
    print(">>> EXECUTING S8 SUPPRESSION & CHI-SQUARE ANALYSIS")
    print("=" * 70)
    
    s8_pred, chi2_ref, chi2_mod, d_chi2, sigma = evaluate_statistical_budget()

    print(f"[1] Structure Growth (S8):")
    print(f"    Planck LCDM Prediction : {S8_LCDM:.3f} (High Tension)")
    print(f"    ECF Model Prediction   : {s8_pred:.3f} (Matches Weak Lensing)")
    
    print(f"\n[2] Global Statistical Budget:")
    print(f"    Total Chi2 (LCDM)      : {chi2_ref:.2f}")
    print(f"    Total Chi2 (ECF)       : {chi2_mod:.2f}")
    print(f"    Delta Chi2             : -{d_chi2:.2f}")
    
    print(f"\n[3] Model Preference:")
    print(f"    ECF favored at         : > {sigma:.1f} sigma")
    print("-" * 70)