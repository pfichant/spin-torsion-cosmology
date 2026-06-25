import numpy as np
# =============================================================================
# ECF FRAMEWORK: ANALYTICAL PREDICTION OF CONTEMPORARY MASS RATIO (z=0)
# =============================================================================

print("--- ECF Analytical Prediction Model ---")

# 1. Initial Conditions (Planck 2018 CMB Data at z ~ 1100)
R_cmb = 5.40
err_R_cmb = 0.015 # Uncertainty from Planck data

# 2. ECF Secular Mass Loss Parameters (Integrated over 13.4 Gyr)
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
print(f"ECF PREDICTION FOR EUCLID (z=0): R_0 = {R_0:.3f} +/- {absolute_error:.3f}")
print("-" * 40)
print(f"Confidence Interval (1-sigma)  : [{R_0 - absolute_error:.3f} , {R_0 + absolute_error:.3f}]")
