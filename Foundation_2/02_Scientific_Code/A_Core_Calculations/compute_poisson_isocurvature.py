#!/usr/bin/env python3
"""
compute_poisson_isocurvature.py
================================
Foundation II -- fills an audit gap found on 30/08/2026 (ECF_CHANTIER_
pavage_bulles_29-08.md): the "frozen knot network" paragraph (F2,
Introduction, "Note on the Primordial Power Spectrum") quoted an M_eff
and a Poisson power P_Poisson with NO REPRODUCIBLE SCRIPT behind them,
and with a stale M_micro value (6.1e24 kg instead of the corrected
3.74e24 kg).

THIS SCRIPT REDOES THE FULL CALCULATION, TRANSPARENTLY AND VERIFIABLY:
  1. Imports M_micro FROM calculate_microknot_mass.py (never redefined).
  2. Independently checks the "M_eff = 3 x M_micro" factor by analytically
     integrating the moments of the power-law dn/dM ~ M^(-7/2) (alpha=5/2),
     rather than assuming it.
  3. Computes P_Poisson = M_eff / rho_DM_bar with the standard present-day
     mean dark-matter density (Omega_DM * rho_crit,0).
  4. Compares against the value quoted in the text (P_Poisson ~ 4e-17 Mpc^3)
     and against the claimed "twenty orders of magnitude" gap relative to
     the observed adiabatic power.

Does NOT guess any missing factor: if the result does not match the
current text, this is reported explicitly, without blindly editing the
text to match.
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import os
import sys
import importlib.util as _ilu
import numpy as np

# -- Import M_micro from THE canonical script (never re-derived) -----------
_ROOT = os.path.dirname(os.path.abspath(__file__))
_spec = _ilu.spec_from_file_location(
    "microknot_mass", os.path.join(_ROOT, "calculate_microknot_mass.py"))
_mk = _ilu.module_from_spec(_spec)
sys.argv_backup = sys.argv
sys.argv = ["compute_poisson_isocurvature.py"]  # avoid side effects from argv
_spec.loader.exec_module(_mk)
sys.argv = sys.argv_backup

H_calc = _mk.hubble_rate(_mk.T_C)
M_MICRO = _mk.horizon_mass(H_calc)

print("="*72)
print("  STEP 1 -- M_micro imported (never redefined locally)")
print("="*72)
print(f"\n  M_micro = {M_MICRO:.3e} kg  (source: calculate_microknot_mass.py)\n")

# -- Standard physical constants --------------------------------------------
G = 6.674e-11          # m^3 kg^-1 s^-2
Msun = 1.989e30        # kg
Mpc_to_m = 3.0857e22   # m

H0_kms_Mpc = 67.4
H0_SI = H0_kms_Mpc * 1000 / Mpc_to_m   # s^-1
Om = 0.315
Ob = 0.049
Odm = Om - Ob

rho_crit0 = 3 * H0_SI**2 / (8*np.pi*G)     # kg/m^3
rho_DM_bar = Odm * rho_crit0                # kg/m^3

print("="*72)
print("  STEP 2 -- INDEPENDENT check of the 'M_eff = 3 x M_micro' factor")
print("="*72)
print("""
  Corpus text: dn/dM ~ M^(-7/2)  (alpha=5/2), moments dominated by the
  lower cutoff M_micro. Analytic integral from M_micro to infinity:

    <M>   = integral[M   * M^(-7/2) dM] / integral[M^(-7/2) dM] = (5/3) M_micro
    <M^2> = integral[M^2 * M^(-7/2) dM] / integral[M^(-7/2) dM] = 5 * M_micro^2

    M_eff = <M^2>/<M> = 5*M_micro^2 / [(5/3)*M_micro] = 3 * M_micro
""")
MEFF_FACTOR = 3.0   # verified analytically above, NOT assumed
print(f"  ==> Analytically verified factor: M_eff = {MEFF_FACTOR} x M_micro\n")

M_eff_kg = MEFF_FACTOR * M_MICRO
M_eff_Msun = M_eff_kg / Msun

print("="*72)
print("  STEP 3 -- M_eff with the CORRECT (updated) M_micro value")
print("="*72)
print(f"\n  M_eff = {MEFF_FACTOR} x {M_MICRO:.3e} kg = {M_eff_kg:.3e} kg")
print(f"        = {M_eff_Msun:.3e} Msun\n")

print("="*72)
print("  STEP 4 -- P_Poisson = M_eff / rho_DM_bar")
print("="*72)
print(f"\n  Omega_DM = Omega_m - Omega_b = {Om} - {Ob} = {Odm:.3f}")
print(f"  rho_crit,0 = {rho_crit0:.3e} kg/m^3")
print(f"  rho_DM_bar = Omega_DM * rho_crit,0 = {rho_DM_bar:.3e} kg/m^3\n")

P_Poisson_m3 = M_eff_kg / rho_DM_bar
P_Poisson_Mpc3 = P_Poisson_m3 / Mpc_to_m**3

print(f"  P_Poisson = {M_eff_kg:.3e} / {rho_DM_bar:.3e} = {P_Poisson_m3:.3e} m^3")
print(f"            = {P_Poisson_Mpc3:.3e} Mpc^3\n")

print("="*72)
print("  STEP 5 -- COMPARISON with the current corpus text (F2, l.885-889)")
print("="*72)

M_micro_OLD = 6.1e24   # stale value quoted in the text
M_eff_OLD_Msun = MEFF_FACTOR * M_micro_OLD / Msun
P_Poisson_OLD_quoted_Mpc3 = 4e-17   # value as printed in the text
M_eff_quoted_Msun = 1.5e-6           # value as printed in the text

print(f"""
  {'Quantity':<28}{'Current text (stale)':<24}{'This script (correct M_micro)'}
  {'-'*28}{'-'*24}{'-'*30}
  {'M_micro used':<28}{M_micro_OLD:.3e} kg{'':<8}{M_MICRO:.3e} kg
  {'M_eff (computed, 3x)':<28}{M_eff_OLD_Msun:.3e} Msun{'':<5}{M_eff_Msun:.3e} Msun
  {'M_eff (quoted in text)':<28}{M_eff_quoted_Msun:.3e} Msun{'':<5}(compare above)
  {'P_Poisson (quoted in text)':<28}{P_Poisson_OLD_quoted_Mpc3:.3e} Mpc^3{'':<3}{P_Poisson_Mpc3:.3e} Mpc^3
""")

gap_Meff = M_eff_quoted_Msun / M_eff_OLD_Msun
print(f"  Warning: the M_eff QUOTED in the text ({M_eff_quoted_Msun:.2e} Msun) does")
print(f"  NOT follow from 3xM_micro_OLD ({M_eff_OLD_Msun:.2e} Msun) -- ratio {gap_Meff:.2f}.")
print(f"  The original paragraph already carried an internal inconsistency,")
print(f"  INDEPENDENT of the M_micro correction made on 27/08.\n")

print("="*72)
print("  STEP 6 -- does the qualitative argument still hold regardless?")
print("="*72)
# Typical observed adiabatic power, standard order of magnitude at k~0.05-0.2 Mpc^-1
P_adiabatic_typical_Mpc3 = 1e4   # standard order of magnitude, Mpc^3, to be confirmed if needed

gap_orders = np.log10(P_adiabatic_typical_Mpc3 / P_Poisson_Mpc3)
print(f"""
  Typical observed adiabatic power (standard order of magnitude)
     ~ {P_adiabatic_typical_Mpc3:.0e} Mpc^3

  With the CORRECTED M_micro value, P_Poisson = {P_Poisson_Mpc3:.3e} Mpc^3
  ==> Gap: approximately {gap_orders:.1f} orders of magnitude BELOW the
      observed adiabatic power.

  The text claimed "some twenty orders of magnitude". With the CORRECTED
  M_micro value, the gap found here is {gap_orders:.0f} orders --
  {"close to" if abs(gap_orders-20)<3 else "DIFFERENT from"} the text's claim.
  The QUALITATIVE CONCLUSION (the frozen network cannot source the
  primordial spectrum) appears robust either way -- the gap is
  overwhelming regardless -- but the PRECISE number quoted must be
  updated.
""")

print("="*72)
print("  SUMMARY -- WHAT MUST CHANGE IN THE F2 TEXT (around line 885-889)")
print("="*72)
print(f"""
  1. "computed as 6.1e24 kg" -> "computed as {M_MICRO:.2e} kg"
     (M_micro corrected on 27/08/2026, already used everywhere else).
  2. "M_eff = 3 M_micro ~= 1.5e-6 Msun" -> "M_eff = 3 M_micro ~= {M_eff_Msun:.2e} Msun"
     (the "1.5e-6" figure did NOT already follow from 3xM_micro_OLD --
     a double correction is needed, not just the M_micro update).
  3. "P_Poisson ~ 4e-17 Mpc^3" -> "P_Poisson ~ {P_Poisson_Mpc3:.1e} Mpc^3"
  4. "some twenty orders of magnitude below" -> rephrase with the exact
     number found above ({gap_orders:.0f} orders), after confirming the
     adiabatic reference value used here (order-of-magnitude only --
     TO BE CONFIRMED before publication).
""")
