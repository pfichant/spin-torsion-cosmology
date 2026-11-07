#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_nonminimal_coupling_flrw.py
==================================
Does the non-minimal torsion-curvature coupling survive on an FLRW background?

WHY THIS SCRIPT EXISTS
----------------------
Appendix J.3 of Foundation II identifies ONE remaining route to a dynamical
dark-energy sector:

    "a non-minimal torsion-curvature coupling (~ R^{mu nu} dS_mu dS_nu) arising
     from the cross terms of R~(g,T) breaks the conformal invariance of the
     Goldstone sector and reshapes the fluctuation spectrum; extracting it and
     settling the result quantitatively requires a dedicated Einstein-Cartan
     perturbation solver, not developed here."

The perturbation part is indeed out of reach here. But the BACKGROUND piece is
not, and it has never been computed in the corpus. It answers a sharp question:

    The Proca kinetic term vanishes identically on FLRW (F_{mu nu} = 0), which
    is exactly why the ECF condensate is static (w = -1). Does the non-minimal
    coupling vanish too -- or does it survive?

If it survives, it supplies precisely what is missing: a term that does NOT
vanish on the homogeneous background, and whose coefficient EVOLVES.

WHAT IS COMPUTED
----------------
  (1) The Ricci tensor of FLRW with spatial curvature k retained.
  (2) R^{mu nu} S_mu S_nu for the homogeneous axial ansatz S_mu = (s(t),0,0,0).
  (3) Whether the result vanishes, and if not, how its coefficient evolves.
  (4) The consequence for the vacuum expectation value and hence for w.

SCOPE -- stated up front
------------------------
This is the BACKGROUND piece only. Appendix J speaks of dS (fluctuations); the
fluctuation spectrum still requires the perturbation solver. What this can
settle is whether the mechanism is available at all on the homogeneous
background, which is a prerequisite for anything else.

Sign convention: signature (-,+,+,+); R^a_{bcd} = d_c Gamma^a_{bd} - ...
Dependency: sympy.  Usage: python3 verify_nonminimal_coupling_flrw.py
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi', real=True)
k = sp.Symbol('k', real=True)
a = sp.Function('a', positive=True)(t)
x = [t, r, th, ph]

g = sp.diag(-1,
            a**2 / (1 - k * r**2),
            a**2 * r**2,
            a**2 * r**2 * sp.sin(th)**2)
ginv = sp.simplify(g.inv())

print("=" * 74)
print("  Non-minimal coupling R^{mu nu} S_mu S_nu on FLRW  (k retained)")
print("=" * 74)

# ---------------------------------------------------------------------------
# (1) Christoffel, Riemann, Ricci
# ---------------------------------------------------------------------------
def christoffel(g, ginv, x):
    n = len(x)
    G = [[[0] * n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(m, n):
                e = 0
                for s_ in range(n):
                    e += ginv[l, s_] * (sp.diff(g[s_, m], x[nu])
                                        + sp.diff(g[s_, nu], x[m])
                                        - sp.diff(g[m, nu], x[s_]))
                e = sp.simplify(e / 2)
                G[l][m][nu] = e
                G[l][nu][m] = e
    return G

G = christoffel(g, ginv, x)

def ricci(G, x):
    n = len(x)
    R = sp.zeros(n, n)
    for m in range(n):
        for nu in range(m, n):
            e = 0
            for l in range(n):
                e += sp.diff(G[l][m][nu], x[l]) - sp.diff(G[l][m][l], x[nu])
                for s_ in range(n):
                    e += G[l][l][s_] * G[s_][m][nu] - G[l][nu][s_] * G[s_][m][l]
            e = sp.simplify(e)
            R[m, nu] = e
            R[nu, m] = e
    return R

Ric = ricci(G, x)
print("\n(1) Ricci tensor, component R_00:")
R00 = sp.simplify(Ric[0, 0])
print(f"    R_00 = {R00}")

# ---------------------------------------------------------------------------
# (2) Contract with the homogeneous axial ansatz
# ---------------------------------------------------------------------------
s = sp.Function('s')(t)
S_low = sp.Matrix([s, 0, 0, 0])                 # S_mu = (s(t), 0, 0, 0)

# R^{mu nu} S_mu S_nu  =  g^{mu p} g^{nu q} R_{pq} S_mu S_nu
val = 0
for m in range(4):
    for nu in range(4):
        if S_low[m] == 0 or S_low[nu] == 0:
            continue
        e = 0
        for pp in range(4):
            for q in range(4):
                e += ginv[m, pp] * ginv[nu, q] * Ric[pp, q]
        val += e * S_low[m] * S_low[nu]
val = sp.simplify(val)

print("\n(2) Contraction with the homogeneous ansatz")
print(f"    R^{{mu nu}} S_mu S_nu = {val}")

vanishes = sp.simplify(val) == 0
print()
if vanishes:
    print("    => VANISHES, like the Proca term. The route is closed at this order.")
else:
    print("    => DOES NOT VANISH. Unlike the Proca kinetic term, the non-minimal")
    print("       coupling SURVIVES on the homogeneous background.")

# ---------------------------------------------------------------------------
# (3) How does its coefficient evolve?
# ---------------------------------------------------------------------------
H = sp.Function('H')(t)
adot = sp.diff(a, t)
addot = sp.diff(a, t, 2)

coeff = sp.simplify(val / s**2) if not vanishes else sp.Integer(0)
print("\n(3) Coefficient multiplying s^2")
print(f"    R^{{00}} = {coeff}")

# rewrite in terms of H = adot/a and its derivative
coeff_H = sp.simplify(coeff.subs(addot, a * (sp.diff(H, t) + H**2))
                          .subs(adot, a * H))
print(f"    in terms of H:  {sp.simplify(coeff_H)}")
print("    i.e. proportional to  adot../a = Hdot + H^2  --  a TIME-DEPENDENT quantity,")
print("    not a constant.")

# ---------------------------------------------------------------------------
# (4) Consequence for the VEV and for w
# ---------------------------------------------------------------------------
print("\n(4) Consequence")
print("    Adding  xi * R^{mu nu} S_mu S_nu  to the Lagrangian shifts the")
print("    effective potential by a term  xi * R^{00} * s^2, i.e. an effective")
print("    mass-squared shifted by a quantity proportional to (Hdot + H^2).")
print()
print("    The VEV solves  W'(s0) + 2 xi R^{00} s0 = 0.  Because R^{00} EVOLVES,")
print("    the minimum MOVES: s0 = s0(t), and the condensate density is no")
print("    longer constant.  Hence w != -1.")
print()
print("    Compare:")
print("      Proca kinetic term  F_{mu nu} F^{mu nu} :  vanishes on FLRW  -> w = -1 exactly")
print("      non-minimal coupling R^{mu nu}S_mu S_nu :  survives, evolves   -> w != -1")

print("\n" + "=" * 74)
if not vanishes:
    print("  RESULT: the mechanism identified in Appendix J.3 is AVAILABLE already")
    print("  at the level of the homogeneous background -- it does not require the")
    print("  fluctuations to be switched on. The obstruction that makes the Proca")
    print("  sector static (F = 0 on FLRW) does NOT apply to the non-minimal term.")
else:
    print("  RESULT: the route is closed at background level.")
print("=" * 74)

print("\nWHAT THIS DOES NOT ESTABLISH:")
print("  * the VALUE of xi -- it is not derived here, and the corpus does not fix it;")
print("  * whether the resulting w(z) matches (w0, wa) = (-0.904, -0.153):")
print("    that needs the sign and magnitude of xi, hence the cross terms of R~(g,T);")
print("  * anything about ghosts or stability of the coupled sector;")
print("  * the FLUCTUATION spectrum, which is what Appendix J.3 actually asks for.")
print("  => This shows the door is not locked. It does not walk through it.")
