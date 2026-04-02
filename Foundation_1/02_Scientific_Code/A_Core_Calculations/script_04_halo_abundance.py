# script_04_halo_abundance.py
# Paper: Foundation I - High-Redshift Halo Density Check
# Author: Pascal Fichant (2026)
# Description: Calculates the cumulative halo number density at z=15 
# using the Press-Schechter formalism with ECF Model parameters.

import numpy as np
from scipy.special import erfc
import math

# --- 1. MODEL PARAMETERS (From Previous Scripts) ---
H0 = 73.04                # km/s/Mpc
h = H0 / 100.0
OMEGA_M = 0.315           # Matter density
SIGMA_8_ECF = 0.766       # The value found in Script 02 (Solving S8 tension)
NS = 0.965                # Spectral index
DELTA_C = 1.686           # Critical overdensity for collapse

# --- 2. PHYSICS FUNCTIONS ---

def growth_factor_approx(z, omega_m):
    """Approximate growth factor D(z) for high z (Matter dominated).
    D(z) ~ 1/(1+z) normalized to D(0)=1 is too simple.
    We use the Carroll, Press & Turner approximation or simple (1+z) scaling
    valid at z=15 where Omega_m(z) ~ 1.
    """
    # At z=15, the Universe is matter dominated, so D(z) scales as 1/(1+z)
    # accurately enough for this order of magnitude check.
    return 1.0 / (1.0 + z)

def sigma_mass(M, sigma_8, omega_m, h_val):
    """
    Extrapolates sigma(M) from sigma_8 assuming a power law P(k) ~ k^n.
    Standard approximation: sigma(M) = sigma_8 * (M / M_8)^(-alpha)
    """
    # Mass contained in 8 Mpc/h sphere
    rho_crit = 2.775e11 # h^2 M_sun / Mpc^3
    rho_m = omega_m * rho_crit # h^2 M_sun / Mpc^3
    R8 = 8.0 # Mpc/h
    M8 = (4.0/3.0) * np.pi * R8**3 * rho_m
    
    # Slope alpha ~ (n_s + 3) / 6 for cluster scales, 
    # but steeper for galaxy scales. Effective index n_eff at high k is ~ -2.3
    # alpha = (n_eff + 3) / 6. Let's use standard LambdaCDM calculator approx.
    # At 10^10 M_sun, alpha is approx 0.25 - 0.3.
    alpha = 0.28 
    
    return sigma_8 * (M / M8)**(-alpha)

def number_density_ps(M_min_h, z):
    """
    Calculates cumulative number density n(>M) in (Mpc/h)^3 using Press-Schechter.
    """
    # 1. Background Density
    rho_crit = 2.775e11 # h^2 M_sun / Mpc^3
    rho_mean = OMEGA_M * rho_crit
    
    # 2. Variance at mass M and redshift z
    D_z = growth_factor_approx(z, OMEGA_M)
    sigma_M_z0 = sigma_mass(M_min_h, SIGMA_8_ECF, OMEGA_M, h)
    sigma_M_z = sigma_M_z0 * D_z
    
    # 3. Nu parameter
    nu = DELTA_C / sigma_M_z
    
    # 4. Press-Schechter Cumulative Function
    # n(>M) = int_M^inf (dn/dM) dM
    # Analytical approx for high mass tail:
    # n(>M) ~ (rho_m / M) * erfc(nu / sqrt(2)) 
    # (Note: This is an order of magnitude estimator)
    
    n_cum = (rho_mean / M_min_h) * erfc(nu / np.sqrt(2.0))
    return n_cum

# --- 3. CALCULATION AT z=15 ---
TARGET_Z = 15.0
TARGET_DENSITY = 1.0e-4 # Mpc^-3 -> We need to convert h units

print(f"{'='*60}")
print(f"--- SCRIPT 04: JWST HALO ABUNDANCE CHECK (z={TARGET_Z}) ---")
print(f"{'='*60}")
print(f"Model: ECF (Sigma_8 = {SIGMA_8_ECF})")

# Scan masses to find where density hits 10^-4
masses = [1e8, 5e8, 1e9, 5e9, 1e10, 5e10] # h^-1 M_sun

found_mass = False
for M in masses:
    # Density in (h/Mpc)^3
    n_h3 = number_density_ps(M, TARGET_Z)
    
    # Convert to physical Mpc^-3: n_phys = n_h3 * h^3
    n_phys = n_h3 * h**3
    
    print(f"Mass > {M:.1e} h^-1 M_sun : n = {n_phys:.2e} Mpc^-3")
    
    if 9e-5 < n_phys < 5e-4:
        print(f"   >>> MATCH FOUND! This density matches the 10^-4 claim.")
        print(f"   >>> Interpretation: JWST objects correspond to halos of ~{M:.1e} M_sun.")

print(f"{'='*60}")