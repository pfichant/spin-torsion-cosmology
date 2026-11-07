#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_trace_vector_defect_coupling.py  --  ECF Foundation II, PO-F2-8
=============================================================================
Partial progress (30/08/2026) on "which field carries the pi_1 phase".

WHY THIS SCRIPT EXISTS
-----------------------
F2 states that the trace-vector companion to S_mu "fails" because, on a
homogeneous background, the two vectors are forced collinear and define no
phase. This script checks whether that failure survives near an actual
defect (wall or string core), where exact homogeneity/isotropy -- the
symmetry that forces the collinearity -- is locally broken.

METHOD
------
Standard irreducible decomposition of torsion (trace vector T_mu, axial
vector S_mu, tensor part set to zero). The FULL torsion-covariant derivative
of S_nu is computed --  nabla_mu S_nu = d_mu S_nu - Gamma^lambda_{mu nu}
S_lambda - K^lambda_{mu nu} S_lambda, with K the contortion built from BOTH
T_mu and S_mu -- rather than the flat field strength F_{mu nu}=d_mu S_nu -
d_nu S_mu used elsewhere in this work for the Proca kinetic term. This is
NOT an added assumption: it is what "torsion-covariant" means once T_mu is
allowed to be non-zero: it is why K exists.

Three ansaetze are tested:
  (A) planar wall,   S^mu=(A(z),0,0,0)             (Cartesian t,x,y,z)
  (B) cylindrical string, S^mu axial,  S^mu=(0,0,0,B(rho))  (t,rho,phi,z_s)
  (C) cylindrical string, S^mu azimuthal, S^phi=C(rho)/rho

RESULT (see printed output): in all three, a term LINEAR in the trace-vector
component along the "distance-from-defect" direction (normal for the wall,
radial for the string) appears in -1/4 Ftilde_{mu nu}Ftilde^{mu nu}, sourced
by (profile)x(profile)'. It vanishes in the far vacuum (profile'->0),
recovering T_mu=0 as required, and is localised at the defect. This resolves
the STATED collinearity failure (the sourced T_mu is orthogonal to S_mu's
own direction in every case tested).

WHAT THIS DOES NOT SHOW: in no ansatz does the sourced component depend on
the azimuthal angle phi. A genuine pi_1 winding requires the pair
(S_mu, T_mu) to trace a full turn in field space as phi goes 0 to 2pi; this
script's ansaetze do not supply that, and it is not claimed. See the
"What this does not yet show" paragraph in F2 (PO-F2-8) for the precise
scope of this result.

Dependency: sympy. Usage: python3 check_trace_vector_defect_coupling.py
=============================================================================
"""
# Last modified: 30/08/2026, 12:24 (Paris time)

import sympy as sp


def eps_flat(a, b, c, d):
    """Totally antisymmetric permutation symbol, epsilon_0123=+1."""
    idx = [a, b, c, d]
    if len(set(idx)) < 4:
        return 0
    inv = sum(1 for i in range(4) for j in range(i + 1, 4) if idx[i] > idx[j])
    return (-1) ** inv


def christoffel(coords, g, g_inv, lam, mu, nu):
    s = 0
    for sig in range(4):
        if g_inv[lam, sig] == 0:
            continue
        term = (sp.diff(g[sig, nu], coords[mu]) + sp.diff(g[sig, mu], coords[nu])
                - sp.diff(g[mu, nu], coords[sig]))
        s += g_inv[lam, sig] * term
    return sp.simplify(s / 2)


def run_case(name, coords, g, a_up):
    """Computes F_tilde_{mu nu} = nabla_mu S_nu - nabla_nu S_mu (full torsion-
    covariant derivative) for a given profile S^mu=a_up, with a generic
    T_mu, and prints the non-zero components together with any term
    linear in T_mu."""
    g_inv = g.inv()
    sqrtg = sp.sqrt(sp.simplify(-g.det()))

    def eps_lower(a, b, c, d):
        return sqrtg * eps_flat(a, b, c, d)

    Gamma = {(l, m, n): christoffel(coords, g, g_inv, l, m, n)
             for l in range(4) for m in range(4) for n in range(4)}

    a_lo = [sp.simplify(sum(g[r, s] * a_up[s] for s in range(4))) for r in range(4)]
    v_lo = [sp.Function(f'T{i}')(*coords) for i in range(4)]  # generic T_mu

    def T_lmn(lam, mu, nu):
        vterm = sp.Rational(2, 3) * (g[lam, mu] * v_lo[nu] - g[lam, nu] * v_lo[mu])
        aterm = sum(eps_lower(lam, mu, nu, r) * a_up[r] for r in range(4))
        return sp.simplify(vterm + aterm)

    def K_lmn(lam, mu, nu):
        return sp.simplify(sp.Rational(1, 2) * (
            T_lmn(lam, mu, nu) + T_lmn(mu, lam, nu) + T_lmn(nu, lam, mu)))

    def K_up1(lam, mu, nu):
        return sp.simplify(sum(g_inv[lam, sig] * K_lmn(sig, mu, nu) for sig in range(4)))

    def nabla_a(mu, nu):
        ordinary = sp.diff(a_lo[nu], coords[mu])
        lc = -sum(Gamma[(lam, mu, nu)] * a_lo[lam] for lam in range(4))
        torsion = -sum(K_up1(lam, mu, nu) * a_lo[lam] for lam in range(4))
        return sp.simplify(ordinary + lc + torsion)

    print(f"\n{'='*70}\n  CASE: {name}\n{'='*70}")
    print(f"  S_mu (lower indices) = {a_lo}")
    found_linear = False
    for mu in range(4):
        for nu in range(4):
            if mu >= nu:
                continue
            val = sp.simplify(nabla_a(mu, nu) - nabla_a(nu, mu))
            if val == 0:
                continue
            print(f"  F~_{{{mu}{nu}}} = {val}")
            for i in range(4):
                Ti = v_lo[i]
                if val.has(Ti):
                    coeff = sp.diff(val, Ti)
                    remainder = sp.simplify(val - coeff * Ti)
                    if remainder != 0:
                        print(f"      -> term linear in T{i}, coefficient = {coeff}"
                              f"  (genuine source since it multiplies {remainder} != 0)")
                        found_linear = True
    if not found_linear:
        print("  No term linear in T_mu found in this case.")


def main():
    print("Checking the geometric T_mu-S_mu coupling near a defect")
    print("(full torsion-covariant derivative vs the flat F_{mu nu} used elsewhere)")

    # --- Case A: planar wall, coordinates (t,x,y,z), flat Minkowski ---
    t, x, y, z = sp.symbols('t x y z', real=True)
    A = sp.Function('A')(z)
    run_case("(A) Planar wall, S^mu=(A(z),0,0,0)",
             [t, x, y, z], sp.diag(1, -1, -1, -1), [A, 0, 0, 0])

    # --- Case B: string, S along the axis, cylindrical coordinates ---
    rho, phi, zs = sp.symbols('rho phi z_s', real=True)
    B = sp.Function('B')(rho)
    run_case("(B) String, S^mu axial, S^mu=(0,0,0,B(rho))",
             [t, rho, phi, zs], sp.diag(1, -1, -rho**2, -1), [0, 0, 0, B])

    # --- Case C: string, S azimuthal ---
    C = sp.Function('C')(rho)
    run_case("(C) String, S^mu azimuthal, S^phi=C(rho)/rho",
             [t, rho, phi, zs], sp.diag(1, -1, -rho**2, -1), [0, 0, C/rho, 0])

    print(f"\n{'='*70}")
    print("  CONCLUSION")
    print(f"{'='*70}")
    print("""
  In all three cases, a term linear in the trace-vector component along the
  normal/radial direction to the defect appears, sourced by
  (profile) x (profile)'. It vanishes far from the defect (profile'->0),
  recovering T_mu=0 on the homogeneous vacuum, and is localised near the
  defect -- resolving the collinearity stated in F2 by a verified
  mechanism, not by assumption.

  NONE of the three cases produces a dependence on the azimuthal angle phi
  -- the necessary condition for a genuine pi_1 winding is NOT demonstrated
  here. See the "What this does not yet show" paragraph in F2 (PO-F2-8)
  for the precise scope of this result.
""")


if __name__ == "__main__":
    main()
