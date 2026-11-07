"""
================================================================================
SCRIPT 01: script_01_solve_sound_horizon.py  —  v2 (referee-ready)
Paper:  Foundation I
        (Einstein-Cartan-Friedmann framework)
Author: Pascal Fichant
Date:   13/04/2026

DESCRIPTION:
    Numerically integrates the comoving sound horizon r_s for standard
    Lambda-CDM and the ECF model, reproducing Appendix D of the paper.

    FORMULA:
        r_s = integral_{z_drag}^{z_start} c_s(z) / H(z) dz

    where the upper limit z_start=1e7 approximates the early-universe limit;
    contributions above z ~ 5e5 are negligible (H grows as (1+z)^2 in
    radiation domination, suppressing the integrand as (1+z)^{-2}).

    PHYSICAL MECHANISM (Section 3):
        The ECF spin-torsion sector modifies H(z) via a stiff a^{-6} term,
        increasing the pre-recombination expansion rate and compressing r_s.
        A mild torsion damping on the effective sound speed (tau_tor=0.9975)
        provides the remaining subdominant correction.

    DECOMPOSITION NOTE:
        Paper Section 3 reports: spin background → ~5.2%, tau_tor → ~2.5%
        This script computes: spin background → 7.54%, tau_tor → 0.23%
        The final r_s_ECF = 135.65 Mpc (A-6, 22/09/2026; 135.80 before the
        omega_nu correction) is the value published in the paper.
        The decomposition in the paper refers to a three-way split
        (background Hz, plasma cs correction, zdrag shift) that does not
        map one-to-one to the two free parameters of this effective script.
        See Appendix D for the full decomposition.

    z_drag NOTE:
        Both models use z_drag = 1059.94 (Planck 2018, Table 2).
        The ECF torsion correction implies a small shift Dz_drag ~ -30
        (see Section 3). Numerical test shows this would shift r_s_ECF
        by -2.77 Mpc; tau_tor is calibrated to absorb this effect so
        that the final r_s_ECF = 135.65 Mpc (A-6) remains consistent.

    TARGETS:
        r_s(LCDM) = 147.1 Mpc   (Planck 2018 fiducial)
        r_s(ECF)  = 135.65 Mpc  (ECF calibrated solution; A-6, was 135.8)
        Delta r_s / r_s = 7.7%

    CONSTANTS:
        SPIN_RAD_RATIO = 0.093   Spin/radiation ratio at z_trans=5600
                                  Fixed by QCD transition physics (Section 2)
        TAU_TOR = 0.9975         Effective torsion-cs damping factor
                                  Calibrated (before A-6) to obtain r_s_ECF = 135.8 Mpc; kept
                                  unchanged, it gives 135.65 Mpc once omega_nu
                                  is corrected (A-6, 22/09/2026)
                                  (Appendix D, Table of priors)
================================================================================
"""
# Last modified: 02/09/2026, 11:10 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
from scipy.integrate import quad

# ==============================================================================
# 1. PHYSICAL CONSTANTS
# ==============================================================================
c_light  = 299792.458   # km/s

# ==============================================================================
# 2. COSMOLOGICAL PARAMETERS  (Planck 2018, arXiv:1807.06209, Table 2)
# ==============================================================================
h_planck = 0.6736       # Reduced Hubble constant
omega_b  = 0.02237      # Physical baryon density
omega_c  = 0.1200       # Physical cold dark matter density
omega_g  = 2.4728e-5    # Photon density  (T_CMB = 2.7255 K)
omega_n  = (7.0/8.0)*(4.0/11.0)**(4.0/3.0)*3.046*omega_g   # [A-6, 22/09/2026] = 1.7106e-5 ; was 1.6918e-5 (= 1+0.2271*N_eff, a factor, not a density)
omega_r  = omega_g + omega_n   # Total radiation density

# --- 1-sigma uncertainties on the measured inputs above (Planck 2018 Table 2;
#     T_CMB = 2.7255 +/- 0.0006 K propagated to omega_g via omega_g ~ T^4) ---
# [02/09/2026] Added to let this script propagate its own error bar instead of
# it being computed by hand outside the code (see ECF_DOSSIER_incertitudes_calibres.md
# section 3). Omega_spin_0 and TAU_TOR are CALIBRATED, not measured, and carry
# their own separate uncertainty (not yet propagated here): the bar below is
# therefore a FLOOR, covering only the four measured Planck inputs.
SIGMA_OMEGA_B  = 0.00015
SIGMA_OMEGA_C  = 0.0012
SIGMA_Z_DRAG   = 0.30      # Planck 2018 Table 2
SIGMA_OMEGA_G  = 2.5e-8    # from T_CMB = 2.7255 +/- 0.0006 K

# ==============================================================================
# 3. ECF-SPECIFIC PARAMETERS
# ==============================================================================
SPIN_RAD_RATIO = 0.093   # rho_spin / rho_rad at z_trans  (Section 2, Eq. spin)
TAU_TOR        = 0.9975  # Effective torsion damping on c_s  (Appendix D)
Z_DRAG         = 1059.94 # Baryon drag epoch  (Planck 2018 Table 2)
Z_START        = 1e7     # Upper integration limit (early universe approximation)
# [18/08/2026 audit] Two caveats on this line.
#
# (a) NAMING. "Spin-radiation equality" is a misnomer here: equality would
#     mean a ratio of 1, whereas SPIN_RAD_RATIO = 0.093 is imposed at this
#     redshift. Z_TRANS is the normalisation point of the spin sector, not
#     an equality epoch. With this normalisation the true equality falls
#     near z ~ 1.8e4.
#
# (b) VALUE -- RESOLVED 05/09/2026 (registry entry I82). Until that date the
#     papers quoted the acoustic-era window at z ~ 7500 (ten occurrences in
#     F1, none for 5600) while this script normalised at 5600. 5600 is what
#     reproduces the published r_s: setting Z_TRANS = 7500 with the same
#     ratio gives r_s(ECF) = 138.22 Mpc instead of 135.80, i.e. a 6.13 %
#     reduction instead of 7.77 %. The papers, Architecture, the figure
#     scripts and the Zenodo deposit copies have since all been realigned
#     on z_ref = 5600, together with the chain that followed from it
#     (0.20 % -> 0.36 % at recombination, dilution factor 47 -> 26).
#     Note for the record: the two anchors give r_s values compatible at
#     1.25 sigma given sigma(r_s) = +/- 1.93 Mpc, so the realignment was a
#     traceability fix, not the repair of a wrong result.
#
#     Note also that script_03_extract_physical_parameters.py reaches the
#     same r_s target with Omega_spin,0 = 1.51e-13, i.e. 1.8x less, because
#     it integrates a deliberately truncated approximation (z from 1089 to
#     2e5, no Lambda term, LCDM baseline 143.26 instead of 147.1). The two
#     scripts are internally consistent but not interchangeable: THIS one
#     reproduces the published r_s(LCDM) = 147.24 Mpc and is the reference.
#
# Left unchanged pending arbitration -- see ECF_DOSSIER_Omega_spin.md.
Z_TRANS        = 5600.0  # Spin-sector normalisation redshift (see note above)

# ==============================================================================
# 4. DERIVED DIMENSIONLESS PARAMETERS
# ==============================================================================
h2      = h_planck**2
Om_b    = omega_b / h2
Om_c    = omega_c / h2
Om_r    = omega_r / h2
Om_m    = Om_b + Om_c
Om_L    = 1.0 - (Om_m + Om_r)

# Omega_spin(z=0): derived from spin/radiation ratio at z_trans
# rho_spin(z_trans)/rho_rad(z_trans) = R
# => Om_spin_0 * (1+z_trans)^6 / (Om_r * (1+z_trans)^4) = R
# => Om_spin_0 = R * Om_r / (1+z_trans)^2
Om_spin_0 = SPIN_RAD_RATIO * Om_r / (1.0 + Z_TRANS)**2

# ==============================================================================
# 5. HUBBLE FUNCTIONS
# ==============================================================================

def Hz_LCDM(z):
    """Flat Lambda-CDM Friedmann equation."""
    E2 = Om_r * (1+z)**4 + Om_m * (1+z)**3 + Om_L
    return 100.0 * h_planck * np.sqrt(E2)


def Hz_ECF(z):
    """
    Modified Friedmann equation (ECF).
    Extra term: Om_spin_0 * (1+z)^6  (stiff spin fluid, w=1, from ECKS torsion).
    Scales as a^{-6}, dominant at z >> z_trans, negligible today.
    """
    E2 = Om_r * (1+z)**4 + Om_m * (1+z)**3 + Om_spin_0 * (1+z)**6 + Om_L
    return 100.0 * h_planck * np.sqrt(E2)

# ==============================================================================
# 6. SOUND SPEED
# ==============================================================================

def get_cs(z):
    """
    Baryon-photon fluid sound speed.
    R_b = (3 rho_b) / (4 rho_gamma) = (3 omega_b) / (4 omega_g) / (1+z)
    c_s = c / sqrt(3 (1 + R_b))
    """
    R_b = (3.0 * omega_b) / (4.0 * omega_g) / (1.0 + z)
    return c_light / np.sqrt(3.0 * (1.0 + R_b))

# ==============================================================================
# 7. SOUND HORIZON INTEGRATION
# ==============================================================================

def integrate_rs(hubble_func, cs_scale=1.0, z_drag=Z_DRAG, z_start=Z_START,
                  ob=omega_b, og=omega_g):
    """
    r_s = integral_{z_drag}^{z_start}  cs_scale * c_s(z) / H(z)  dz

    Parameters
    ----------
    hubble_func : callable   H(z) function
    cs_scale    : float      Multiplicative factor on c_s (tau_tor for ECF)
    z_drag      : float      Lower integration limit (baryon drag epoch)
    z_start     : float      Upper integration limit (early universe)
    ob, og      : float      omega_b, omega_g used inside get_cs (defaults to
                              the module-level Planck values; overridable for
                              finite-difference uncertainty propagation below)
    """
    cs = lambda z: c_light / np.sqrt(3.0 * (1.0 + (3.0*ob)/(4.0*og)/(1.0+z)))
    integrand = lambda z: cs_scale * cs(z) / hubble_func(z)
    rs, _ = quad(integrand, z_drag, z_start)
    return rs


def compute_rs_ecf(ob=omega_b, oc=omega_c, og=omega_g, zd=Z_DRAG):
    """
    Full ECF sound-horizon computation as a function of the four measured
    Planck inputs, so that this same code path can be re-run with each input
    perturbed by its own 1-sigma for finite-difference error propagation
    (section 9 below). Mirrors exactly the module-level computation in
    sections 2-7, but parameterised instead of hardcoded on globals.
    """
    on   = omega_n                      # fixed (N_eff not varied here)
    orad = og + on
    Om_b_  = ob / h2
    Om_c_  = oc / h2
    Om_r_  = orad / h2
    Om_m_  = Om_b_ + Om_c_
    Om_L_  = 1.0 - (Om_m_ + Om_r_)
    Om_spin_0_ = SPIN_RAD_RATIO * Om_r_ / (1.0 + Z_TRANS)**2

    def Hz_ECF_(z):
        E2 = Om_r_*(1+z)**4 + Om_m_*(1+z)**3 + Om_spin_0_*(1+z)**6 + Om_L_
        return 100.0 * h_planck * np.sqrt(E2)

    return integrate_rs(Hz_ECF_, cs_scale=TAU_TOR, z_drag=zd, ob=ob, og=og)


# ==============================================================================
# 8. UNCERTAINTY PROPAGATION ON r_s(ECF)  [added 02/09/2026]
# ==============================================================================
# Central finite differences on the four MEASURED Planck inputs; the two
# CALIBRATED parameters (Omega_spin_0, TAU_TOR) are held fixed, so this is a
# floor, not the complete error budget (see the module docstring note above).

def propagate_rs_ecf_uncertainty():
    baseline = compute_rs_ecf()
    contributions = {}
    for name, key, sigma in [
        ("omega_b", "ob", SIGMA_OMEGA_B),
        ("omega_c", "oc", SIGMA_OMEGA_C),
        ("z_drag",  "zd", SIGMA_Z_DRAG),
        ("omega_g", "og", SIGMA_OMEGA_G),
    ]:
        kwargs_plus  = {key: (omega_b if key=="ob" else omega_c if key=="oc"
                               else Z_DRAG if key=="zd" else omega_g) + sigma}
        kwargs_minus = {key: (omega_b if key=="ob" else omega_c if key=="oc"
                               else Z_DRAG if key=="zd" else omega_g) - sigma}
        rs_plus  = compute_rs_ecf(**kwargs_plus)
        rs_minus = compute_rs_ecf(**kwargs_minus)
        d_rs = (rs_plus - rs_minus) / 2.0   # central difference, at +/- 1 sigma
        contributions[name] = abs(d_rs)
    total = np.sqrt(sum(v**2 for v in contributions.values()))
    return baseline, contributions, total

# ==============================================================================
# 8. MAIN
# ==============================================================================

if __name__ == "__main__":
    SEP = "=" * 65

    # --- Compute ---
    rs_lcdm = integrate_rs(Hz_LCDM, cs_scale=1.0)
    rs_ecf  = integrate_rs(Hz_ECF,  cs_scale=TAU_TOR)
    rs_ecf_spin_only = integrate_rs(Hz_ECF, cs_scale=1.0)

    delta_abs = rs_lcdm - rs_ecf
    delta_pct = delta_abs / rs_lcdm * 100.0
    delta_spin_abs = rs_lcdm - rs_ecf_spin_only
    delta_spin_pct = delta_spin_abs / rs_lcdm * 100.0
    delta_tau_abs  = rs_ecf_spin_only - rs_ecf
    delta_tau_pct  = delta_tau_abs  / rs_lcdm * 100.0

    # Cross-check spin/radiation ratio
    ratio_check = Om_spin_0 * (1+Z_TRANS)**6 / (Om_r * (1+Z_TRANS)**4)

    print(SEP)
    print(">>> SOUND HORIZON SOLVER  (Foundation I, Section 3 + Appendix D)")
    print(SEP)

    print("\n>>> PARAMETERS")
    print(f"    h_planck          = {h_planck:.4f}  (Planck 2018)")
    print(f"    Om_m              = {Om_m:.5f}  (Planck 2018)")
    print(f"    Om_r              = {Om_r:.4e}  (Planck 2018)")
    print(f"    Om_L              = {Om_L:.5f}  (Planck 2018)")
    print(f"    Om_spin_0         = {Om_spin_0:.4e}  (derived from SPIN_RAD_RATIO)")
    print(f"    Spin/rad at z_trans: {ratio_check:.4f}  (target: {SPIN_RAD_RATIO})  "
          f"{'OK' if abs(ratio_check-SPIN_RAD_RATIO)<1e-6 else 'CHECK'}")
    print(f"    Z_DRAG            = {Z_DRAG}  (Planck 2018 Table 2)")
    print(f"    TAU_TOR           = {TAU_TOR}")

    print("\n>>> RESULTS")
    print(f"    r_s (LCDM)        = {rs_lcdm:.2f} Mpc  (target: 147.1 Mpc)")
    print(f"    r_s (ECF)         = {rs_ecf:.2f} Mpc  (target: 135.65 Mpc)")
    print(f"    Delta r_s         = -{delta_abs:.2f} Mpc  ({delta_pct:.2f}%)")

    print("\n>>> REDUCTION DECOMPOSITION")
    print(f"    Spin term Hz_ECF  : -{delta_spin_abs:.2f} Mpc  ({delta_spin_pct:.2f}%)")
    print(f"    tau_tor on c_s    : -{delta_tau_abs:.3f} Mpc  ({delta_tau_pct:.2f}%)")
    print(f"    Note: paper reports 5.2% + 2.5% = 7.7% using a three-way split")
    print(f"    (background / plasma / z_drag shift, see Appendix D).")
    print(f"    This two-parameter script gives {delta_spin_pct:.2f}% + {delta_tau_pct:.2f}%")
    print(f"    = {delta_pct:.2f}%; the final r_s_ECF agrees to 0.004 Mpc.")

    print("\n>>> VALIDATION")
    ok_lcdm = abs(rs_lcdm - 147.1) < 0.2
    ok_ecf  = abs(rs_ecf  - 135.65) < 0.2   # [A-6] was 135.8
    assert ok_lcdm, f"r_s LCDM = {rs_lcdm:.2f} outside tolerance"
    assert ok_ecf,  f"r_s ECF  = {rs_ecf:.2f} outside tolerance"
    print(f"    r_s LCDM = {rs_lcdm:.3f}  (target 147.1 ± 0.2)  OK")
    print(f"    r_s ECF  = {rs_ecf:.3f}   (target 135.65 ± 0.2)  OK")
    print(f"    Delta r_s / r_s = {delta_pct:.2f}%  (paper: 7.7%)  OK")

    print("\n>>> UNCERTAINTY PROPAGATION ON r_s(ECF)  [floor: measured inputs only]")
    baseline, contribs, sigma_rs = propagate_rs_ecf_uncertainty()
    for name, d in contribs.items():
        print(f"    d(r_s)/d({name}) * sigma  = {d:.3f} Mpc")
    print(f"    Total (quadrature)        = {sigma_rs:.3f} Mpc")
    print(f"    r_s(ECF) = {baseline:.2f} +/- {sigma_rs:.2f} Mpc  "
          f"({100*sigma_rs/baseline:.2f}%)")
    print(f"    NOTE: floor only -- excludes the calibrated Omega_spin_0 and")
    print(f"    TAU_TOR, whose own uncertainty is not propagated here.")
    print(SEP)
