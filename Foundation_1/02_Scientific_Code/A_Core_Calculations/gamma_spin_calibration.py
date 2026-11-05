#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gamma_spin_calibration.py — producteur de γ_spin et de son incertitude (audit v2, 22/09/2026)

Relation (forme divisive de F1, script_06) :  S8_ECF = S8_LCDM / (1 + (F_ion − 1) γ_spin)
  ⇒  γ_spin = (S8_LCDM / S8_obs − 1) / (F_ion − 1)

γ_spin est CALIBRÉ : il est fixé de sorte que S8_ECF = S8_obs. Ce n'est pas une prédiction.

Entrées :
  S8_obs  = 0,766 (+0,020 / −0,014) — KiDS-1000 3×2pt, Heymans et al. 2021, A&A 646, A140, arXiv:2007.15632
            (lentillage KiDS-1000 + clustering BOSS + lentillage galaxie-galaxie 2dFLenS), vérifié à la source le 22/09.
  S8_LCDM = 0,832 — valeur du corpus (script_06 l. 54). Incertitude NON propagée par défaut, car la valeur n'est pas relue à la source
            dans le corpus ; option --avec-s8lcdm SIGMA pour l'ajouter (quadratiquement, symétrique).
  F_ion   = 1,2765 — calibré en amont (F1) ; incertitude non propagée ici.

Méthode : incertitude asymétrique par inversion des bornes 1σ de S8_obs (la relation est monotone décroissante :
S8_obs − σ₋ donne la borne haute de γ, S8_obs + σ₊ la borne basse).
Comparaison (non canonique) : DES Y3 3×2pt 0,776 ± 0,017 (arXiv:2105.13549) ; DES Y3 + KiDS-1000 0,790 (+0,018/−0,014)
(arXiv:2305.17173) — une recalibration sur l'une d'elles serait une NOUVELLE calibration (rerun S8, fσ8, P(k)).
"""
import argparse, json

S8_LCDM, F_ION = 0.832, 1.2765
MESURES = {
    "KiDS-1000 3x2pt (Heymans+2021) [CANONIQUE]": (0.766, 0.020, 0.014),
    "DES Y3 3x2pt (Abbott+2022) [comparaison]": (0.776, 0.017, 0.017),
    "DES Y3 + KiDS-1000 cosmic shear (2023) [comparaison]": (0.790, 0.018, 0.014),
}


def gamma(s8obs, s8l=S8_LCDM, f=F_ION):
    return (s8l / s8obs - 1.0) / (f - 1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--avec-s8lcdm", type=float, default=None, help="σ de S8_LCDM à propager (ex. 0.013, à sourcer)")
    a = ap.parse_args()
    out = {}
    for nom, (s, sp, sm) in MESURES.items():
        g = gamma(s)
        up, dn = gamma(s - sm) - g, g - gamma(s + sp)
        if a.avec_s8lcdm:
            dl = a.avec_s8lcdm / (s * (F_ION - 1.0))
            up, dn = (up ** 2 + dl ** 2) ** 0.5, (dn ** 2 + dl ** 2) ** 0.5
        out[nom] = dict(S8_obs=s, gamma=round(g, 4), plus=round(up, 3), moins=round(dn, 3))
        print(f"{nom:52s} S8={s:.3f}  γ_spin = {g:.4f}  (+{up:.3f} / −{dn:.3f})")
    s8_back = S8_LCDM / (1 + (F_ION - 1) * 0.3116)
    print(f"\nContrôle : γ = 0,3116 redonne S8_ECF = {s8_back:.4f} (inversion exacte : γ = {gamma(0.766):.6f})")
    print("Propagé : incertitude de S8_obs seule" + (f" + σ(S8_LCDM) = {a.avec_s8lcdm}" if a.avec_s8lcdm else "") +
          " ; F_ion et S8_LCDM tenus fixes sinon.")
    json.dump(out, open("gamma_spin_sortie.json", "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
