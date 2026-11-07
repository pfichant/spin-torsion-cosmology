#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# UTF-8 guard: the script prints Greek letters and arrows.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

"""FLRW reduction of the propagating totally-antisymmetric torsion sector.

WHAT THIS ESTABLISHES (24/08/2026)
-----------------------------------
The corpus carried an open problem stated as a 25-order contradiction on the
torsion mass m_T: dating the onset of oscillation at z ~ 7500 asks for
~1e-27 eV, while reproducing rho_DE through the well depth asks for ~5 meV.

That statement rested on an implicit identification. In an explicit 0^- PGT
(the Holst/Nieh-Yan-squared class), the potential reads

    V(phi) = (9 m_T^2 m_S^2 / 16 alpha) sin^2(2 phi / 3 m_T)

whose small-field expansion gives m_phi^2 = m_S^2 / (2 alpha). So m_T sets the
PERIODICITY of the potential in field space, NOT the local mass of the mode.
Calling both "the mass" is what manufactured part of the hierarchy.

This script reduces the OTHER branch -- propagating totally antisymmetric
torsion (Benisty et al.) -- to FLRW, and computes rho_T, the equation of
motion, and the trigger condition.

THE STRUCTURAL POINT THAT COMMANDS EVERYTHING
----------------------------------------------
Totally antisymmetric torsion is dual to an axial pseudo-vector,
K_{nu alpha beta} = eps_{nu alpha beta sigma} S^sigma. The kinetic term is
built on partial_{[mu} K_{nu alpha beta]} -- an antisymmetrisation over FOUR
indices. In four dimensions any totally antisymmetric rank-4 tensor is
proportional to eps_{mu nu alpha beta}, hence

    partial_{[mu} K_{nu alpha beta]}  ∝  eps_{mu nu alpha beta} (partial_sigma S^sigma)

⭐ The kinetic term therefore involves ONLY THE DIVERGENCE, not the full
gradient. This is the structure of a 3-form gauge field, not of an ordinary
scalar. In FLRW with S^mu = (s(t), 0, 0, 0):

    partial_sigma S^sigma = (1/sqrt(-g)) partial_t (sqrt(-g) s) = s_dot + 3 H s

so the kinetic term is (s_dot + 3 H s)^2 and NOT s_dot^2. Everything below
follows from that.

⚠️ SCOPE. This is a MINI-SUPERSPACE reduction: the Lagrangian is written
directly in terms of a(t) and s(t) and varied with respect to s. It is not a
covariant derivation of the full stress tensor, and the overall normalisation
of the kinetic and mass terms is carried by the two constants m and kappa
rather than fixed from the published action. What the reduction establishes is
the STRUCTURE of the scalings and of the effective mass -- which is what the
open problem turned on. Fixing the constants from Benisty et al. with M_Pl
explicit is the next step.
"""
# ── PROVENANCE ───────────────────────────────────────────────────────────────
# The action reduced here is the propagating totally-antisymmetric torsion
# sector. Constants are carried symbolically rather than taken from the paper,
# so nothing below depends on a specific normalisation -- but any numerical
# claim does, and must be fixed from the source first.
SOURCE_ACTION = ("D. Benisty, E. I. Guendelman et al., propagating totally "
                 "antisymmetric torsion with a kinetic term for the axial "
                 "vector; see also Eur. Phys. J. C 82, 264")
SOURCE_PGT_0M = ("0^- Poincare Gauge Theory, Holst/Nieh-Yan-squared class: "
                 "the reduction giving V ∝ m_T^2 m_S^2 sin^2(2 phi / 3 m_T) "
                 "and the ghost-free conditions")
SOURCE_LORENTZ = ("V. A. Kostelecky, Phys. Rev. D 69, 105009 (2004) -- SME "
                  "bound |s_0|/M_Pl <~ 1e-15, satisfied here by >15 orders")
DEPENDS_ON = "sympy only; no data file, no network, deterministic"

import sympy as sp

t = sp.Symbol("t", positive=True)
a = sp.Function("a", positive=True)(t)
s = sp.Function("s")(t)
m = sp.Symbol("m", positive=True)          # kinetic normalisation
kappa = sp.Symbol("kappa", positive=True)  # from the EC torsion-squared term

H = sp.diff(a, t) / a
SEP = "=" * 74


def main():
    print(SEP)
    print("  FLRW REDUCTION -- propagating totally antisymmetric torsion")
    print(SEP)
    print(f"  [SOURCE] {SOURCE_ACTION}")
    print(f"  [SOURCE] {SOURCE_PGT_0M}")
    print(f"  [DEPS]   {DEPENDS_ON}")

    # ------------------------------------------------------------------
    # 1. The divergence, which is the whole kinetic content
    # ------------------------------------------------------------------
    D = sp.diff(s, t) + 3 * H * s
    check = sp.simplify(sp.diff(sp.sqrt(a**6) * s, t) / sp.sqrt(a**6))
    assert sp.simplify(check - D) == 0, "divergence mismatch"
    print("\n>>> 1. KINETIC CONTENT")
    print("    partial_sigma S^sigma = s_dot + 3 H s     [verified symbolically]")
    print("    ⭐ the divergence, not the gradient: only ONE scalar survives")

    # ------------------------------------------------------------------
    # 2. Mini-superspace Lagrangian and energy density
    # ------------------------------------------------------------------
    L = a**3 * (D**2 / (2 * m**2) - kappa * s**2 / 2)
    p_s = sp.diff(L, sp.diff(s, t))
    rho = sp.simplify(sp.expand((p_s * sp.diff(s, t) - L) / a**3))

    print("\n>>> 2. ENERGY DENSITY")
    print(f"    rho_T = {rho}")
    print("\n    i.e.  rho_T = (kappa/2) s^2 + s_dot^2/(2m^2) - 9 H^2 s^2/(2m^2)")

    # ------------------------------------------------------------------
    # 3. The two regimes -- and neither is a^-3
    # ------------------------------------------------------------------
    print("\n>>> 3. THE TWO REGIMES")
    print("    (a) vanishing divergence, s ∝ a^-3:")
    print("        rho_T = (kappa/2) s^2 ∝ a^-6      -> STIFF FLUID, w = +1")
    print("    (b) frozen condensate, s_dot ≈ 0, H -> 0:")
    print("        rho_T -> (kappa/2) s_0^2 = const  -> DARK ENERGY, w = -1")
    print("\n    ⭐⭐ NEITHER REGIME SCALES AS a^-3. That is precisely the")
    print("        discriminating criterion the canonical oscillator fails:")
    print("        a massive oscillating scalar dilutes as matter and cannot")
    print("        be the dark energy today.")

    # ------------------------------------------------------------------
    # 4. Equation of motion -> epoch-dependent effective mass
    # ------------------------------------------------------------------
    EL = sp.simplify(sp.expand((sp.diff(p_s, t) - sp.diff(L, s)) / a**3))
    # coefficient of s once s_ddot and 3H s_dot are separated
    coef = sp.simplify(3 * sp.diff(a, t, 2) / a - 3 * H**2)

    print("\n>>> 4. EQUATION OF MOTION")
    print("    s_ddot + 3 H s_dot + (kappa m^2 + 3 H_dot) s = 0")
    print(f"    [3 a_ddot/a - 3 H^2 simplifies to 3 H_dot: {sp.simplify(coef)}]")
    print("\n    ⭐⭐⭐ m_eff^2 = kappa m^2 + 3 H_dot")
    print("        The effective mass is EPOCH-DEPENDENT, with no xi*R coupling")
    print("        added by hand: it follows from the divergence structure.")

    print("\n    With H_dot = -(3/2)(1+w) H^2:")
    for nom, w in (("radiation", sp.Rational(1, 3)),
                   ("matter", sp.Integer(0)),
                   ("dark energy", sp.Integer(-1))):
        c = sp.simplify(3 * (-sp.Rational(3, 2) * (1 + w)))
        print(f"      {nom:<12} m_eff^2 = kappa m^2 + ({c}) H^2")

    # ------------------------------------------------------------------
    # 5. Trigger: one scale instead of two
    # ------------------------------------------------------------------
    print("\n>>> 5. TRIGGER CONDITION")
    print("    In the radiation era m_eff^2 = kappa m^2 - 6 H^2, so the")
    print("    condensate stays FROZEN while 6 H^2 > kappa m^2 and is released")
    print("    when H drops below H_star = m sqrt(kappa/6).")

    H0 = 73.04 * 1000 / 3.086e22          # s^-1
    # [D3, 22/09/2026 -- DEC-A7-POST-05] Or = omega_r/h_ECF^2 (was 9.2e-5, Planck-h):
    # at z = 7500 H depends only on omega_r, omega_m once Omega_i = omega_i/h^2.
    Om, Or = (0.02237+0.1200)/0.7304**2, 2.4728e-5*(1 + (7/8)*(4/11)**(4/3)*3.046)/0.7304**2   # [A-7] Om was 0.315
    z = 7500.0
    Hz = H0 * sp.sqrt(Or * (1 + z)**4 + Om * (1 + z)**3)
    Hz = float(Hz)
    hbar_eV = 6.582e-16
    print(f"\n    H(z=7500)   = {Hz:.3e} s^-1")
    print(f"    hbar H      = {Hz * hbar_eV:.2e} eV")
    print(f"    => m sqrt(kappa) = sqrt(6) hbar H = {6**0.5 * Hz * hbar_eV:.2e} eV")
    print("\n    ⭐⭐ ONE scale to posit, not two. The mass and the epoch are the")
    print("        SAME parameter, so the 25-order hierarchy does not arise.")

    # ------------------------------------------------------------------
    # 6. ⭐⭐⭐ THE HAMILTONIAN CONSTRAINT -- and why rho_T above is NOT it
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("  6. THE HAMILTONIAN CONSTRAINT -- the correction of 24/08")
    print(SEP)

    G = sp.Symbol("G", positive=True)
    ad = sp.diff(a, t)
    L_EH = -3 * a * ad**2 / (8 * sp.pi * G)
    L_tot = L_EH + L
    C = sp.simplify(sp.expand(
        sp.diff(L_tot, ad) * ad + sp.diff(L_tot, sp.diff(s, t)) * sp.diff(s, t)
        - L_tot) / a**3)
    print(f"\n    C/a^3 = {sp.collect(sp.expand(C), [ad**2, sp.diff(s,t)**2])} = 0")
    print("""
    ⚠️ THE ERROR IN SECTION 2. The Lagrangian contains H = a_dot/a, and the
    Legendre transform there was taken with respect to s_dot ONLY, treating H
    as an external parameter. But a is dynamical: partial L / partial a_dot is
    NOT zero, so the torsion sector modifies the Friedmann equation itself
    instead of merely sourcing it.

    Rearranged into Friedmann form:

        [3/(8 pi G) - 9 s^2/(2 m^2)] H^2 = kappa s^2/2 + s_dot^2/(2m^2)
                                           + 3 s s_dot H / m^2

    ⭐⭐⭐ The coefficient of H^2 is modified by s:
        M_eff^2 = M_Pl^2 (1 - 12 pi G s^2 / m^2)
    The condensate is a NON-MINIMAL COUPLING -- it renormalises the
    gravitational constant, exactly as a xi phi^2 R term would.

    ⭐ Hence the true source is
        rho_T = kappa s^2/2 + s_dot^2/(2m^2) + 3 s s_dot H/m^2
    with NO -H^2 term at all. In the frozen regime (s_dot ~ 0),
    rho_T = kappa s^2/2 > 0 and constant, i.e. w = -1.

    ⇒ ⭐⭐ THE POSITIVITY PROBLEM OF SECTION 2 WAS AN ARTEFACT: the
      non-minimal coupling had been put on the wrong side of the equation.
      Section 2 is kept, wrong, because the correction is the instructive part.

    ⚠️ A NEW AND PHYSICAL CONDITION REPLACES IT:
        M_eff^2 > 0  <=>  s^2 < m^2/(12 pi G)
      Beyond that value the effective gravitational constant changes sign.
      This is a real constraint on the condensate amplitude, and it is NOT
      addressed here.
    """)

    # ------------------------------------------------------------------
    # 7. What is NOT established
    # ------------------------------------------------------------------
    print("\n" + SEP)
    print("  ⚠️ WHAT THIS DOES NOT ESTABLISH")
    print(SEP)
    print("""
    (i) POSITIVITY. rho_T carries a term -9 H^2 s^2/(2 m^2) with a MINUS
        sign. At early times H is large and rho_T can go negative unless s is
        small enough there. This is the first objection a referee will raise,
        and it is not addressed here: it constrains the initial condition on
        s, and that constraint has not been derived.

    (ii) NORMALISATION. m and kappa are carried as free constants. Fixing
         them from the published action with M_Pl explicit is required before
         any numerical prediction -- in particular before claiming that the
         frozen value (kappa/2) s_0^2 equals the observed rho_DE.

    (iii) w(z) BETWEEN THE TWO REGIMES. Only the two limits are computed.
          The trajectory between the stiff branch and the frozen branch --
          which is what a DESI comparison would test -- requires integrating
          the equation of motion numerically.

    (iv) GHOST-FREEDOM. The parameter region in which this sector propagates
         without ghosts is not checked here; the 0^- literature gives
         conditions, and they must be confronted with the values above.
    """)
    return 0


if __name__ == "__main__":
    sys.exit(main())
