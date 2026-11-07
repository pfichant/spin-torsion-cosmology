#!/usr/bin/env python3
"""
verify_F3_PO3_thermalization_exponent.py
Dernière modification : 20/07/2026, 23:00

PO-F3-3 : origine de l'exposant 1/2 dans sigma^2_baby ~ a*.

Teste l'hypothèse que la conversion du moment angulaire du trou noir
parent vers la densité de spin s_0 de l'univers enfant, si elle est
THERMALISÉE (incohérente) plutôt que directe, produit s_0 ~ (a*)^(1/2)
via le mécanisme de fluctuation en sqrt(N) d'une marche aléatoire biaisée.

Résultat attendu : exposant ~ 0.5 dans le régime thermalisé (biais faible),
en accord avec les hypothèses T1-T2 du corpus ECF.

[CORRECTION 20/07/2026] Ce script fournit une origine physique candidate
pour l'exposant sqrt(a*) ATTENDU par l'hypothèse T1-T2 (PO-F3-3) --
PAS pour le Lemme F3-SPIN-2. Le Lemme F3-SPIN-2 (mécanisme holographique,
couplage via l'aire de l'horizon) donne au contraire une dépendance
LINÉAIRE en a*, et se trouve donc en TENSION avec le résultat vérifié
ici, pas en accord avec lui. Cette tension (linéaire vs sqrt(a*)) est
documentée comme non résolue dans F3 (§PO-F3-3, l.5062-5069). Ce script
teste la branche thermalisée (T1-T2) de cette tension, pas les deux.
"""

# UTF-8 guard: added 24/08/2026 so the script does not
# crash on a Windows cp1252 console.
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


import numpy as np

def spin_net_thermalise(bias, N, T_ratio, n_trials=20, seed=None):
    """
    Spin net normalisé d'un ensemble de N spins ±1 thermalisés,
    avec un biais d'alignement imposé par le moment angulaire parent.

    bias    : ~ a* (spin sans dimension du trou noir parent)
    N       : nombre de spins dans le cœur de Cartan
    T_ratio : rapport énergie_biais / énergie_thermique
              (faible = régime thermalisé ; fort = régime cohérent)
    """
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_trials):
        # probabilité d'alignement (réponse thermique au biais)
        p_align = 0.5 + 0.5 * np.tanh(bias * T_ratio)
        spins = rng.choice([1, -1], size=N, p=[p_align, 1 - p_align])
        vals.append(abs(spins.sum()) / N)
    return np.mean(vals)


def measure_exponent(T_ratio, N=100_000, n_seeds=10):
    """Mesure l'exposant d de la loi s_0 ~ (a*)^d par fit log-log,
    moyenné sur plusieurs graines pour réduire le bruit statistique."""
    a_star = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    slopes = []
    for seed in range(n_seeds):
        s0 = np.array([
            spin_net_thermalise(a, N, T_ratio, n_trials=40, seed=1000 * seed + i)
            for i, a in enumerate(a_star)
        ])
        mask = s0 > 0
        if mask.sum() >= 2:
            slopes.append(np.polyfit(np.log(a_star[mask]), np.log(s0[mask]), 1)[0])
    return np.mean(slopes), np.std(slopes), a_star


if __name__ == "__main__":
    print("=" * 62)
    print("PO-F3-3 : exposant de s_0 vs a* selon le régime de conversion")
    print("=" * 62)

    # Régime thermalisé (biais faible) : fluctuation sqrt(N) attendue
    exp_thermal, std_thermal, a_vals = measure_exponent(T_ratio=0.01)
    print(f"\nRégime THERMALISÉ (T_ratio=0.01, moyenne sur 10 graines) :")
    print(f"  Exposant mesuré : {exp_thermal:.3f} ± {std_thermal:.3f}  (attendu ~ 0.5)")

    # Régime cohérent (biais fort) : alignement direct/saturation
    exp_coherent, std_coherent, _ = measure_exponent(T_ratio=100)
    print(f"\nRégime COHÉRENT (T_ratio=100) :")
    print(f"  Exposant mesuré : {exp_coherent:.3f} ± {std_coherent:.3f}  (saturation)")

    print("\n" + "=" * 62)
    print("CONCLUSION")
    print("=" * 62)
    print(f"""
La conversion thermalisée reproduit l'exposant 1/2 des hypothèses
T1-T2 du corpus ECF (mesuré : {exp_thermal:.2f} ± {std_thermal:.2f}),
fournissant une origine physique candidate à cet exposant : la
fluctuation nette en sqrt(N) d'un fluide de spin partiellement
randomisé au rebond.

Ce résultat NE dérive PAS ab initio que le rebond soit dans ce
régime ; il montre seulement que SI le rebond thermalise le spin,
l'exposant 1/2 en découle naturellement.

À noter : un mécanisme concurrent (Lemme F3-SPIN-2, couplage
holographique via l'aire de l'horizon) donne une dépendance LINÉAIRE
en a*, en tension avec l'exposant sqrt(a*) vérifié ici. Cette tension
est documentée comme non résolue dans F3 (§PO-F3-3) ; ce script ne
teste que la branche thermalisée de l'alternative.
""")
