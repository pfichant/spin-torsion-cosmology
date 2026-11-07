#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estimate_w_from_nonminimal.py
=============================
If the non-minimal coupling were added, what (w0, wa) would it produce --
and what value of xi would be required?

STATUS OF THIS SCRIPT -- read first
-----------------------------------
This is a MODEL OF THE MECHANISM, not a derivation from the ECF action.
extract_nonminimal_xi.py established that the coupling is NOT contained in
R~(g,T) and would have to be added; nothing fixes xi. What follows therefore
answers a conditional question:

    IF a term  xi * R^{mu nu} S_mu S_nu  is added, what w(z) follows,
    and what xi would be needed to land on (w0, wa) = (-0.904, -0.153)?

Everything below is contingent on that "if". No claim is made that the ECF
predicts these numbers.

THE MECHANISM, IN ONE LINE
--------------------------
verify_nonminimal_coupling_flrw.py gave R^{00} = -3(Hdot + H^2) = -3 addot/a.
The coupling therefore shifts the effective mass of the condensate:

    m^2_eff(a) = m_T^2 + 6 xi (addot/a)

The VEV sits where the effective potential is minimised, so for a quartic
W(X) = (1/2) m^2 X + (lambda/4!) X^2 the condensate density scales as

    rho(a)  ~  [ m^2_eff(a) ]^2  =  m_T^4 [ 1 + eps(a) ]^2 ,
    eps(a) = 6 xi (addot/a) / m_T^2

and then, by the continuity equation,

    w(a) = -1 - (1/3) dln(rho)/dln(a).

Since addot/a evolves, w != -1: that is the whole point. The quartic form is
a choice; a different W changes the power, not the qualitative conclusion.

Dependency: numpy, scipy.  Usage: python3 estimate_w_from_nonminimal.py
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np
from scipy.optimize import brentq

# [D3, 22/09/2026 -- DEC-A7-POST-05] The background of the estimate is the
# calibrated ECF one (targets = ECF (w0, wa); q0 "from the calibrated
# background", see the end of the script), hence Omega_m = omega_m/h_ECF^2 (A-7).
# Was OM0, OL0 = 0.315, 0.685 (Planck-h value).
OM0 = (0.02237 + 0.1200)/0.7304**2      # 0.266868 -- background for the estimate
OL0 = 1.0 - OM0
W0_TARGET, WA_TARGET = -0.904, -0.153   # ECF calibrated values

print("=" * 74)
print("  Conditional estimate: w(z) from a non-minimal coupling")
print("=" * 74)
print("\n  /!\\ CONDITIONAL. The coupling is NOT in R~(g,T) (see")
print("      extract_nonminimal_xi.py); xi is a NEW parameter, not derived.")


def addot_over_a(a, Om0=OM0, OL0=OL0):
    """addot/a = -q H^2, for a matter + Lambda background, in units of H0^2."""
    E2 = Om0 * a**-3 + OL0
    q = 0.5 * (Om0 * a**-3) / E2 - OL0 / E2       # q = (1/2)Om - OL, normalised
    return -q * E2                                 # in units of H0^2


def w_of_a(a, eps0, n=2.0):
    """
    Equation of state from rho ~ [1 + eps(a)]^n, with eps normalised so that
    eps(a=1) = eps0. n = 2 for a quartic potential.
    w = -1 - (1/3) dln rho / dln a, computed by centred differences.
    """
    r0 = addot_over_a(1.0)
    def rho(x):
        return (1.0 + eps0 * addot_over_a(x) / r0) ** n
    h = 1e-5
    dlnrho = (np.log(rho(a * (1 + h))) - np.log(rho(a * (1 - h)))) / (2 * h)
    return -1.0 - dlnrho / 3.0


def cpl_fit(eps0, n=2.0):
    """Read off (w0, wa) in the CPL sense: w(a) = w0 + wa (1 - a)."""
    w0 = w_of_a(1.0, eps0, n)
    h = 1e-3
    dw_da = (w_of_a(1.0 + h, eps0, n) - w_of_a(1.0 - h, eps0, n)) / (2 * h)
    wa = -dw_da                      # since dw/da = -wa
    return w0, wa


# ---------------------------------------------------------------------------
# 1. What eps0 reproduces w0 = -0.904 ?
# ---------------------------------------------------------------------------
print("\n(1) Which coupling strength reproduces w0 = -0.904 ?")
try:
    eps_sol = brentq(lambda e: cpl_fit(e)[0] - W0_TARGET, -0.9, 5.0, xtol=1e-10)
    w0_s, wa_s = cpl_fit(eps_sol)
    print(f"    eps0 = 6 xi (addot/a)_0 / m_T^2  =  {eps_sol:+.4f}")
    print(f"    gives  w0 = {w0_s:+.4f}   (target {W0_TARGET:+.3f})")
    print(f"           wa = {wa_s:+.4f}   (target {WA_TARGET:+.3f})")
except ValueError:
    eps_sol = None
    print("    no solution in the scanned range.")

# ---------------------------------------------------------------------------
# 2. The decisive test: is wa right once w0 is fixed?
# ---------------------------------------------------------------------------
print("\n(2) THE DECISIVE TEST -- wa is NOT free once w0 is fixed")
print("    The mechanism has ONE parameter. Fixing w0 fixes wa. So the model")
print("    is falsifiable on wa alone: it either lands on -0.153 or it does not.")
if eps_sol is not None:
    print()
    print(f"      predicted wa = {wa_s:+.4f}")
    print(f"      required  wa = {WA_TARGET:+.4f}")
    d = wa_s - WA_TARGET
    print(f"      discrepancy  = {d:+.4f}")
    if abs(d) < 0.05:
        print("      => COMPATIBLE at this crude level.")
    else:
        print("      => NOT compatible. The single-parameter mechanism cannot")
        print("         reach both values simultaneously with a quartic potential.")

# ---------------------------------------------------------------------------
# 3. Does another potential power help?
# ---------------------------------------------------------------------------
print("\n(3) Does a different potential (different power n) rescue it?")
print(f"    {'n':>5} {'eps0':>10} {'w0':>9} {'wa':>9}   verdict")
for n in (1.0, 1.5, 2.0, 3.0, 4.0):
    try:
        e = brentq(lambda x: cpl_fit(x, n)[0] - W0_TARGET, -0.9, 20.0, xtol=1e-10)
        a0, b0 = cpl_fit(e, n)
        ok = "compatible" if abs(b0 - WA_TARGET) < 0.05 else "no"
        print(f"    {n:>5.1f} {e:>10.4f} {a0:>+9.4f} {b0:>+9.4f}   {ok}")
    except ValueError:
        print(f"    {n:>5.1f} {'--':>10} {'--':>9} {'--':>9}   no solution")

# ---------------------------------------------------------------------------
# 4. w(z) shape
# ---------------------------------------------------------------------------
if eps_sol is not None:
    print("\n(4) Shape of w(z) for the fitted coupling")
    print(f"    {'z':>6} {'w(z) model':>12} {'w(z) CPL':>10}")
    for z in (0.0, 0.5, 1.0, 2.0, 3.0):
        a = 1.0 / (1 + z)
        wm = w_of_a(a, eps_sol)
        wc = W0_TARGET + WA_TARGET * (1 - a)
        print(f"    {z:>6.1f} {wm:>+12.4f} {wc:>+10.4f}")

print("\n" + "=" * 74)
print("  HOW xi COULD BE PINNED DOWN")
print("=" * 74)
print("  eps0 = 6 xi (addot/a)_0 / m_T^2, and both (addot/a)_0 and m_T are")
print("  already fixed elsewhere in the corpus:")
print("    * (addot/a)_0 = -q0 H0^2, with q0 from the calibrated background;")
print("    * m_T^2 s0^2 = 4 |Omega_tau| rho_crit,0 (F2, eq. mass_coupling).")
print("  So xi is NOT a free knob once the rest is held fixed: it is one number,")
print("  and it is determined by w0. That is what makes wa a PREDICTION rather")
print("  than a second fit -- and therefore a falsification test.")
print()
print("WHAT THIS DOES NOT ESTABLISH:")
print("  * that the ECF action generates this coupling -- it does not;")
print("  * the quartic form of W, which sets the power n;")
print("  * the sign of xi, or ghost-freedom of the coupled sector;")
print("  * the perturbation sector, hence nothing about S8 or G_eff.")
