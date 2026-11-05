#!/usr/bin/env python3
# Last modified: 09/10/2026, 08:47 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
"""
scan_F_ion_H0_BAO.py — Foundation I (FIG-ACTIVES, 09/10/2026)

What the H0 calibration costs on the BAO sector, on the ACTIVE background (A-7).

F_ion is CALIBRATED on H0 (r_s = 135.65 Mpc -> H0 = 73.04). This script asks a
different question: on the same background, which F_ion would a joint fit of
SH0ES and the four diagonal BAO bins (BOSS DR12 + eBOSS DR16, the points of
chi_carre.py) prefer, and how far is the calibrated point from that compromise?

Assumptions (status CALCULATED-CONDITIONAL, to be stated wherever a number is quoted):
  - H0(F) = 67.4 + 20.40 (F - 1)            (linear map of Foundation I)
  - r_s(F) = 147.1 (67.4/H0)^p, p fixed so that r_s(1.2765) = 135.65 Mpc
  - Omega_m(F) = omega_m / h(F)^2, omega_m = 0.14237 (A-7)
  - flat late-time background, spin term neglected (Omega_s0 ~ 1e-13)
  - r_drag identified with r_s (PO-ECF-BAO-RDRAG, OPEN); no CMB block.
Sensitivity: r_s proportional to 1/H0 instead of the power law moves the
minimum by ~0.003 in F_ion (printed below).
"""
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
from scipy.optimize import minimize_scalar, brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chi_carre as cc   # BAO data and D_M/r_s of the partial chi2 budget

OB = cc.obs_data['BAO']
OMEGA_M = 0.02237 + 0.1200
H0_L, RS_L = 67.4, 147.1
F_CAL, H0_CAL, RS_CAL = 1.2765, 73.04, 135.65
SLOPE = (H0_CAL - H0_L) / (F_CAL - 1.0)
P_RS = np.log(RS_L / RS_CAL) / np.log(H0_CAL / H0_L)

def background(F, power=True):
    H0 = H0_L + SLOPE * (F - 1.0)
    Om = OMEGA_M / (H0 / 100.0) ** 2
    rs = RS_L * (H0_L / H0) ** (P_RS if power else 1.0)
    return H0, Om, rs

def chi2_bao(F, power=True):
    H0, Om, rs = background(F, power)
    return sum(((OB['val'][i] - cc.compute_DM_rs(OB['z'][i], H0, Om, rs)) / OB['err'][i]) ** 2
               for i in range(len(OB['z'])))

def chi2_h0(F):
    return ((background(F)[0] - cc.obs_data['H0']['val']) / cc.obs_data['H0']['err']) ** 2

def total(F, power=True):
    return chi2_bao(F, power) + chi2_h0(F)

if __name__ == "__main__":
    print("F_ion scan on the active background (A-7), H0 + 4 BAO bins")
    print(f"  slope dH0/dF = {SLOPE:.3f} ; r_s exponent p = {P_RS:.4f}")
    for F in (1.0, F_CAL):
        H0, Om, rs = background(F)
        print(f"  F = {F:.4f}: H0 = {H0:.2f}, Omega_m = {Om:.4f}, r_s = {rs:.2f} Mpc, "
              f"chi2_BAO = {chi2_bao(F):.2f}, chi2_H0 = {chi2_h0(F):.2f}, total = {total(F):.2f}")
    r = minimize_scalar(total, bounds=(1.0, 1.4), method='bounded')
    Fm = r.x; H0m, Omm, rsm = background(Fm)
    print(f"  joint minimum: F = {Fm:.3f}, H0 = {H0m:.2f}, Omega_m = {Omm:.4f}, "
          f"chi2_BAO = {chi2_bao(Fm):.2f}, chi2_H0 = {chi2_h0(Fm):.2f}, total = {r.fun:.2f}")
    print(f"  calibrated point above the minimum: Delta chi2 = {total(F_CAL) - r.fun:.2f}")
    g = lambda F: total(F) - r.fun - 1.0
    lo, hi = brentq(g, 1.0, Fm), brentq(g, Fm, 1.4)
    print(f"  Delta chi2 < 1 (68 %, one parameter): F in [{lo:.3f}, {hi:.3f}], "
          f"H0 in [{background(lo)[0]:.2f}, {background(hi)[0]:.2f}]")
    r2 = minimize_scalar(lambda F: total(F, power=False), bounds=(1.0, 1.4), method='bounded')
    print(f"  sensitivity (r_s ~ 1/H0): F = {r2.x:.3f}, H0 = {background(r2.x)[0]:.2f}")
    rb = minimize_scalar(chi2_bao, bounds=(1.0, 1.4), method='bounded')
    print(f"  BAO alone, physical domain F >= 1: minimum at F = {rb.x:.3f} (chi2_BAO = {rb.fun:.2f})")
