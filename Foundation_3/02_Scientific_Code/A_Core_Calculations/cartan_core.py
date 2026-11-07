#!/usr/bin/env python3

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
#  ECF / Foundation III - The Cartan core (item CORE-1)
#  Fichant, P. (2026).  File: cartan_core.py
#
#  [Translated to English 24/08/2026 -- rule 5quatervicies: what is deposited
#   is written in English. Physics, numbers and structure unchanged.]
# =============================================================================
#
#  THE ORIGINAL QUESTION (P. Fichant)
#  ----------------------------------
#  "What becomes of the parent's matter that keeps falling in AFTER the
#   bounce? If there is an inner bounce, then re-contraction, then another
#   bounce...?"
#
#  FIRST LINE EXPLORED: damped oscillation of successive bounces converging
#  towards a statically balanced core.
#  => THE INTUITION ABOUT THE RESULT (a static core) PROVED RIGHT, but the
#     MECHANISM is different: it is not a series of damped bounces, because
#     the Friedmann-torsion equation FORBIDS the density from exceeding
#     rho_c (see TEST 1). The core relaxes towards a HYDROSTATIC equilibrium
#     (TOV + torsion), not through FRW oscillations.
#
#  WHAT THIS SCRIPT ESTABLISHES
#  ----------------------------
#   (T1) The bound rho <= rho_c is EXACT (Friedmann-torsion constraint).
#        => no "overshoot and return" oscillation is possible.
#   (T2) A hydrostatic equilibrium exists: torsion repulsion (proportional to
#        rho^2) balances gravity (proportional to rho) at rho_eq ~ rho_c.
#        This is the CARTAN CORE (the analogue of the "Planck star",
#        Rovelli-Vidotto, in loop quantum gravity).
#   (T3) Asymmetry between the first collapse and later accretion: only the
#        initial COHERENT collapse nucleates a child universe.
#   (T4) [ADDED 16/07/2026] The criterion t_dyn << t_acc QUANTIFIED: a margin
#        of 15-17 orders of magnitude in the standard regime (ISM, Eddington).
#        The hypercritical regime (collapsar/GRB) is identified as the only
#        non-trivial boundary (item CORE-1-HYPERACC), diagnosed through
#        Delta_M(t_dyn), and MERGED into the ab initio problem (T2) rather
#        than solved separately.
#
#  WHY IT MATTERS FOR THE CORPUS
#  -----------------------------
#   If every new batch of infalling matter bounced, a black hole would be a
#   "universe factory" and the extended Drake equation (N_fertile =
#   N_BH x f_M x ...) would be invalid. The result established here -- a
#   static core, a single nucleation event -- PRESERVES that count:
#   ONE BLACK HOLE = ONE CHILD UNIVERSE.
#
#  LIMITATIONS
#  -----------
#   [L1] TEST 2 is an ORDER-OF-MAGNITUDE argument (balancing the rho and
#        rho^2 scalings), not a complete TOV-torsion solution. It remains
#        DEFERRED to Foundation IV (multi-session work, numerical
#        relativity). The hypercritical regime (T4/CORE-1-HYPERACC) is the
#        same missing ingredient, not a separate problem.
#   [L2] [CLOSED 16/07/2026 for standard regimes, see T4] The asymmetry (T3)
#        is now QUANTIFIED (margin of 15-17 orders of magnitude,
#        ISM/Eddington). The hypercritical regime stays open (see [L1]).
#   [L3] No backreaction of the core on the exterior metric.
#
#  ⚠️ AUDIT 24/08/2026 -- THE TWO BOUNDS ARE NOT RIVALS, AND THE SCRIPT
#   SHOWS ONLY ONE OF THEM.
#   T1 below derives rho <= rho_c. The final STATUS block announces
#   rho <= rho_c/2. Both are right, and they are DIFFERENT STATEMENTS:
#     * rho <= rho_c   -- the FRIEDMANN bound: kinematic and exact. Beyond
#       it H^2 < 0, so the density simply cannot get there. This is what
#       T1 proves.
#     * rho <  rho_c/2 -- the TOV bound: hydrostatic and finer. With the
#       stiff equation of state, rho_eff = rho(1 - rho/rho_c) is NOT
#       monotonic: it peaks at rho_c/2. A BOUND core must satisfy both
#       dP_eff/dr < 0 (TOV) and drho/dr < 0, and since
#       dP_eff/dr = rho_c c^2 (1 - 2 rho/rho_c) drho/dr, the two are
#       compatible only below rho_c/2.
#       Derived in Foundation III Extended, "Resolution TOV", item CORE-1,
#       which calls it explicitly "the FINER bound".
#   ⇒ This script is not wrong, it is INCOMPLETE: its status block quotes a
#     bound that its own T1 does not establish, without saying where it
#     comes from. A reader running the script alone cannot reconstruct the
#     factor of two. Deriving the TOV bound here would be new work; naming
#     its source costs nothing, and that is what the note below does.
#
#  Reproducibility: Python >= 3.9, numpy. Deterministic.
# =============================================================================

import numpy as np

SEP = "=" * 72

# --- Constants --------------------------------------------------------------
G = 6.674e-11
c = 2.998e8
hbar = 1.055e-34
RHO_C = c**5 / (hbar * G**2)      # Cartan density  [kg/m^3]

print(SEP); print("CARTAN CORE - what becomes of the accreted matter?"); print(SEP)
print(f"  Cartan density: rho_c = c^5/(hbar G^2) = {RHO_C:.3e} kg/m^3")

# =============================================================================
#  TEST 1 - Is the bound rho <= rho_c EXACT?
# =============================================================================
print(); print(SEP); print("T1 - Friedmann-torsion constraint: rho <= rho_c?"); print(SEP)
print("""
  Equation (Poplawski):  H^2 = (8 pi G/3) rho (1 - rho/rho_c)
  Stiff fluid (w=1): rho = rho_c * u^-6,  u = a/a_bounce.
  H^2 >= 0  requires  (1 - u^-6) >= 0  <=>  u >= 1  <=>  rho <= rho_c.
""")
print("  Check:")
for u in [0.90, 0.99, 1.00, 1.10, 1.50, 2.00]:
    x = u**-6                       # rho/rho_c
    H2 = x * (1.0 - x)              # H^2 in units of (8 pi G rho_c/3)
    tag = "FORBIDDEN (H^2 < 0)" if H2 < 0 else "allowed"
    print(f"    u = {u:4.2f}  |  rho/rho_c = {x:7.4f}  |  H^2 = {H2:+7.4f}   {tag}")
print("""
  => The density CANNOT exceed rho_c: it is a WALL, not a turning point one
     could cross. No "overshoot and return" oscillation is possible.
     => The line of successive damped bounces is RULED OUT.""")

# =============================================================================
#  TEST 2 - Does a hydrostatic equilibrium exist? (the Cartan core)
# =============================================================================
print(); print(SEP); print("T2 - Balance: torsion (~rho^2) against gravity (~rho)"); print(SEP)
print("""
  Below the horizon the core is NOT an isolated FRW universe: it is
  permanently compressed by the accreted matter. The relevant framework is
  therefore hydrostatic equilibrium (TOV) with torsion:

      P_eff = P - (kappa/2) sigma^2      [torsion term: REPULSIVE]

  Scalings:   gravity  ~ rho          (linear)
              torsion  ~ rho^2/rho_c  (quadratic)
  Equality defines the equilibrium density.
""")
print("  Ratio (torsion repulsion)/(gravitational attraction) = x:")
for x in [1e-3, 1e-2, 1e-1, 0.5, 0.9, 1.0]:
    ratio = x
    if ratio < 0.1:
        reg = "gravity dominates (collapse)"
    elif ratio < 1.0:
        reg = "torsion not negligible"
    else:
        reg = "EQUILIBRIUM (torsion = gravity)"
    print(f"    rho/rho_c = {x:6.3f}  ->  ratio = {ratio:6.3f}   {reg}")
print(f"""
  => Equilibrium is reached at rho_eq ~ rho_c (up to a factor of order one).
     The black hole therefore holds a STATIC DENSE CORE at the Cartan
     density -- not a singularity. This is the "Cartan core", the analogue
     of the Planck star (Rovelli-Vidotto) in loop quantum gravity.
     rho_eq ~ {RHO_C:.2e} kg/m^3""")

# =============================================================================
#  TEST 3 - Why does only the FIRST collapse nucleate a universe?
# =============================================================================
print(); print(SEP); print("T3 - Asymmetry: coherent collapse vs gradual accretion"); print(SEP)
print("""
  If later accretion produced new bounces, a black hole would spawn SEVERAL
  universes, invalidating the count of the extended Drake equation
  (N_fertile = N_BH x f_M x f_a x ...). An ASYMMETRY between the first
  collapse and what follows is therefore required.

  Proposed mechanism:
    * FIRST COLLAPSE - coherent and dynamical. The whole core falls in
      together (dynamical time t_dyn ~ 1/sqrt(G rho)), reaches rho_c with
      considerable momentum, and opens the Einstein-Rosen bridge: a child
      universe is nucleated.
    * LATER ACCRETION - gradual. Matter arrives drop by drop (accretion time
      t_acc >> t_dyn) onto a core ALREADY at equilibrium. It is absorbed
      without coherent collapse, hence without a bounce, hence without a
      new bridge.

  CRITERION (to be formalised, item CORE-1):
      nucleation  <=>  t_dyn  <<  t_acc
  The initial stellar collapse satisfies it by a wide margin; later Bondi
  accretion does not.
""")
print(f"""{SEP}
CONCLUSION
{SEP}
  * The density is BOUNDED by rho_c (exact result).
  * The core relaxes towards a HYDROSTATIC EQUILIBRIUM at rho ~ rho_c
    (the Cartan core), not through a series of damped bounces.
  * Only the initial coherent collapse nucleates a child universe.
    => ONE BLACK HOLE = ONE CHILD UNIVERSE.
    => The count of the extended Drake equation is PRESERVED.

  Status: T1 proven; T2 established to order of magnitude; T3 physically
  motivated, quantitative criterion to be formalised (item CORE-1).
""")

# =============================================================================
#  TEST 4 - Nucleation criterion QUANTIFIED (update 16/07/2026)
#  Closes limitation [L2] above for standard accretion regimes; identifies
#  the hypercritical regime as the only open boundary (item
#  CORE-1-HYPERACC, merged into the ab initio problem of T2/[L1]).
# =============================================================================
print(); print(SEP)
print("T4 - Nucleation criterion QUANTIFIED: t_dyn << t_acc (upd. 16/07/2026)")
print(SEP)
print("""
  t_dyn is set by the LEAST dense phase (pre-supernova iron core,
  rho_i ~ 1e9 kg/m^3), since t_dyn ~ 1/sqrt(G rho) decreases as rho^-1/2.
""")
rho_i = 1e9
t_dyn = 1.0 / np.sqrt(G * rho_i)
print(f"  t_dyn ~ 1/sqrt(G*rho_i) = {t_dyn:.2f} s   (rho_i = {rho_i:.0e} kg/m^3)")

M_sun_yr_to_kg_s = 1.989e30 / 3.156e7
regimes = [
    ("ISM / typical Bondi",           1e-9, M_sun_yr_to_kg_s),
    ("Eddington limit (eta=0.1)",     None, None),   # t_Edd handled separately
    ("Hyperaccretion (collapsar/GRB)", 1e-2, 1.0),   # Msun/s directly
]
t_Edd = 1.4e16  # s, Salpeter time, independent of M

print("\n  Regime                          | t_acc (s)   | t_dyn/t_acc")
print("  " + "-" * 66)
for label, val, unit in regimes:
    if label.startswith("Eddington"):
        t_acc = t_Edd
    elif label.startswith("ISM"):
        Mdot = val * M_sun_yr_to_kg_s
        t_acc = 10 * 1.989e30 / Mdot   # order of magnitude, M ~ 10 Msun
    else:
        Mdot_kg_s = val * 1.989e30
        t_acc = 10 * 1.989e30 / Mdot_kg_s
    ratio = t_dyn / t_acc
    print(f"  {label:32s} | {t_acc:9.2e}   | {ratio:9.2e}")

print(f"""
  => A margin of 15 to 17 orders of magnitude in the standard regime (ISM,
     Eddington): the criterion is closed quantitatively, not fine-tuned.
  => The HYPERCRITICAL regime (collapsar/GRB, Mdot ~ 1e-2 to 1 Msun/s,
     MacFadyen & Woosley 1999) is the ONLY regime where the criterion stops
     being trivially satisfied (ratio ~1e-2 to 1e-3).
     The right test there is the mass accreted per dynamical time, not the
     ratio of the times:""")
for Mdot_msun_s in [1e-2, 1.0]:
    Mdot_kg_s = Mdot_msun_s * 1.989e30
    delta_M = Mdot_kg_s * t_dyn
    delta_M_msun = delta_M / 1.989e30
    print(f"    Mdot={Mdot_msun_s:.0e} Msun/s : Delta_M(t_dyn) = {delta_M_msun:.3f} Msun"
          f"  (~{delta_M_msun/5*100:.0f}% of M_BH~5 Msun)")
print("""
  => Delta_M(t_dyn) reaches a few per cent to several tens of per cent of
     M_BH: NOT negligible, unlike the standard regime (~1e-16).
  => This case does NOT close on its own: it requires knowing how the core
     reacts dynamically to an inflow too fast for it to readjust -- exactly
     the ingredient missing from T2/[L1] (a complete TOV-torsion solution).
     CORE-1-HYPERACC is therefore MERGED into the ab initio problem, not
     solved separately (deferred to Foundation IV).

  UPDATED STATUS (item CORE-1, 16/07/2026):
    - Bound rho <= rho_c/2: PROVEN -- but NOT by T1 above.
      T1 gives the Friedmann bound rho <= rho_c (kinematic, exact). The
      factor of two comes from the TOV treatment in Foundation III
      Extended ("Resolution TOV", item CORE-1): rho_eff = rho(1-rho/rho_c)
      peaks at rho_c/2, and a bound core cannot sit above that peak. See
      the header of this file.
    - Equilibrium (T2): established to order of magnitude (rho vs rho^2).
    - Nucleation criterion (T3): QUANTIFIED for ISM/Eddington
      (margin of 15-17 orders of magnitude).
    - Hypercritical regime (CORE-1-HYPERACC): diagnosed via Delta_M(t_dyn),
      merged into the ab initio problem (T2/[L1]), not solved separately.
    - Complete ab initio derivation (T2/[L1]): DEFERRED to Foundation IV.
""")
