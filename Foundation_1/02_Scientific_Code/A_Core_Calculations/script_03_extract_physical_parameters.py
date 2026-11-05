"""
================================================================================
SCRIPT 03 v2: ECF PHYSICAL PARAMETERS EXTRACTION
Paper: Foundation I — The Metric Universe (Extended)
Author: Pascal Fichant (2026)
================================================================================
DESCRIPTION:
  Solves the inverse problem: extracts the primordial spin density omega_seed
  (physical units) such that the ECF-modified sound horizon matches the
  calibrated target rs = 135.65 Mpc (paper Sec. 3; A-6, was 135.80).
  Maps the Spin/Radiation ratio evolution to document the Stiff Phase dynamics.

VALIDATION STATUS (independent audit, 2026-04-14):
  v1 → v2 corrections:
    1. brentq upper bound : 1e-10 → 1e-8  (robustness margin)
    2. alpha_proxy        : renamed and documented — NOT the paper's torsion=0.151
                           (different quantity: linear inversion vs. full CPL formula)
    3. VALEUR_PAPIER      : added explicit verification print (was defined, never checked)
    4. Solver scope noted : truncated integral z∈[1089, 2e5] → ΛCDM baseline=143.26 Mpc
                           (paper 147.1 Mpc requires z_drag + z_up→∞, see chicarre.py)

  v2 → v3 (02/10/2026) — SOLVER ALIGNED ON script_01 (reference):
    5. The truncated integral is replaced by the script_01 integral
       (z_drag = 1059.94 to z = 1e7, Lambda term included, c_s scaled by
       TAU_TOR = 0.9975). Reason: the target TARGET_RS = 135.65 Mpc comes from the
       FULL integral (LCDM baseline 147.1 Mpc) but v2 imposed it on an integral
       whose LCDM baseline is 143.26 Mpc, so the inversion asked for 7.6 Mpc of
       reduction instead of 11.5 Mpc and returned 5.41 % instead of ~9.3 %.
    6. Inputs aligned on script_01 (Planck 2018: h = 0.6736, omega_b = 0.02237,
       omega_c = 0.1200, omega_g = 2.4728e-5, omega_nu from N_eff = 3.046
       [A-6]); omega_r = 4.1834e-5. v2 used h = 0.674, Omega_m = 0.315 h^2,
       omega_r = 4.15e-5.
    7. The module-level claim "reproduces spin_peak = 9.3 % correctly" is now true
       by construction check (section [4] prints the deviation).
    8. One equation, two unknowns: TAU_TOR is held at its calibrated value
       (0.9975). With TAU_TOR = 1 the same target needs ~10.1 %: the 9.3 % is
       conditional on TAU_TOR (F1 l.1782-1789 states the joint calibration).

INPUTS (traceable to literature):
  TARGET_RS    = 135.65 Mpc      Paper Sec. 3, Table K1 (A-6)
  TARGET_W0    = -0.904          ECF calibrated value (Foundation I, PO-F1-B); not a DESI measurement
  VALEUR_PAPIER= 0.093           spin_peak = 9.3%, paper Abstract
  TORSION_PAPER= 0.151           Dark-sector MLE fit, paper Appendix B
  h_ref        = 0.6736          Planck 2018 (as script_01)
  omega_b      = 0.02237         Planck 2018
  omega_c      = 0.1200          Planck 2018
  omega_g      = 2.4728e-5       Photons only (T_CMB = 2.7255 K)
  omega_nu     = 1.7106e-5       N_eff = 3.046 [A-6]  -> omega_r = 4.1834e-5
  TAU_TOR      = 0.9975          Calibrated (as script_01)

NOTE ON INTEGRAL SCOPE (v3):
  Same integral as script_01: z from z_drag = 1059.94 to 1e7, Lambda included.
  LCDM baseline here = 147.07 Mpc (script_01). The omega_seed extracted
  reproduces Omega_spin,0 of script_01 (2.73e-13 in the h_Planck convention)
  and spin_peak = 9.3 %. Statistical budget → chicarre.py.

NOTE ON DARK SECTOR:
  alpha_proxy = 3*(w0+1) = 0.288 is a linear CPL inversion.
  Paper torsion = 0.151 is the MLE coupling via DE(a)=1-torsion*(1-a).
  These are different quantities. alpha_proxy is informational only
  and is NOT used in the rs solver.
================================================================================
"""
# Last modified: 02/10/2026 (Paris time) — v3, promoted 07/10/2026
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import warnings

warnings.filterwarnings("ignore")


# =============================================================================
# 1. TARGETS & CONSTANTS
# =============================================================================
TARGET_RS     = 135.65   # [A-6 22/09/2026] was 135.80. ECF sound horizon (Mpc) as produced by script_01
TARGET_W0     = -0.904   # ECF calibrated w0 (Foundation I); not a DESI Y1 value (A-9)
VALEUR_PAPIER = 0.093    # spin_peak = 9.3% — paper Abstract
TORSION_PAPER = 0.151    # Dark-sector MLE coupling — paper Appendix B

# [v3, 02/10/2026] Inputs aligned on script_01_solve_sound_horizon.py (reference).
h_ref        = 0.6736
omega_b_phys = 0.02237
omega_c_phys = 0.1200
omega_g_phys = 2.4728e-5
omega_n_phys = (7.0/8.0)*(4.0/11.0)**(4.0/3.0)*3.046*omega_g_phys   # A-6 : 1.7106e-5
omega_r_phys = omega_g_phys + omega_n_phys                          # 4.1834e-5
omega_m_phys = omega_b_phys + omega_c_phys
omega_L_phys = h_ref**2 - omega_m_phys - omega_r_phys               # flat, as script_01
TAU_TOR      = 0.9975   # calibrated damping of c_s (script_01, Appendix D)
Z_DRAG       = 1059.94  # Planck 2018 Table 2
Z_START      = 1e7      # as script_01


# =============================================================================
# 2. SOUND HORIZON SOLVER
# =============================================================================
def get_rs_physical(omega_spin_phys):
    """
    r_s = TAU_TOR * integral_{z_drag}^{z_start} c_s(z) / H_ECF(z) dz   (as script_01)
    H_ECF^2 = 1e4 * [omega_m(1+z)^3 + omega_r(1+z)^4 + omega_spin(1+z)^6 + omega_L]
    c_s(z)  = c / sqrt(3*(1+R)),  R = 0.75*(omega_b/omega_g)/(1+z)

    [v3, 02/10/2026] Replaces the truncated integral of v2 (z from 1089 to 2e5,
    no Lambda), whose LCDM baseline (143.26 Mpc) is inconsistent with the target
    TARGET_RS = 135.65 Mpc, itself derived from the full integral (LCDM 147.1 Mpc).
    omega_spin_phys is the physical density omega_spin,0 = Omega_spin,0 * h^2.
    """
    def hubble(z):
        return 100.0 * np.sqrt(
            omega_m_phys * (1+z)**3 +
            omega_r_phys * (1+z)**4 +
            omega_spin_phys * (1+z)**6 +
            omega_L_phys
        )

    def integrand(z):
        R  = 0.75 * (omega_b_phys / omega_g_phys) / (1+z)
        cs = 299792.458 / np.sqrt(3.0 * (1.0 + R))
        return TAU_TOR * cs / hubble(z)

    try:
        val, _ = quad(integrand, Z_DRAG, Z_START, limit=400)
        return val
    except Exception:
        return np.nan


def solve_parameters(target_rs=TARGET_RS):
    rs_baseline = get_rs_physical(0.0) / TAU_TOR   # LCDM baseline: no torsion damping
    print(f"   ΛCDM baseline (script_01 integral) : {rs_baseline:.2f} Mpc  (paper: 147.1 Mpc)")
    try:
        omega_seed = brentq(
            lambda x: get_rs_physical(x) - target_rs,
            0.0, 1e-8, xtol=1e-16
        )
        return omega_seed
    except Exception as e:
        print(f"   [ERROR] Solver failed: {e}")
        return None


# [02/09/2026] Propagate the r_s uncertainty (not an independent recomputation
# of the four Planck inputs for THIS truncated integral -- see script_01 for
# that, which is the reference solver). sigma(TARGET_RS) = 0.32 Mpc comes from
# script_01_solve_sound_horizon.py's own finite-difference propagation; reusing
# it here shows how that uncertainty translates through THIS script's inversion
# into omega_seed and the 9.3% ratio, which is what this script actually checks.
SIGMA_TARGET_RS = 0.32  # Mpc, from script_01's propagate_rs_ecf_uncertainty()

def propagate_omega_seed_uncertainty(omega_seed_central):
    os_plus  = brentq(lambda x: get_rs_physical(x) - (TARGET_RS + SIGMA_TARGET_RS),
                       0.0, 1e-8, xtol=1e-16)
    os_minus = brentq(lambda x: get_rs_physical(x) - (TARGET_RS - SIGMA_TARGET_RS),
                       0.0, 1e-8, xtol=1e-16)
    sigma_omega_seed = abs(os_plus - os_minus) / 2.0
    ratio_plus  = os_plus  * (1+5600)**6 / (omega_r_phys * (1+5600)**4) * 100
    ratio_minus = os_minus * (1+5600)**6 / (omega_r_phys * (1+5600)**4) * 100
    sigma_ratio = abs(ratio_plus - ratio_minus) / 2.0
    return sigma_omega_seed, sigma_ratio


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
        print(f"   rs (verification)              : {rs_check:.4f} Mpc  (target: {TARGET_RS} {'✓' if abs(rs_check - TARGET_RS) < 0.01 else 'MISMATCH'})")   # [D3] was an unconditional ✓
        print(f"{'-'*65}")

        # --- Ratio evolution ---
        print(f"\n[3] SPIN / RADIATION RATIO EVOLUTION")
        print(f"   rho_spin ∝ (1+z)⁶,  rho_rad ∝ (1+z)⁴  →  ratio ∝ (1+z)²")
        print()
        print(f"   {'z':<10} | {'Ratio (%)':<12} | Note")
        print(f"   {'-'*52}")

        ratio_at_zref = None
        ratio_at_rec = None
        for z in [8000, 5600, 4000, 2000, 1100]:
            ratio = omega_seed * (1+z)**6 / (omega_r_phys * (1+z)**4) * 100
            note  = ""
            if z == 8000:
                note = "Onset of acoustic era"
            if z == 5600:
                ratio_at_zref = ratio
                note = f"Stiff Phase peak  →  paper: {VALEUR_PAPIER*100:.1f}%"
            if z == 1100:
                ratio_at_rec = ratio
                note = "Recombination (CMB last scattering)"
            print(f"   z = {z:<6} | {ratio:>8.3f} %   | {note}")

        print(f"   {'-'*52}")

        # --- Validation ---
        dev  = abs(ratio_at_zref/100 - VALEUR_PAPIER) / VALEUR_PAPIER * 100
        flag = "✓" if dev < 1.0 else "✗"
        print(f"\n[4] VALIDATION — spin ratio @ z_ref=5600 vs. paper")
        print(f"   Computed : {ratio_at_zref:.3f}%")
        print(f"   Paper    : {VALEUR_PAPIER*100:.1f}%")
        print(f"   Deviation: {dev:.2f}%  {flag}")
        print()
        print(f"   → Stiff phase (~9.3%) shrinks rs before recombination.")
        print(f"   → At z=1100, spin contribution ≈ {ratio_at_rec:.2f}% of radiation — CMB fit preserved.")  # [05/10/2026, audit SCRIPT-01] was a hard-coded, stale '< 0.21%'

        print(f"\n[5] UNCERTAINTY PROPAGATION  [02/09/2026, floor]")
        sigma_omega_seed, sigma_ratio = propagate_omega_seed_uncertainty(omega_seed)
        print(f"   sigma(TARGET_RS) = {SIGMA_TARGET_RS} Mpc  (from script_01, reference solver)")
        print(f"   omega_seed       = {omega_seed:.4e} +/- {sigma_omega_seed:.2e}")
        print(f"   spin ratio @ z_ref=5600 = {ratio_at_zref:.3f} +/- {sigma_ratio:.3f} %")
        print(f"   NOTE: this uncertainty comes from propagating r_s's own bar")
        print(f"   through THIS script's inversion, not from an")
        print(f"   independent re-propagation of the four Planck inputs.")

    else:
        print("\n   [FAILURE] Solver aborted.")

    print(f"\n{'='*65}")
    print(f"   NOTE: TAU_TOR held at its calibrated value (one equation, two unknowns).")
    print(f"         Full-precision statistical budget → chicarre.py")
    print(f"{'='*65}\n")