import numpy as np
import os

# =============================================================================
# ECF FRAMEWORK: MOCK OBSERVATIONAL DATA GENERATOR
# =============================================================================
# This script generates synthetic telescope data (Mock Data) mimicking the 
# topological annihilation of a Macro-Knot (e.g., the GRB 250702B archetype).
# It automatically saves the output CSV file into the '../data' directory.
# 
# OPEN SCIENCE & EDUCATION:
# This tool is provided for students and researchers to generate custom 
# observational datasets. By modifying the instrumental parameters below 
# (such as 'noise_level' or 'cadence'), users can test the robustness of the 
# ECF theoretical fit and observe how telescope precision impacts the final 
# reduced Chi-Square (X^2_v) statistics.
#
# Author: Pascal Fichant
# Framework: Foundation II: The Chiral Universe
# Script: generate_mock_grb_data.py
# =============================================================================

def ecf_topological_grb_theory(t):
    flux = np.zeros_like(t)
    # PHASE 1
    t_flashes, widths, amps = [0.5, 1.5, 2.0], [0.06, 0.04, 0.03], [0.3, 0.55, 0.85]
    for tf, w, a in zip(t_flashes, widths, amps):
        flux += a * np.exp(-0.5 * ((t - tf) / w)**2)
    # PHASE 2
    t_start_plateau, t_end_plateau = 2.2, 9.2 
    plateau_mask = (t >= t_start_plateau) & (t <= t_end_plateau)
    flux[plateau_mask] = 0.9 - 0.15 * (t[plateau_mask] - t_start_plateau) / 7.0
    # PHASE 3
    cutoff_mask = t > t_end_plateau
    if len(flux[plateau_mask]) > 0:
        flux[cutoff_mask] = flux[plateau_mask][-1] * np.exp(-(t[cutoff_mask] - t_end_plateau) / 0.05)
    return flux

# Parameters
RANDOM_SEED = 42 
T_START, T_END = 0.2, 11.5
NUM_OBSERVATIONS = 80 
NOISE_LEVEL = 0.05 
ERROR_MIN, ERROR_MAX = 0.02, 0.08
FILENAME = "grb_250702B_data.csv"

# =============================================================================
# PATH MANAGEMENT (Points to ../data/)
# =============================================================================
# Get the directory where this script is located (A_Core_Calculations)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level, then into the 'data' folder
data_dir = os.path.join(current_dir, '..', 'data')

# Create the 'data' folder if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Full path for the output file
output_filepath = os.path.join(data_dir, FILENAME)

# =============================================================================
# DATA GENERATION
# =============================================================================
print("Generating Mock Data...")
if RANDOM_SEED is not None: np.random.seed(RANDOM_SEED)

t_obs = np.linspace(T_START, T_END, NUM_OBSERVATIONS)
flux_obs = np.clip(ecf_topological_grb_theory(t_obs) + np.random.normal(0, NOISE_LEVEL, size=NUM_OBSERVATIONS), 0, None)
flux_err = np.random.uniform(ERROR_MIN, ERROR_MAX, size=NUM_OBSERVATIONS)

# Save to CSV in the data folder
data_matrix = np.column_stack((t_obs, flux_obs, flux_err))
csv_header = "Time_Hours,Flux_Normalized,Flux_Error"
np.savetxt(output_filepath, data_matrix, delimiter=",", header=csv_header, comments='', fmt='%.4f')

print(f"Success! Data saved to: {output_filepath}")