S8_LCDM = 0.832     # Planck
F_ION = 1.2765
gamma_spin = 0.31

if __name__ == "__main__":
    denom = 1 + (F_ION - 1)*gamma_spin
    S8_ECF = S8_LCDM / denom
    print(f"S8_LCDM = {S8_LCDM:.3f}")
    print(f"F_ION   = {F_ION:.4f}, gamma_spin = {gamma_spin:.3f}")
    print(f"S8_ECF  = {S8_ECF:.3f}")
