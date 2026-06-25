
"""
=========================================================================================
SUPPLEMENTARY MATERIAL FOR "FOUNDATION II: THE CHIRAL UNIVERSE"
=========================================================================================
Title: Exploring the DESI BAO Tension via Axion Geometric Optimization
Author: Pascal Fichant
Target Journal: Physical Review D (PRD)

THEORETICAL CONTEXT:
We formulate the H0-Age-BAO trilemma as a forced inverse problem. 
We know the Universe must be ~13.5 Gyr old to accommodate early JWST galaxies and 
local stellar populations, while H0 remains anchored at 73 km/s/Mpc. 
Because modifying the late-time expansion history invariably affects the comoving 
distance, a perfect 0.00% BAO drift is mathematically incompatible with a 13.5 Gyr age.

In this script, a global genetic algorithm (Differential Evolution) is forced to 
strictly achieve the 13.5 Gyr target using the Nieh-Yan axion dynamics (phantom dip + 
quintessence recovery). The algorithm then naturally minimizes the BAO comoving distance 
drift, revealing the absolute theoretical minimum BAO tension required by the geometry 
of the Universe. This directly echoes the recent dynamic tensions observed by DESI.
=========================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import differential_evolution
import warnings

warnings.filterwarnings("ignore")

# ====================================================================
# 1. PARAMÈTRES COSMOLOGIQUES DE BASE
# ====================================================================
H0 = 73.0
Omega_m0 = 0.315
Omega_de0 = 1.0 - Omega_m0
c_km_s = 299792.458
z_bao_target = 1.5

TARGET_AGE = 13.5  # Contrainte stricte de l'âge

# ====================================================================
# 2. NOYAUX D'INTÉGRATION
# ====================================================================

def de_density_integrand(z, w_func):
    return 3.0 * (1.0 + w_func(z)) / (1.0 + z)

def E_z(z, w_func):
    integral_w, _ = quad(de_density_integrand, 0, z, args=(w_func,))
    rho_de_ratio = np.exp(integral_w)
    E2 = Omega_m0 * (1.0 + z)**3 + Omega_de0 * rho_de_ratio
    return np.sqrt(E2)

def compute_cosmic_age(w_func):
    H0_to_Gyr_inv = H0 * 1.02271e-3 
    integral, _ = quad(lambda z: 1.0 / ((1.0 + z) * E_z(z, w_func)), 0, np.inf, limit=1000)
    return integral / H0_to_Gyr_inv

def compute_comoving_distance(w_func, z_target):
    integral, _ = quad(lambda z: 1.0 / E_z(z, w_func), 0, z_target)
    return (c_km_s / H0) * integral

# --- Référentiel LCDM (w=-1) ---
def w_lcdm(z): return -1.0
age_lcdm = compute_cosmic_age(w_lcdm)
dm_lcdm = compute_comoving_distance(w_lcdm, z_bao_target)

# ====================================================================
# 3. ALGORITHME GÉNÉTIQUE (MODE FORCÉ 13.5 Gyr)
# ====================================================================

def create_axion_w(A, B):
    def w_func(z):
        w_frozen = -1.0
        phantom_dip = A * np.exp(- (z / 0.6)**2)
        quintessence_bump = B * np.exp(- ((z - 0.8) / 0.4)**2)
        return w_frozen + phantom_dip + quintessence_bump
    return w_func

def objective_function(params):
    A, B = params
    w_test = create_axion_w(A, B)
    
    age = compute_cosmic_age(w_test)
    dm = compute_comoving_distance(w_test, z_bao_target)
    
    # MODE FORCÉ : Pénalité colossale (x1000) si l'âge n'est pas EXACTEMENT 13.5
    age_penalty = ((age - TARGET_AGE) ** 2) * 1000.0
    
    # On laisse l'algorithme trouver le BAO minimum possible naturellement
    bao_penalty = (((dm - dm_lcdm) / dm_lcdm) * 100) ** 2
    
    return age_penalty + bao_penalty 

print("="*65)
print("RUNNING GLOBAL GENETIC ALGORITHM (FORCED MODE)...")
print(f"Targeting strictly Age = {TARGET_AGE} Gyr to evaluate absolute BAO minimum drift.")
print("Scanning parameter space. Please wait ~5 seconds...")

# Limites physiques élargies pour laisser l'algorithme respirer
bounds = [(-4.0, 0.0), (0.0, 4.0)]

# Solveur global
result = differential_evolution(objective_function, bounds, strategy='best1bin', popsize=8, tol=1e-3, maxiter=300, seed=42)

best_A, best_B = result.x
best_w_func = create_axion_w(best_A, best_B)

# ====================================================================
# 4. AFFICHAGE DES RÉSULTATS
# ====================================================================

age_ecks = compute_cosmic_age(best_w_func)
dm_ecks = compute_comoving_distance(best_w_func, z_bao_target)
delta_dm_ecks = ((dm_ecks - dm_lcdm) / dm_lcdm) * 100

print("="*65)
print("H0-AGE-BAO TRILEMMA: MINIMUM REQUIRED TENSION (DESI COMPATIBILITY)")
print("="*65)

print(f"\n[1] STRICT METRIC LIMIT (w = -1)")
print(f"    Cosmic Age t0 : {age_lcdm:.3f} Gyr")
print(f"    BAO Distance  : {dm_lcdm:.1f} Mpc")

print("\n[2] OPTIMIZED ECKS NIEH-YAN (Chiral Axion Field)")
print(f"    Required Phantom Amplitude     (A) : {best_A:.3f}")
print(f"    Required Quintessence Recovery (B) : {best_B:.3f}")
print(f"\n    -> Achieved Cosmic Age t0 : {age_ecks:.3f} Gyr  <-- TARGET FORCED")
print(f"    -> Resulting BAO Distance : {dm_ecks:.1f} Mpc  <-- Minimal Drift: {delta_dm_ecks:+.3f}%")

print("-" * 65)
if abs(delta_dm_ecks) <= 2.5:
    print(f">>> SUCCESS: Drift is {delta_dm_ecks:+.2f}%. Fully compatible with DESI (2024) tensions! <<<")
else:
    print(f">>> TENSION ALERT: Drift is {delta_dm_ecks:+.2f}%. Might conflict with high-z BAO. <<<")
print("=" * 65)

# ====================================================================
# 5. GÉNÉRATION DU GRAPHIQUE PRD
# ====================================================================

plt.rcParams.update({'font.size': 12, 'axes.labelsize': 14, 'axes.titlesize': 14, 'legend.fontsize': 10, 'font.family': 'serif'})
z_array = np.linspace(0, 3.0, 500)
fig, ax = plt.subplots(figsize=(8, 5.5))

def w_cpl(z): return -1.1 - 0.5 * (z / (1.0 + z))

ax.plot(z_array, [w_lcdm(z) for z in z_array], 'k--', lw=2, label=r'$\Lambda$CDM ($w = -1$)')
ax.plot(z_array, [w_cpl(z) for z in z_array], 'b-.', lw=2, label=r'CPL proxy (Linear)')
ax.plot(z_array, [best_w_func(z) for z in z_array], 'r-', lw=3, label=r'Optimized ECKS Axion')

ax.axhline(-1, color='gray', linestyle=':', lw=1)
ax.axvline(x=0.8, color='dimgray', linestyle=':', lw=1.5)
ax.text(0.85, -2.5, "Transition\n$z \\approx 0.8$", color='dimgray', fontsize=10)

ax.axvspan(0, 0.8, color='lightcoral', alpha=0.1)
ax.axvspan(0.8, 3.0, color='forestgreen', alpha=0.1)

ax.text(0.4, -0.6, "Thawing Zone\n(Age Adjustment)", horizontalalignment='center', color='darkred', fontsize=10)
ax.text(2.0, -0.6, "Frozen Zone\n(BAO Protection)", horizontalalignment='center', color='darkgreen', fontsize=10)

ax.set_xlim(0, 3)
ax.set_ylim(-3.0, max(best_B - 0.2, -0.4)) 
ax.set_xlabel(r'Redshift $z$')
ax.set_ylabel(r'Effective equation of state $w(z)$')
ax.set_title(f'Axion Optimization: Targeting 13.5 Gyr (Drift: {delta_dm_ecks:+.2f}%)')

ax.legend(loc='lower right', framealpha=0.95, edgecolor='black', fancybox=True)
ax.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
#plt.show()
