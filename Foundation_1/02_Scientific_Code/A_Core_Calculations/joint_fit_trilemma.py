#!/usr/bin/env python3
"""
joint_fit_trilemma.py -- ECF Foundation I/II
Last modified: 24/07/2026, 13:20 (sigma theta_* corrected + sensitivity scan)
Joint H0-Age-BAO-CMB fit (the omega_m lead, 20/07/2026)

CONTEXT
-------
The existing scripts (script_01_solve_sound_horizon.py,
plot_trilemma_irreducibility.py) treat Om_m=0.315 (the Planck value at
h=0.6736) as fixed, without recomputing it for H0_ECF=73.04. This script
corrects that: omega_m = omega_b + omega_c (PHYSICAL densities, fixed by
CMB measurements independently of H0) is the fundamental parameter, and
Om_m = omega_m / h_ECF^2 follows from it. r_s is recomputed
self-consistently for every omega_m tested, instead of being frozen at
135.8 Mpc.

CONSTRAINTS FITTED JOINTLY (at fixed H0 = 73.04):
  1. BAO  : D_M(z=1.48)/r_s = 30.21 +/- 0.79        (Hou+2021, eBOSS DR16)
  2. Age  : t0 = 13.32 +/- 0.08 Gyr                 (Valcin+2021)
  3. CMB  : 100*theta_* -- see the dedicated block below for the target
            and, importantly, for the uncertainty actually used.

FREE PARAMETERS  : omega_c (physical CDM density), w0, wa
FIXED PARAMETERS : H0 = 73.04, omega_b = 0.02237 (BBN + CMB baryon
                   acoustic peak ratio; very well measured, not
                   questioned here)

EXPECTED CROSS-CHECK. If no point satisfies chi2_total below a reasonable
threshold (say chi2 < 3 per constraint, i.e. ~1 sigma combined), this
CONFIRMS and SHARPENS the 19-20/07 conclusion -- that the trilemma is in
fact a quadrilemma including omega_m^CMB -- rather than contradicting it.

WHAT IS AND IS NOT ROBUST HERE (read before quoting any number).
The *sign* and *order of magnitude* of the required omega_m shift are
robust; its precise value is not, because it depends on the weight given
to theta_*. The script therefore prints a sensitivity scan rather than a
single figure. Definitive quantification requires a Boltzmann-code
treatment (CLASS-EC), not the approximate theta_* integral used here.
"""

import numpy as np
from scipy import integrate, optimize

# -----------------------------------------------------------------------
# 1. CONSTANTES FIXES
# -----------------------------------------------------------------------
c_light = 299792.458          # km/s
H0 = 73.04                    # km/s/Mpc -- FIXE (SH0ES/ECF)
h_ecf = H0/100.0

omega_b  = 0.02237            # Densite baryonique physique (Planck 2018 + BBN)
omega_g  = 2.4728e-5
omega_n  = 1.6918e-5
omega_r_fixed = omega_g + omega_n

SPIN_RAD_RATIO = 0.093
TAU_TOR        = 0.9975
Z_DRAG         = 1059.94
Z_STAR         = 1089.90      # Recombination (CMB), distinct from z_drag
Z_START_INT    = 2e5
Z_TRANS        = 5600.0
z_bao          = 1.48

# Cibles observationnelles + incertitudes (1 sigma)
TARGET_BAO_RATIO, SIG_BAO   = 30.21, 0.79        # Hou+2021 eBOSS DR16
TARGET_AGE, SIG_AGE          = 13.32, 0.08        # Valcin+2021
# --- theta_*: BOTH the target and the uncertainty are specific to THIS model -
# Target: the self-consistent LCDM value of the simplified integral used here
#   (1.03116), and NOT the literature Planck value (1.04109). Comparing this
#   model against the literature would conflate model error with genuine
#   disagreement.
#
# Uncertainty [CORRECTED 24/07/2026]: we deliberately do NOT use Planck's
#   observational error bar (0.00030). The theta_* integral used here is
#   approximate -- it already departs by ~1% from the reference value on
#   standard LCDM. Assigning it an error bar 30x tighter than its own
#   systematic error would give it unwarranted weight: with 0.00030, theta_*
#   outweighed BAO and age combined by a factor ~1e4, and the optimiser
#   collapsed omega_m by 46% purely to satisfy it. We therefore adopt an
#   uncertainty dominated by the model systematic (~1%), and we document how
#   sensitive the result is to that choice (see the scan at the end).
TARGET_THETA100 = 1.03116
SIG_THETA       = 0.0103          # ~1% : systematique du modele, pas Planck

Gyr_conv = 977.79222168

# -----------------------------------------------------------------------
# 2. MODELE  (omega_c, w0, wa) -> observables
# -----------------------------------------------------------------------
def observables(omega_c, w0, wa):
    omega_m = omega_b + omega_c
    h2 = h_ecf**2
    Om_m = omega_m/h2
    Om_r = omega_r_fixed/h2
    Om_L = 1.0 - (Om_m + Om_r)
    if Om_L <= 0:
        return None
    Om_spin_0 = SPIN_RAD_RATIO*Om_r/(1+Z_TRANS)**2

    def de_evol(z):
        return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

    def Hz(z):
        E2 = Om_r*(1+z)**4 + Om_m*(1+z)**3 + Om_spin_0*(1+z)**6 + Om_L*de_evol(z)
        return 100.0*h_ecf*np.sqrt(E2)

    def cs(z):
        Rb = (3.0*omega_b)/(4.0*omega_g)/(1+z)
        return c_light/np.sqrt(3.0*(1+Rb))

    # r_s at drag epoch (BAO ruler) and at z* (CMB ruler) -- slightly different
    rs_drag, _ = integrate.quad(lambda z: TAU_TOR*cs(z)/Hz(z), Z_DRAG, Z_START_INT, limit=100)
    rs_star, _ = integrate.quad(lambda z: TAU_TOR*cs(z)/Hz(z), Z_STAR, Z_START_INT, limit=100)

    # Comoving distance to z_bao and to z*
    D_M_bao, _ = integrate.quad(lambda z: c_light/Hz(z), 0, z_bao, limit=100)
    D_M_star, _ = integrate.quad(lambda z: c_light/Hz(z), 0, Z_STAR, limit=150)
    D_A_star = D_M_star  # comoving angular diameter distance = D_M for flat universe; theta_MC convention uses D_M directly, not D_M/(1+z)

    age_int, _ = integrate.quad(lambda z: 1.0/((1+z)*Hz(z)/H0), 0, 3000, limit=150)
    age_gyr = age_int*Gyr_conv/H0

    bao_ratio = D_M_bao/rs_drag
    theta100 = 100.0*rs_star/D_A_star

    return dict(rs_drag=rs_drag, rs_star=rs_star, D_M_bao=D_M_bao,
                bao_ratio=bao_ratio, theta100=theta100, age=age_gyr,
                Om_m=Om_m, omega_m=omega_m)

# -----------------------------------------------------------------------
# 3. CHI2 COMBINE
# -----------------------------------------------------------------------
def chi2_total(params, verbose=False):
    omega_c, w0, wa = params
    obs = observables(omega_c, w0, wa)
    if obs is None:
        return 1e6
    chi2_bao   = ((obs['bao_ratio']-TARGET_BAO_RATIO)/SIG_BAO)**2
    chi2_age   = ((obs['age']-TARGET_AGE)/SIG_AGE)**2
    chi2_theta = ((obs['theta100']-TARGET_THETA100)/SIG_THETA)**2
    total = chi2_bao+chi2_age+chi2_theta
    if verbose:
        print(f"  omega_c={omega_c:.5f} (omega_m={obs['omega_m']:.5f}, Om_m={obs['Om_m']:.4f}), "
              f"w0={w0:.3f}, wa={wa:.3f}")
        print(f"  -> BAO ratio={obs['bao_ratio']:.3f} (target {TARGET_BAO_RATIO}+/-{SIG_BAO}), chi2={chi2_bao:.2f}")
        print(f"  -> Age={obs['age']:.3f} Gyr (target {TARGET_AGE}+/-{SIG_AGE}), chi2={chi2_age:.2f}")
        print(f"  -> 100*theta*={obs['theta100']:.5f} (target {TARGET_THETA100}+/-{SIG_THETA}), chi2={chi2_theta:.2f}")
        print(f"  -> r_s(drag)={obs['rs_drag']:.2f} Mpc, r_s(z*)={obs['rs_star']:.2f} Mpc")
        print(f"  -> chi2_total={total:.3f}")
    return total

# -----------------------------------------------------------------------
# 4. MINIMISATION
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("="*70)
    print("  JOINT H0-AGE-BAO-CMB FIT (omega_c, w0, wa free)")
    print("  H0 = 73.04 km/s/Mpc held fixed")
    print("="*70)

    omega_c_planck = 0.1200
    x0 = [omega_c_planck, -0.904, -0.153]  # start from Planck omega_c + calibrated (w0,wa)

    print("\n>>> STARTING POINT (Planck omega_c + ECF-calibrated (w0,wa))")
    chi2_total(x0, verbose=True)

    res = optimize.minimize(chi2_total, x0, method='Nelder-Mead',
                             options={'xatol':1e-6,'fatol':1e-6,'maxiter':5000})

    print("\n>>> BEST FIT FOUND")
    chi2_total(res.x, verbose=True)

    print(f"\n>>> Convergence: {res.success}, iterations: {res.nit}")

    # Sanity: how far is omega_c from Planck's value?
    omega_m_best = omega_b + res.x[0]
    print(f"\n>>> omega_m best-fit = {omega_m_best:.5f}  vs Planck omega_m = {omega_b+omega_c_planck:.5f}"
          f"  (deviation: {(omega_m_best-(omega_b+omega_c_planck))/(omega_b+omega_c_planck)*100:+.2f}%)")

    # -----------------------------------------------------------------------
    # SENSITIVITY TO THE theta_* UNCERTAINTY  [added 24/07/2026]
    # The result depends strongly on the weight given to theta_*. We expose that
    # dependence rather than publishing a single figure that would convey false
    # precision.
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print("  SENSITIVITY TO THE CHOICE OF sigma(theta_*)")
    print("="*70)
    print("  The theta_* integral used here carries a ~1% systematic of its own.")
    print("  Using Planck's observational error bar (0.00030) over-weights")
    print("  theta_* by a factor ~30 and exaggerates the omega_m shift required.\n")
    print(f"  {'sigma':>9} | {'omega_m':>8} | {'vs Planck':>12} | {'BAO err':>8} | {'Age':>6}")
    print("  " + "-"*56)
    for sig, lab in [(0.00030, "Planck obs."), (0.0103, "1% model syst."), (0.0206, "2% conservative")]:
        def _c2(prm):
            oc, w0_, wa_ = prm
            o = observables(oc, w0_, wa_)
            if o is None: return 1e6
            return (((o['bao_ratio']-TARGET_BAO_RATIO)/SIG_BAO)**2
                  + ((o['age']-TARGET_AGE)/SIG_AGE)**2
                  + ((o['theta100']-TARGET_THETA100)/sig)**2)
        rr = optimize.minimize(_c2, x0, method='Nelder-Mead',
                               options={'xatol':1e-7,'fatol':1e-7,'maxiter':8000})
        o = observables(*rr.x)
        dev = (o['omega_m']-0.14237)/0.14237*100
        bao = abs(o['bao_ratio']-TARGET_BAO_RATIO)/TARGET_BAO_RATIO*100
        print(f"  {sig:9.5f} | {o['omega_m']:8.5f} | {dev:+11.1f}% | {bao:7.2f}% | {o['age']:6.2f}   [{lab}]")

    print("""
  HOW TO READ THIS. The numerical size of the required omega_m shift
  (19% to 46%) is NOT robust: it depends on the weight given to theta_*.
  What IS robust is its SIGN and order of magnitude -- omega_m must be
  lowered by several tens of percent, whereas the CMB constrains it to
  ~1%, independently of the late-time expansion history. The quadrilemma
  is therefore real; only its precise quantification awaits a CLASS-EC
  calculation.""")
