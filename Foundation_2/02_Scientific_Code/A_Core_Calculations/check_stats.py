
#!/usr/bin/env python3
"""
check_stats.py
ECF Foundation II — Pascal Fichant, May 2026

Purpose:
    Calculates the true global weighted reduced chi-squared for the ECF 
    torsion-halo fits over the 175 galaxies of the SPARC database.
    This script appropriately weights each galaxy by its degrees of freedom 
    (number of data points - 2 parameters) to prevent low-quality data 
    from skewing the unweighted mean.
"""

import pandas as pd

# Load the recently generated fit results
# Ensure this script is run from the same directory containing the 'output' folder
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
import os as _os2

def _find_found_dir(start):
    d = start
    for _ in range(5):
        if _os2.path.isdir(_os2.path.join(d, "data")) and _os2.path.isdir(_os2.path.join(d, "output")):
            return d
        parent = _os2.path.dirname(d)
        if parent == d: break
        d = parent
    return _os2.path.dirname(_os2.path.abspath(__file__))

_FOUNDATION2_DIR2 = _find_found_dir(_os2.path.dirname(_os2.path.abspath(__file__)))
_CSV = _os2.path.join(_FOUNDATION2_DIR2, "output", "sparc175_fit_results.csv")
df = pd.read_csv(_CSV).dropna()

# Calculate the true global chi-squared, weighted by degrees of freedom (N - 2)
degrees_of_freedom = df["n_points"] - 2
chi2_global = (df["chi2_ecf"] * degrees_of_freedom).sum() / degrees_of_freedom.sum()

print("\n=== SPARC STATISTICAL DIAGNOSTIC ===")
print(f"Global weighted chi2  : {chi2_global:.3f}")
print(f"Median chi2           : {df['chi2_ecf'].median():.3f}")
print(f"Mean chi2 (unweighted): {df['chi2_ecf'].mean():.3f}")
print("-" * 36)
print(f"Excellent fits (chi2 < 2) : {(df['chi2_ecf'] < 2).sum()} / 175")
print(f"Outliers / Poor fits (chi2 > 5) : {(df['chi2_ecf'] > 5).sum()} / 175")
print("====================================\n")
