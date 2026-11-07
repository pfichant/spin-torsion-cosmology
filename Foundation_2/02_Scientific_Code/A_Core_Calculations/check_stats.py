# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import sys
#check_stats.py
import pandas as pd

# Load the results just generated
# ⚠️ CHAIN POSITION (documented 23/08/2026). This script READS the reference
# fit; it does not produce it. Without the CSV it used to die on a raw
# FileNotFoundError, which reads like a broken repository -- it is not: the
# file is written by fit_sparc175.py, which must run first.
CSV = "output/sparc175_fit_results.csv"
if not os.path.exists(CSV):
    sys.exit(f"[STOP] {CSV} not found.\n"
             "       Run fit_sparc175.py first -- it produces the reference fit\n"
             "       (171 galaxies after the nu >= 3 cut, median chi2_red 0.802).\n"
             "       The whole pipeline in the right order: "
             "python3 run_all_simulations_F2.py")

df = pd.read_csv(CSV).dropna()

# ⚠️ CORRECTED 23/08/2026: the denominators below were HARD-CODED to 175.
# Since the nu >= 3 cut (minimum 5 points per rotation curve) the reference
# fit contains 171 galaxies, so the script was printing "x / 175" over a
# 171-row table. Now taken from len(df), which follows the CSV.

# Global chi2, weighted by the degrees of freedom
chi2_global = (df["chi2_ecf"] * (df["n_points"] - 2)).sum() / (df["n_points"] - 2).sum()

print("\n=== DIAGNOSTIC STATISTIQUE SPARC ===")
print(f"chi2_global pondéré : {chi2_global:.3f}")
print(f"chi2 médian         : {df['chi2_ecf'].median():.3f}")
print(f"chi2 moyen (simple) : {df['chi2_ecf'].mean():.3f}")
print(f"Galaxies excellentes (chi2 < 2) : {(df['chi2_ecf'] < 2).sum()} / {len(df)}")
print(f"Galaxies problématiques (chi2 > 5): {(df['chi2_ecf'] > 5).sum()} / {len(df)}")
print("====================================\n")