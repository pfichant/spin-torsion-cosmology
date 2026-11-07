#!/usr/bin/env python3
"""
check_torsion_sme_bound.py  (22/10/2026)

Laboratory (SME) bound on a cosmological axial-torsion condensate
<S_mu> = s0 delta_mu^0, S_mu = (1/6) eps_{mu nu la rho} T^{nu la rho}
(same definition as A_mu in Kostelecky, Russell & Tasson, PRL 100, 111102 (2008),
arXiv:0712.4393, Eq. 1).

Minimal coupling of Dirac fermions (ECKS):  b_mu = -(3/4) A_mu  (KRT Eq. 3 with xi4 = 3/4).
KRT Eq. 6 (minimal coupling, Sun-centred celestial equatorial frame T,X,Y,Z):
    |A_T| < 2.9e-27 GeV, |A_X| < 2.1e-31 GeV, |A_Y| < 2.5e-31 GeV, |A_Z| < 1.0e-29 GeV.

A condensate purely timelike in the CMB rest frame acquires, in the Sun-centred frame,
spatial components A_i = -gamma (v/c) n_i s0 (Lorentz boost), with v the Sun's velocity
relative to the CMB (Planck 2018 dipole: 369.82 km/s towards l = 264.021 deg,
b = 48.253 deg).  Earth's orbital motion (~30 km/s) is neglected (< 10 %).

Dark-energy normalisation of Foundation II (Eq. mass_coupling):
    rho_Lambda^eff = (1/4) m_T^2 s0^2 = 3.0e-47 GeV^4  =>  s0 = 2 sqrt(rho)/m_T.
"""
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

c_kms = 299792.458
v_kms = 369.82
dip = SkyCoord(l=264.021*u.deg, b=48.253*u.deg, frame='galactic').icrs
ra, dec = dip.ra.rad, dip.dec.rad
n = np.array([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
beta = v_kms / c_kms
gamma = 1/np.sqrt(1-beta**2)

bounds = {'T': 2.9e-27, 'X': 2.1e-31, 'Y': 2.5e-31, 'Z': 1.0e-29}   # GeV, KRT Eq. 6
coef = {'T': gamma, 'X': gamma*beta*abs(n[0]), 'Y': gamma*beta*abs(n[1]), 'Z': gamma*beta*abs(n[2])}

rho = 3.0e-47                      # GeV^4
two_sqrt_rho = 2*np.sqrt(rho)      # GeV^2

print(f"CMB dipole direction: RA = {np.degrees(ra):.2f} deg, Dec = {np.degrees(dec):.2f} deg")
print(f"n = ({n[0]:+.3f}, {n[1]:+.3f}, {n[2]:+.3f}),  v/c = {beta:.3e}")
print(f"2 sqrt(rho_Lambda^eff) = {two_sqrt_rho:.3e} GeV^2\n")
smax = {}
for k in 'TXYZ':
    smax[k] = bounds[k]/coef[k]
    print(f"component {k}: |A_{k}| < {bounds[k]:.1e} GeV, coefficient {coef[k]:.3e} -> s0 < {smax[k]:.2e} GeV"
          f"  ->  m_T > {two_sqrt_rho/smax[k]:.2e} GeV")
best = min(smax, key=smax.get)
print(f"\nmost constraining component: {best}: s0 < {smax[best]:.2e} GeV, m_T > {two_sqrt_rho/smax[best]:.2e} GeV")

print("\nValues used in the corpus:")
for label, mT in [("illustrative m_T (F2 App. F, s0 = 4.8e-3 eV)", two_sqrt_rho/4.8e-12),
                  ("m_T ~ eta_EW = 246.22 GeV (F2, string core)", 246.22)]:
    s0 = two_sqrt_rho/mT
    print(f"  {label}: m_T = {mT:.3e} GeV, s0 = {s0:.3e} GeV, "
          f"s0/s0_max(T) = {s0/smax['T']:.2e}, s0/s0_max({best}) = {s0/smax[best]:.2e}")
print(f"\nformer stated bound |s0|/M_Pl < 1e-15 (M_Pl = 1.22e19 GeV) -> s0 < {1e-15*1.22e19:.2e} GeV,"
      f" i.e. {1e-15*1.22e19/smax['T']:.1e} times looser than the A_T bound")

print("\nQuartic self-coupling implied by the VEV relation s0^2 = m_T^2/(lambda_T/3!) (F2 Eq. torsion_vev):")
for label, mT in [("illustrative m_T", two_sqrt_rho/4.8e-12),
                  ("m_T at the A_T bound", two_sqrt_rho/smax['T']),
                  (f"m_T at the A_{best} bound", two_sqrt_rho/smax[best])]:
    s0 = two_sqrt_rho/mT
    print(f"  {label}: m_T = {mT:.2e} GeV, lambda_T = 6 m_T^2/s0^2 = {6*mT**2/s0**2:.1e}")
