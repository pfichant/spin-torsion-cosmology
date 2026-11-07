#!/usr/bin/env python3
"""
estimate_omega_mono_F3.py -- Foundation III, MONO-1, checks [A] and [B]
=======================================================================
Order-of-magnitude estimate of the monopole abundance for a Kibble-Zurek
network formed at the GUT scale, WITHOUT inflation, with standard radiative
dilution to today. Added 15/10/2026 (decision F3-A14): the figure quoted in
Foundation III (Eq. omega_mono_estimate) had no producing script.

[A]  xi_KZ(T_GUT) ~ xi_0 (tau_Q/tau_0)^(1/4)    (mean field, nu = 1/2, z = 2)
     xi_0 = hbar c / T_GUT,  tau_0 = hbar / T_GUT,  tau_Q = 1/H(T_GUT)
     H = 1.66 sqrt(g*) T^2 / M_Pl  (radiation era)
[B]  n_mono ~ p / xi_KZ^3  (p ~ 0.3), diluted as (T0/T_GUT)^3, optionally
     times the entropy factor g*s,0/g*s(T_GUT); Omega = n M_mono / rho_crit.

WHAT THIS DOES NOT ESTABLISH: the monopole mass, the Kibble fraction p and
the effective g* at T_GUT are inputs, not ECF results; the stiff phase,
which would modify a(T), is not included (NEFOLD-1). Order of magnitude only.
"""
import math

HBAR_GeVs = 6.582e-25      # GeV s
HBARC_GeVm = 1.9733e-16    # GeV m
M_PL = 1.2209e19           # GeV (non-reduced)
GEV_KG = 1.7827e-27        # kg per GeV/c^2
T_GUT = 1e16               # GeV
G_STAR = 106.75            # SM value used as a floor at T_GUT
G_S0 = 3.91
P_KIBBLE = 0.3
T0 = 2.725 * 8.617e-5 * 1e-9   # GeV
H_LITTLE = 0.6736
RHO_CRIT = 1.8784e-26 * H_LITTLE**2   # kg/m^3

H = 1.66 * math.sqrt(G_STAR) * T_GUT**2 / M_PL / HBAR_GeVs
tau0, tauQ, xi0 = HBAR_GeVs / T_GUT, 1.0 / H, HBARC_GeVm / T_GUT
xi = xi0 * (tauQ / tau0) ** 0.25
print("[A] xi_KZ(T_GUT)")
print(f"    H(T_GUT) = {H:.3e} s^-1, tau_Q/tau_0 = {tauQ/tau0:.1f}")
print(f"    xi_0 = {xi0:.2e} m, xi_KZ = {xi:.2e} m = {xi/xi0:.2f} xi_0")

n0 = P_KIBBLE / xi**3
print("\n[B] Omega_mono today (no inflation)")
print(f"    {'M_mono [GeV]':>12} {'with entropy':>14} {'without':>10}")
for M in (1e16, 1e17, 1e18):
    out = []
    for g in (G_S0 / G_STAR, 1.0):
        n_today = n0 * (T0 / T_GUT) ** 3 * g
        out.append(n_today * M * GEV_KG / RHO_CRIT)
    print(f"    {M:>12.0e} {out[0]:>14.1e} {out[1]:>10.1e}")
print("\n    Preskill (1979) without inflation: Omega h^2 ~ 1e11")
print("    -> every case above exceeds it by 10 or more orders of magnitude.")
