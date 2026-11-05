"""
================================================================================
SCRIPT : Global Cosmic History (Scale Factor and Temperature)
Paper  : Foundation I -- Extended Version
Author : Pascal Fichant (2026)
Description :
    Two-panel log-log plot of a(t) and T(t) from pre-bounce to dark energy era.
    ECF bounce at t~1e-44 s (rho = rho_c, F2 Cartan time threshold; a_bounce~1e-32, App. D). [07/10/2026: was 1e-41 s, withdrawn in F2]
    t_eq = 1.609e12 s (z_eq = 3402, matter-radiation equality computed from omega_m = 0.14237 and omega_r = 4.1837e-5; [02/10/2026] was 1.24e12 s, which does not correspond to a_eq = 2.86e-4).
    t0(ECF) = 13.33 Gyr (F1 §5, Omega_m = omega_m/h^2 = 0.267, A-7; was 12.74 at Omega_m = 0.315) [02/10/2026]; t0(ΛCDM) = 13.81 Gyr (Planck 2018).
================================================================================
"""
# Last modified: 07/10/2026, 19:59 (Paris time)
# Corpus: Foundation I — github.com/pfichant/spin-torsion-cosmology
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter

T0           = 2.725
t_bounce     = 1.0e-44   # s [07/10/2026: was 1.0e-41]
t_eq         = 1.609e12   # s, z_eq = 3402 [02/10/2026: was 1.24e12 -> z = 3926]
t_today_ecf  = 4.206e17   # s = 13.327 Gyr x 3.156e7 s/yr (script_09; was 4.020e17 = 12.74 Gyr)
t_today_lcdm = 4.355e17

def get_a_evolution(t_arr, model='ECF'):
    if model == 'LCDM':
        a = np.where(t_arr < t_eq,
                     (t_arr / t_eq)**0.5,
                     (t_arr / t_eq)**(2/3))
        a_today = (t_today_lcdm / t_eq)**(2/3)
    else:
        a = np.where(t_arr < t_bounce,
                (t_arr / t_bounce)**(1/3),
            np.where(t_arr < t_eq,
                (t_arr / t_bounce)**0.5,
                ((t_eq / t_bounce)**0.5) * (t_arr / t_eq)**(2/3)))
        a_today = ((t_eq / t_bounce)**0.5) * (t_today_ecf / t_eq)**(2/3)
    return a / a_today

time_full = np.logspace(-46, 18.5, 1200)
a_l = get_a_evolution(time_full, 'LCDM')
a_e = get_a_evolution(time_full, 'ECF')
temp_l = T0 / a_l
temp_e = T0 / a_e

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
fig.suptitle('Global Cosmic History: From Big Bounce to Dark Energy Era',
             fontsize=15, fontweight='bold', y=0.97)

eras = [
    {'name': 'Spin-Torsion', 'start': 1e-46,    'end': t_bounce, 'color': 'mediumorchid', 'alpha': 0.40},
    {'name': 'Radiation',    'start': t_bounce,  'end': t_eq,     'color': 'dodgerblue',   'alpha': 0.25},
    {'name': 'Matter',       'start': t_eq,      'end': 3e17,     'color': 'limegreen',    'alpha': 0.18},
    {'name': 'Dark Energy',  'start': 3e17,      'end': 3e18,     'color': 'salmon',       'alpha': 0.28},
]
for era in eras:
    for ax in (ax1, ax2):
        ax.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'])
    mid = np.sqrt(era['start'] * era['end'])
    ax1.text(mid, 5e-33, era['name'], rotation=90, ha='center', va='bottom',
             fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.7, ec='none'))

ax1.loglog(time_full, a_l, color='blue', linestyle='--', linewidth=3.5,
           alpha=0.55, label=r'Standard $\Lambda$CDM ($t_0=13.81\,$Gyr)')
ax1.loglog(time_full, a_e, color='red',  linestyle='-',  linewidth=2.5,
           label=r'ECF Model ($t_0=13.33\,$Gyr)')
ax2.loglog(time_full, temp_l, color='blue', linestyle='--', linewidth=3.5, alpha=0.55)
ax2.loglog(time_full, temp_e, color='red',  linestyle='-',  linewidth=2.5)

secax1 = ax1.secondary_xaxis('top')
t_ticks  = [t_bounce, 1e-21, 1e-7, t_eq, 3e15, t_today_ecf]
z_labels = [r'$z_{\rm bounce}$', r'$10^{19}$', r'$10^{9}$', '3400', '30', '0']
secax1.set_xticks(t_ticks)
secax1.xaxis.set_major_formatter(FixedFormatter(z_labels))
for lbl in secax1.get_xticklabels():
    lbl.set_fontweight('bold')
    lbl.set_color('darkred')
    lbl.set_fontsize(9)
secax1.set_xlabel(r'Redshift $z$', fontsize=12, fontweight='bold',
                  color='darkred', labelpad=10)

ax1.set_ylabel(r'Scale Factor $a(t)$', fontsize=12)
ax2.set_ylabel(r'Temperature $T(t)$ [K]', fontsize=12)
ax2.set_xlabel(r'Cosmic Time $t$ [seconds]', fontsize=12)
ax1.set_ylim(1e-35, 10)
ax2.set_ylim(1e-2, 1e35)
ax1.legend(loc='upper left', fontsize=11, framealpha=0.97)
ax1.grid(True, which='both', ls=':', alpha=0.3)
ax2.grid(True, which='both', ls=':', alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('Figure_global_history.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: Figure_global_history.png")
