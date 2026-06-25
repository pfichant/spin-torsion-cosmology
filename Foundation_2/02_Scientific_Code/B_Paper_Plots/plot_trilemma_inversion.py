
"""
=========================================================================================
SUPPLEMENTARY MATERIAL FOR "FOUNDATION II: THE CHIRAL UNIVERSE"
=========================================================================================
Title: Axion Dynamics Optimization with Quintessence Peak at z=0.63
Author: Pascal Fichant
Target Journal: Physical Review D (PRD)

DESCRIPTION:
This script uses a Global Genetic Algorithm to solve the H0-Age-BAO trilemma by 
shifting the Axion quintessence recovery peak to z=0.63. This test aims to reduce 
the BAO drift while maintaining a 13.5 Gyr cosmic age.
=========================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import differential_evolution
import warnings

warnings.filterwarnings("ignore")

# ====================================================================
# 1. PARAMÈTRES COSMOLOGIQUES
# ====================================================================
H0 = 73.0
Omega_m0 = 0.315
Omega_de0 = 1.0 - Omega_m0
c_km_s = 299792.458
z_bao_target = 1.5
TARGET_AGE = 13.5  

# ====================================================================
# 2. NOYAUX D'INTÉGRATION
# ====================================================================
def de_density_integrand(z, w_func):
    return 3.0 * (1.0 + w_func(z)) / (1.0 + z)

def E_z(z, w_func):
    integral_w, _ = quad(de_density_integrand, 0, z, args=(w_func,))
    rho_de_ratio = np.exp(integral_w)
    return np.sqrt(Omega_m0 * (1.0 + z)**3 + Omega_de0 * rho_de_ratio)

def compute_cosmic_age(w_func):
    integral, _ = quad(lambda z: 1.0 / ((1.0 + z) * E_z(z, w_func)), 0, np.inf, limit=1000)
    return integral / (H0 * 1.02271e-3)

def compute_comoving_distance(w_func, z_target):
    integral, _ = quad(lambda z: 1.0 / E_z(z, w_func), 0, z_target)
    return (c_km_s / H0) * integral

def w_lcdm(z): return -1.0
age_lcdm = compute_cosmic_age(w_lcdm)
dm_lcdm = compute_comoving_distance(w_lcdm, z_bao_target)

# ====================================================================
# 3. ALGORITHME GÉNÉTIQUE (Peak à z=0.63)
# ====================================================================
def create_axion_w(A, B):
    def w_func(z):
        # Paramètres ajustés : Maxi à z=0.63
        phantom_dip = A * np.exp(- (z / 0.5)**2)
        quintessence_bump = B * np.exp(- ((z - 0.63) / 0.3)**2)
        return -1.0 + phantom_dip + quintessence_bump
    return w_func

def objective_function(params):
    w_test = create_axion_w(params[0], params[1])
    age = compute_cosmic_age(w_test)
    dm = compute_comoving_distance(w_test, z_bao_target)
    
    # On force l'âge à 13.5, on minimise le BAO
    age_penalty = ((age - TARGET_AGE) ** 2) * 1000.0
    bao_penalty = (((dm - dm_lcdm) / dm_lcdm) * 100) ** 2
    return age_penalty + bao_penalty 

print("="*65)
print("RUNNING GLOBAL OPTIMIZATION (Peak z=0.63)...")
print("Searching for the most efficient chiral transition configuration.")

bounds = [(-4.0, 0.0), (0.0, 4.0)]
result = differential_evolution(objective_function, bounds, strategy='best1bin', popsize=5, maxiter=150, tol=1e-2, seed=42)

best_A, best_B = result.x
best_w_func = create_axion_w(best_A, best_B)

age_ecks = compute_cosmic_age(best_w_func)
dm_ecks = compute_comoving_distance(best_w_func, z_bao_target)
delta_dm_ecks = ((dm_ecks - dm_lcdm) / dm_lcdm) * 100

# ====================================================================
# 4. RÉSULTATS ET GRAPHIQUE
# ====================================================================
print("="*65)
print(f"RESULTS FOR PEAK AT z=0.63")
print(f"Phantom Amplitude (A) : {best_A:.3f}")
print(f"Quintessence Amplitude (B) : {best_B:.3f}")
print(f"Final Age : {age_ecks:.3f} Gyr")
print(f"Minimal BAO Drift : {delta_dm_ecks:+.3f}%")
print("="*65)

plt.rcParams.update({'font.size': 11, 'font.family': 'serif', 'mathtext.fontset': 'stix'})
z_array = np.linspace(0, 3.0, 500)
fig, ax = plt.subplots(figsize=(8, 5.5))

ax.plot(z_array, [w_lcdm(z) for z in z_array], 'k--', lw=1.5, label=r'$\Lambda$CDM')
ax.plot(z_array, [best_w_func(z) for z in z_array], 'firebrick', lw=2.5, label='Optimized Axion (z_max=0.63)')

ax.axvline(x=0.63, color='gray', linestyle=':', lw=1.2)
ax.text(0.65, -2.5, r"Peak Transition $z=0.63$", color='dimgray', fontsize=9)

ax.axvspan(0, 0.63, color='indianred', alpha=0.1)
ax.axvspan(0.63, 3.0, color='seagreen', alpha=0.08)

ax.set_xlim(0, 2.5)
ax.set_ylim(-3.0, 0.5)
ax.set_xlabel(r'Redshift $z$')
ax.set_ylabel(r'Equation of State $w(z)$')
ax.set_title(f'Trilemma Resolution (Drift: {delta_dm_ecks:+.2f}%)')
ax.legend(loc='lower right', frameon=True, edgecolor='black')
ax.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.show()
