#!/usr/bin/env python3
"""
check_rs_spin_domain.py  (added 23/10/2026)

Domain of validity of the calibrated Foundation I spin branch (Eq. friedmann_ecf_late):
    E^2(z) = Om_r (1+z)^4 + Om_m (1+z)^3 + Om_spin_0 (1+z)^6 + Om_L,
normalised by rho_spin = 0.093 rho_r at z_ref = 5600 (script_01_solve_sound_horizon.py).

Three checks, same inputs as script_01 (Planck 2018 omega_b, omega_c; omega_r = omega_g + omega_n;
tau_tor = 0.9975; z_drag = 1059.94; upper limit 1e7):
 (1) rho_spin/rho_r at the Great-Annihilation window and at BBN if the a^-6 law is extended;
     redshift of equality with radiation.
 (2) Sensitivity of r_s to the redshift z_c up to which the a^-6 law is kept.
     Beyond z_c, two variants: 'frozen' (spin/radiation ratio kept constant, term ~ (1+z)^4)
     and 'zero' (spin term removed).
 (3) Comparison with a primordial stiff term that equals radiation at t_eq = 1e-11 s
     (Foundation II) and then dilutes as a^-6: ratio ~ t_eq/t in the radiation era.
Not a derivation: it states what the calibrated branch requires. Status: PO-ECF-BBN-SPIN.
"""
import numpy as np
from scipy.integrate import quad

h, wb, wc = 0.6736, 0.02237, 0.1200
wg, wn = 2.4728e-5, 1.710606110185788e-5
c_kms, TAU, Z_DRAG, Z_START = 299792.458, 0.9975, 1059.94, 1e7
R_REF, Z_REF = 0.093, 5600.0
Om_r = (wg + wn) / h**2; Om_m = (wb + wc) / h**2; Om_L = 1 - Om_m - Om_r
Om_s0 = R_REF * Om_r / (1 + Z_REF)**2

def ratio_spin_rad(z):
    return R_REF * ((1 + z) / (1 + Z_REF))**2

def rs(zc=None, mode='full'):
    def f(z):
        if mode == 'full' or z <= zc: sp = Om_s0 * (1 + z)**6
        elif mode == 'frozen': sp = Om_s0 * (1 + zc)**6 * ((1 + z) / (1 + zc))**4
        else: sp = 0.0
        H = 100 * h * np.sqrt(Om_r * (1 + z)**4 + Om_m * (1 + z)**3 + sp + Om_L)
        cs = c_kms / np.sqrt(3 * (1 + 3 * wb / (4 * wg) / (1 + z)))
        return TAU * cs / H
    pts = np.logspace(np.log10(Z_DRAG), np.log10(Z_START), 200)
    return sum(quad(f, a, b)[0] for a, b in zip(pts[:-1], pts[1:]))

def t_rad(z):  # radiation era, H = H0 sqrt(Om_r) (1+z)^2, t = 1/(2H), H0 = 73.04 km/s/Mpc (ECF)
    H0 = 73.04e3 / 3.0857e22; Or = (wg + wn) / 0.7304**2
    return 1 / (2 * H0 * np.sqrt(Or) * (1 + z)**2)

if __name__ == '__main__':
    r_full = rs()
    print(f"r_s(full a^-6 branch) = {r_full:.3f} Mpc  (script_01: 135.65 ; check)")
    assert abs(r_full - 135.65) < 0.05
    print("\n(1) spin/radiation if the a^-6 law is extended")
    for lab, z in (("recombination", 1090), ("z_ref", Z_REF), ("equality", Z_REF / np.sqrt(R_REF) ),
                   ("GA, low edge z=6.9e8", 6.9e8), ("GA, high edge z=6.9e9", 6.9e9)):
        print(f"  {lab:24s} z={z:9.3e}  ratio = {ratio_spin_rad(z):9.3e}")
    print(f"  equality with radiation at 1+z = {(1+Z_REF)/np.sqrt(R_REF):.3e}")
    print("\n(2) r_s versus the redshift z_c up to which the a^-6 law is kept")
    print(f"  (LCDM with the same integrator: {rs(mode='zero', zc=0.0)/TAU:.3f} Mpc, tau_tor = 1)")
    print("  z_c       ratio(z_c)  r_s frozen   r_s zero")
    for zc in (6e3, 1e4, 2e4, 5e4, 1e5, 3e5, 1e6):
        print(f"  {zc:8.0e}  {ratio_spin_rad(zc):9.2f}  {rs(zc,'frozen'):10.3f}  {rs(zc,'zero'):9.3f}")
    print("\n(3) primordial stiff term equal to radiation at t = 1e-11 s, then a^-6 (ratio ~ 1e-11 s / t)")
    for lab, z in (("z=6e9 (t=%.2g s)" % t_rad(6e9), 6e9), ("z=5600 (t=%.2g s)" % t_rad(5600), 5600), ("z=1090", 1090)):
        r3 = 1e-11 / t_rad(z); r1 = ratio_spin_rad(z)
        print(f"  {lab:24s} calibrated={r1:9.2e}  primordial={r3:9.2e}  gap={np.log10(r1/r3):.1f} orders")
