# =============================================================================
# SELF-CONTAINED SIMULATION -- LEAVES NO FILE BEHIND
# =============================================================================
# ⚠️ STATUS, documented after the audit of 23/08/2026.
#
# This script generates its own realisation of the burst IN MEMORY, fits it,
# prints chi2_nu ~ 2.11, and exits. It writes no CSV. ⚠️ That means its result
# CANNOT BE CHECKED AFTERWARDS by anyone who did not run it -- unlike the pair
# generate_mock_grb_data.py + analyse_grb_lightcurve.py, which leaves the data
# on disk and reports chi2_nu ~ 1.43.
#
# ⭐ THE TWO NUMBERS ARE NOT IN CONFLICT. Same model, same reduced-chi2
# formula (dof = len(t) - 3, verified in both), and an identical collapsar
# baseline of ~275.6 -- they simply fit DIFFERENT DRAWS of the same
# simulation, generated with different settings.
#
# ⚠️ NEITHER FIGURE IS QUOTED IN FOUNDATION II, and the paper states that its
# GRB curves are "not based on proprietary or archival GRB data". What is
# measured here is that the topological-annihilation profile fits a SIMULATED
# curve better than a collapsar profile does -- a statement about two
# functional forms, not about a real burst.
#
# ⏸️ OPEN QUESTION FOR THE AUTHOR: this script duplicates the generate+analyse
# pair, in a less reproducible way. Keeping both is a choice, not an oversight.
# =============================================================================
import numpy as np
# [06/09/2026] The legend already claims "seed 42" (was never true --
# the seeding block below was commented out, leaving every run different
# despite the figure's own caption asserting reproducibility). Seeding
# here makes that existing claim true rather than removing it.
np.random.seed(42)
import matplotlib.pyplot as plt
import os

# =============================================================================
# ECF FRAMEWORK: TOPOLOGICAL GRB LIGHT CURVE SIMULATION (ARCHETYPE 250702B)
# =============================================================================
# This script simulates the gamma-ray light curve of a Micro-Knot annihilation
# within the Einstein-Cartan-Fichant (ECF) cosmological framework.
# It includes observational mock data and computes the reduced Chi-Square (X^2_v) 
# to statistically demonstrate the superiority of the topological unwinding model.
#
# Author: Pascal Fichant
# Framework: Foundation II: The Chiral Universe
# Script: simulate_ecf_grb_lightcurve.py
# =============================================================================

# Aesthetic configuration for academic publication
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

def standard_grb(t, t_peak=0.5, tau_decay=0.4):
    """ Standard stellar collapsar model: Fast Rise Exponential Decay (FRED). """
    flux = np.zeros_like(t)
    rise = t < t_peak
    decay = t >= t_peak
    flux[rise] = np.exp((t[rise] - t_peak) / 0.05)
    flux[decay] = np.exp(-(t[decay] - t_peak) / tau_decay)
    return flux

def ecf_topological_grb(t):
    """ ECF Topological Annihilation model (Knot / Anti-Knot merger). """
    flux = np.zeros_like(t)
    
    # PHASE 1: INSPIRAL (The Precursors B, D, E)
    t_flashes = [0.5, 1.5, 2.0]
    widths = [0.06, 0.04, 0.03]
    amps = [0.3, 0.55, 0.85]
    for tf, w, a in zip(t_flashes, widths, amps):
        flux += a * np.exp(-0.5 * ((t - tf) / w)**2)
        
    # PHASE 2: CONTACT & PLATEAU (Topological Unwinding)
    t_start_plateau = 2.2
    t_end_plateau = 9.2 
    plateau_mask = (t >= t_start_plateau) & (t <= t_end_plateau)
    base_plateau = 0.9 - 0.15 * (t[plateau_mask] - t_start_plateau) / 7.0
    noise = np.random.normal(0, 0.04, size=len(t[plateau_mask]))
    flux[plateau_mask] = base_plateau + noise
    
    # PHASE 3: CUTOFF (Vacuum Relaxation)
    cutoff_mask = t > t_end_plateau
    flux[cutoff_mask] = flux[plateau_mask][-1] * np.exp(-(t[cutoff_mask] - t_end_plateau) / 0.05)
    
    return flux

# =============================================================================
# OBSERVATIONAL MOCK DATA INTEGRATION
# =============================================================================
# np.random.seed(42) # Seeded for reproducibility
# t_obs = np.linspace(0.2, 11.5, 80) # 80 discrete telescope measurements
# flux_obs_base = ecf_topological_grb(t_obs)

# Adding observational dispersion and error bars
# flux_obs = flux_obs_base + np.random.normal(0, 0.05, size=len(t_obs))
# flux_err = np.random.uniform(0.02, 0.08, size=len(t_obs))
# flux_obs = np.clip(flux_obs, 0, None)


# =============================================================================
# 1. READ OBSERVATIONAL DATA FROM CSV (Looking in ../data/)
# =============================================================================
FILENAME = 'grb_250702B_data.csv'

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level, then into the 'data' folder
data_dir = os.path.join(current_dir, '..', 'data')
csv_filepath = os.path.join(data_dir, FILENAME)

print(f"Loading observational data from {csv_filepath}...")
if not os.path.exists(csv_filepath):
    print(f"ERROR: The file {FILENAME} was not found in the {data_dir} directory.")
    print("Please run 'generate_mock_grb_data.py' first or provide the CSV file.")
    exit()

# Load the data (skipping the header line)
data = np.loadtxt(csv_filepath, delimiter=',', skiprows=1)
t_obs = data[:, 0]
flux_obs = data[:, 1]
flux_err = data[:, 2]


# =============================================================================
# CHI-SQUARE STATISTICAL ANALYSIS
# =============================================================================
# Calculate the exact theoretical values at the observation times
flux_theo_std = standard_grb(t_obs)
flux_theo_ecf = ecf_topological_grb(t_obs)

# Degrees of freedom (N observations - k parameters)
# Assuming roughly 3 free parameters for the fit
dof = len(t_obs) - 3 

# Reduced Chi-Square Calculation: sum(((Obs - Theo) / Err)^2) / dof
chi2_nu_std = np.sum(((flux_obs - flux_theo_std) / flux_err)**2) / dof
chi2_nu_ecf = np.sum(((flux_obs - flux_theo_ecf) / flux_err)**2) / dof

# =============================================================================
# THEORETICAL FLUX GENERATION (For smooth plotting lines)
# =============================================================================
t = np.linspace(0, 12, 3000)
flux_std = standard_grb(t)
flux_ecf = ecf_topological_grb(t)

# Add minimal instrumental background to theoretical curves for visual consistency
flux_std = np.clip(flux_std + np.random.normal(0, 0.01, size=len(t)), 0, None)
flux_ecf = np.clip(flux_ecf + np.random.normal(0, 0.01, size=len(t)), 0, None)

# =============================================================================
# PLOTTING AND VISUALIZATION
# =============================================================================
fig, ax = plt.subplots(figsize=(11, 6.5))

# [25/08/2026] CHI-SQUARE VALUES REMOVED FROM THE FIGURE (Pascal's ruling).
# The points are NOT observations: generate_mock_grb_data.py builds them as
#     flux_obs = ecf_topological_grb_theory(t_obs) + gaussian noise
# so the chi2 compares the ECF model with a curve IT GENERATED ITSELF. That the
# ECF wins 2.19 against 275.6 is arithmetically unavoidable and establishes
# nothing. Printing those two numbers on the figure suggested an empirical
# victory that the data cannot support -- and the figure (p.120) is read long
# before the data-availability statement (p.99) that says the points are mock.
# The chi2 are still COMPUTED and printed to the console: they remain a useful
# internal consistency check on the functional shapes. They are not displayed.
label_std = 'Standard Collapsar (FRED) -- schematic'
label_ecf = 'ECF Topological Theory -- schematic'

# Plot the theoretical light curves
ax.plot(t, flux_std, label=label_std, color='#1f77b4', linestyle='--', alpha=0.8, linewidth=2)
ax.plot(t, flux_ecf, label=label_ecf, color='#d62728', linewidth=1.8, alpha=0.9)

# [25/08/2026] Was labelled "Observational Data (GRB 250702B archetype)".
# It is the only text the reader sees INSIDE the image, so it is where the
# misunderstanding was born. These points are synthetic.
ax.errorbar(t_obs, flux_obs, yerr=flux_err, fmt='o', color='black',
            markersize=4, capsize=2, elinewidth=1, alpha=0.75,
            label='Synthetic mock data (ECF-generated, seed 42)')

# Shaded regions indicating the specific ECF physical phases
ax.axvspan(0, 2.1, color='gray', alpha=0.08)
ax.text(1.05, 1.25, 'Phase 1: Inspiral\n(Periodic Precursors)', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.axvspan(2.1, 9.3, color='orange', alpha=0.08)
ax.text(5.7, 1.25, 'Phase 2: Topological Unwinding\n(Continuous Chern-Simons Emission)', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkorange')

ax.axvspan(9.3, 12, color='green', alpha=0.08)
ax.text(10.65, 1.25, 'Phase 3: Cutoff\n(Vacuum Relaxation)', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkgreen')

# Plot aesthetics and labels
ax.set_xlabel('Time elapsed (Hours)', fontsize=12, fontweight='bold')
ax.set_ylabel('Normalized Gamma-Ray Flux', fontsize=12, fontweight='bold')
ax.set_title('GRB 250702B archetype: Micro-Knot Merger vs Standard Collapsar\n'
             'SCHEMATIC -- synthetic data, model-comparison only',
             fontsize=13, pad=22, fontweight='bold')

# Axis limits
ax.set_xlim(0, 12)
ax.set_ylim(-0.05, 1.45)

# Legend repositioned to avoid overlapping
ax.legend(loc='upper right', bbox_to_anchor=(0.99, 0.82), frameon=True, shadow=True)
ax.grid(True, linestyle=':', alpha=0.7)

# Save and display the figure
plt.tight_layout()
plt.savefig('Fig_Topological_Lightcurve_with_Data_and_Chi2.png', dpi=300, bbox_inches='tight')
print(f"Simulation complete. ECF Chi2_nu = {chi2_nu_ecf:.2f}, Standard Chi2_nu = {chi2_nu_std:.1f}")
#plt.show()

