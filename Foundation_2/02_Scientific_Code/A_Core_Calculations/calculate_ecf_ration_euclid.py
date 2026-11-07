import numpy as np
# =============================================================================
# EXPLORATORY -- NOT A RESULT OF FOUNDATION II
# =============================================================================
# ⚠️ STATUS, set after the audit of 22/08/2026. This script is kept in the
# repository for transparency, but its output is NOT quoted in any paper and
# MUST NOT be read as an ECF prediction. Three reasons, in order of weight:
#
# (1) ⚠️ ITS STARTING POINT IS AN OBSERVATION, NOT THE THEORY.
#     R_cmb = 5.40 is essentially the Planck 2018 measurement
#     (omega_c/omega_b = 0.1200/0.02237 = 5.36, agreeing to 0.7%), NOT the
#     framework's 5:1 partition. So the script computes "given the measured
#     CMB ratio, what is it today?" -- an evolution calculation valid for ANY
#     model, not a test of Einstein-Cartan.
#
# (2) ⚠️⚠️ STARTING FROM THE THEORY INSTEAD GIVES A VALUE ALREADY EXCLUDED.
#     With R_cmb = 5.00 (the 5:1 partition), R_0 = 5.134 +/- 0.027, which sits
#     about 7% -- some 9 sigma -- below the Planck-derived 5.504 +/- 0.042.
#     ⭐ This is NOT a failure of the framework: Foundation II writes "~5:1"
#     with a tilde and states explicitly that it is "a consistency result
#     under the Weyssenhoff approximation, NOT a parameter-free
#     first-principles derivation". The ratio is an order of magnitude, not a
#     three-digit number -- so quoting a +/-0.027 prediction from it would be
#     FALSE PRECISION.
#
# (3) ⭐ AND THE EVOLUTION ITSELF IS TOO SMALL TO DISCRIMINATE.
#     The CMB-to-today correction is only +2.7%. Euclid measuring R_0 cannot
#     separate this framework from LCDM by this ratio: both predict the same
#     number to within the measurement error.
#
# ⭐ WHAT THE SCRIPT DOES WELL, and why it is worth keeping: it prints its
# value, its error bar AND its confidence interval (rule 1bis), and its
# calculation is fully transparent -- it was reproduced independently during
# the audit (5.5447 +/- 0.0329 against 5.545 +/- 0.033).
# The defect was never in the code; it was the absence of a declared status.
# =============================================================================
# Contemporary mass ratio at z=0 -- evolution of a measured CMB ratio
# =============================================================================

print("--- EXPLORATORY: evolution of the measured CMB ratio (NOT an ECF prediction) ---")

# 1. Initial Conditions (Planck 2018 CMB Data at z ~ 1100)
R_cmb = 5.40
err_R_cmb = 0.015 # Uncertainty from Planck data

# 2. ECF Secular Mass Loss Parameters (Integrated over 13.4 Gyr)
# [19/10/2026] 13.4 Gyr is a rounded cosmic time and is not used numerically; corpus value t0 = 13.33 Gyr (w=-1), 13.19 Gyr at the calibrated (w0, wa) point.
# Fractional baryonic mass loss (Stars + AGN)
eps_b = 0.030 
err_eps_b = 0.005 # 0.5% uncertainty on star formation history

# Fractional topological mass loss (GRB / Macro-Knot Annihilation)
eps_t = 0.004
err_eps_t = 0.001 # 0.1% uncertainty on cosmic merger rates

# 3. Calculation of Contemporary Ratio R_0
# R_0 = (M_DM_cmb * (1 - eps_t)) / (M_BM_cmb * (1 - eps_b))
R_0 = R_cmb * ((1.0 - eps_t) / (1.0 - eps_b))

# 4. Standard Error Propagation (Partial Derivatives Method)
# Using the formula: (dR/R)^2 = (dR_cmb/R_cmb)^2 + (deps_t/(1-eps_t))^2 + (deps_b/(1-eps_b))^2
term1 = (err_R_cmb / R_cmb)**2
term2 = (err_eps_t / (1.0 - eps_t))**2
term3 = (err_eps_b / (1.0 - eps_b))**2

relative_error = np.sqrt(term1 + term2 + term3)
absolute_error = R_0 * relative_error

# 5. Output the Scientific Prediction
print(f"Primordial Ratio (CMB) : {R_cmb:.3f} +/- {err_R_cmb:.3f}")
print(f"Baryonic Mass Loss     : {eps_b*100:.1f}% +/- {err_eps_b*100:.1f}%")
print(f"Topological Mass Loss  : {eps_t*100:.2f}% +/- {err_eps_t*100:.2f}%")
print("-" * 40)
print(f"EVOLVED RATIO AT z=0 (exploratory)  : R_0 = {R_0:.3f} +/- {absolute_error:.3f}")
print("-" * 40)
print(f"Confidence Interval (1-sigma)  : [{R_0 - absolute_error:.3f} , {R_0 + absolute_error:.3f}]")
