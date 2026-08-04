#!/usr/bin/env python3
"""
plot_quadrilemma_omega_m.py — ECF Foundation I
Last modified: 24/07/2026, 13:30 (all figure text translated to English)
Figure: fig_quadrilemma_omega_m.png

Complements fig_trilemma_irreducibility_contours.png (script 08).
That figure scans (w0, z_t) at FIXED Omega_m=0.315 (Planck-h value,
never recomputed for H0=73.04). This script scans Omega_m itself, at
the ACTUAL calibrated (w0,wa)=(-0.904,-0.153), and shows why the
trilemma is in fact a quadrilemma once the CMB acoustic scale theta_*
is included: age, BAO, and theta_* pull Omega_m in mutually
incompatible directions.

Added 20/07/2026, following the omega_m consistency check (see
Foundation I footnote (b) to the trilemma table, and Foundation II
PO-F2-5). Uses the same simplified integral as joint_fit_trilemma.py;
theta_* has a known ~1% systematic offset vs. the literature Planck
value (see that script's docstring) and should not be over-interpreted
at the percent level.
"""

import numpy as np
from scipy import integrate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

c_light = 299792.458
H0 = 73.04
h_ecf = H0/100.0

omega_b = 0.02237
omega_g = 2.4728e-5
omega_n = 1.6918e-5
omega_r_fixed = omega_g + omega_n

SPIN_RAD_RATIO = 0.093
TAU_TOR = 0.9975
Z_STAR = 1089.90
Z_DRAG = 1059.94
Z_TRANS = 5600.0
z_bao = 1.48
w0, wa = -0.904, -0.153   # calibrated ECF values (PIT/Foundation II)

TARGET_BAO, SIG_BAO = 30.21, 0.79
TARGET_AGE, SIG_AGE = 13.32, 0.08
TARGET_THETA_SELFCONSISTENT = 1.03116   # this model's own LCDM value (see joint_fit_trilemma.py)
Gyr_conv = 977.79222168


def observables(omega_c):
    omega_m = omega_b + omega_c
    h2 = h_ecf**2
    Om_m = omega_m/h2
    Om_r = omega_r_fixed/h2
    Om_L = 1.0 - (Om_m+Om_r)
    Om_spin_0 = SPIN_RAD_RATIO*Om_r/(1+Z_TRANS)**2

    def de_evol(z):
        return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))
    def Hz(z):
        E2 = Om_r*(1+z)**4+Om_m*(1+z)**3+Om_spin_0*(1+z)**6+Om_L*de_evol(z)
        return 100.0*h_ecf*np.sqrt(E2)
    def cs(z):
        Rb = (3.0*omega_b)/(4.0*omega_g)/(1+z)
        return c_light/np.sqrt(3.0*(1+Rb))

    rs_drag,_ = integrate.quad(lambda z: TAU_TOR*cs(z)/Hz(z), Z_DRAG, 2e5, limit=100)
    rs_star,_ = integrate.quad(lambda z: TAU_TOR*cs(z)/Hz(z), Z_STAR, 2e5, limit=100)
    D_M_bao,_ = integrate.quad(lambda z: c_light/Hz(z), 0, z_bao, limit=100)
    D_M_star,_ = integrate.quad(lambda z: c_light/Hz(z), 0, Z_STAR, limit=150)
    age_int,_ = integrate.quad(lambda z: 1.0/((1+z)*Hz(z)/H0), 0, 3000, limit=150)

    return dict(Om_m=Om_m, omega_m=omega_m,
                bao_ratio=D_M_bao/rs_drag,
                theta100=100.0*rs_star/D_M_star,
                age=age_int*Gyr_conv/H0)


if __name__ == "__main__":
    omega_c_arr = np.linspace(0.02, 0.16, 60)
    Om_m_arr, age_arr, bao_arr, theta_arr = [], [], [], []
    for oc in omega_c_arr:
        o = observables(oc)
        Om_m_arr.append(o['Om_m']); age_arr.append(o['age'])
        bao_arr.append(o['bao_ratio']); theta_arr.append(o['theta100'])
    Om_m_arr = np.array(Om_m_arr)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)

    ax = axes[0]
    ax.plot(Om_m_arr, age_arr, '-', color='crimson', lw=2.2)
    ax.axhline(TARGET_AGE, color='gray', ls='--', lw=1)
    ax.axhspan(TARGET_AGE-SIG_AGE, TARGET_AGE+SIG_AGE, color='gray', alpha=0.2)
    ax.axvline(0.315, color='steelblue', ls=':', lw=1.3, label=r'$\Omega_m$ at Planck-$h$ (0.315)')
    ax.axvline(0.268, color='darkorange', ls=':', lw=1.3, label=r'$\Omega_m$ corrected ($H_0$=73.04, 0.268)')
    ax.set_xlabel(r'$\Omega_m$'); ax.set_ylabel(r'$t_0$ [Gyr]')
    ax.set_title('Age vs $\\Omega_m$\n(target: Valcin+2021)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)

    ax = axes[1]
    ax.plot(Om_m_arr, bao_arr, '-', color='#2c7a2c', lw=2.2)
    ax.axhline(TARGET_BAO, color='gray', ls='--', lw=1)
    ax.axhspan(TARGET_BAO-1.5*SIG_BAO, TARGET_BAO+1.5*SIG_BAO, color='gray', alpha=0.2, label='1.5% tolerance')
    ax.axvline(0.315, color='steelblue', ls=':', lw=1.3)
    ax.axvline(0.268, color='darkorange', ls=':', lw=1.3)
    ax.set_xlabel(r'$\Omega_m$'); ax.set_ylabel(r'$D_M(z=1.48)/r_s$')
    ax.set_title('BAO vs $\\Omega_m$\n(target: Hou+2021 eBOSS DR16)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)

    ax = axes[2]
    ax.plot(Om_m_arr, theta_arr, '-', color='#7a1a7a', lw=2.2)
    ax.axhline(TARGET_THETA_SELFCONSISTENT, color='gray', ls='--', lw=1,
               label=r'self-consistent $\Lambda$CDM target (this model)')
    ax.axvline(0.315, color='steelblue', ls=':', lw=1.3)
    ax.axvline(0.268, color='darkorange', ls=':', lw=1.3)
    ax.set_xlabel(r'$\Omega_m$'); ax.set_ylabel(r'$100\,\theta_*$')
    ax.set_title(r'CMB acoustic scale vs $\Omega_m$' + '\n(~1% systematic bias, see text)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)

    fig.suptitle(r'The $H_0$-Age-BAO-$\theta_*$ quadrilemma: the three observables pull '
                 r'$\Omega_m$ in mutually incompatible directions' + '\n' +
                 r'(at fixed calibrated $(w_0,w_a)=(-0.904,-0.153)$, $H_0=73.04$)', fontsize=11)
    plt.savefig('fig_quadrilemma_omega_m.png', dpi=200, bbox_inches='tight', facecolor='white')
    print("Figure saved: fig_quadrilemma_omega_m.png")
