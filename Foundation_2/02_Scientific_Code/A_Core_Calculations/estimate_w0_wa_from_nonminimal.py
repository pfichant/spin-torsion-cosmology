#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estimate_w0_wa_from_nonminimal.py
=================================
If the non-minimal coupling were added, what (w0, wa) would it give?

THE CHAIN, step by step
-----------------------
1. Foundation II fixes the condensate by the minimum of W(X):
       s0^2 = m_T^2 / (lambda_T/3!)          (Eq. torsion_vev)
   and the dark-energy density by the well depth:
       rho_Lambda = (1/4) m_T^2 s0^2          (Eq. rho_lambda)
   Both are constant, hence w = -1 exactly (F2 l.1433).

2. verify_nonminimal_coupling_flrw.py showed that a term xi R^{mu nu}S_mu S_nu
   does NOT vanish on FLRW:
       R^{mu nu} S_mu S_nu = -3 (addot/a) s^2,   R^{00} = -3(Hdot + H^2).

3. It therefore shifts the effective mass squared:
       m_eff^2(t) = m_T^2 + 2 xi R^{00} = m_T^2 - 6 xi (Hdot + H^2).

4. The minimum moves with it, s0^2 = m_eff^2/lambda, and the well depth becomes
       rho(t) = (1/4) m_eff^2 s0^2 = m_eff^4 / (4 lambda)
   so that
       rho(a) proportional to [ 1 - eps * (Hdot + H^2)/H0^2 ]^2,
   with the single dimensionless combination
       eps  ==  6 xi H0^2 / m_T^2.

5. Then w(a) = -1 - (1/3) dln(rho)/dln(a).

WHAT THIS IS AND IS NOT
-----------------------
This is a LEADING-ORDER estimate on a FIXED LambdaCDM background: the modified
dark-energy density is not fed back into H(z). A self-consistent solution would
require integrating the coupled system. The purpose here is narrower and worth
stating plainly: to find out whether the mechanism produces (w0, wa) of the
right ORDER and, crucially, of the right SIGN -- and in particular whether
matching w0 = -0.904 forces a value of wa anywhere near -0.153.

If the signs disagree, no tuning of xi can rescue it, and that is a result.

Dependency: numpy.  Usage: python3 estimate_w0_wa_from_nonminimal.py
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

# --- ECF / Foundation I calibrated targets -------------------------------
W0_TARGET = -0.904          # Foundation I
WA_TARGET = -0.153          # Foundation I
# [D3, 22/09/2026 -- DEC-A7-POST-05] Was 0.3089 ("F2 uses this in Fig.3
# context"; not found in any candidate paper). The targets are the ECF (w0, wa),
# so the background is the ECF one: Omega_m = omega_m/h_ECF^2 (A-7).
OM0 = (0.02237 + 0.1200)/0.7304**2   # 0.266868 matter fraction (ECF background, A-7)


# --- Background: flat LambdaCDM ------------------------------------------
def E2(a):
    """H^2/H0^2 for flat LambdaCDM."""
    return OM0 * a**-3 + (1.0 - OM0)


def Hdot_plus_H2_over_H02(a):
    """(Hdot + H^2)/H0^2 = addot/(a H0^2), exact for flat LambdaCDM."""
    # addot/a = -(1/2) H0^2 [ Om a^-3 - 2 OL ]
    return -0.5 * (OM0 * a**-3 - 2.0 * (1.0 - OM0))


def rho_of_a(a, eps):
    """rho ~ [1 - eps*(Hdot+H^2)/H0^2]^2, up to a constant."""
    return (1.0 - eps * Hdot_plus_H2_over_H02(a)) ** 2


def w_of_a(a, eps, h=1e-5):
    """w = -1 - (1/3) dln(rho)/dln(a), by centred differences in ln a."""
    lna = np.log(a)
    rp = rho_of_a(np.exp(lna + h), eps)
    rm = rho_of_a(np.exp(lna - h), eps)
    dlnrho_dlna = (np.log(rp) - np.log(rm)) / (2 * h)
    return -1.0 - dlnrho_dlna / 3.0


def w0_wa(eps):
    """CPL fit: w0 = w(a=1); wa = -dw/da at a=1."""
    w0 = w_of_a(1.0, eps)
    da = 1e-4
    dw_da = (w_of_a(1.0 + da, eps) - w_of_a(1.0 - da, eps)) / (2 * da)
    return w0, -dw_da


print("=" * 74)
print("  (w0, wa) produced by the non-minimal coupling, as a function of xi")
print("=" * 74)
print(f"\n  Targets (Foundation I):  w0 = {W0_TARGET},  wa = {WA_TARGET}")
print(f"  Background: flat LambdaCDM, Om0 = {OM0}")
print("\n  Single dimensionless parameter:  eps = 6 xi H0^2 / m_T^2")

# --- scan -----------------------------------------------------------------
print("\n" + "-" * 74)
print(f"{'eps':>10} {'w0':>12} {'wa':>12}   note")
print("-" * 74)
for eps in (-0.5, -0.2, -0.1, -0.05, 0.0, 0.05, 0.1, 0.2, 0.5):
    w0, wa = w0_wa(eps)
    note = "  <- unperturbed, w = -1 exactly" if eps == 0.0 else ""
    print(f"{eps:>10.3f} {w0:>12.4f} {wa:>12.4f}{note}")

# --- solve for eps that reproduces w0 = -0.904 ----------------------------
print("\n" + "-" * 74)
print("  Solving for the eps that reproduces w0 = -0.904")
print("-" * 74)

lo, hi = -2.0, 2.0
target = W0_TARGET
sols = []
grid = np.linspace(lo, hi, 20001)
vals = np.array([w0_wa(e)[0] for e in grid])
sign = np.sign(vals - target)
for i in range(len(grid) - 1):
    if sign[i] != sign[i + 1] and np.isfinite(vals[i]) and np.isfinite(vals[i + 1]):
        a_, b_ = grid[i], grid[i + 1]
        for _ in range(80):
            m = 0.5 * (a_ + b_)
            if (w0_wa(a_)[0] - target) * (w0_wa(m)[0] - target) <= 0:
                b_ = m
            else:
                a_ = m
        sols.append(0.5 * (a_ + b_))

if not sols:
    print("  No eps reproduces w0 = -0.904 in the scanned range.")
else:
    for e in sols:
        w0, wa = w0_wa(e)
        print(f"  eps = {e:+.5f}   ->   w0 = {w0:+.4f}   wa = {wa:+.4f}")
        print(f"      target wa = {WA_TARGET:+.4f}   =>  ratio wa/target = "
              f"{wa / WA_TARGET:+.2f}")
        print(f"      sign of wa: {'MATCHES' if wa * WA_TARGET > 0 else 'OPPOSITE'} the target")

print("\n" + "=" * 74)
print("  READING")
print("=" * 74)
print("""
  The mechanism gives one dimensionless knob, eps = 6 xi H0^2 / m_T^2, and
  therefore CANNOT fit w0 and wa independently: once eps is fixed by w0, the
  value of wa FOLLOWS. That is the interesting part -- it makes the proposal
  falsifiable rather than adjustable.

  Read the sign line above before anything else. If wa comes out with the
  opposite sign to -0.153, no choice of xi rescues the mechanism, and the
  route of Appendix J.3 fails at the background level -- which would be a
  clean negative result, obtained without the perturbation solver.
""")

print("SCOPE -- what this does NOT establish:")
print("  * no back-reaction: H(z) is held at LambdaCDM, so the numbers shift")
print("    once the modified density is fed back;")
print("  * the CPL form is a 2-parameter fit to a function that is not CPL;")
print("    w0 and wa here are the local expansion at a = 1, not a fit over a range;")
print("  * xi itself is not derived -- only the combination eps is constrained;")
print("  * ghosts and stability of the coupled sector are untouched.")
