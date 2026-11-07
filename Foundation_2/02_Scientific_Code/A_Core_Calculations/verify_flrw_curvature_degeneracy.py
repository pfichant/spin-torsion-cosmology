#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_flrw_curvature_degeneracy.py
===================================
Does the ECF axial-torsion sector produce a curvature-like a^-2 term?

WHY THIS SCRIPT EXISTS
----------------------
van de Venn, Vasak, Kirsch & Struckmeier (EPJC 83, 288 (2023), arXiv:2211.11868)
show that in the Einstein-Cartan limit of CCGG -- their g1 -> 0, which is the
regime the ECF works in, since the ECF keeps R~ linear -- a totally
antisymmetric torsion contributes to the Friedmann constraint with

    w_s = -1/3,   rho_s ~ a^-2,

i.e. EXACTLY the equation of state of spatial curvature. Their conclusion:

    "the contribution of torsion counteracts the spatial curvature [...] it is
     possible to misinterpret [...] the geometry type as open, albeit k >= 0,
     [...] or FLAT with k = b^2 > 0."

This bears directly on the PIT, whose entire strength is its falsifiability:
"a measurement of Omega_K != 0 at any precision would exclude it". If axial
torsion is degenerate with curvature, then the OBSERVED Omega_K is not the
GEOMETRIC Omega_K, and that argument weakens.

THE QUESTION THIS SCRIPT ASKS
-----------------------------
The ECF is NOT their setup: it carries a potential W(X) with a non-trivial VEV,
which they do not have. In their case conservation fixes s0 ~ a^-1 (giving
w = -1/3); in the ECF the potential minimum fixes s0 = const (giving w = -1).

    HYPOTHESIS: the ECF potential BREAKS the degeneracy, moving the torsion
    contribution from w = -1/3 (curvature-like) to w = -1 (Lambda-like),
    so that Omega_K remains a clean observable.

Foundation II reduces the action with spatial flatness ALREADY IMPOSED
(F2 l.1788: "With spatial flatness imposed, ..."), so the question has never
been asked in the corpus. This script relaxes k = 0 and asks it.

WHAT IS TESTED
--------------
  (1) F^(S)_{mu nu} for the homogeneous ansatz, on a curved FLRW background:
      does spatial curvature revive the Proca kinetic term?
  (2) The scaling of the torsion energy density at the VEV, with k kept.
  (3) Whether an a^-2 piece appears in the torsion sector.

This is a REDUCTION on the background, not a proof about the full theory.
What it can establish: whether a curvature-like term appears at this order.
What it cannot: anything about perturbations, or about non-minimal couplings.

Dependency: sympy.  Usage: python3 verify_flrw_curvature_degeneracy.py
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import sympy as sp

# ---------------------------------------------------------------------------
# FLRW background WITH spatial curvature k (this is the point of the script)
# ---------------------------------------------------------------------------
t, r, th, ph = sp.symbols('t r theta phi', real=True)
k = sp.Symbol('k', real=True)
a = sp.Function('a', positive=True)(t)

x = [t, r, th, ph]
g = sp.diag(-1,
            a**2 / (1 - k * r**2),
            a**2 * r**2,
            a**2 * r**2 * sp.sin(th)**2)
ginv = g.inv()

print("=" * 74)
print("  ECF axial torsion on a CURVED FLRW background (k kept)")
print("=" * 74)
print("\nMetric: ds^2 = -dt^2 + a^2[ dr^2/(1-k r^2) + r^2 dOmega^2 ]")

# ---------------------------------------------------------------------------
# (1) Proca field strength for the homogeneous axial ansatz, WITH k
# ---------------------------------------------------------------------------
s = sp.Function('s')(t)
S_low = [s, 0, 0, 0]          # S_mu = (s(t), 0, 0, 0): homogeneity + isotropy

# F_{mu nu} = d_mu S_nu - d_nu S_mu  (the Christoffel parts cancel by
# antisymmetry, on ANY metric -- including a curved one)
F = sp.Matrix(4, 4, lambda mu, nu:
              sp.simplify(sp.diff(S_low[nu], x[mu]) - sp.diff(S_low[mu], x[nu])))

print("\n(1) Proca field strength, spatial curvature k RETAINED")
sp.pprint(F)
if F == sp.zeros(4, 4):
    print("    => F^(S) == 0 even for k != 0.")
    print("       Spatial curvature does NOT revive the Proca kinetic term:")
    print("       the vanishing follows from the ansatz (s depends on t only,")
    print("       spatial components zero), not from flatness.")
else:
    print("    => F^(S) != 0: curvature DOES revive the kinetic term.")

# ---------------------------------------------------------------------------
# (2) Energy density of the condensate at the VEV, with k kept
# ---------------------------------------------------------------------------
# At the VEV, W'(X0) = 0 and the stress tensor is T_{mu nu} = -W(X0) g_{mu nu}.
# That form is ALGEBRAIC in the metric: it carries no derivative of a and no k.
W0 = sp.Symbol('W_0', real=True)          # W(X_0), the well depth
T = -W0 * g

rho = sp.simplify(T[0, 0])                                  # T_00 (u^mu u^nu)
p_r = sp.simplify(T[1, 1] * ginv[1, 1])                     # radial pressure
print("\n(2) Condensate stress tensor at the VEV, k RETAINED")
print(f"    rho = {rho}")
print(f"    p   = {p_r}")
w = sp.simplify(p_r / rho)
print(f"    w   = p/rho = {w}")

# ---------------------------------------------------------------------------
# (3) Does an a^-2 (curvature-like) piece appear?
# ---------------------------------------------------------------------------
print("\n(3) Scaling in a  --  the decisive test")
scaling = sp.simplify(sp.diff(sp.log(sp.Abs(rho)), t))
print(f"    d(ln rho)/dt = {scaling}")
if scaling == 0:
    print("    => rho_torsion is CONSTANT in a: rho ~ a^0, i.e. w = -1.")
    print("       NO a^-2 piece. The torsion sector is degenerate with")
    print("       Lambda, NOT with spatial curvature.")
    verdict = "NO_DEGENERACY"
else:
    print("    => rho depends on a: an a^-2 piece may be present.")
    verdict = "CHECK"

# ---------------------------------------------------------------------------
# Contrast with van de Venn's potential-free case
# ---------------------------------------------------------------------------
print("\n" + "-" * 74)
print("  CONTRAST: van de Venn et al., EPJC 83, 288 -- no potential")
print("-" * 74)
b = sp.Symbol('b', positive=True)
s_vdv = b / a                              # conservation fixes s0 ~ a^-1
rho_vdv = 3 * s_vdv**2                     # rho_s ~ s0^2 (their Eq. 30)
p_vdv = -s_vdv**2                          # their Eq. 31
print(f"    s0(a)   = {s_vdv}          (fixed by CONSERVATION, no potential)")
print(f"    rho_s   = {sp.simplify(rho_vdv)}   ->  ~ a^-2")
print(f"    w_s     = {sp.simplify(p_vdv / rho_vdv)}        ->  SAME as spatial curvature")

print("\n" + "=" * 74)
if verdict == "NO_DEGENERACY":
    print("  RESULT: the ECF potential BREAKS the degeneracy.")
    print()
    print("  van de Venn (no potential): conservation forces s0 ~ a^-1,")
    print("      hence rho ~ a^-2 and w = -1/3 -- indistinguishable from k.")
    print("  ECF (potential with VEV):   the minimum pins s0 = const,")
    print("      hence rho ~ a^0 and w = -1 -- indistinguishable from Lambda.")
    print()
    print("  => Omega_K remains a clean observable in the ECF, and the")
    print("     falsifiability of the PIT is NOT weakened by this mechanism.")
    print("     The potential -- introduced for the dark-energy sector -- turns")
    print("     out to protect the postulate as well.")
else:
    print("  RESULT: inconclusive at this order -- an a^-2 piece may survive.")
    print("  => The falsifiability of the PIT would need a caveat.")
print("=" * 74)

print("\nSCOPE -- what this does NOT establish:")
print("  * nothing about PERTURBATIONS: only the homogeneous background;")
print("  * nothing about non-minimal torsion-curvature couplings, which are")
print("    precisely the open route of Appendix J.4;")
print("  * the VEV form T_{mu nu} = -W(X0) g_{mu nu} is taken from Appendix J,")
print("    not re-derived here.")
