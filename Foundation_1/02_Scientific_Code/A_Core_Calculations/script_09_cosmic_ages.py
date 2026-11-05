#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Script      : script_09_cosmic_ages.py
Description : Computes cosmic ages t(z) for the LCDM and ECF backgrounds,
              reproducing every entry of the "Comparison of timescales"
              table in Foundation I.
Produced    : 13/09/2026
Revised     : 06/10/2026 (AGE-01, audit de cohérence du 05/10) -- the spin
              branch of script_09b_cosmic_ages_spin.py (candidate of 02/10,
              never deposited) is merged here. Two outputs:
                without_spin : matter + radiation + Lambda (the former ECF column)
                with_spin    : + Om_spin_0 (1+z)^6, the background that gives
                               r_s = 135.65 Mpc (script_01) -> t_rec = 368.4 kyr
              The script stops if either recombination age drifts.
=============================================================================

WHY THIS SCRIPT EXISTS
    Foundation I quotes t_rec ~ 365,000 yr as "natively derived by integrating
    the Friedmann time-evolution equation", but no script in the corpus
    performed that integration. Every number in the papers must be
    reproducible from code; this closes that gap for the age column.

WHAT IT FOUND
    See the verdict printed at the end, computed since D3 (22/09/2026):
    it compares each computed age with the value quoted by the F1 table.

METHOD
    t(z) = (1/H0) * Int_z^inf dz' / [(1+z') E(z')]
    with E(z) = sqrt(Om_r (1+z)^4 + Om_m (1+z)^3 + Om_spin (1+z)^6 + Om_L),
    Om_spin = 0 for LCDM and for the ECF without_spin branch,
    Om_spin_0 = 0.093 Om_r / (1+z_ref)^2, z_ref = 5600, for ECF with_spin
    (same convention as script_01; Om_L = 1 - Om_m - Om_r as in script_09b).
    The with_spin result is converged in the upper bound (1e8 to 1e14 agree
    to 1e-4 kyr, script_09b).

    NB: the upper bound must reach z ~ 1e8. Truncating at a few thousand
    omits the radiation era and underestimates t(z=1100) by ~7%, while
    leaving t_0 unaffected to 3e-5 -- the integrand concentrates its weight
    differently in the two cases. Log spacing keeps the cost low.

VALIDATION
    At z* = 1089.9 with Planck parameters this returns 371 kyr, against the
    372 kyr published by Planck 2018. The method is therefore sound.
"""
import sys
try:  # [04/10/2026, test E2] UTF-8 guard for Windows cp1252 terminals
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np

# NumPy renamed trapz -> trapezoid in 2.0. The corpus runs on both (some
# scripts still call trapz), so bind whichever is available rather than
# assuming one. Without this, this script fails on NumPy < 2.0 while the
# rest of the pipeline runs fine -- a failure mode that would surface only
# on the reproducing machine, not here.
_trapz = getattr(np, "trapezoid", None) or np.trapz

# -- Constants ---------------------------------------------------------------
MPC = 3.086e22          # m
YR  = 3.156e7           # s

# -- Cosmological parameters -------------------------------------------------
# Om_r = 9.2e-5 includes the neutrino contribution (photons alone give 5.4e-5).
OM_M, OM_R = 0.315, 9.2e-5
OM_M_ECF = (0.02237 + 0.1200)/0.7304**2   # [A-7, 22/09/2026] Omega_m = omega_m/h_ECF^2 = 0.266868 ; was 0.315 (Planck-h value)
H0_LCDM = 67.4          # km/s/Mpc, Planck 2018
H0_ECF  = 73.04         # km/s/Mpc, canonical value of the corpus (SH0ES baseline)
# [D3, 22/09/2026 -- DEC-A7-POST-05] Omega_r of the ECF column = omega_r/h_ECF^2,
# the A-7 rule applied to radiation (was OM_R = 9.2e-5, a Planck-h value, i.e.
# omega_r inflated by (0.7304/0.674)^2 = 1.17). omega_r = omega_g [1 + 7/8
# (4/11)^(4/3) N_eff], omega_g = 2.4728e-5 (script_01, A-6). The LCDM column
# keeps OM_M, OM_R at h = 0.674.
OM_R_ECF = 2.4728e-5*(1 + (7/8)*(4/11)**(4/3)*3.046)/0.7304**2   # 7.8417e-5
# [AGE-01, 06/10/2026] spin term of the modified Friedmann equation, as in script_01
SPIN_RAD_RATIO, Z_REF = 0.093, 5600.0
OM_SPIN_ECF = SPIN_RAD_RATIO*OM_R_ECF/(1 + Z_REF)**2
# Reference values (kyr) at z* = 1089.9, script_09b of 02/10/2026; checked at run time.
T_REC_WITH_SPIN_REF, T_REC_WITHOUT_SPIN_REF, T_REC_TOL = 368.417, 371.799, 0.01


def age(z, H0_kms, Om_m=OM_M, Om_r=OM_R, Om_spin=0.0, n=400000):
    """Time elapsed since the bounce at redshift z, in years.
    Om_spin = 0 : without_spin ; Om_spin = OM_SPIN_ECF : with_spin."""
    H0 = H0_kms * 1e3 / MPC
    Om_L = 1.0 - Om_m - Om_r
    zs = np.logspace(np.log10(1 + z), 8, n) - 1
    E = np.sqrt(Om_r*(1 + zs)**4 + Om_m*(1 + zs)**3 + Om_spin*(1 + zs)**6 + Om_L)
    return _trapz(1/((1 + zs)*E), zs) / H0 / YR


def main():
    print("=" * 86)
    print("COSMIC AGES -- LCDM vs ECF (without_spin / with_spin)")
    print("=" * 86)

    # -- Method validation against a published value -------------------------
    t_planck = age(1089.9, H0_LCDM)/1e3
    print(f"\nValidation: t(z* = 1089.9) at H0 = 67.4 -> {t_planck:.0f} kyr")
    print(f"            Planck 2018 publishes ~372 kyr."
          f"  {'OK' if abs(t_planck-372) < 8 else 'MISMATCH'}")

    # -- The table of Foundation I -------------------------------------------
    # F1 columns = values quoted by the candidate F1 v13 table. The ECF entry of
    # F1 is the with_spin branch (AGE-01, 06/10/2026); without_spin is printed
    # for reference (former ECF column: 13.33 Gyr / 287 Myr / 372 kyr).
    rows = [
        ("Today",          0.0,   "13.81 Gyr", "13.33 Gyr", 1e9, "Gyr"),
        ("JWST galaxies", 14.3,   "290 Myr",   "287 Myr",   1e6, "Myr"),
        ("Recombination", 1089.9, "371 kyr",   "368 kyr",   1e3, "kyr"),
    ]
    print("\n" + "-" * 86)
    print(f"{'Milestone':16}{'z':>8}{'F1 LCDM':>11}{'LCDM':>12}"
          f"{'ECF without_spin':>18}{'F1 ECF':>11}{'ECF with_spin':>15}")
    print("-" * 86)
    res = {}
    for label, z, f1_l, f1_e, div, unit in rows:
        cl = age(z, H0_LCDM)/div
        c0 = age(z, H0_ECF, Om_m=OM_M_ECF, Om_r=OM_R_ECF)/div
        c1 = age(z, H0_ECF, Om_m=OM_M_ECF, Om_r=OM_R_ECF, Om_spin=OM_SPIN_ECF)/div
        res[label] = (cl, c0, c1)
        print(f"{label:16}{z:>8.1f}{f1_l:>11}{cl:>9.3f} {unit}"
              f"{c0:>15.3f} {unit}{f1_e:>11}{c1:>12.3f} {unit}")

    # -- Verdict --------------------------------------------------------------
    print("\n" + "=" * 86)
    print("VERDICT (F1 ECF entry = with_spin branch)")
    print("=" * 86)
    for label, z, f1_l, f1_e, div, unit in rows:
        cl, c0, c1 = res[label]
        ql, qe = float(f1_l.split()[0]), float(f1_e.split()[0])
        print(f"  {label:14} LCDM {cl:8.3f} {unit} (F1 {ql:g}, {100*(cl-ql)/ql:+.1f}%)"
              f"   ECF with_spin {c1:8.3f} {unit} (F1 {qe:g}, {100*(c1-qe)/qe:+.1f}%)"
              f"   spin effect {c1-c0:+.3f} {unit}")
    t_l, t_0, t_1 = res["Recombination"]
    print(f"\n  At z* = 1089.9 :  ECF with_spin - LCDM = {t_1 - t_l:+.2f} kyr ;"
          f"  ECF without_spin - LCDM = {t_0 - t_l:+.2f} kyr ;"
          f"  spin effect = {t_1 - t_0:+.2f} kyr ({100*(t_1 - t_0)/t_0:+.2f} %)")

    # -- Checks (AGE-01) --------------------------------------------------------
    ok1 = abs(t_1 - T_REC_WITH_SPIN_REF) < T_REC_TOL
    ok0 = abs(t_0 - T_REC_WITHOUT_SPIN_REF) < T_REC_TOL
    print(f"\n  check with_spin    t_rec = {t_1:.3f} kyr  (ref {T_REC_WITH_SPIN_REF}, tol {T_REC_TOL}) -> {'OK' if ok1 else 'FAIL'}")
    print(f"  check without_spin t_rec = {t_0:.3f} kyr  (ref {T_REC_WITHOUT_SPIN_REF}, tol {T_REC_TOL}) -> {'OK' if ok0 else 'FAIL'}")
    assert ok1, f"with_spin t_rec = {t_1:.3f} kyr differs from {T_REC_WITH_SPIN_REF} kyr"
    assert ok0, f"without_spin t_rec = {t_0:.3f} kyr differs from {T_REC_WITHOUT_SPIN_REF} kyr"

    print("""
without_spin: with Omega_i = omega_i/h^2 for matter AND radiation (A-7 rule, D3),
the integrand at z >> 1 depends on omega_m and omega_r only, so t(z*) does not
depend on H0; the ECF-LCDM difference then only reflects omega_m (0.14237 for
ECF vs 0.315 x 0.674^2 = 0.1431 for the LCDM column).
with_spin: the spin term Om_spin_0 (1+z)^6 of the modified Friedmann equation
is added; this is the background that gives r_s = 135.65 Mpc (script_01). It
shortens t(z*) by about 3.4 kyr and leaves t_0 and the JWST age unchanged to
better than 0.01 Myr. F_ion does not enter this integral. The recombination
age is not an observable; no signature is claimed from these differences.

History:
RESOLVED 13/09/2026. The table previously quoted 380,000 yr (LCDM) and
365,000 yr (ECF) at z = 1100. The 380,000 figure was the textbook round
number rather than a value computed for these parameters, and the ECF entry
followed from it by subtracting an estimated 15 kyr shift.
Both columns are evaluated at the Planck decoupling redshift z* = 1089.9,
where this script reproduces the published Planck age to within 1 kyr.
02/10/2026: the ECF column (372 kyr) omitted the spin term; script_09b gave
368.4 kyr on the full background. 06/10/2026 (AGE-01): script_09b merged here
as the with_spin branch, so that the script cited by F1 and the Architecture
produces the quoted value.

Tracked as I154 and AGE-01.
""")


if __name__ == "__main__":
    main()
