"""
plot_structure_zoom.py
Author: Pascal Fichant (2026)

Late-time cosmic chronology: structure formation and dark energy onset.
Compares scale factor a(t) and CMB temperature T(t) for LCDM and ECF.

Key ECF signature: t0 = 12.74 Gyr vs LCDM t0 = 13.81 Gyr,
arising from the H0-Age-BAO trilemma (F1 extended v2, Sec. 5, Tab. 2).

The primordial stiff phase a~t^(1/3) is not visible on this timescale
(t_bounce ~ 1e-35 s); see plot_Cosmic_History_Omegas.py for full history.

Pivot redshifts calibrated via matter-dominated Friedmann:
    t(z) = t0 / (1+z)^(3/2)

Physical inputs:
    T0_CMB  = 2.725 K              (Planck 2018)
    t_eq    = 1.48e12 s            (z_eq ~ 3500, Planck 2018)
    t0_LCDM = 4.358e17 s = 13.81 Gyr
    t0_ECF  = 4.020e17 s = 12.74 Gyr  (F1 extended v2, Tab. 2)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter

# --- Physical parameters ---
T0_CMB  = 2.725        # K, CMB temperature today (Planck 2018)
t_eq    = 1.48e12      # s, matter-radiation equality (Planck 2018, z_eq ~ 3500)
t0_LCDM = 4.358e17     # s, 13.81 Gyr
t0_ECF  = 4.020e17     # s, 12.74 Gyr (H0-Age-BAO trilemma, Tab. 2)

def get_a(t_arr, t0):
    """
    Piecewise scale factor: radiation era a~t^0.5 (t < t_eq),
    matter era a~t^(2/3) (t > t_eq), normalised to a=1 at t0.
    """
    a = np.where(t_arr < t_eq, (t_arr / t_eq)**0.5, (t_arr / t_eq)**(2/3))
    return a / (t0 / t_eq)**(2/3)

def t_of_z(z, t0=t0_LCDM):
    """Matter-dominated: t(z) = t0 / (1+z)^1.5."""
    return t0 / (1 + z)**1.5

# --- Time grid ---
time = np.logspace(np.log10(8e12), np.log10(6e17), 1200)

a_lcdm = get_a(time, t0_LCDM)
a_ecf  = get_a(time, t0_ECF)
T_lcdm = T0_CMB / a_lcdm
T_ecf  = T0_CMB / a_ecf

# --- Cosmic eras ---
eras = [
    {'name': 'Dark Ages',           'start': 8e12,       'end': t_of_z(20), 'color': 'limegreen',  'alpha': 0.22},
    {'name': 'Structure Formation', 'start': t_of_z(20), 'end': 2.5e17,     'color': 'darkorange', 'alpha': 0.28},
    {'name': 'Dark Energy Era',     'start': 2.5e17,     'end': 6e17,       'color': 'salmon',     'alpha': 0.25},
]

# --- Calibrated pivot lines ---
pivots = {
    r'Recombination ($z=1100$)':   t_of_z(1100),
    r'Cosmic Dawn ($z\sim20$)':    t_of_z(20),
    r'Galaxy Assembly ($z\sim3$)': t_of_z(3),
}

# --- Redshift axis ticks (calibrated) ---
t_ticks = [t_of_z(1100), t_of_z(150), t_of_z(20), t_of_z(3), t0_LCDM]
z_labels = ['1100', '150', '20', '3', '0']

# --- Figure ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
fig.suptitle(
    'Cosmic Structure Formation & Dark Energy Onset — ECF vs. $\\Lambda$CDM',
    fontsize=14, fontweight='bold', y=0.97
)

for ax in (ax1, ax2):
    for era in eras:
        ax.axvspan(era['start'], era['end'], color=era['color'], alpha=era['alpha'], zorder=0)

for era in eras:
    mid = np.sqrt(era['start'] * era['end'])
    ax1.text(mid, 3e-3, era['name'], ha='center', va='bottom',
             fontsize=11, fontweight='bold', color='darkslategray')

ax1.loglog(time, a_lcdm, color='royalblue', ls='--', lw=2.5, alpha=0.75,
           label=r'Standard $\Lambda$CDM ($t_0=13.81\,\mathrm{Gyr}$)')
ax1.loglog(time, a_ecf,  color='crimson',   ls='-',  lw=2.0,
           label=r'ECF ($t_0=12.74\,\mathrm{Gyr},\;H_0=73.0\,\mathrm{km\,s^{-1}\,Mpc^{-1}}$)')

ax2.loglog(time, T_lcdm, color='royalblue', ls='--', lw=2.5, alpha=0.75)
ax2.loglog(time, T_ecf,  color='crimson',   ls='-',  lw=2.0)

for name, tp in pivots.items():
    for ax in (ax1, ax2):
        ax.axvline(tp, color='black', lw=1.2, ls=':', alpha=0.6, zorder=2)
    ax1.text(tp * 1.12, 6e-3, name, rotation=90, va='bottom',
             fontsize=9.5, fontweight='bold', color='#2c2c2c')

ax1.axvline(t0_LCDM, color='royalblue', lw=1.0, ls=':', alpha=0.7)
ax1.axvline(t0_ECF,  color='crimson',   lw=1.0, ls=':', alpha=0.7)
ax1.text(t0_LCDM * 1.02, 3e-1, r'$t_0^{\Lambda\rm CDM}$',
         color='royalblue', fontsize=9, va='top', rotation=90)
ax1.text(t0_ECF  * 0.97, 3e-1, r'$t_0^{\rm ECF}$',
         color='crimson',   fontsize=9, va='top', ha='right', rotation=90)

secax = ax1.secondary_xaxis('top')
secax.set_xticks(t_ticks)
secax.xaxis.set_major_formatter(FixedFormatter(z_labels))
secax.set_xlabel(r'Redshift $z$', fontsize=11, fontweight='bold',
                 color='darkred', labelpad=8)
for lbl in secax.get_xticklabels():
    lbl.set_fontweight('bold')
    lbl.set_color('darkred')

ax1.set_ylabel(r'Scale Factor $a(t)$', fontsize=11)
ax2.set_ylabel(r'CMB Temperature $T(t)$ [K]', fontsize=11)
ax2.set_xlabel(r'Cosmic Time $t$ [seconds]', fontsize=11)
ax1.set_xlim(8e12, 6e17)
ax1.set_ylim(1e-4, 3)
ax2.set_ylim(0.7, 1.5e4)
ax1.legend(loc='lower right', fontsize=9.5, framealpha=0.95)
for ax in (ax1, ax2):
    ax.grid(True, which='both', ls=':', alpha=0.35)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('Figure_Structure_Zoom.png', dpi=300, bbox_inches='tight')
plt.close()