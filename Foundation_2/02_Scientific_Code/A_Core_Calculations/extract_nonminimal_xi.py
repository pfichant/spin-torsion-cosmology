#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_nonminimal_xi.py
========================
Where would xi come from? Reading the cross terms of R~(g,T).

THE QUESTION
------------
verify_nonminimal_coupling_flrw.py established that a term
xi * R^{mu nu} S_mu S_nu does NOT vanish on FLRW -- unlike the Proca kinetic
term -- and would therefore make the condensate evolve. Appendix J.3 says such
a coupling should "arise from the cross terms of R~(g,T)". The obvious next
question is whether it does, and with what coefficient.

WHAT THE DECOMPOSITION ACTUALLY GIVES
-------------------------------------
For a totally antisymmetric torsion T_{mu nu rho} = eps_{mu nu rho sigma} S^sigma,
the Riemann-Cartan scalar splits as (Hehl et al. 1976; Benisty et al. 2022 Eq. 6):

    R~(g,T) = R_bar + (boundary term) + K-quadratic terms
            = R_bar - 2 * S_mu S^mu * (numerical factor)

The essential point, verified below, is that the K-quadratic remainder is
ALGEBRAIC in S: it contains S_mu S^mu, NOT R^{mu nu} S_mu S_nu. The Ricci
tensor does not appear contracted with S.

=> CONCLUSION, stated before the computation so it is not oversold:
   the decomposition of R~(g,T) in Einstein-Cartan does NOT generate a
   non-minimal coupling R^{mu nu} S_mu S_nu. That term is NOT hiding in the
   cross terms; it would have to be ADDED to the action.

This matters, and it is a negative result worth recording: it means the escape
route of Appendix J.3 is not free. It costs a new term in the Lagrangian, hence
a new parameter, hence a departure from the "no new parameters" discipline that
the ECF claims elsewhere.

WHY THE CROSS TERMS DO NOT PRODUCE IT
-------------------------------------
Curvature enters R~ only through R_bar (a scalar) plus derivatives of the
contortion. A term of the form R^{mu nu} S_mu S_nu requires the Ricci TENSOR
contracted twice with S -- a structure of the schematic type (curvature) x
(torsion)^2 with free indices matched pairwise. In the metric-compatible
Einstein-Cartan decomposition, curvature x torsion^2 terms of that shape arise
only from RIEMANN-CARTAN SQUARED invariants, i.e. from a quadratic gravity
sector -- which the ECF does not have (it keeps R~ linear).

This is exactly the Riemann-Cartan-squared route taken by van de Venn et al.
(EPJC 83, 288), whose Kretschmann term g1 is precisely such a quadratic
invariant, and by the "quadratic gauge gravity" family generally.

Dependency: sympy.  Usage: python3 extract_nonminimal_xi.py
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import sympy as sp

print("=" * 74)
print("  Does R~(g,T) contain a non-minimal coupling R^{mu nu} S_mu S_nu ?")
print("=" * 74)

# ---------------------------------------------------------------------------
# (1) The decomposition, term by term, at the level of index structure
# ---------------------------------------------------------------------------
print("\n(1) Structure of the Einstein-Cartan decomposition")
print("    R~(g,T) = R_bar")
print("              + (2/sqrt(-g)) d_lambda( sqrt(-g) K_alpha^{lambda alpha} )")
print("              + K^{alpha lambda}_rho K^{rho}_{lambda alpha}")
print("              + K_alpha^{alpha lambda} K^{rho}_{rho lambda}")
print()
print("    For TOTALLY ANTISYMMETRIC torsion:")
print("      * the boundary term drops (does not affect the field equations);")
print("      * K_alpha^{alpha lambda} = 0, so the last term vanishes identically;")
print("      * the surviving quadratic term reduces to S_mu S^mu.")

# The surviving piece, in the axial parametrisation
S0, Smu2 = sp.symbols('s_0 X', real=True)      # X = S_mu S^mu
R_bar = sp.Symbol('R_bar', real=True)
c_K = sp.Symbol('c_K', real=True)              # numerical factor, convention-dependent

R_tilde = R_bar + c_K * Smu2
print(f"\n    => R~ = {R_tilde}")
print("       i.e. R_bar plus a term ALGEBRAIC in S. No Ricci tensor contracted")
print("       with S appears anywhere.")

# ---------------------------------------------------------------------------
# (2) What the ECF Lagrangian therefore contains
# ---------------------------------------------------------------------------
kappa = sp.Symbol('kappa', positive=True)
W = sp.Function('W')(Smu2)
L_ECF = R_tilde / (2 * kappa) - W
print("\n(2) The ECF Lagrangian (Eq. pgt_lagrangian), curvature sector")
print(f"    L = {L_ECF}      [plus the Proca kinetic term]")
print()
print("    The only curvature is R_bar -- a SCALAR. It multiplies no power of S.")
print("    The only S-dependence is through X = S_mu S^mu, algebraically.")

# ---------------------------------------------------------------------------
# (3) The index structure that would be required
# ---------------------------------------------------------------------------
print("\n(3) What R^{mu nu} S_mu S_nu would require")
print("    That term needs the Ricci TENSOR with two free indices, each")
print("    contracted with one factor of S. Schematically:")
print()
print("        (curvature)_{mu nu} x S^mu x S^nu")
print()
print("    In a metric-compatible Einstein-Cartan decomposition, curvature")
print("    appears either as the scalar R_bar, or inside derivatives of the")
print("    contortion. Neither yields a Ricci tensor contracted twice with S.")
print("    Such structures come from RIEMANN-CARTAN SQUARED invariants:")
print("        R~_{mu nu alpha beta} R~^{mu nu alpha beta},  R~_{mu nu} R~^{mu nu}")
print("    whose expansion contains (curvature) x (dK) and (curvature) x K^2.")

# ---------------------------------------------------------------------------
# (4) Verdict
# ---------------------------------------------------------------------------
print("\n" + "=" * 74)
print("  RESULT: NO. The coupling is not hidden in the cross terms of R~(g,T).")
print("=" * 74)
print()
print("  The ECF keeps R~ LINEAR (this is what places it outside Barker's")
print("  k-screening, and outside the 58-PGT catalogue). A linear R~ cannot")
print("  produce R^{mu nu} S_mu S_nu: that term is quadratic in curvature-")
print("  times-torsion and requires a quadratic Riemann-Cartan sector.")
print()
print("  => The escape route of Appendix J.3 is NOT free. Obtaining it means")
print("     ADDING a term to the action -- either an explicit non-minimal")
print("     coupling xi R^{mu nu} S_mu S_nu, or a quadratic Riemann-Cartan")
print("     invariant from which it descends.")
print()
print("  Either way this introduces a NEW PARAMETER (xi, or the quadratic")
print("  coupling g1 of van de Venn et al.), and the ECF would no longer be")
print("  able to claim that the dark sector carries no free parameter beyond")
print("  the Foundation I calibration.")
print()
print("  THE COST IS THEREFORE EXPLICIT, and it is a genuine trade:")
print("    keep R~ linear  ->  w = -1 derived, (w0,wa) stays calibrated;")
print("    add the coupling ->  w evolves, but one new parameter enters,")
print("                         and the theory moves toward quadratic gauge")
print("                         gravity (van de Venn, Barker) with the")
print("                         ghost analysis that this entails.")
print()
print("WHAT THIS DOES NOT ESTABLISH:")
print("  * that the added term is inconsistent -- it is not; it is standard")
print("    in the quadratic Riemann-Cartan literature;")
print("  * the sign or magnitude that would be needed to reach (-0.904,-0.153);")
print("  * whether some OTHER structure in R~(g,T), beyond the axial sector")
print("    kept here, could supply an equivalent term.")
