#check_stats.py
import pandas as pd

# Charger les résultats que vous venez de générer
df = pd.read_csv("output/sparc175_fit_results.csv").dropna()

# Calcul du vrai chi2 global pondéré par les degrés de liberté
chi2_global = (df["chi2_ecf"] * (df["n_points"] - 2)).sum() / (df["n_points"] - 2).sum()

print("\n=== DIAGNOSTIC STATISTIQUE SPARC ===")
print(f"chi2_global pondéré : {chi2_global:.3f}")
print(f"chi2 médian         : {df['chi2_ecf'].median():.3f}")
print(f"chi2 moyen (simple) : {df['chi2_ecf'].mean():.3f}")
print(f"Galaxies excellentes (chi2 < 2) : {(df['chi2_ecf'] < 2).sum()} / 175")
print(f"Galaxies problématiques (chi2 > 5): {(df['chi2_ecf'] > 5).sum()} / 175")
print("====================================\n")