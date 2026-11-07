#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[02/10/2026] STATUS: EXPLORATORY DIAGNOSTIC, NOT USED IN ANY PAPER.
The background is a generic rounded one (Omega_m = 0.30, Omega_r = 9.2e-5), not the
A-7 ECF background. Audit of 02/10/2026: on the 8 x 5 grid below only the delta = 0
points (8 of 40) converge to the tolerance; the 32 points with delta != 0 diverge
(NaN / overflow). For eps > 0 the dark-energy density is NEGATIVE at early times.
The "best fit" does not reproduce the target (w0 = -1.0125 versus -0.904).
This script now reports non-convergence explicitly instead of skipping or printing it.

ECF_solver_JalonB_couplage.py
=============================
Projet CLASS-EC — Bloc 1, JALON B : le w(z) est-il DÉRIVABLE du couplage
non minimal torsion-courbure ?

ACTION (secteur pertinent, 8*pi*G = 1) :
    L = f(X) R  -  W(X)  -  (1/4) F^2 ,   f(X) = 1/2 - (xi/2) X ,  X = S_mu S^mu

POTENTIEL : forme STABLE (bumblebee / Einstein-aether), adoptée après
vérification que la forme quartique de F2, prise comme potentiel ordinaire,
donne un MAXIMUM (mode radial tachyonique) :
    W(X) = V_0 + (lambda/4) (X + b^2)^2     ->  min en X_0 = -b^2, W'' = lambda/2 > 0

ÉQUATION DU CHAMP (fond homogène, F=0) :
    2 W'(X) + xi R = 0     ->    W'(X_0) = -(xi/2) Rbar(a)
    (xi=0  =>  W'(X_0)=0 : VEV gelée, w=-1  -> on retrouve le verdict P0)
    forme stable  ->  X_0(a) = -b^2 - xi Rbar(a)/lambda

ÉQUATION DE FRIEDMANN (les termes en S_mu S_nu s'annulent ON-SHELL car
f' R - W' = -(xi/2)R + (xi/2)R = 0) :
    6 f H^2 + 6 H fdot - W = rho_m + rho_r
 => 3H^2 = rho_m + rho_r + rho_DE,  avec le T_mu_nu NON MINIMAL COMPLET :
    rho_DE = W(X_0) + 3 xi [ H^2 X_0 + H Xdot_0 ]
                        ^^^^^^^^^^^^^^^^^^^^^^^ termes dérivés (le "manque"
                        identifié à l'étape précédente)

PARAMÈTRES SANS DIMENSION :
    eps   = xi b^2                (force du couplage)
    delta = xi H0^2 / (lambda b^2)  (amplitude du décalage de VEV)
    r(a)  = Rbar(a)/H0^2 ,  u(a) = X_0/(-b^2) = 1 + delta*r(a)

    Omega_DE(a) = Omega_V0 + (eps*delta/12) r^2  -  eps E^2 u  -  eps a E^2 u'

Résolution AUTO-COHÉRENTE (r dépend de E qui dépend de Omega_DE qui dépend de r).

QUESTION DU JALON B : existe-t-il (eps, delta) tel que w(z) reproduise
(w0, wa) = (-0.904, -0.153) AVEC franchissement de -1 vers z ~ 1.7 ?
"""
# [AJOUTE 15/09/2026] Garde UTF-8. Sans lui, un print contenant un caractere
# non-ASCII (fleche, etoile, accent) fait planter le script sur une console
# Windows en cp1252 : UnicodeEncodeError, code de sortie 1. Quatre scripts F2
# ont echoue ainsi chez Pascal le 15/09 alors qu'ils tournaient sous Linux.
# [CORRIGE 15/09/2026] Le chemin de sortie etait « /mnt/user-data/outputs/ »,
# un chemin absolu de l'environnement ou le script a ete ecrit. Il ne peut
# exister sur aucune autre machine : FileNotFoundError garanti chez quiconque
# reproduit le corpus. Remplace par une sortie dans le dossier du script.

import os
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# [D3, 22/09/2026 -- DEC-A7-POST-05] Generic rounded background (Omega_m = 0.30,
# no H0), qualitative exploration of the coupling: NOT the A-7 ECF background
# (omega_m/h_ECF^2 = 0.267). Kept; to be aligned if a number from here is quoted.
Om, Orad = 0.30, 9.2e-5
W0_T, WA_T = -0.904, -0.153          # cible calibrée (Foundation I)

lna = np.linspace(np.log(1e-3), 0.0, 3000)
a   = np.exp(lna)

def d_dlna(y):
    return np.gradient(y, lna)

def solve_background(eps, delta, n_iter=200, tol=1e-12):
    """Résout E(a) et Omega_DE(a) de façon auto-cohérente."""
    OV = 1.0 - Om - Orad                       # départ : Lambda pur
    E2 = Om*a**-3 + Orad*a**-4 + OV
    converged = False
    for _ in range(n_iter):
        E  = np.sqrt(np.maximum(E2, 1e-300))
        # r = Rbar/H0^2 = 6 E (a E' + 2E) = 6 E (dE/dlna + 2E)
        r  = 6.0*E*(d_dlna(E) + 2.0*E)
        u  = 1.0 + delta*r
        du = delta*d_dlna(r)                   # a*u' = du/dlna
        extra = (eps*delta/12.0)*r**2 - eps*E2*u - eps*E2*du
        # normalisation : E(a=1) = 1
        OV_new = 1.0 - Om - Orad - extra[-1]
        ODE    = OV_new + extra
        E2_new = Om*a**-3 + Orad*a**-4 + ODE
        if np.max(np.abs(E2_new - E2)/np.maximum(E2,1e-30)) < tol:
            E2 = E2_new; converged = True; break
        E2 = 0.5*E2 + 0.5*E2_new               # sous-relaxation
    E   = np.sqrt(E2)
    ODE = E2 - Om*a**-3 - Orad*a**-4
    w   = -1.0 - d_dlna(ODE)/(3.0*ODE)
    # [02/10/2026] report convergence and finiteness over the WHOLE array
    ok = converged and bool(np.all(np.isfinite(E2)) and np.all(np.isfinite(w)))
    return E, ODE, w, ok

def diagnose(eps, delta):
    E, ODE, w, ok = solve_background(eps, delta)
    z  = 1.0/a - 1.0
    m  = (z < 3.0) & (z >= 0.0)                # fenêtre d'intérêt
    w0 = w[-1]
    # wa via CPL : w = w0 + wa(1-a)  -> pente locale autour de a=1
    sel = (z < 1.0)
    wa  = np.polyfit(1.0 - a[sel], w[sel] - w0, 1)[0]
    ww  = w[m]
    crossing = (np.nanmin(ww) < -1.0) and (np.nanmax(ww) > -1.0)
    zc = np.nan
    if crossing:
        zz = z[m]; idx = np.where(np.diff(np.sign(ww + 1.0)))[0]
        if len(idx): zc = zz[idx[0]]
    return dict(w0=w0, wa=wa, crossing=crossing, zc=zc, w=w, z=z, ODE=ODE, ok=ok,
                rho_de_min=float(np.nanmin(ODE)) if np.any(np.isfinite(ODE)) else float('nan'))

print("="*70)
print("JALON B — w(z) dérivé du couplage non minimal torsion-courbure")
print("="*70)
print("Contrôle xi=0 (doit redonner le verdict P0 : w = -1 exact) :")
d0 = diagnose(0.0, 0.0)
print(f"   w0 = {d0['w0']:+.6f}   (attendu -1.000000)  -> "
      f"{'OK' if abs(d0['w0']+1)<1e-6 else 'ECHEC'}\n")

print("Balayage (eps, delta) :")
print(f"{'eps':>8} {'delta':>8} | {'w0':>9} {'wa':>9} | franchit -1 ?")
print("-"*54)
best = None
n_conv = n_div = 0
for eps in [-0.3, -0.1, -0.03, -0.01, 0.01, 0.03, 0.1, 0.3]:
    for delta in [-0.05, -0.01, 0.0, 0.01, 0.05]:
        d = diagnose(eps, delta)
        if not d['ok']:
            n_div += 1
            print(f"{eps:>8.3f} {delta:>8.3f} | {'--':>9} {'--':>9} | NOT CONVERGED / diverged (excluded)")
            continue
        n_conv += 1
        tag = f"OUI (z={d['zc']:.2f})" if d['crossing'] else "non"
        neg = "  [rho_DE<0 in the past: min=%.2e]" % d['rho_de_min'] if d['rho_de_min'] < 0 else ""
        print(f"{eps:>8.3f} {delta:>8.3f} | {d['w0']:>+9.4f} {d['wa']:>+9.4f} | {tag}{neg}")
        err = (d['w0']-W0_T)**2 + (d['wa']-WA_T)**2
        if best is None or err < best[0]: best = (err, eps, delta, d)

print("-"*54)
print(f"Convergence report: {n_conv} converged, {n_div} diverged / not converged, out of {n_conv+n_div} grid points.")
err, eps_b, delta_b, db = best
print(f"Meilleur ajustement de (w0,wa)=({W0_T},{WA_T}) :")
print(f"   eps={eps_b:+.3f}, delta={delta_b:+.3f}  ->  w0={db['w0']:+.4f}, wa={db['wa']:+.4f}")
print(f"   franchissement de -1 : {'OUI' if db['crossing'] else 'NON'}")

# ---- figure comparative ----
zc = np.linspace(0, 2.5, 400); ac = 1/(1+zc)
w_cpl = W0_T + WA_T*(1-ac)
plt.figure(figsize=(7.4,4.7))
plt.axhline(-1, ls='--', c='gray', lw=1.3, label='w = -1')
plt.plot(zc, w_cpl, c='#1f3b66', lw=2.0, label='cible calibrée (CPL, Foundation I)')
m = (db['z']>=0)&(db['z']<=2.5)
plt.plot(db['z'][m], db['w'][m], c='crimson', lw=2.0,
         label=f'dérivé du couplage (eps={eps_b:+.2f}, delta={delta_b:+.2f})')
plt.xlabel("décalage vers le rouge z"); plt.ylabel("w")
plt.title("Jalon B — w(z) dérivé vs w(z) calibré")
plt.legend(fontsize=8.5); plt.tight_layout()
# [CORRIGE 15/09/2026] Sortie deplacee vers _generated/ : cette courbe est
# un diagnostic du solveur, pas une figure du papier. Elle n'est citee par
# aucun document et n'a pas sa place dans figures_output, que la
# centralisation reserve aux figures publiees. _generated/ est exclu du
# balayage depuis ce matin, pour la meme raison que les frames d'animation.
_DIAG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_generated")
os.makedirs(_DIAG, exist_ok=True)
plt.savefig(os.path.join(_DIAG, "ECF_solver_JalonB_wz.png"), dpi=130)
print("\nFigure : ECF_solver_JalonB_wz.png")
print("="*70)
