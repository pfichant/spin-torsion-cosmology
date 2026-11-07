#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Project     : Foundation II: Topological Crystallization of the Vacuum
Script Name : plot_growth_comparison.py
Author      : Pascal Fichant
Version     : 2.0 (16/10/2026, decision SEED-1)
Description :
    Eddington-limited growth M(t) = M_seed * exp(f_Edd * k * (t - t_form)),
    k = 0.016 Myr^-1 (corpus value), for a Pop III seed (1e2 Msun) and an
    ECF Macro-Knot seed (1e5 Msun; benchmark scale, formation efficiency
    eps_coll not derived), accretion starting at z_form = 20, on the ECF
    closure background (H0 = 73.04, Omega_m = omega_m/h^2 = 0.267).
    Compared with two observed black holes:
      UHZ1        z = 10.1,  M_BH ~ 4e7 Msun (range 1e7-1e8; Bogdan et al. 2024,
                  Nat. Astron. 8, 126; Natarajan et al. 2024, ApJL)
      J1342+0928  z = 7.54,  M_BH = 7.8e8 Msun (Banados et al. 2018)
    and prints the Eddington ratio f_Edd each seed needs to reach them.

CORRECTION 16/10/2026 (SEED-1). Version 1.0.4 started the growth at
t = 10 Myr after the Big Bang (not at a formation redshift), announced a
"~300 Myr head start" (the head start for a factor 1e3 in mass is
ln(1e3)/k = 432 Myr) and supported the claim that the ECF seed reaches
1e9 Msun by z ~ 10 at the Eddington rate. On the corpus inputs it reaches
~1e7 Msun at z = 10 and 1e9 Msun only near z ~ 7; 1e9 Msun at z = 10
requires f_Edd ~ 2.

Output      : Fig_JWST_Growth_Comparison.png
=============================================================================
"""
import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H0_KMS, H_DIM = 73.04, 0.7304
OMEGA_M = 0.14237 / H_DIM**2
OMEGA_R = 4.1834e-5 / H_DIM**2
OMEGA_L = 1.0 - OMEGA_M - OMEGA_R
K_EDD = 0.016            # Myr^-1 at f_Edd = 1 (corpus value)
Z_FORM = 20.0
SEEDS = {'Pop III seed ($10^2\\,M_\\odot$)': 1e2, 'ECF Macro-Knot seed ($10^5\\,M_\\odot$)': 1e5}
OBS = [('UHZ1 (Bogdán+2024)', 10.1, 4e7), ('J1342+0928 (Bañados+2018)', 7.54, 7.8e8)]

def age_myr(z):
    Hs = H0_KMS * 1e3 / 3.0857e22
    f = lambda zz: 1.0 / ((1 + zz) * Hs * np.sqrt(OMEGA_M*(1+zz)**3 + OMEGA_R*(1+zz)**4 + OMEGA_L))
    return quad(f, z, np.inf)[0] / 3.156e13

def main():
    t_form = age_myr(Z_FORM)
    t = np.linspace(t_form, 900.0, 600)
    print(f"Accretion onset z_form = {Z_FORM:.0f} (t = {t_form:.0f} Myr); k = {K_EDD} Myr^-1")
    for name, z, M in OBS:
        dt = age_myr(z) - t_form
        req = {lab: np.log(M / M0) / (K_EDD * dt) for lab, M0 in SEEDS.items()}
        print(f"  {name:28s} z={z:5.2f} t={age_myr(z):4.0f} Myr  M={M:.1e}  "
              f"f_Edd needed: Pop III {list(req.values())[0]:.2f}, ECF {list(req.values())[1]:.2f}")
    t10 = age_myr(10.0)
    print(f"  At f_Edd = 1: ECF seed at z=10 -> {1e5*np.exp(K_EDD*(t10-t_form)):.1e} Msun; "
          f"head start for a factor 1e3: {np.log(1e3)/K_EDD:.0f} Myr")

    plt.figure(figsize=(10, 6), dpi=300)
    styles = [('blue', '--'), ('red', '-')]
    for (lab, M0), (c, ls) in zip(SEEDS.items(), styles):
        plt.plot(t, M0 * np.exp(K_EDD * (t - t_form)), color=c, ls=ls, lw=2.3,
                 label=lab + r' at $f_{\rm Edd}=1$')
    for name, z, M in OBS:
        plt.scatter([age_myr(z)], [M], s=70, color='k', zorder=5)
        plt.annotate(f"{name}\n$z={z}$", (age_myr(z), M), textcoords='offset points',
                     xytext=(-120, 12), fontsize=9)
    plt.axvline(t10, color='purple', ls='-.', alpha=0.5, label=r'$z=10$')
    plt.axhline(1e9, color='k', ls=':', lw=1.2, label=r'$10^9\,M_\odot$')
    plt.yscale('log'); plt.ylim(10, 1e10); plt.xlim(0, 900)
    plt.xlabel('Cosmic time (Myr after the bounce; ECF closure background)', fontsize=11)
    plt.ylabel(r'Black-hole mass ($M_\odot$)', fontsize=11)
    plt.title(r'Eddington-limited growth from $z_{\rm form}=20$ ($k=0.016$ Myr$^{-1}$)', fontsize=12)
    plt.grid(True, which='both', ls='--', alpha=0.3)
    plt.legend(loc='lower right', fontsize=9)
    plt.tight_layout()
    plt.savefig('Fig_JWST_Growth_Comparison.png')
    print("Saved: Fig_JWST_Growth_Comparison.png")

if __name__ == '__main__':
    main()
