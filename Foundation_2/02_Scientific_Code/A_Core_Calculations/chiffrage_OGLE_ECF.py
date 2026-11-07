"""15/10/2026 — Chiffrage : halo ECF (agrégats M_typ = 6,8e-5 Msun, f = 1) contre OGLE-IV 2010-2015 vers le bulbe.
Trois estimations indépendantes, ordre de grandeur. Sources :
 Mróz et al. 2017 (Nature 548, 183 ; arXiv:1707.07634) : 2617 événements, ~5e7 étoiles, 6 événements ultracourts (t_E < 0,5 j) ;
   « 5 M_Terre, 5 par étoile de la séquence principale -> 2,2 événements ultracourts attendus » (efficacité incluse).
 Niikura et al. 2019 (PRD 99, 083503 ; arXiv:1901.07120) : meilleure borne sur 1e-6..1e-3 Msun ; point limite cité (6,9e-5 Msun ; f = 0,014).
 F2 : tau_ECF = 5e-8 (repère) à 1,5e-7 (pseudo-isotherme) ; t_E^typ = 6,3 h. Fond mesuré tau_star ~ 1,6e-6."""
import numpy as np
Msun=1.0; MT=3.0035e-6  # masse terrestre en Msun
tau_star=1.6e-6
for tau_ecf in (5e-8,1.5e-7):
    r_tau=tau_ecf/tau_star
    print(f"\n=== tau_ECF = {tau_ecf:.1e}  (tau_ECF/tau_star = {r_tau:.3f})")
    # (1) Calibration Mróz 2017 : population 5 M_T, 5 par étoile SP -> 2,2 événements (avec efficacité)
    M_ref=5*MT; rho_ref=5*M_ref            # Msun par étoile SP
    M_ecf=6.8e-5
    for Mbar in (0.3,0.5,0.8):              # masse des lentilles stellaires par étoile SP (incertaine)
        rho_ecf=r_tau*Mbar                  # même pondération géométrique supposée (approximation)
        N=2.2*(rho_ecf/rho_ref)*np.sqrt(M_ref/M_ecf)   # N ∝ n sqrt(M) = rho/sqrt(M) ; efficacité : prise égale (prudent, t_E ECF plus long)
        print(f"  (1) Mróz-calibré, Mbar={Mbar}: N_ECF ≈ {N:.0f}  (observés : 6)")
    # (2) Rapport de taux ECF/stellaire x efficacité relative
    tE_star=22.0; tE_ecf=6.3/24
    ratio=r_tau*tE_star/tE_ecf
    for eps in (0.03,0.1,0.3):
        print(f"  (2) taux ECF/stellaire = {ratio:.1f} ; efficacité relative {eps}: N_ECF ≈ {2617*ratio*eps:.0f}")
# (3) Niikura 2019 : à 6,9e-5 Msun, f = 0,014 correspond au plus à ~6 événements -> f = 1 : ~6/0,014
print(f"\n(3) Niikura-échelle : f=1 à 6,9e-5 Msun -> ≈ {6/0.014:.0f} événements (contre 6 observés, dont certains possiblement des étoiles éruptives)")
