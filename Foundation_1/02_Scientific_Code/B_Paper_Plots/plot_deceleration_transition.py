"""
plot_deceleration_transition.py (02/10/2026, Corpus) -- promoted 07/10/2026.
Deceleration parameter q(z): LCDM reference (Planck, Omega_m = 0.315) vs ECF background w = -1 with A-7 values:
  h_ECF = 0.7304, Omega_m = omega_m/h^2 = 0.2669, Omega_r = 7.84e-5, Omega_spin,0 = 2.325e-13 (rho_spin/rho_rad = 0.093 at z = 5600).
  q(z) = [Omega_r(1+z)^4 + Omega_m(1+z)^3/2 - Omega_L + 2 Omega_spin(1+z)^6] / E^2, flat, w = -1.
Result: z_t(ECF) = 0.764 (analytical (2 Omega_L/Omega_m)^(1/3)-1 = 0.765), z_t(LCDM) = 0.632.
The former version drew the ECF curve with LCDM's Omega_m = 0.315 and Omega_spin,0 = 1e-60 (pre-A-7 / pre-script_01 values).
1-sigma on z_t(ECF): Monte-Carlo on omega_b, omega_c (Planck 2018) and H0 = 73.04 +/- 1.04 (SH0ES), as for the Omega_tau/Omega_m figure.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq

def params_ecf():
    h = 0.7304
    Om = (0.02237 + 0.12) / h**2
    Or = 2.4728e-5 * (1 + (7/8) * (4/11)**(4/3) * 3.046) / h**2
    Os = 0.093 * Or / (1 + 5600)**2
    return Om, Or, Os

def q_of_z(z, Om, Or=0.0, Os=0.0):
    OL = 1 - Om - Or - Os
    E2 = Or*(1+z)**4 + Om*(1+z)**3 + OL + Os*(1+z)**6
    return (Or*(1+z)**4 + 0.5*Om*(1+z)**3 - OL + 2*Os*(1+z)**6) / E2

Om_e, Or_e, Os_e = params_ecf()
Om_l = 0.315
z = np.linspace(0, 2.5, 1000)
q_l = q_of_z(z, Om_l)
q_e = q_of_z(z, Om_e, Or_e, Os_e)
zt_l = brentq(lambda x: q_of_z(x, Om_l), 0, 3)
zt_e = brentq(lambda x: q_of_z(x, Om_e, Or_e, Os_e), 0, 3)
q0_l, q0_e = q_l[0], q_e[0]

rng = np.random.default_rng(20261002)
N = 200000
hh = rng.normal(0.7304, 0.0104, N); wb = rng.normal(0.02237, 0.00015, N); wc = rng.normal(0.12, 0.0012, N)
Om_s = (wb + wc) / hh**2
zt_s = (2*(1 - Om_s)/Om_s)**(1/3) - 1      # radiation/spin negligible at z ~ 0.8 (checked: 0.7639 vs 0.7646)
lo, hi = np.percentile(zt_s, [15.865, 84.135])
print(f"Omega_m(ECF)={Om_e:.4f}  Omega_r={Or_e:.3e}  Omega_spin0={Os_e:.3e}")
print(f"z_t ECF = {zt_e:.3f}  (analytical {(2*(1-Om_e)/Om_e)**(1/3)-1:.3f}); 68% interval [{lo:.3f}, {hi:.3f}]")
print(f"z_t LCDM(0.315) = {zt_l:.3f};  q0: ECF {q0_e:.3f}  LCDM {q0_l:.3f}")

plt.rcParams.update({'font.family': 'serif', 'font.size': 12, 'axes.linewidth': 1.2})
fig, ax = plt.subplots(figsize=(9, 6))
fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.13)
ax.fill_between(z, 0, 1, color='#d8d8d8', alpha=0.35, zorder=0)
ax.fill_between(z, -1, 0, color='#b8d4f0', alpha=0.30, zorder=0)
ax.axhline(0, color='black', ls=':', lw=1.0, zorder=1)
ax.plot(z, q_l, color='steelblue', ls='--', lw=2.2, zorder=3, label=r'$\Lambda$CDM  ($\Omega_m=0.315$)')
ax.plot(z, q_e, color='#C00000', ls='-', lw=2.8, zorder=2,
        label=rf'ECF, $w=-1$  ($\Omega_m=\omega_m/h^2={Om_e:.3f}$)')
ax.axvspan(lo, hi, color='#C00000', alpha=0.15, lw=0, zorder=1)
ax.scatter([zt_l], [0], color='steelblue', s=50, zorder=5)
ax.scatter([zt_e], [0], color='#C00000', s=50, zorder=5)
ax.annotate(rf'$z_t^{{\Lambda{{\rm CDM}}}} = {zt_l:.2f}$', xy=(zt_l, 0), xytext=(zt_l - 0.55, 0.45),
            arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.1), fontsize=11, color='steelblue')
ax.annotate(rf'$z_t^{{\rm ECF}} = {zt_e:.2f}\pm{(hi-lo)/2:.2f}$', xy=(zt_e, 0), xytext=(zt_e + 0.25, 0.32),
            arrowprops=dict(arrowstyle='->', color='#C00000', lw=1.1), fontsize=11, fontweight='bold', color='#C00000')
ax.text(0.18, 0.80, r'Decelerating ($q>0$)', color='#444', fontsize=9.5)
ax.text(0.18, -0.85, r'Accelerating ($q<0$)', color='#1a5999', fontsize=9.5)
ax.text(1.40, -0.62, r'$q(z)=\Omega_r+\frac{1}{2}\Omega_m-\Omega_\Lambda+2\Omega_{\rm spin}$',
        fontsize=11, color='#222', va='center', bbox=dict(facecolor='white', edgecolor='#777', boxstyle='round,pad=0.38', alpha=0.95))
ax.set_xlabel(r'Redshift $z$', fontsize=13)
ax.set_ylabel(r'Deceleration parameter $q(z)$', fontsize=13)
ax.set_xlim(0, 2.5); ax.set_ylim(-1.0, 1.0)
ax.grid(True, ls=':', alpha=0.30, color='gray'); ax.tick_params(labelsize=11)
ax.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax.set_title('Cosmic deceleration--acceleration transition', fontsize=13)
plt.savefig('figure_deceleration_transition.png', dpi=300, bbox_inches='tight')
print("Saved figure_deceleration_transition.png")
