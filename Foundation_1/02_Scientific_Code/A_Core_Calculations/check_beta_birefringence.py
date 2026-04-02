import numpy as np

# Observations Minami & Komatsu
beta_obs = 0.35  # degrés
beta_obs_err = 0.14

F_ION = 1.2765   # ton facteur de raideur

if __name__ == "__main__":
    # Calibre k sur l'observation Planck
    k = beta_obs / F_ION      # degrés par unité F_ION
    beta_th = k * F_ION       # = beta_obs, mais maintenant tu peux varier F_ION

    print(f"F_ION      = {F_ION:.4f}")
    print(f"k          = {k:.3f} deg / F_ION")
    print(f"beta_th    = {beta_th:.3f} deg")
    print(f"Planck obs = {beta_obs:.3f} ± {beta_obs_err:.3f} deg")
    print("Interpretation : pour F_ION modifie, beta_th suit lineairement.")
