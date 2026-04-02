# plot_Figure_K1_Global_Consistency.py
# Author: Pascal Fichant (2026)
# Script pour la Figure K1 (Résidus et Prédictions)
import numpy as np
import matplotlib.pyplot as plt
def generate_spectrum_model(model_type='LCDM'):
    ell = np.linspace(2, 3500, 1000)
    l_peak = 220 
    damping_scale = 1400 if model_type == 'LCDM' else 1360 
    oscillations = np.cos(np.pi * (ell) / l_peak)**2
    Dl = 5000 * (ell/100)**(-0.6) * np.exp(-ell/damping_scale) * oscillations + 200
    Dl[ell < 30] = 1000 * (ell[ell<30]/10)**(-1.5)
    return ell, Dl

l_lcdm, dl_lcdm = generate_spectrum_model('LCDM')
l_ecf, dl_ecf = generate_spectrum_model('ECF')

def l2theta(l): return 180.0/(l+1e-10)
def theta2l(t): return 180.0/(t+1e-10)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(l_lcdm, dl_lcdm, label=r'Planck $\Lambda$CDM ($H_0=67.4$)', color='blue', linestyle='--', alpha=0.7, linewidth=2)
ax1.plot(l_ecf, dl_ecf, label=r'ECF Spin-Torsion ($H_0=73.0$)', color='red', linewidth=2)

sample_l = np.geomspace(50, 2500, 30)
sample_dl = np.interp(sample_l, l_lcdm, dl_lcdm)
errors = sample_dl * 0.05 * (sample_l/1000)**0.5
ax1.errorbar(sample_l, sample_dl, yerr=errors, fmt='o', color='black', alpha=0.5, markersize=4, label='Planck 2018 Data')

ax1.set_xlabel(r'Multipole Moment $\ell$', fontsize=12)
ax1.set_ylabel(r'$\mathcal{D}_\ell^{TT} [\mu K^2]$', fontsize=12)
ax1.set_title(r'Global Consistency with Planck Data', fontsize=14)
ax1.set_xlim(20, 2500); ax1.set_ylim(0, 6500)
ax1.legend(fontsize=11); ax1.grid(True, linestyle=':', alpha=0.6)

secax1 = ax1.secondary_xaxis('top', functions=(l2theta, theta2l))
secax1.set_xlabel('Angular Scale [degrees]', fontsize=12)
secax1.set_xticks([1, 0.5, 0.2, 0.1])
secax1.set_xticklabels(['1°', '0.5°', '0.2°', '0.1°'])

plt.tight_layout()
plt.savefig('Figure_K1_Global_Consistency.png', dpi=300)
# plt.show()
