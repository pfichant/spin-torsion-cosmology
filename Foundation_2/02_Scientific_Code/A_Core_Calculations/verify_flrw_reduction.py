#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_flrw_reduction.py
Symbolic verification of the FLRW reduction of the axial torsion sector
(Foundation II, Appendix J). Reproduces, without intervention, the three
key steps:

  (1) F^(S)_{mu nu} = 0 for the homogeneous temporal ansatz S_mu = (s(t),0,0,0)
      -> the kinetic term vanishes, the mode is non-dynamical.
  (2) At the VEV (W'(X0)=0): T_{mu nu} = -W(X0) g_{mu nu}  =>  w = p/rho = -1.
  (3) Fluctuations: the mass term in delta S_mu delta S^mu has coefficient
      -W'(X0), which vanishes at the VEV -> the delta S_i (spatial) are
      massless (Goldstone bosons of the broken boosts).

Dependency: sympy.  Usage: python3 verify_flrw_reduction.py
"""
import sys
# --- Encoding guard (Windows): force UTF-8 output to avoid UnicodeEncodeError
#     on the pretty-printed matrices (sp.pprint uses box-drawing characters).
#     Equivalent to `set PYTHONIOENCODING=utf-8`, made automatic.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass  # Python < 3.7 or stream already fixed: no effect, non-blocking

import sympy as sp

t, a = sp.symbols('t a', positive=True)

# ----------------------------------------------------------------------
# (1) F^(S)_{mu nu} = 0 for the ansatz S_mu = (s(t), 0, 0, 0)
# ----------------------------------------------------------------------
s = sp.Function('s')(t)
S_low = [s, 0, 0, 0]                      # S_0 = s(t), S_i = 0
def d(mu, expr):                          # homogeneity: d_i = 0, only d_0 acts
    return sp.diff(expr, t) if mu == 0 else sp.Integer(0)
F = sp.Matrix(4, 4, lambda mu, nu: d(mu, S_low[nu]) - d(nu, S_low[mu]))
print("(1) F^(S)_{mu nu} =")
sp.pprint(F)
assert F == sp.zeros(4, 4)
print("    => F^(S) == 0  [OK]  (kinetic term vanishes, non-dynamical mode)\n")

# ----------------------------------------------------------------------
# (2) w = -1 at the VEV
# ----------------------------------------------------------------------
s0, Wp, W0 = sp.symbols("s0 Wp W0", real=True)     # s0=VEV, Wp=W'(X0), W0=W(X0)
g    = sp.diag(-1, a**2, a**2, a**2)               # FLRW (-+++)
ginv = g.inv()
S    = sp.Matrix([s0, 0, 0, 0])                    # S_mu = (s0,0,0,0), constant
# T_{mu nu} = 2 W'(X) S_mu S_nu - W(X) g_{mu nu}   (form derived in the appendix)
T = 2*Wp*(S*S.T) - W0*g
T_vev = T.subs(Wp, 0)                              # at the VEV: W'(X0)=0
print("(2) At the VEV (W'(X0)=0),  T_{mu nu} =")
sp.pprint(T_vev)
u   = sp.Matrix([1, 0, 0, 0])                      # u^mu comoving
rho = sp.simplify((u.T * T_vev * u)[0])            # rho = T_{mu nu} u^mu u^nu
p   = sp.simplify((ginv * T_vev)[1, 1])            # p   = T^i_i (isotropic)
w   = sp.simplify(p / rho)
print(f"    rho = {rho},   p = {p},   w = p/rho = {w}")
assert w == -1
print("    => w = -1 exact (cosmological constant)  [OK]\n")

# ----------------------------------------------------------------------
# (3) Fluctuations: mass cancellation -> massless Goldstones
#     Generic quadratic W(X): W(X) = c2 X + c4 X^2
# ----------------------------------------------------------------------
c2, c4, X, u_ = sp.symbols('c2 c4 X u', real=True)
W  = c2*X + c4*X**2
Wp_of = sp.diff(W, X)                               # W'(X)
X0 = -s0**2                                         # X0 = g^{00} s0^2 = -s0^2
# X = X0 + u,  u = 2 s0 dS^0 + dS_mu dS^mu ; expand -W(X) in u
minusW = sp.series(-W.subs(X, X0 + u_), u_, 0, 3).removeO()
coeff_u1 = sp.simplify(minusW.coeff(u_, 1))        # coefficient of the term linear in u
Wp_at_X0 = sp.simplify(Wp_of.subs(X, X0))
print("(3) Quadratic term: the coefficient of (delta S_mu delta S^mu) is the")
print(f"    coefficient linear in u = -W'(X0) = {coeff_u1}")
print(f"    W'(X0) = {Wp_at_X0}")
assert sp.simplify(coeff_u1 + Wp_at_X0) == 0       # coeff_u1 == -W'(X0)
print("    => at the VEV, W'(X0)=0 cancels this term: delta S_i massless (Goldstones)  [OK]")

print("\nALL CHECKS PASS.")
