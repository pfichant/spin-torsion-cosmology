# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 1. PARAMÈTRES DE TEMPS
# Range extended from 10^-44 s to 10^12 s (about 30,000 years)
# ---------------------------------------------------
t_log = np.linspace(-47, 12, 2000)  # [08/10/2026: was -44, Cartan time moved to 1e-44 s]
t = 10**t_log

# ---------------------------------------------------
# 2. VITESSE MODÈLE STANDARD (Lambda-CDM + Inflaton)
# ---------------------------------------------------
v_standard = np.zeros_like(t)

t_start_inf = 10**-36
t_end_inf = 10**-32

v_max_std = 1e15 * np.exp(15) # Environ 3.2 * 10^21

for i, ti in enumerate(t):
    if ti < t_start_inf:
        v_standard[i] = 1e15 * (ti / t_start_inf)**(-0.5)
    elif ti <= t_end_inf:
        v_standard[i] = 1e15 * np.exp(15 * (ti - t_start_inf) / (t_end_inf - t_start_inf))
    else:
        v_standard[i] = v_max_std * (ti / t_end_inf)**(-0.5)

# ---------------------------------------------------
# 3. VITESSE MODÈLE ECF (Big Spin Bounce)
# ---------------------------------------------------
v_ecf = np.zeros_like(t)
t_cartan = 10**-44  # [08/10/2026: was 1e-41 s, withdrawn in F2 (rho = rho_c at ~1e-44 s)]

for i, ti in enumerate(t):
    if ti < t_cartan:
        v_ecf[i] = 1e30 * (ti / t_cartan)**2
    else:
        # Phase Stiff Era (w=1) -> a ~ t^(1/3) -> v ~ t^(-2/3)
        v_ecf[i] = 1e30 * (ti / t_cartan)**(-2/3)

# ---------------------------------------------------
# 4. CRÉATION DU GRAPHIQUE
# ---------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

ax.plot(t, v_standard, label=r'Standard Inflation ($\dot{a}/c$)', color='blue', linestyle='--', linewidth=2.5)
ax.plot(t, v_ecf, label=r'ECF Natural Bounce ($\dot{a}/c$)', color='red', linewidth=3)

# Peak annotations
ax.scatter([t_cartan], [1e30], color='red', zorder=5)
ax.annotate('Maximum Expansion Velocity\n(Cartan Time: $\\sim10^{-44}$ s)', 
            xy=(t_cartan, 1e30), xytext=(t_cartan*10**1, 5e31),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
            fontsize=11, color='red', fontweight='bold')

ax.annotate('End of Standard Inflation', 
            xy=(t_end_inf, v_max_std), xytext=(10**-30, 1e24),
            arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5, headwidth=8),
            fontsize=11, color='blue', fontweight='bold')

# Speed-of-light line (c = 1)
ax.axhline(1, color='green', linewidth=1.5, linestyle=':', label='Speed of Light ($v = c$)')

# Annotations for the crossing below c (1)
t_cross_ecf = t_cartan * 10**45  # Temps de croisement ECF (v = 1 : (t/t_cartan)^(-2/3) = 1e-30) [08/10/2026: was 10**4 for t_cartan = 1e-41]
t_cross_std = 10**11 # Temps de croisement Standard

ax.scatter([t_cross_ecf], [1], color='red', zorder=5)
ax.annotate('ECF Drops Below $c$', 
            xy=(t_cross_ecf, 1), xytext=(10**-1, 1e-4),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, color='red')

ax.scatter([t_cross_std], [1], color='blue', zorder=5)
ax.annotate('Standard Drops Below $c$', 
            xy=(t_cross_std, 1), xytext=(10**7, 1e4),
            arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, color='blue')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(10**-47, 10**12)
ax.set_ylim(1e-6, 1e35)

ax.set_xlabel('Cosmic Time (Seconds after Singularity/Bounce)', fontsize=12, fontweight='bold')
ax.set_ylabel(r'Relative Expansion Velocity ($v/c$)', fontsize=12, fontweight='bold')
ax.set_title('Cosmic Expansion Velocity: ECF Model vs Standard Inflation', fontsize=14, fontweight='bold')

ax.grid(True, which="both", ls="--", alpha=0.3)
ax.legend(loc='lower left', fontsize=11)

plt.tight_layout()
plt.savefig('Fig_Inflation_Velocity_Extended.png')
print("Image étendue générée avec succès.")
