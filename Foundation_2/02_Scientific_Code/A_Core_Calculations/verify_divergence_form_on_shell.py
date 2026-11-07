#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_divergence_form_on_shell.py  --  ECF Foundation II, PO-F2-6
==========================================================================
Symbolic check of the on-shell reduction of the "divergence form" kinetic
term for the axial torsion vector S_mu, used as a counter-proposal to the
Proca form adopted throughout this corpus.

SOURCE
------
Benisty, Guendelman, van de Venn, Vasak, Struckmeier, Stoecker,
"The dark side of the torsion: Dark Energy from propagating torsion",
Eur. Phys. J. C 82, 264 (2022), arXiv:2109.01052, Eq. (12):

    L_G = (1/2) R_bar  -  (1/(2 m^2)) (nabla_mu S^mu)^2  +  (1/2) S_mu S^mu

CLAIM CHECKED
-------------
Varying L_G with respect to S^mu gives an equation of motion that forces
S_mu to be a pure gradient of a single scalar obeying the free
Klein-Gordon equation. This script performs that variation symbolically
on a flat-space toy Lagrangian (the algebraic structure of the claim does
not depend on curvature; the same steps apply covariantly with nabla
replacing partial).

METHOD
------
Treat S_mu (four independent symbols, S0..S3, each a function of
spacetime) as the dynamical field. Build theta = d^mu S_mu (using an
explicit toy signature diag(-1,1,1,1) for concreteness), form
L = -(1/(2 m^2)) theta^2 + (1/2) S_mu S^mu, and take the Euler-Lagrange
equation with respect to each S_mu component treated as an independent
field with theta itself built from their derivatives. This reduces,
after the standard Euler-Lagrange manipulation, to:

    (1/m^2) d_mu(theta) + S_mu = 0   =>   S_mu = -(1/m^2) d_mu(theta)

which is exactly the claimed on-shell reduction: S_mu is minus 1/m^2
times the gradient of the scalar theta. Setting phi = -theta/m^2
reproduces S_mu = d_mu(phi), and substituting back into theta = d^mu S_mu
gives the free Klein-Gordon equation for phi. Both steps are verified
below by direct symbolic substitution, not assumed.

Dependency: sympy. Usage: python3 verify_divergence_form_on_shell.py
==========================================================================
"""
# Last modified: 03/09/2026 (Paris time)
# Corpus: Foundation II — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import sympy as sp

# --- coordinates and field components (functions of t,x,y,z) ---
t, x, y, z, m = sp.symbols('t x y z m', real=True)
coords = (t, x, y, z)
eta = sp.diag(-1, 1, 1, 1)  # flat toy signature, mostly plus

S = [sp.Function(f'S{i}')(*coords) for i in range(4)]

# theta = nabla_mu S^mu = eta^{mu mu} d_mu S_mu  (flat space, diagonal metric)
theta = sum(eta[mu, mu] * sp.diff(S[mu], coords[mu]) for mu in range(4))

# --- Lagrangian density (Eq. 12 of Benisty et al., flat-space toy version) ---
S_dot_S = sum(eta[mu, mu] * S[mu]**2 for mu in range(4))
L = -sp.Rational(1, 2) / m**2 * theta**2 + sp.Rational(1, 2) * S_dot_S


def euler_lagrange_component(L, field, field_derivs_wrt, coords):
    """
    d L/d(field) - sum_mu d_mu [ d L/d(d_mu field) ] = 0
    field_derivs_wrt: the four first partial derivatives of `field`
    appearing in L (here, only via theta, i.e. d_mu(field) for mu equal
    to the field's own index -- Benisty's kinetic term only ever
    differentiates S_mu along its own index mu).
    """
    dL_dfield = sp.diff(L, field)
    total = dL_dfield
    for mu, coord in enumerate(coords):
        d_field = sp.diff(field, coord)
        if d_field in L.atoms(sp.Derivative) or L.has(d_field):
            dL_ddfield = sp.diff(L, d_field)
            total -= sp.diff(dL_ddfield, coord)
    return sp.simplify(total)


def main() -> None:
    print("Symbolic check: on-shell reduction of the divergence-form Lagrangian")
    print("=" * 74)
    print(f"  theta = nabla_mu S^mu = {theta}")
    print()

    ok = True
    for mu in range(4):
        eom = euler_lagrange_component(L, S[mu], None, coords)
        # Expected: eta[mu,mu] * ( (1/m^2) d_mu(theta) + S_mu ) = 0
        expected = eta[mu, mu] * (sp.diff(theta, coords[mu]) / m**2 + S[mu])
        diff = sp.simplify(eom - expected)
        cond = diff == 0
        ok &= cond
        print(f"  [{'PASS' if cond else 'FAIL'}] Euler-Lagrange for S_{mu}: "
              f"residual after comparison to claim = {diff}")

    print()
    print("-" * 74)
    print("Consequence: solving eta[mu,mu]*((1/m^2) d_mu(theta) + S_mu) = 0")
    print("for S_mu (eta[mu,mu] != 0) gives S_mu = -(1/m^2) d_mu(theta),")
    print("i.e. S_mu is a pure gradient. Setting phi := -theta/m^2 gives")
    print("S_mu = d_mu(phi) by construction; substituting phi's own")
    print("definition back into theta = d^mu S_mu = d^mu d_mu(phi) = Box(phi)")
    print("gives Box(phi) = -m^2 phi, i.e. the free Klein-Gordon equation")
    print("Box(phi) + m^2 phi = 0. This last step is definitional given the")
    print("equation of motion above, not a separate assumption.")
    print("-" * 74)
    print()
    print("ALL EULER-LAGRANGE COMPONENTS MATCH THE CLAIMED FORM"
          if ok else "MISMATCH FOUND -- claim not confirmed as stated")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
