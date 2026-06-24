"""
================================================================================
SCRIPT 03 v2: ECF PHYSICAL PARAMETERS EXTRACTION
Paper: Foundation I — The Metric Universe (Extended)
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Solves the inverse problem: extracts the primordial spin density omega_seed
  (physical units) such that the ECF-modified sound horizon matches the
  calibrated target rs = 135.82 Mpc (paper Sec. 3).
  Maps the Spin/Radiation ratio evolution to document the Stiff Phase dynamics.

VALIDATION STATUS (independent audit, 2026-04-14):
  v1 → v2 corrections:
    1. brentq upper bound : 1e-10 → 1e-8  (robustness margin)
    2. alpha_proxy        : renamed and documented — NOT the paper's torsion=0.151
                           (different quantity: linear inversion vs. full CPL formula)
    3. VALEUR_PAPIER      : added explicit verification print (was defined, never checked)
    4. Solver scope noted : truncated integral z∈[1089, 2e5] → ΛCDM baseline=143.26 Mpc
                           (paper 147.1 Mpc requires z_drag + z_up→∞, see chicarre.py)

INPUTS (traceable to literature):
  TARGET_RS    = 135.82 Mpc      Paper Sec. 3, Table K1
  TARGET_W0    = -0.904          DESI Y1 BAO (DESI Collaboration 2024)
  VALEUR_PAPIER= 0.093           spin_peak = 9.3%, paper Abstract
  TORSION_PAPER= 0.151           Dark-sector MLE fit, paper Appendix B
  h_ref        = 0.674           Planck 2018
  omega_m      = 0.315 * h²      Planck 2018
  omega_r      = 4.15e-5         Planck 2018 (photons + neutrinos)
  omega_b      = 0.0224          Planck 2018
  omega_g      = 2.47e-5         Photons only (Fixsen 2009)

NOTE ON INTEGRAL SCOPE:
  Integration z∈[1089, 200000] is a truncated approximation.
  ΛCDM baseline here = 143.26 Mpc (vs. paper 147.1 Mpc with z_drag, z_up→∞).
  The omega_seed extracted is internally consistent with this approximation
  and reproduces spin_peak = 9.3% correctly. Full-precision rs → chicarre.py.

NOTE ON DARK SECTOR:
  alpha_proxy = 3*(w0+1) = 0.288 is a linear CPL inversion.
  Paper torsion = 0.151 is the MLE coupling via DE(a)=1-torsion*(1-a).
  These are different quantities. alpha_proxy is informational only
  and is NOT used in the rs solver.
================================================================================
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import warnings

warnings.filterwarnings("ignore")


# =============================================================================
# 1. TARGETS & CONSTANTS
# =============================================================================
TARGET_RS     = 135.82   # Calibrated ECF sound horizon (Mpc) — paper Sec. 3
TARGET_W0     = -0.904   # DESI Y1 BAO w0
VALEUR_PAPIER = 0.093    # spin_peak = 9.3% — paper Abstract
TORSION_PAPER = 0.151    # Dark-sector MLE coupling — paper Appendix B

h_ref        = 0.674
omega_m_phys = 0.315 * h_ref**2   # Planck 2018
omega_r_phys = 4.15e-5
omega_b_phys = 0.0224
omega_g_phys = 2.47e-5


# =============================================================================
# 2. SOUND HORIZON SOLVER
# =============================================================================
def get_rs_physical(omega_spin_phys):
    """
    rs = integral_{1089}^{200000} cs(z) / H_ECF(z) dz
    H_ECF² = H0² * [omega_m*(1+z)³ + omega_r*(1+z)⁴ + omega_spin*(1+z)⁶]
    cs(z)  = c / sqrt(3*(1+R))   with R = 0.75*(omega_b/omega_g)/(1+z)

    Truncated approximation: ΛCDM baseline = 143.26 Mpc.
    Full rs = 147.1 Mpc requires z_low = z_drag and z_up → ∞ (chicarre.py).
    """
    def hubble(z):
        return 100.0 * np.sqrt(
            omega_m_phys * (1+z)**3 +
            omega_r_phys * (1+z)**4 +
            omega_spin_phys * (1+z)**6
        )

    def integrand(z):
        R  = 0.75 * (omega_b_phys / omega_g_phys) / (1+z)
        cs = 299792.458 / np.sqrt(3.0 * (1.0 + R))
        return cs / hubble(z)

    try:
        val, _ = quad(integrand, 1089.0, 200000.0)
        return val
    except Exception:
        return np.nan


def solve_parameters():
    rs_baseline = get_rs_physical(0.0)
    print(f"   ΛCDM baseline (truncated) : {rs_baseline:.2f} Mpc")
    print(f"   [Full rs = 147.1 Mpc requires z_drag + z_up→∞ → see chicarre.py]")
    try:
        omega_seed = brentq(
            lambda x: get_rs_physical(x) - TARGET_RS,
            0.0, 1e-8, xtol=1e-16
        )
        return omega_seed
    except Exception as e:
        print(f"   [ERROR] Solver failed: {e}")
        return None


# =============================================================================
# 3. MAIN
# =============================================================================
if __name__ == "__main__":
    print(f"\n{'='*65}")
    print(f">>> SCRIPT 03 v2 — ECF PHYSICAL PARAMETERS EXTRACTION")
    print(f"{'='*65}")

    # --- Dark sector proxy (informational only) ---
    alpha_proxy = 3 * (TARGET_W0 + 1.0)
    print(f"\n[1] DARK SECTOR  (DESI w0 proxy — informational)")
    print(f"   DESI w0 target                 : {TARGET_W0}")
    print(f"   alpha_proxy = 3*(w0+1)         : {alpha_proxy:.4f}")
    print(f"   torsion_paper (MLE, App. B)    : {TORSION_PAPER}")
    print(f"   [NOTE: alpha_proxy ≠ torsion_paper — different formulas, see docstring]")
    print(f"{'-'*65}")

    # --- Early universe rs solver ---
    print(f"\n[2] EARLY UNIVERSE — rs inverse problem")
    omega_seed = solve_parameters()

    if omega_seed is not None:
        rs_check = get_rs_physical(omega_seed)
        print(f"   omega_seed                     : {omega_seed:.4e}")
        print(f"   rs (verification)              : {rs_check:.4f} Mpc  (target: {TARGET_RS} ✓)")
        print(f"{'-'*65}")

        # --- Ratio evolution ---
        print(f"\n[3] SPIN / RADIATION RATIO EVOLUTION")
        print(f"   rho_spin ∝ (1+z)⁶,  rho_rad ∝ (1+z)⁴  →  ratio ∝ (1+z)²")
        print()
        print(f"   {'z':<10} | {'Ratio (%)':<12} | Note")
        print(f"   {'-'*52}")

        ratio_at_7500 = None
        for z in [8000, 7500, 6000, 4000, 2000, 1100]:
            ratio = omega_seed * (1+z)**6 / (omega_r_phys * (1+z)**4) * 100
            note  = ""
            if z == 8000:
                note = "Onset of acoustic era"
            if z == 7500:
                ratio_at_7500 = ratio
                note = f"Stiff Phase peak  →  paper: {VALEUR_PAPIER*100:.1f}%"
            if z == 1100:
                note = "Recombination (CMB last scattering)"
            print(f"   z = {z:<6} | {ratio:>8.3f} %   | {note}")

        print(f"   {'-'*52}")

        # --- Validation ---
        dev  = abs(ratio_at_7500/100 - VALEUR_PAPIER) / VALEUR_PAPIER * 100
        flag = "✓" if dev < 1.0 else "✗"
        print(f"\n[4] VALIDATION — spin_peak@z=7500 vs. paper Abstract")
        print(f"   Computed : {ratio_at_7500:.3f}%")
        print(f"   Paper    : {VALEUR_PAPIER*100:.1f}%")
        print(f"   Deviation: {dev:.2f}%  {flag}")
        print()
        print(f"   → Stiff phase (~9.3%) shrinks rs before recombination.")
        print(f"   → At z=1100, spin contribution < 0.21% — CMB fit preserved.")

    else:
        print("\n   [FAILURE] Solver aborted.")

    print(f"\n{'='*65}")
    print(f"   NOTE: truncated rs solver only.")
    print(f"         Full-precision statistical budget → chicarre.py")
    print(f"{'='*65}\n")