# Last modified: 30/08/2026, 12:24 (Paris time)
import numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# GRB LIGHT CURVE ANALYZER -- RUNS ON MOCK DATA
# =============================================================================
# ⚠️ STATUS, set after the audit of 22/08/2026. The chi2 values this script
# prints (ECF ~1.4 against Standard ~276) are NOT quoted in Foundation II,
# and must not be read as an observational result. The reason is stated by
# the paper itself: its GRB curves are "not based on proprietary or archival
# GRB data" -- they are generated with a fixed seed.
#
# ⭐ The script agrees: when the CSV is missing it prints
# "Please run generate_mock_grb_data.py first" -- the word is MOCK.
#
# ⚠️ CHAIN POSITION (documented 23/08/2026). This script READS the CSV; it
# does not create it. The chain is:
#   generate_mock_grb_data.py  (seed 42, 80 points, noise 0.05)  -- WRITES
#   analyse_grb_lightcurve.py  (this file)                       -- READS
# ⭐ A third script, simulate_ecf_grb2025_lightcurve.py, does BOTH in memory
# with its own settings. UPDATE (30/08/2026): that script has no fixed seed
# and is NOT reproducible run-to-run -- five consecutive runs gave chi2_nu
# = 2.26, 1.57, 1.85, 2.15, 2.01. Read as "order 1-2", not a specific value;
# the ~1.43 here (fixed seed 42) IS reproducible.
# The two are NOT in conflict: same model, same formula (dof = len(t) - 3 in
# both, verified), but DIFFERENT DRAWS. The collapsar baseline chi2 ~ 275.6 is
# identical in both, which is what confirms the models agree.
#
# ⇒ What the ratio measures is that the topological-annihilation profile fits
#   the SIMULATED curve better than a collapsar profile does. That is a
#   statement about the two functional forms, not about a real burst. A real
#   test needs archival data, which this repository does not contain.
# =============================================================================
# Fits the ECF Topological Annihilation model against the Standard Collapsar
# model on the MOCK light curve supplied in data/ (not an observed burst).
# =============================================================================
# This script reads (MOCK, seed 42) data from a .csv file and fits it against 
# the ECF Topological Annihilation model and the Standard Collapsar Model.
# =============================================================================

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
    # PHASE 1: Inspiral (Flashes)
    for tf, w, a in zip([0.5, 1.5, 2.0], [0.06, 0.04, 0.03], [0.3, 0.55, 0.85]):
        flux += a * np.exp(-0.5 * ((t - tf) / w)**2)
    # PHASE 2: Plateau (Chern-Simons Unwinding)
    t_start_plateau, t_end_plateau = 2.2, 9.2 
    plateau_mask = (t >= t_start_plateau) & (t <= t_end_plateau)
    flux[plateau_mask] = 0.9 - 0.15 * (t[plateau_mask] - t_start_plateau) / 7.0
    # PHASE 3: Cutoff
    cutoff_mask = t > t_end_plateau
    if len(flux[plateau_mask]) > 0:
        flux[cutoff_mask] = flux[plateau_mask][-1] * np.exp(-(t[cutoff_mask] - t_end_plateau) / 0.05)
    return flux
    

# =============================================================================
# 1. READ OBSERVATIONAL DATA FROM CSV (Looking in ../data/)
# =============================================================================
FILENAME = 'grb_250702B_data.csv'

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level, then into the 'data' folder
data_dir = os.path.join(current_dir, '..', 'data')
csv_filepath = os.path.join(data_dir, FILENAME)

print(f"Loading MOCK data (generate_mock_grb_data.py, seed 42) from {csv_filepath}...")
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
# 2. CHI-SQUARE STATISTICAL ANALYSIS
# =============================================================================
flux_theo_std = standard_grb(t_obs)
flux_theo_ecf = ecf_topological_grb(t_obs)

dof = len(t_obs) - 3 
chi2_nu_std = np.sum(((flux_obs - flux_theo_std) / flux_err)**2) / dof
chi2_nu_ecf = np.sum(((flux_obs - flux_theo_ecf) / flux_err)**2) / dof

print(f"Analysis complete. ECF Chi2_nu = {chi2_nu_ecf:.2f}, Standard Chi2_nu = {chi2_nu_std:.1f}")

# =============================================================================
# 3. THEORETICAL FLUX GENERATION (For smooth plotting lines)
# =============================================================================
t = np.linspace(0, 12, 3000)
flux_std = standard_grb(t)
flux_ecf = ecf_topological_grb(t)

# =============================================================================
# 4. PLOTTING AND VISUALIZATION
# =============================================================================
fig, ax = plt.subplots(figsize=(11, 6.5))

label_std = f'Standard Collapsar (FRED) [$\\chi^2_\\nu = {chi2_nu_std:.1f}$]'
label_ecf = f'ECF Topological Theory [$\\chi^2_\\nu = {chi2_nu_ecf:.2f}$]'

ax.plot(t, flux_std, label=label_std, color='#1f77b4', linestyle='--', alpha=0.8, linewidth=2)
ax.plot(t, flux_ecf, label=label_ecf, color='#d62728', linewidth=1.8, alpha=0.9)

# Plot the data read from the CSV
ax.errorbar(t_obs, flux_obs, yerr=flux_err, fmt='o', color='black', 
            markersize=4, capsize=2, elinewidth=1, alpha=0.75, 
            label='Synthetic mock data (ECF-generated, seed 42)')   # [02/10/2026] was "Observational Data (<path>)": data are mock (see header) and the label leaked a local file path

# Styling (shaded regions and labels)
ax.axvspan(0, 2.1, color='gray', alpha=0.08)
ax.text(1.05, 1.25, 'Phase 1: Inspiral\n(Periodic Precursors)', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.axvspan(2.1, 9.3, color='orange', alpha=0.08)
ax.text(5.7, 1.25, 'Phase 2: Topological Unwinding\n(Continuous Chern-Simons Emission)', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkorange')
ax.axvspan(9.3, 12, color='green', alpha=0.08)
ax.text(10.65, 1.25, 'Phase 3: Cutoff\n(Vacuum Relaxation)', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkgreen')

ax.set_xlabel('Time elapsed (Hours)', fontsize=12, fontweight='bold')
ax.set_ylabel('Normalized Gamma-Ray Flux', fontsize=12, fontweight='bold')
ax.set_title(f'Data Fit Analysis: Standard Model vs ECF Theory', fontsize=14, pad=25, fontweight='bold')

ax.set_xlim(0, 12)
ax.set_ylim(-0.05, 1.45)
ax.legend(loc='upper right', bbox_to_anchor=(0.99, 0.82), frameon=True, shadow=True)
ax.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
output_fig = 'Fig_Data_Fit_Analysis.png'
plt.savefig(output_fig, dpi=300, bbox_inches='tight')
# plt.show()
